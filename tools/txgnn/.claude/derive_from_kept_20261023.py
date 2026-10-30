"""FHIR ClinicalUseDefinition 與 search-index.json 從 kept_predictions 產生（2026-10-23，pm：頁面、FHIR、search-index 一律從 kept 產生）。
取代 .claude/regen_fhir.py（讀 integrated_predictions，含 KG very_high）與 rebuild_search_index.py（解析頁面「NN.NN%」，分數改 0.xxxx 後失效）。

每個藥（只處理指定的頁）：
  FHIR：刪掉該藥（MedicationKnowledge id）的預測 CUD（個別檔與 Bundle 內的 entry），依 kept 重寫；
        格式沿用該站現有 CUD 當模板（沒有 CUD 的站用 TwTxGNN 的模板、網域換成該站）；
        extension：txgnn-score＝證據包分數（4 位）、evidence-level＝頁面上該預測的等級（找不到用 L5）、
        prediction-status＝predicted、source（模板有才寫）＝"TxGNN deep learning model"
  search-index：drugs[slug].indications＝kept（name＝「當地名 (English)」或英文、score＝百分比數字到 2 位、level 同上）、
        drugs[slug].level＝頁面 evidence_level；indications 反查表依全部 drugs 重建
已知用途頁、無預測頁：kept 為空 → 刪掉該藥全部預測 CUD、search-index 的 indications 清空。
用法（母目錄）：python3 .claude/derive_from_kept_20261023.py [--apply] --pages site:page,... | 站 ...
"""
import copy
import csv
import importlib.util
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


ck = _load("ck", BASE / ".claude/check_drug_page.py")
kf, amf = ck.kf, ck.amf


def slugify(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9()]+", "-", s.lower())).strip("-")


def site_host(site):
    cfg = (BASE / site / "docs/_config.yml").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^url:\s*[\"']?(https?://[^\"'\s]+)", cfg, re.M)
    return m.group(1).rstrip("/") if m else f"https://{site.lower()}.yao.care"


def template(site):
    d = BASE / site / "docs/fhir/ClinicalUseDefinition"
    f = next(iter(sorted(d.glob("*.json"))), None) if d.exists() else None
    if f:
        return json.loads(f.read_text(encoding="utf-8")), False
    t = json.loads(next(iter(sorted((BASE / "TwTxGNN/docs/fhir/ClinicalUseDefinition").glob("*.json")))).read_text(encoding="utf-8"))
    return json.loads(json.dumps(t).replace("https://twtxgnn.yao.care", site_host(site))), True


def page_levels(site, page_text, kept, preds):
    """kept 每個預測在頁面上的等級（逐列對應；概覽表等級列對應概覽預測列的病）"""
    fm, _, body = page_text[4:].partition("\n---")
    out = {}
    tbs = ck.tables(body)
    for hdr, rows, lines, _ in tbs:
        li = next((i for i, h in enumerate(hdr) if ck.LEVEL_ROW.search(h)), None)
        for cells, line in zip(rows, lines):
            lvc = cells[li] if li is not None and li < len(cells) else (cells[1] if len(cells) > 1 and ck.LEVEL_ROW.search(cells[0]) else "")
            m = ck.LEVEL.search(lvc or "")
            if not m:
                continue
            for k in kept:
                if k in out:
                    continue
                p = preds.get(ck.norm_name(k))
                hit = any(rx.search(line) for rx in ck.name_regexes(site, k))
                if not hit and p:
                    hit = any(abs(round(p["txgnn_score"] * 100, 2) - v * 100) < 0.005 or abs(round(p["txgnn_score"], 4) - v) < 0.00005
                              for v, _, _ in ck.score_tokens(line))
                if hit:
                    out[k] = m.group(1)
    ov = tbs[0][1] if tbs else []
    pr = next((r for r in ov if len(r) >= 2 and ck.PRED_ROW.search(r[0])), None)
    lr = next((r for r in ov if len(r) >= 2 and ck.LEVEL_ROW.search(r[0]) and ck.LEVEL.search(r[1])), None)
    if pr and lr:
        for k in kept:
            if k not in out and any(rx.search(" ".join(pr[1:])) for rx in ck.name_regexes(site, k)):
                out[k] = ck.LEVEL.search(lr[1]).group(1)
    return {k: out.get(k, "L5") for k in kept}


def local_label(site, en):
    locs = sorted(ck.local_names(site).get(ck.norm_name(en), ()), key=len)
    return f"{locs[0]} ({en})" if locs else en


