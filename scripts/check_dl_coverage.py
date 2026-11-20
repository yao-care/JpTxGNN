#!/usr/bin/env python3
"""證據包有沒有漏收 DL 預測（2026-11-16 建，check_seo_docs.py 的一項）。

2026-11-16 盤點發現：證據包以前只用「藥名完全相同」撈 DL 預測，當地語言藥名、鹽類全名撈不到，
證據包寫「0 個預測」、頁面就被 noindex，而且沒有任何警示（2,913 頁 noindex 裡約 1,020 頁是這樣）。
這裡逐一檢查：證據包 predicted_indications 是空的，但 DL 預測檔裡這個藥（依 collectors/drug_bundle.py 的
resolve_dl_drug：藥名→DrugBank ID→drug_mapping.csv→去鹽名）有分數 ≥0.99、不在知識圖譜已知關係裡的預測 → 列為錯誤。
修法：python3 scripts/batch_collect_bundles.py --patch-empty（可加 --drugs 指定），有新預測的再產報告、重產頁面。

沒有 data/（例如 GitHub Pages 建置時沒還原 Release）就略過，不算錯。轉址頁不檢查。
用法：python3 scripts/check_dl_coverage.py（列出漏收的證據包；exit 1＝有漏收）
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def check_errors(limit_examples: int = 8) -> list:
    dl = DATA / "processed" / "txgnn_dl_predictions.csv.gz"
    bundles = DATA / "bundles"
    if not dl.exists() or not bundles.exists():
        return []
    sys.path.insert(0, str(ROOT / "src"))
    sys.path.insert(0, str(ROOT / "scripts"))
    pkg = next(p.name for p in (ROOT / "src").iterdir() if p.name.endswith("txgnn") and p.is_dir())
    resolve = __import__(f"{pkg}.collectors.drug_bundle", fromlist=["resolve_dl_drug"]).resolve_dl_drug
    from batch_collect_bundles import preload_predictions
    pre = preload_predictions(min_score=0.99, top_n=10)
    pages = ROOT / "docs" / "_drugs"
    missed = []
    for d in sorted(bundles.iterdir()):
        f = d / "drug_bundle.json"
        if not f.is_file():
            continue
        page = next((p for p in (pages / f"{d.name}.md", pages / f"{d.name.replace('_', '-')}.md") if p.exists()), None)
        if page is None:
            continue
        head = page.read_text(encoding="utf-8", errors="replace")[:3000]
        if 'http-equiv="refresh"' in head or re.search(r"^layout:\s*id_redirect", head, re.M):
            continue
        try:
            b = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:  # 2026-11-20：以前靜默略過，讀壞的證據包不會被檢查到
            missed.append(f"{d.name}（證據包讀不到：{e}）")
            continue
        drug = b.get("drug") or {}
        if drug.get("predicted_indications"):
            continue
        name = drug.get("inn") or drug.get("name") or d.name
        dl_name, _, how = resolve(name, drug.get("drugbank_id"))
        hits = pre.get((dl_name or name).lower()) or []
        if hits:
            missed.append(f"{d.name}（DL：{dl_name}，對應方式 {how}，{len(hits)} 個 ≥0.99 預測）")
    if not missed:
        return []
    return [f"證據包漏收 DL 預測或讀不到 {len(missed)} 個（證據包寫 0 個預測，DL 預測檔有這個藥的高分預測）："
            f"{'；'.join(missed[:limit_examples])}"
            "（跑 python3 scripts/batch_collect_bundles.py --patch-empty，有新預測的再產報告、重產頁面；說明見 scripts/check_dl_coverage.py）"]


if __name__ == "__main__":
    e = check_errors(limit_examples=10**6)
    print(e[0] if e else "證據包 DL 預測：沒有漏收（或沒有 data/，略過）")
    sys.exit(1 if e else 0)
