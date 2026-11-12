#!/usr/bin/env python3
"""產生許可證快照 snapshots/<站碼>_licenses.json.gz（2026-11-12 建，本站查核機制；比照 TwTxGNN snapshots/tfda_licenses.json.gz、
UsTxGNN scripts/build_license_snapshot.py）。

為什麼要有這支：藥物頁概覽表的狀態列、張數列是程式依證據包（data/bundles，放在 Release）與事實層（.claude/cache/license_facts，
dump_license_facts 依證據包算）產生的。gate（scripts/check_seo_docs.py）要在沒有 data/ 的環境也能驗證頁面上的許可證號屬於本藥、
狀態列與張數列跟事實一致，所以把驗證要用的部分存成快照放進 git。

內容（鍵＝藥物頁檔名去 .md）：bundle（證據包鍵）、facts（事實層那一筆）、own（本藥所有許可證號：證據包裡每個含 records 的區塊的
license_id，跟事實層同一套來源）；meta：產生日、Release tag。內容相同時檔案位元組相同（gzip mtime=0）。
什麼時候跑：證據包或事實層變了之後（每週許可證排程與依成分重建都會自動跑，並把 snapshots/ 跟 docs/ 一起 commit）。
用法（repo 根目錄，先還原 data/ 並在工作目錄跑 dump_license_facts）：
  python3 scripts/build_license_snapshot.py --ws <工作目錄> [--release-tag data-YYYYMMDD-HHMMSS]
"""
import datetime as dt
import gzip
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from jptxgnn.regulatory import site as C  # noqa: E402

OUT = ROOT / "snapshots" / f"{C.CODE}_licenses.json.gz"


def bundle_for(stem):
    for key in dict.fromkeys((stem, stem.replace("-", "_"), stem.replace("_", "-"))):
        f = ROOT / "data/bundles" / key / "drug_bundle.json"
        if f.exists():
            return key, json.loads(f.read_text(encoding="utf-8"))
    return None, None


def own_ids(b):
    out = set()
    for v in b.values():
        if isinstance(v, dict) and isinstance(v.get("records"), list):
            for r in v["records"]:
                k = str(r.get("license_id") or "").strip()
                if k:
                    out.add(k)
    return sorted(out)


def build(ws, tag=""):
    fp = Path(ws) / ".claude/cache/license_facts" / f"{C.SITE}.json"
    if not fp.exists():
        sys.exit(f"找不到事實層 {fp}（先跑 dump_license_facts）")
    fs = json.loads(fp.read_text(encoding="utf-8"))
    drugs = {}
    for page in sorted((ROOT / "docs/_drugs").glob("*.md")):
        head = page.read_text(encoding="utf-8", errors="replace")[:3000]
        if "layout: id_redirect" in head or 'http-equiv="refresh"' in head:
            continue
        key, b = bundle_for(page.stem)
        if b is None:
            continue
        fc = fs.get(key) or fs.get(page.stem) or fs.get(page.stem.replace("-", "_")) or fs.get(page.stem.replace("_", "-"))
        drugs[page.stem] = {"bundle": key, "facts": fc, "own": own_ids(b)}
    meta = {"built": dt.date.today().isoformat(), "release_tag": tag, "pages": len(drugs),
            "rule": "own：證據包含 records 的區塊的 license_id；facts：tools/txgnn/.claude/dump_license_facts_20261021.py"}
    OUT.parent.mkdir(exist_ok=True)
    raw = json.dumps({"meta": meta, "drugs": drugs}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    with gzip.GzipFile(OUT, "wb", mtime=0) as fh:
        fh.write(raw)
    print(f"許可證快照：{len(drugs)} 頁 → {OUT.relative_to(ROOT)}（{OUT.stat().st_size // 1024} KB）")


if __name__ == "__main__":
    a = sys.argv[1:]
    ws = a[a.index("--ws") + 1]
    tag = a[a.index("--release-tag") + 1] if "--release-tag" in a else ""
    if not re.fullmatch(r"(data-[\w-]+)?", tag):
        sys.exit("--release-tag 要是 data-… 的 tag")
    build(ws, tag)
