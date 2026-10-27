#!/usr/bin/env python3
"""docs 的 SEO 結構守門 —— 給 seo-ops 反思／大腦的自動改動當 gate。

由 TwTxGNN 的 scripts/check_seo_docs.py 移植（2026-10-15，母專案 .claude/seo_templates/）。
主機上沒有 ruby／bundler／jekyll，只能用 Python 標準函式庫檢查「scope 改壞了卻不會有畫面症狀」的事：

  1. 關鍵 permalink 還在（改掉或刪掉 permalink＝該網址靜默 404）。
  2. llms.txt／llms-full.txt 列的自站網址都對得上實際 permalink（AI 引用的入口清單）。
  3. head_custom.html 的 GA4 評量 ID 還在、script 標籤成對、每個 ld+json 區塊仍是合法 JSON
     （Liquid 輸出 {{ … }} 先代換成 0 再解析；結構化資料壞掉不影響版面，只會讓 rich result 消失）。
  4. docs/*.md 的站內連結指到存在的 permalink、redirect_from 或實際檔案。
     permalink 含 collection 文件（_drugs/、_news/）：照 _config.yml 的 permalink 樣板
     （:name／:slug／:title）＋Jekyll slugify 推導。

Tw 專屬的檢查（TFDA 許可證表、docs/_data/drug_reviews.json 人工查核紀錄、drug_stats.json）沒有移植；
本站之後若建立同類機制，再把對應檢查加回來。

用法：python3 scripts/check_seo_docs.py      # 非零＝不通過
"""
import json
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
GA4_ID = "G-W7ZNBYKJHJ"
SITE = "https://" + (DOCS / "CNAME").read_text(encoding="utf-8").strip()

# llms.txt 對外宣告的入口；只列本站實際存在的頁（移植時依 docs/*.md 實查）
CRITICAL = [p for p, f in [("/", "index.md"), ("/drugs/", "drugs.md"), ("/methodology/", "methodology.md"),
                           ("/guide/", "guide.md"), ("/sources/", "sources.md"), ("/downloads/", "downloads.md"),
                           ("/about/", "about.md"), ("/news/", "news.md"), ("/evidence-high/", "evidence-high.md"),
                           ("/evidence-medium/", "evidence-medium.md"), ("/evidence-low/", "evidence-low.md")]
            if (DOCS / f).exists()]

errors = []

# 主機 clone 只有進版控的檔案：本機有、但被 .gitignore 排除的檔案上線會 404（2026-10-15 Th 的 docs/downloads/ 就是這樣漏掉）。
# 有 git 時以 git ls-files 為準，沒有 git 時退回檢查磁碟。
try:
    import subprocess
    _ls = subprocess.run(["git", "ls-files", "-z", "--", "."], cwd=DOCS, capture_output=True, check=True).stdout
    TRACKED = {x.decode("utf-8") for x in _ls.split(b"\0") if x}
except Exception:
    TRACKED = None


def file_exists(rel):
    rel = rel.lstrip("/")
    if TRACKED is None:
        return (DOCS / rel).exists()
    return rel in TRACKED or any(t.startswith(rel.rstrip("/") + "/") for t in TRACKED)


