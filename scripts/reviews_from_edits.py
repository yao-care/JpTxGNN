#!/usr/bin/env python3
"""把藥物頁正文的刪改轉成查核紀錄（docs/_data/drug_reviews.json 的 action: correct）（2026-11-12 建，本站查核機制；
比照 UsTxGNN scripts/reviews_from_edits.py，本站的提交清單、切句規則、note 文字在 src/<套件>/regulatory/site.py）。

為什麼要有這支：
  2026-10-31～11-06 依新事實刪掉的矛盾子句，是直接刪的，頁面上看不出改過什麼，下次 scripts/sync_notes_to_docs.py 依 notes
  重寫整頁時也會被蓋回去。用戶 2026-11-12 決定：這些刪改轉成查核紀錄（頁面上顯示查核更正框與查核紀錄表），以後的刪句也一樣。
  兩種用法共用同一套抽取規則：
    --git：依 git 提交前後的頁面轉（歷史的刪改，site.COMMITS）
    --dirs：依改寫前後兩個目錄轉（刪句後呼叫）

抽取規則（只看正文）：
  - 去掉 front matter、查核框、受管區塊；表格、標題、kramdown 屬性列、HTML 註解不算正文。
  - 正文切成段落、段落再切成行與句子（site.SENT；中文、日文以句號類標點斷句，泰文以空白斷句），依序比對；
    有變的連續句子＝一筆（claim＝原句、replacement＝新句）。
  - 整句被刪：claim 往前（沒有前句就往後）多帶一句，replacement＝那一句；整段被刪：claim＝那一段、replacement 空、anchor＝前後段。
  - 同一處前後改過多次，依時間合併成一筆（claim＝最早的原句、replacement＝最後的版本）。
理由：scripts/license_sentence_fixes.json 的人工清單有這句 → finding＝該筆 reason；note（頁面上顯示，本站語言）依被刪文字分類
  （台灣模板殘留、註銷／查無許可、張數、其他；分類用本站 checker 的 tw_left 與 X_LOCAL 當地語言規則），附快照裡目前的張數。
狀態：頁面上找得到 replacement（或 anchor）→ 顯示框；找不到而頁面之後被 AI 重產過（site.REGEN_COMMITS）→ resolved_by_regeneration；
  其他找不到的不寫入，列出交人工判斷。

用法（repo 根目錄）：
  python3 scripts/reviews_from_edits.py --git [--write]
  python3 scripts/reviews_from_edits.py --dirs 前目錄 後目錄 --date YYYY-MM-DD --commit 說明 [--write]
沒有 --write 只列出結果，不寫檔。寫入後跑 python3 scripts/apply_drug_reviews.py。
"""
from __future__ import annotations

import difflib
import gzip
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "_data" / "drug_reviews.json"
FIXES = ROOT / "scripts" / "license_sentence_fixes.json"
sys.path.insert(0, str(ROOT / "src"))
from jptxgnn.regulatory import site as C  # noqa: E402
SNAP = ROOT / "snapshots" / f"{C.CODE}_licenses.json.gz"
COMMITS, REGEN_COMMITS, SOURCES, SENT = C.COMMITS, C.REGEN_COMMITS, C.SOURCES, C.SENT
BLOCK_RE = re.compile(r"<!-- (review:begin \S+|brand-names:start) -->.*?<!-- (review:end \S+|brand-names:end) -->", re.S)


# ---------- 抽取 ----------
def body(t):
    t = t.replace("\r\n", "\n")
    if t.startswith("---"):
        e = t.find("\n---", 3)
        t = t[e + 4:] if e >= 0 else t
    return re.sub(r"<!-- licenses:(?:begin|end) -->", "", BLOCK_RE.sub("", t))


def is_prose(p):
    s = p.strip()
    return bool(s) and not s.startswith("|") and not s.startswith("{:") and not s.startswith("<!--") and not s.startswith("#") \
        and not re.fullmatch(r"[-*_]{3,}", s)  # 水平線不是正文


