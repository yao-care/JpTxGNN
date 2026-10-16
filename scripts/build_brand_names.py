"""日本產品名（販売名）→ 成分頁 對照表（2026-10-17，U-03 後續）。

來源：data/processed/drug_mapping.csv（承認番号／販売名／原始主成分／標準化成分／drugbank_id），
以及 data/raw/jp_fda_drugs.json 的「商品名一覧」。比對步驟：
  1. 販売名／原始主成分／標準化成分 NFKC 正規化後完全相同 → drugbank_id
  2. 退而取開頭的片假名成分名（例：ケトチフェン点眼液０.０５ → ケトチフェン），對到唯一 drugbank_id
drugbank_id 再對到可收錄的成分頁（front matter 或證據包的 drugbank_id）。
輸出 docs/_data/brand_names.json：{成分頁檔名: [販売名, …]}，成分頁「日本の主な販売名」段與 search-index 的 brands 讀它。
用法：uv run python scripts/build_brand_names.py
"""
import csv, json, re, unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRUGS = ROOT / "docs/_drugs"
OUT = ROOT / "docs/_data/brand_names.json"
KANA_HEAD = re.compile(r"^[ァ-ヶー]{3,}")


def norm(s):
    return re.sub(r"[\s_・\-－（）()「」『』､、,，.]", "", unicodedata.normalize("NFKC", s or "")).lower()


def kana_head(s):
    m = KANA_HEAD.match(unicodedata.normalize("NFKC", s or ""))
    return m.group(0) if m else None


def main():
    rows = list(csv.DictReader(open(ROOT / "data/processed/drug_mapping.csv", encoding="utf-8-sig")))
    exact, head = {}, defaultdict(set)
    for r in rows:
        db = r.get("drugbank_id")
        if not db:
            continue
        for k in ("販売名", "原始主成分", "標準化成分"):
            exact.setdefault(norm(r[k]), db)
        h = kana_head(r["原始主成分"]) or kana_head(r["標準化成分"])
        if h:
            head[h].add(db)
    # drugbank_id → 可收錄成分頁
    id2page = {}
    def indexable(p):
        t = p.read_text(encoding="utf-8", errors="replace")[:3000]
        return 'http-equiv="refresh"' not in t and not re.search(r"^noindex:\s*true", t, re.M)
    for f in DRUGS.glob("*.md"):
        m = re.search(r"^drugbank_id:\s*(DB\d+)", f.read_text(encoding="utf-8", errors="replace")[:3000], re.M)
        if m and indexable(f):
            id2page.setdefault(m.group(1), f.stem)
    for b in (ROOT / "data/bundles").glob("*/drug_bundle.json"):
        try:
            db = json.load(open(b, encoding="utf-8"))["drug"].get("drugbank_id")
        except Exception:
            continue
        p = DRUGS / f"{b.parent.name}.md"
        if db and p.exists() and indexable(p):
            id2page.setdefault(db, b.parent.name)

    def lookup(name):
        db = exact.get(norm(name))
        if not db:
            h = kana_head(name)
            cands = head.get(h) if h else None
            db = next(iter(cands)) if cands and len(cands) == 1 else None
        return id2page.get(db) if db else None

    brands = defaultdict(set)
    for r in rows:
        page = id2page.get(r.get("drugbank_id")) if r.get("drugbank_id") else lookup(r["販売名"])
        if page and r["販売名"]:
            brands[page].add(unicodedata.normalize("NFKC", r["販売名"]).strip())
    # jp_fda_drugs.json「商品名一覧」：真正的商品名（例：ガスター），去掉廠商括號與「後発品」標記，排在前面
    trade = defaultdict(set)
    num2db = {r["承認番号"]: r.get("drugbank_id") for r in rows}
    try:
        raw = json.load(open(ROOT / "data/raw/jp_fda_drugs.json", encoding="utf-8"))
    except Exception:
        raw = []
    for d in raw:
        db = num2db.get(str(d.get("承認番号", "")))
        page = id2page.get(db) if db else lookup(d.get("販売名", ""))
        if not page:
            continue
        for line in str(d.get("商品名一覧", "")).split("\n"):
            nm = re.sub(r"\s*[(（][^)）]*[)）]\s*$", "", line.replace("後発品", "")).strip()
            nm = unicodedata.normalize("NFKC", nm)
            if nm and len(nm) <= 30:
                trade[page].add(nm)
    # 以產品名命名的筆記（原本生成過產品名頁）也併入
    for d in (ROOT / "data/notes").iterdir():
        if d.is_dir() and re.search(r"[゠-ヿ＀-￯]", d.name):
            page = lookup(d.name)
            if page:
                brands[page].add(unicodedata.normalize("NFKC", d.name).replace("_", " ").strip())
    pages = set(brands) | set(trade)
    out = {k: (sorted(trade.get(k, set())) + sorted(brands.get(k, set()) - trade.get(k, set())))[:40] for k in sorted(pages)}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"成分頁 {len(out)} 頁、販売名 {sum(len(v) for v in out.values())} 個 → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
