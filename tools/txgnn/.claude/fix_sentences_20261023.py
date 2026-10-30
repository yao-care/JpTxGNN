"""第 2 層：只改命中的句子（2026-10-23，pm 定案；做法同 A9 散文市場句，模型 Sonnet）。
程式化處理（第 1 層）之後 checker 仍報錯的頁，只把命中的那幾行送模型改寫或刪除，其他行凍結：
  - P5：把 KG 寫成預測／分數來源的行
  - 寫到已排除／已移除預測的行（含帶分數的舊預測、H1、description）
  - 本文分數對不上 kept 或寫成百分比的行
事實只給：該藥 kept 預測（英文、當地名、4 位分數）、已排除病名、語言。模型回傳 JSON {行號: 新行 或 "DELETE"}。
驗收（不過就不寫）：回傳行號只能是送出的行；新行不得含 kept 以外的分數、不得再命中 P5；改完整頁 checker（P7 除外）要 0，否則列入第 3 層（整頁重生）。
頁面與 notes 同步改（notes 裡找得到完全相同的行才改）。
用法（母目錄）：python3 .claude/fix_sentences_20261023.py [--dry] --pages site:page,...
輸出 .claude/audit_20261016/sentences/：results.tsv（site, page, sent, result, remaining）、<站>.diff
"""
import os as _os, sys as _sys
if __name__ == "__main__" and _os.environ.get("ALLOW_AI_REGEN") != "1" and "--selftest" not in _sys.argv:
    _sys.exit("已停用（2026-10-28）：藥物頁事實改由 .claude/factlayer_20261028.py 程式產生，不再用 AI 整頁重生。"
              "確定要用 AI 重產時，先經 pm 同意並試跑 20 頁，再以 ALLOW_AI_REGEN=1 執行。")
import csv
import difflib
import importlib.util
import json
import re
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / ".claude/audit_20261016/sentences"


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


ck = _load("ck", BASE / ".claude/check_drug_page.py")
kf, amf = ck.kf, ck.amf
LANGNAME = {"es": "Spanish", "pt": "Brazilian Portuguese", "de": "German", "da": "Danish", "fi": "Finnish", "fr": "French",
            "zh": "Traditional Chinese", "it": "Italian", "ja": "Japanese", "ko": "Korean", "ms": "Malay", "nl": "Dutch",
            "no": "Norwegian Bokmål", "ar": "Arabic", "sv": "Swedish", "th": "Thai", "en": "English", "en-us": "American English"}
SYSTEM = """You fix specific lines of a {lang} drug report page for pharmacists. Rewrite ONLY the lines given, one by one, \
in {lang}, keeping Markdown formatting. Do not add facts.

Facts for this drug:
- Current predictions of the TxGNN model (deep learning), with exact scores (write scores exactly like this, 4 decimals, never as %):
{kept}
- These diseases are NOT predictions on this page (they are known uses or were removed from the prediction list): {excluded}
- Main prediction (must be the one named in the page title line and description): {main}
- Market facts in this country: {market}

Rules for each line:
1. The knowledge graph is never the source of a prediction or score. Predictions and scores come from the TxGNN model \
(deep learning). If a line says a score/prediction comes from, reflects or rests on the knowledge graph (or its proximity, \
network, paths, artefacts), rewrite it to say the score comes from the TxGNN model (deep learning) and may reflect \
similarities the model learned between related diseases, not biological evidence.
2. A line that presents one of the non-prediction diseases above as a prediction or gives it a score: remove that part. \
If nothing meaningful remains, return "DELETE".
3. Scores: only the scores listed above, written with 4 decimals (e.g. 0.9977 or 0,9977 if the line uses decimal commas). \
A threshold such as "≥ 0.99" may stay.
4. Market status: never say all licences are cancelled / none valid if the facts say some are valid, and never say the drug \
is marketed if the facts say it is not. Use the facts above.
5. A title line ("# ..."), description, or the overview-table row for the new predicted indication that names another disease \
(or a broader/narrower disease, a ranking note, or a second disease) must name exactly the main prediction instead, in {lang}, \
with nothing else in that table cell.
6. Keep everything else in the line unchanged (names, numbers, references, links).

Answer with JSON only: {{"<line id>": "<new line>" or "DELETE", ...}} for every line id given."""


