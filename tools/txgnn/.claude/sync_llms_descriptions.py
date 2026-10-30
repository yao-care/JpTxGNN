"""llms.txt／llms-full.txt 的頁面清單行，名稱與說明改由頁面 front matter 產生（2026-10-17，T-311）。

只改「- `PATH` 名稱 — 說明」這種清單行：PATH 對應到 docs/ 下 permalink 相同的頁，用該頁的 title 與
description 重寫（description 不存在就不動）。其餘文字（seo-ops 反思層維護的段落）一律不碰。
首頁、/drugs/ 的數字因此跟著 update_home_counts.py 與頁面 front matter 走，不再寫死。
用法：python3 .claude/sync_llms_descriptions.py [站 ...]
"""
import json, re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
LINE = re.compile(r"^- `(/[^`]*)` (.+?) — (.+)$")


def yaml_str(v):
    v = v.strip()
    if v.startswith('"') and v.endswith('"'):
        try:
            return json.loads(v)
        except ValueError:
            return v[1:-1]
    if v.startswith("'") and v.endswith("'"):
        return v[1:-1].replace("''", "'")
    return v


def pages(proj: Path) -> dict:
    out = {}
    for f in list((proj / "docs").glob("*.md")) + list((proj / "docs").glob("*/index.md")):
        t = f.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"(?:﻿)?---\r?\n(.*?)\r?\n---", t, re.S)
        if not m:
            continue
        fm = m.group(1)
        g = lambda k: (re.search(rf"^{k}:\s*(.+)$", fm, re.M) or [None, None])[1]
        pl = g("permalink")
        if not pl:
            pl = "/" if f.name == "index.md" and f.parent.name == "docs" else None
        if pl and g("description"):
            out[yaml_str(pl)] = (yaml_str(g("title") or ""), yaml_str(g("description")))
    return out


def main(argv):
    sites = argv or [p.name for p in sorted(BASE.glob("*TxGNN"))]
    for s in sites:
        proj = BASE / s
        pg = pages(proj)
        n = 0
        for name in ("llms.txt", "llms-full.txt"):
            f = proj / "docs" / name
            if not f.exists():
                continue
            b = f.read_bytes()
            nl = "\r\n" if b"\r\n" in b else "\n"
            lines = b.decode("utf-8").split(nl)
            for i, l in enumerate(lines):
                m = LINE.match(l)
                if m and m.group(1) in pg:
                    title, desc = pg[m.group(1)]
                    new = f"- `{m.group(1)}` {title or m.group(2)} — {desc}"
                    if new != l:
                        lines[i] = new
                        n += 1
            out = nl.join(lines).encode("utf-8")
            if out != b:
                f.write_bytes(out)
        print(f"{s}: {n} 行更新")


if __name__ == "__main__":
    main(sys.argv[1:])
