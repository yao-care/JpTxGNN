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
  5. 日本販売名區塊與 search-index 的 brands 跟 docs/_data/brand_names.json 一致；docs/_data/drug_stats.json 與寫死的藥物數一致（scripts/generate_drug_stats.py）。
  6. Markdown 表格前後有空行（2026-11-03；缺空行 kramdown 會把整張表排成純文字，scripts/fix_table_spacing.py 修）。
  7. docs/nav-*.md、evidence-*.md、drugs.md 不寫死該由 drug_stats.json 來的藥物總數、等級分布條寬度、等級藥物數（2026-11-03）。
  8. llms.txt／llms-full.txt 範例藥物行「名稱 (Lx): 網址」的標籤＝藥物頁 evidence_level，且不指向轉址／noindex／不存在的頁（2026-11-03）。
  9. llms.txt／llms-full.txt 的本站資料區塊（site-data）剛好一個、等級分布＝drug_stats.json、資料集網址出現在本站 sources 頁（2026-11-04）。
  10. docs/_data/hreflang.json 裡本站自己的頁（說明頁等，藥物頁除外）存在、不是 noindex／轉址頁、組裡有自我參照、沒有 x-default（2026-11-04）。
  12. docs/data/drugs.json 等於公開藥物頁：不含 noindex／轉址頁、等級＝頁首、筆數＝drug_stats.json total_drugs、original_indication 不是預測說明或截斷的句子、predicted_indication／txgnn_score 不是表頭字或預測說明（2026-11-06）。
  13. 藥物頁 front matter description 的證據等級字樣＝頁首 evidence_level（母目錄 .claude/sync_description_levels.py，2026-11-06）。
  14. FHIR：MedicationKnowledge 等級＝藥物頁頁首、不含 noindex 藥物頁的藥，Bundle／summary／index／metadata 的數字＝實際檔數（母目錄 .claude/sync_fhir_levels.py，2026-11-06）。
  15. FHIR metadata（docs/fhir/metadata*）的在地欄位：jurisdiction 國碼＝本站 ISO 3166-1 alpha-2、不出現別站國名／代號、網址在本站網域、非中日文站不含漢字（2026-11-06）。
  16. docs/fhir 所有檔的 jurisdiction 國碼＝本站、含 txgnn／github.io 的網址在本站網域；metadata 與 metadata.json 內容相同、只宣稱 read（2026-11-06）。
  17. docs/_data/drug_reviews.json 的查核紀錄（更正／加註／待重審／重審結果）都還套在藥物頁上
      （頁面被產線或排程改寫會蓋掉；修法：python3 scripts/apply_drug_reviews.py）（2026-11-12，本站查核機制）。
  18. 藥物頁的許可證資訊＝snapshots/jp_licenses.json.gz：市場段落表格的許可證號屬於本藥、狀態列與張數列＝事實層寫法、
      表格列狀態不跟事實相反（src/jptxgnn/regulatory/licenses.py）（2026-11-12）。
  19. 藥物頁頁首等級＝快速總覽等級格的等級（規則見 src/jptxgnn/regulatory/site.py 的 HEADER_RULE；主預測撤回時為其他預測表最高
      等級或 N/A），parent 對應列表頁（src/jptxgnn/regulatory/page_format.py）（2026-11-12）。
  20. 查核紀錄裡重審撤回（verdict=withdraw）的預測，不出現在 search-index.json、FHIR ClinicalUseDefinition、
      證據監測清單 scripts/drug_list.json（src/jptxgnn/regulatory/withdrawn.py）（2026-11-12）。

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
errors.extend(f"{e}（跑 scripts/generate_drug_stats.py）" for e in _gds.count_spot_problems(_want) + _gds.index_date_problems(_want) + _gds.hardcode_problems(_want))

# 6) 表格前後缺空行（2026-11-03 補）：kramdown 會把整張表排成純文字（線上出現 `| 欄 | 欄 | |---|---|`）。
#    修法：python3 scripts/fix_table_spacing.py（只補空行，不改字）。
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fix_table_spacing as _fts  # noqa: E402
for _f in _fts.targets():
    _n = len(_fts.problems(_f.read_bytes().decode("utf-8", errors="replace")))
    if _n:
        errors.append(f"{_f.relative_to(DOCS)}：{_n} 處表格前後缺空行，會被排成純文字（跑 scripts/fix_table_spacing.py）")

# 7) 導覽頁與等級列表頁不得寫死該由 docs/_data/drug_stats.json 來的數字（2026-11-03 補）：
#    docs/nav-*.md 的藥物／報告總數、等級分布條（dist-high／dist-medium／dist-low）的寬度、等級卡片的藥物數，
#    以及 nav-*.md、evidence-*.md、drugs.md 等級表（| L1-L2 | 數字 |）的藥物數。nav-*.md 曾被自動化層寫入
#    寫死的數字後過期（MyTxGNN 2026-11-03：寫 799 份、14%／5%／81%，實際 606 份）。
#    修法：內文改用 Liquid 讀 site.data.drug_stats（total_drugs、level_counts，百分比在 Liquid 裡算）；
#    front matter description 不能用 Liquid，不寫數字（非寫不可就列進 scripts/generate_drug_stats.py 的 COUNT_SPOTS 由它同步）。
import generate_drug_stats as _gds_nav  # noqa: E402
_NAV_W = (r"(?:drugs?|medicines?|medications?|ubat|medicamentos?|fármacos?|farmacos?|arzneimittel\w*|lægemidl\w*|"
          r"geneesmiddel\w*|läkemed\w*|legemid\w*|lääk\w*|médicaments?|farmaci|藥物?|药物?|薬|医薬品|약물|의약품|ยา|أدوية|دواء|"
          r"reports?|relatórios?|informes?|rapports?|berichte\w*|rapporter|rapporten|rapporti|laporan|รายงาน|レポート|報告|报告|보고서)")
