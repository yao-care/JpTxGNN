#!/usr/bin/env python3
"""重新生成單一站台的 FHIR ClinicalUseDefinition 資源。

用法:
    python3 .claude/regen_fhir.py <project_dir> [--apply]

為什麼需要這支工具：
各站 scripts/generate_fhir_resources.py 從 repurposing_candidates.csv.gz 取前
MAX_CUD_RESOURCES(50000) 列。在候選檔是未過濾 KG 笛卡爾積的站，那 5 萬列全部
落在最前面的 2-3 個藥身上（每個藥配掉整個疾病詞彙表），於是 FHIR 對外宣稱五萬筆
臨床用途、實際只涵蓋 3 個藥且內容無意義。舊腳本也從不清除已不存在的資源檔，
改資料後會留下大量孤兒。

取數規則與藥品頁一致（見 scripts/generate_drug_pages.py）：
  - 候選檔若已過濾就直接用，否則改用 integrated_predictions 並以 confidence
    收斂（very_high 優先，某藥若無才退回其 high）
  - 依 dl_score 排序後每個藥最多取 TOP_PER_DRUG 筆

各站的 CUD 結構彼此不同（id 大小寫、藥名 slug vs DrugBank ID、concept.text vs
coding、status 形態、extension 欄位都不一樣），所以這裡不套統一格式，而是讀該站
現有的一個資源當模板，只替換與資料相關的欄位，其餘原樣保留。
"""
import copy
import csv
import gzip
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

TOP_PER_DRUG = 50
UNFILTERED_THRESHOLD = 500   # 每藥列數超過此值視為未過濾的笛卡爾積


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-") or "unknown"


def pick(fields, *names):
    for n in names or []:
        if fields and n in fields:
            return n
    return None


