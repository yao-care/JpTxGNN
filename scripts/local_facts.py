#!/usr/bin/env python3
"""說明頁與證據等級頁的在地資料（2026-11-19 用戶決定的第一批改版）。不用 AI、不讀網路，只讀本站 repo 裡的檔案。

母目錄 .claude/local_facts_lib.py 與各站 scripts/local_facts.py 是同一份（逐站複製，不經 sync_site_tools）。
產生兩個資料檔，頁面用 Liquid 讀（頁面區塊由母目錄 .claude/gen_local_pages_20261119.py 寫入）：

  docs/_data/local_facts.json          說明頁（about／guide／sources／downloads／methodology）的本站資料：
                                       報告藥數與等級分布、本站資料（snapshots/*_licenses.json.gz 的事實層）有幾個藥有現行品項、
                                       查核紀錄數與更正頁數、FHIR 資源數、品項最多的藥、查核紀錄最多的藥
  docs/_data/evidence_tier_facts.json  證據等級頁（high＝L1/L2、medium＝L3/L4、low＝L5）每個藥一列：
                                       主預測新適應症、本地資料的品項數與現行品項數、查核紀錄數、是否本站獨有預測

「本站獨有」「30 站中位數」要讀 30 站，放在 cross 欄位，只由母目錄產生器更新；本檔 --write 保留原值、--check 不比。
用法（站上）：
  python3 scripts/local_facts.py --write   重算兩個檔（apply_drug_reviews.py、build_license_snapshot.py 結尾會自動跑）
  python3 scripts/local_facts.py --check   跟重算結果比，過期就 exit 1（check_seo_docs.py 的 gate 項目）
"""
import gzip
import json
import re
import sys
import unicodedata
from pathlib import Path

FM = re.compile(r"\A﻿?---\r?\n(.*?)\r?\n---\r?\n", re.S)
TIERS = {"high": ("L1", "L2"), "medium": ("L3", "L4"), "low": ("L5",)}
LF, TF = "docs/_data/local_facts.json", "docs/_data/evidence_tier_facts.json"
EV_PAGES = {"high": "docs/evidence-high.md", "medium": "docs/evidence-medium.md", "low": "docs/evidence-low.md"}


def slugify(s):
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"^-|-$", "", re.sub(r"(?:[^\w]|_)+", "-", s)).lower()