_NAV_N = r"(?<![A-Za-z\d.,/#:\-])(\d{1,3}(?:[,.]\d{3})+|\d{2,5})(?![A-Za-z\d%.,/])"
_NAV_HARD = re.compile(_NAV_N + r"[^\d\n]{0,12}?" + _NAV_W + "|" + _NAV_W + r"[^\d\n]{0,40}?" + _NAV_N, re.I)
_NAV_MASK = re.compile(r"\{\{.*?\}\}|\{%.*?%\}|<[^>\n]*>|https?://\S+|&#?\w+;", re.S)
_NAV_BAR = re.compile(r"<[^>]*\bdist-(?:high|medium|low|l[1-5])\b[^>]*>", re.I)
_NAV_CARD = re.compile(r'class="drug-card-count">\s*([\d][\d,.]*)\s*<', re.I)
_NAV_LVROW = re.compile(r"^\|\s*\**L[1-5](?:\s*[-–~]\s*L[1-5])?\**\s*\|\s*\**(\d[\d,.]*)\**\s*\|", re.M)
_nav_spots = {}
for _sp in _gds_nav.COUNT_SPOTS:
    _nav_spots.setdefault(_sp[0], []).append(_sp[1])
for _f in sorted(DOCS.glob("nav-*.md")) + sorted(DOCS.glob("evidence-*.md")) + [DOCS / "drugs.md"]:
    if not _f.exists():
        continue
    _t = _f.read_bytes().decode("utf-8", errors="replace")
    _ln = lambda i: _t.count("\n", 0, i) + 1  # noqa: E731
    _bad = []
    for _m in _NAV_BAR.finditer(_t):
        _w = re.search(r"width:\s*([^;\"']+)", _m.group(0))
        if _w and "{{" not in _w.group(1):
            _bad.append(f"{_ln(_m.start())} 行等級分布條寬度寫死 {_w.group(1).strip()}")
    _bad += [f"{_ln(_m.start())} 行等級卡片寫死 {_m.group(1)}" for _m in _NAV_CARD.finditer(_t)]
    _bad += [f"{_ln(_m.start())} 行等級表寫死 {_m.group(1)}" for _m in _NAV_LVROW.finditer(_t)]
    if _f.name.startswith("nav-") and _f.name != "nav-safety.md":  # nav-safety 的數字是 DDInter 等安全性資料集的規模，不是 drug_stats
        _skip = [(_m.start(), _m.end()) for _p in _nav_spots.get(f"docs/{_f.name}", [])
                 for _m in re.finditer(_p, _t, re.M)]  # COUNT_SPOTS 管的位置（腳本同步）不算
        _masked = _NAV_MASK.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), _t)
        for _m in _NAV_HARD.finditer(_masked):
            _num = (_m.group(1) or _m.group(2)).replace(",", "").replace(".", "")
            if int(_num) < 50 or 1990 <= int(_num) <= 2099 or any(a <= _m.start() < b for a, b in _skip):
                continue  # 個位數／每藥前 N 筆之類的小數字、年份不是藥物總數
            _bad.append(f"{_ln(_m.start())} 行寫死的藥物／報告數「{' '.join(_m.group(0).split())}」")
    errors.extend(f"{_f.name}：{b}（改用 site.data.drug_stats 的 Liquid；description 不寫數字）" for b in _bad)

# 8) llms.txt／llms-full.txt 的範例藥物行「- 名稱 (Lx): 網址」（2026-11-03 補）：標籤＝該藥物頁 front matter 的
#    evidence_level，且網址指到存在的藥物頁、不是 ID 轉址頁、不是 noindex 頁（藥物頁重新評級後標籤會過期，
#    NZTxGNN 等站曾發生）。修法：母目錄 python3 .claude/sync_llms_descriptions.py <站> 會依頁面同步標籤；
#    指到轉址／noindex／不存在頁的行要人工換一個藥。
_LLM_LINE = re.compile(r"^\s*[-*]\s*(.+?)\s*\((L[1-5]|N/A)\)\s*:\s*(https?://\S+?)\s*$", re.M)
_llm_pages, _llm_prefix = {}, []
for _cn, _pat in collection_rules().items():
    if _cn != "drugs":
        continue
    _llm_prefix.append(_pat.split(":")[0])
    for _f in (DOCS / "_drugs").glob("*.md"):
        _t = _f.read_text(encoding="utf-8", errors="replace")
        _fm = front_matter(_t)
        _u = _fm.get("permalink") or re.sub(r":(name|slug|title)\b", jekyll_slugify(_fm.get("slug") or _f.stem), _pat)
        _llm_pages[_u.rstrip("/") + "/"] = (_fm, 'http-equiv="refresh"' in _t)
for _name in ("llms.txt", "llms-full.txt"):
    _f = DOCS / _name
    if not _f.exists():
        continue
    for _m in _LLM_LINE.finditer(_f.read_text(encoding="utf-8", errors="replace")):
        _url, _lv = _m.group(3), _m.group(2)
        if not _url.startswith(SITE):
            continue
        _path = (_url[len(SITE):].split("#")[0].split("?")[0] or "/").rstrip("/") + "/"
        if not any(_path.startswith(p) for p in _llm_prefix):
            continue  # 不是藥物頁（如 /evidence-low/ 的等級說明行）
        if _path not in _llm_pages:
            errors.append(f"{_name}：「{_m.group(1)} ({_lv})」指到不存在的藥物頁 {_url}（換一個藥）")
            continue
        _fm, _refresh = _llm_pages[_path]
        if _fm.get("layout") == "id_redirect" or _refresh or _fm.get("redirect_to"):
            errors.append(f"{_name}：「{_m.group(1)} ({_lv})」指到轉址頁 {_url}（換一個藥）")
        elif _fm.get("noindex", "").lower() == "true":
            errors.append(f"{_name}：「{_m.group(1)} ({_lv})」指到 noindex 頁 {_url}（換一個藥）")
        elif _fm.get("evidence_level", "") != _lv:
            errors.append(f"{_name}：「{_m.group(1)} ({_lv})」標籤與頁面 evidence_level {_fm.get('evidence_level') or '（無）'} 不符"
                          f"（跑母目錄 .claude/sync_llms_descriptions.py）")

# 9) llms.txt／llms-full.txt 的「本站資料」區塊（2026-11-04 補）：<!-- site-data:begin … --> 到 <!-- site-data:end -->，
#    每個 llms 檔剛好一個。等級分布行的 L1–L5、N/A 頁數＝docs/_data/drug_stats.json（N/A＝total_drugs 減 L1–L5 總和），
#    並寫出 total_drugs；資料集行的網址都要出現在本站 sources 頁（資料集要有出處，不在 llms 自創來源）。
#    修法：母目錄 python3 .claude/sync_llms_descriptions.py <站>；資料集行改母目錄 .claude/llms_site_data.tsv（先改 sources 頁）。
_SD_BLOCK = re.compile(r"<!-- site-data:begin\b.*?-->(.*?)<!-- site-data:end -->", re.S)
_sd_stats = json.loads((DOCS / "_data" / "drug_stats.json").read_text(encoding="utf-8"))
_sd_total = int(_sd_stats.get("total_drugs") or 0)
_sd_want = {f"L{_i}": int((_sd_stats.get("level_counts") or {}).get(f"L{_i}", 0)) for _i in range(1, 6)}
_sd_want["N/A"] = _sd_total - sum(_sd_want.values())
_sd_src = "\n".join(_p.read_text(encoding="utf-8", errors="replace")
                    for _p in (DOCS / "sources.md", DOCS / "data-sources.md") if _p.exists())
