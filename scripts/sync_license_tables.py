#!/usr/bin/env python3
"""「## 日本市販情報」段落の許可證表改由程式依證據包產生（2026-11-24，用戶決定；全程不用 AI）。

為什麼：以前這張表是報告（AI）寫的自由格式表（多數是「| 承認番号 | 商品名 | 剤形 | 承認適応症 |」；號碼其實是医薬品マスターの
医薬品コード（9 碼レセ電コード），不是承認番号；適応症欄是 AI 依 KEGG 寫的），每週許可證排程只改得到概覽表的狀態列與張數列，
表裡寫死的狀態（「有効」「取消」）跟著医薬品マスター變動就過期（薬価削除），checker 擋整頁、開 issue。
改成程式表後，每週排程（scripts/license_adapter.py 的 sync_tables 掛鉤）依同一套規則重排，gate 依快照驗內容。

表格（比照 HkTxGNN／SgTxGNN／UkTxGNN／NZTxGNN／UsTxGNN 的程式表；欄位照医薬品マスター原文，不翻譯）：
- 段落裡原有的第一張表（不論原欄位）換成「| 医薬品コード | 医薬品名・規格名 | 状態 |」；資料是證據包 pmda.records
  （医薬品マスター全件ファイル；license_id＝医薬品コード、brand_name_zh＝医薬品名・規格名（漢字名称））。
- 選列與順序：換表當時報告原表列出的医薬品コード（config/license_table_pins.json，依原表順序）在前——正文常寫「上記は主要な 5 件です」
  「残りの 3 件（…）も有効です」，換成別的列會對不上；其餘（以及原本沒有表的頁）依程式排序：有効在前、薬価削除在後，再依医薬品コード。
- 狀態欄：有効／薬価削除（YYYY-MM-DD[、後継コード N]）（license_status＝cancelled 時照證據包 status 原文，scripts/license_adapter.py 的 preprocess
  寫入；薬価基準からの削除は承認の取消しを意味しない，所以不寫「取消」）。
- 列數＝原表列數（最多 20 列）；段落裡沒有表的頁補 min(5, 總數) 列。總數多於列數時，表下加一句「上表はデータ上の {m} 件のうち {n} 件です。」；
  證據包只收了一部分（total_matches 多於紀錄數）時改寫「データには承認の一部のみが含まれています。上表はそのうち {n} 件です。」。
  證據包沒有任何紀錄時補 NONE_LINE。
- 表以外的文字不動（正文張數由 scripts/rewrite_license_counts.py 依快照事實層改寫）。
程式區塊標記：程式表（連同表下說明句，或 NONE_LINE）前後各一行「<!-- licenses:begin -->」「<!-- licenses:end -->」（前後空行）。
program_rows 給 scripts/build_license_snapshot.py（快照存最多 20 列可列的列，gate 比頁面上的前 N 列，狀態欄由 checker 另驗）；
carry_block 給 scripts/sync_notes_to_docs.py 重寫整頁時移植舊頁的程式區塊；run 給 scripts/license_adapter.py 的 sync_tables。
用法（repo 根目錄，先還原 data/）：python3 scripts/sync_license_tables.py [--dry-run] [頁 ...]
  --pin：從目前頁面的市場段落表格記下原表選列到 config/license_table_pins.json（只在換表前跑一次；已有的頁不覆蓋）
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECS = ("日本市販情報",)
HEAD = ["| 医薬品コード | 医薬品名・規格名 | 状態 |", "|------|------|------|"]
NONE_LINE = "医薬品マスター（薬価基準収載品目、本レポートで使用したデータ）には本薬の成分を含む品目がありません。"
SHOW = "上表はデータ上の {m} 件のうち {n} 件です。"
PART = "データには承認の一部のみが含まれています。上表はそのうち {n} 件です。"
SHOW_RX = re.compile(r"^(上表はデータ上の \d+ 件のうち \d+ 件です。|データには承認の一部のみが含まれています。上表はそのうち \d+ 件です。)$")
BEGIN = "<!-- licenses:begin -->"
END = "<!-- licenses:end -->"
MAX_ROWS = 20
ST_VALID = "有効"


def cell(x, cap=None):
    s = re.sub(r"\s+", " ", str(x or "").replace("|", "／")).strip()
    return s[:cap].rstrip() + "…" if cap and len(s) > cap else s


def is_cancelled(r):
    return str(r.get("license_status") or "").lower() == "cancelled"


def status_text(r):
    if not is_cancelled(r):
        return ST_VALID
    s = cell(r.get("status"))
    return s if s.startswith("薬価削除") else (s or "薬価削除")


def uniq(recs):
    seen = {}
    for r in recs or []:
        k = str(r.get("license_id") or "").strip()
        if k and k not in seen:
            seen[k] = r
    return list(seen.values())


def is_combo(r):
    """配合剤：医薬品マスターの医薬品名・規格名（brand_name_zh）或一般名（brand_name_en）寫「配合」
    （證據包 ingredients 欄是品名、事實層 single_total 把每張都算單剤，不能用；2026-11-24）"""
    return "配合" in str(r.get("brand_name_zh") or "") + str(r.get("brand_name_en") or "")


def mix(recs):
    """單剤／配合剤件數（含有効件數），給快照與正文張數改寫用（只驗不改）"""
    u = uniq(recs)
    s = [r for r in u if not is_combo(r)]
    c = [r for r in u if is_combo(r)]
    return {"single_total": len(s), "combo_total": len(c),
            "valid_single": sum(1 for r in s if not is_cancelled(r)), "valid_combo": sum(1 for r in c if not is_cancelled(r))}


PINS_FILE = ROOT / "config" / "license_table_pins.json"
_PINS = None


def pins_for(stem):
    """換表當時報告原表依序列出的医薬品コード（config/license_table_pins.json）；沒有就是 []"""
    global _PINS
    if _PINS is None:
        _PINS = json.loads(PINS_FILE.read_text(encoding="utf-8")).get("pins", {}) if PINS_FILE.exists() else {}
    return _PINS.get(stem) or _PINS.get(stem.replace("-", "_")) or _PINS.get(stem.replace("_", "-")) or []


def table_rows(recs, pins=()):
    """全部可列的列：pins（原表選列）依序在前，其餘依程式排序"""
    u = sorted(uniq(recs), key=lambda r: (is_cancelled(r), str(r.get("license_id")).strip()))
    rank = {k: i for i, k in enumerate(pins or [])}
    u.sort(key=lambda r: rank.get(str(r.get("license_id")).strip(), len(rank)))  # 穩定排序：沒選的保持程式排序
    rows = []
    for r in u:
        name = cell(r.get("brand_name_zh") or r.get("brand_name_en"), 80) or "記載なし"
        rows.append(f"| {str(r['license_id']).strip()} | {name} | {status_text(r)} |")
    return rows


def is_partial(tf):
    n = len(uniq(tf.get("records") or []))
    tm = tf.get("total_matches")
    return isinstance(tm, int) and tm > n


def block_for(tf, n=None, pins=()):
    """程式區塊的內容（不含標記）：n 列的表＋說明句；n 預設 min(5, 總數)；沒有任何紀錄時是 NONE_LINE 一句"""
    rows = table_rows(tf.get("records") or [], pins)
    if not rows:
        return [NONE_LINE]
    n = min(5, len(rows)) if n is None else min(n, len(rows))
    if is_partial(tf):
        return HEAD + rows[:n] + ["", PART.format(n=n)]
    return HEAD + rows[:n] + (["", SHOW.format(n=n, m=len(rows))] if len(rows) > n else [])


def program_rows(tf, fc=None, pins=()):
    """快照用：(程式表最多可列的列, None)；頁面的列數依原表列數（1～20），gate 比前 N 列"""
    return table_rows(tf.get("records") or [], pins)[:MAX_ROWS], None


def strip_marks(lines):
    return [l for l in lines if l.strip() not in (BEGIN, END)]


def wrap(block):
    return [BEGIN, ""] + block + ["", END]


def bounds(lines):
    """第一個市場段落（## 或 ### 日本市販情報）的 (標題下一行, 段落結尾)；沒有回 (None, None)"""
    for i, ln in enumerate(lines):
        m = re.match(r"^(#{2,3}) (.+?)\s*$", ln)
        if m and m.group(2) in SECS:
            lv = len(m.group(1))
            j = next((k for k in range(i + 1, len(lines)) if re.match(rf"^#{{1,{lv}}} ", lines[k])), len(lines))
            return i + 1, j
    return None, None


