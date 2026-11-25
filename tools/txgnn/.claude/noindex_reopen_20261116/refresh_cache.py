"""母目錄事實快取 .claude/cache/license_facts/<站>.json 依站上快照 snapshots/*_licenses.json.gz 的 facts 更新。

用法（母目錄）：python3 .claude/noindex_reopen_20261116/refresh_cache.py <站> [...]   （無條件從快照覆寫有 facts 的頁）
2026-11-25 起 check_drug_page.py／checker_trend.py 跑之前也呼叫 refresh(site, only_if_newer=True)：快照檔比快取新才更新
（排程裡 dump_license_facts 剛重算的快取比快照新，不會被舊快照蓋掉）。各站 tools/txgnn 同步同一份（sync_site_tools.py）。
"""
import glob
import gzip
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]


def snapshot_path(site):
    f = sorted(glob.glob(str(BASE / site / "snapshots" / "*_licenses.json.gz")))
    return Path(f[0]) if f else None


def cache_path(site):
    return BASE / ".claude/cache/license_facts" / f"{site}.json"


def refresh(site, only_if_newer=False):
    """回傳 (狀態, 更新筆數)。狀態：updated／fresh（快取不比快照舊）／no_snapshot／no_facts（快照沒有 facts，例 Tw）。
    快照讀不到或壞掉直接 raise（不當成沒有資料）。"""
    sp, cp = snapshot_path(site), cache_path(site)
    if sp is None:
        return "no_snapshot", 0
    if only_if_newer and cp.exists() and cp.stat().st_mtime >= sp.stat().st_mtime:
        return "fresh", 0
    snap = json.loads(gzip.open(sp).read())["drugs"]
    if not any(e.get("facts") for e in snap.values()):
        if site == "TwTxGNN" and cp.exists():
            # Tw 的快照是 tfda_licenses（不存 facts）；事實層由 tw_license_facts_from_tfda 從同一份快照算（同 dump_license_facts 的 Tw 分支）
            import importlib.util
            import contextlib
            import io
            before = json.loads(cp.read_text(encoding="utf-8"))
            sp_ = importlib.util.spec_from_file_location("twf", BASE / ".claude/tw_license_facts_from_tfda_20261023.py")
            m = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(m)
            with contextlib.redirect_stdout(io.StringIO()):
                m.main()
            after = json.loads(cp.read_text(encoding="utf-8"))
            key = lambda e: tuple((e or {}).get(x) for x in ("market_status", "total", "valid", "cancelled", "licenses"))
            return "updated", sum(key(before.get(k)) != key(after.get(k)) for k in set(before) | set(after))
        return "no_facts", 0
    try:
        c = json.loads(cp.read_text(encoding="utf-8")) if cp.exists() else {}
    except ValueError:
        c = {}
    n = 0
    for page, e in snap.items():
        if e.get("facts"):
            for k in {page, e.get("bundle") or page}:
                if c.get(k) != e["facts"]:
                    n += 1
                c[k] = e["facts"]
    cp.parent.mkdir(parents=True, exist_ok=True)
    cp.write_text(json.dumps(c, ensure_ascii=False), encoding="utf-8")  # 寫回也更新 mtime，下次不再比對
    return "updated", n


if __name__ == "__main__":
    for s in sys.argv[1:]:
        st, n = refresh(s)
        print(s, "updated" if st == "updated" else st, n)
