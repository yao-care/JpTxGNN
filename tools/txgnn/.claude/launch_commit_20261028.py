"""上線提交（2026-10-28）：各站 commit docs／scripts／prompts → pull --rebase → 解衝突 → gate → push。

衝突處理（pm 2026-10-27 定案）：docs/_drugs/*.md 跟 origin「藥物頁只留一個 h1」commit 衝突時，取本機版（事實層＋批次結果），
再用 origin 同一套規則（頁首 `# 藥名` 之外的 `# ` 降為 `## ` 並掛 `{: .text-alpha }`）處理，每頁恰好一個 h1。
其他檔案衝突：不自動解，該站停下、列出來。gate（scripts/check_seo_docs.py）不過不推。
用法（母目錄）：python3 .claude/launch_commit_20261028.py [--push] 站 ...
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
MSG = """fix: 藥物頁事實層改由程式產生（kept／license_facts），無預測頁改「目前無保留預測」版面，FHIR／search-index 依 kept 重產，449 頁 noindex

- 概覽表主預測 kept[0]、分數 0.xxxx、原適應症（有效單方本地許可證原文，沒有寫未記載）、市場狀態與張數由程式產生
- checker 報的違規句整句刪除；已歸零的頁不動
- sync_notes_to_docs.py 寫頁後自動套用事實層（notes 舊事實不再蓋回頁面）
- prompts：分數寫 4 位小數、主預測＝第一筆、不提知識圖譜、原適應症由程式填

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013aGXmSFHkDr36Tyvwp1kkA"""


def git(site, *a, check=False):
    r = subprocess.run(["git", *a], cwd=BASE / site, capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(a)}: {r.stderr[-300:]}")
    return r


def demote(text):
    """頁首 `# 藥名`（下一行 {: .fs-9 }）以外、code fence 以外的 `# ` → `## ` ＋ {: .text-alpha }（同 origin demote_body_h1）"""
    lines = text.split("\n")
    out, fence, first = [], False, True
    for i, l in enumerate(lines):
        if l.lstrip().startswith(("```", "~~~")):
            fence = not fence
        if not fence and l.startswith("# "):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if first and nxt.strip() == "{: .fs-9 }":
                first = False
                out.append(l); continue
            out.append("#" + l)
            if nxt.strip() != "{: .text-alpha }":
                out.append("{: .text-alpha }")
            continue
        out.append(l)
    return "\n".join(out)


def h1_count(text):
    fence, n = False, 0
    for l in text.split("\n"):
        if l.lstrip().startswith(("```", "~~~")):
            fence = not fence
        elif not fence and l.startswith("# "):
            n += 1
    return n


def in_rebase(site):
    gd = BASE / site / ".git"
    return (gd / "rebase-merge").exists() or (gd / "rebase-apply").exists()


def resolve(site):
    """rebase 停在衝突：docs/_drugs 取本機版＋demote；其他檔有衝突就回報"""
    un = [x for x in git(site, "diff", "--name-only", "--diff-filter=U").stdout.split("\n") if x]
    # 新聞頁與新聞索引歸 CI 排程產生：衝突一律取 origin（ours）
    ci = [x for x in un if x.startswith(("docs/_news/", "data/news/")) or x in ("docs/data/news-index.json", "docs/_data/drug_news.json")]
    for x in ci:
        if git(site, "checkout", "--ours", "--", x).returncode:  # origin 已刪掉這頁 → 跟著刪
            git(site, "rm", "-q", "--", x, check=True)
        else:
            git(site, "add", "--", x, check=True)
    un = [x for x in un if x not in ci]
    # pull 之後會依頁面重產的衍生檔：先取本機版讓 rebase 繼續，之後 gen_drug_stats／update_home_counts／sync_llms 重產
    derived = [x for x in un if x in ("docs/llms-full.txt", "docs/llms.txt", "docs/_data/drug_stats.json", "docs/_data/site_stats.yml", "README.md")]
    for x in derived:
        git(site, "checkout", "--theirs", "--", x, check=True)
        git(site, "add", "--", x, check=True)
    un = [x for x in un if x not in derived]
    other = [x for x in un if not x.startswith("docs/_drugs/")]
    if other:
        return other
    for x in un:
        git(site, "checkout", "--theirs", "--", x, check=True)  # rebase 中 theirs＝本機這次的 commit
        p = BASE / site / x
        raw = p.read_bytes().decode("utf-8")
        crlf = "\r\n" in raw[:500]
        t = demote(raw.replace("\r\n", "\n"))
        p.write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))
        git(site, "add", "--", x, check=True)
    return []


def main(argv):
    push = "--push" in argv
    sites = [a for a in argv if a.endswith("TxGNN")]
    for s in sites:
        try:
            if not in_rebase(s):  # 上次停在 rebase 中：直接接著解衝突
                git(s, "add", "docs/", "scripts/", "prompts/", check=True)
                if git(s, "diff", "--cached", "--quiet").returncode:
                    git(s, "commit", "-q", "-m", MSG, check=True)
                git(s, "pull", "--rebase", "--autostash")
            rounds = 0
            while in_rebase(s) and rounds < 20:
                bad = resolve(s)
                if bad:
                    print(f"✗ {s}：非藥物頁衝突，停下：{bad[:5]}"); break
                e = dict(__import__("os").environ); e["GIT_EDITOR"] = "true"
                subprocess.run(["git", "rebase", "--continue"], cwd=BASE / s, capture_output=True, text=True, env=e)
                rounds += 1
            if in_rebase(s):
                continue
            # pull 後站上有了 generate_drug_stats.py 等：衍生檔依公開頁重算，有變就再 commit
            for cmd in ([sys.executable, ".claude/gen_drug_stats.py", s], [sys.executable, ".claude/update_home_counts.py", s],
                        [sys.executable, ".claude/sync_llms_descriptions.py", s], [sys.executable, ".claude/prune_search_index_20261028.py", s],
                        [sys.executable, ".claude/gen_hreflang_20261029.py", "--apply", s], [sys.executable, ".claude/gen_local_home_20261029.py", "--apply", s]) + \
                       (([sys.executable, ".claude/apply_brand_names.py", s],) if s == "JpTxGNN" else ()):
                subprocess.run(cmd, cwd=BASE, capture_output=True, text=True)
            git(s, "add", "-A", "docs", "README.md")
            if git(s, "diff", "--cached", "--quiet").returncode:
                git(s, "commit", "-q", "-m", "fix: drug_stats、首頁數字、llms 清單依公開頁重算\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_013aGXmSFHkDr36Tyvwp1kkA", check=True)
            # 每頁恰好一個 h1（藥物頁）
            multi = []
            for f in (BASE / s / "docs/_drugs").glob("*.md"):
                t = f.read_text(encoding="utf-8", errors="replace")
                if "http-equiv" in t[:3000] or "layout: id_redirect" in t[:3000]:
                    continue
                if h1_count(t) != 1:
                    multi.append(f.name)
            g = subprocess.run([sys.executable, "scripts/check_seo_docs.py"], cwd=BASE / s, capture_output=True, text=True)
            ok = g.returncode == 0
            ahead = git(s, "rev-list", "--count", "@{u}..HEAD").stdout.strip()
            print(f"{'✓' if ok and not multi else '✗'} {s} ahead={ahead} h1≠1:{len(multi)} {multi[:3]} gate={'ok' if ok else g.stdout.strip().splitlines()[-1][:120]}")
            if push and ok and not multi:
                git(s, "pull", "-q", "--rebase")
                p = git(s, "push", "-q")
                print(f"  push {s}: {'ok' if p.returncode == 0 else p.stderr[-200:]}")
        except Exception as e:
            print(f"✗ {s}：{e}")


if __name__ == "__main__":
    main(sys.argv[1:])
