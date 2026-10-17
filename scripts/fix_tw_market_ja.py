"""報告裡殘留台灣許可證資料（衛署／衛部字號、「承認数 N 張」）的頁，改成 PMDA 資料（2026-10-17，T-314）。

- 「## 日本上市情報」段整段換成 PMDA 承認一覽（data/raw/jp_fda_drugs.json，經 drug_mapping.csv 對到同一 DrugBank ID），最多 5 列。
- 概要表「日本上市」「承認数」兩列換成「日本市販状況」「承認番号数」，數字取 PMDA 件數。
- 本文其他段落（中文敘述）不在這裡處理。
同時改 docs/_drugs/<藥>.md 與 data/notes/<藥>/drug_pharmacist_notes.md（sync 會用筆記重生頁面）。
用法：uv run python scripts/fix_tw_market_ja.py [--dry-run]
"""
import csv, json, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TW = re.compile(r"許可證|註銷|衛署|衛部|藥證|TFDA|台灣|臺灣|健保|承認数\s*\|\s*[^|\n]*張")
SECTION = re.compile(r"^## 日本上市情報\n.*?(?=^## )", re.M | re.S)
ROW_MARKET = re.compile(r"^\|\s*日本上市\s*\|[^\n]*\|$", re.M)
ROW_COUNT = re.compile(r"^\|\s*承認数\s*\|[^\n]*\|$", re.M)


def pmda_records():
    raw = json.load(open(ROOT / "data/raw/jp_fda_drugs.json", encoding="utf-8"))
    mp = {r["承認番号"]: r.get("drugbank_id") for r in csv.DictReader(open(ROOT / "data/processed/drug_mapping.csv", encoding="utf-8-sig"))}
    out = defaultdict(list)
    for d in raw:
        db = mp.get(str(d.get("承認番号")))
        if db:
            out[db].append(d)
    return out


def indication(d):
    lines = [l for l in str(d.get("効能・効果", "")).split("\n") if l.strip()]
    ds = [re.sub(r"\[DS:[^\]]*\]", "", re.sub(r"^疾患\s*", "", l)).strip() for l in lines if "[DS:" in l]
    if ds:
        return "、".join(dict.fromkeys(ds))[:80]
    return lines[0].replace(", ", "、")[:80] if lines else "—"


def section(recs):
    if not recs:
        return "## 日本市販情報\n\n日本の承認情報は本サイトのデータに未収載です。\n\n"
    act = [d for d in recs if d.get("承認状況") == "有効"]
    head = f"PMDA の承認は {len(recs)} 件（うち有効 {len(act)} 件）です。主な承認は次のとおりです。"
    rows = ["| 承認番号 | 販売名 | 剤形 | 効能・効果 |", "|---------|------|------|-----------|"]
    for d in (act or recs)[:5]:
        rows.append(f"| {d.get('承認番号')} | {d.get('販売名', '')} | {d.get('剤形', '')} | {indication(d)} |")
    return "## 日本市販情報\n\n" + head + "\n\n" + "\n".join(rows) + "\n\n"


def fix(t, recs):
    act = sum(1 for d in recs if d.get("承認状況") == "有効")
    status = (f"販売承認あり（有効 {act} 件）" if act else "有効な承認なし") if recs else "本サイトのデータに未収載"
    t = SECTION.sub(lambda m: section(recs), t, count=1)
    t = ROW_MARKET.sub(f"| 日本市販状況 | {status} |", t, count=1)
    t = ROW_COUNT.sub(f"| 承認番号数 | {len(recs)} 件 |" if recs else "| 承認番号数 | — |", t, count=1)
    return t


def main(dry):
    pm = pmda_records()
    n = 0
    for f in sorted((ROOT / "docs/_drugs").glob("*.md")):
        t = f.read_text(encoding="utf-8", errors="replace")
        if 'http-equiv="refresh"' in t or not TW.search(t):
            continue
        b = ROOT / "data/bundles" / f.stem / "drug_bundle.json"
        db = json.load(open(b, encoding="utf-8"))["drug"].get("drugbank_id") if b.exists() else None
        recs = pm.get(db, []) if db else []
        new = fix(t, recs)
        left = [l for l in new.splitlines() if TW.search(l)]
        print(f"{f.stem}\tPMDA {len(recs)} 件\t殘留 {len(left)} 行")
        if dry or new == t:
            continue
        n += 1
        f.write_text(new, encoding="utf-8")
        note = ROOT / "data/notes" / f.stem / "drug_pharmacist_notes.md"
        if note.exists():
            nt = note.read_text(encoding="utf-8")
            nn = fix(nt, recs)
            if nn != nt:
                note.write_text(nn, encoding="utf-8")
    print(f"改寫 {n} 頁")


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
