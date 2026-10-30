"""首頁藥物數／預測適應症數改由實際頁面計算（2026-10-16，pm SEO 稽核 #2）。

計算口徑：可收錄的藥物頁（docs/_drugs 排除 dbNNNNN 轉址頁、nav_exclude、noindex 頁）；
預測新適應症數＝這些頁 front matter indication_count 合計。

用法：python3 .claude/update_home_counts.py [站 ...]
  數字存在 docs/_data/site_stats.yml；首頁 index.md 中與上次數字相同的寫死數字會換成新數字。
  第一次執行用 --seed 舊藥物數,舊適應症數 指定首頁現有的寫死數字（可用逗號分隔多個舊值，以 / 分隔兩組）。
"""
import re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def counts(proj: Path):
    """drugs＝可收錄的藥物頁數（排除 ID 轉址頁、nav_exclude、noindex）；indications＝這些頁的 indication_count 合計。"""
    n = ind = 0
    for f in (proj / "docs/_drugs").glob("*.md"):
        t = f.read_text(encoding="utf-8", errors="replace")
        if re.fullmatch(r"db\d+", f.stem.lower()) or 'http-equiv="refresh"' in t:
            continue
        head = t[:1500]
        if re.search(r"^(nav_exclude|noindex):\s*true", head, re.M):
            continue
        n += 1
        m = re.search(r"^indication_count:\s*(\d+)", head, re.M)
        ind += int(m.group(1)) if m else 0
    return n, ind


def fmt(n):
    return f"{n:,}"


def replace_nums(text: str, olds, new: int):
    for o in olds:
        if not o or o == new:
            continue
        for pat in {fmt(o), str(o)}:
            text = re.sub(rf"(?<![\d,.#-]){re.escape(pat)}(?![\d,.%])", fmt(new), text)
    return text


def main(argv):
    seed = None
    if "--seed" in argv:
        i = argv.index("--seed")
        seed = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    sites = argv or [p.name for p in sorted(BASE.glob("*TxGNN"))]
    for s in sites:
        proj = BASE / s
        idx = proj / "docs/index.md"
        if not idx.exists():
            continue
        stats = proj / "docs/_data/site_stats.yml"
        old_d, old_i = [], []
        if seed:
            a, _, b = seed.partition("/")
            old_d = [int(x) for x in a.replace(" ", "").split(",") if x]
            old_i = [int(x) for x in b.replace(" ", "").split(",") if x]
        elif stats.exists():
            st = dict(re.findall(r"^(\w+):\s*(\d+)", stats.read_text(), re.M))
            old_d, old_i = [int(st.get("drugs", 0))], [int(st.get("indications", 0))]
        d, i = counts(proj)
        raw = idx.read_bytes()
        t = raw.decode("utf-8")
        new = replace_nums(replace_nums(t, old_d, d), old_i, i)
        if new != t:
            idx.write_bytes(new.encode("utf-8"))
        stats.parent.mkdir(exist_ok=True)
        stats.write_text(f"# 由 .claude/update_home_counts.py 產生\ndrugs: {d}\nindications: {i}\n", encoding="utf-8")
        print(f"{s}: drugs {old_d}→{d} indications {old_i}→{i} {'(index.md 已更新)' if new != t else ''}")


if __name__ == "__main__":
    main(sys.argv[1:])