for _name in ("llms.txt", "llms-full.txt"):
    _f = DOCS / _name
    if not _f.exists():
        continue
    _blocks = _SD_BLOCK.findall(_f.read_text(encoding="utf-8", errors="replace"))
    if len(_blocks) != 1:
        errors.append(f"{_name}：本站資料區塊（site-data）應該剛好 1 個，現在 {len(_blocks)} 個"
                      f"（跑母目錄 .claude/sync_llms_descriptions.py）")
        continue
    _got = {_k: int(_v) for _k, _v in re.findall(r"(?<![\w/])(L[1-5]|N/A) (\d+)\b", _blocks[0])}
    if _got != _sd_want or not re.search(rf"(?<![\d.,]){_sd_total}(?![\d.,])", _blocks[0]):
        errors.append(f"{_name}：本站資料區塊的等級分布 {_got} 與 drug_stats.json {_sd_want}（total_drugs {_sd_total}）"
                      f"不符或沒寫出總數（跑母目錄 .claude/sync_llms_descriptions.py）")
    _urls = re.findall(r"https?://[^\s,;<>()（）]+", _blocks[0])
    if not _urls:
        errors.append(f"{_name}：本站資料區塊沒有資料集下載網址（改母目錄 .claude/llms_site_data.tsv）")
    for _u in _urls:
        if _u not in _sd_src:
            errors.append(f"{_name}：本站資料區塊的資料集網址 {_u} 不在本站 sources 頁"
                          f"（先在 sources 頁寫明出處，再改母目錄 .claude/llms_site_data.tsv）")

# 10) hreflang（2026-11-04 補）：docs/_data/hreflang.json 的 pages 裡本站自己的頁（藥物頁 /drugs/<藥>/ 由母目錄
#    .claude/gen_hreflang_20261029.py 管，這裡不查）要對得上存在的 permalink、不是 noindex／轉址頁，組裡要含本站自己
#    （自我參照），而且不得含 x-default（首頁沒有）。說明頁（privacy／methodology／guide／downloads／about）的組由
#    母目錄 .claude/gen_hreflang_pages.py 產生：頁改成 noindex、刪頁或改 permalink 後，在母目錄重跑它（建表＋--apply）。
_HL_F = DOCS / "_data" / "hreflang.json"
if _HL_F.exists():
    _hl = json.loads(_HL_F.read_text(encoding="utf-8"))
    _hl_base = "https://" + (DOCS / "CNAME").read_text(encoding="utf-8").strip()
    _hl_me = [_i for _i, _s in enumerate(_hl.get("sites", [])) if _s[1].rstrip("/") == _hl_base]
    if len(_hl_me) != 1:
        errors.append(f"_data/hreflang.json 的 sites 表找不到本站 {_hl_base}（在母目錄重跑 .claude/gen_hreflang_pages.py --apply）")
    else:
        _hl_pg = {}  # permalink → (front matter 原文, 內文)
        for _f in DOCS.rglob("*"):
            _rel = _f.relative_to(DOCS).parts
            if _f.suffix not in (".md", ".html") or any(_p.startswith(("_", ".")) or _p in ("vendor", "node_modules", "assets") for _p in _rel[:-1]):
                continue
            _t = _f.read_text(encoding="utf-8", errors="replace")
            _m = re.match(r"\A\ufeff?---\r?\n(.*?)\r?\n---\r?\n", _t, re.S)
            if not _m:
                continue
            _pm = re.search(r'^permalink:\s*"?([^"\s]+)"?\s*$', _m.group(1), re.M)
            if _pm:
                _hl_pg["/" + _pm.group(1).strip("/") + "/" if _pm.group(1).strip("/") else "/"] = (_m.group(1), _t[_m.end():])
            elif _f.name == "index.md" and len(_rel) == 1:
                _hl_pg["/"] = (_m.group(1), _t[_m.end():])
        for _k, _alt in _hl.get("pages", {}).items():
            if _k.startswith("/drugs/") and _k != "/drugs/":
                continue
            if _k not in _hl_pg:
                errors.append(f"_data/hreflang.json 列了 {_k}，本站沒有這個 permalink（在母目錄重跑 .claude/gen_hreflang_pages.py）")
                continue
            _fmt, _body = _hl_pg[_k]
            if (re.search(r"^noindex:\s*true\b", _fmt, re.M) or re.search(r"<meta[^>]+name=[\"']robots[\"'][^>]*noindex", _body, re.I)
                    or re.search(r"^(redirect_to:|layout:\s*id_redirect)", _fmt, re.M) or 'http-equiv="refresh"' in _body[:3000]):
                errors.append(f"_data/hreflang.json 列了 {_k}，但本站這頁是 noindex 或轉址頁，不得列入 hreflang（在母目錄重跑 .claude/gen_hreflang_pages.py）")
            if [_hl_me[0], _k] not in _alt:
                errors.append(f"_data/hreflang.json 的 {_k} 組沒有本站自己（自我參照）")
            if any(str(_hl["sites"][_a[0]][0]).lower() == "x-default" for _a in _alt):
                errors.append(f"_data/hreflang.json 的 {_k} 組有 x-default（首頁沒有，不加）")

