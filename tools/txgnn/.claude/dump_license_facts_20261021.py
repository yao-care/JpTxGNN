"""軌 5 第二版的事實來源（2026-10-21）：每站用自己的 reviewer._local_regulatory（修正後：張數＝不重複許可證號、
partial_list、archivée／Opinion 判為無效）算出每個藥的市場狀態與逐張許可證狀態，寫到
.claude/cache/license_facts/<站>.json：{bundle 名: {market_status, total, valid, cancelled, partial, licenses: {字號: valid|cancelled}}}
不呼叫模型。用法（母目錄）：python3 .claude/dump_license_facts_20261021.py [站 ...]
"""
import sys as _sys, pathlib as _pl; _sys.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import site_registry as _site_registry  # noqa: E402  # 30 站名單（不含 CnTxGNN）
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CODE = r'''
import glob, importlib, json, sys, types
from pathlib import Path
G = importlib.import_module(sys.argv[1] + ".reviewer.drug_evidence_pack").DrugEvidencePackGenerator
out = {}
for f in sorted(glob.glob("data/bundles/*/drug_bundle.json")):
    try:
        lr = G._local_regulatory(types.SimpleNamespace(**json.load(open(f, encoding="utf-8"))))
    except Exception as e:
        out[Path(f).parent.name] = {"error": str(e)[:150]}
        continue
    lic = {x["license_number"]: x["status"] for x in lr.get("licenses", [])}
    _raw = json.load(open(f, encoding="utf-8"))  # 獸用許可（Dk 2026-11-05：veterinary_records，不算人用）
    vet = sum(len(x.get("veterinary_records") or []) for x in _raw.values() if isinstance(x, dict) and "records" in x)
    v = sum(1 for s in lic.values() if s == "valid")
    nm = sum(1 for s in lic.values() if s == "not_marketed")
    out[Path(f).parent.name] = {"market_status": lr.get("market_status"), "total": lr.get("total_licenses") if not lr.get("partial_list") else None,
                                "valid": v, "not_marketed": nm, "cancelled": sum(1 for s in lic.values() if s == "cancelled"),
                                **({"unknown": sum(1 for s in lic.values() if s == "unknown")} if "unknown" in lic.values() else {}), **({"unconfirmed": lr["unconfirmed"]} if lr.get("unconfirmed") else {}), **({"unconfirmed_ids": sorted(x["license_number"] for x in lr.get("licenses", []) if x.get("status_unconfirmed"))} if lr.get("unconfirmed") else {}), "partial": bool(lr.get("partial_list")), "licenses": lic, **({"veterinary": vet} if vet else {}),
                                **({"listed": lr["listed_products"]} if lr.get("listed_products") else {}),
                                **({"valid_single": sum(1 for x in lr.get("licenses", []) if x.get("kind") == "single" and x.get("status") == "valid"),
                                    "single_total": sum(1 for x in lr.get("licenses", []) if x.get("kind") == "single")}
                                   if any(x.get("kind") for x in lr.get("licenses", [])) else {}),  # 2026-11-06：單方有效張數（checker 的有效張數說法「N valid single-ingredient …」）
                                **{k: lr[k] for k in ("export_only", "export_total", "export_valid", "domestic_total") if lr.get("export_only")}}
json.dump(out, sys.stdout, ensure_ascii=False)
'''


def main(argv):
    sites = argv or sorted(p.name for p in _site_registry.glob_sites(BASE))
    d = BASE / ".claude/cache/license_facts"
    d.mkdir(parents=True, exist_ok=True)
    for s in sites:
        pkg = s.lower() if (BASE / s / "src" / s.lower()).is_dir() else \
            next(p.name for p in (BASE / s / "src").iterdir() if p.is_dir() and not p.name.startswith("."))  # Uk 另有 src/txgnn_backup
        r = subprocess.run(["uv", "run", "python", "-c", CODE, pkg], cwd=BASE / s, capture_output=True, text=True, timeout=3600)
        if r.returncode != 0:
            print(f"✗ {s}: {r.stderr[-200:]}")
            continue
        facts = json.loads(r.stdout)
        (d / f"{s}.json").write_text(json.dumps(facts, ensure_ascii=False), encoding="utf-8")
        print(f"{s}: {len(facts)} 藥，部分紀錄 {sum(1 for x in facts.values() if x.get('partial'))}", flush=True)
        if s == "TwTxGNN" and (BASE / s / "snapshots/tfda_licenses.json.gz").exists():
            # Tw 的 facts 以頁面許可證表的來源（tfda_licenses 快照）為準（pm 2026-10-23）；只用證據包算會跟頁面差 66 頁以上。
            # 2026-10-31：原本要另外手動跑，全站重算時漏掉、Tw 排程也沒跑 → 寫進這裡，一律接著覆蓋
            subprocess.run([sys.executable, str(BASE / ".claude/tw_license_facts_from_tfda_20261023.py")], check=True)


if __name__ == "__main__":
    main(sys.argv[1:])
