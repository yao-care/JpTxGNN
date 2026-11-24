"""JP 證據包依成分補收医薬品マスター現行品目、排除對照錯的品目（2026-11-24，用戶決定「證據包成分對照修正」第三輪 A；全程不用 AI）。

證據包的許可證紀錄（pmda 區塊）是 collectors/jpfda.py 依 data/processed/drug_mapping.csv 收的：品目（医薬品コード）的一般名或カナ名 → DrugBank ID →
同一 DrugBank ID 的品目。沒有一般名處方名、カナ名又只是商品名的品目（ビソノテープ、フロベン錠、ゼンタコート、ケイツーＮ、アラセナ－Ａ点滴、
カベルゴリン錠「サワイ」…）對照失敗就收不到；カナ名轉英文偶爾對錯成分（ﾄﾎﾟﾃｼﾝ→TOPOTECAN，其實是イリノテカン；ﾚﾐﾌｪﾝﾀﾆﾙ→FENTANYL；
炭酸リチウム→LITHIUM→DB14507 Lithium citrate）。

医薬品マスター（薬価基準収載品目）的 YJ コード（薬価基準収載医薬品コード）前 7 碼＝薬効分類 4 碼＋投与経路・成分 3 碼，同一群是同一成分（含同一配合）的品目。
這支照同一套來源補收、排除（不放寬一般名比對）：
1. 群的 DrugBank ID：drug_mapping.csv 對照成功的品目所屬的群，群內只有一個 DrugBank ID 才用；config/ingredient_groups.json 的人工對照（每筆附依據）優先，
   也覆寫 drug_mapping.csv 對這個群的列（--dry-run 不寫）。
2. 補收（規則 R1）：群的 DrugBank ID 在證據包 drugbank_ids 裡、群內現行品目（最新全件ファイル）不在證據包紀錄、也不是 drug_mapping 已算進 total_matches 的，補一筆。
3. 補收（規則 R2，跨薬効分類）：drug_mapping 沒有任何對照的群，群內每個品目的漢字名稱都以本藥的先發商品名（data/raw/jp_fda_drugs.json「商品名一覧」裡「後発品」
   之前、三字以上）或本藥的一般名基本名（一般名處方名去規格劑形）開頭、後面接的不是片假名（或是劑形字），而且只對得到一個證據包，才整群補。
4. 排除：證據包紀錄所屬的群經人工對照是別的 DrugBank ID 的，移到 pmda.excluded_records（附 reason）；drug_mapping 算進 total_matches、沒存成紀錄的同類品目從 total_matches 扣掉。
- 不處理的證據包（EXCLUDE）：離子類 calcium、magnesium、zinc、iron（drug_mapping 把各種鹽對到裸離子，ホスミシン（ホスホマイシンカルシウム）、ヘパリンカルシウム也在裡面，補收會放大誤配）。
- 只處理有藥物頁（非轉址）的證據包。補的紀錄欄位照 scripts/license_adapter.py 的 _successor_record（convert_ssk_to_json 的轉法），status「有効」，
  另記 source（全件ファイル名、YJ 群、規則）、added（補收日）、yj_group；不設筆數上限（同後継コード補收），total_matches 同步加。
- 只加不刪（排除是移到 excluded_records，不丟）、可重複執行。
用法（repo 根目錄）：python3 scripts/add_current_ingredient_items.py [--master y_ALL*.zip] [--dry-run] [--report out.tsv]
  不給 --master 就從 hpdx.or.jp 下載最新全件ファイル（同 license_adapter.fetch）。
"""
import argparse
import csv
import io
import json
import re
import sys
import time
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "ingredient_groups.json"
MAP = ROOT / "data" / "processed" / "drug_mapping.csv"
MIN_ROWS = 15000
EXCLUDE = {
    "calcium": "離子類（カルシウム塩・ヘパリンカルシウム・ホスホマイシンカルシウム等が裸のカルシウムに対照されている）",
    "magnesium": "離子類（酸化マグネシウム等の塩が裸のマグネシウムに対照されている）",
    "zinc": "離子類", "iron": "離子類",
}
KATA = re.compile(r"[ァ-ヺー]")
FORMS = ("テープ", "パップ", "クリーム", "ローション", "シロップ", "カプセル", "ゲル", "スプレー", "パッチ", "ドライシロップ", "エアゾール")


def nfkc(s):
    return unicodedata.normalize("NFKC", s or "").strip()


