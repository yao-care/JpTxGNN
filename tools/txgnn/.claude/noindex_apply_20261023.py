"""上線時開 noindex（2026-10-23 接續清單步驟 5）。

只讀 .claude/audit_20261016/m2/classification.tsv 的 no_pred_noindex（449 頁）：
front matter 加 noindex: true、sitemap: false（寫法同 url_cleanup_20261016.py）。
classification 裡其他類別的頁若有 noindex: true 只列出不動（checker N1 會擋）。
各站 head_custom.html 必須已有 robots 那行，沒有就列出。

用法（母目錄）：python3 .claude/noindex_apply_20261023.py [--apply] [站 ...]
不加 --apply 只算數。套用後跑 python3 .claude/check_drug_page.py --noindex 驗證，
再重跑 search-index／llms 等衍生檔（rebuild_search_index.py 會排除 noindex 頁）。
"""
import csv, re, sys
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parents[1]
CL = BASE / ".claude/audit_20261016/m2/classification.tsv"
ROBOTS = '{% if page.noindex %}<meta name="robots" content="noindex">{% endif %}'


def split_fm(b: bytes):
    nl = b"\r\n" if b"\r\n" in b[:300] else b"\n"
    m = re.match(rb"(?:\xef\xbb\xbf)?---\r?\n(.*?)\r?\n---\r?\n", b, re.S)
    return nl, m


def add_fm(b: bytes, nl: bytes, m, items):
    fm = m.group(1).decode("utf-8")
    add = [f"{k}: {v}" for k, v in items if not re.search(rf"^{k}:", fm, re.M)]
    if not add:
        return b
    start = m.start(1)
    return b[:start] + nl.join(a.encode() for a in add) + nl + b[start:]


def main(argv):
    apply = "--apply" in argv
    sites = [a for a in argv if a.endswith("TxGNN")]
    rows = [r for r in csv.DictReader(open(CL, encoding="utf-8"), delimiter="\t") if not sites or r["site"] in sites]
    c, problems = Counter(), []
    for r in rows:
        f = BASE / r["site"] / "docs/_drugs" / f"{r['page']}.md"
        if not f.exists():
            problems.append(f"缺檔 {r['site']}:{r['page']}")
            continue
        b = f.read_bytes()
        nl, m = split_fm(b)
        if not m:
            problems.append(f"無 front matter {r['site']}:{r['page']}")
            continue
        has = bool(re.search(r"^noindex:\s*true", m.group(1).decode("utf-8"), re.M))
        if r["class"] != "no_pred_noindex":
            if has:
                problems.append(f"非 no_pred_noindex 卻有 noindex {r['site']}:{r['page']} class={r['class']}")
            continue
        c["target"] += 1
        nb = add_fm(b, nl, m, [("noindex", "true"), ("sitemap", "false")])
        if nb == b:
            c["already"] += 1
            continue
        c["write"] += 1
        if apply:
            f.write_bytes(nb)
    for s in sorted({r["site"] for r in rows}):
        hc = BASE / s / "docs/_includes/head_custom.html"
        if not hc.exists() or ROBOTS not in hc.read_text(encoding="utf-8"):
            problems.append(f"head_custom 缺 robots {s}")
    for p in problems:
        print(p)
    print(("已寫入" if apply else "dry-run"), dict(c), "問題", len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