def _first_table(lines, a, b):
    tb = [k for k in range(a, b) if lines[k].startswith("|")]
    if not tb:
        return None, None
    x = y = tb[0]
    while y + 1 < b and lines[y + 1].startswith("|"):
        y += 1
    return x, y


# 母目錄 known_use_pages_20261022.py 以前產生的程式表（「| 承認番号 | 販売名 | 剤形 | 状態 |」）下的部分紀錄註記：程式表的 PART 句取代它
OLD_PART = "データには承認の一部のみが含まれており、一覧は不完全な可能性があります。"


def _is_prog(l):
    s = l.strip()
    return bool(SHOW_RX.match(s)) or s in (NONE_LINE, OLD_PART)


def process(text, tf, pins=()):
    """回傳新內容（沒變回 None）"""
    lines = strip_marks(text.split("\n"))
    a, b = bounds(lines)
    if a is None:
        return None
    x, y = _first_table(lines, a, b)
    if x is None:
        lines = lines[:a] + [""] + wrap(block_for(tf, None, pins)) + [""] + [l for l in lines[a:] if l.strip() != NONE_LINE]
    else:
        n = min(MAX_ROWS, max(1, y - x - 1))
        rest = [l for l in lines[y + 1:b] if not _is_prog(l)]
        lines = lines[:x] + ([""] if lines[x - 1].strip() else []) + wrap(block_for(tf, n, pins)) + [""] + rest + lines[b:]
    t2 = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
    return t2 if t2 != text else None