def _g(fm, k):
    m = re.search(rf"^{k}:\s*(.+?)\s*$", fm, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else ""


# 主預測前面的固定說法（各站 description 的寫法；取本地寫法時拿掉）
_PREFIX = re.compile(r"^(?:vorhergesagte neue Indikation|forudsagt ny indikation|ennustettu uusi käyttöaihe|indikasi baharu diramal|"
                     r"predikert ny indikasjon|predikterad ny indikation|voorspelde nieuwe indicatie|nueva indicación predicha|"
                     r"nova indicação prevista|nouvelle indication prédite|nuova indicazione prevista|predicted new indication|"
                     r"預測新適應症為|預測新適應症|予測新適応症は|예측 신규 적응증은|예측 신규 적응증|الاستطباب الجديد المتوقع|"
                     r"ข้อบ่งใช้ใหม่ที่คาดการณ์)\s*[:：]?\s*", re.I)


def main_indication(desc, preds):
    """主預測（description 寫的那一個；description 沒寫就取 predicted_indications 第一個）→ (本地寫法, 英文)。
    description 的寫法是「…<本地寫法> (<英文>)…」；取不到本地寫法就回英文"""
    for eng in preds:
        for a, b in (("(", ")"), ("（", "）")):
            i = desc.find(a + eng + b)
            if i > 0:
                head = desc[:i].rstrip()
                cut = max(head.rfind(c) for c in (",", "，", ":", "：", "、", "؛", "،", " – ", "—"))
                loc = _PREFIX.sub("", head[cut + 1:].strip(" *\"'“”「」"))
                for c in ("は", "은", "는"):
                    if c in loc and loc.index(c) < len(loc) - 1:
                        loc = loc.split(c, 1)[1].strip()
                if not loc or len(loc) > 90 or loc.lower() == eng.lower() or re.search(r"\b(L[1-5]|DB\d+)\b", loc):
                    return eng, eng
                return loc, eng
    return (preds[0], preds[0]) if preds else ("", "")


def _mk_ids(root):
    """FHIR MedicationKnowledge 的 id（多半＝頁名）→ DrugBank ID；front matter 沒有 drugbank_id 的頁用它補"""
    out = {}
    for f in (root / "docs/fhir/MedicationKnowledge").glob("*.json") if (root / "docs/fhir/MedicationKnowledge").is_dir() else []:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        code = next((c.get("code") for c in (d.get("code") or {}).get("coding", []) if str(c.get("code", "")).startswith("DB")), None)
        if code:
            out[str(d.get("id") or f.stem).lower()] = code
    return out


def public_pages(root):
    out = []
    mk = _mk_ids(root)
    for f in sorted((root / "docs/_drugs").glob("*.md")):
        t = f.read_text(encoding="utf-8", errors="replace")
        m = FM.match(t)
        fm = m.group(1) if m else ""
        if re.search(r"^layout:\s*id_redirect", fm, re.M) or re.search(r"^noindex:\s*true", fm, re.M) or 'http-equiv="refresh"' in t[:3000]:
            continue
        try:
            pred = [str(x).strip() for x in json.loads(_g(fm, "predicted_indications") or "[]")]
        except ValueError:
            pred = []
        out.append({"stem": f.stem, "title": _g(fm, "title") or f.stem, "url": f"/drugs/{slugify(f.stem)}/",
                    "level": _g(fm, "evidence_level"), "pred": pred, "desc": _g(fm, "description"),
                    "dbid": _g(fm, "drugbank_id") or mk.get(f.stem.lower(), "")})
    return out


def licence_facts(root):
    """頁名（小寫）→ {total, valid}；本站 snapshots/*_licenses.json.gz 的事實層（Tw 是許可證清單）"""
    snaps = sorted((root / "snapshots").glob("*_licenses.json.gz"))
    if not snaps:
        return None, {}
    d = json.loads(gzip.open(snaps[0]).read())
    out = {}
    for k, v in d.get("drugs", {}).items():
        if isinstance(v, list) or (isinstance(v, dict) and isinstance(v.get("licenses"), list)):
            lic = v if isinstance(v, list) else v["licenses"]
            ids = {x.get("id"): x.get("status") for x in lic}
            out[k.lower()] = {"total": len(ids), "valid": sum(1 for s in ids.values() if s == "valid"), "partial": False}
        elif isinstance(v, dict) and isinstance(v.get("facts"), dict):
            fc = v["facts"]
            out[k.lower()] = {"total": int(fc.get("total") or 0), "valid": int(fc.get("valid") or 0), "partial": bool(fc.get("partial"))}
    return snaps[0].name, out


def _short(s, n=110):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    s = re.sub(r"[*_`|]", "", s)
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0] if " " in s[:n] else s[:n]
    return cut.rstrip(",;:、，") + "…"


def review_counts(root):
    """回傳 (全部紀錄, 頁名→筆數, 頁名→最新一筆的摘要與日期)；摘要取紀錄的 summary（站上語言，查核紀錄表本來就公開）"""
    f = root / "docs/_data/drug_reviews.json"
    if not f.exists():
        return [], {}, {}
    recs = json.loads(f.read_text(encoding="utf-8")).get("records", [])
    per, last = {}, {}
    for r in recs:
        d = (r.get("drug") or "").lower()
        if not d:
            continue
        per[d] = per.get(d, 0) + 1
        s = r.get("summary") or ""
        if s and r.get("status") not in ("superseded", "withdrawn"):
            k = (r.get("action") != "mechanism", str(r.get("checked") or ""), str(r.get("id") or ""))  # 作用機轉紀錄是固定句型，排在更正之後
            if d not in last or k > last[d][0]:
                last[d] = (k, _short(s), str(r.get("checked") or ""), str(r.get("id") or ""), r.get("action") != "mechanism")
    return recs, per, last


