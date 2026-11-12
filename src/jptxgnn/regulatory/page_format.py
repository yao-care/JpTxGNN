"""藥物頁的確定性格式規則：頁首證據等級、description 的等級、表格前後空行（2026-11-12 建）。

比照 TwTxGNN src/twtxgnn/regulatory/page_format.py、UsTxGNN src/ustxgnn/regulatory/page_format.py 的核心流程；
本站的字樣與頁首規則細節在同目錄 site.py（HEADER_RULE 等）。scripts/apply_drug_reviews.py 與 gate（scripts/check_seo_docs.py）
都呼叫這裡，規則只有一份。

頁首等級規則：頁首（front matter evidence_level、parent、頁首「<等級標籤>: **Lx**」列）＝快速總覽表「證據等級」列：
  HEADER_RULE="first"：儲存格裡第一個等級（主預測）；HEADER_RULE="max"：儲存格裡最高等級（數字最小）。
  各站用哪一條，是 2026-11-12 依該站現有頁面實測的（頁首全部符合的那一條；見 site.py 的說明），不改現有等級。
  儲存格沒有任何 Lx 或沒有這一列：頁首不動。頁首已是 N/A 的頁（已知用途／沒有保留預測，checker P1 要求 N/A）不依總覽格重算
  （site.HEADER_KEEP_NA）。site.HEADER_EXCEPTIONS 列的頁維持現有等級（2026-11-12 實測與規則不符、需要重審的頁，同時列在
  docs/_data/drug_reviews_uncertain.json；重審後經 rereview_result 改等級，再從例外清單拿掉）。
  主預測重審撤回：查核紀錄的 table_updates 把總覽等級格換成撤回字樣（site.WITHDRAWN_RE，格內不再有 Lx）時，頁首改取本頁其他
  預測表（表頭有等級欄的表）保留的最高等級；沒有就是 N/A，parent 歸 docs/known-uses.md 的 title。
description 的等級：action: description_level 紀錄由 apply_drug_reviews.py 呼叫 sync_description_level，只換 description 裡
  「<等級字樣> Lx」的 Lx（N/A 頁換成 site.NA_DESC），其他文字一字不動。母目錄 .claude/sync_description_levels.py 走同一條規則。
表格前後空行：規則與修法在本站 scripts/fix_table_spacing.py（gate 既有項目），這裡直接用它。
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

from . import site as C

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs"
EVIDENCE_PAGES = {"evidence-high.md": (1, 2), "evidence-medium.md": (3, 4), "evidence-low.md": (5, 5)}  # 標題沒寫等級範圍時用
KNOWN_USES_PAGE = "known-uses.md"
NA = "N/A"
_LBL = "|".join(re.escape(x) for x in C.OVERVIEW_LEVEL_LABELS)
OVERVIEW_ROW_RE = re.compile(rf"^\|\s*(?:{_LBL})\s*\|([^|\n]*)\|", re.M)
REVIEW_BLOCK_RE = re.compile(r"<!-- review:begin (\S+) -->.*?<!-- review:end \1 -->", re.S)
LEVEL_RE = r"(?:L[1-5]|N/A)"
HEADER_RE = re.compile(rf"^({re.escape(C.HEADER_LABEL)}\s*[:：]\s*\*\*)({LEVEL_RE})(\*\*)", re.M)
_PARENTS: dict = {}


def _fts():
    s = importlib.util.spec_from_file_location(f"{C.SITE}_fix_table_spacing", ROOT / "scripts" / "fix_table_spacing.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


_FTS = _fts()


def best_level(cell: str) -> str | None:
    lv = re.findall(r"L([1-5])", cell or "")
    return f"L{min(lv)}" if lv else None


def first_level(cell: str) -> str | None:
    m = re.search(r"L([1-5])", cell or "")
    return f"L{m.group(1)}" if m else None


def cell_level(cell: str) -> str | None:
    return first_level(cell) if C.HEADER_RULE == "first" else best_level(cell)


def overview_level(text: str) -> str | None:
    m = OVERVIEW_ROW_RE.search(REVIEW_BLOCK_RE.sub("", text))
    return cell_level(m.group(1)) if m else None


def overview_withdrawn(text: str) -> bool:
    m = OVERVIEW_ROW_RE.search(REVIEW_BLOCK_RE.sub("", text))
    return bool(m and C.WITHDRAWN_RE.match(m.group(1)) and not best_level(m.group(1)))


def other_prediction_levels(text: str) -> list[str]:
    """快速總覽以外、表頭有等級欄的表格裡，該欄的等級（查核框與程式碼區塊內不算）。"""
    text = REVIEW_BLOCK_RE.sub("", text)
    out, col, fence = [], None, False
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("```"):
            fence = not fence
        if fence or not ln.startswith("|"):
            col = None
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        prev = lines[i - 1] if i else ""
        if not prev.startswith("|"):  # 表頭列
            col = next((k for k, c in enumerate(cells) if c in C.OVERVIEW_LEVEL_LABELS), None)
            continue
        if col is None or set(ln.replace("|", "").strip()) <= set("-: "):
            continue
        if col < len(cells):
            lv = best_level(cells[col])
            if lv:
                out.append(lv)
    return out


def target_level(text: str, stem: str | None = None) -> str | None:
    if stem and stem in C.HEADER_EXCEPTIONS:
        return None
    if C.HEADER_KEEP_NA and header_state(text)["evidence_level"] == NA and not overview_withdrawn(text):
        return None
    best = overview_level(text)
    if best:
        return best
    if overview_withdrawn(text):
        return best_level(" ".join(other_prediction_levels(text))) or NA
    return None


def _title(p: Path):
    m = re.search(r"^title:\s*(.+?)\s*$", p.read_text(encoding="utf-8"), re.M)
    return m.group(1).strip().strip('"').strip("'") if m else None


def parent_titles() -> dict:
    """證據等級 → 列表頁標題（docs/evidence-*.md 的 title；標題有 L 範圍照標題，沒有照檔名；N/A → known-uses.md）。"""
    if not _PARENTS:
        p = DOCS / KNOWN_USES_PAGE
        if p.exists() and _title(p):
            _PARENTS[NA] = _title(p)
        for fname, (lo, hi) in EVIDENCE_PAGES.items():
            p = DOCS / fname
            if not p.exists() or not _title(p):
                continue
            title = _title(p)
            lv = [int(x) for x in re.findall(r"L([1-5])", title)]
            if lv:
                lo, hi = min(lv), max(lv)
            for n in range(lo, hi + 1):
                _PARENTS.setdefault(f"L{n}", title)
    return _PARENTS


def _split_fm(text: str):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    return (text[:end], text[end:]) if end >= 0 else (None, text)


def header_state(text: str) -> dict:
    fm, rest = _split_fm(text)
    fm = fm or ""
    lv = re.search(rf"^evidence_level:[ \t]*({LEVEL_RE})[ \t]*$", fm, re.M)
    par = re.search(r"^parent:[ \t]*(.*?)[ \t]*$", fm, re.M)
    head = HEADER_RE.search(rest)
    return {"evidence_level": lv.group(1) if lv else None,
            "parent": par.group(1).strip().strip('"').strip("'") if par else None,
            "header": head.group(2) if head else None}


def sync_header_level(text: str, stem: str | None = None) -> str:
    best = target_level(text, stem)
    fm, rest = _split_fm(text)
    if not best or fm is None:
        return text
    fm = re.sub(rf"^(evidence_level:[ \t]*){LEVEL_RE}[ \t]*$", lambda x: x.group(1) + best, fm, count=1, flags=re.M)
    parent = parent_titles().get(best)
    if parent:
        fm = re.sub(r"^parent:.*$", lambda x: f"parent: {parent}", fm, count=1, flags=re.M)
    rest = HEADER_RE.sub(lambda x: x.group(1) + best + x.group(3), rest, count=1)
    return fm + rest


DESC_LEVEL_RE = re.compile(rf"({C.DESC_LEVEL_WORD})\s*(L[1-5]|N/A)", re.I)


def _desc_line(fm: str):
    return re.search(r"^description:.*$", fm, re.M)


def description_level_text(level: str, word: str | None = None) -> str:
    return C.NA_DESC if level == NA else f"{word or C.DESC_LEVEL_DEFAULT} {level}"


def sync_description_level(text: str) -> str:
    fm, rest = _split_fm(text)
    lv = header_state(text)["evidence_level"]
    m = _desc_line(fm or "")
    if not m or not lv:
        return text
    line = DESC_LEVEL_RE.sub(lambda x: description_level_text(lv, x.group(1)), m.group(0))
    return fm[:m.start()] + line + fm[m.end():] + rest


def description_level_problems(text: str) -> list[str]:
    fm, _ = _split_fm(text)
    lv = header_state(text)["evidence_level"]
    m = _desc_line(fm or "")
    if not m or not lv:
        return []
    bad = sorted({x[1].upper() for x in DESC_LEVEL_RE.findall(m.group(0)) if x[1].upper() != lv})
    return [f"description 寫「{x}」，頁首等級={lv}" for x in bad]


def header_problems(text: str, stem: str | None = None) -> list[str]:
    best = target_level(text, stem)
    st = header_state(text)
    if not best:
        want = parent_titles().get(NA)
        if st["evidence_level"] == NA and want and st["parent"] is not None and st["parent"] != want:  # 沒有 parent 的頁（noindex／nav_exclude）不查
            return [f"parent={st['parent']}，N/A 頁應為 {want}（docs/known-uses.md 的 title）"]
        return []
    errs = []
    if st["evidence_level"] != best:
        errs.append(f"front matter evidence_level={st['evidence_level']}，快速總覽等級（規則 {C.HEADER_RULE}）={best}")
    if st["header"] not in (None, best):
        errs.append(f"頁首等級列={st['header']}，快速總覽等級={best}")
    want = parent_titles().get(best)
    if want and st["parent"] is not None and st["parent"] != want:
        errs.append(f"parent={st['parent']}，應為 {want}")
    return errs


def fix_table_spacing(text: str) -> str:
    return _FTS.fix(text)


def table_spacing_problems(text: str) -> list[str]:
    return [f"第 {i + 1} 行的表格{'前' if k == 'before' else '後'}面缺空行" for k, i in _FTS.problems(text)]