# 11) DDInter 筆數（2026-11-05 補）：本站的 DDInter 資料是 ddinter_code_*.csv 8 個下載檔，列數與去重後的藥物配對數記在
#    .github/ddi-versions.json 的 site_data（ddinter_rows、ddinter_unique_pairs；重算方式見 site_data.note）。docs、README.md、CITATION.cff 裡提到 DDInter 或 DDI 的那一行（含後面 3 行，涵蓋 HTML
#    表格分行的 <td>）只能寫這兩個數；DDInter 2.0 網站自己公布的總數（ddi-versions.json 的 ddinter.ddi_total_pairs，該區塊 note 寫明是網站統計、不是本站資料）只在同一行寫明「DDInter 2.0」時放行。
_DDI_NUM = re.compile(r"(?<![\d,.])(\d{3})[,.\u00a0\u202f ](\d{3})(?![\d,.]?\d)")
# 2026-11-05：允許值改讀 .github/ddi-versions.json 的 site_data（ddinter_rows、ddinter_unique_pairs），不在這裡寫死
_ddi_ver = json.loads((DOCS.parent / ".github" / "ddi-versions.json").read_text(encoding="utf-8"))
_ddi_sd = _ddi_ver.get("site_data", {})
_DDI_OK = {_ddi_sd[_k] for _k in ("ddinter_rows", "ddinter_unique_pairs") if isinstance(_ddi_sd.get(_k), int)}
# 2026-11-05：DDInter 2.0 網站統計的放行值也改讀 ddi-versions.json（ddinter.ddi_total_pairs），不寫死；原本一併放行的 200,000（別站頁面「200,000+」的概數）本站頁面沒用到，不放行
_DDI_OK20 = {_x for _x in [_ddi_ver.get("ddinter", {}).get("ddi_total_pairs")] if isinstance(_x, int)}
if len(_DDI_OK) != 2:
    errors.append(".github/ddi-versions.json 的 site_data 缺 ddinter_rows 或 ddinter_unique_pairs（DDInter 筆數檢查要用）")
_ddi_files = [_f for _f in DOCS.rglob("*") if _f.suffix in (".md", ".html", ".txt")
              and not any(_p in ("_site", "vendor", "node_modules", ".jekyll-cache") for _p in _f.relative_to(DOCS).parts)]
_ddi_files += [DOCS.parent / "README.md", DOCS.parent / "CITATION.cff"]
for _f in _ddi_files:
    if not _f.is_file():
        continue
    _ls = _f.read_text(encoding="utf-8", errors="replace").splitlines()
    _bad = set()
    for _i, _ln in enumerate(_ls):
        if not re.search(r"DDInter(?!act)|\bDDI\b", _ln):
            continue
        for _j in range(_i, min(_i + 4, len(_ls))):
            for _m in _DDI_NUM.finditer(_ls[_j]):
                _v = int(_m.group(1) + _m.group(2))
                if _v in _DDI_OK or (_v in _DDI_OK20 and "DDInter 2.0" in _ls[_j]):
                    continue
                _bad.add((_j + 1, _m.group(0)))
    for _ln_no, _num in sorted(_bad):
        errors.append(f"{_f.relative_to(DOCS.parent)}:{_ln_no} 寫了 DDInter／DDI 筆數 {_num}：本站資料只能寫 {_ddi_sd.get('ddinter_rows', 0):,}（列數）或 {_ddi_sd.get('ddinter_unique_pairs', 0):,}（去重配對數，見 site_data）")

# 12) docs/data/drugs.json（2026-11-06 補）：新聞排程（scripts/process_news.py、generate_news_keywords.py）讀這份檔取藥物的
#    evidence_level、original_indication，下載頁與部分頁面的 JS 也讀它。它要等於公開藥物頁：不得收 noindex／轉址／
#    不存在的頁，每筆 evidence_level＝該頁 front matter（沒寫時當 L5，同 generate_drug_stats.py），筆數＝drug_stats.json 的 total_drugs，
#    公開藥物頁一個不漏。藥物頁改等級、改 noindex 後這份會過期（2026-11-06 實查時本站這份已過期）。
#    修法：母目錄 python3 .claude/generate_drugs_json.py <本站目錄>（整份重產，只讀 docs/_drugs/*.md 的 front matter）。
_DJ_F = DOCS / "data" / "drugs.json"
if _DJ_F.exists():
    _dj = json.loads(_DJ_F.read_text(encoding="utf-8"))
    _dj_list = _dj.get("drugs", []) if isinstance(_dj, dict) else _dj
    _dj_pat = collection_rules().get("drugs", "/drugs/:name/")
    _dj_pages = {}  # 網址 → (front matter, 是否轉址)
    for _f in sorted((DOCS / "_drugs").glob("*.md")):
        _t = _f.read_text(encoding="utf-8", errors="replace")
        _fm = front_matter(_t)
        _u = _fm.get("permalink") or re.sub(r":(name|slug|title)\b", jekyll_slugify(_fm.get("slug") or _f.stem), _dj_pat)
        _dj_pages[norm(_u)] = (_fm, 'http-equiv="refresh"' in _t or _fm.get("layout") == "id_redirect" or bool(_fm.get("redirect_to")))
    _dj_public = {_u for _u, (_fm, _r) in _dj_pages.items() if not _r and _fm.get("noindex", "").lower() != "true"}
    _dj_bad, _dj_seen = [], set()
    for _e in _dj_list:
        _u = norm(_e.get("url") or f"/drugs/{_e.get('slug', '')}/")
        _dj_seen.add(_u)
        if _u not in _dj_pages:
            _dj_bad.append(f"{_u} 沒有這個藥物頁")
        elif _dj_pages[_u][1]:
            _dj_bad.append(f"{_u} 是轉址頁")
        elif _dj_pages[_u][0].get("noindex", "").lower() == "true":
            _dj_bad.append(f"{_u} 是 noindex 頁")
        elif str(_e.get("evidence_level", "")) != (_dj_pages[_u][0].get("evidence_level") or "L5"):
            _dj_bad.append(f"{_u} 等級 {_e.get('evidence_level')}，頁首 {_dj_pages[_u][0].get('evidence_level') or 'L5'}")
    # original_indication 要是真的原適應症（2026-11-06 補）：以前產生器沒有 front matter 值時從內文抓句子，抓到的全是
    #   預測說明（「he TxGNN model predicts it may be effective for …」）或其他段落，還在 200 字處截成「...」，新聞頁把它當原適應症顯示。
    _DJ_OI_BAD = re.compile(r"predict|may be effective|TxGNN|top-ranked|模型預測|模型预测|預測適應症|预测适应症", re.I)
    for _e in _dj_list:
        _oi = str(_e.get("original_indication") or "").strip()
        if _oi and (_DJ_OI_BAD.search(_oi) or _oi.endswith(("...", "…"))):
            _dj_bad.append(f"{norm(_e.get('url') or '/drugs/' + str(_e.get('slug', '')) + '/')} original_indication 是預測說明或截斷的句子：{_oi[:40]}")
    # predicted_indication、txgnn_score（2026-11-06 補）：產生器以前用 regex 從內文抓預測表第一列與分數，有值的多半是表頭字
    #   （「預測適應症」「Predicted Indication」「Forudsagt indikation」「Sykdom」…）。用戶決定這兩欄留空（欄位保留）；
    #   有值時不得等於本站藥物頁任何表格的表頭字或粗體列名，不得含預測說明字樣，txgnn_score 只能是數字（0–1 或百分比）。
    _DJ_SEP = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
    _DJ_HDR = set()
    for _f in sorted((DOCS / "_drugs").glob("*.md")):
        _ls = _f.read_text(encoding="utf-8", errors="replace").splitlines()
        for _i, _l in enumerate(_ls):
            if _i and "|" in _ls[_i - 1] and _DJ_SEP.match(_l):
                _DJ_HDR |= {_c.strip(" *_`").casefold() for _c in _ls[_i - 1].strip().strip("|").split("|") if _c.strip(" *_`")}
            _m = re.match(r"^\s*\|\s*\*\*([^|*]+)\*\*\s*\|", _l)
            if _m:
                _DJ_HDR.add(_m.group(1).strip().casefold())
    _DJ_PRED_BAD = re.compile(r"predict|prédi|predic|vorhergesagt|forudsag|voorspeld|ennust|förutsag|predikert|予測|예측|預測|预测"
                              r"|may be effective|TxGNN|top-ranked|score|分數|分数|スコア|점수", re.I)
    for _e in _dj_list:
        _du = norm(_e.get("url") or "/drugs/" + str(_e.get("slug", "")) + "/")
        for _k in ("predicted_indication", "txgnn_score"):
            _v = str(_e.get(_k) if _e.get(_k) is not None else "").strip()
            if not _v:
                continue
            if _v.strip(" *_`").casefold() in _DJ_HDR or _DJ_PRED_BAD.search(_v):
                _dj_bad.append(f"{_du} {_k} 是表頭字或預測說明：{_v[:40]}")
            elif _k == "txgnn_score" and not re.fullmatch(r"(0(\.\d+)?|1(\.0+)?|\d{1,3}(\.\d+)?\s*%)", _v):
                _dj_bad.append(f"{_du} txgnn_score 不是分數：{_v[:40]}")
    _dj_bad += [f"{_u} 是公開藥物頁但不在 drugs.json" for _u in sorted(_dj_public - _dj_seen)]
    _dj_total = json.loads((DOCS / "_data" / "drug_stats.json").read_text(encoding="utf-8")).get("total_drugs")
    if len(_dj_list) != _dj_total or (isinstance(_dj, dict) and _dj.get("total_count", len(_dj_list)) != len(_dj_list)):
        _dj_bad.insert(0, f"筆數 {len(_dj_list)}（total_count {_dj.get('total_count') if isinstance(_dj, dict) else '—'}），"
                          f"drug_stats.json total_drugs {_dj_total}")
    if _dj_bad:
        errors.append(f"docs/data/drugs.json 與藥物頁不一致 {len(_dj_bad)} 項，例：{'；'.join(_dj_bad[:5])}"
                      f"（母目錄跑 python3 .claude/generate_drugs_json.py <本站目錄>）")