def compute(root):
    root = Path(root)
    stats = json.loads((root / "docs/_data/drug_stats.json").read_text(encoding="utf-8"))
    pages = public_pages(root)
    snap, lic = licence_facts(root)
    recs, per_rev, last_rev = review_counts(root)
    fhir = root / "docs/fhir"
    n_mk = len(list((fhir / "MedicationKnowledge").glob("*.json"))) if (fhir / "MedicationKnowledge").is_dir() else 0
    n_cud = len(list((fhir / "ClinicalUseDefinition").glob("*.json"))) if (fhir / "ClinicalUseDefinition").is_dir() else 0
    rows = []
    for p in pages:
        lf = lic.get(p["stem"].lower())
        loc, eng = main_indication(p["desc"], p["pred"])
        rows.append({"s": p["stem"], "t": p["title"], "u": p["url"], "l": p["level"],
                     "i": loc, "ie": eng,
                     "lt": lf["total"] if lf else None, "lv": lf["valid"] if lf else None,
                     "lp": bool(lf and lf["partial"]), "r": per_rev.get(p["stem"].lower(), 0),
                     "rs": (last_rev.get(p["stem"].lower()) or (0, ""))[1],
                     "rk": (last_rev.get(p["stem"].lower()) or ((), "", "", "", False))[2:]})
    with_data = [r for r in rows if r["lt"]]
    key = lambda r: r["t"].lower()
    top_lic = sorted([r for r in with_data if r["lv"]], key=lambda r: (-r["lv"], key(r)))[:8]
    no_valid = sorted([r for r in with_data if r["lv"] == 0], key=key)
    top_rev = sorted([r for r in rows if r["r"]], key=lambda r: (-r["r"], key(r)))[:6]
    pick = lambda r: {"t": r["t"], "u": r["u"], "l": r["l"], "lt": r["lt"], "lv": r["lv"], "r": r["r"], "i": r["i"]}
    lc = stats.get("level_counts", {})
    acts = {}
    for r in recs:
        acts[r.get("action") or "?"] = acts.get(r.get("action") or "?", 0) + 1
    local = {
        "_about": "本檔由 scripts/local_facts.py 產生（母目錄 .claude/local_facts_lib.py），勿手改；cross 欄位由母目錄 .claude/gen_local_pages_20261119.py 更新",
        "drugs_total": stats.get("total_drugs", 0),
        "level_counts": {k: lc.get(k, 0) for k in ("L1", "L2", "L3", "L4", "L5")},
        "level_na": stats.get("total_drugs", 0) - sum(lc.get(k, 0) for k in ("L1", "L2", "L3", "L4", "L5")),
        "public_pages": len(rows),
        "licence_snapshot": snap,
        "licence": {
            "drugs_with_data": len(with_data),
            "drugs_with_current": sum(1 for r in with_data if r["lv"]),
            "drugs_none_current": len(no_valid),
            "drugs_without_data": len(rows) - len(with_data),
            "drugs_partial": sum(1 for r in with_data if r["lp"]),
            "items_total": sum(r["lt"] for r in with_data),
            "items_current": sum(r["lv"] for r in with_data),
        },
        "reviews": {"records": len(recs), "pages": len({(r.get("drug") or "").lower() for r in recs if r.get("drug")}),
                    "public_pages_with_records": sum(1 for r in rows if r["r"]), "by_action": dict(sorted(acts.items()))},
        "fhir": {"medication_knowledge": n_mk, "clinical_use_definition": n_cud},
        "top_licensed": [pick(r) for r in top_lic],
        "no_current": [pick(r) for r in no_valid[:12]],
        "no_current_more": max(0, len(no_valid) - 12),
        "most_reviewed": [pick(r) for r in top_rev],
    }
    def _count(rel, key=None):
        f = root / rel
        if not f.exists():
            return None
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            return None
        if isinstance(d, dict):
            for k in (key, "drugs", "items", "entries"):
                if k and isinstance(d.get(k), list):
                    return len(d[k])
            return None
        return len(d) if isinstance(d, list) else None
    exs = sorted([r for r in rows if r["lt"] and r["lv"] and r["i"] and r["l"] in ("L1", "L2", "L3", "L4", "L5")],
                 key=lambda r: (r["l"], -r["lv"], key(r)))
    local["example"] = pick(exs[0]) if exs else None
    rec = sorted([r for r in rows if r["rs"] and r["rk"][2]], key=lambda r: (r["rk"][0], r["rk"][1]), reverse=True)
    local["recent_reviews"] = [{"t": r["t"], "u": r["u"], "s": r["rs"], "d": r["rk"][0]} for r in rec[:24]]
    lic_rec = [r for r in rec if re.search(r"-(lic|row)-", r["rk"][1])]
    local["recent_licence_reviews"] = [{"t": r["t"], "u": r["u"], "s": r["rs"], "d": r["rk"][0]} for r in lic_rec[:8]]
    local["files"] = {"search_index": _count("docs/data/search-index.json", "drugs"), "drugs_json": _count("docs/data/drugs.json", "drugs")}
    local["by_level"] = {lv: {"n": sum(1 for r in rows if r["l"] == lv), "current": sum(1 for r in rows if r["l"] == lv and r["lv"])}
                         for lv in ("L1", "L2", "L3", "L4", "L5")}
    tiers = {"_about": local["_about"]}
    for tier, lvs in TIERS.items():
        tr = [r for r in rows if r["l"] in lvs]
        tr.sort(key=lambda r: (r["l"], -(r["lv"] or 0) if tier == "low" else 0, key(r)))
        cur = [r for r in tr if r["lv"]]
        tiers[tier] = {
            "count": len(tr), "by_level": {lv: sum(1 for r in tr if r["l"] == lv) for lv in lvs},
            "with_current": len(cur), "none_current": sum(1 for r in tr if r["lt"] and r["lv"] == 0),
            "without_data": sum(1 for r in tr if not r["lt"]), "with_reviews": sum(1 for r in tr if r["r"]),
            "rows": [{k: r[k] for k in ("t", "u", "l", "i", "lt", "lv", "r", "rs")} for r in tr],
            "none_current_list": [{"t": r["t"], "u": r["u"]} for r in tr if r["lt"] and r["lv"] == 0][:15],
        }
    return local, tiers


