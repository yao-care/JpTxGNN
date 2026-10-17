"""「既存適応症」欄混入繁體中文（台灣 TFDA 適應症）的頁，改成日本的寫法（2026-10-17，T-314）。

- 有 PMDA 資料（data/raw/jp_fda_drugs.json 的「効能・効果」，經 drug_mapping.csv 對到同一 DrugBank ID）：
  取疾患名（[DS:] 行）去重，最多 8 個。
- 沒有：寫「日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：…）」（不寫「記載なし」，避免讀成日本未核准），取 data/external/drug_disease_relations.csv
  的 indication 最多 6 個（英文病名）。
同時改 docs/_drugs/<藥>.md 與 data/notes/<藥>/drug_pharmacist_notes.md（sync 會用筆記重生頁面）。
用法：uv run python scripts/fix_original_indication_ja.py [--dry-run]
"""
import csv, json, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# 只有繁體中文會用、日文不用的字（中日共用字如 機・異・預・縮 不列入）
TRAD = re.compile(r"[關經應劑與藥體學處臟擴發變壓營氣醫雜齒顯鹽黴會獲濕歲癥蟲瘧鬱腦膽擔歡衛護屬歷漸險將專從傳單產狹壞]")
ROW = re.compile(r"^(\|\s*既存適応症\s*\|)([^|\n]+)(\|)", re.M)


def pmda_diseases():
    raw = json.load(open(ROOT / "data/raw/jp_fda_drugs.json", encoding="utf-8"))
    mp = {r["承認番号"]: r for r in csv.DictReader(open(ROOT / "data/processed/drug_mapping.csv", encoding="utf-8-sig"))}
    out = defaultdict(list)
    for d in raw:
        r = mp.get(str(d.get("承認番号")))
        if not r or not r.get("drugbank_id"):
            continue
        for line in str(d.get("効能・効果", "")).split("\n"):
            if "[DS:" not in line:
                continue
            name = re.sub(r"\[DS:[^\]]*\]", "", re.sub(r"^疾患\s*", "", line)).strip()
            if name and name not in out[r["drugbank_id"]]:
                out[r["drugbank_id"]].append(name)
    return out


def kg_indications():
    out = defaultdict(list)
    with open(ROOT / "data/external/drug_disease_relations.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["relation"] == "indication" and r["y_name"] not in out[r["x_id"]]:
                out[r["x_id"]].append(r["y_name"])
    return out


def main(dry):
    pm, kg = pmda_diseases(), kg_indications()
    n_pm = n_kg = n_skip = 0
    for f in sorted((ROOT / "docs/_drugs").glob("*.md")):
        t = f.read_text(encoding="utf-8", errors="replace")
        if 'http-equiv="refresh"' in t:
            continue
        m = ROW.search(t)
        if not m or not TRAD.search(m.group(2)):
            continue
        old = m.group(2).strip()
        b = ROOT / "data/bundles" / f.stem / "drug_bundle.json"
        db = json.load(open(b, encoding="utf-8"))["drug"].get("drugbank_id") if b.exists() else None
        if db and pm.get(db):
            new = "、".join(pm[db][:8]); n_pm += 1
        elif db and kg.get(db):
            new = "日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：" + "、".join(kg[db][:6]) + "）"; n_kg += 1
        else:
            new = "日本の承認適応症は本サイトのデータに未収載"; n_skip += 1
        print(f"{f.stem}\t{old[:50]}\t→\t{new[:70]}")
        if dry:
            continue
        f.write_text(t.replace(m.group(0), f"{m.group(1)} {new} {m.group(3)}", 1), encoding="utf-8")
        note = ROOT / "data/notes" / f.stem / "drug_pharmacist_notes.md"
        if note.exists():
            nt = note.read_text(encoding="utf-8")
            nm = ROW.search(nt)
            if nm and nm.group(2).strip() == old:
                note.write_text(nt.replace(nm.group(0), f"{nm.group(1)} {new} {nm.group(3)}", 1), encoding="utf-8")
    print(f"PMDA {n_pm}、知識圖譜 {n_kg}、皆無 {n_skip}")


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
