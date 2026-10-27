#!/usr/bin/env python3
"""產生 docs/_data/drug_stats.json，並同步／檢查站上寫死的藥物數（照 EuTxGNN 1893e24d 的規則移植，2026-10-27）。

為什麼需要這支：
  站上的藥物總數曾經散落寫死在首頁、smart/*.md、head_custom.html 的 JSON-LD、README 裡，
  產線新增或下架藥物頁後沒人改（My 508、Sg 745、Th 191、Za 404……），ItemList numberOfItems
  還用 site.drugs.size（含 noindex 鹽類頁與轉址頁）。

規則：
  - 能用 Liquid 的地方一律寫 {{ site.data.drug_stats.total_drugs }}（.md 內文、_includes/*.html）。
  - 不能用 Liquid 的地方才列在 COUNT_SPOTS：README.md 的「藥物報告」列（不經 Jekyll）、
    scripts/drug_count_spots.json 列的各站位置（front matter description、靜態 svg 等）。
  - 首頁 index.md 的寫死數字由母專案 .claude/update_home_counts.py 維護，這裡不重複管。
  - total_drugs＝公開的藥物報告數＝docs/_drugs/*.md 扣掉 noindex 頁與舊 ID 轉址頁
    （和 docs/drugs.md 列表的 where_exp 篩選相同）。

守門（兩層）：
  - Jekyll 建置內：docs/drugs.md 比對 drug_stats.json 與實際公開藥物頁數／等級分布，不符就 include
    不存在的檔讓 GitHub Pages 建置失敗（錯誤訊息即修法）。
  - 本支 --check（scripts/check_seo_docs.py 也會跑）：另外檢查 COUNT_SPOTS 與 Liquid 檔裡寫死的藥物數。

用法：
  python3 scripts/generate_drug_stats.py           # 重算 drug_stats.json 並改正 COUNT_SPOTS
  python3 scripts/generate_drug_stats.py --check   # 只檢查，不一致就列出檔案並以非零結束
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRUGS = ROOT / "docs" / "_drugs"
OUT = ROOT / "docs" / "_data" / "drug_stats.json"
SPOTS_FILE = ROOT / "scripts" / "drug_count_spots.json"

# (檔案, 正則（group 2 是數字）)；每條必須剛好命中一處。README 第一列統計固定是藥物報告數。
COUNT_SPOTS = [("README.md", r"\A((?:.*\n){21}\| \*\*[^*|\n]+\*\* \| )([\d,]+)( \|)")]
if SPOTS_FILE.exists():
    COUNT_SPOTS += [tuple(x) for x in json.loads(SPOTS_FILE.read_text(encoding="utf-8"))]

# 寫死藥物數的偵測：數字前後三個詞內有「藥物／報告」字樣
_W = (r"(?:drugs?|medicines?|medications?|ubat|medicamentos?|fármacos?|farmacos?|arzneimittel\w*|lægemidl\w*|"
      r"geneesmiddel\w*|läkemed\w*|legemid\w*|lääk\w*|médicaments?|farmaci|藥物?|药物?|薬|医薬品|약물|의약품|ยา|أدوية|دواء|"
      r"reports?|relatórios?|informes?|rapports?|berichte|rapporter|rapporten|rapporti|laporan|รายงาน)")
_N = r"(?<![\d.,/#:\-])(\d{1,3}(?:[,.]\d{3})+|\d{2,4})(?![\d%.,/])"
_HARD = re.compile(_N + r"\s*\**\s*(?:\S+\s+){0,3}?\**" + _W + "|" + _W + r"\W{0,6}(?:\S+\s+){0,2}?" + _N, re.I)


def front(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    meta = {}
    for line in (m.group(1).splitlines() if m else []):
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def listed_drugs():
    drugs = []
    for p in sorted(DRUGS.glob("*.md")):
        fm = front(p.read_text(encoding="utf-8", errors="replace"))
        if fm.get("noindex", "").lower() == "true" or fm.get("layout") == "id_redirect":
            continue
        ic = fm.get("indication_count") or "0"
        drugs.append({"name": fm.get("title", p.stem), "slug": p.stem, "level": fm.get("evidence_level") or "L5",
                      "indication_count": int(ic) if ic.isdigit() else 0})
    return drugs


def build_stats(drugs, generated):
    counts = {f"L{n}": sum(d["level"] == f"L{n}" for d in drugs) for n in range(1, 6)}
    return {"generated": generated, "total_drugs": len(drugs), "level_counts": counts, "all_drugs": drugs}


def same(a, b):
    """generated 以外的欄位相同。"""
    return {k: v for k, v in a.items() if k != "generated"} == {k: v for k, v in b.items() if k != "generated"}


def fmt(n):
    return f"{n:,}"


def count_spot_problems(stats, fix=False):
    errs, by_file = [], {}
    for rel, pat in COUNT_SPOTS:
        by_file.setdefault(rel, []).append(re.compile(pat, re.M))
    for rel, rules in by_file.items():
        path = ROOT / rel
        if not path.exists():
            errs.append(f"{rel}：檔案不存在（scripts/drug_count_spots.json 要跟著改）")
            continue
        text = path.read_bytes().decode("utf-8")
        new = text
        for rx in rules:
            ms = list(rx.finditer(new))
            if len(ms) != 1:
                errs.append(f"{rel}：找不到（或不只一處）{rx.pattern}")
                continue
            want = fmt(stats["total_drugs"]) if "," in ms[0].group(2) or stats["total_drugs"] >= 1000 else str(stats["total_drugs"])
            if ms[0].group(2).replace(",", "") != str(stats["total_drugs"]):
                errs.append(f"{rel}：寫死的數字 {ms[0].group(2)} 應為 {want}")
                new = rx.sub(lambda m: m.group(1) + want + m.group(3), new, count=1)
        if fix and new != text:
            path.write_bytes(new.encode("utf-8"))
    return errs


def hardcode_problems(stats):
    """Liquid 可用的檔（docs 下有 front matter 的 .md 內文、_includes/*.html）不得寫死目前的藥物總數。
    index.md 由 update_home_counts.py 管，不掃。"""
    errs, total = [], stats["total_drugs"]
    docs = ROOT / "docs"
    cands = [p for p in docs.rglob("*.md")] + list((docs / "_includes").glob("*.html"))
    for p in sorted(cands):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(("docs/_drugs/", "docs/_news/", "docs/_site/", "docs/_posts/", "docs/fhir/")) or rel == "docs/index.md":
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        body_start = 0
        if p.suffix == ".md":
            m = re.match(r"---\r?\n.*?\r?\n---\r?\n", text, re.S)
            if not m:
                continue
            body_start = m.end()
        for m in _HARD.finditer(text, body_start):
            n = (m.group(1) or m.group(2) or "").replace(",", "").replace(".", "")
            if n == str(total):
                line = text.count("\n", 0, m.start()) + 1
                errs.append(f"{rel}:{line}：寫死的藥物數「{m.group(0)}」，改用 {{{{ site.data.drug_stats.total_drugs }}}}")
    return errs


def main():
    check = "--check" in sys.argv[1:]
    drugs = listed_drugs()
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    stats = build_stats(drugs, old.get("generated", ""))
    errs = []
    if check:
        if not same(old, stats):
            errs.append(f"docs/_data/drug_stats.json：total_drugs={old.get('total_drugs')}，公開藥物頁 {len(drugs)} 頁"
                        f"（或等級分布不符）")
    else:
        if not same(old, stats):
            stats["generated"] = date.today().isoformat()
            OUT.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"drug_stats.json：{stats['total_drugs']} 個藥，{stats['level_counts']}")
    errs += count_spot_problems(stats, fix=not check)
    errs += hardcode_problems(stats)
    if check:
        if errs:
            print("藥物數同步檢查：✗（修法：python3 scripts/generate_drug_stats.py，Liquid 檔手改）")
            for e in errs:
                print("  ✗", e)
            sys.exit(1)
        print(f"藥物數同步檢查：✓（{stats['total_drugs']} 個藥物報告）")
    else:
        rest = [e for e in errs if "應為" not in e]
        print(f"寫死的藥物數：更新 {len(errs) - len(rest)} 處")
        for e in rest:
            print("  ✗", e)
        sys.exit(1 if rest else 0)


if __name__ == "__main__":
    main()
