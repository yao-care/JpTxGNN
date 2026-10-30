"""JP（醫藥品マスター，社会保険診療報酬支払基金／hpdx.or.jp）下載與狀態對應，給 license_refresh_20261029.py 用（2026-10-30）。

站上的本地資料原本就是這份「医薬品マスター」（y_ALL<日期>.zip，薬価基準収載品目），不是 PMDA 的承認資料庫；
這裡沿用同一來源。下載頁 https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html（原 ssk.or.jp，會轉址），
取頁面上最新的 y_ALL*.zip（免金鑰，CSV、cp932）。欄位：第 3 欄 医薬品コード（＝證據包 pmda 區塊 license_id）、
第 31 欄 廃止年月日（99999999＝未廃止）。
寫回：廃止年月日已過 → status「廃止」、license_status cancelled（日文「廃止」與 reviewer 的「廢止」字形不同，另寫 license_status）；
未廃止 → status「有効」（證據包原值）。新檔沒有的コード保留原狀態。
"""
import csv
import io
import re
import time
import zipfile

import requests

RAW_FILE = "raw/y_master_status.json"
# 薬価基準から削除された品目は主檔から消える（2026-10-30 實測證據包 4,543 個コード對得上 90.5%）；涵蓋門檻 85%，其餘保留原狀態。
COVER_MIN = 0.85
PAGE = "https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html"


def _get(url, **kw):
    for attempt in range(4):
        try:
            r = requests.get(url, timeout=300, headers={"User-Agent": "Mozilla/5.0 (compatible; TxGNN/1.0; research)"}, **kw)
            r.raise_for_status()
            return r
        except Exception:
            if attempt == 3:
                raise
            time.sleep(15 * (attempt + 1))


def fetch():
    page = _get(PAGE)
    links = sorted(set(re.findall(r'href="([^"]*y_ALL(\d{8})\.zip)"', page.text)), key=lambda x: x[1])
    if not links:
        raise RuntimeError("下載頁上找不到 y_ALL*.zip")
    href = links[-1][0]
    url = requests.compat.urljoin(page.url, href)
    z = zipfile.ZipFile(io.BytesIO(_get(url).content))
    text = z.read(z.namelist()[0]).decode("cp932", "replace")
    out = []
    for c in csv.reader(io.StringIO(text)):
        if len(c) > 30 and c[2].strip().isdigit():
            out.append({"code": c[2].strip(), "haishi": c[30].strip()})
    return out


def validate(new, old):
    p = []
    if len(new) < 15000:
        p.append(f"只解析出 {len(new)} 筆，疑似格式改變")
    if sum(1 for r in new if not re.fullmatch(r"\d{8}", r["haishi"])) > 0.01 * max(1, len(new)):
        p.append("超過 1% 的廃止年月日不是 8 碼日期")
    if old and len(new) < 0.9 * len(old):
        p.append(f"筆數 {len(new)} 比上次 {len(old)} 少超過 10%")
    return p


def status_index(new):
    today = time.strftime("%Y%m%d")
    return {r["code"]: ("廃止" if r["haishi"] < today else "有効") for r in new if re.fullmatch(r"\d{8}", r["haishi"])}


def record_id(rec):
    return str(rec.get("license_id") or "").strip()


def update(rec, new):
    cls = "cancelled" if new == "廃止" else "valid"
    if rec.get("status") == new and rec.get("license_status", "valid" if new == "有効" else None) == cls:
        return False
    rec["status"], rec["license_status"] = new, cls
    return True