def main(argv):
    apply_ = "--apply" in argv
    pages = None
    if "--pages" in argv:
        pages = {tuple(x.split(":", 1)) for x in argv[argv.index("--pages") + 1].split(",")}
    sites = [a for a in argv if a.endswith("TxGNN")] or sorted({p[0] for p in pages})
    for s in sites:
        root = BASE / s / "docs"
        todo = sorted(f.stem for f in (root / "_drugs").glob("*.md") if pages is None or (s, f.stem) in pages)
        cud, mk = ck.fhir(s)
        tpl, borrowed = template(s)
        cud_dir = root / "fhir/ClinicalUseDefinition"
        bundle_f = root / "fhir/Bundle/all-predictions.json"
        bundle = json.loads(bundle_f.read_text(encoding="utf-8")) if bundle_f.exists() else None
        idx_f = next((root / p for p in ("data/search-index.json", "assets/data/search-index.json", "search-index.json") if (root / p).exists()), None)
        idx = json.loads(idx_f.read_text(encoding="utf-8")) if idx_f else None
        drugs = {str(x.get("slug", "")).lower(): x for x in (idx.get("drugs", []) if isinstance(idx, dict) else [])}
        n_cud_del = n_cud_new = n_idx = 0
        no_mk = []
        for page in todo:
            f = root / "_drugs" / f"{page}.md"
            t = f.read_text(encoding="utf-8").replace("\r\n", "\n")
            if 'http-equiv="refresh"' in t[:3000]:
                continue
            b = amf.load_bundle(BASE / s, page)
            if b is None:
                continue
            d = b.get("drug") or {}
            preds = {ck.norm_name(p["disease_name"]): p for p in d.get("predicted_indications") or [] if p.get("disease_name")}
            kept = kf.kept_predictions(BASE / s, b)
            lv = page_levels(s, t, kept, preds)
            # FHIR
            keys = {ck.norm_name(page), ck.norm_name(page.replace("_", "-")), ck.norm_name(page.replace("-", "_")),
                    ck.norm_name(d.get("drugbank_id")), ck.norm_name(d.get("inn")), ck.norm_name(d.get("name"))} - {""}
            ids = [i for i, names in mk.items() if names & keys]
            if not ids:
                if kept:
                    no_mk.append(page)
            for mid in ids:
                if cud_dir.exists():
                    for cf in cud_dir.glob("*.json"):
                        try:
                            c = json.loads(cf.read_text(encoding="utf-8"))
                        except Exception:
                            continue
                        if ((c.get("subject") or [{}])[0].get("reference") or "").split("/")[-1] == mid and c.get("type") == "indication":
                            n_cud_del += 1
                            if apply_:
                                cf.unlink()
                if bundle:
                    before = len(bundle.get("entry", []))
                    bundle["entry"] = [e for e in bundle.get("entry", []) if not (
                        (e.get("resource") or {}).get("resourceType") == "ClinicalUseDefinition" and
                        (((e.get("resource") or {}).get("subject") or [{}])[0].get("reference") or "").split("/")[-1] == mid)]
                    n_cud_del += before - len(bundle["entry"])
                for k in kept:
                    p = preds.get(ck.norm_name(k))
                    c = copy.deepcopy(tpl)
                    c["id"] = f"{mid}-{slugify(k)}"
                    c["subject"] = [{"reference": f"MedicationKnowledge/{mid}"}]
                    c["indication"] = {"diseaseSymptomProcedure": {"concept": {"text": k}}}
                    exts = []
                    host = site_host(s)
                    for e in tpl.get("extension", []):
                        key = e.get("url", "").rsplit("/", 1)[-1]
                        e2 = {"url": e["url"]}
                        if key == "prediction-status":
                            e2["valueCode"] = "predicted"
                        elif key == "evidence-level":
                            e2["valueCode"] = lv.get(k, "L5")
                        elif "score" in key:
                            e2["valueDecimal"] = round(p["txgnn_score"], 4)
                        elif key == "source":
                            e2[next((x for x in e if x.startswith("value")), "valueString")] = "TxGNN deep learning model"
                        else:
                            e2 = copy.deepcopy(e)
                        exts.append(e2)
                    if not any("score" in e["url"].rsplit("/", 1)[-1] for e in exts):
                        exts.append({"url": f"{host}/fhir/StructureDefinition/txgnn-score", "valueDecimal": round(p["txgnn_score"], 4)})
                    c["extension"] = exts
                    n_cud_new += 1
                    if apply_:
                        cud_dir.mkdir(parents=True, exist_ok=True)
                        (cud_dir / f"{c['id']}.json").write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")
            # search-index
            x = drugs.get(page.lower()) or drugs.get(page.replace("_", "-").lower())
            if x is not None:
                fl = re.search(r"^evidence_level:\s*(\S+)", t, re.M)
                x["indications"] = [{"name": local_label(s, k), "score": round(preds[ck.norm_name(k)]["txgnn_score"] * 100, 2), "level": lv.get(k, "L5")}
                                    for k in kept if ck.norm_name(k) in preds]
                if fl:
                    x["level"] = fl.group(1)
                n_idx += 1
        if idx is not None and isinstance(idx, dict):
            cross = defaultdict(list)
            for x in idx.get("drugs", []):
                for i in x.get("indications") or []:
                    cross[i["name"]].append({"drug": x.get("name"), "slug": x.get("slug"), "score": i.get("score")})
            idx["indications"] = [{"name": n, "drug_count": len(v), "drugs": sorted(v, key=lambda y: -(y.get("score") or 0))[:10]}
                                  for n, v in sorted(cross.items())]
            idx["indication_count"] = len(idx["indications"])
            if apply_:
                idx_f.write_text(json.dumps(idx, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        if apply_ and bundle is not None:
            bundle_f.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
        ck.fhir.cache_clear(); ck.search_index.cache_clear()
        print(s, f"頁 {len(todo)}、刪 CUD {n_cud_del}、新 CUD {n_cud_new}、search-index {n_idx}、找不到 MK {len(no_mk)} {no_mk[:5]}"
              f"{'（CUD 模板借用 TwTxGNN）' if borrowed else ''}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
