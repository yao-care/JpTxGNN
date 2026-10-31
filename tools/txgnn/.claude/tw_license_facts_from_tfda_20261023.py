"""Tw 的 license_facts 改從 TwTxGNN/snapshots/tfda_licenses.json.gz 匯出（2026-10-23，pm 同意：Tw 以 tfda_licenses 為準）。
原本的 facts 來自 reviewer._local_regulatory（證據包裡的 TFDA 紀錄），與頁面上 tfda_licenses.py 依資料集 36 產生的許可證表有 66 頁張數不同
（例：acitretin 頁面含陸輸原料藥「阿西視網酸（粉）」，facts 沒有）。頁面不動，facts 跟著頁面的來源走。
  total＝不重複許可證號；valid＝status valid（單方＋複方）；cancelled＝cancelled＋expired
  market_status：valid>0 → Marketed；有許可證但都無效 → Cancelled only；快照沒有該藥 → 保留舊值並註明
每筆加 source、snapshot_date；舊值存在 previous（reviewer 來源）以便比對。
用法（母目錄）：python3 .claude/tw_license_facts_from_tfda_20261023.py
"""
import gzip
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
F = BASE / ".claude/cache/license_facts/TwTxGNN.json"


def main():
    snap = json.load(gzip.open(BASE / "TwTxGNN/snapshots/tfda_licenses.json.gz"))
    meta = snap["meta"]
    src = f"{meta['source']}；TwTxGNN/snapshots/tfda_licenses.json.gz（tfda_licenses.py 產生，與頁面許可證表同一份）"
    old = json.loads(F.read_text(encoding="utf-8"))
    new, diff = {}, 0
    for k in sorted(set(old) | set(snap["drugs"])):
        o = old.get(k)
        if k not in snap["drugs"]:
            new[k] = dict(o, source="reviewer._local_regulatory（tfda 快照沒有此藥，沿用）", snapshot_date=None)
            continue
        lic = {}
        for l in snap["drugs"][k]["licenses"]:
            lic.setdefault(l["id"], "valid" if l["status"] == "valid" else l["status"])
        v = sum(1 for s in lic.values() if s == "valid")
        rec = {"market_status": "Marketed" if v else ("Cancelled only" if lic else "Not marketed"),
               "total": len(lic), "valid": v, "cancelled": len(lic) - v, "partial": False, "licenses": lic,
               "source": src, "snapshot_date": meta["data_date"]}
        if o:
            rec["previous"] = {x: o.get(x) for x in ("market_status", "total", "valid", "cancelled")}
            diff += (o.get("total"), o.get("valid")) != (rec["total"], rec["valid"])
        new[k] = rec
    F.write_text(json.dumps(new, ensure_ascii=False, indent=1), encoding="utf-8")
    print("藥", len(new), "張數與舊 facts 不同", diff)


if __name__ == "__main__":
    main()