LIMIT_RX = re.compile(r"usage limit|rate.?limit|\b429\b|overloaded|limit reached|hit your limit|limit.{0,40}resets", re.I)  # 2026-10-23 pm：撞額度要退避重試，不算失敗


def call(system, text):
    cmd = ["claude", "-p", "--output-format", "text", "--tools", "", "--strict-mcp-config", "--mcp-config",
           '{"mcpServers":{}}', "--model", "sonnet", "--system-prompt", system]
    attempt = 0
    while attempt < 5:
        r = subprocess.run(cmd, input=text, capture_output=True, text=True, timeout=1200)
        if r.returncode == 0 and r.stdout.strip() and not LIMIT_RX.search(r.stdout[:300]):
            o = r.stdout.strip()
            m = re.search(r"\{.*\}", o, re.S)
            return m.group(0) if m else o
        if LIMIT_RX.search((r.stderr or "") + (r.stdout or "")[:300]):
            print("額度退避 300s", file=sys.stderr, flush=True); time.sleep(300); continue
        time.sleep(30 * (attempt + 1)); attempt += 1
    raise RuntimeError("claude 呼叫失敗：" + (r.stderr or "")[-200:])


def bad_lines(site, t, kept, excluded, kept_sc, cls="keep", removed=(), facts=None, why=None):
    """要送模型的行號（從 0 起算，以整份檔案為準）；why 給 dict 時填每行命中原因（回饋重試用）"""
    why = {} if why is None else why
    lines = t.split("\n")
    lang = ck.LANG.get(site, "en")
    ex_rx = [rx for x in excluded for rx in ck.name_regexes(site, x)]
    keep_rx = [rx for k in kept for rx in ck.name_regexes(site, k)]
    in_fm = lines[0].strip() == "---"
    out, section = [], ""
    for i, line in enumerate(lines):
        if i > 0 and in_fm and line.strip() == "---":
            in_fm = False; continue
        if in_fm and not line.startswith("description:"):
            continue
        if line.startswith("|") and not ck.score_tokens(line):
            continue  # 表格只處理帶分數的列（原適應症、已知用途表、許可證表不動）
        if line.lstrip().startswith("#"):
            section = line
        p5 = ck.p5_hits(line, lang, section)
        hit = bool(p5)
        if hit:
            why[i] = ("P5", "The knowledge graph must not appear as the source/basis of a prediction or score. Remove or rewrite: " + " | ".join(p5))
        # 已排除病名多半是已知用途：只有和分數／預測字樣同行（當成預測在講）才改；已知用途頁不套
        if not hit and cls != "known_use" and any(rx.search(line) for rx in ex_rx) and ck.SCORE_OR_PRED.search(line) \
                and not any(rx.search(line) for rx in keep_rx):
            hit = True
            why[i] = ("P3", "Must not present these non-predictions as predictions: " + ", ".join(x for x in excluded if any(rx.search(line) for rx in ck.name_regexes(site, x))))
        if not hit and ck.SCORE_CTX.search(line):
            toks = [x for x in ck.score_tokens(line) if x[0] >= 0.5]
            if any(p or not ck.matches_kept(v, kept_sc) for v, p, _ in toks):
                hit = True
                why[i] = ("P2", "Scores in this line must be exactly one of the listed scores, 4 decimals, never %.")
        # M3：正文市場說法與事實矛盾
        if not hit and facts and site != "KrTxGNN" and not line.startswith(("|", "#")):
            v = facts.get("valid") or 0
            if (v > 0 and ck.ALL_CANCEL.search(line)) or (facts.get("market_status") in ("Cancelled only", "Not marketed") and
                    (ck.marketed_word(lang) in line or ck.MKT_CLAIM_EXTRA.search(line)) and not ck.mv2.NEG.search(line)):
                hit = True
                why[i] = ("M3", "Market statement contradicts the market facts above; state them correctly or drop the claim.")
        # C6：因門檻／刷新移除（非已知用途）的預測仍被當預測
        if not hit and removed and cls != "known_use" and (ck.score_tokens(line) or ck.SCORE_PRED_STRICT.search(line)):
            if any(rx.search(line) for x in removed for rx in ck.name_regexes(site, x)) and not any(rx.search(line) for rx in keep_rx):
                hit = True
                why[i] = ("P3", "Delete every mention of these removed predictions: " + ", ".join(x for x in removed if any(rx.search(line) for rx in ck.name_regexes(site, x))))
        # 主預測：H1（報告標題）與 description 要提到 kept[0]
        if not hit and kept and cls not in ("known_use", "no_pred_keep", "no_pred_noindex") and \
                (line.startswith("# ") or line.startswith("description:")) and ":" in line or "：" in line[:200]:
            if (line.startswith("# ") or line.startswith("description:")) and not any(rx.search(line) for rx in ck.name_regexes(site, kept[0])):
                hit = True
                why[i] = ("P3", f"This line must name the main prediction {kept[0]}.")
        # pm 指定（main_by_score 全量核對）：概覽表「預測新適應症」列要送
        if not hit and FORCE and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and ck.PRED_ROW.search(cells[0]):
                hit = True
                why[i] = ("P3", f"The cell must name exactly the main prediction {kept[0] if kept else ''} and nothing else.")
        if hit:
            out.append(i)
    return out


