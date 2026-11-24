#!/usr/bin/env python3
"""產生許可證快照 snapshots/<站碼>_licenses.json.gz（2026-11-12 建，本站查核機制；比照 TwTxGNN snapshots/tfda_licenses.json.gz、
UsTxGNN scripts/build_license_snapshot.py）。

為什麼要有這支：藥物頁概覽表的狀態列、張數列是程式依證據包（data/bundles，放在 Release）與事實層（.claude/cache/license_facts，
dump_license_facts 依證據包算）產生的。gate（scripts/check_seo_docs.py）要在沒有 data/ 的環境也能驗證頁面上的許可證號屬於本藥、
狀態列與張數列跟事實一致，所以把驗證要用的部分存成快照放進 git。

內容（鍵＝藥物頁檔名去 .md）：bundle（證據包鍵）、facts（事實層那一筆）、own（本藥所有許可證號：證據包裡每個含 records 的區塊的
license_id，跟事實層同一套來源）；rows（2026-11-24 起：市場段落程式許可證表最多可列的 20 列，scripts/sync_license_tables.py
的 program_rows，選列依 config/license_table_pins.json，gate 比頁面上的前 N 列）、nrows（可列的總列數）、tpart（證據包只收了一部分）、mix（單剤／配合剤件數，依品名「配合」；事實層 single_total 每張都算單剤，不能用）；
meta：產生日、Release tag。內容相同時檔案位元組相同（gzip mtime=0）。
寫完快照後跑 scripts/sync_license_tables.py（程式表依證據包重排）與 scripts/rewrite_license_counts.py（正文許可證張數依新事實改寫）；
--no-rewrite 兩支都不跑（母目錄 license_rebuild_run 轉紀錄前用）。--from-snapshot：不讀 data/，只用既有快照跑上面兩支的改寫
（程式表重排需要 data/bundles，沒有就略過）。
什麼時候跑：證據包或事實層變了之後（每週許可證排程與依成分重建都會自動跑，並把 snapshots/ 跟 docs/ 一起 commit）。
用法（repo 根目錄，先還原 data/ 並在工作目錄跑 dump_license_facts）：
  python3 scripts/build_license_snapshot.py --ws <工作目錄> [--release-tag data-YYYYMMDD-HHMMSS]
"""
import datetime as dt
import gzip
import importlib.util
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


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def build(ws, tag=""):
    fp = Path(ws) / ".claude/cache/license_facts" / f"{C.SITE}.json"
    if not fp.exists():
        sys.exit(f"找不到事實層 {fp}（先跑 dump_license_facts）")
    fs = json.loads(fp.read_text(encoding="utf-8"))
    S = _load("jp_sync_license_tables", ROOT / "scripts" / "sync_license_tables.py")
    drugs = {}
    for page in sorted((ROOT / "docs/_drugs").glob("*.md")):
        head = page.read_text(encoding="utf-8", errors="replace")[:3000]
        if "layout: id_redirect" in head or 'http-equiv="refresh"' in head:
            continue
        key, b = bundle_for(page.stem)
        if b is None:
            continue
        fc = fs.get(key) or fs.get(page.stem) or fs.get(page.stem.replace("-", "_")) or fs.get(page.stem.replace("_", "-"))
        tf = b.get("pmda") or {}
        rows, _ = S.program_rows(tf, fc, S.pins_for(page.stem))
        drugs[page.stem] = {"bundle": key, "facts": fc, "own": own_ids(b), "rows": rows,
                             "nrows": len(S.table_rows(tf.get("records") or [])), "tpart": S.is_partial(tf), "mix": S.mix(tf.get("records") or [])}
    meta = {"built": dt.date.today().isoformat(), "release_tag": tag, "pages": len(drugs),
            "rule": "own：證據包含 records 的區塊的 license_id；facts：tools/txgnn/.claude/dump_license_facts_20261021.py；"
                    "rows、nrows、tpart、mix：scripts/sync_license_tables.py"}
    OUT.parent.mkdir(exist_ok=True)
    raw = json.dumps({"meta": meta, "drugs": drugs}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    with gzip.GzipFile(OUT, "wb", mtime=0) as fh:
        fh.write(raw)
    print(f"許可證快照：{len(drugs)} 頁 → {OUT.relative_to(ROOT)}（{OUT.stat().st_size // 1024} KB）")


if __name__ == "__main__":
    # 2026-11-19：說明頁／證據等級頁的資料檔跟著重算（scripts/local_facts.py；--check 時不跑）
    import atexit as _lf_ax, os as _lf_os, subprocess as _lf_sp, sys as _lf_sys
    _lf_here = _lf_os.path.dirname(_lf_os.path.abspath(__file__))  # 先算好：atexit 時 __main__ 的 __file__ 已不在（NameError，2026-11-19 修）
    _lf_fail = []  # 2026-11-20：結尾自動重算的回傳值以前被丟掉，失敗不會被發現；現在失敗會印 ✗ 並讓整支 exit 1
    def _lf_chk(r, what):
        if r.returncode:
            print(f"  ✗ 結尾自動重算失敗：{what}（exit {r.returncode}）", file=_lf_sys.stderr)
            _lf_fail.append(what)
        return r
    _lf_ax.register(lambda: _lf_fail and (_lf_sys.stdout.flush(), _lf_os._exit(1)))  # 最先註冊＝最後執行
    _lf_ax.register(lambda: "--check" in _lf_sys.argv or _lf_chk(_lf_sp.run([_lf_sys.executable, _lf_os.path.join(_lf_here, "local_facts.py"), "--write"]), "local_facts.py --write"))
    # 2026-11-19：藥物頁 description 句尾依許可證快照事實層重算（tools/txgnn/.claude/drug_meta_description.py；--check 時不跑）
    _dl_root = _lf_os.path.dirname(_lf_os.path.dirname(_lf_os.path.abspath(__file__)))
    _dl_p = _lf_os.path.join(_dl_root, "tools", "txgnn", ".claude", "drug_meta_description.py")
    _lf_ax.register(lambda: "--check" in _lf_sys.argv or not _lf_os.path.exists(_dl_p) or _lf_chk(_lf_sp.run([_lf_sys.executable, _dl_p, "--apply", "--root", _dl_root]), "drug_meta_description.py --apply"))
    a = sys.argv[1:]
    if "--from-snapshot" not in a:
        ws = a[a.index("--ws") + 1] if "--ws" in a else str(ROOT.parent)  # 排程傳 --ws <母目錄>；不帶參數時用 repo 的上一層
        tag = a[a.index("--release-tag") + 1] if "--release-tag" in a else ""
        if not re.fullmatch(r"(data-[\w-]+)?", tag):
            sys.exit("--release-tag 要是 data-… 的 tag")
        build(ws, tag)
    # 2026-11-24：快照換了事實，程式許可證表重排、正文許可證張數跟著改寫（每週排程是先套紀錄再建快照，所以這裡用新快照再跑一次；比照 Hk／Kr／My）
    if "--no-rewrite" not in a:
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "scripts" / "sync_license_tables.py")], check=True)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "rewrite_license_counts.py")], check=True)