def load_master(path):
    if path:
        content = Path(path).read_bytes()
        name = Path(path).name
    else:
        sys.path.insert(0, str(ROOT / "scripts"))
        import license_adapter as A
        import requests
        page = A._get(A.PAGE)
        links = sorted(set(re.findall(r'href="([^"]*y_ALL(\d{8})\.zip)"', page.text)), key=lambda x: x[1])
        href = links[-1][0]
        content = A._get(requests.compat.urljoin(page.url, href)).content
        name = href.rsplit("/", 1)[-1]
    z = zipfile.ZipFile(io.BytesIO(content))
    rows = [c for c in csv.reader(io.StringIO(z.read(z.namelist()[0]).decode("cp932", "replace"))) if len(c) > 37 and c[2].strip().isdigit()]
    return {c[2].strip(): c for c in rows}, name


def record(c, master_name, grp, rule):
    import importlib.util
    sp = importlib.util.spec_from_file_location("_ssk", ROOT / "scripts" / "convert_ssk_to_json.py")
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    brand, kana = c[4].strip(), c[6].strip()
    generic = re.sub(r"^【般】", "", c[37].strip()).strip()
    base, form = m.parse_drug_name(brand)
    ing = m.extract_generic_name(generic, "") if generic else m.extract_generic_name(base, kana)
    return {"license_id": c[2].strip(), "brand_name_zh": brand, "brand_name_en": generic, "ingredients": ing, "indication": "",
            "dosage_form": form, "manufacturer": "", "license_holder": "", "approval_date": c[29].strip(), "expiry_date": "",
            "status": "有効", "yj_group": grp,
            "source": f"医薬品マスター全件ファイル {master_name}（YJ コード前 7 碼 {grp} の同成分品目、{rule}）",
            "added": time.strftime("%Y-%m-%d")}


def base_generic(g):
    """【般】ビソプロロールフマル酸塩錠５ｍｇ → ビソプロロールフマル酸塩"""
    s = re.sub(r"^【般】", "", nfkc(g))
    s = re.split(r"(錠|カプセル|散|顆粒|細粒|注射|注|シロップ|液|点眼|点鼻|軟膏|クリーム|ゲル|テープ|パップ|貼付|坐剤|吸入|ローション|外用|\d)", s)[0]
    return s.strip(" ・")