# 13) 藥物頁 front matter description 的證據等級字樣＝頁首 evidence_level（2026-11-06 補）：description 裡「等級標籤＋Lx」
#    （evidence level L4、nivel de evidencia L4、證據等級 L4…）要等於該頁 evidence_level；頁首 N/A 的頁不得寫 Lx。
#    Sg 的 abacavir 曾寫 L4、頁首 L5。修法：母目錄 python3 .claude/sync_description_levels.py <本站> --apply
#    （只換等級字樣，改動記在 docs/_data/description_level_log.json）；N/A 頁要人工改寫。
_LV_LABELS = ("evidence level", "nivel de evidencia", "nível de evidência", "Evidenzstufe", "evidensniveau", "näytön taso",
              "niveau de preuve", "證據等級", "livello di evidenza", "エビデンスレベル", "근거 수준", "tahap bukti", "evidensnivå",
              "bewijsniveau", "مستوى الدليل", "ระดับหลักฐาน")
_LV_TOK = re.compile(r"(?:" + "|".join(re.escape(_x) for _x in _LV_LABELS) + r")\s*(L[1-5])(?![0-9])", re.I)


def _lv_val(_block, _key):
    _m = re.search(rf"^{_key}:[ \t]*(.*)$", _block, re.M)
    return _m.group(1).strip().strip("\"'") if _m else ""


_LV_PAGES = {}  # 檔名 → 頁面資訊
for _f in sorted((DOCS / "_drugs").glob("*.md")):
    _t = _f.read_text(encoding="utf-8", errors="replace")
    _e = _t.find("\n---", 3) if _t.startswith("---") else -1
    _b = _t[3:_e] if _e >= 0 else ""
    _pm = re.search(r"^permalink:\s*[\"']?/drugs/([^/\"'\s]+)/?[\"']?\s*$", _b, re.M)
    _tg = re.search(r'http-equiv="refresh"[^>]*url=(?:https?://[^/"]+)?/drugs/([^/"\s>]+)', _t, re.I)
    _LV_PAGES[_f.stem] = {
        "level": _lv_val(_b, "evidence_level") or "L5",
        "desc": _lv_val(_b, "description"),
        "noindex": _lv_val(_b, "noindex").lower() == "true" or _lv_val(_b, "search_exclude").lower() == "true",
        "redirect": 'http-equiv="refresh"' in _t or _lv_val(_b, "layout") == "id_redirect" or bool(_lv_val(_b, "redirect_to")),
        "target": _tg.group(1) if _tg else None,
        "url": _pm.group(1) if _pm else re.sub(r"[\W_]+", "-", _f.stem, flags=re.U).strip("-").lower(),
        "db": _lv_val(_b, "drugbank_id").lower(),
    }
_lv_bad = []
for _s, _p in _LV_PAGES.items():
    if _p["redirect"]:
        continue
    _toks = set(_LV_TOK.findall(_p["desc"]))
    if _toks and _toks != {_p["level"]}:
        _lv_bad.append(f"{_s}（description 寫 {'/'.join(sorted(_toks))}，頁首 {_p['level']}）")
if _lv_bad:
    errors.append(f"藥物頁 description 的證據等級與頁首不一致 {len(_lv_bad)} 頁，例：{'；'.join(_lv_bad[:5])}"
                  f"（母目錄跑 python3 .claude/sync_description_levels.py <本站> --apply；N/A 頁人工改寫）")

