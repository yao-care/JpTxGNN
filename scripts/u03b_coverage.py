"""U-03 刪除的 262 個產品名頁，在 docs/_data/brand_names.json 的覆蓋情形（2026-10-17）。

演算法（照順序，先符合者歸類）：
  名稱來源：JpTxGNN 提交 40c43ff0 刪除的 docs/_drugs/*.md 檔名，NFKC 後把「_」換回「.」。
  norm()：NFKC → 去掉空白 _ ・ - － （）() 「」『』 ､、,，. → 小寫（與 build_brand_names.norm 相同）。
  1 完全相同：norm(刪除名) 等於對照表任一名稱（trade／hanbai／combo）的 norm
  2 前綴：norm(刪除名) 是某個對照表名稱 norm 的開頭
  3 反向前綴：某個對照表名稱 norm 是 norm(刪除名) 的開頭（長度 ≥ 4）
  4 成分頁存在但沒列：刪除名去規格劑形鹽類後，對到 drug_mapping 的 drugbank_id，而該 ID 有可收錄成分頁
  5 無成分頁：其餘
用法：uv run python scripts/u03b_coverage.py（在 JpTxGNN 目錄）；明細寫到 stdout 之外的 u03b_coverage.json（不進 git）
"""
import csv, glob, importlib.util, json, os, re, subprocess, unicodedata

spec = importlib.util.spec_from_file_location("bb", "scripts/build_brand_names.py")
bb = importlib.util.module_from_spec(spec); spec.loader.exec_module(bb)
names = [l.strip().split("/")[-1][:-3] for l in subprocess.run(
    ["git", "-c", "core.quotepath=false", "show", "--diff-filter=D", "--name-only", "--format=", "40c43ff0", "--", "docs/_drugs"],
    capture_output=True, text=True).stdout.splitlines() if l.strip()]
d = json.load(open("docs/_data/brand_names.json"))
listed = {}
for p, v in d.items():
    for k in v:
        for x in v[k]:
            listed.setdefault(bb.norm(x), p)
b2db = {}
for r in csv.DictReader(open("data/processed/drug_mapping.csv", encoding="utf-8-sig")):
    if r["drugbank_id"]:
        b2db.setdefault(bb.norm(bb.SALT.sub("", bb.base_name(r["原始主成分"]))), r["drugbank_id"])
id2page = {}
for f in glob.glob("docs/_drugs/*.md"):
    t = open(f, errors="replace").read()[:3000]
    if 'http-equiv' in t or re.search(r"^noindex:\s*true", t, re.M):
        continue
    m = re.search(r"^drugbank_id:\s*(DB\d+)", t, re.M)
    s = os.path.basename(f)[:-3]
    if not m and os.path.exists(f"data/bundles/{s}/drug_bundle.json"):
        db = json.load(open(f"data/bundles/{s}/drug_bundle.json"))["drug"].get("drugbank_id")
    else:
        db = m.group(1) if m else None
    if db:
        id2page.setdefault(db, s)
cat = {k: [] for k in ("完全相同", "前綴", "反向前綴", "成分頁存在但沒列", "無成分頁")}
for n in names:
    nn = unicodedata.normalize("NFKC", n).replace("_", ".")
    k = bb.norm(nn)
    if k in listed:
        cat["完全相同"].append(nn)
    elif any(x.startswith(k) for x in listed):
        cat["前綴"].append(nn)
    elif any(len(x) >= 4 and k.startswith(x) for x in listed):
        cat["反向前綴"].append(nn)
    elif id2page.get(b2db.get(bb.norm(bb.SALT.sub("", bb.base_name(nn))))):
        cat["成分頁存在但沒列"].append(nn)
    else:
        cat["無成分頁"].append(nn)
print("共", len(names), "  " + "  ".join(f"{k} {len(v)}" for k, v in cat.items()))
json.dump(cat, open("u03b_coverage.json", "w"), ensure_ascii=False, indent=1)
