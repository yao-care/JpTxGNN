"""Kr 證據包的本國適應症欄存的是 MFDS 효능효과 PDF 網址，known_use_filter 讀不到文字（2026-10-23，pm：第 2 類，會擋上線）。
只處理 M2 分類裡目前有預測、會顯示在頁面上的 Kr 藥（regen／keep／known_use），單方許可證的 EE PDF：
下載 → pdftotext → .claude/cache/kr_mfds_ee/<許可證號>.txt（known_use_filter._clean_indication 讀這裡）。
不用模型。轉不出文字的（掃描檔等）列在 .claude/audit_20261016/m2/kr_mfds_fail.tsv。可續跑（已有快取的跳過）。
用法（母目錄）：python3 .claude/kr_mfds_ee_20261023.py
"""
import csv
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / ".claude"))
CACHE = BASE / ".claude/cache/kr_mfds_ee"
PDF = BASE / ".claude/cache/kr_mfds_pdf"  # 下載檔自成一個目錄，只拿來 pdftotext
OUT = BASE / ".claude/audit_20261016/m2/kr_mfds_fail.tsv"
URL = re.compile(r"https://nedrug\.mfds\.go\.kr/pbp/cmn/pdfDownload/(\d+)/EE")


def main():
    import known_use_filter as K
    CACHE.mkdir(parents=True, exist_ok=True); PDF.mkdir(parents=True, exist_ok=True)
    with open(BASE / ".claude/audit_20261016/m2/classification.tsv", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh, delimiter="\t") if r["site"] == "KrTxGNN" and r["class"] in ("regen", "keep", "known_use")]
    want = {}
    for r in rows:
        f = BASE / "KrTxGNN/data/bundles" / r["bundle"] / "drug_bundle.json"
        if not f.exists():
            continue
        b = json.loads(f.read_text(encoding="utf-8"))
        for rec in K._single_records(b):
            m = URL.match(str(rec.get("indication") or ""))
            if m:
                want.setdefault(m.group(1), r["page"])
    todo = [i for i in want if not (CACHE / f"{i}.txt").exists()]
    print("藥", len(rows), "許可證 PDF", len(want), "待下載", len(todo), flush=True)
    fails = []

    def one(lid):
        url = f"https://nedrug.mfds.go.kr/pbp/cmn/pdfDownload/{lid}/EE"
        pdf = PDF / f"{lid}.pdf"
        for i in range(5):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                pdf.write_bytes(urllib.request.urlopen(req, timeout=60).read())
                txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, timeout=60).stdout
                break
            except urllib.error.HTTPError as e:
                err = f"HTTP {e.code}"
                # 429／5xx：退避（30、60、120、240 秒），避免被封鎖；Retry-After 有給就照它
                ra = e.headers.get("Retry-After") if e.headers else None
                time.sleep(int(ra) if ra and ra.isdigit() else 30 * 2 ** i) if e.code == 429 or e.code >= 500 else time.sleep(3)
                if e.code < 500 and e.code != 429:
                    break
            except Exception as e:
                err = str(e)[:120]; time.sleep(5 * (i + 1))
        else:
            return (lid, want[lid], "download_error", err)
        txt = re.sub(r"^\s*효능\s*효과\s*$", "", txt, flags=re.M).strip()
        if len(re.sub(r"\s", "", txt)) < 4:
            return (lid, want[lid], "no_text", "")
        (CACHE / f"{lid}.txt").write_text(txt, encoding="utf-8")
        return None

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(6) as ex:  # MFDS 單線程每份約 10 秒，6 並行
        for n, r in enumerate(ex.map(one, todo), 1):
            if r:
                fails.append(r)
            if n % 200 == 0:
                print(n, "/", len(todo), "失敗", len(fails), flush=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("license_id\tpage\treason\tdetail\n")
        for r in fails:
            fh.write("\t".join(r) + "\n")
    print("完成", len(todo), "失敗", len(fails), flush=True)


if __name__ == "__main__":
    main()