# 14) FHIR（docs/fhir）與藥物頁一致（2026-11-06 補）：MedicationKnowledge 的 evidence-level＝它對應藥物頁的頁首，
#    noindex／search_exclude 藥物頁的藥不得有 MedicationKnowledge 或 ClinicalUseDefinition（照 Tw 的規則不發布），
#    Bundle/all-predictions.json 的 entry＝它所收資源類型的實際檔案（內容相同、total＝entry 數），Bundle/summary.json
#    與 index.json 的總數、metadata 描述裡的藥物數／適應症數＝實際檔數。Th 的 amlodipine 曾標 L4、頁首 L5。
#    MedicationKnowledge 對頁：同名頁（大小寫、- 與 _ 視為相同；轉址頁跟著轉址）→ front matter drugbank_id →
#    去掉分隔符號同名 → docs/_data/fhir_page_map.json（依其他站 DrugBank ID 對到的頁）；都對不到的不查。
#    修法：母目錄 python3 .claude/sync_fhir_levels.py <本站> --apply（在地欄位不動）。
_LV_FHIR = DOCS / "fhir"
if (_LV_FHIR / "MedicationKnowledge").is_dir():
    _lv_mapf = DOCS / "_data" / "fhir_page_map.json"
    _lv_map = json.loads(_lv_mapf.read_text(encoding="utf-8")).get("map", {}) if _lv_mapf.exists() else {}
    _lv_key, _lv_url, _lv_db, _lv_norm = {}, {}, {}, {}
    for _s, _p in _LV_PAGES.items():
        for _k in {_s.lower(), _s.lower().replace("-", "_"), _s.lower().replace("_", "-")}:
            _lv_key.setdefault(_k, []).append(_s)
        _lv_url.setdefault(_p["url"], []).append(_s)
        if _p["db"] and not _p["redirect"]:
            _lv_db.setdefault(_p["db"], []).append(_s)
        _lv_norm.setdefault(re.sub(r"[^a-z0-9]", "", _s.lower()), []).append(_s)

    def _lv_page(_id):
        _k = _id.lower()
        _hit = None
        for _c in (_k, _k.replace("-", "_"), _k.replace("_", "-")):
            _h = _lv_key.get(_c) or []
            if _h:
                _hit = _h[0] if len(_h) == 1 else next((_x for _x in _h if _x == _id), None)
                break
        if _hit is None:
            if re.fullmatch(r"db\d{5}", _k):
                _h = _lv_db.get(_k) or []
                _hit = _h[0] if len(_h) == 1 else None
            else:
                _h = _lv_norm.get(re.sub(r"[^a-z0-9]", "", _k)) or []
                _hit = _h[0] if len(_h) == 1 else None
        if _hit is None and _id in _lv_map:
            _hit = _lv_map[_id].get("page") if _lv_map[_id].get("page") in _LV_PAGES else None
        _seen = set()
        while _hit and _LV_PAGES[_hit]["redirect"] and _hit not in _seen:
            _seen.add(_hit)
            _h = [_x for _x in _lv_url.get(_LV_PAGES[_hit]["target"] or "", []) if _x != _hit]
            _hit = _h[0] if len(_h) == 1 else None
        return None if (_hit and _LV_PAGES[_hit]["redirect"]) else _hit

    _lv_mk = {_f.stem: json.loads(_f.read_text(encoding="utf-8")) for _f in (_LV_FHIR / "MedicationKnowledge").glob("*.json")}
    _lv_cud = {_f.stem: json.loads(_f.read_text(encoding="utf-8")) for _f in (_LV_FHIR / "ClinicalUseDefinition").glob("*.json")}
    _lv_lvl, _lv_hid = [], set()
    for _s, _r in _lv_mk.items():
        _pg = _lv_page(_r.get("id") or _s)
        if not _pg:
            continue
        if _LV_PAGES[_pg]["noindex"]:
            _lv_hid.add(_r.get("id") or _s)
            continue
        _ext = next((_x for _x in _r.get("extension") or [] if str(_x.get("url", "")).endswith("/evidence-level")), None)
        if _ext is not None and _ext.get("valueCode") != _LV_PAGES[_pg]["level"]:
            _lv_lvl.append(f"{_s}（{_ext.get('valueCode')}，頁首 {_LV_PAGES[_pg]['level']}）")
    for _r in _lv_cud.values():
        _ref = next((str(_x.get("reference", "")) for _x in _r.get("subject") or []
                     if str(_x.get("reference", "")).startswith("MedicationKnowledge/")), "")
        _sid = _ref.split("/", 1)[1] if _ref else ""
        if _sid and _sid not in _lv_hid:
            _pg = _lv_page(_sid)
            if _pg and _LV_PAGES[_pg]["noindex"]:
                _lv_hid.add(_sid)
    _lv_fb = []
    if _lv_lvl:
        _lv_fb.append(f"MedicationKnowledge 等級與頁首不一致 {len(_lv_lvl)} 個，例：{'；'.join(_lv_lvl[:5])}")
    if _lv_hid:
        _lv_fb.append(f"含 noindex 藥物頁的藥 {len(_lv_hid)} 個，例：{sorted(_lv_hid)[:5]}")
    _n_mk, _n_cud = len(_lv_mk), len(_lv_cud)
    _bp = _LV_FHIR / "Bundle" / "all-predictions.json"
    if _bp.exists():
        _bd = json.loads(_bp.read_text(encoding="utf-8"))
        _ent = _bd.get("entry") or []
        _types = {_x["resource"]["resourceType"] for _x in _ent}
        _files = {}
        if "MedicationKnowledge" in _types:
            _files.update({("MedicationKnowledge", _r.get("id") or _s): _r for _s, _r in _lv_mk.items()})
        if "ClinicalUseDefinition" in _types:
            _files.update({("ClinicalUseDefinition", _r.get("id") or _s): _r for _s, _r in _lv_cud.items()})
        _got = {(_x["resource"]["resourceType"], _x["resource"].get("id")): _x["resource"] for _x in _ent}
        if _bd.get("total") != len(_ent):
            _lv_fb.append(f"Bundle/all-predictions.json total={_bd.get('total')}，entry {len(_ent)} 筆")
        if set(_got) != set(_files) or len(_got) != len(_ent):
            _lv_fb.append(f"Bundle/all-predictions.json 與資源檔不一致：缺 {len(set(_files) - set(_got))}、多 {len(set(_got) - set(_files))}、"
                          f"重複 {len(_ent) - len(_got)}")
        elif any(_got[_k] != _files[_k] for _k in _files):
            _lv_fb.append("Bundle/all-predictions.json 有 entry 與資源檔內容不同")
    _sp = _LV_FHIR / "Bundle" / "summary.json"
    if _sp.exists() and json.loads(_sp.read_text(encoding="utf-8")).get("total") != _n_mk + _n_cud:
        _lv_fb.append(f"Bundle/summary.json total 不等於 MedicationKnowledge＋ClinicalUseDefinition 檔數 {_n_mk + _n_cud}")
    _ip = _LV_FHIR / "index.json"
    if _ip.exists():
        _ix = json.loads(_ip.read_text(encoding="utf-8"))
        _cnt = {(_x.get("resource") or {}).get("resourceType"): (_x.get("resource") or {}).get("count") for _x in _ix.get("entry") or []}
        if {_k: _v for _k, _v in _cnt.items() if _k in ("MedicationKnowledge", "ClinicalUseDefinition")} != \
                {_k: _v for _k, _v in {"MedicationKnowledge": _n_mk, "ClinicalUseDefinition": _n_cud}.items() if _k in _cnt} \
                or _ix.get("total") != sum(_v or 0 for _v in _cnt.values()):
            _lv_fb.append(f"index.json 的 count／total 與實際檔數（MedicationKnowledge {_n_mk}、ClinicalUseDefinition {_n_cud}）不符")
    for _mn in ("metadata", "metadata.json"):
        _mp = _LV_FHIR / _mn
        if not _mp.exists():
            continue
        _md = json.loads(_mp.read_text(encoding="utf-8")).get("description", "")
        for _pat in (r"Contains (\d+) drugs and (\d+) predicted indications",
                     r"Contains (\d+) MedicationKnowledge and (\d+) ClinicalUseDefinition resources",
                     r"(\d+) 医薬品、(\d+) 予測適応症"):
            _mm = re.search(_pat, _md)
            if _mm and (int(_mm.group(1)), int(_mm.group(2))) != (_n_mk, _n_cud):
                _lv_fb.append(f"fhir/{_mn} 寫 {_mm.group(1)}／{_mm.group(2)}，實際 MedicationKnowledge {_n_mk}、ClinicalUseDefinition {_n_cud}")
    if _lv_fb:
        errors.append(f"FHIR 與藥物頁不一致：{'；'.join(_lv_fb)}（母目錄跑 python3 .claude/sync_fhir_levels.py <本站> --apply）")