def front_block(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    return text[3:end] if end >= 0 else None


def redirect_paths(text):
    """front matter 的 redirect_from 清單（jekyll-redirect-from 產的舊網址）。"""
    block = front_block(text)
    if block is None:
        return []
    out, collecting = [], False
    for line in block.splitlines():
        if re.match(r"^redirect_from:\s*$", line):
            collecting = True
            continue
        if collecting:
            m = re.match(r"^\s*-\s*(\S+)\s*$", line)
            if m:
                out.append(m.group(1).strip('"').strip("'"))
                continue
            collecting = False
        m = re.match(r"^redirect_from:\s*(\S+)\s*$", line)
        if m:
            out.append(m.group(1).strip('"').strip("'"))
    return out


def front_matter(text):
    block = front_block(text)
    out = {}
    for line in (block or "").splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return out


def norm(p):
    return "/" if p in ("", "/") else p.rstrip("/") + "/"


# 收集全站 permalink（index.md 沒寫 permalink 時就是 /）
permalinks = {"/"} if (DOCS / "index.md").exists() else set()
redirects = set()
for md in DOCS.rglob("*.md"):
    if any(part.startswith(("_site", "vendor", "node_modules")) for part in md.relative_to(DOCS).parts):
        continue
    text = md.read_text(encoding="utf-8", errors="replace")
    fm = front_matter(text)
    if fm.get("permalink"):
        permalinks.add(norm(fm["permalink"]))
    elif md.parent == DOCS and md.stem != "index" and front_block(text) is not None:
        permalinks.add(f"/{md.stem}/")  # 未寫 permalink 的頂層頁：just-the-docs 預設 /<檔名>/（_config 無 permalink: pretty 時為 .html，兩者都收）
        permalinks.add(f"/{md.stem}.html/")
    redirects.update(redirect_paths(text))


def jekyll_slugify(s):
    """Jekyll Utils.slugify 預設模式：非英數（含底線）連成一個 '-'、去頭尾 '-'、轉小寫。"""
    return re.sub(r"[\W_]+", "-", s).strip("-").lower()


def collection_rules():
    """從 _config.yml 的 collections: 區塊讀 {名稱: permalink 樣板}，只取 output: true 的。"""
    cfg = DOCS / "_config.yml"
    if not cfg.exists():
        return {}
    rules, cur, inside = {}, None, False
    for line in cfg.read_text(encoding="utf-8", errors="replace").splitlines():
        if re.match(r"^collections:\s*$", line):
            inside = True
            continue
        if not inside:
            continue
        if line.strip() == "" or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            break
        m = re.match(r"^  ([A-Za-z_][\w-]*):\s*$", line)
        if m:
            cur = m.group(1)
            rules[cur] = {}
            continue
        m = re.match(r"^\s{4,}(output|permalink):\s*(\S+)\s*$", line)
        if m and cur:
            rules[cur][m.group(1)] = m.group(2).strip('"').strip("'")
    return {k: v["permalink"] for k, v in rules.items()
            if v.get("output") == "true" and v.get("permalink")}


for cname, pattern in collection_rules().items():
    if re.search(r":(?!(name|slug|title)\b)\w+", pattern):
        errors.append(f"_config.yml collection {cname} 的 permalink {pattern} 含本 gate 不認得的變數（只支援 :name／:slug／:title），請擴充 check_seo_docs.py")
        continue
    for f in (DOCS / f"_{cname}").glob("*"):
        if f.suffix not in (".md", ".markdown", ".html"):
            continue
        fm = front_matter(f.read_text(encoding="utf-8", errors="replace"))
        if fm.get("permalink"):
            continue
        slug = jekyll_slugify(fm.get("slug") or f.stem)
        url = re.sub(r":(name|slug|title)\b", slug, pattern)
        permalinks.add(norm(url))

# 1) 關鍵 permalink
for p in CRITICAL:
    if p not in permalinks:
        errors.append(f"關鍵 permalink 消失：{p}（llms.txt 與導覽都指向它）")

# 2) llms.txt 內的自站網址
for name in ("llms.txt", "llms-full.txt"):
    f = DOCS / name
    if not f.exists():
        errors.append(f"{name} 不存在（AI 引用入口清單）")
        continue
    for url in re.findall(r"https?://[^\s)\]>`]+", f.read_text(encoding="utf-8", errors="replace")):
        if not url.startswith(SITE):
            continue
        path = url[len(SITE):] or "/"
        path = path.split("#")[0].split("?")[0]
        if path.endswith((".txt", ".xml", ".json")):
            if not file_exists(path) and path != "/sitemap.xml":
                errors.append(f"{name} 指向不存在的檔案：{url}")
            continue
        if norm(path) not in permalinks:
            errors.append(f"{name} 指向不存在的網址：{url}")

# 3) head_custom.html
head = DOCS / "_includes" / "head_custom.html"
if not head.exists():
    errors.append("_includes/head_custom.html 不存在（GA4 與全部結構化資料都在裡面）")
else:
    t = head.read_text(encoding="utf-8", errors="replace")
    if GA4_ID not in t:
        errors.append(f"head_custom.html 不再含 GA4 評量 ID {GA4_ID}（改壞了不會有畫面症狀，數據直接歸零）")
    if t.count("<script") != t.count("</script>"):
        errors.append(f"head_custom.html 的 script 標籤不成對（{t.count('<script')} 開 / {t.count('</script>')} 閉）")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    if not blocks:
        errors.append("head_custom.html 找不到任何 ld+json 區塊（結構化資料全失）")
    for i, b in enumerate(blocks, 1):
        if "{%" in b:
            continue  # 含 Liquid 流程控制的區塊無法離線還原，只檢查不含控制語法的區塊
        try:
            json.loads(re.sub(r"\{\{.*?\}\}", "0", b, flags=re.S))
        except Exception as e:
            errors.append(f"head_custom.html 第 {i} 個 ld+json 不是合法 JSON：{e}")

# 4) docs/*.md 的站內連結
for md in sorted(DOCS.glob("*.md")):
    text = md.read_text(encoding="utf-8", errors="replace")
    for link in re.findall(r"\]\((/[^)\s]*)\)", text):
        path = link.split("#")[0].split("?")[0]
        if not path or path.startswith("/assets/") or "{{" in path:
            continue
        if norm(path) in permalinks or path in redirects or path.rstrip("/") in redirects:
            continue
        if file_exists(path):
            continue
        errors.append(f"{md.name} 的站內連結指不到東西：{link}")

# 5) 日本販売名（2026-10-20，U-03b）：docs/_data/brand_names.json 改了，成分頁區塊與 search-index 的 brands 必須跟著重產
#    （build_brand_names.py → 母目錄 .claude/apply_brand_names.py → .claude/rebuild_search_index.py JpTxGNN）
bm = DOCS / "_data/brand_names.json"
if bm.exists():
    bmap = json.loads(bm.read_text(encoding="utf-8"))
    want = {k: sorted(set(v.get("trade", []) + v.get("hanbai", []) + v.get("combo", []))) for k, v in bmap.items()}
    stale = []
    for md in sorted((DOCS / "_drugs").glob("*.md")):
        t_ = md.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
        if 'http-equiv="refresh"' in t_:
            continue
        m = re.search(r"<!-- brand-names:start -->(.*?)<!-- brand-names:end -->", t_, re.S)
        got = sorted({x for line in (m.group(1) if m else "").splitlines() if "：" in line and line.startswith("**")
                      for x in line.split("：", 1)[1].split("、") if x})
        if got != want.get(md.stem, []):
            stale.append(md.stem)
    if stale:
        errors.append(f"{len(stale)} 個成分頁的販売名區塊與 brand_names.json 不符（例：{', '.join(stale[:5])}），請跑 .claude/apply_brand_names.py JpTxGNN")
    si = DOCS / "data/search-index.json"
    if si.exists():
        idx = json.loads(si.read_text(encoding="utf-8"))
        rows = idx.get("drugs", idx) if isinstance(idx, dict) else idx
        bad = [d.get("slug") for d in rows if isinstance(d, dict) and d.get("slug") and
               sorted(set(d.get("brands") or [])) != want.get(re.sub(r"-", "_", d["slug"]), want.get(d["slug"], []))]
        if bad:
            errors.append(f"search-index.json 有 {len(bad)} 筆 brands 與 brand_names.json 不符（例：{', '.join(map(str, bad[:5]))}），請跑 .claude/rebuild_search_index.py JpTxGNN")

# 5) 寫死的藥物數（2026-10-27 補）：drug_stats.json 要等於公開藥物頁數，
#    不能用 Liquid 的寫死數字要一致、能用 Liquid 的檔不得寫死。規則與修法：scripts/generate_drug_stats.py。
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_drug_stats as _gds  # noqa: E402
_stats_now = json.loads((DOCS / "_data" / "drug_stats.json").read_text(encoding="utf-8"))
_want = _gds.build_stats(_gds.listed_drugs(), _stats_now.get("generated", ""))
if not _gds.same(_stats_now, _want):
    errors.append(f"drug_stats.json total_drugs={_stats_now.get('total_drugs')}，公開藥物頁 {_want['total_drugs']} 頁（跑 scripts/generate_drug_stats.py）")
errors.extend(f"{e}（跑 scripts/generate_drug_stats.py）" for e in _gds.count_spot_problems(_want) + _gds.hardcode_problems(_want))

if errors:
    print(f"docs SEO 守門：✗ {len(errors)} 項")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"docs SEO 守門：✓（{len(permalinks)} 個 permalink、{len(CRITICAL)} 個關鍵入口）")
