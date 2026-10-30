"""藥物頁 last_modified_at 依「正文實際改動日」修正（2026-10-29，pm 驗收：10/28 起改過的頁有 19,217 頁仍是舊日期）。

規則（不用 AI）：
  - 基準＝台北 10/28 00:00 前最後一個 commit。之後每個 commit（含工作區未提交的改動，日期算今天）逐一比對藥物頁正文。
  - 正文＝去掉 front matter、每行去尾空白、去掉空行後的內容；只有空白或 front matter 變動的不算改動。
  - 正文最後一次改變的那個 commit 的台北日期 → last_modified_at；正文跟基準相同的頁不動。
  - 只改 front matter 的 last_modified_at 一行（沒有就加在 front matter 結尾前）；CRLF 保留。
用法（母目錄）：python3 .claude/lastmod_fix_20261029.py [--apply] 站 ...
"""
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TPE = timezone(timedelta(hours=8))
SINCE = "2026-10-28 00:00 +0800"
FM = re.compile(r"\A﻿?---\r?\n.*?\r?\n---\r?\n", re.S)


def body(text):
    if text is None:
        return None
    t = FM.sub("", text.replace("\r\n", "\n"), count=1)
    return "\n".join(l.rstrip() for l in t.split("\n") if l.strip())


class Cat:
    """git cat-file --batch：一次讀很多 blob"""
    def __init__(self, repo):
        self.p = subprocess.Popen(["git", "cat-file", "--batch"], cwd=repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def get(self, rev, path):
        self.p.stdin.write(f"{rev}:{path}\n".encode()); self.p.stdin.flush()
        head = self.p.stdout.readline().decode()
        if head.endswith("missing\n"):
            return None
        n = int(head.split()[2])
        data = self.p.stdout.read(n); self.p.stdout.read(1)
        return data.decode("utf-8", errors="replace")


def git(repo, *a):
    return subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True).stdout


def main(argv):
    apply_ = "--apply" in argv
    today = datetime.now(TPE).strftime("%Y-%m-%d")
    for s in [a for a in argv if a.endswith("TxGNN")]:
        repo = BASE / s
        base = git(repo, "rev-list", "-1", f"--before={SINCE}", "HEAD").strip()
        commits = [l.split() for l in git(repo, "log", "--reverse", "--format=%H %ct", f"{base}..HEAD").split("\n") if l.strip()]
        cat = Cat(repo)
        last = {}  # path -> 日期
        prev_rev = base
        for h, ct in commits:
            files = [x for x in git(repo, "diff", "--name-only", prev_rev, h, "--", "docs/_drugs").split("\n") if x.endswith(".md")]
            day = datetime.fromtimestamp(int(ct), TPE).strftime("%Y-%m-%d")
            for f in files:
                if body(cat.get(prev_rev, f)) != body(cat.get(h, f)):
                    last[f] = day
            prev_rev = h
        # 工作區未提交的改動
        for f in [x for x in git(repo, "diff", "--name-only", "HEAD", "--", "docs/_drugs").split("\n") if x.endswith(".md")]:
            p = repo / f
            if p.exists() and body(cat.get("HEAD", f)) != body(p.read_text(encoding="utf-8", errors="replace")):
                last[f] = today
        changed = 0
        for f, day in last.items():
            p = repo / f
            if not p.exists():
                continue
            raw = p.read_bytes().decode("utf-8", errors="replace")
            if body(cat.get(base, f)) == body(raw):
                continue  # 改來改去又回到基準：不算改動
            crlf = "\r\n" in raw[:500]
            t = raw.replace("\r\n", "\n")
            m = FM.match(t)
            if not m:
                continue
            fm = t[:m.end()]
            cur = re.search(r"^last_modified_at:\s*(\S+)", fm, re.M)
            if cur and cur.group(1) == day:
                continue
            if cur:
                fm2 = re.sub(r"^last_modified_at:.*$", f"last_modified_at: {day}", fm, count=1, flags=re.M)
            else:
                fm2 = re.sub(r"\n---\n\Z", f"\nlast_modified_at: {day}\n---\n", fm)
            t2 = fm2 + t[m.end():]
            changed += 1
            if apply_:
                p.write_bytes((t2.replace("\n", "\r\n") if crlf else t2).encode("utf-8"))
        cat.p.stdin.close()
        print(f"{s}: 基準 {base[:8]}、commit {len(commits)}、正文有改的頁 {len(last)}、lastmod 要更新 {changed}{'（已寫入）' if apply_ else ''}")


if __name__ == "__main__":
    main(sys.argv[1:])