# 15) FHIR metadata 的在地欄位（2026-11-06 補）：docs/fhir/metadata、metadata.json（CapabilityStatement）當初從別站複製，
#    Dk／Nl／Za 的 metadata.json 曾寫「Australia」、國碼寫成「Dk」這種不合 ISO 3166-1 alpha-2 的格式，Ph 的 url 曾是 github.io。
#    jurisdiction（urn:iso:std:iso:3166）國碼＝本站國碼；所有文字欄位不得出現別站國名或別站代號；
#    url、implementation.url、contact 的網址要在本站網域；非中日文站的文字欄位不得有漢字（Kr 的 description 曾是中文）。
#    本站的值寫死在這裡（國碼＝ISO 3166-1 alpha-2，網域＝_config.yml 的 url），不讀別站。
#    修法：只改 docs/fhir/metadata* 錯的欄位，scripts/generate_fhir_resources.py 寫錯的地方一起改，數字欄位不動。
_MD_ISO = "JP"
_MD_HOST = "https://jptxgnn.yao.care"
_MD_HAN_OK = True
_MD_OTHER_NAMES = re.compile(r"\bArgentin|\bAustralia|\bBrazil|\bSwitzerland\b|\bSwiss\b|\bColombia|\bCanad(?:a|ian)\b|\bGermany\b|\bGerman\b|\bDenmark\b|\bDanish\b|\bSpain\b|\bSpanish\b|\bEuropean Union\b|\bFinland\b|\bFinnish\b|\bFrance\b|\bFrench\b|\bHong Kong\b|\bItaly\b|\bItalian\b|\bIndian?\b|\bKorea|\bMalaysia|\bNorway\b|\bNorwegian\b|\bNew Zealand\b|\bNetherlands\b|\bDutch\b|\bPhilippine|\bSaudi\b|\bSweden\b|\bSwedish\b|\bSingapore|\bThailand\b|\bThai\b|\bTaiwan|\bUnited Kingdom\b|\bUK\b|\bBritish\b|\bUnited States\b|\bUSA\b|\bSouth Africa")
_MD_OTHER_SITES = re.compile(r"\b(?:ARTxGNN|AuTxGNN|BrTxGNN|CHTxGNN|COTxGNN|CaTxGNN|DETxGNN|DkTxGNN|ESTxGNN|EuTxGNN|FITxGNN|FRTxGNN|HkTxGNN|ITTxGNN|InTxGNN|KrTxGNN|MyTxGNN|NOTxGNN|NZTxGNN|NlTxGNN|PhTxGNN|SATxGNN|SETxGNN|SgTxGNN|ThTxGNN|TwTxGNN|UkTxGNN|UsTxGNN|ZaTxGNN|CnTxGNN)\b", re.I)


def _md_strings(_v, _path=""):
    if isinstance(_v, dict):
        for _k, _x in _v.items():
            yield from _md_strings(_x, f"{_path}.{_k}" if _path else _k)
    elif isinstance(_v, list):
        for _i, _x in enumerate(_v):
            yield from _md_strings(_x, f"{_path}[{_i}]")
    elif isinstance(_v, str):
        yield _path, _v


