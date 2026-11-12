"""藥物頁許可證資訊的驗證（2026-11-12 建，本站查核機制；比照 TwTxGNN gate 第 6 項、UsTxGNN src/ustxgnn/regulatory/licenses.py）。

依 snapshots/<站碼>_licenses.json.gz（scripts/build_license_snapshot.py 產生）檢查，不需要 data/：
  1. 市場段落（## 或 ### 標題＝site.MARKET_SECTIONS）裡各張表第一欄的許可證號（含數字的格）都屬於本藥（快照 own，依 checker 的 norm_id 比）。
  2. 概覽表的狀態列與張數列＝事實層的寫法：本站 tools/txgnn/.claude/check_drug_page.py 的 M1／M4 同一套函式
     （marketed_text／not_marketed_text／unknown_status_text／not_reg_text／NO_CENTRAL、count_text）。
  3. 表格列寫的狀態不跟事實相反（checker：有效許可證寫成註銷、row_status_conflicts）。
本站的許可證表是報告裡的表格（沒有程式產生的許可證表），所以不驗表格列內容；事實層只涵蓋部分來源時（checker X_SCOPE），
跟 checker 一樣只驗資料能證明的部分。
修法：資料變了→跑每週排程（重排狀態格、狀態列、張數列並重建快照）；正文或表格寫錯→寫查核紀錄（docs/_data/drug_reviews.json）
再跑 scripts/apply_drug_reviews.py。
"""
from __future__ import annotations

import gzip
import importlib.util
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

from . import site as C

ROOT = Path(__file__).resolve().parents[3]
SNAP = ROOT / "snapshots" / f"{C.CODE}_licenses.json.gz"
SITE = C.SITE