def carry_block(old_text, new_text):
    """sync_notes_to_docs.py 重寫整頁時用：舊頁的程式區塊移植到新頁的市場段落，取代新頁模型寫的第一張表；
    新頁段落沒有表時接在標題下。舊頁沒有程式區塊就原樣回傳新頁。"""
    old = old_text.replace("\r\n", "\n").split("\n")
    if BEGIN not in old or END not in old:
        return new_text
    blk = old[old.index(BEGIN):old.index(END) + 1]
    lines = strip_marks(new_text.split("\n"))
    a, b = bounds(lines)
    if a is None:
        return new_text
    x, y = _first_table(lines, a, b)
    if x is None:
        out = lines[:a] + [""] + blk + [""] + lines[a:]
    else:
        rest = [l for l in lines[y + 1:b] if not _is_prog(l)]
        out = lines[:x] + [""] + blk + [""] + rest + lines[b:]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out))


def bundle_file(stem):
    for key in dict.fromkeys((stem, stem.replace("-", "_"), stem.replace("_", "-"))):
        f = ROOT / "data/bundles" / key / "drug_bundle.json"
        if f.exists():
            return f
    return None


def _pages():
    for page in sorted((ROOT / "docs/_drugs").glob("*.md")):
        raw = page.read_bytes().decode("utf-8")
        if "layout: id_redirect" in raw[:3000] or 'http-equiv="refresh"' in raw[:3000]:
            continue
        yield page, raw


def pin(only=None):
    """換表前：記下各頁市場段落第一張表依序列出的、屬於本藥的医薬品コード"""
    doc = json.loads(PINS_FILE.read_text(encoding="utf-8")) if PINS_FILE.exists() else {"pins": {}}
    doc.setdefault("note", "換表當時（2026-11-24）報告原表依序列出的医薬品コード；scripts/sync_license_tables.py 依此選列（之後新增的頁不用）")
    n = 0
    for page, raw in _pages():
        if (only and page.stem not in only) or page.stem in doc["pins"]:
            continue
        bf = bundle_file(page.stem)
        if bf is None:
            continue
        lines = raw.replace("\r\n", "\n").split("\n")
        if BEGIN in lines:
            continue
        a, b = bounds(lines)
        if a is None:
            continue
        x, y = _first_table(lines, a, b)
        if x is None:
            continue
        own = {str(r.get("license_id") or "").strip() for r in (json.loads(bf.read_text(encoding="utf-8")).get("pmda") or {}).get("records") or []}
        ids = []
        for l in lines[x + 2:y + 1]:
            c = re.sub(r"[*_`\[\]]", "", l.strip().strip("|").split("|")[0]).strip()
            m = re.match(r"\d{9}", c)
            if m and m.group(0) in own and m.group(0) not in ids:
                ids.append(m.group(0))
        if ids:
            doc["pins"][page.stem] = ids
            n += 1
    doc["pins"] = dict(sorted(doc["pins"].items()))
    PINS_FILE.parent.mkdir(exist_ok=True)
    PINS_FILE.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return n


def run(only=None, dry=False):
    """全站（或 only 指定的頁）重排程式表。回傳改到的頁（檔名去 .md）。沒有 data/bundles 就什麼都不做。"""
    changed = []
    if not (ROOT / "data/bundles").is_dir():
        return changed
    for page, raw in _pages():
        if only and page.stem not in only:
            continue
        bf = bundle_file(page.stem)
        if bf is None:
            continue
        crlf = "\r\n" in raw[:500]
        tf = json.loads(bf.read_text(encoding="utf-8")).get("pmda") or {}
        new = process(raw.replace("\r\n", "\n"), tf, pins_for(page.stem))
        if new is None:
            continue
        changed.append(page.stem)
        if not dry:
            page.write_bytes((new.replace("\n", "\r\n") if crlf else new).encode("utf-8"))
    return changed


if __name__ == "__main__":
    a = sys.argv[1:]
    only = {x for x in a if not x.startswith("--")} or None
    if "--pin" in a:
        print(f"原表選列：記下 {pin(only)} 頁 → {PINS_FILE.relative_to(ROOT)}")
        sys.exit(0)
    ch = run(only, "--dry-run" in a)
    print(f"許可證表{'（試跑）' if '--dry-run' in a else ''}改 {len(ch)} 頁")
