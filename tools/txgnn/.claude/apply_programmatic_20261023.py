"""第 6 步：不用模型的頁面處理（2026-10-23，pm 定案）。只動 check_drug_page.py 會檢查的格子，其他一字不動。

對 M2 分類為 keep、regen(only_removed) 的頁：
  1. front matter predicted_indications＝kept、indication_count、標題列「預測適應症 **N**」
  2. 帶分數的預測列：分數對不上 kept 的整列刪掉（已移除的預測）
  3. 分數寫法：百分比 → 0.xxxx（用證據包的精確分數，保留該站的小數點符號）；表格與本文（同句有分數字樣）都改
  4. P4：標 L1–L4 但證據包沒有直接研究該病的列 → L5（概覽表等級列、front matter evidence_level／parent、標題列一併改）
  5. 軌 5 v5：本站狀態列、張數列依 license_facts 整格覆寫（Marketed 完整／部分、核准未上市、kr＝Unknown）；
     許可證表裡有效的許可證把註銷字樣換成有效（mv2.VALID_WORD）；Tw 張數列與許可證表由 tfda 程式產生，不動
  6. P5：只做 fix_kg_pred_source 的明確片語替換；替換後仍命中 P5 的頁列入重生
處理完用 check_drug_page.check_page 檢查，仍有錯的頁列入 to_regen.tsv（pm：P3 一律重生、P5 換不掉就重生、其他非 0 也重生）。
CRLF 保留。預設乾跑（寫 diff），--apply 才寫檔。notes 不動（sync 會從 notes 重產頁面的頁，不在這支的範圍）。
用法（母目錄）：python3 .claude/apply_programmatic_20261023.py [--apply] [--any] [--local] [--pages site:page,...] [站 ...]
  --any：不限分類（重生／已知用途頁的後處理）；--local：讀本機檔而不是 HEAD
輸出 .claude/audit_20261016/programmatic/：changes.diff、to_regen.tsv、summary.tsv
"""
import csv
import difflib
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
import os
OUT = Path(os.environ.get("PROG_OUT", BASE / ".claude/audit_20261016/programmatic"))


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


ck = _load("ck", BASE / ".claude/check_drug_page.py")
fk = _load("fk", BASE / ".claude/fix_kg_pred_source_20261022.py")
kf, amf, mv2, rr = ck.kf, ck.amf, ck.mv2, ck.rr
HEAD_N = re.compile(r"^(.*\*\*L\d\*\*[^\n]*?\*\*)(\d+)(\*\*)", re.M)
HEAD_L = re.compile(r"^(.*?\*\*)(L[1-5])(\*\*)", re.M)


def parent_map(site):
    """evidence_level → parent（取該站現有頁最常見的對應）"""
    c = {}
    for f in (BASE / site / "docs/_drugs").glob("*.md"):
        fm = f.read_text(encoding="utf-8", errors="replace")[:1500]
        lv = re.search(r"^evidence_level:\s*(L[1-5])", fm, re.M)
        pa = re.search(r"^parent:\s*(.+)$", fm, re.M)
        if lv and pa:
            c.setdefault(lv.group(1), Counter())[pa.group(1).strip()] += 1
    return {k: v.most_common(1)[0][0] for k, v in c.items()}


_CL = {}


def count_label(site):
    """該站概覽表張數列最常用的標題"""
    if site not in _CL:
        c = Counter()
        for f in list((BASE / site / "docs/_drugs").glob("*.md"))[:400]:
            for line in f.read_text(encoding="utf-8", errors="replace").split("\n")[:80]:
                if line.startswith("|"):
                    cell = line.strip("|").split("|")[0].strip()
                    if ck.is_count_label(cell) and not ck.FOREIGN_ANY.search(cell):
                        c[cell] += 1
        _CL[site] = c.most_common(1)[0][0] if c else "Number of licences"
    return _CL[site]


def fmt_score(v, comma, sample):
    s = f"{v:.4f}"
    return s.replace(".", ",") if comma else s


LOCAL = "--local" in sys.argv  # 重生後的頁：讀本機新版


def head_text(site, f):
    """本機有未推修改的頁（之前的試跑頁）以 HEAD 版為起點；--local 時讀本機檔（重生後處理）"""
    import subprocess
    if LOCAL:
        return f.read_bytes().decode("utf-8")
    rel = f"docs/_drugs/{f.name}"
    dirty = subprocess.run(["git", "diff", "--name-only", "HEAD", "--", rel], cwd=BASE / site, capture_output=True, text=True).stdout.strip()
    if dirty:
        return subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=BASE / site, capture_output=True).stdout.decode("utf-8")
    return f.read_bytes().decode("utf-8")


