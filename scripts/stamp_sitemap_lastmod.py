#!/usr/bin/env python3
"""把 <lastmod> 蓋回建置好的 sitemap.xml，日期取該網址對應原始檔的 git commit 日期。

為什麼需要這支：
    本站用 GitHub 官方的 actions/jekyll-build-pages 建置，插件受 GitHub Pages 白名單限制，
    裝不了 jekyll-last-modified-at。而 jekyll-sitemap 只給有 date／last_modified_at 的頁 lastmod，
    首頁、about、方法論這類固定頁都沒有；沒有 front matter 的靜態檔則給建置當下的時間。
    沒有 lastmod，Google 就沒有「這一頁變了」的訊號，seo-ops 每天的 sitemap 過期重送判準
    也只剩「網址數有沒有變」——改寫既有頁面永遠不會觸發，GSC 會一直停在很久以前的那次檢索。
    線上現況用母 repo 的 .claude/check_sitemap_lastmod.py 查。

為什麼取 git commit 日期而不是建置時間：
    用建置時間的話，每次 build 都等於宣稱全站更新，那是假訊號，比沒有 lastmod 更糟
    （見 seo-ops doctrine 的 sitemap 段）。

⚠️ CI 的 checkout 必須是 fetch-depth: 0。淺 clone 只有一個 commit，所有檔案的日期會一樣。

壞資料處理：查不到原始檔或查不到 commit 日期的網址，保留它原本的樣子（有 lastmod 就留著，
沒有就不加），逐筆印出來，不中斷整批。
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def slug(name: str) -> str:
    """Jekyll 的 :name 會把底線變連字號並轉小寫。

    ⚠️ 不要反過來拿網址猜檔名。`bempedoic-acid` 的原始檔是 `bempedoic_acid.md`，
    但同一個集合裡也有本來就帶連字號的 `dl-alpha-tocopherol.md`——反推會兩邊都猜錯。
    正確做法是把集合目錄整個掃一遍、用同一支 slug 建索引再查。
    """
    return name.replace("_", "-").lower()


_collection_index: dict[str, dict[str, Path]] = {}


def collection_lookup(docs: Path, collection: str, name: str) -> Path | None:
    idx = _collection_index.get(collection)
    if idx is None:
        idx = {}
        d = docs / f"_{collection}"
        if d.is_dir():
            for f in d.iterdir():
                if f.suffix in (".md", ".html", ".markdown"):
                    idx.setdefault(slug(f.stem), f)
        _collection_index[collection] = idx
    return idx.get(slug(name))


_permalink_index: dict[Path, dict[str, Path]] = {}
_PERMALINK_RE = re.compile(r"\A﻿?---\r?\n(?:.*?\r?\n)??permalink:\s*[\"']?([^\"'\r\n]+?)[\"']?\s*\r?\n", re.S)
_SKIP_DIRS = {"_site", ".jekyll-cache", "vendor", "node_modules", ".bundle"}


def permalink_lookup(docs: Path, p: str) -> Path | None:
    """front matter 寫了 permalink 的頁，以它為準。

    檔名跟網址不一定一樣：導覽頁 nav-safety.md 的 permalink 是 /safety/，
    My 站 nav-help.md 是 /bantuan/。只靠檔名猜會對不到，甚至對到同名的別頁。
    含 :name 這類變數的 permalink 不是單一網址，略過。
    """
    idx = _permalink_index.get(docs)
    if idx is None:
        idx = {}
        for f in sorted(docs.rglob("*")):
            if f.suffix not in (".md", ".html", ".markdown") or not f.is_file():
                continue
            if _SKIP_DIRS.intersection(f.relative_to(docs).parts):
                continue
            try:
                head = f.read_text(encoding="utf-8", errors="replace")[:2000]
            except OSError:
                continue
            fm_end = head.find("\n---", 3)
            m = _PERMALINK_RE.match(head[: fm_end + 1] if fm_end > 0 else "")
            if m and ":" not in m.group(1):
                idx.setdefault(m.group(1).strip().strip("/"), f)
        _permalink_index[docs] = idx
    return idx.get(p)


def source_for(url_path: str, docs: Path) -> Path | None:
    """網址路徑 → Jekyll 原始檔。找不到回 None。

    先看 front matter 的 permalink；沒有的話照 docs/_config.yml 的規則猜：
    頂層 .md 走 permalink /:name/，集合 drugs／news 走 /drugs/:name/、/news/:name/。
    """
    p = url_path.strip("/")
    hit = permalink_lookup(docs, p) if p else None
    if hit is not None:
        return hit
    if not p:
        for c in ("index.md", "index.html"):
            if (docs / c).is_file():
                return docs / c
        return None

    # docs / p：沒有 front matter 的靜態檔（/smart/app.html）。jekyll-sitemap 給這類檔的 lastmod
    # 是建置當下的檔案時間，每次部署都變成「今天」，等於假訊號，要換成 git 日期。
    candidates = [docs / p, docs / f"{p}.md", docs / f"{p}.html", docs / p / "index.md", docs / p / "index.html"]
    # 站上有一批直接輸出 .html 的頁（/smart/api-spec.html），原始檔是同名 .md。
    if p.endswith(".html"):
        stem = p[: -len(".html")]
        candidates += [docs / f"{stem}.md", docs / f"{stem}.markdown"]
    for c in candidates:
        if c.is_file():
            return c
    parts = p.split("/")
    if len(parts) == 2:
        # 集合：/drugs/temozolomide/ → docs/_drugs/temozolomide.md（檔名可能用底線）
        hit = collection_lookup(docs, parts[0], parts[1])
        if hit is not None:
            return hit
    return None


def commit_date(path: Path, repo: Path) -> str | None:
    # 2026-10-17：藥物頁 front matter 有 last_modified_at（內文實際最後變動日，排除只改 front matter 的批次提交）就用它，
    # 否則 2026-10-16 這類全站維護提交會讓所有頁的 lastmod 變成同一天。
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        head = text[:2000]
        if head.startswith("---"):
            m = re.search(r"^last_modified_at:\s*(\d{4}-\d{2}-\d{2})", head, re.M)
            if m:
                return m.group(1)
    except OSError:
        text = ""
    own = _git_commit_date(path, repo)
    deps = _liquid_dependency_dates(text, repo)
    return max([d for d in [own, *deps] if d], default=None)


# 2026-11-03：列表頁（evidence-high／-medium／-low、known-uses、drugs、news、nav-drugs）的內容是 Liquid 從
# site.drugs／site.news 的 front matter 即時組出來的，原始檔本身多半幾個月沒動。只看原始檔的 git 日期，
# evidence-high／-medium 的 lastmod 停在 2026-03-04、evidence-low 停在 10-17，但頁上列的藥物名單在 10-21、10-28、10-29 都改過——Google 不會知道要回來重爬。
# 這裡只把「會出現在列表上的欄位」（標題、證據等級、適應症數、noindex、轉址、網址）的變動算進來，
# 藥物頁內文改了（許可證張數等）不算，免得每週排程都讓列表頁假裝更新。
_LISTING_FIELDS = r"^(title|evidence_level|indication_count|noindex|layout|permalink|nav_exclude|sitemap):"
_listing_cache: dict[str, str | None] = {}


def _liquid_dependency_dates(text: str, repo: Path) -> list[str | None]:
    out: list[str | None] = []
    for coll in sorted(set(re.findall(r"\bsite\.(drugs|news)\b", text))):
        if coll not in _listing_cache:
            try:
                r = subprocess.run(
                    ["git", "log", "-1", "--format=%cs", f"-G{_LISTING_FIELDS}", "--", f"docs/_{coll}"],
                    cwd=repo, capture_output=True, text=True, timeout=120,
                )
                _listing_cache[coll] = r.stdout.strip() or None
            except (subprocess.SubprocessError, OSError):
                _listing_cache[coll] = None
        out.append(_listing_cache[coll])
    # site.data.X → docs/_data/X.{yml,json,…} 的 git 日期（首頁、drugs 頁的藥物數與等級分布）
    for name in sorted(set(re.findall(r"\bsite\.data\.(\w+)", text))):
        for f in sorted((repo / "docs" / "_data").glob(f"{name}.*")):
            out.append(_git_commit_date(f, repo))
    return out


def _git_commit_date(path: Path, repo: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path.relative_to(repo))],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    d = out.stdout.strip()
    return d or None


# 2026-11-03：首頁、about、藥物頁、個別新聞頁的 JSON-LD dateModified 原本在 head_custom.html 寫死（2026-03-04），
# 內容改了日期也不變——sitemap 說這頁最近改過，頁上的結構化資料卻還是舊日期，兩個訊號互相矛盾。
# head_custom.html 已改成取 page.last_modified_at，但首頁、about 的內容大多是 Liquid 從 site.data／site.drugs
# 組出來的，front matter 反映不了，所以在這裡把建置好的頁面 JSON-LD 的 dateModified 對齊到上面蓋進 sitemap
# 的 lastmod（同一個日期、同一套算法，不用另外維護清單）。
# 規則：只動 <script type="application/ld+json"> 裡值是純日期（YYYY-MM-DD）的 "dateModified"，
# 只在 lastmod 比現值新時改。有 last_modified_at 的頁（藥物頁、新聞頁）dateModified 與 lastmod 同取該值，不會動；
# jekyll-seo-tag 輸出的帶時間的值不碰。改完重新解析該段 JSON，解析不過就不寫回、列出網址。
_LDJSON_RE = re.compile(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.S)
_DATE_MODIFIED_RE = re.compile(r'("dateModified"\s*:\s*")(\d{4}-\d{2}-\d{2})(")')


def built_html(url_path: str, site_dir: Path) -> Path | None:
    p = unquote(url_path).lstrip("/")
    if not p or p.endswith("/"):
        f = site_dir / p / "index.html"
    else:
        f = site_dir / p
        if not f.suffix:
            f = site_dir / f"{p}.html"
    return f if f.suffix == ".html" and f.is_file() else None


def sync_jsonld_date_modified(site_dir: Path, page_dates: dict[str, str]) -> tuple[list[str], list[str]]:
    changed: list[str] = []
    bad_json: list[str] = []
    for loc, date in page_dates.items():
        f = built_html(urlparse(loc).path, site_dir)
        if f is None:
            continue
        html = f.read_text(encoding="utf-8")
        if '"dateModified"' not in html:
            continue

        def fix_block(m: re.Match) -> str:
            body = m.group(2)
            new = _DATE_MODIFIED_RE.sub(
                lambda d: d.group(1) + date + d.group(3) if d.group(2) < date else d.group(0), body)
            if new == body:
                return m.group(0)
            try:
                json.loads(new)
            except ValueError:
                bad_json.append(loc)
                return m.group(0)
            return m.group(1) + new + m.group(3)

        new_html = _LDJSON_RE.sub(fix_block, html)
        if new_html != html:
            f.write_text(new_html, encoding="utf-8")
            changed.append(loc)
    return changed, bad_json


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    sitemap = Path(sys.argv[1]) if len(sys.argv) > 1 else repo / "_site" / "sitemap.xml"
    docs = repo / "docs"
    if not sitemap.is_file():
        print(f"[lastmod] 找不到 {sitemap}，略過（不擋建置）")
        return 0

    ET.register_namespace("", NS)
    tree = ET.parse(sitemap)
    root = tree.getroot()

    stamped = kept = 0
    page_dates: dict[str, str] = {}
    unresolved: list[str] = []
    for url_el in root.findall(f"{{{NS}}}url"):
        loc_el = url_el.find(f"{{{NS}}}loc")
        if loc_el is None or not loc_el.text:
            continue
        # ⚠️ 一定要 unquote：中文檔名的網址是百分號編碼的（/news/%E8%85%AB%E7%98%A4/
        # ＝ /news/腫瘤/），不解碼就永遠對不到 docs/_news/腫瘤.md。
        src = source_for(unquote(urlparse(loc_el.text).path), docs)
        date = commit_date(src, repo) if src else None
        if not date:
            existing = url_el.find(f"{{{NS}}}lastmod")
            # jekyll-sitemap 已經給了日期的（_posts 走 front matter 的 date）不算問題。
            if existing is None or not (existing.text or "").strip():
                unresolved.append(loc_el.text)
            kept += 1
            continue
        lastmod_el = url_el.find(f"{{{NS}}}lastmod")
        if lastmod_el is None:
            lastmod_el = ET.SubElement(url_el, f"{{{NS}}}lastmod")
        lastmod_el.text = date
        page_dates[loc_el.text] = date
        stamped += 1

    tree.write(sitemap, encoding="UTF-8", xml_declaration=True)
    changed, bad_json = sync_jsonld_date_modified(sitemap.parent, page_dates)
    print(f"[lastmod] JSON-LD dateModified 對齊 sitemap lastmod：{len(changed)} 頁"
          + (f"（{'、'.join(urlparse(u).path for u in changed[:5])}{' …' if len(changed) > 5 else ''}）" if changed else ""))
    if bad_json:
        print(f"[lastmod] ⚠️ 這些頁的 JSON-LD 改完解析不過，沒寫回：{bad_json[:10]}")
    total = stamped + kept
    print(f"[lastmod] {sitemap.name}：{total} 個網址，蓋上 git 日期 {stamped}，保留原樣 {kept}"
          f"（其中 {kept - len(unresolved)} 個原本就有 lastmod）")
    if unresolved:
        print("[lastmod] ⚠️ 查不到原始檔或 commit 日期，且原本也沒有 lastmod（保留原樣，不中斷）：")
        for u in unresolved[:20]:
            print(f"    - {u}")
        if len(unresolved) > 20:
            print(f"    …等共 {len(unresolved)} 筆")
    return 0


if __name__ == "__main__":
    # sitemap 蓋不上 lastmod **不該**擋住整個站的部署——沒有 lastmod 只是 SEO 訊號變弱，
    # 部署不出去是整站停更。但也不能安靜地失敗，否則哪天壞掉沒人知道，又回到大部分網址沒有 lastmod 的狀態。
    # 折衷：吞掉例外回 0，同時輸出 GitHub Actions 的 ::warning:: 註記，會出現在 run 摘要上。
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 —— 這裡就是要攔全部
        print(f"::warning title=sitemap lastmod 沒蓋成::{type(exc).__name__}: {exc}")
        print("[lastmod] 未中斷部署，但這次的 sitemap 沒有 git 日期，請看上面的錯誤。")
        raise SystemExit(0) from None
