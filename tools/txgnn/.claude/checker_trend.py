"""全量 checker（check_drug_page.py）→ 各站非 0 頁數，往 .claude/state/checker_trend.json 後面加一筆（不覆寫）。2026-10-28。

範圍＝所有非轉址的藥物頁（2026-10-29 起；之前只算稽核分類表）；P7（FHIR／search-index 衍生檔）不算。
每筆：{date, site, nonzero, total, by_rule:{P2,P3,...}}。主機巡檢每天用 gh api 讀這個檔畫趨勢，連續 2 天沒下降就告警。
逐頁結果另寫 .claude/audit_20261016/checker_full/<date>.tsv（不進 git）。
用法（母目錄）：python3 .claude/checker_trend.py [--no-append] [站 ...]
"""
import csv
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from multiprocessing import Pool
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TREND = BASE / ".claude/state/checker_trend.json"


def _ck():
    s = importlib.util.spec_from_file_location("ck", BASE / ".claude/check_drug_page.py")
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def run_site(args):
    site, pages = args
    ck = _ck()
    cl = ck.classification()
    out = []
    for p in pages:
        f = BASE / site / "docs/_drugs" / f"{p}.md"
        if not f.exists():
            continue
        try:
            errs = sorted({e[0] for e in ck.check_page(site, f, cl.get((site, p), "keep"), False) if e[0] != "P7"})
        except Exception as e:
            errs = ["EXC"]
        out.append((site, p, cl.get((site, p), "keep"), ",".join(errs)))
    return out


def main(argv):
    only = {a for a in argv if a.endswith("TxGNN")}
    by_site = defaultdict(list)
    # 2026-10-29（pm 驗收）：範圍＝所有非轉址的藥物頁（含 noindex 頁、稽核分類表以外的頁），不只分類表
    for d in sorted(BASE.glob("*TxGNN")):
        if only and d.name not in only:
            continue
        for f in sorted((d / "docs/_drugs").glob("*.md")):
            head = f.read_text(encoding="utf-8", errors="replace")[:3000]
            if 'http-equiv="refresh"' in head or "layout: id_redirect" in head:
                continue
            by_site[d.name].append(f.stem)
    with Pool(6) as pool:
        res = [x for chunk in pool.map(run_site, sorted(by_site.items())) for x in chunk]
    now = datetime.now(timezone(timedelta(hours=8)))
    day = now.strftime("%Y-%m-%d")
    detail = BASE / ".claude/audit_20261016/checker_full" / f"{now.strftime('%Y%m%d_%H%M')}.tsv"
    detail.parent.mkdir(parents=True, exist_ok=True)
    with open(detail, "w", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t"); w.writerow(["site", "page", "class", "rules"]); w.writerows(res)
    recs = []
    for site in sorted(by_site):
        rows = [r for r in res if r[0] == site]
        nz = [r for r in rows if r[3]]
        recs.append({"date": day, "time": now.strftime("%H:%M"), "site": site, "nonzero": len(nz), "total": len(rows),
                     "by_rule": dict(sorted(Counter(c for r in nz for c in r[3].split(",")).items()))})
    if "--no-append" not in argv:
        TREND.parent.mkdir(parents=True, exist_ok=True)
        old = json.loads(TREND.read_text(encoding="utf-8")) if TREND.exists() else []
        TREND.write_text(json.dumps(old + recs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tot = sum(r["nonzero"] for r in recs)
    print(f"全部 {sum(r['total'] for r in recs)} 頁，非 0 {tot}；明細 {detail.relative_to(BASE)}")
    for r in recs:
        print(f"  {r['site']}\t{r['nonzero']}/{r['total']}\t{r['by_rule']}")


if __name__ == "__main__":
    main(sys.argv[1:])