def transform(site, f, cls, pmap):
    raw = head_text(site, f)
    crlf = "\r\n" in raw[:500]
    t = raw.replace("\r\n", "\n")
    fm, sep, body = t[4:].partition("\n---")
    lang = ck.LANG.get(site, "en")
    b = amf.load_bundle(BASE / site, f.stem)
    d = b.get("drug") or {}
    preds = {ck.norm_name(p["disease_name"]): p for p in d.get("predicted_indications") or [] if p.get("disease_name")}
    kept = kf.kept_predictions(BASE / site, b)
    kept_p = [preds[ck.norm_name(k)] for k in kept if ck.norm_name(k) in preds]
    kept_sc = [p["txgnn_score"] for p in kept_p]

    def match(v):
        for p in kept_p:
            k = p["txgnn_score"]
            if abs(v - k) < 0.00005 or abs(round(k * 100, 2) - v * 100) < 0.005 or abs(round(k, 4) - v) < 0.00005:
                return p
        return None

    def conv_scores(text):
        """百分比 → 0.xxxx（只換對得上 kept 的分數）"""
        def rep(m):
            g = ck.norm_digits(m.group(1))
            v = float(g.replace(",", ".")) / 100
            p = match(v)
            if not p:
                return m.group(0)
            return fmt_score(p["txgnn_score"], "," in m.group(1) or "٫" in m.group(1), m.group(0))
        text = re.sub(r"(?<![\d.,])(\d{1,3}(?:[.,٫]\d+)?)\s?[%％٪]", rep, text)

        def rep_dec(m):
            v = float(ck.norm_digits(m.group(1)).replace(",", "."))
            if match(v):
                return m.group(0)
            near = [p for p in kept_p if abs(p["txgnn_score"] - v) < 0.0006]
            if len(near) == 1:
                return fmt_score(near[0]["txgnn_score"], "," in m.group(1), m.group(0))
            return m.group(0)
        return re.sub(r"(?<![\d.,≥>])(0[.,]9\d{1,3})(?![\d%])", rep_dec, text)

    lines = body.split("\n")
    tbs = ck.tables(body)
    # 表頭的分數欄位置（逐表）
    out, i, in_tab, hdr, si, li = [], 0, False, None, None, None
    for line in lines:
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not in_tab:
                in_tab, hdr = True, cells
                si = next((k for k, h in enumerate(cells) if ck.SCORE_HDR.search(h)), None)
                li = next((k for k, h in enumerate(cells) if ck.LEVEL_ROW.search(h)), None)
                out.append(line); continue
            if re.fullmatch(r"[\s|:\-]+", line):
                out.append(line); continue
            # 分數欄的列：分數對不上 kept → 刪列
            if si is not None and si < len(cells) and ck.score_tokens(cells[si]):
                vs = [v for v, _, _ in ck.score_tokens(cells[si])]
                if not any(match(v) for v in vs):
                    continue
                line = conv_scores(line)
                if li is not None and li < len(cells):
                    m = ck.LEVEL.search(cells[li])
                    p = next((match(v) for v in vs if match(v)), None)
                    if m and m.group(1) != "L5" and p and not rr.direct_evidence(p["disease_name"], ck.evidence_titles(p)):
                        line = re.sub(r"(?<![A-Za-z0-9])(\**)" + m.group(1) + r"(\**)(?![A-Za-z0-9])", r"\1L5\2", line, count=1)
                out.append(line); continue
            # 概覽表的分數列（第一欄是分數標籤）
            if len(cells) >= 2 and ck.SCORE_HDR.search(cells[0]) and ck.score_tokens(cells[1]):
                out.append(conv_scores(line)); continue
            out.append(line); continue
        in_tab = False
        # 本文：同句有分數字樣才換
        if ck.SCORE_CTX.search(line):
            line = conv_scores(line)
        out.append(line)
    body = "\n".join(out)

    # P4（凡有等級欄的表格；對應方式同 checker：病名或分數）
    bl = body.split("\n")
    hdr_lv = None
    for j, line in enumerate(bl):
        if not line.startswith("|"):
            hdr_lv = None; continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if hdr_lv is None:
            hdr_lv = next((k for k, h in enumerate(cells) if ck.LEVEL_ROW.search(h)), -1); continue
        if hdr_lv < 0 or re.fullmatch(r"[\s|:\-]+", line) or hdr_lv >= len(cells):
            continue
        m = ck.LEVEL.search(cells[hdr_lv])
        if not m or m.group(1) == "L5":
            continue
        p = next((preds.get(ck.norm_name(k)) for k in kept if any(rx.search(line) for rx in ck.name_regexes(site, k))), None)
        if p is None:
            vs = [v for v, _, _ in ck.score_tokens(line)]
            p = next((match(v) for v in vs if match(v)), None)
        if p and not rr.direct_evidence(p["disease_name"], ck.evidence_titles(p)):
            bl[j] = re.sub(r"(?<![A-Za-z0-9])(\**)" + m.group(1) + r"(\**)(?![A-Za-z0-9])", r"\1L5\2", line, count=1)
    body = "\n".join(bl)

    # 概覽表：P4（主預測等級）、狀態列、張數列
    tbs = ck.tables(body)
    ov = tbs[0][1] if tbs else []
    pred_row = next((r for r in ov if len(r) >= 2 and ck.PRED_ROW.search(r[0])), None)
    lvl_row = next((r for r in ov if len(r) >= 2 and ck.LEVEL_ROW.search(r[0]) and ck.LEVEL.search(r[1])), None)
    new_level = None
    if lvl_row:
        lv = ck.LEVEL.search(lvl_row[1]).group(1)
        new_level = lv
        p = None
        if pred_row:
            for k in kept:
                if any(rx.search(" ".join(pred_row[1:])) for rx in ck.name_regexes(site, k)):
                    p = preds.get(ck.norm_name(k)); break
            if p is None and kept_p:
                p = kept_p[0]
        if lv != "L5" and p and not rr.direct_evidence(p["disease_name"], ck.evidence_titles(p)):
            new_level = "L5"
            body = re.sub(r"^(\|\s*" + re.escape(lvl_row[0]) + r"\s*\|\s*\**)" + lv, r"\1L5", body, count=1, flags=re.M)

    def set_cell(body, label, value):
        return re.sub(r"^(\|\s*" + re.escape(label) + r"\s*\|)[^|\n]*(\|)", lambda m: f"{m.group(1)} {value} {m.group(2)}", body, count=1, flags=re.M)

    fc = ck.facts(site).get(f.stem) or ck.facts(site).get(f.stem.replace("-", "_")) or ck.facts(site).get(f.stem.replace("_", "-"))
    all_rows = [r for _, rows, _, _ in tbs for r in rows]
    st = ck.status_row(site, all_rows)
    if fc and st:
        ms, v, n, partial = fc.get("market_status"), fc.get("valid"), fc.get("total"), fc.get("partial")
        tl = mv2.T.get(lang) or mv2.T["en"]
        want = None
        if site == "KrTxGNN":
            want = ck.KR_UNKNOWN
        elif ms == "Marketed":
            want = ck.marketed_text(site, lang, v, n, partial)
        elif ms == "Approved, not marketed":
            want = ck.NOT_MKT.get(lang, ck.NOT_MKT["en"]).format(n=n)
        elif ms == "Cancelled only":
            want = ck.cancelled_text(site, lang, n)
        elif ms == "Not marketed":
            want = ck.not_reg_text(site, lang)
        if want and st[1] != want:
            body = set_cell(body, st[0], want)
        cr = ck.count_row(site, all_rows)
        if cr is None and site not in ("TwTxGNN", "KrTxGNN") and (n is not None or partial) and st is not None:
            # 已知用途頁等模板沒有張數列：依該站最常用的張數列標題補一列，放在狀態列下面；部分紀錄 total 為空 → 用已收錄張數
            want_c = (tl[3].format(n=n if n is not None else len(fc.get("licenses") or {})) if partial else tl[2].format(n=n, v=v or 0))
            body = re.sub(r"^(\|\s*" + re.escape(st[0]) + r"\s*\|[^\n]*\n)", lambda m: m.group(1) + f"| {count_label(site)} | {want_c} |\n",
                          body, count=1, flags=re.M)
        if cr and site not in ("TwTxGNN", "KrTxGNN") and n is not None:  # 所有狀態都依事實（非上市類：有效 0）
            want_c = (tl[3].format(n=n) if partial else tl[2].format(n=n, v=v or 0))
            if cr[1] != want_c:
                body = set_cell(body, cr[0], want_c)
        if site != "TwTxGNN":
            lic = {mv2.norm_id(k): s for k, s in (fc.get("licenses") or {}).items()}
            vw = mv2.VALID_WORD.get(lang, mv2.VALID_WORD["en"])
            bl = body.split("\n")
            for j, line in enumerate(bl):
                if line.startswith("|"):
                    cells = [c.strip() for c in line.strip().strip("|").split("|")]
                    if cells and lic.get(mv2.norm_id(cells[0])) == "valid" and mv2.TABLE_NEG.search(" ".join(cells[1:])):
                        for a, bb in vw:
                            line = line.replace(a, bb)
                        bl[j] = line
            body = "\n".join(bl)

    # P5：明確片語替換
    rules = fk.RULES.get(fk.LANG.get(site, "en"), []) + (fk.RULES["en"] if fk.LANG.get(site, "en") != "en" else [])
    bl = body.split("\n")
    for j, line in enumerate(bl):
        if ck.p5_hits(line, lang):
            for a, rep in rules:
                line = re.sub(a, rep, line, flags=re.I)
            bl[j] = line
    body = "\n".join(bl)

    # front matter 與標題列
    fm2 = re.sub(r"^predicted_indications:.*(?:\n[ \t]*-[ \t].*)*", "predicted_indications: " + json.dumps(kept, ensure_ascii=False), fm, count=1, flags=re.M)
    if "predicted_indications:" not in fm2:
        fm2 += "\npredicted_indications: " + json.dumps(kept, ensure_ascii=False)
    fm2 = re.sub(r"^indication_count: \d+$", f"indication_count: {len(kept)}", fm2, flags=re.M)
    body = HEAD_N.sub(lambda m: f"{m.group(1)}{len(kept)}{m.group(3)}", body, count=1)
    if new_level:
        old = (re.search(r"^evidence_level:\s*(\S+)", fm2, re.M) or [None, None])[1]
        if old != new_level:
            fm2 = re.sub(r"^evidence_level:\s*\S+", f"evidence_level: {new_level}", fm2, flags=re.M)
            if new_level in pmap:
                fm2 = re.sub(r"^parent:\s*.+$", f"parent: {pmap[new_level]}", fm2, count=1, flags=re.M)
            body = HEAD_L.sub(lambda m: f"{m.group(1)}{new_level}{m.group(3)}", body, count=1)
    t2 = "---" + fm2 + sep + body if t.startswith("---") else t
    t2 = t[:4] + fm2 + sep + body
    return t, t2, crlf


