#!/usr/bin/env python3
"""Markdown 表格前後補空行（2026-11-03）。

為什麼需要這支：
    kramdown（GitHub Pages 的 Markdown 引擎）要求表格前後都是空行。
    「## 早見表／## クイック概要」標題下一行直接接表格，或表格最後一列下一行直接接「## 免責事項」，
    整張表會被排成一段純文字（線上看到的是 `| 項目 | 内容 | |---|---|`）。
    2026-11-03 實測：本站 99 個藥物頁、366 處有這個問題（多半是「快速概覽」表與
    已核准／同類別／知識圖譜各小節標題下的表）。這是渲染錯誤，不是內容問題：只補空行，不改任何字。

規則：
    - 表格＝以 `|` 開頭的一行，下一行是分隔列（`|---|---|`）；表格延續到最後一個以 `|` 開頭的連續行。
    - 表格前一行不是空行、也不是表格行 → 補一個空行。
    - 表格後一行不是空行、不是 `{:`（kramdown 屬性列要緊貼表格）、也不是 Liquid `{%` → 補一個空行。
    - 跳過 front matter、``` 程式碼區塊、轉址頁（layout: id_redirect）。

用法：
    python3 scripts/fix_table_spacing.py            # 修正並列出改了哪些檔
    python3 scripts/fix_table_spacing.py --check    # 只檢查；有問題回非零（scripts/check_seo_docs.py 也會呼叫）
    python3 scripts/fix_table_spacing.py --touch    # 修正，並把有改到的藥物頁 last_modified_at 設成今天
                                                    # （表格從純文字變成表格，頁面確實變了，sitemap lastmod 應反映）
"""
from __future__ import annotations

import datetime as _dt
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
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
    """回傳 [('before'|'after', 行號)]：需要在該行之前補空行的位置。"""
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
            if prev.strip() and not _is_row(prev):
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


def fix(text: str) -> str:
    probs = problems(text)
    if not probs:
        return text
    nl = "\r\n" if "\r\n" in text else "\n"  # 保留原檔換行字元
    lines = text.replace("\r\n", "\n").split("\n")
    for _, idx in sorted(probs, key=lambda p: p[1], reverse=True):
        lines.insert(idx, "")
    return nl.join(lines)


def targets() -> list[Path]:
    out = []
    for f in sorted(DOCS.rglob("*.md")):
        rel = f.relative_to(DOCS).parts
        if rel[0] in ("_site", "vendor", ".jekyll-cache", "node_modules"):
            continue
        head = f.read_text(encoding="utf-8", errors="replace")[:600]
        if re.search(r"^layout:\s*id_redirect", head, re.M):
            continue
        out.append(f)
    return out


def main(argv: list[str]) -> int:
    check = "--check" in argv
    touch = "--touch" in argv
    today = _dt.date.today().isoformat()
    bad = []
    for f in targets():
        t = f.read_bytes().decode("utf-8")
        probs = problems(t)
        if not probs:
            continue
        bad.append((f, len(probs)))
        if check:
            continue
        new = fix(t)
        if touch and f.parent.name == "_drugs":
            new = re.sub(r"^(last_modified_at:\s*)\d{4}-\d{2}-\d{2}", rf"\g<1>{today}", new, count=1, flags=re.M)
        f.write_bytes(new.encode("utf-8"))
    if check:
        for f, n in bad:
            print(f"  - {f.relative_to(DOCS)}：{n} 處表格前後缺空行（跑 scripts/fix_table_spacing.py）")
        return 1 if bad else 0
    print(f"[table-spacing] 修正 {len(bad)} 個檔、{sum(n for _, n in bad)} 處")
    for f, n in bad:
        print(f"    {f.relative_to(DOCS)}  {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