_md_bad = []
for _mn in ("metadata", "metadata.json"):
    _mp = DOCS / "fhir" / _mn
    if not _mp.exists():
        continue
    try:
        _md = json.loads(_mp.read_text(encoding="utf-8"))
    except ValueError as _e:
        _md_bad.append(f"fhir/{_mn} 不是合法 JSON：{_e}")
        continue
    for _j in _md.get("jurisdiction") or []:
        for _c in _j.get("coding") or []:
            if _c.get("system") == "urn:iso:std:iso:3166" and _c.get("code") != _MD_ISO:
                _md_bad.append(f"fhir/{_mn} jurisdiction 國碼 {_c.get('code')!r}，本站是 {_MD_ISO}")
    _urls = [("url", _md.get("url"))] + [("implementation.url", (_md.get("implementation") or {}).get("url"))] + \
            [("contact", _t.get("value")) for _ct in _md.get("contact") or [] for _t in _ct.get("telecom") or []
             if _t.get("system") == "url"]
    for _k, _u in _urls:
        if _u and not (_u == _MD_HOST or _u.startswith(_MD_HOST + "/")):
            _md_bad.append(f"fhir/{_mn} {_k}={_u} 不在本站網域 {_MD_HOST}")
    for _k, _t in _md_strings(_md):
        if _k.startswith("rest") and _k.endswith(("profile", "definition")):
            continue
        for _rx, _what in ((_MD_OTHER_NAMES, "別站國名"), (_MD_OTHER_SITES, "別站代號")):
            _m = _rx.search(_t)
            if _m:
                _md_bad.append(f"fhir/{_mn} {_k} 出現{_what}「{_m.group(0)}」：{_t[:80]}")
        if not _MD_HAN_OK and re.search(r"[\u4e00-\u9fff]", _t):
            _md_bad.append(f"fhir/{_mn} {_k} 有漢字（本站不是中日文站）：{_t[:80]}")
if _md_bad:
    errors.append(f"FHIR metadata 在地欄位錯 {len(_md_bad)} 處：{'；'.join(_md_bad[:6])}"
                  f"（只改 docs/fhir/metadata* 錯的欄位與 scripts/generate_fhir_resources.py，數字欄位不動）")


# 16) 所有 FHIR 檔的在地欄位（2026-11-06 補）：docs/fhir 底下每個檔（MedicationKnowledge、ClinicalUseDefinition、Bundle 等）
#    jurisdiction（urn:iso:std:iso:3166）國碼都＝本站國碼（上一項的 _MD_ISO；Dk／Nl／Za 的 MedicationKnowledge 曾寫 Dk／Nl／Za）；
#    網址的主機名含 txgnn 或是 github.io 的，必須是本站網域（Ph 曾有 2,289 個檔寫 phtxgnn.github.io）；
#    metadata 與 metadata.json 都在時內容要相同（/fhir/metadata 才是實際對外的那份）；metadata* 只宣稱 read（靜態站做不到 search-type）。
_fx_bad, _fx_code, _fx_host = [], {}, {}
_fx_rx_code = re.compile(r'"system":\s*"urn:iso:std:iso:3166",\s*"code":\s*"([^"]*)"')
_fx_rx_host = re.compile(r'https?://([A-Za-z0-9.-]+)')
_fx_own = _MD_HOST.split("://", 1)[1]
for _fp in sorted((DOCS / "fhir").rglob("*")) if (DOCS / "fhir").is_dir() else []:
    if not _fp.is_file():
        continue
    _ft = _fp.read_text(encoding="utf-8", errors="ignore")
    _rel = _fp.relative_to(DOCS).as_posix()
    for _c in _fx_rx_code.findall(_ft):
        if _c != _MD_ISO:
            _fx_code.setdefault(_c, []).append(_rel)
    for _h in set(_fx_rx_host.findall(_ft)):
        _hl = _h.lower()
        if ("txgnn" in _hl or _hl.endswith("github.io")) and _hl != _fx_own:
            _fx_host.setdefault(_h, []).append(_rel)
for _c, _fs in _fx_code.items():
    _fx_bad.append(f"jurisdiction 國碼 {_c!r}（本站 {_MD_ISO}）{len(_fs)} 個檔，例：{_fs[0]}")
for _h, _fs in _fx_host.items():
    _fx_bad.append(f"網址主機 {_h} 不是本站 {_fx_own}，{len(_fs)} 個檔，例：{_fs[0]}")
_fx_md = {}
for _mn in ("metadata", "metadata.json"):
    _mp = DOCS / "fhir" / _mn
    if _mp.exists():
        try:
            _fx_md[_mn] = json.loads(_mp.read_text(encoding="utf-8"))
        except ValueError:
            continue
        _ints = {_i.get("code") for _r in _fx_md[_mn].get("rest") or [] for _x in _r.get("resource") or []
                 for _i in _x.get("interaction") or []}
        if _ints - {"read"}:
            _fx_bad.append(f"fhir/{_mn} 宣稱 {sorted(_ints - {'read'})}，靜態站只支援 read")
if len(_fx_md) == 2 and _fx_md["metadata"] != _fx_md["metadata.json"]:
    _fx_bad.append("fhir/metadata 與 fhir/metadata.json 內容不同（/fhir/metadata 是實際對外的那份，metadata.json 要跟它一樣）")
if _fx_bad:
    errors.append(f"FHIR 檔的在地欄位錯 {len(_fx_bad)} 項：{'；'.join(_fx_bad[:6])}"
                  f"（只改國碼／網域那一處；metadata.json 照 metadata 寫；scripts/generate_fhir_resources.py 寫錯的地方一起改）")

# 17–20) 本站查核機制（2026-11-12，用戶決定 30 站各有自己的查核機制，核心流程比照 TwTxGNN／UsTxGNN）
sys.path.insert(0, str(DOCS.parent / "src"))
sys.path.insert(0, str(DOCS.parent / "scripts"))
from apply_drug_reviews import check_errors as _review_errors  # noqa: E402
from jptxgnn.regulatory import licenses as _Lic, page_format as _Pf, withdrawn as _Wd  # noqa: E402
errors += _review_errors()
_lic_errs = _Lic.site_problems()
if _lic_errs:
    errors.append(f"許可證資訊跟快照不一致 {len(_lic_errs)} 項：{'；'.join(_lic_errs[:5])}")
_hdr = []
for _f in sorted((DOCS / "_drugs").glob("*.md")):
    _t = _f.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in _t[:3000] or re.search(r"^layout:\s*id_redirect", _t[:3000], re.M):
        continue
    _hdr += [f"{_f.name}：{x}" for x in _Pf.header_problems(_t, _f.stem)]
if _hdr:
    errors.append(f"藥物頁頁首等級跟快速總覽不一致 {len(_hdr)} 頁：{'；'.join(_hdr[:5])}"
                  "（等級要改經查核紀錄 rereview_result；規則見 src/jptxgnn/regulatory/page_format.py）")
_left = _Wd.published_withdrawn(DOCS)
if _left:
    errors.append(f"重審撤回的預測仍對外發布 {len(_left)} 處：{'；'.join(_left[:5])}")

if errors:
    print(f"docs SEO 守門：✗ {len(errors)} 項")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"docs SEO 守門：✓（{len(permalinks)} 個 permalink、{len(CRITICAL)} 個關鍵入口）")
