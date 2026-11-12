"""證據包 local_regulatory 用各站目前的 _local_regulatory 重算（2026-11-12，不呼叫模型）。

背景：各站 Release 的證據包（data/evidence_packs/<藥>/*_drug_evidence_pack.json）多數是 2026-10-15 產生的；當時
_local_regulatory 把「許可證 status 欄有值」一律算成註銷（2026-10-17 才改成只認註銷類字樣），所以 Jp（有効）、NO（Authorised）、
NZ 等站有效的許可證在證據包裡全標 cancelled、market_status＝Cancelled only。證據包是公開 Release 的一部分，
母目錄的重產路線（regen_writer_20261027.build_pack）也會把它交給模型；build_pack 已改成整組換成事實層，這支把證據包本身修正。

做法：每站在站目錄用該站自己的 reviewer.drug_evidence_pack.DrugEvidencePackGenerator._local_regulatory 從 bundle 重算，
證據包的 local_regulatory 換成重算結果（保留產生時另外加的 dosage_forms_by_route），其他欄位不動；內容沒變就不改寫檔案。
各站的狀態字樣對照都在各站自己那份程式（不互相覆寫）。

用法（母目錄，站的 data/ 已從 Release 還原）：
  python3 .claude/refresh_pack_regulatory_20261112.py --check [站 ...]   # 只量：幾個證據包、市場狀態或逐張狀態會變
  python3 .claude/refresh_pack_regulatory_20261112.py [站 ...]           # 改寫證據包（只改本機 data/，要另外發 Release 才會上線）
  --json：最後一行印出 {"stats","changed"}（每週許可證排程 license_refresh_20261029.py 步驟 2c 用；同步進各站 tools/txgnn）
"""
import sys as _sys, pathlib as _pl; _sys.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import site_registry as _site_registry  # noqa: E402  # 30 站名單（不含 CnTxGNN）
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
KEEP = ("dosage_forms_by_route",)  # 產生器在 _local_regulatory 之外加的欄位
CODE = r'''
import collections, glob, importlib, json, sys, types
from pathlib import Path
sys.path.insert(0, "src")
try:
    import httpx  # noqa: F401  收集器才用得到；這裡只為了 import 套件
except ImportError:
    sys.modules["httpx"] = types.ModuleType("httpx")
G = importlib.import_module(sys.argv[1] + ".reviewer.drug_evidence_pack").DrugEvidencePackGenerator
write, keep = sys.argv[2] == "1", json.loads(sys.argv[3])
st, changed = collections.Counter(), []
for pk in sorted(glob.glob("data/evidence_packs/*/*_drug_evidence_pack.json")):
    name = Path(pk).parent.name
    bf = Path("data/bundles") / name / "drug_bundle.json"
    if not bf.exists():
        st["no_bundle"] += 1
        continue
    pack = json.load(open(pk, encoding="utf-8"))
    old = pack.get("local_regulatory") or {}
    new = G._local_regulatory(types.SimpleNamespace(**json.load(open(bf, encoding="utf-8"))))
    new.update({k: old[k] for k in keep if k in old})
    st["packs"] += 1
    ol = {x.get("license_number"): x.get("status") for x in old.get("licenses") or []}
    diff = sum(1 for x in new.get("licenses") or [] if ol.get(x["license_number"]) not in (None, x["status"]))
    st["licences"] += len(new.get("licenses") or [])
    st["licence_status_changed"] += diff
    if old.get("market_status") != new.get("market_status"):
        st[f"market_status {old.get('market_status')} -> {new.get('market_status')}"] += 1
    if old == new:
        continue
    st["packs_changed"] += 1
    changed.append(name)
    if write:
        pack["local_regulatory"] = new
        Path(pk).write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"stats": dict(st), "changed": changed}, ensure_ascii=False))
'''


def pkg_of(site):
    src = BASE / site / "src"
    for p in sorted(src.iterdir()):
        if (p / "reviewer/drug_evidence_pack.py").exists():
            return p.name
    return None


def main(argv):
    write = "--check" not in argv
    sites = [a for a in argv if not a.startswith("--")] or [p.name for p in _site_registry.glob_sites(BASE)]
    bad = 0
    for s in sites:
        pkg = pkg_of(s)
        if not pkg or not (BASE / s / "data/evidence_packs").is_dir():
            print(f"- {s}: 沒有 reviewer 或沒有還原 data/evidence_packs，略過")
            continue
        r = subprocess.run([sys.executable, "-c", CODE, pkg, "1" if write else "0", json.dumps(KEEP)],
                           cwd=BASE / s, capture_output=True, text=True, timeout=3600)
        if r.returncode != 0:
            bad += 1
            print(f"✗ {s}: {r.stderr.strip()[-300:]}")
            continue
        out = json.loads(r.stdout.strip().splitlines()[-1])
        if "--json" in argv:  # 給 license_refresh_20261029.py 讀（最後一行是 JSON）
            print(json.dumps(out, ensure_ascii=False), flush=True)
            continue
        print(f"{'✎' if write else '·'} {s}: {json.dumps(out['stats'], ensure_ascii=False)}", flush=True)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