FORCE = False


LIST_PREFIX = re.compile(r"^(\s*(?:[-*+]|\d+[.)])\s+)?(.*)$", re.S)
DISCLAIMER = re.compile(r"disclaimer|免責|免责|avertissement|haftungsausschluss|descargo|aviso legal|isenção|esclusione di responsabilità|"
                        r"avvertenz|ansvarsfraskrivelse|vastuuvapaus|ansvarsfriskrivning|vrijwaring|면책|penafian|إخلاء|ข้อจำกัดความรับผิดชอบ", re.I)
CONNECTIVE = re.compile(r"(However|Moreover|Furthermore|Therefore|Thus|In addition|Additionally|Nevertheless|Also|"
                        r"此外|然而|因此|另外|不過|同時|しかし|また|さらに|したがって|그러나|또한|따라서|"
                        r"Sin embargo|Además|Por lo tanto|No entanto|Além disso|Portanto|Cependant|De plus|En outre|Par conséquent|"
                        r"Jedoch|Außerdem|Darüber hinaus|Daher|Tuttavia|Inoltre|Pertanto|Echter|Bovendien|Daarom|"
                        r"Dog|Desuden|Derfor|Dock|Dessutom|Därför|Kuitenkin|Lisäksi|Siksi|Selain itu|Oleh itu|Walau bagaimanapun|"
                        r"ومع ذلك|بالإضافة إلى ذلك|لذلك)\b[,，、]?", re.I)
ABBR = {"e.g.", "i.e.", "vs.", "al.", "dr.", "z.b.", "bzw.", "p.ex.", "cf.", "approx.", "ca.", "nr.", "no.", "fig.", "s.", "u.a.", "d.h.", "z.", "ex."}
OPEN_Q, CLOSE_Q = "“«「『（([", "”»」』）)]"


def aligned(new):
    """刪掉的行以空行占位，行號不變"""
    return "\n".join(x if x is not None else "" for x in new)