def paras(t):
    """正文段落：空行分段；段落裡的標題行（# 開頭，例：清單後直接接「## Disclaimer」）也斷開，標題本身不算正文"""
    out = []
    for blk in re.split(r"\n[ \t]*\n", t):
        cur = []
        for ln in blk.split("\n"):
            if ln.startswith("#"):
                if cur:
                    out.append("\n".join(cur))
                cur = []
                continue
            cur.append(ln)
        if cur:
            out.append("\n".join(cur))
    return [p.strip("\n") for p in out if is_prose(p)]


def spans(p):
    out, i = [], 0
    for m in SENT.finditer(p):
        if m.start() > i:
            out.append((i, m.start()))
        i = m.end()
    if i < len(p):
        out.append((i, len(p)))
    return out


def in_para(a, b):
    """段落 a→b 有變的句子群 → [[(claim, replacement), …]]：每群由小到大的候選（往前後多帶相同的句子），
    claim 是 a 的子字串、replacement 是 b 的子字串；定稿時取第一個在頁面上唯一的候選。
    邊界一律落在兩版相同句子的起訖點：沒多帶句子的一側，邊界是相鄰相同句子的結尾（前側）或開頭（後側），
    被刪句子前後的分隔字元（空白、換行）算在差異裡；這樣套用結果跟實際刪改後一字不差（2026-11-12 SE lisdexamfetamine：
    整句刪除往後多帶一句時，舊算法把換行吃掉、留下前面的空白）。"""
    sa, sb = spans(a), spans(b)
    ta, tb = [a[x:y] for x, y in sa], [b[x:y] for x, y in sb]
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        cands = []
        for k1 in range(0, 4):
            for k2 in range(0, 4):
                x1, x2, y1, y2 = i1 - k1, i2 + k2, j1 - k1, j2 + k2
                if x1 < 0 or y1 < 0 or x2 > len(ta) or y2 > len(tb):
                    continue
                A0 = sa[x1][0] if k1 else (sa[i1 - 1][1] if i1 > 0 else 0)
                B0 = sb[y1][0] if k1 else (sb[j1 - 1][1] if j1 > 0 else 0)
                A1 = sa[x2 - 1][1] if k2 else (sa[i2][0] if i2 < len(sa) else len(a))
                B1 = sb[y2 - 1][1] if k2 else (sb[j2][0] if j2 < len(sb) else len(b))
                c, r = a[A0:A1], b[B0:B1]
                if not r.strip() or c == r:
                    continue
                cands.append((k1 + k2, (c, r)))
                if A0 == 0 and A1 == len(a) and B0 == 0 and B1 == len(b):  # 整段：前後帶換行，跟段落中間的同一句區分
                    cands.append((k1 + k2 + 0.5, (f"\n{a}\n", f"\n{b}\n")))
        if not cands:
            continue  # 段落只剩這句又整句刪：由段落層級處理
        out.append([c for _, c in sorted(cands, key=lambda x: x[0])])
    return out


def changes(before, after):
    """兩版頁面 → [(claim, replacement, anchor)]"""
    pa, pb = paras(body(before)), paras(body(after))
    out = []
    def deleted(i, j1):
        """整段刪掉：錨點候選＝新版前後各三段（定稿時取第一個在頁面上唯一的）"""
        near = [pb[j] for j in (j1 - 1, j1, j1 - 2, j1 + 1, j1 - 3, j1 + 2) if 0 <= j < len(pb)]
        out.append([(pa[i], "", x) for x in near] or [(pa[i], "", "")])

    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, pa, pb, autojunk=False).get_opcodes():
        if op == "equal" or op == "insert":
            continue  # 只有新增（沒有刪改）不是更正
        # 逐段配對：原段落依序配新段落裡最相似的一段（相似度 ≥0.5），配上的做段內比對，配不上的是整段刪除。
        # 不把多段接成一筆：段落之間常隔著表格，接起來的字串在頁面上不相連，套用時找不到（2026-11-12 atomoxetine 等 4 頁）
        j = j1
        for i in range(i1, i2):
            best, bj = 0.0, None
            for k in range(j, j2):
                sm = difflib.SequenceMatcher(None, pa[i], pb[k], autojunk=False)
                r = sm.ratio()
                kept = sum(m.size for m in sm.get_matching_blocks())
                if pb[k].strip() and len(pb[k].strip()) >= 2 and kept >= 0.95 * len(pb[k]):
                    r = max(r, 0.99)  # 新段落的字幾乎都依序留在原段落裡（只刪不改：刪掉大半只剩一句；各語言適用，不靠空白分詞）
                if r > best:
                    best, bj = r, k
            if bj is not None and best >= 0.5:
                for cands in in_para(pa[i], pb[bj]):
                    out.append([(c, r, "") for c, r in cands])
                j = bj + 1
            else:
                deleted(i, j)
    return out