def starts(name, stem):
    n = nfkc(name)
    if len(stem) < 3 or not n.startswith(stem):
        return False
    rest = n[len(stem):]
    return not rest or not KATA.match(rest[0]) or rest.startswith(FORMS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report")
    a = ap.parse_args()
    if not (ROOT / "data/bundles").is_dir():
        sys.exit("沒有 data/bundles（先還原 data/）")
    M, mname = load_master(a.master)
    if len(M) < MIN_ROWS:
        sys.exit(f"全件ファイル只有 {len(M)} 列，疑似下載或格式有問題，不補收")
    cfg = json.loads(CFG.read_text(encoding="utf-8"))["groups"]
    yj = {k: c[31].strip() for k, c in M.items()}
    kegg = {}
    for r in json.loads((ROOT / "data/raw/jp_fda_drugs.json").read_text(encoding="utf-8")):
        k = str(r.get("承認番号"))
        yj.setdefault(k, str(r.get("薬価基準コード") or ""))
        kegg[k] = r
    rows = list(csv.DictReader(open(MAP, encoding="utf-8-sig", newline="")))
    fields = list(rows[0].keys())
    dm0 = {r["承認番号"]: r["drugbank_id"] for r in rows if r["映射成功"] == "True" and r["drugbank_id"]}   # 覆寫前（原收集器用的）
    fixed = 0
    for r in rows:   # 人工對照覆寫 drug_mapping 的列
        g = cfg.get(yj.get(r["承認番号"], "")[:7])
        if g and (r["drugbank_id"] != (g["drugbank_id"] or "") or r["映射成功"] != ("True" if g["drugbank_id"] else "False")):
            r["drugbank_id"], r["映射成功"] = g["drugbank_id"] or "", "True" if g["drugbank_id"] else "False"
            r["映射來源"] = "manual_20261124:config/ingredient_groups.json"
            fixed += 1
    dm = {r["承認番号"]: r["drugbank_id"] for r in rows if r["映射成功"] == "True" and r["drugbank_id"]}
    gdb = defaultdict(set)
    for code, db in dm.items():
        if len(yj.get(code, "")) >= 7:
            gdb[yj[code][:7]].add(db)
    for g, v in cfg.items():
        gdb[g] = {v["drugbank_id"]}
    members = defaultdict(list)
    for code in M:
        if len(yj[code]) >= 7:
            members[yj[code][:7]].append(code)

    pages = {p.stem for p in (ROOT / "docs/_drugs").glob("*.md") if "layout: id_redirect" not in p.read_text(encoding="utf-8")[:3000]}
    bundles = {}
    for f in sorted((ROOT / "data/bundles").glob("*/drug_bundle.json")):
        key = f.parent.name
        if key in pages or key.replace("_", "-") in pages:
            bundles[key] = (f, json.loads(f.read_text(encoding="utf-8")))
    # R2 用：每個證據包的先發商品名與一般名基本名
    stems = {}
    for key, (f, b) in bundles.items():
        if key in EXCLUDE:
            continue
        ids = set((b.get("pmda") or {}).get("drugbank_ids") or [])
        st = set()
        for code, db in dm.items():
            if db not in ids:
                continue
            kr = kegg.get(code) or {}
            for line in str(kr.get("商品名一覧") or "").split("\n"):
                if line.strip().startswith("後発品"):
                    break
                n = nfkc(re.sub(r"\s*\(.*\)\s*$", "", line))
                if len(n) >= 3 and KATA.match(n[0]):
                    st.add(n)
            if code in M and M[code][37].strip():
                bg = base_generic(M[code][37])
                if len(bg) >= 3 and "・" not in bg:
                    st.add(bg)
        stems[key] = st
    r2 = {}   # 群 → 證據包
    for g, codes in members.items():
        if gdb.get(g):
            continue
        hit = {key for key, st in stems.items() if all(any(starts(M[c][4], s) for s in st) for c in codes)}
        if len(hit) == 1:
            r2[g] = hit.pop()

    report, n_add, n_exc, touched = [], 0, 0, 0
    for key, (f, b) in bundles.items():
        p = b.get("pmda") or {}
        ids = set(p.get("drugbank_ids") or [])
        if key in EXCLUDE or not ids:
            continue
        recs = p.get("records") or []
        have = {str(r.get("license_id") or "").strip() for r in recs}
        have |= {str(r.get("license_id") or "").strip() for r in p.get("excluded_records") or []}
        counted = {c for c, d in dm0.items() if d in ids}   # 原收集器（覆寫前的 drug_mapping）算進 total_matches 的
        ch = False
        # 4. 排除：人工對照說是別的成分
        keep, gone = [], []
        for r in recs:
            g = yj.get(str(r.get("license_id") or "").strip(), "")[:7]
            if g in cfg and cfg[g]["drugbank_id"] not in ids:
                r = dict(r, excluded=time.strftime("%Y-%m-%d"),
                         reason=f"YJ {g}（{cfg[g]['name']}）は {cfg[g]['drugbank_id'] or '本站に対照なし'}、本薬（{'、'.join(sorted(ids))}）ではない：{cfg[g]['basis']}")
                gone.append(r)
            else:
                keep.append(r)
        # 原 drug_mapping 算進 total_matches、沒存成紀錄、人工對照後不屬本藥的品目
        uncounted = {c for c in counted if yj.get(c, "")[:7] in cfg and cfg[yj[c][:7]]["drugbank_id"] not in ids
                     and c not in {str(r.get("license_id")) for r in gone} and c in kegg}
        if gone or uncounted:
            p["records"] = recs = keep
            p.setdefault("excluded_records", []).extend(gone)
            p["total_matches"] = max(len(recs), int(p.get("total_matches") or 0) - len(gone) - len(uncounted))
            p["found"] = bool(recs)
            n_exc += len(gone)
            ch = True
            for r in gone:
                report.append((key, "exclude", r["license_id"], r.get("brand_name_zh", ""), yj.get(r["license_id"], "")[:7]))
            for c in sorted(uncounted):
                report.append((key, "uncount", c, kegg[c].get("販売名", ""), yj[c][:7]))
        # 2./3. 補收
        new = []
        for g, codes in members.items():
            db = gdb.get(g, set())
            rule = "R1" if len(db) == 1 and db <= ids else ("R2" if r2.get(g) == key else None)
            if g in cfg and cfg[g]["drugbank_id"] in ids:
                rule = "人工対照 config/ingredient_groups.json"
            if not rule:
                continue
            for c in sorted(codes):
                if c in have or c in counted:
                    continue
                new.append(record(M[c], mname, g, "R1：同群に drug_mapping の対照あり" if rule == "R1" else rule))
                report.append((key, rule, c, M[c][4], g))
        if new:
            n0 = len(recs)
            tm = int(p.get("total_matches") or 0)
            recs.extend(new)
            p["records"] = recs
            p["total_matches"] = tm + len(new) if tm >= n0 else len(recs)
            p["found"] = True
            n_add += len(new)
            ch = True
        if ch:
            touched += 1
            b["pmda"] = p
            if not a.dry_run:
                f.write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if fixed and not a.dry_run:
        with open(MAP, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
    if a.report:
        with open(a.report, "w", encoding="utf-8") as fh:
            fh.write("bundle\trule\tcode\tname\tyj7\n")
            for x in report:
                fh.write("\t".join(map(str, x)) + "\n")
    print(f"{'（試跑）' if a.dry_run else ''}依成分補收 {n_add} 筆、排除 {n_exc} 筆、{touched} 個證據包；drug_mapping.csv 覆寫 {fixed} 列（{mname}）")


if __name__ == "__main__":
    main()
