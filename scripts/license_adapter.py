"""JP（醫藥品マスター，社会保険診療報酬支払基金／hpdx.or.jp）下載與狀態對應，給 license_refresh_20261029.py 用（2026-10-30）。

站上的本地資料原本就是這份「医薬品マスター」（y_ALL<日期>.zip，薬価基準収載品目），不是 PMDA 的承認資料庫；
這裡沿用同一來源。下載頁 https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html（原 ssk.or.jp，會轉址），
取頁面上最新的 y_ALL*.zip（免金鑰，CSV、cp932）。欄位：第 3 欄 医薬品コード（＝證據包 pmda 區塊 license_id）、
第 31 欄 廃止年月日（99999999＝未廃止）。
寫回：廃止年月日已過 → status「廃止」、license_status cancelled（日文「廃止」與 reviewer 的「廢止」字形不同，另寫 license_status）；
未廃止 → status「有効」（證據包原值）。新檔沒有的コード保留原狀態。

2026-11-17（用戶要求確認 11-16 排程「新資料查不到」的 431 張）：医薬品マスター只收薬価基準収載品目，コード在廃止年月日（経過措置期間満了）
過後就從全件ファイル消失，所以「查不到」大多是薬価削除，不等於承認失效（承認情報不在這份資料裡）。做法：
- fetch() 另下載同一頁上的全件ファイル（y_ALL*.zip）、改定分ファイル（y_*.csv）與経過措置医薬品一覧（keikasoti_*.xlsx），
  收集主檔自己記錄的廃止年月日（変更区分 9 或廃止年月日≠99999999、経過措置一覧的廃止日與後継コード）→ HAISHI。
- 最新全件ファイルのコード → CURRENT（少於 MIN_CURRENT 不判定）。任一份下載失敗就不判定。
- preprocess：不在 CURRENT、且 HAISHI 有已過的廃止年月日的コード，標 license_status＝cancelled、yakka_deleted＝廃止年月日、
  ssk_not_listed＝第一次發現日，status 改「薬価削除（YYYY-MM-DD）」（有後継コード加「、後継コード N」；原值存 status_before_yakka_deleted）。
  這是「薬価基準から削除」，頁面照這個寫，不寫承認取消。又出現在全件ファイル就還原。
- 不在 CURRENT、主檔也沒有廃止紀錄的コード不推定，維持原狀態（排程照樣列為「查不到」）。
- confirmed_absent(lid)：不在 CURRENT 且有廃止紀錄（下載到的或證據包已記的 yakka_deleted）。
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
CURRENT: set = set()   # fetch() 填：最新全件ファイルの医薬品コード；空的就不做「不在主檔」判定
HAISHI: dict = {}      # fetch() 填：コード → {"date": 廃止年月日, "succ": 後継コード or None, "src": 檔名}
MIN_CURRENT = 15000
_RECORDED = None       # 證據包已標 yakka_deleted 的コード（confirmed_absent 用，第一次呼叫時掃描）


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


def _rows(content, is_zip):
    if is_zip:
        z = zipfile.ZipFile(io.BytesIO(content))
        content = z.read(z.namelist()[0])
    return [c for c in csv.reader(io.StringIO(content.decode("cp932", "replace"))) if len(c) > 33 and c[2].strip().isdigit()]


def fetch():
    page = _get(PAGE)
    links = sorted(set(re.findall(r'href="([^"]*y_ALL(\d{8})\.zip)"', page.text)), key=lambda x: x[1])
    if not links:
        raise RuntimeError("下載頁上找不到 y_ALL*.zip")
    href = links[-1][0]
    url = requests.compat.urljoin(page.url, href)
    rows = _rows(_get(url).content, True)
    out = [{"code": c[2].strip(), "haishi": c[30].strip()} for c in rows]
    CURRENT.clear()
    HAISHI.clear()
    try:
        hs = _fetch_haishi(page, href)
    except Exception as e:
        print(f"改定分／経過措置一覧下載失敗，不判定不在主檔的コード：{e}")
        hs = None
    if hs is not None and len(out) >= MIN_CURRENT:
        CURRENT.update(r["code"] for r in out)
        HAISHI.update(hs)
    return out


def _fetch_haishi(page, latest):
    """同一頁上其他全件ファイル、改定分ファイル、経過措置一覧裡記錄的廃止年月日（主檔自己的廃止紀錄）"""
    import openpyxl
    hs = {}

    def put(code, date, succ, src):
        if re.fullmatch(r"\d{8}", date or "") and date != "99999999":
            h = hs.setdefault(code, {"date": date, "succ": None, "src": src})
            h["date"] = min(h["date"], date)
            if succ and succ.isdigit() and succ != "0" and not h["succ"]:
                h["succ"] = succ
    for href in sorted(set(re.findall(r'href="([^"]*/y_(?:ALL)?\d{8}\.(?:zip|csv))"', page.text))):
        if href == latest:
            continue
        name = href.rsplit("/", 1)[-1]
        for c in _rows(_get(requests.compat.urljoin(page.url, href)).content, name.endswith(".zip")):
            put(c[2].strip(), c[30].strip(), c[22].strip() if c[0].strip() == "9" else None, name)
    for href in sorted(set(re.findall(r'href="([^"]*keikasoti[^"]*\.xlsx)"', page.text))):
        name = href.rsplit("/", 1)[-1]
        ws = openpyxl.load_workbook(io.BytesIO(_get(requests.compat.urljoin(page.url, href)).content), read_only=True).worksheets[0]
        for row in ws.iter_rows(values_only=True):
            if row and len(row) > 8 and str(row[2] or "").strip().isdigit():
                put(str(row[2]).strip(), str(row[8] or "").strip(), str(row[6] or "").strip(), name)
    return hs


def _recorded():
    global _RECORDED
    if _RECORDED is None:
        import json
        from pathlib import Path
        _RECORDED = set()
        for f in (Path(__file__).resolve().parents[1] / "data/bundles").glob("*/drug_bundle.json"):
            try:
                b = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            _RECORDED.update(str(r.get("license_id")) for r in ((b.get("pmda") or {}).get("records") or []) if r.get("yakka_deleted"))
    return _RECORDED


def _gone(lid):
    h = HAISHI.get(lid)
    return h and h["date"] < time.strftime("%Y%m%d")


def confirmed_absent(lid):
    """給 license_refresh：最新全件ファイルにない、かつ主檔に廃止年月日の記錄がある（＝薬価基準から削除済み）"""
    lid = str(lid).strip()
    return bool(CURRENT) and lid.isdigit() and lid not in CURRENT and bool(_gone(lid) or lid in _recorded())


def preprocess(bundle):
    """薬価基準から削除されたコードを標記（cancelled＋yakka_deleted）；全件ファイルに再び現れたら還原。有改回 True"""
    if not CURRENT:
        return False
    today = time.strftime("%Y-%m-%d")
    ch = False
    for r in (bundle.get("pmda") or {}).get("records") or []:
        lid = str(r.get("license_id") or "").strip()
        if not lid.isdigit():
            continue
        if lid in CURRENT:
            if r.get("yakka_deleted"):
                for k in ("yakka_deleted", "yakka_successor", "ssk_not_listed", "license_status"):
                    r.pop(k, None)
                r["status"] = r.pop("status_before_yakka_deleted", "有効")
                ch = True
        elif not r.get("yakka_deleted") and _gone(lid):
            h = HAISHI[lid]
            d = f"{h['date'][:4]}-{h['date'][4:6]}-{h['date'][6:]}"
            succ = h["succ"] if h["succ"] and h["succ"] in CURRENT else None
            r["status_before_yakka_deleted"] = r.get("status")
            r["status"] = f"薬価削除（{d}" + (f"、後継コード {succ}" if succ else "") + "）"
            r["license_status"] = "cancelled"
            r["yakka_deleted"] = d
            r["ssk_not_listed"] = today
            if succ:
                r["yakka_successor"] = succ
            ch = True
    return ch


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