def merge_cross(new_local, new_tiers, old_local, old_tiers):
    """保留母目錄寫的 cross 欄位（本站獨有、30 站比較）：每列依網址接回"""
    if old_local and "cross" in old_local:
        new_local["cross"] = old_local["cross"]
    if old_tiers:
        for tier in TIERS:
            o = old_tiers.get(tier) or {}
            if "cross" in o:
                new_tiers[tier]["cross"] = o["cross"]
            uniq = {r["u"]: r.get("x") for r in o.get("rows", [])}
            for r in new_tiers[tier]["rows"]:
                r["x"] = uniq.get(r["u"])
            if "meta" in o:
                new_tiers[tier]["meta"] = o["meta"]
    return new_local, new_tiers


def strip_cross(d):
    d = json.loads(json.dumps(d))
    d.pop("cross", None)
    for tier in TIERS:
        if tier in d:
            d[tier].pop("cross", None)
            d[tier].pop("meta", None)
            for r in d[tier].get("rows", []):
                r.pop("x", None)
    return d


def dumps(d):
    return json.dumps(d, ensure_ascii=False, indent=1, sort_keys=False) + "\n"


def meta_description(tiers, tier):
    """證據等級頁 front matter description：模板（母目錄寫進 meta.template）＋本頁藥數＋代表藥（依等級、名稱排序的第一個）"""
    m = (tiers.get(tier) or {}).get("meta")
    if not m:
        return None
    t = tiers[tier]
    ex = ", ".join(r["t"] for r in t["rows"][:3])
    return (m["template"] if t["count"] else m["template_empty"]).format(n=t["count"], ex=ex)


def sync_descriptions(root, tiers, write):
    """回傳描述跟資料不符的頁；write 時改 front matter description 那一行"""
    bad = []
    for tier, rel in EV_PAGES.items():
        want = meta_description(tiers, tier)
        f = root / rel
        if want is None or not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        m = FM.match(t)
        cur = _g(m.group(1), "description") if m else None
        if cur != want:
            bad.append(rel)
            if write and m:
                line = "description: " + json.dumps(want, ensure_ascii=False)
                fm = re.sub(r"^description:.*$", lambda _: line, m.group(1), count=1, flags=re.M) if re.search(r"^description:", m.group(1), re.M) \
                    else m.group(1) + "\n" + line
                f.write_text(t[:m.start(1)] + fm + t[m.end(1):], encoding="utf-8")
    return bad


def run(root, mode):
    root = Path(root)
    lp, tp = root / LF, root / TF
    old_l = json.loads(lp.read_text(encoding="utf-8")) if lp.exists() else None
    old_t = json.loads(tp.read_text(encoding="utf-8")) if tp.exists() else None
    new_l, new_t = compute(root)
    new_l, new_t = merge_cross(new_l, new_t, old_l, old_t)
    if mode == "write":
        for p, d, o in ((lp, new_l, old_l), (tp, new_t, old_t)):
            if o != d:
                p.write_text(dumps(d), encoding="utf-8")
        sync_descriptions(root, new_t, True)
        return 0
    errs = []
    if old_l is None or old_t is None:
        errs.append("缺 docs/_data/local_facts.json 或 evidence_tier_facts.json")
    else:
        if strip_cross(old_l) != strip_cross(new_l):
            errs.append("docs/_data/local_facts.json 過期")
        if strip_cross(old_t) != strip_cross(new_t):
            errs.append("docs/_data/evidence_tier_facts.json 過期")
        errs += [f"{p} 的 description 跟 evidence_tier_facts.json 不符" for p in sync_descriptions(root, old_t, False)]
    for e in errs:
        print("✗ " + e + "（重跑 python3 scripts/local_facts.py --write）")
    return 1 if errs else 0


if __name__ == "__main__":
    here = Path(__file__).resolve()
    root = Path(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--root=")), here.parents[1]))
    sys.exit(run(root, "write" if "--write" in sys.argv else "check"))
