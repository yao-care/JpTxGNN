#!/usr/bin/env python3
"""快速總覽「原適應症」列的程式化交叉驗證（只列待查，不改頁面）（2026-11-12 建，比照 TwTxGNN／UsTxGNN 同名腳本；
本站的列標籤與「資料沒有」的寫法在 src/<套件>/regulatory/site.py）。

做法：把每頁快速總覽「原適應症」的文字切成詞組，逐一比對
  (a) 本藥證據包（data/bundles/<藥>/drug_bundle.json）的許可證／仿單適應症文字（含 records 的區塊的 indication、package_insert）；
  (b) 其他藥的許可證／仿單適應症文字。
某詞組在 (a) 找不到、卻在 (b) 找得到，就是「只出現在不屬於本藥的許可證」的詞組。一頁有這種詞組且占該列詞組一半以上，
就寫進 docs/_data/drug_reviews_uncertain.json（source＝本程式；每次執行整批替換這個 source 的項目），交人工判讀。
「資料沒有」的寫法（site.ORIGINAL_NONE_RE）不比對。證據包沒有適應症文字的頁也不比對，程式照實回報可比對頁數。

用法：python3 scripts/check_original_indications.py   （需要 data/bundles）
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from jptxgnn.regulatory import site as C  # noqa: E402
UNCERTAIN = ROOT / "docs" / "_data" / "drug_reviews_uncertain.json"
SOURCE = "Original Indication 交叉驗證（scripts/check_original_indications.py）"
ROW_RE = re.compile(r"^\|\s*(?:" + "|".join(re.escape(x) for x in C.ORIGINAL_LABELS) + r")\s*\|([^|\n]*)\|", re.M)
NONE_RE = C.ORIGINAL_NONE_RE
SPLIT_RE = C.PHRASE_SPLIT
REVIEW_RE = re.compile(r"<!-- review:begin (\S+) -->.*?<!-- review:end \1 -->", re.S)


def phrases(cell):
    cell = re.sub(r"\*\*|\[[^\]]*\]\([^)]*\)", "", cell)
    return [p.strip().lower() for p in SPLIT_RE.split(cell) if len(p.strip()) >= C.PHRASE_MIN]


def label_text(bundle):
    parts = [r.get("indication") or r.get("approved_indication_text") or "" for v in bundle.values()
             if isinstance(v, dict) and isinstance(v.get("records"), list) for r in v["records"]]
    pi = bundle.get("package_insert") or {}
    parts += [pi.get("indications") or pi.get("indications_and_usage") or ""] if isinstance(pi, dict) else []
    return " ".join(p for p in parts if p).lower()


def main():
    bundles = {}
    for f in sorted((ROOT / "data/bundles").glob("*/drug_bundle.json")):
        txt = label_text(json.loads(f.read_text(encoding="utf-8")))
        if txt.strip():
            bundles[f.parent.name] = txt
    pages, items, stat = 0, [], Counter()
    for page in sorted((ROOT / "docs/_drugs").glob("*.md")):
        t = REVIEW_RE.sub("", page.read_text(encoding="utf-8"))
        m = ROW_RE.search(t)
        if not m or NONE_RE.match(m.group(1)):
            stat["no_original"] += 1
            continue
        own = bundles.get(page.stem) or bundles.get(page.stem.replace("-", "_"))
        if not own:
            stat["no_label_text"] += 1
            continue
        pages += 1
        ph = phrases(m.group(1))
        foreign = [p for p in ph if p not in own and any(p in v for k, v in bundles.items() if k != page.stem)]
        if ph and len(foreign) * 2 >= len(ph):
            items.append({"source": SOURCE, "drug": page.stem, "file": page.name, "status": "open",
                          "claim": m.group(1).strip(), "foreign_phrases": foreign,
                          "note": "原適應症列的詞組多半只出現在其他藥的許可證／仿單適應症，待人工對照仿單"})
    doc = json.loads(UNCERTAIN.read_text(encoding="utf-8")) if UNCERTAIN.exists() else {"_doc": DOC, "items": []}
    doc["items"] = [x for x in doc["items"] if x.get("source") != SOURCE] + items
    UNCERTAIN.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"原適應症交叉驗證：可比對 {pages} 頁、待查 {len(items)} 頁（沒有原適應症 {stat['no_original']} 頁、"
          f"證據包沒有適應症文字 {stat['no_label_text']} 頁）")


DOC = ("藥物頁待查清單（2026-11-12 建，比照 TwTxGNN／UsTxGNN docs/_data/drug_reviews_uncertain.json）。項目不刪：查清標 status: resolved"
       "（附 record_ids，指向 docs/_data/drug_reviews.json 的紀錄），查不出定論標 status: unresolvable（附 searched、unresolvable_reason）。")

if __name__ == "__main__":
    sys.exit(main())