def load_predictions(project: Path):
    """回傳 ({drugbank_id: [(indication, source), ...]}, 來源檔名, 是否用 integrated)。"""
    processed = project / "data" / "processed"
    cand = processed / "repurposing_candidates.csv.gz"
    integ = processed / "integrated_predictions.csv.gz"

    use_integrated = True
    if cand.exists():
        drugs, n = set(), 0
        with gzip.open(cand, "rt", encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            dcol = pick(r.fieldnames, "drugbank_id")
            for row in r:
                n += 1
                if dcol:
                    drugs.add(row[dcol])
                if n >= 200_000:
                    break
        use_integrated = (n / max(len(drugs), 1)) > UNFILTERED_THRESHOLD

    src = integ if use_integrated else cand
    if not src.exists():
        raise SystemExit(f"{project.name}: 找不到 {src.name}")

    per_drug = defaultdict(list)
    with gzip.open(src, "rt", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        fields = r.fieldnames or []
        dcol = pick(fields, "drugbank_id")
        icol = pick(fields, "potential_indication", "潛在新適應症", "disease_name")
        scol = pick(fields, "source", "來源")
        ccol = pick(fields, "confidence")
        sccol = pick(fields, "dl_score")
        if not dcol or not icol:
            raise SystemExit(f"{project.name}: 欄位對不上 {fields}")
        for row in r:
            did = (row.get(dcol) or "").strip()
            ind = (row.get(icol) or "").strip()
            if not did or not ind:
                continue
            conf = (row.get(ccol) or "") if ccol else ""
            if use_integrated and conf not in ("very_high", "high"):
                continue
            try:
                sc = float(row.get(sccol) or 0)
            except (TypeError, ValueError):
                sc = 0.0
            per_drug[did].append((ind, (row.get(scol) or "KG").strip(), conf, sc))

    out = {}
    for did, rows in per_drug.items():
        if use_integrated:
            vh = [x for x in rows if x[2] == "very_high"]
            rows = vh if vh else [x for x in rows if x[2] == "high"]
        seen, uniq = set(), []
        for ind, s, _c, _sc in sorted(rows, key=lambda x: -x[3]):
            if ind not in seen:
                seen.add(ind)
                uniq.append((ind, s))
        if uniq:
            out[did] = uniq[:TOP_PER_DRUG]
    return out, src.name, use_integrated


def mk_index(project: Path):
    """建立 {DRUGBANK_ID(大寫): MedicationKnowledge 資源 id}。

    各站的 MK id 慣例不同（DB01048 / db01048 / abacavir），一律從資源內容取
    DrugBank ID 來對應，不猜檔名。
    """
    mk_dir = project / "docs" / "fhir" / "MedicationKnowledge"
    idx = {}
    for p in mk_dir.glob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        did = None
        for c in (d.get("code") or {}).get("coding") or []:
            code = str(c.get("code") or "")
            if re.fullmatch(r"DB\d+", code, re.I):
                did = code
                break
        if not did:
            for ext in d.get("extension") or []:
                if str(ext.get("url", "")).endswith("drugbank-id"):
                    did = str(ext.get("valueString") or ext.get("valueCode") or "")
                    break
        if not did and re.fullmatch(r"db\d+", p.stem, re.I):
            did = p.stem
        if did:
            idx.setdefault(did.upper(), d.get("id") or p.stem)
    return idx


def build(template, mk_id, drug_id, indication, source):
    """以模板為基礎，替換與資料相關的欄位。"""
    r = copy.deepcopy(template)
    rid = f"{mk_id}-{slugify(indication)}"
    if len(rid) > 180:
        rid = rid[:180].rstrip("-")
    r["id"] = rid

    subj = {"reference": f"MedicationKnowledge/{mk_id}"}
    old = (template.get("subject") or [{}])[0]
    if "display" in old:
        subj["display"] = old.get("display")
    r["subject"] = [subj]

    dsp = ((r.get("indication") or {}).get("diseaseSymptomProcedure")) or {}
    if "concept" in dsp:
        dsp["concept"] = {"text": indication}
    else:
        # 舊版宣告 system 為 MONDO 卻填 row index，改用站內 CodeSystem
        base = ""
        for ext in template.get("extension") or []:
            m = re.match(r"(https://[^/]+)/fhir/", str(ext.get("url", "")))
            if m:
                base = m.group(1)
                break
        dsp["coding"] = [{"system": f"{base}/fhir/CodeSystem/predicted-indication",
                          "code": slugify(indication), "display": indication}]
        dsp["text"] = indication
    r.setdefault("indication", {})["diseaseSymptomProcedure"] = dsp

    for ext in r.get("extension") or []:
        url = str(ext.get("url", ""))
        if url.endswith("prediction-source"):
            ext["valueString"] = f"TxGNN {source}" if not source.startswith("TxGNN") else source
        elif url.endswith("drugbank-id"):
            if "valueCode" in ext:
                ext["valueCode"] = drug_id
            else:
                ext["valueString"] = drug_id
    return r


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    project = Path(sys.argv[1]).resolve()
    apply = "--apply" in sys.argv

    cud_dir = project / "docs" / "fhir" / "ClinicalUseDefinition"
    existing = sorted(cud_dir.glob("*.json")) if cud_dir.is_dir() else []
    if not existing:
        raise SystemExit(f"{project.name}: 沒有現成 CUD 可當結構模板")
    template = json.loads(existing[0].read_text(encoding="utf-8"))

    per_drug, src_name, used_integrated = load_predictions(project)
    idx = mk_index(project)

    matched = {d: v for d, v in per_drug.items() if d.upper() in idx}
    missing = sorted(set(per_drug) - set(matched))
    total = sum(len(v) for v in matched.values())
    print(f"{project.name}: 來源={src_name}"
          f"({'integrated+confidence' if used_integrated else '已過濾候選'}) "
          f"藥={len(matched)} CUD={total} 舊CUD={len(existing)} "
          f"對不到MK的藥={len(missing)}")
    if not apply:
        return

    shutil.rmtree(cud_dir)
    cud_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    used = set()
    collisions = 0
    for did, inds in sorted(matched.items()):
        mk_id = idx[did.upper()]
        for ind, source in inds:
            res = build(template, mk_id, did, ind, source)
            # 不同適應症可能產生相同 slug（標點差異），不處理會讓後者覆蓋前者而靜默掉檔
            rid = res["id"]
            if rid in used:
                collisions += 1
                n = 2
                while f"{rid}-{n}" in used:
                    n += 1
                rid = f"{rid}-{n}"
                res["id"] = rid
            used.add(rid)
            (cud_dir / f"{rid}.json").write_text(
                json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
            written += 1
    print(f"  寫入 {written} 個 ClinicalUseDefinition"
          f"（舊目錄已清除；slug 碰撞另加後綴 {collisions} 筆）")


main()
