#!/usr/bin/env python3
"""把 <lastmod> 蓋回建置好的 sitemap.xml，日期取該網址對應原始檔的 git commit 日期。

為什麼需要這支：
    本站用 GitHub 官方的 actions/jekyll-build-pages 建置，插件受 GitHub Pages 白名單限制，
    裝不了 jekyll-last-modified-at。而 jekyll-sitemap 只對有 date 的文件（_posts）產 lastmod，
    於是 521 個網址裡只有 8 個有 lastmod。沒有 lastmod，Google 就沒有「這一頁變了」的訊號，
    seo-ops 每天的 sitemap 過期重送判準也只剩「網址數有沒有變」——改寫既有頁面永遠不會觸發。
    實例：/drugs/ 的 GSC 記錄停在 2026-05-28 的一次 404，線上早就正常，三個月沒被重抓。

為什麼取 git commit 日期而不是建置時間：
    用建置時間的話，每次 build 都等於宣稱全站更新，那是假訊號，比沒有 lastmod 更糟
    （見 seo-ops doctrine 的 sitemap 段）。

⚠️ CI 的 checkout 必須是 fetch-depth: 0。淺 clone 只有一個 commit，所有檔案的日期會一樣。

壞資料處理：查不到原始檔或查不到 commit 日期的網址，保留它原本的樣子（有 lastmod 就留著，
沒有就不加），逐筆印出來，不中斷整批。
"""
from __future__ import annotations

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


def source_for(url_path: str, docs: Path) -> Path | None:
    """網址路徑 → Jekyll 原始檔。找不到回 None。

    對應規則來自 docs/_config.yml：頂層 .md 走 permalink /:name/，
    集合 drugs／news 走 /drugs/:name/、/news/:name/。
    """
    p = url_path.strip("/")
    if not p:
        for c in ("index.md", "index.html"):
            if (docs / c).is_file():
                return docs / c
        return None

    candidates = [docs / f"{p}.md", docs / f"{p}.html", docs / p / "index.md", docs / p / "index.html"]
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
        head = path.read_text(encoding="utf-8", errors="replace")[:2000]
        if head.startswith("---"):
            import re as _re
            m = _re.search(r"^last_modified_at:\s*(\d{4}-\d{2}-\d{2})", head, _re.M)
            if m:
                return m.group(1)
    except OSError:
        pass
    return _git_commit_date(path, repo)


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
        stamped += 1

    tree.write(sitemap, encoding="UTF-8", xml_declaration=True)
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
    # 部署不出去是整站停更。但也不能安靜地失敗，否則哪天壞掉沒人知道，又回到 8/521 的狀態。
    # 折衷：吞掉例外回 0，同時輸出 GitHub Actions 的 ::warning:: 註記，會出現在 run 摘要上。
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 —— 這裡就是要攔全部
        print(f"::warning title=sitemap lastmod 沒蓋成::{type(exc).__name__}: {exc}")
        print("[lastmod] 未中斷部署，但這次的 sitemap 沒有 git 日期，請看上面的錯誤。")
        raise SystemExit(0) from None