def split_sentences(text):
    """切句（句後空白歸前一句，''.join 可還原）。不切：小數點、縮寫、網址／連結裡的點、括號內、引號內。"""
    out, start, depth, inq, k, n = [], 0, 0, False, 0, len(text)
    while k < n:
        ch = text[k]
        if ch in OPEN_Q:
            depth += 1
        elif ch in CLOSE_Q:
            depth = max(0, depth - 1)
        elif ch == '"':
            inq = not inq
        end = False
        if not depth and not inq:
            nxt = text[k + 1] if k + 1 < n else ""
            end = ch in "。！？؟।" or (ch in ".!?" and (nxt == "" or nxt.isspace()))
            if end and ch == ".":
                words = text[start:k + 1].split()
                tok = words[-1].lstrip("*_(\"'“«").lower() if words else ""
                if tok in ABBR or re.fullmatch(r"[a-z]\.", tok):  # 網址裡的點後面不接空白，本來就不切
                    end = False
            # 引號／括號內以句號結尾，收尾符號後接空白 → 句子在收尾符號後結束
            if ch in '"”»」』' and k > 0 and text[k - 1] in ".!?。！？" and (nxt == "" or nxt.isspace()):
                end = True
        k += 1
        if end:
            while k < n and text[k].isspace():
                k += 1
            out.append(text[start:k]); start = k
    if start < n:
        out.append(text[start:])
    return out


def deletable(site, new, i, fm_end):
    line = new[i] or ""
    if site == "ThTxGNN" or i < fm_end or line.lstrip().startswith(("#", "|", ">")):
        return False
    s = line.strip().strip("*").strip()
    if s.endswith(("?", "？", "؟")) and len(split_sentences(s)) == 1:  # FAQ 問句
        return False
    # 導言行（冒號結尾、下一個非空行是條列）一律不刪：條列可能是禁忌／安全資訊（pm 2026-10-23）
    if line.rstrip().rstrip("*").rstrip().endswith((":", "：")):
        nxt = next((x for x in new[i + 1:] if x is not None and x.strip()), "")
        if LIST_PREFIX.match(nxt).group(1):
            return False
    for j in range(i - 1, fm_end - 1, -1):
        h = new[j] or ""
        if h.startswith("#"):
            return not DISCLAIMER.search(h)
    return True


def selftest():
    cases = [
        ("Score 0.99 is high. Next one.", ["Score 0.99 is high. ", "Next one."]),
        ("Le score est de 99,5 % ici. Ensuite.", ["Le score est de 99,5 % ici. ", "Ensuite."]),
        ("Use e.g. aspirin daily. Stop.", ["Use e.g. aspirin daily. ", "Stop."]),
        ("Smith et al. reported it. Done.", ["Smith et al. reported it. ", "Done."]),
        ("Dies gilt z.B. hier. Ende.", ["Dies gilt z.B. hier. ", "Ende."]),
        ("See [the trial](https://clinicaltrials.gov/ct2/show/NCT01.x) now. End.", ["See [the trial](https://clinicaltrials.gov/ct2/show/NCT01.x) now. ", "End."]),
        ("Visit https://example.org/a.b. Then go.", ["Visit https://example.org/a.b. ", "Then go."]),
        ("It works (see Fig. 1. and more.) well. End.", ["It works (see Fig. 1. and more.) well. ", "End."]),
        ('He said "It is fine. Really." Then left.', ['He said "It is fine. Really." ', "Then left."]),
        ("此藥有效。此外，也安全。", ["此藥有效。", "此外，也安全。"]),
        ("A vs. B compared. End.", ["A vs. B compared. ", "End."]),
    ]
    bad = 0
    for s, want in cases:
        got = split_sentences(s)
        if got != want or "".join(got) != s:
            bad += 1; print("✗", repr(s), got)
    c = [CONNECTIVE.match("However, it is.") is not None, CONNECTIVE.match("此外，也安全。") is not None, CONNECTIVE.match("Aspirin is.") is None]
    bad += c.count(False)
    print(f"selftest {len(cases) + 3 - bad}/{len(cases) + 3} 通過")
    return bad == 0