def main(argv):
    apply_ = "--apply" in argv
    pages = None
    if "--pages" in argv:
        pages = {tuple(x.split(":", 1)) for x in argv[argv.index("--pages") + 1].split(",")}
    sites = [a for a in argv if a.endswith("TxGNN")] or sorted({p[0] for p in pages} if pages else (p.name for p in BASE.glob("*TxGNN")))
    OUT.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(BASE / ".claude/audit_20261016/m2/classification.tsv", encoding="utf-8"), delimiter="\t"))
    skip = set()
    if os.environ.get("PROG_SKIP"):
        skip = {tuple(x.split(":", 1)) for x in Path(os.environ["PROG_SKIP"]).read_text().strip().split(",")}
    todo = [(r["site"], r["page"], r["class"]) for r in rows if r["site"] in sites and (r["site"], r["page"]) not in skip and
            ("--any" in argv or r["class"] == "keep" or (r["class"] == "regen" and r["regen_type"] == "only_removed")) and
            (pages is None or (r["site"], r["page"]) in pages)]
    diffs, to_regen, summ = [], [], Counter()
    pm_cache = {}
    for s, p, cls in todo:
        f = BASE / s / "docs/_drugs" / f"{p}.md"
        if s not in pm_cache:
            pm_cache[s] = parent_map(s)
        try:
            t, t2, crlf = transform(s, f, cls, pm_cache[s])
        except Exception as e:
            to_regen.append((s, p, "X", f"處理失敗：{str(e)[:80]}")); continue
        if t2 != t:
            diffs += difflib.unified_diff(t.splitlines(True), t2.splitlines(True), f"a/{s}/docs/_drugs/{p}.md", f"b/{s}/docs/_drugs/{p}.md", n=0)
            summ[(s, "changed")] += 1
        # 檢查（用改後的內容；P7 另由 FHIR／search-index 重產處理，這裡不算）
        tmp = OUT / "_tmp" / s / f"{p}.md"  # 各組各自的暫存
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(t2, encoding="utf-8")
        errs = [e for e in ck.check_page(s, tmp, cls, False) if e[0] != "P7"]
        if errs:
            to_regen.append((s, p, ",".join(sorted({e[0] for e in errs})), "; ".join(e[1] for e in errs)[:200]))
            summ[(s, "to_regen")] += 1
        if apply_ and t2 != t:  # 有殘錯也寫回（已修的格子不白做；殘錯頁另列 to_regen／第 2 層）
            f.write_bytes((t2.replace("\n", "\r\n") if crlf else t2).encode("utf-8"))
    (OUT / "changes.diff").write_text("".join(diffs), encoding="utf-8")
    with open(OUT / "to_regen.tsv", "w", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t"); w.writerow(["site", "page", "codes", "detail"]); w.writerows(to_regen)
    with open(OUT / "summary.tsv", "w", encoding="utf-8") as fh:
        fh.write("site\tpages\tchanged\tto_regen\n")
        for s in sites:
            n = sum(1 for x in todo if x[0] == s)
            fh.write(f"{s}\t{n}\t{summ[(s, 'changed')]}\t{summ[(s, 'to_regen')]}\n")
    print("頁數", len(todo), "有改", sum(v for (s, k), v in summ.items() if k == "changed"), "轉重生", len(to_regen),
          Counter(c for _, _, cs, _ in to_regen for c in cs.split(",")))


if __name__ == "__main__":
    main(sys.argv[1:])
