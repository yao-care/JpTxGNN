#!/usr/bin/env python3
"""正文許可證張數依快照事實層改寫（2026-11-24 建，用戶決定；移植 KrTxGNN／MyTxGNN 同名程式）。

規則在 src/jptxgnn/regulatory/count_prose.py（本站日文句型）；事實＝snapshots/jp_licenses.json.gz 的 facts（医薬品マスター收載品目；
「薬価削除」算 cancelled，不是承認取消）。
比照 TwTxGNN 的 page_postprocess.rewrite_count_prose：程式改寫的張數敘述是程式產生的正文，不逐筆寫查核紀錄、頁面不加說明框；
查核紀錄的 replacement／anchor 所在的句子不改（免得紀錄對不上）。

誰會跑：scripts/apply_drug_reviews.py（非 --check 時結尾自動跑，所以 sync_notes_to_docs.py、license_rebuild_run.py、
母目錄每週排程 license_refresh_20261029.py 的 4b 都會跑到）、scripts/build_license_snapshot.py（寫完新快照再跑一次，用新事實）。
gate：scripts/check_seo_docs.py 的「正文許可證張數」項（再跑一次不會變）。

用法：
  python3 scripts/rewrite_license_counts.py            # 改寫
  python3 scripts/rewrite_license_counts.py --check    # 只檢查，有要改的頁 exit 1
  python3 scripts/rewrite_license_counts.py --list     # 列出判斷不了、沒改的句子（ambiguous／premise／zero-premise／to-zero／numeral-word／single-combo）
  python3 scripts/rewrite_license_counts.py --uncertain   # 把上面那些句子加進 docs/_data/drug_reviews_uncertain.json（只附加，不刪既有項目）
  加 --touch 連 last_modified_at 一起改成今天
"""
import datetime as _dt
import gzip
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from jptxgnn.regulatory import count_prose as CP  # noqa: E402

SNAP = ROOT / "snapshots" / "jp_licenses.json.gz"
DRUGS = ROOT / "docs" / "_drugs"
DATA = ROOT / "docs" / "_data" / "drug_reviews.json"
UNCERTAIN = ROOT / "docs" / "_data" / "drug_reviews_uncertain.json"
SOURCE = "正文許可證張數程式改寫判斷不了的句子（scripts/rewrite_license_counts.py）"
REVIEW_NEEDED = ("ambiguous", "premise", "zero-premise", "to-zero", "numeral-word", "single-combo")


def _facts():
    if not SNAP.exists():
        return {}
    return json.loads(gzip.open(SNAP).read().decode("utf-8")).get("drugs", {})


def _protect():
    out = {}
    if DATA.exists():
        for r in json.loads(DATA.read_text(encoding="utf-8")).get("records", []):
            if r.get("status") in ("superseded", "resolved_by_regeneration", "resolved_by_program", "withdrawn"):
                continue  # 不再顯示的紀錄不保護原句（比照 COTxGNN）
            out.setdefault(r["file"], []).extend([r.get("replacement") or "", r.get("anchor") or ""])
    return out


def _touch(text):
    today = _dt.date.today().isoformat()
    return re.sub(r"^(last_modified_at:\s*)\d{4}-\d{2}-\d{2}", rf"\g<1>{today}", text, count=1, flags=re.M)


def run(check=False, only=None, touch_date=False):
    """回傳 (改到的頁, 判斷不了的句子 [(頁, 理由, 句子)])。"""
    facts, prot = _facts(), _protect()
    changed, skipped = [], []
    for p in sorted(DRUGS.glob("*.md")):
        if only and p.name not in only:
            continue
        e = facts.get(p.stem)
        if not e:
            continue
        t = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in t[:3000] or re.search(r"^layout:\s*id_redirect", t[:3000], re.M):
            continue
        n, sk = CP.rewrite(t, e.get("facts"), e.get("mix"), prot.get(p.name, ()))
        skipped += [(p.stem, why, s) for why, s in sk if why in REVIEW_NEEDED]
        if n != t:
            changed.append(p.name)
            if not check:
                p.write_text(_touch(n) if touch_date else n, encoding="utf-8")
    return changed, skipped


def check_errors():
    """給 check_seo_docs.py 用：正文張數跟快照事實層不一致（程式改寫後會變）的頁。"""
    changed, _ = run(check=True)
    if not changed:
        return []
    return [f"正文許可證張數跟快照事實層不一致 {len(changed)} 頁：{'、'.join(changed[:8])}"
            "（請跑 python3 scripts/rewrite_license_counts.py；規則見 src/jptxgnn/regulatory/count_prose.py）"]


def add_uncertain(skipped):
    doc = json.loads(UNCERTAIN.read_text(encoding="utf-8")) if UNCERTAIN.exists() else {"items": []}
    have = {(x.get("drug"), x.get("claim")) for x in doc["items"]}
    n = 0
    for drug, why, s in skipped:
        if (drug, s) in have:
            continue
        doc["items"].append({"source": SOURCE, "drug": drug, "file": f"{drug}.md", "status": "open", "claim": s,
                             "reason": why, "added": _dt.date.today().isoformat(),
                             "note": "正文許可證張數跟快照事實層可能不一致，但句型判斷不了要怎麼改（說「すべて有効」而事實不符、"
                                     "沒有限定詞而有効數≠總數、建立在 0 件前提上或要改成 0 件、用漢數字「二件」「三件」寫，或單剤／配合剤件數；"
                                     "医薬品マスターの成分欄是品名，單剤／配合剤只驗不改），程式沒改；要改請寫查核紀錄"})
        have.add((drug, s))
        n += 1
    UNCERTAIN.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return n


if __name__ == "__main__":
    a = sys.argv[1:]
    only = {x if x.endswith(".md") else x + ".md" for x in a if not x.startswith("--")} or None
    check = "--check" in a or "--list" in a or "--uncertain" in a
    changed, skipped = run(check=check, only=only, touch_date="--touch" in a)
    if "--list" in a:
        for drug, why, s in skipped:
            print(f"{drug}\t{why}\t{s}")
    if "--uncertain" in a:
        print(f"待查清單新增 {add_uncertain(skipped)} 項")
    if "--check" in a:
        print(f"正文許可證張數：{'✗' if changed else '✓'} 待改寫 {len(changed)} 頁")
        sys.exit(1 if changed else 0)
    if not check:
        print(f"正文許可證張數：改寫 {len(changed)} 頁（判斷不了、沒改的句子 {len(skipped)} 句，--list 列出）")