# ---------- 理由 ----------
def load_fixes():
    if not FIXES.exists():
        return {}
    return json.loads(FIXES.read_text(encoding="utf-8"))


def snap_facts():
    if not SNAP.exists():
        return {}
    return {k: v.get("facts") or {} for k, v in json.loads(gzip.open(SNAP).read().decode("utf-8"))["drugs"].items()}


def removed_text(claim, repl):
    sm = difflib.SequenceMatcher(None, claim, repl, autojunk=False)
    return " ".join(claim[i1:i2] for op, i1, i2, j1, j2 in sm.get_opcodes() if op in ("delete", "replace"))


def _ck():
    import importlib.util
    p = ROOT / "tools" / "txgnn" / ".claude" / "check_drug_page.py"
    s = importlib.util.spec_from_file_location(f"{C.SITE}_ck", p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


CK = _ck()
CK_LANG = CK.LANG.get(C.SITE, "en")


def _hit(rx, s):
    if rx is None:
        return False
    if isinstance(rx, (list, tuple)):
        return any(_hit(x, s) for x in rx)
    return bool(rx.search(s))


def classify(rm, reason=""):
    """被刪文字的類別：tw（台灣模板殘留）、cancel（說註銷／查無有效許可）、count（張數）、generic。
    人工清單的 reason（中文）優先；其次用本站 checker 的 tw_left 與 X_LOCAL 當地語言規則，再用 site.CLASS_EXTRA。"""
    if reason:
        if re.search(r"台灣|TFDA|模板殘留", reason):
            return "tw"
        if re.search(r"註銷|撤銷|查無|未上市|沒有有效|全部無效|過期", reason):
            return "cancel"
        if re.search(r"張數|總數|有效張|件數|筆數", reason):
            return "count"
    if CK.tw_left(C.SITE, rm):
        return "tw"
    R = CK.X_LOCAL.get(CK_LANG) or {}
    if any(_hit(R.get(k), rm) for k in ("canc", "noreg", "none_cancel")) or _hit(C.CLASS_EXTRA.get("cancel"), rm):
        return "cancel"
    if any(_hit(R.get(k), rm) for k in ("count", "total", "ccount", "valid")) or _hit(C.CLASS_EXTRA.get("count"), rm):
        return "count"
    return "generic"


def note_for(kind, date, fc):
    fig = C.FIGURES.format(total=fc["total"], valid=fc.get("valid") or 0) if fc and fc.get("total") is not None else ""
    return C.NOTES[kind].format(date=date) + (fig if kind in ("cancel", "count", "generic") else "")  # 其他類別（tw 等）不附張數


def manual_reason(fixes, stem, claim):
    for it in fixes.get(stem) or []:
        s = (it.get("sentence") or "").strip()
        cuts = it.get("cut") or []
        cuts = [x.strip(" ,;") for x in (cuts if isinstance(cuts, list) else [cuts])]
        if (s and s in claim) or any(len(c) > 6 and c in claim for c in cuts):
            return it.get("reason") or ""
    return ""


# ---------- 合併與狀態 ----------
def compose(recs, cands, meta):
    """同一處前後改過多次 → 合併成一筆（claim＝最早原句、replacement＝最新版）。回傳是否已併入既有紀錄。
    合併用最小的候選比對；合併後候選只剩合併結果（再往外帶句子的候選要依新頁面重算，這裡不做）"""
    claim, repl, anchor = cands[0]
    for r in recs:
        old = r["cands"][0][1]
        if old and claim and claim in old:
            new = [(c0, old.replace(claim, repl, 1), a0 or anchor) for c0, r0, a0 in r["cands"] if r0 == old] or \
                  [(r["cands"][0][0], old.replace(claim, repl, 1), anchor)]
        elif old and claim and old in claim:
            new = [(c.replace(old, r["cands"][0][0], 1), rp, a) for c, rp, a in cands if old in c]
        else:
            continue
        r["cands"] = new
        r["_meta"].append(meta)
        return True
    return False


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout


def show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def commit_date(h):
    return git("log", "-1", "--format=%cs", h).strip()


def regen_pages():
    out = set()
    for h in REGEN_COMMITS:
        out |= {Path(f).name for f in git("diff", "--name-only", f"{h}^", h, "--", "docs/_drugs").split()}
    return out


def build(pairs):
    """pairs：[(檔名, 前文, 後文, 日期, 提交)]，依時間排序 → {檔名: [紀錄草稿]}"""
    by = {}
    for fname, before, after, date, commit in pairs:
        recs = by.setdefault(fname, [])
        for cands in changes(before, after):
            meta = {"date": date, "commit": commit}
            if not compose(recs, cands, meta):
                recs.append({"cands": cands, "_meta": [meta]})
    return by


def pick(cands, cur_body):
    """候選裡第一個能在目前頁面上唯一定位的：replacement（整段刪除時是 anchor）在頁面上剛好出現一次；
    或頁面上又是原句（claim 剛好出現一次，套用時會再更正）。都不行回 None"""
    for c, r, a in cands:
        loc = r or a
        if c == r or not c.strip():
            continue
        if loc and cur_body.count(loc) == 1:
            return c, r, a, "located"
    for c, r, a in cands:
        if c.strip() and c != r and cur_body.count(c) == 1 and (r or a):
            return c, r, a, "claim_on_page"
    return None


def finalize(by, current, regen, fixes, facts, existing_ids):
    """草稿 → 正式紀錄；回傳 (紀錄, 無法定位的草稿)"""
    out, lost = [], []
    for fname, recs in sorted(by.items()):
        stem = fname[:-3]
        cur = current(fname)
        if cur is None or 'http-equiv="refresh"' in cur[:3000]:
            continue
        cur_body = body(cur)
        n = 0
        for r in recs:
            got = pick(r["cands"], cur_body)
            if got is None:
                c0, r0, a0 = r["cands"][0]
                if c0 == r0 or not c0.strip():
                    continue
                if fname in regen:
                    got = (c0, r0, a0, "regen")
                else:
                    lost.append((fname, {"claim": c0, "replacement": r0}))
                    continue
            r = dict(r, claim=got[0], replacement=got[1], anchor=got[2], how=got[3])
            n += 1
            first, last = r["_meta"][0], r["_meta"][-1]
            rm = removed_text(r["claim"], r["replacement"])
            reason = manual_reason(fixes, stem, r["claim"])
            ck_kind = next((getattr(C, "COMMIT_KIND", {}).get(m["commit"]) for m in r["_meta"] if getattr(C, "COMMIT_KIND", {}).get(m["commit"])), None)
            kind = ck_kind or classify(rm, reason)  # site.COMMIT_KIND：整筆提交的刪改類別固定（例：移除程式編造的許可證號）
            rec = {
                "id": f"{C.CODE}-lic-{first['date'].replace('-', '')}-{stem}-{n}",
                "drug": stem, "file": fname, "action": "correct",
                "claim": r["claim"], "replacement": r["replacement"],
                "note": note_for(kind, last["date"], facts.get(stem)),
                "finding": reason or f"依成分重建許可證後，正文跟新事實矛盾的子句由刪句工具刪除（分類：{kind}）",
                "sources": [dict(s, accessed=last["date"]) for s in SOURCES],
                "checked": last["date"],
                "summary": C.SUMMARY.format(text=" ".join((rm.strip(C.STRIP_CHARS) or r["claim"]).split())[:140]),
                "method": ("2026-11-12 由 git 提交前後的頁面轉入查核紀錄（scripts/reviews_from_edits.py）；原本的刪改：" +
                           "、".join(f"{m['commit']}（{m['date']}）" for m in r["_meta"])),
            }
            if not r["replacement"]:
                rec["anchor"] = r["anchor"]
            if r["how"] == "regen":
                rec["status"] = "resolved_by_regeneration"
                rec["resolved_on"] = "2026-11-12"
                rec["resolved_note"] = C.REGEN_NOTE
            if rec["id"] in existing_ids:
                continue
            out.append(rec)
    return out, lost


def write(new):
    doc = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {"_doc": DOC, "schema_version": 1, "records": []}
    have = {r["id"] for r in doc["records"]}
    doc["records"] += [r for r in new if r["id"] not in have]
    DATA.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


DOC = ("藥物頁人工查核紀錄（單一真實來源；2026-11-12 建，核心流程比照 TwTxGNN docs/_data/drug_reviews.json，欄位相同）。"
       "每筆＝一次查核：drug／file／claim（頁面原句）／replacement（更正後）／note（頁面上顯示的說明，本站語言）／finding（內部查證結論）／"
       "sources（網址＋查閱日）／checked（查核日）／action（correct 更正｜annotate 加註｜rereview 待重審｜section 附來源段落｜"
       "rereview_result 重審結果｜header_level｜description_level）。由 scripts/apply_drug_reviews.py 套到 docs/_drugs/*.md；"
       "改寫頁面的程式結尾都會重套，scripts/check_seo_docs.py 擋未套用的紀錄。原則：基本事實照本站主管機關資料更正；"
       "模型預測原文不刪不改寫，只加註；證據等級與決策只在重審結果為降級、升級或撤回時更新。"
       "2026-10-31～11-06 依新事實直接刪掉的矛盾子句，2026-11-12 由 scripts/reviews_from_edits.py 依 git 前後版本轉入"
       "（id 以 <站碼>-lic- 開頭）；報告在 11 月經 AI 重產、原句已不在頁面的標 status=resolved_by_regeneration。"
       "同 id 重發時前版存進 history（retired、reason），不覆蓋丟棄。")


def main(argv):
    fixes, facts = load_fixes(), snap_facts()
    existing = {r["id"] for r in json.loads(DATA.read_text(encoding="utf-8"))["records"]} if DATA.exists() else set()
    if "--git" in argv:
        pairs = []
        for h in COMMITS:
            d = commit_date(h)
            for f in git("diff", "--name-only", f"{h}^", h, "--", "docs/_drugs").split():
                b, a = show(f"{h}^", f), show(h, f)
                if b and a:
                    pairs.append((Path(f).name, b, a, d, h))
        by = build(pairs)
        current = lambda fn: (ROOT / "docs/_drugs" / fn).read_text(encoding="utf-8") if (ROOT / "docs/_drugs" / fn).exists() else None
        recs, lost = finalize(by, current, regen_pages(), fixes, facts, existing)
    elif "--dirs" in argv:
        i = argv.index("--dirs")
        bd, ad = Path(argv[i + 1]), Path(argv[i + 2])
        d = argv[argv.index("--date") + 1]
        c = argv[argv.index("--commit") + 1] if "--commit" in argv else "license-rebuild"
        pairs = [(f.name, f.read_text(encoding="utf-8"), (ad / f.name).read_text(encoding="utf-8"), d, c)
                 for f in sorted(bd.glob("*.md")) if (ad / f.name).exists()]
        by = build(pairs)
        current = lambda fn: (ad / fn).read_text(encoding="utf-8") if (ad / fn).exists() else None
        recs, lost = finalize(by, current, set(), fixes, facts, existing)
    else:
        sys.exit(__doc__)
    act = sum(1 for r in recs if not r.get("status"))
    print(f"紀錄 {len(recs)} 筆（顯示框 {act}、報告重產後已無此錯誤 {len(recs) - act}），{len({r['file'] for r in recs})} 頁；"
          f"無法定位 {len(lost)} 筆")
    for fn, r in lost[:30]:
        print(f"  ? {fn}：{r['claim'][:90]!r} → {r['replacement'][:60]!r}")
    if "--write" in argv:
        write(recs)
        print(f"已寫入 {DATA.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
