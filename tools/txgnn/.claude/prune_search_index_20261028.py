"""search-index 拿掉 noindex 頁、轉址頁、已不存在的頁，反查表依剩下的 drugs 重建（2026-10-28）。

原因：derive_from_kept 只更新既有項目，2026-10-28 開了 449 頁 noindex 後，這些頁仍留在站內搜尋。
反查表重建方式同 derive_from_kept_20261023.py。可重複執行。
用法（母目錄）：python3 .claude/prune_search_index_20261028.py 站 ...
"""
import json, re, sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def public_slugs(site):
    out = set()
    for f in (BASE / site / "docs/_drugs").glob("*.md"):
        t = f.read_text(encoding="utf-8", errors="replace")[:3000]
        if 'http-equiv="refresh"' in t or "layout: id_redirect" in t or re.search(r"^noindex:\s*true", t, re.M):
            continue
        out |= {f.stem.lower(), f.stem.replace("_", "-").lower()}
    return out


def main(argv):
    for s in [a for a in argv if a.endswith("TxGNN")]:
        root = BASE / s / "docs"
        f = next((root / p for p in ("data/search-index.json", "assets/data/search-index.json", "search-index.json") if (root / p).exists()), None)
        if f is None:
            print(s, "沒有 search-index"); continue
        idx = json.loads(f.read_text(encoding="utf-8"))
        if not isinstance(idx, dict) or "drugs" not in idx:
            print(s, "格式不同，略過"); continue
        pub = public_slugs(s)
        before = len(idx["drugs"])
        idx["drugs"] = [x for x in idx["drugs"] if str(x.get("slug", "")).lower() in pub or str(x.get("slug", "")).replace("_", "-").lower() in pub]
        cross = defaultdict(list)
        for x in idx["drugs"]:
            for i in x.get("indications") or []:
                cross[i["name"]].append({"drug": x.get("name"), "slug": x.get("slug"), "score": i.get("score")})
        idx["indications"] = [{"name": n, "drug_count": len(v), "drugs": sorted(v, key=lambda y: -(y.get("score") or 0))[:10]}
                              for n, v in sorted(cross.items())]
        idx["indication_count"] = len(idx["indications"])
        if "drug_count" in idx:
            idx["drug_count"] = len(idx["drugs"])
        f.write_text(json.dumps(idx, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(s, f"search-index {before}→{len(idx['drugs'])}")


if __name__ == "__main__":
    main(sys.argv[1:])