@lru_cache(maxsize=None)
def CK():
    p = ROOT / "tools" / "txgnn" / ".claude" / "check_drug_page.py"
    s = importlib.util.spec_from_file_location(f"{SITE}_check_drug_page", p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


@lru_cache(maxsize=None)
def snapshot() -> dict:
    if not SNAP.exists():
        return {}
    return json.loads(gzip.open(SNAP).read().decode("utf-8"))


def _tables(lines):
    out, cur = [], []
    for ln in lines + [""]:
        if ln.startswith("|"):
            cur.append(ln)
        elif cur:
            out.append(cur)
            cur = []
    return out


def _rows(tbl):
    return [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in tbl[2:]]


def _sections(lines):
    """市場段落（## 或 ### 標題＝site.MARKET_SECTIONS 之一；可能不只一段）的行範圍：到下一個同級或更高一級的標題為止"""
    out = []
    for i, ln in enumerate(lines):
        m = re.match(r"^(#{2,3}) (.+?)\s*$", ln)
        if m and m.group(2) in C.MARKET_SECTIONS:
            lv = len(m.group(1))
            j = next((k for k in range(i + 1, len(lines)) if re.match(rf"^#{{1,{lv}}} ", lines[k])), len(lines))
            out.append((i + 1, j))
    return out


def _id_token(cell):
    """許可證號格：取第一個號碼片段（格裡常接狀態註記，例「52445 (indraget)」「NDA208743 (cancelled)」）"""
    s = re.sub(r"[*_`\[\]]", "", cell or "").strip()
    return re.split(r"\s+[\(（]|[\(（]|\s{2,}|\s[-–—]\s", s, maxsplit=1)[0].strip()


def expected_status(fc):
    ck = CK()
    lang = ck.LANG.get(SITE, "en")
    ms, v, n, partial = fc.get("market_status"), fc.get("valid"), fc.get("total"), fc.get("partial")
    if ms == "Marketed":
        return ck.marketed_text(SITE, lang, v, n, partial, fc)
    if ms == "Approved, not marketed":
        return ck.not_marketed_text(SITE, lang, fc)
    if ms == "Status unknown" and SITE in ck.UNKNOWN_ST:
        return ck.unknown_status_text(SITE, lang, fc)
    if ms == "Not marketed" and SITE in ck.VET_ONLY:
        return ck.not_reg_text(SITE, lang, fc)
    if ms == "Not marketed" and SITE in ck.NO_CENTRAL:
        return ck.NO_CENTRAL[SITE]
    return None


def page_problems(stem: str, text: str) -> list[str]:
    e = (snapshot().get("drugs") or {}).get(stem)
    if e is None:
        return []  # 快照沒有的頁（沒有證據包）：不驗
    ck = CK()
    body = ck.MANAGED.sub("", text.replace("\r\n", "\n"))
    lines = body.split("\n")
    errs = []
    own = {ck.mv2.norm_id(y) for x in e.get("own") or [] for y in (x, x.split("//")[0])}  # 「RVG 120202//33414」（Nl：註冊號//產品號）也認主號碼
    if own:
        for a, b in _sections(lines):
            for t in _tables(lines[a:b]):
                for cells in _rows(t):
                    k = ck.mv2.norm_id(_id_token(cells[0])) if cells else ""
                    if k and re.search(r"\d", k) and k not in own and len(k) >= 4:
                        errs.append(f"市場段落表格的許可證號不屬於本藥：{cells[0][:30]}")
    fc = e.get("facts")
    if not fc:
        return errs
    lang = ck.LANG.get(SITE, "en")
    all_rows = [r for t in _tables(lines) for r in _rows(t)]
    st = ck.status_row(SITE, all_rows)
    want_s = expected_status(fc)
    if st is not None and want_s and st[1] != want_s:
        errs.append(f"狀態列「{st[1][:50]}」≠ 事實層寫法「{want_s}」")
    cr = ck.count_row(SITE, all_rows)
    n, v, ms, partial = fc.get("total"), fc.get("valid"), fc.get("market_status"), fc.get("partial")
    if cr is not None and n is not None:
        nums = [int(x) for x in re.findall(r"\d+", ck.norm_digits(cr[1]))]
        if not (n in nums and (v is None or ms != "Marketed" or v in nums)) or (partial and not ck.AT_LEAST.search(cr[1])):
            errs.append(f"張數列「{cr[1][:50]}」≠ 共 {n}／有效 {v}")
    if cr is not None and (n is not None or partial):
        want_c = ck.count_text(SITE, lang, fc)
        if cr[1] != want_c:
            errs.append(f"張數列「{cr[1][:50]}」≠ 事實層寫法「{want_c}」")
    lic = {ck.mv2.norm_id(k): s for k, s in (fc.get("licenses") or {}).items()}
    for cells in all_rows:
        k = ck.mv2.norm_id(cells[0]) if cells else ""
        if lic.get(k) == "valid" and ck.mv2.TABLE_NEG.search(" ".join(cells[1:])):
            errs.append(f"有效許可證 {cells[0][:30]} 寫成註銷")
    for a, b in _sections(lines):
        for t in _tables(lines[a:b]):
            for code, d in ck.row_status_conflicts(SITE, _rows(t), lic):
                errs.append(f"許可證表列的狀態跟事實相反：{d}")
    return errs


def site_problems(drugs_dir: Path | None = None) -> list[str]:
    drugs_dir = drugs_dir or ROOT / "docs" / "_drugs"
    if not snapshot():
        return [f"找不到 {SNAP.relative_to(ROOT)}（跑 scripts/build_license_snapshot.py）"]
    out = []
    for f in sorted(drugs_dir.glob("*.md")):
        t = f.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in t[:3000] or re.search(r"^layout:\s*id_redirect", t[:3000], re.M):
            continue
        out += [f"{f.name}：{x}" for x in page_problems(f.stem, t)]
    return out


if __name__ == "__main__":
    errs = site_problems()
    for x in errs[:50]:
        print("  ✗", x)
    print(f"許可證檢查：{'✗' if errs else '✓'} {len(errs)} 項")
    sys.exit(1 if errs else 0)