def run(site, page, dry):
    f = BASE / site / "docs/_drugs" / f"{page}.md"
    raw = f.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw[:500]
    t = raw.replace("\r\n", "\n")
    b = amf.load_bundle(BASE / site, page)
    d = b["drug"]
    preds = {ck.norm_name(p["disease_name"]): p for p in d.get("predicted_indications") or []}
    kept = kf.kept_predictions(BASE / site, b)
    top = [p["disease_name"] for p in d.get("predicted_indications") or [] if (p.get("txgnn_score") or 0) >= kf.SCORE_MIN][:10]
    excluded = [x for x in top if ck.norm_name(x) not in {ck.norm_name(k) for k in kept}]
    kept_sc = [preds[ck.norm_name(k)]["txgnn_score"] for k in kept]
    global FORCE
    fm_list = BASE / ".claude/audit_20261016/layers23/force_main.txt"
    FORCE = fm_list.exists() and f"{site}:{page}" in fm_list.read_text().split()
    cls = ck.classification().get((site, page), "keep")
    fc = ck.facts(site).get(page) or ck.facts(site).get(page.replace("-", "_")) or {}
    bk = BASE / ".claude/cache/bundle_backup_20261022" / site / page / "drug_bundle.json"
    old = [p.get("disease_name") for p in json.loads(bk.read_text(encoding="utf-8"))["drug"].get("predicted_indications") or []] if bk.exists() else []
    cand = sorted({x for x in old + [p.get("disease_name") for p in d.get("predicted_indications") or []] if x and ck.norm_name(x) not in {ck.norm_name(k) for k in kept}})
    removed = [x for x in cand if x in set(kf.filter_predictions(BASE / site, d.get("drugbank_id") or "", (d.get("inn") or d.get("name") or "").strip(), cand, b))] if cand else []
    idx = bad_lines(site, t, kept, excluded, kept_sc, cls, removed, fc)
    if not idx:
        return 0, "no_lines", t, t
    lines = t.split("\n")
    # 2026-10-23 pm：命中行超過正文一半、或 P3 命中 3 處以上 → 逐句改不乾淨，直接留給第 3 層整頁重生
    fm_end = lines.index("---", 1) + 1 if lines[0].strip() == "---" and "---" in lines[1:] else 0
    body = [x for x in lines[fm_end:] if x.strip()]
    if len(idx) > len(body) / 2 or sum(e[0] == "P3" for e in ck.check_page(site, f, cls, False)) >= 3:
        return len(idx), "to_l3", t, t
    lang = LANGNAME.get(ck.LANG.get(site, "en"), "English")
    kept_txt = "\n".join(f"  - {k}" + (f" (local name: {sorted(ck.local_names(site).get(ck.norm_name(k), ()), key=len)[0]})" if ck.local_names(site).get(ck.norm_name(k)) else "") + f": {preds[ck.norm_name(k)]['txgnn_score']:.4f}"
                         for k in kept) or "  (none — this page has no new predictions)"
    mk = fc.get("market_status")
    market = (f"marketed, {fc.get('valid')} valid licence(s) of {fc.get('total')}" if mk == "Marketed" else
              f"not marketed ({mk})" if mk else "unknown")
    sysmsg = SYSTEM.format(lang=lang, kept=kept_txt, excluded=", ".join(sorted(set(excluded) | set(removed))) or "(none)",
                           main=kept[0] if kept else "(none — no new prediction)", market=market)
    new = list(lines)
    why = {}
    bad_lines(site, t, kept, excluded, kept_sc, cls, removed, fc, why)
    cur = list(idx)
    # 2026-10-23 pm：送一次＋帶回饋重試最多 2 次（只送仍命中的行，附上命中規則與詞）
    for rnd in range(3):
        if rnd == 0:
            ask = json.dumps({str(i): new[i] for i in cur}, ensure_ascii=False, indent=1)
        else:
            ask = json.dumps({str(i): {"line": new[i], "problem": why[i][1]} for i in cur}, ensure_ascii=False, indent=1) + \
                "\n\nThese lines still break the rules. Fix each one so the named problem is gone (keep the rest); " \
                "if that is impossible, return \"DELETE\". Answer with the same JSON format: {\"<line id>\": \"<new line>\"}."
        try:
            ans = json.loads(call(sysmsg, ask))
        except ValueError:
            ans = {}
        for k, v in (ans.items() if isinstance(ans, dict) else ()):
            try:
                i = int(k)
            except ValueError:
                continue
            if i not in cur:
                continue
            if isinstance(v, dict):
                v = v.get("line", "")
            new[i] = None if v == "DELETE" else str(v)
        why = {}
        cur = bad_lines(site, aligned(new), kept, excluded, kept_sc, cls, removed, fc, why)
        if not cur:
            break
    # 重試後仍命中：正文句由程式刪除（保底）；標題、表格、引言、FAQ 問句、免責聲明、front matter、泰文 → 第 3 層
    deleted, to_l3 = [], []
    for i in cur:
        if not deletable(site, new, i, fm_end):
            to_l3.append(i); continue
        rule = why.get(i, ("?", ""))[0]
        m = LIST_PREFIX.match(new[i])
        prefix, text = m.group(1) or "", m.group(2)
        parts = split_sentences(text)
        hit_s = lambda s: bool(bad_lines(site, s, kept, excluded, kept_sc, cls, removed, fc))
        keep_p = [s for s in parts if not hit_s(s)]
        gone = [s for s in parts if hit_s(s)]
        if keep_p and hit_s(prefix + "".join(keep_p)):  # 命中靠整段上下文 → 整段刪
            gone, keep_p = parts, []
        if keep_p and all(CONNECTIVE.match(s.strip()) for s in keep_p):  # 只剩連接詞開頭的句子
            gone, keep_p = parts, []
        deleted += [(rule, s.strip()) for s in gone]
        new[i] = (prefix + "".join(keep_p).rstrip()) if keep_p else None
        if new[i] is None and 0 < i < len(new) - 1 and (new[i - 1] or "").strip() == "" and (new[i + 1] or "") .strip() == "":
            new[i + 1] = None  # 整段移除後不留兩個空行
    t2 = "\n".join(x for x in new if x is not None)
    notes_miss = False
    if not dry:
        f.write_bytes((t2.replace("\n", "\r\n") if crlf else t2).encode("utf-8"))
        nb = BASE / site / "data/notes" / page / "drug_pharmacist_notes.md"
        nt = nb.read_text(encoding="utf-8") if nb.exists() else None
        for i, old in enumerate(lines):
            if new[i] == old or not old.strip():
                continue
            if nt is not None and nt.count(old) == 1:
                nt = nt.replace(old + "\n", "") if new[i] is None else nt.replace(old, new[i])
            else:
                notes_miss = True
        if nt is not None:
            nb.write_text(nt, encoding="utf-8")
        if deleted:
            with open(OUT / "deleted_sentences.tsv", "a", encoding="utf-8") as fh:
                for rule, s in deleted:
                    fh.write("\t".join((site, page, rule, s.replace("\t", " "), "notes_miss" if notes_miss else "")) + "\n")
    res = "to_l3" if to_l3 else ("ok_notes_miss" if notes_miss else "ok")
    return len(idx), res, t, t2


