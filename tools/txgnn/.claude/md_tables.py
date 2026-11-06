#!/usr/bin/env python3
"""Markdown 表格的共用小工具（2026-11-03）：表格前後補空行、表格格子清理。

為什麼需要：
    kramdown（GitHub Pages 的 Markdown 引擎）要求表格前後是空行。標題下一行直接接表格
    （「## Quick overview」＋「| Item | Content |」），或表格最後一列下一行直接接「## Disclaimer」，
    整張表會被排成一段純文字（線上看到 `| 項目 | 內容 | |——|——|`）。格子裡帶換行也一樣：
    表格在換行處斷掉，後半列變成純文字。2026-11-03 實測 29 站約 5,000 處，來源是
    known_use_pages_20261022.py 的版面樣板（標題緊接表格）與各站 writer 產出的 notes 結尾沒有換行
    （sync 接上「\\n## Disclaimer」後表格緊貼標題）。

規則（與 HkTxGNN scripts/fix_table_spacing.py、TwTxGNN page_format.fix_table_spacing 同）：
    - 表格＝以 `|` 開頭的一行，下一行是分隔列（`|---|---|`）；延續到最後一個以 `|` 開頭的連續行。
    - 表格前一行不是空行、不是表格行、不是 kramdown 屬性列 `{:` → 補一個空行。
    - 表格後一行不是空行、不是 `{:`（屬性列要緊貼表格）、不是 Liquid `{%`（for 迴圈產生的列）→ 補一個空行。
    - 跳過 front matter、``` ／ ~~~ 程式碼區塊。只補空行，不改任何字；CRLF 保留。

用法：
    import：problems(text)、fix_table_spacing(text)、cell(value, limit)
    CLI（只讀，不改檔；p9_content_check.sh 用）：
        python3 .claude/md_tables.py --report <站目錄> [...]
        每站輸出一行「頁數<TAB>處數」，有問題的頁（最多 5 頁）列在 stderr。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SEP = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")


def _fm_end(lines: list[str]) -> int:
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return i + 1
    return 0


def _is_row(line: str) -> bool:
    return line.lstrip().startswith("|")


def problems(text: str) -> list[tuple[str, int]]:
    """回傳 [('before'|'after', 行號)]：要在該行之前補一個空行的位置（行號以 \\n 切分計）。"""
    lines = text.replace("\r\n", "\n").split("\n")
    start = _fm_end(lines)
    out: list[tuple[str, int]] = []
    fence = False
    i = start
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
            i += 1
            continue
        if not fence and _is_row(line) and i + 1 < len(lines) and SEP.match(lines[i + 1]):
            prev = lines[i - 1] if i > start else ""
            if prev.strip() and not _is_row(prev) and not prev.lstrip().startswith("{:"):
                out.append(("before", i))
            j = i + 2
            while j < len(lines) and _is_row(lines[j]):
                j += 1
            if j < len(lines):
                nxt = lines[j].lstrip()
                if nxt and not nxt.startswith(("{:", "{%")):
                    out.append(("after", j))
            i = j
            continue
        i += 1
    return out


def fix_table_spacing(text: str) -> str:
    """表格前後補空行；沒有問題時原樣回傳（同一個物件）。"""
    probs = problems(text)
    if not probs:
        return text
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.replace("\r\n", "\n").split("\n")
    for _, idx in sorted(probs, key=lambda p: p[1], reverse=True):
        lines.insert(idx, "")
    return nl.join(lines)


def cell(value, limit: int | None = None) -> str:
    """表格格子：換行與連續空白收成一個空格、`|` 換成 `/`（兩者都會把表格拆壞），再截長度。"""
    s = re.sub(r"\s+", " ", str(value if value is not None else "")).replace("|", "/").strip()
    return s[:limit] if limit else s


def _site_pages(site: Path):
    docs = site / "docs"
    for f in sorted(docs.rglob("*.md")):
        rel = f.relative_to(docs).parts
        if rel[0] in ("_site", "vendor", ".jekyll-cache", "node_modules"):
            continue
        t = f.read_text(encoding="utf-8", errors="replace")
        head = t[:3000]
        if re.search(r"^layout:\s*id_redirect", head, re.M) or 'http-equiv="refresh"' in head:
            continue
        yield f, t


def report(site_dirs: list[str]) -> int:
    for d in site_dirs:
        site = Path(d)
        bad = [(f, len(p)) for f, t in _site_pages(site) if (p := problems(t))]
        print(f"{len(bad)}\t{sum(n for _, n in bad)}")
        for f, n in bad[:5]:
            print(f"{f.relative_to(site / 'docs')}({n})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--report"] and len(a) > 1:
        raise SystemExit(report(a[1:]))
    raise SystemExit(__doc__)
