#!/usr/bin/env python3
"""把人工查核紀錄（docs/_data/drug_reviews.json）套用到 docs/_drugs/*.md（2026-11-12 建）。

比照 TwTxGNN／UsTxGNN scripts/apply_drug_reviews.py 的核心流程（用戶 2026-11-12 決定：30 站各有自己的查核機制，核心流程一樣）。
頁面上的查核框與查核紀錄表用本站語言（字樣在 src/<套件>/regulatory/site.py），依據是本站主管機關的資料。

為什麼要有這支：
  藥物頁會被產線與排程改寫（scripts/sync_notes_to_docs.py 整頁覆寫；每週許可證排程重排許可證表、狀態列、張數列）。
  人工或規則查核後的更正、加註、待重審標記，如果只改在頁面上，下次改寫就會被蓋掉，也看不出改過什麼。
  所以查核結果一律記在 docs/_data/drug_reviews.json，再由這支套到頁面；改寫頁面的程式結尾都會呼叫它，
  scripts/check_seo_docs.py 也會檢查每筆紀錄都還套在頁面上。

紀錄的 action（欄位與 Tw 相同）：
  correct   基本事實照官方資料更正：頁面上的 claim 換成 replacement，並在該段落後加「查核更正」說明
            （原句、依據、日期）。頁面已經是 replacement（例如 2026-11 已刪掉矛盾子句）時只加說明。
  annotate  原文不動，在 claim（或 anchor）所在段落後加「查核加註」。
  rereview  在 anchor 所在段落後加「待重審」標記（預測本身與證據等級不改）。
  section   在 before 指定的標題前插入一整段 markdown（附來源的段落）。
  rereview_result  重審結論：resolves 指回一筆 rereview；同一位置改顯示「重審結果」框（verdict：maintain｜downgrade｜
            upgrade｜withdraw、原等級→新等級、理由）。table_updates（[{label, claim, replacement}]）把頁面上該適應症的等級／
            決策儲存格換成重審後的值（降級、升級、撤回時才用；升級要附可查證的 PMID／NCT）。
  header_level  頁首等級重算的留存紀錄（original_level／new_level／original_parent／new_parent）：只列在查核紀錄表。
            頁首規則見 src/<套件>/regulatory/page_format.py 與 site.py 的 HEADER_RULE。
  description_level  front matter description 的等級跟著頁首：只列在查核紀錄表（page_format.sync_description_level）。
status：superseded（錨點落在程式產生的區塊上）、resolved_by_regeneration（報告重生後已無此錯誤）、resolved_by_program
（程式改版後已無此錯誤）、withdrawn（查核本身有誤或重複）：紀錄保留、頁面不顯示框，查核紀錄表註明。
同 id 重發時前版存進 history（retired、reason），不覆蓋丟棄。
每頁另在免責聲明標題（site.DISCLAIMER_RE）前產生查核紀錄表（site.LOG_HEAD），列出該頁全部紀錄。

用法：
  python3 scripts/apply_drug_reviews.py           # 套用（可重複執行，結果相同）
  python3 scripts/apply_drug_reviews.py --check   # 只檢查，有未套用的紀錄就 exit 1
  python3 scripts/apply_drug_reviews.py --touch   # 套用，並把有改到的藥物頁 last_modified_at 設成今天
                                                  # （查核框是看得見的變動，JSON-LD dateModified 讀它；同 fix_table_spacing.py --touch）
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from jptxgnn.regulatory import page_format as F, site as C  # noqa: E402
DOCS = ROOT / "docs"
DATA = DOCS / "_data" / "drug_reviews.json"
DRUGS = DOCS / "_drugs"

LABEL = C.LABEL
ACTION_EN = C.ACTION
VERDICT_EN = C.VERDICT
RESOLVED = "resolved_by_regeneration"
WITHDRAWN = "withdrawn"
RESOLVED_PROGRAM = "resolved_by_program"
HIDDEN = ("superseded", RESOLVED, WITHDRAWN, RESOLVED_PROGRAM)
LOG_HEAD = C.LOG_HEAD
DISCLAIMER_RE = C.DISCLAIMER_RE


def load():
    if not DATA.exists():
        return []
    return json.loads(DATA.read_text(encoding="utf-8"))["records"]


def begin(rid):
    return f"<!-- review:begin {rid} -->"


def end(rid):
    return f"<!-- review:end {rid} -->"


def strip_block(text, rid):
    pat = re.compile(r"\n*" + re.escape(begin(rid)) + r".*?" + re.escape(end(rid)) + r"\n*", re.S)
    return pat.sub("\n\n", text)


def sources_md(rec):
    """同一筆紀錄裡重複的來源網址只顯示一次。"""
    seen, out = set(), []
    for s in rec["sources"]:
        if s["url"] in seen:
            continue
        seen.add(s["url"])
        out.append(f"[{s['title']}]({s['url']})")
    return C.LIST_SEP.join(out)


BLOCK_RE = re.compile(r"<!-- review:begin (\S+) -->.*?<!-- review:end \1 -->", re.S)


def find_outside(text, needle):
    """找 needle 在頁面原文中的位置，跳過已插入的查核框（框裡會引用原句，不能當定位點）。"""
    if not needle:
        return -1
    spans = [m.span() for m in BLOCK_RE.finditer(text)]
    start = 0
    while True:
        i = text.find(needle, start)
        if i < 0:
            return -1
        hit = next((s for s in spans if s[0] <= i < s[1]), None)
        if not hit:
            return i
        start = hit[1]


def display(s):
    """原句顯示成一行：表格列改成「cell / cell」；多行（清單項目、多段）用「 / 」接起來，
    避免引言框裡的 | 被當成表格、換行讓框斷掉或在表格列裡斷行（2026-11-12）。"""
    s = s.strip()
    if s.startswith("|"):
        s = C.JOIN.join(c.strip() for c in s.strip("|").split("|"))
    s = re.sub(r"\s*\n\s*(?:[-*+]\s+|\d+\.\s+)?", C.JOIN, s)
    s = re.sub(r"^(?:[-*+]\s+|\d+\.\s+)", "", s)
    return s.replace("|", "&#124;")


def level_text(lv):
    if isinstance(lv, str):
        return lv
    groups = {}
    for k, v in lv.items():
        groups.setdefault(v, []).append(k)
    return C.LIST_SEP.join(f"{C.ITEM_SEP.join(ks)} {v}" for v, ks in groups.items())


def level_change(rec):
    o, n = rec["original_level"], level_text(rec["new_level"])
    return C.LEVEL_SAME.format(o=o) if n == o else C.LEVEL_CHANGE.format(o=o, n=n)


def _sentence(s):
    s = s.strip()
    return s if not s or s[-1] in C.SENT_END else s + C.FULL_STOP


def note_md(rec):
    label = LABEL[rec["action"]]
    head = C.BOX_HEAD.format(label=label, date=rec["checked"])
    if rec["action"] == "correct":
        body = C.ORIG_STATED.format(claim=display(rec["claim"])) + C.SPACE + _sentence(rec["note"])
    elif rec["action"] == "rereview_result":
        body = f"**{VERDICT_EN[rec['verdict']]}**{C.PAREN.format(level_change(rec))}{C.FULL_STOP}{C.SPACE}{_sentence(rec['note'])}"
        ups = rec.get("table_updates") or []
        if ups:
            body += C.SPACE + C.TABLE_UPDATED.format(labels=C.ITEM_SEP.join(u["label"] for u in ups))
    else:
        body = _sentence(rec["note"])
    tail = ""
    if rec["action"] == "rereview_result" and rec.get("decision_note"):
        tail = f"\n>\n> {C.DECISION}{rec['decision_note']}"
    return f"{begin(rec['id'])}\n\n{head}{body}{C.SPACE}{C.SOURCE_WORD}{sources_md(rec)}{C.FULL_STOP}{tail}\n\n{end(rec['id'])}"


def block_end(text, pos):
    """pos 所在段落／表格／清單的結尾：下一個空行，或下一個標題行之前（清單後直接接「## Disclaimer」、中間沒空行時，
    框不能落到標題下面；2026-11-12 oxazepam）。"""
    m = re.compile(r"\n[ \t]*\n|\n(?=#{1,6} )").search(text, pos)
    return m.start() if m else len(text)


def apply_record(text, rec, problems):
    rid = rec["id"]
    text = strip_block(text, rid)
    act = rec["action"]
    if act == "section":
        m = re.search(rec["before"], text, re.M)
        if not m:
            problems.append(f"{rid}：找不到插入位置 {rec['before']}")
            return text
        block = f"{begin(rid)}\n\n{rec['markdown'].strip()}\n\n{end(rid)}\n\n"
        return text[:m.start()] + block + text[m.start():]
    if act == "correct":
        olds = [rec["claim"]] + [h["replacement"] for h in rec.get("history") or []
                                 if h.get("replacement") and h["replacement"] != rec["replacement"]
                                 and not h.get("reanchored") and h["replacement"] not in rec["replacement"]]
        for old in olds:
            j = find_outside(text, old)
            if j >= 0:
                text = text[:j] + rec["replacement"] + text[j + len(old):]
                break
        anchor = rec.get("anchor") or rec["replacement"]
    else:
        anchor = rec.get("anchor") or rec["claim"]
    i = find_outside(text, anchor)
    if i < 0:
        problems.append(f"{rid}：頁面上找不到 {'replacement／anchor' if act == 'correct' else 'anchor'}「{anchor[:50]}…」（頁面可能被改寫，需人工重查）")
        return text
    e = block_end(text, i)
    nxt = re.compile(r"\s*<!-- review:begin (\S+) -->.*?<!-- review:end \1 -->", re.S)
    while True:
        m = nxt.match(text, e)
        if not m or m.group(1) == "log" or re.search(r"^#{1,6} ", m.group(0), re.M):
            break
        e = m.end()
    return text[:e] + "\n\n" + note_md(rec) + text[e:]


def log_md(recs):
    rows = [C.LOG_COLS, "|------|------|------|------|"]
    resolved = {r["resolves"] for r in recs if r["action"] == "rereview_result"}
    for r in recs:
        item = display(r.get("summary") or r["claim"])
        act = ACTION_EN[r["action"]]
        if r["action"] == "rereview" and r["id"] in resolved:
            act = C.ACT_REREVIEWED
        if r["action"] == "header_level":
            act = C.ACT_HEADER.format(o=r["original_level"], n=r["new_level"])
            if r.get("trigger") == "withdraw":
                act = C.ACT_HEADER_WD.format(o=r["original_level"], n=r["new_level"])
                if r["new_level"] == F.NA:
                    act += C.ACT_NA_LIST.format(title=F.parent_titles().get(F.NA, "N/A"))
        if r["action"] == "rereview_result":
            act = C.ACT_RESULT.format(verdict=VERDICT_EN[r["verdict"]], change=level_change(r))
            for u in r.get("table_updates") or []:
                act += C.ACT_TABLE.format(label=u["label"], a=display(u["claim"]), b=display(u["replacement"]))
        if r["action"] == "description_level":
            act = C.ACT_DESC.format(o=r["original_level"], n=F.description_level_text(r["new_level"]))
        if r.get("history"):
            act += C.ACT_REVISED.format(d=r["history"][-1]["retired"])
        if r.get("status") == "superseded":
            act = C.ST_SUPERSEDED.format(act=act)
        elif r.get("status") == RESOLVED:
            act = C.ST_REGEN.format(d=r["resolved_on"], note=r["resolved_note"], act=act)
        elif r.get("status") == RESOLVED_PROGRAM:
            act = C.ST_PROGRAM.format(d=r["resolved_on"], note=r["resolved_note"], act=act)
        elif r.get("status") == WITHDRAWN:
            act = C.ST_WITHDRAWN.format(d=r["withdrawn_on"], note=r["withdrawn_note"], act=act)
        rows.append(f"| {r['checked']} | {item} | {act} | {sources_md(r)} |")
    intro = C.INTRO
    if all(r["action"] in ("header_level", "description_level") for r in recs):
        intro = C.INTRO_HEADER
    elif any(r["action"] == "rereview_result" and r.get("table_updates") for r in recs):
        intro = C.INTRO_RERE
    return f"{begin('log')}\n\n{LOG_HEAD}\n\n{intro}\n\n" + "\n".join(rows) + f"\n\n{end('log')}\n\n"


def apply_text(text, fname):
    """記憶體內套用某頁的紀錄（產線寫頁前用）。回傳 (新內容, 問題清單)。"""
    recs = [r for r in load() if r["file"] == fname]
    if not recs:
        return text, []
    local = []
    for _ in range(4):
        local = []
        nxt = render_page(text, recs, local)
        if nxt == text:
            break
        text = nxt
    return text, local


def apply_page(path, recs, problems):
    orig = path.read_text(encoding="utf-8")
    text, local = orig, []
    for _ in range(4):
        local = []
        nxt = render_page(text, recs, local)
        if nxt == text:
            break
        text = nxt
    problems.extend(local)
    return text, text != orig


def apply_result(text, rereview, res, problems):
    for u in res.get("table_updates") or []:
        j = find_outside(text, u["claim"])
        if j >= 0:
            text = text[:j] + u["replacement"] + text[j + len(u["claim"]):]
        elif find_outside(text, u["replacement"]) < 0:
            problems.append(f"{res['id']}：頁面上找不到要更新的「{u['claim'][:40]}…」（頁面可能被改寫，需人工重查）")
    rec = dict(res, anchor=res.get("anchor") or rereview.get("anchor") or rereview["claim"])
    return apply_record(text, rec, problems)


def validate(recs):
    errs, by_id, seen = [], {r["id"]: r for r in recs}, {}
    if len(by_id) != len(recs):
        errs.append("drug_reviews.json 有重複的 id")
    for r in recs:
        for k in ("id", "file", "action", "checked", "sources"):
            if not r.get(k):
                errs.append(f"{r.get('id')}：缺 {k}")
        if r.get("action") not in ACTION_EN:
            errs.append(f"{r.get('id')}：action 必須是 {sorted(ACTION_EN)}")
        if r.get("action") == "correct" and not (r.get("replacement") or r.get("anchor")):
            errs.append(f"{r['id']}：correct 要有 replacement（或整段刪除時的 anchor）")
        if r["action"] != "rereview_result":
            continue
        tgt = by_id.get(r.get("resolves"))
        if not tgt or tgt["action"] != "rereview" or tgt["file"] != r["file"]:
            errs.append(f"{r['id']}：resolves 指向不存在或不是同頁 rereview 的紀錄 {r.get('resolves')}")
        if r.get("resolves") in seen:
            errs.append(f"{r['id']}：{r['resolves']} 已有重審結果 {seen[r['resolves']]}")
        seen[r.get("resolves")] = r["id"]
        if r.get("verdict") not in VERDICT_EN:
            errs.append(f"{r['id']}：verdict 必須是 {sorted(VERDICT_EN)}")
        o = [int(x) for x in re.findall(r"L([1-5])", r.get("original_level") or "")]
        n = [int(x) for x in re.findall(r"L([1-5])", level_text(r.get("new_level") or ""))]
        if r.get("verdict") == "downgrade" and not (o and n and min(n) > min(o)):
            errs.append(f"{r['id']}：verdict=downgrade 但新等級沒有低於原等級")
        if r.get("verdict") == "upgrade":
            if not (o and n and min(n) < min(o)):
                errs.append(f"{r['id']}：verdict=upgrade 但新等級沒有高於原等級")
            if not r.get("table_updates") or not re.search(r"PMID|NCT", json.dumps(r.get("sources"), ensure_ascii=False)):
                errs.append(f"{r['id']}：verdict=upgrade 需要 table_updates 與可查證的 PMID／NCT 來源")
    return errs


def undo_retired(text, recs):
    """前版做過、現行版本不再做的頁面改寫，先還原成原句（同 Tw）。"""
    for r in recs:
        if r["action"] == "correct" and find_outside(text, r["claim"]) < 0 and find_outside(text, r.get("replacement")) < 0:
            for h in reversed(r.get("history") or []):
                if h.get("action") == "correct" and h.get("replacement") and find_outside(text, h["replacement"]) >= 0:
                    if (h["claim"] != r["claim"] or h["replacement"] != r.get("replacement")) and find_outside(text, h["claim"]) < 0:
                        j = find_outside(text, h["replacement"])
                        text = text[:j] + h["claim"] + text[j + len(h["replacement"]):]
                    break
        for h in r.get("history") or []:
            if h.get("action") == "correct" and r["action"] != "correct" and h.get("replacement"):
                j = find_outside(text, h["replacement"])
                if j >= 0 and find_outside(text, h["claim"]) < 0:
                    text = text[:j] + h["claim"] + text[j + len(h["replacement"]):]
            keep = {u["replacement"] for u in r.get("table_updates") or []}
            for u in h.get("table_updates") or []:
                if u["replacement"] in keep:
                    continue
                j = find_outside(text, u["replacement"])
                if j >= 0:
                    text = text[:j] + u["claim"] + text[j + len(u["replacement"]):]
    return text


def render_page(text, recs, problems):
    text = re.sub(r"\n*<!-- review:begin (\S+) -->.*?<!-- review:end \1 -->\n*", "\n\n", text, flags=re.S)
    text = F.fix_table_spacing(text)
    text = undo_retired(text, recs)
    results = {r["resolves"]: r for r in recs if r["action"] == "rereview_result" and r.get("status") != RESOLVED}
    retired = {r["resolves"] for r in recs if r["action"] == "rereview_result" and r.get("status") == RESOLVED}
    for r in recs:
        if r.get("status") in HIDDEN:
            continue
        if r["action"] in ("rereview_result", "header_level", "description_level"):
            continue
        if r["action"] == "rereview" and r["id"] in retired:
            continue
        if r["action"] == "rereview" and r["id"] in results:
            text = apply_result(text, r, results[r["id"]], problems)
            continue
        text = apply_record(text, r, problems)
    text = F.sync_header_level(text, recs[0]["file"][:-3] if recs else None)
    if any(r["action"] == "description_level" and r.get("status") not in HIDDEN for r in recs):
        text = F.sync_description_level(text)
    m = DISCLAIMER_RE.search(text)
    log = log_md(recs)
    text = text[:m.start()] + log + text[m.start():] if m else text.rstrip() + "\n\n" + log
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def touch(text, today=None):
    import datetime as _dt
    today = today or _dt.date.today().isoformat()
    return re.sub(r"^(last_modified_at:\s*)\d{4}-\d{2}-\d{2}", rf"\g<1>{today}", text, count=1, flags=re.M)


def run(check=False, only=None, touch_date=False):
    recs = load()
    by_file = {}
    for r in recs:
        by_file.setdefault(r["file"], []).append(r)
    problems, changed = validate(recs), []
    for fname, rs in sorted(by_file.items()):
        if only and fname not in only:
            continue
        path = DRUGS / fname
        if not path.exists():
            problems.append(f"{fname}：藥物頁不存在")
            continue
        head = path.read_text(encoding="utf-8", errors="replace")[:3000]
        if 'http-equiv="refresh"' in head or re.search(r"^layout:\s*id_redirect", head, re.M):
            continue  # 已改成轉址頁：紀錄保留為歷史，不再套用
        new, diff = apply_page(path, rs, problems)
        if diff:
            changed.append(fname)
            if not check:
                path.write_text(touch(new) if touch_date else new, encoding="utf-8")
    return problems, changed


def check_errors():
    """給 check_seo_docs.py 用：回傳錯誤字串清單（空＝全部紀錄都已套用在頁面上）。"""
    if not DATA.exists():
        return []
    problems, changed = run(check=True)
    errs = [f"藥物頁查核紀錄：{p}" for p in problems]
    errs += [f"藥物頁查核紀錄未套用（或被改寫蓋掉）：{f}，請跑 python3 scripts/apply_drug_reviews.py" for f in changed]
    return errs


if __name__ == "__main__":
    check = "--check" in sys.argv
    only = {a if a.endswith(".md") else a + ".md" for a in sys.argv[1:] if not a.startswith("--")} or None
    problems, changed = run(check=check, only=only, touch_date="--touch" in sys.argv)
    for p in problems:
        print("  ✗", p)
    if check:
        print(f"查核紀錄：{'✗' if (problems or changed) else '✓'} 待套用 {len(changed)} 頁、問題 {len(problems)} 項")
        sys.exit(1 if (problems or changed) else 0)
    print(f"查核紀錄：已套用 {len(changed)} 頁、問題 {len(problems)} 項")
    sys.exit(1 if problems else 0)