def main(argv):
    if "--selftest" in argv:
        sys.exit(0 if selftest() else 1)
    dry = "--dry" in argv
    pages = [tuple(x.split(":", 1)) for x in argv[argv.index("--pages") + 1].split(",")]
    OUT.mkdir(parents=True, exist_ok=True)
    cl = ck.classification()
    diffs, rows = {}, []
    for s, p in pages:
        try:
            n, res, t, t2 = run(s, p, dry)
        except Exception as e:
            n, res, t, t2 = 0, f"error: {str(e)[:100]}", "", ""
        rem = ""
        if not dry and res.startswith("ok"):
            errs = [e for e in ck.check_page(s, BASE / s / "docs/_drugs" / f"{p}.md", cl.get((s, p), "keep"), False) if e[0] != "P7"]
            rem = ",".join(sorted({e[0] for e in errs}))
        if t2 != t:
            diffs.setdefault(s, []).extend(difflib.unified_diff(t.splitlines(True), t2.splitlines(True), f"a/{s}/{p}.md", f"b/{s}/{p}.md", n=0))
        rows.append((s, p, n, res, rem))
        print(f"{s}:{p} 送 {n} 行 {res} 殘 {rem}", flush=True)
    for s, d in diffs.items():
        (OUT / f"{s}.diff").write_text("".join(d), encoding="utf-8")
    with open(OUT / "results.tsv", "a", encoding="utf-8") as fh:
        for r in rows:
            fh.write("\t".join(map(str, r)) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
