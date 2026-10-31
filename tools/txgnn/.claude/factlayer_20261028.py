"""藥物頁事實層由程式產生（2026-10-28，pm 根治方案；取代「補 prompt 後用 AI 重產」）。不呼叫任何模型。

事實只從一個地方來，checker（check_drug_page.py）讀的是同一份：
  kept 預測與分數（證據包＋known_use_filter）、license_facts（市場狀態、張數）、本地許可證的適應症原文（bundle tfda.records）。
每頁處理順序：
  1. apply_programmatic_20261023.transform：front matter kept／indication_count、狀態列、張數列、許可證表註銷字樣、P4 降級、百分比→0.xxxx、P5 片語
  2. 概覽表：原適應症＝許可證適應症原文（沒有就填該語言「本地資料未記載」）、預測新適應症＝kept[0]、預測分數＝kept[0] 的 4 位小數（一律用點）
  3. 報告 H1 ＝「藥名：kept[0]」
  4. 違規句由程式整句刪除，不重寫（KG、百分比、不屬於 kept 的分數、與事實矛盾的市場說法、已移除預測）；整行都違規就刪整行
  5. description 依概覽表重算（drug_meta_description 的多語模板）
已知用途頁、無預測頁（沒有 kept）不處理。CRLF 保留。預設乾跑（寫 diff），--apply 才寫檔。
用法（母目錄）：python3 .claude/factlayer_20261028.py [--apply] [--any-scope] [--pages site:page,...] [站 ...]
  各站 scripts/sync_notes_to_docs.py 寫完頁面後會自動以 --apply --any-scope --pages 呼叫本支（2026-10-28），
  notes 裡的舊事實不會再蓋回頁面。
輸出 .claude/audit_20261016/factlayer/：changes.diff、results.tsv（每頁改前／改後 checker 規則）
"""
import csv
import difflib
import importlib.util
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get("FL_OUT", BASE / ".claude/audit_20261016/factlayer"))


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


ap = _load("ap", BASE / ".claude/apply_programmatic_20261023.py")
ck = ap.ck
fs = _load("fs", BASE / ".claude/fix_sentences_20261023.py")
dm = _load("dm", BASE / ".claude/drug_meta_description.py")

NOT_RECORDED = {
    "en": "Not recorded in the local data", "es": "No consta en los datos locales", "pt": "Não consta nos dados locais",
    "de": "In den lokalen Daten nicht erfasst", "da": "Ikke registreret i de lokale data", "fi": "Ei kirjattu paikallisiin tietoihin",
    "fr": "Non renseignée dans les données locales", "it": "Non riportata nei dati locali", "ja": "日本の承認情報に適応症の記載なし",
    "ko": "국내 허가 자료에 적응증 기재 없음", "ms": "Tidak direkodkan dalam data tempatan", "nl": "Niet vermeld in de lokale gegevens",
    "no": "Ikke registrert i de lokale dataene", "sv": "Inte angiven i de lokala uppgifterna", "th": "ไม่มีบันทึกในข้อมูลท้องถิ่น",
    "zh": "本地許可證資料未記載適應症", "ar": "غير مسجل في البيانات المحلية",
}
KG_PRED_ROW = re.compile(r"\bKG\b[^|]*(predict|ramalan)|(predict|ramalan)[^|]*\bKG\b", re.I)
SCORE_LABEL = re.compile(r"score|pontua|puntaje|punteggio|poäng|pistemäärä|pisteet|scor|分數|分数|スコア|점수|skor|คะแนน|درجة|Vorhersagewert|voorspellingsscore", re.I)


def lang_of(site):
    code = dm.site_lang(BASE / site)
    return code if code in NOT_RECORDED else code.split("-")[0] if code.split("-")[0] in NOT_RECORDED else "en"


COMBO = re.compile(r";|\+|＋| and |、", re.I)


def orig_value(site, b, page=None):
    """原適應症＝有效、單一成分本地許可證的適應症原文（已註銷證、複方證不算：查核紀錄 camphor／nystatin 的教訓）；
    沒有就填「本地資料未記載」。Tw 的原適應症格屬人工查核範圍（check_original_indications、drug_reviews），回傳 None＝不動。"""
    if site == "TwTxGNN":
        return None
    fc = (ck.facts(site).get(page) or ck.facts(site).get((page or "").replace("-", "_")) or {}) if page else {}
    lic = fc.get("licenses") or {}
    texts = []
    for r in (b.get("tfda") or {}).get("records") or []:
        lid = r.get("license_id") or r.get("license_number") or ""
        if lic and lic.get(lid) not in (None, "valid"):
            continue
        if COMBO.search(r.get("ingredients") or ""):
            continue
        x = re.sub(r"\s+", " ", (r.get("indication") or "").replace("|", "/")).strip()
        if x and x not in texts:
            texts.append(x)
    return "; ".join(texts)[:300] if texts else NOT_RECORDED[lang_of(site)]


def pred_display(site, k0, cell):
    """kept[0] 的顯示名：現有格子若已是 kept[0]（當地名）就沿用當地名，後面附英文名；否則只寫英文名。"""
    rxs = ck.name_regexes(site, k0)
    loc = re.sub(r"\s*[（(][^()（）]*[)）]\s*$", "", (cell or "").strip()).strip(" *")
    eng = k0[:1].upper() + k0[1:]
    simple = loc and len(loc) <= 80 and not re.search(r"[:;。；：]|\brank\b|\d", loc, re.I)
    if simple and any(rx.search(loc) for rx in rxs) and loc.lower() != k0.lower():
        return f"{loc} ({k0})"
    return eng


def set_row(lines, idx, value):
    cells = lines[idx].strip().strip("|").split("|")
    lines[idx] = f"| {cells[0].strip()} | {value} |"


def overview_rows(lines, body_start):
    """第一個表格（快速總覽）的行號"""
    i = body_start
    while i < len(lines) and not (lines[i].startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|\s*$", lines[i + 1])):
        i += 1
    out = []
    j = i + 2
    while j < len(lines) and lines[j].startswith("|"):
        out.append(j); j += 1
    return out


def strip_sentences(site, text, kept, excluded, kept_sc, cls, removed, facts):
    """違規句整句刪除（不重寫）。只動正文行；標題、表格、引言、免責聲明不動（交給 checker 報）。"""
    lines = text.split("\n")
    fm_end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0) + 1
    bad = fs.bad_lines(site, text, kept, excluded, kept_sc, cls, removed, facts)
    new = list(lines)
    for i in bad:
        if i < fm_end or not fs.deletable(site, new, i, fm_end):
            continue
        line = new[i]
        m = fs.LIST_PREFIX.match(line)
        prefix, rest = m.group(1) or "", m.group(2)
        keep = []
        for s in fs.split_sentences(rest):
            probe = "\n".join(lines[:i] + [prefix + s] + lines[i + 1:])
            if i in fs.bad_lines(site, probe, kept, excluded, kept_sc, cls, removed, facts):
                continue
            keep.append(s)
        out = "".join(keep).strip()
        new[i] = (prefix + out) if out else None
    return "\n".join(x for x in new if x is not None)


SNIP = re.compile(r"[：:]\s?(.+)$")


def checker_snippets(site, path, cls):
    """checker 的錯誤訊息裡帶的違規句／違規格（規則只在 checker 一處）"""
    out = []
    for code, msg in ck.check_page(site, path, cls, False):
        if code not in ("P2", "P3", "P5", "P6", "M3"):
            continue
        if code == "P5":
            s = msg
        elif "「" in msg and code in ("P2",) and "分數「" in msg:
            s = msg.split("「", 1)[1].split("」", 1)[0]
        else:
            m = SNIP.search(msg)
            if not m:
                continue
            s = m.group(1)
        s = fs.LIST_PREFIX.match(s.strip()).group(2).strip().strip("*").strip()  # 條列項目的「- **」不算進比對片段
        if len(s) >= 6:
            out.append(s[:40])
    return out


def excluded_score_rows(site, text, cls, excluded, kept, ov):
    """checker 報「已排除 X 出現在預測列」：非快速總覽表、帶分數、寫的是已排除預測的表格列 → 行號"""
    keep_rx = [rx for k in kept for rx in ck.name_regexes(site, k)]
    out = set()
    for i, line in enumerate(text.split("\n")):
        if i in ov or not line.startswith("|") or not ck.score_tokens(line):
            continue
        if any(rx.search(line) for x in excluded for rx in ck.name_regexes(site, x)) and not any(rx.search(line) for rx in keep_rx):
            out.add(i)
    return out


def strip_by_checker(site, text, cls, fname, ov_lines):
    """checker 報的違規句整句刪、違規的表格列整列刪（快速總覽表不動，那裡由程式填）；最多 3 輪"""
    tmp = OUT / "_strip" / site / fname
    tmp.parent.mkdir(parents=True, exist_ok=True)
    ov = set(ov_lines)
    for _ in range(3):
        tmp.write_text(text, encoding="utf-8")
        snips = checker_snippets(site, tmp, cls)
        if not snips:
            break
        norm = lambda x: ck.norm_digits(x)
        lines = text.split("\n")
        fm_end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0) + 1
        changed = False
        for i in range(fm_end, len(lines)):
            line = lines[i]
            if line is None or not line.strip() or line.lstrip().startswith("#"):
                continue
            nl = norm(line)
            if line.startswith("|"):
                if i in ov or re.match(r"^\|[\s:|-]+\|\s*$", line):
                    continue
                if any(norm(s) in nl for s in snips):
                    lines[i] = None; changed = True
                continue
            if not any(norm(s)[:25] in nl for s in snips):
                continue
            m = fs.LIST_PREFIX.match(line)
            prefix, rest = m.group(1) or "", m.group(2)
            keep = [s for s in fs.split_sentences(rest) if not any(norm(x)[:25] in norm(s) for x in snips)]
            out = "".join(keep).strip()
            if out != rest.strip():
                lines[i] = (prefix + out) if out else None; changed = True
        # 資料列被刪光的表格：表頭與分隔列一併拿掉
        for i in range(fm_end, len(lines) - 1):
            if lines[i] and lines[i].startswith("|") and lines[i + 1] and re.match(r"^\|[\s:|-]+\|\s*$", lines[i + 1]):
                j = i + 2
                while j < len(lines) and lines[j] is None:
                    j += 1
                if j >= len(lines) or not (lines[j] or "").startswith("|"):
                    if any(lines[k] is None for k in range(i + 2, j)):
                        lines[i] = lines[i + 1] = None
        text = "\n".join(x for x in lines if x is not None)
        if not changed:
            break
    return text


_SL = {}


def status_label(site):
    """該站概覽表市場狀態列最常用的標題（沿用現有頁，不新寫）"""
    if site not in _SL:
        from collections import Counter as _C
        c = _C()
        for f in list((BASE / site / "docs/_drugs").glob("*.md"))[:400]:
            body = f.read_text(encoding="utf-8", errors="replace")
            tb = ck.tables(body)
            if tb:
                st = ck.status_row(site, tb[0][1])
                if st:
                    c[st[0]] += 1
        _SL[site] = c.most_common(1)[0][0] if c else None
    return _SL[site]


def status_value(site, fc):
    """與 apply_programmatic 同一套多語狀態句"""
    lang = ck.LANG.get(site, "en")
    tl = ck.mv2.T.get(lang) or ck.mv2.T["en"]
    ms, v, n, partial = fc.get("market_status"), fc.get("valid"), fc.get("total"), fc.get("partial")
    if ms == "Marketed":
        return ck.marketed_text(site, lang, v, n, partial)
    if ms == "Approved, not marketed":
        return ck.NOT_MKT.get(lang, ck.NOT_MKT["en"]).format(n=n)
    if ms == "Cancelled only":
        return ck.cancelled_text(site, lang, n)
    if ms == "Not marketed":
        return ck.not_reg_text(site, lang)
    return None


_TW = {}


def tw_count_row(page, text, start):
    """Tw：快速總覽缺「許可證數」列時，用 Tw 自己的許可證快照與 count_text() 補（寫法與 Tw 其他頁相同）"""
    if "T" not in _TW:
        import sys as _s
        _s.path.insert(0, str(BASE / "TwTxGNN" / "src"))
        from twtxgnn.regulatory import tfda_licenses as T
        _TW["T"] = T
        _TW["snap"] = (T.load_snapshot() or {}).get("drugs", {})
    T = _TW["T"]
    lines = text.split("\n")
    ov = overview_rows(lines, start)
    if not ov or any(ck.is_count_label(lines[i].strip().strip("|").split("|")[0].strip()) for i in ov):
        return text
    ent = _TW["snap"].get(page) or _TW["snap"].get(page.replace("-", "_"))
    if not ent:
        return text
    s = T.summarize(ent.get("licenses") or [])
    rows = [[c.strip() for c in lines[i].strip().strip("|").split("|")] for i in ov]
    at = next((i for i, r in zip(ov, rows) if ck.STATUS_LABEL.search(r[0])), ov[-1])
    lines.insert(at + 1, f"| 許可證數 | {T.count_text(s)} |")
    return "\n".join(lines)


def ensure_status_rows(site, page, text, start):
    """概覽表缺市場狀態列 → 依 license_facts 補在原適應症列（或表頭）之後；張數列交給 apply_programmatic 依狀態列補"""
    fc = ck.facts(site).get(page) or ck.facts(site).get(page.replace("-", "_")) or ck.facts(site).get(page.replace("_", "-"))
    lines = text.split("\n")
    ov = overview_rows(lines, start)
    if not ov:
        return text
    rows = [[c.strip() for c in lines[i].strip().strip("|").split("|")] for i in ov]
    st = ck.status_row(site, rows)
    if site == "TwTxGNN":
        return tw_count_row(page, text, start)
    lab = status_label(site)
    if lab is None:
        return text
    want = status_value(site, fc) if fc else NOT_RECORDED[lang_of(site)]
    if want is None:
        want = NOT_RECORDED[lang_of(site)]
    if st is not None:  # 已有狀態列：值由 apply_programmatic／license_table_sync 依事實改
        return text
    at = next((i for i, r in zip(ov, rows) if ck.ORIG_ROW.search(r[0])), ov[0] - 1 if ov else None)
    lines.insert(at + 1, f"| {lab} | {want} |")
    # 已知用途產生器留下的英文佔位狀態列（Jp）：有正式狀態列後拿掉
    lines = [l for l in lines if not (l.startswith("|") and "No licence found in this site's data" in l)]
    return "\n".join(lines)


_NP = {}


def nopred_template(site):
    """該站已上線已知用途頁的 description／parent 反推模板（不新寫翻譯）：(desc_tpl, parent)"""
    if site in _NP:
        return _NP[site]
    from collections import Counter as _C
    tpls, parents = _C(), _C()
    cl = ck.classification()
    for (s, pg), c in cl.items():
        if s != site or c not in ("known_use", "no_pred_keep"):
            continue
        f = BASE / s / "docs/_drugs" / f"{pg}.md"
        if not f.exists():
            continue
        head = f.read_text(encoding="utf-8", errors="replace")[:3000]
        ti = re.search(r"^title:\s*(.+?)\s*$", head, re.M)
        de = re.search(r'^description:\s*"(.*)"\s*$', head, re.M)
        pa = re.search(r"^parent:\s*(.+?)\s*$", head, re.M)
        if pa and re.search(r"^evidence_level:\s*N/A", head, re.M):
            parents[pa.group(1)] += 1
        if ti and de and de.group(1).startswith(ti.group(1).strip('"')):
            tpls["{title}" + de.group(1)[len(ti.group(1).strip('"')):]] += 1
    _NP[site] = (tpls.most_common(1)[0][0] if tpls else None, parents.most_common(1)[0][0] if parents else None)
    return _NP[site]


def transform_nopred(site, f, cls, pmap):
    """沒有 kept 預測的頁：改成「目前無保留預測」版面（預測列、分數、預測段落刪掉；H1／description 用該站模板）"""
    t0, t1, crlf = ap.transform(site, f, cls, pmap)
    b = ck.amf.load_bundle(BASE / site, f.stem)
    tpl, parent = nopred_template(site)
    lines = t1.split("\n")
    fm_end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0) + 1
    fm = lines[:fm_end]
    title = next((l.split(":", 1)[1].strip().strip('"').strip("'") for l in fm if l.startswith("title:")), f.stem)
    fm = [l for l in fm if not re.match(r"^(predicted_indications|indication_count|evidence_level):", l) and not re.match(r"^\s+-\s", l)]
    fm.insert(-1, "predicted_indications: []"); fm.insert(-1, "indication_count: 0"); fm.insert(-1, "evidence_level: N/A")
    if parent:
        fm = [f"parent: {parent}" if l.startswith("parent:") else l for l in fm]
    if tpl:
        fm = [("description: " + json.dumps(tpl.replace("{title}", title), ensure_ascii=False)) if l.startswith("description:") else l for l in fm]
    body = lines[fm_end:]
    body = [ap.HEAD_N.sub(lambda m: f"{m.group(1)}0{m.group(3)}", l, count=1) for l in body]
    body = [ap.HEAD_L.sub(lambda m: f"{m.group(1)}N/A{m.group(3)}", l, count=1) if ap.HEAD_L.search(l) and "**L" in l else l for l in body]
    text = "\n".join(fm + body)
    lines = text.split("\n")
    start = next((i for i, l in enumerate(lines) if 'id="pharmacist"' in l), 0)
    ov = set(overview_rows(lines, start))
    out = []
    h1_done = False
    for i, l in enumerate(lines):
        if l.startswith("|") and not re.match(r"^\|[\s:|-]+\|\s*$", l):
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if i in ov and cells and KG_PRED_ROW.search(cells[0]):
                continue  # 「KG Predictions」列（把知識圖譜當預測）
            if i in ov and len(cells) >= 2:
                if ck.ORIG_ROW.search(cells[0]):
                    ov_ = orig_value(site, b, f.stem)
                    if ov_ is not None:
                        l = f"| {cells[0]} | {ov_} |"
                elif ck.PRED_ROW.search(cells[0]) or dm.PRED_LABEL.search(cells[0]) or SCORE_LABEL.search(cells[0]) or ck.LEVEL_ROW.search(cells[0]):
                    continue
            elif ck.score_tokens(l) and any(SCORE_LABEL.search(c) for c in cells[:1]) is False and re.search(r"0[.,]9\d|\d{2}[.,]\d+\s?%", l):
                continue
        if not h1_done and i > start and is_title(lines, i):
            l = title_line(l, title); h1_done = True
        out.append(l)
    t2 = "\n".join(out)
    if "<!-- known-uses-page -->" not in t2 and site != "TwTxGNN":  # Tw 頁面有人工查核框與程式許可證區塊，不刪段（2026-10-29 urea 教訓）
        t2 = drop_prediction_sections(site, f.stem, t2, start)
    t2 = ensure_status_rows(site, f.stem, t2, start)
    tmp = OUT / "_pass2" / site / f.name
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(t2, encoding="utf-8")
    t2 = ap.transform(site, tmp, cls, pmap)[1]
    t2 = strip_by_checker(site, t2, cls, f.name, overview_rows(t2.split("\n"), start))
    return t0, t2, crlf


DECISION = re.compile(r"decision|決策|判断|決定|결정|decisão|decisión|entscheidung|beslut|besluit|beslutning|päätös|décision|decisione|keputusan|القرار|การตัดสินใจ|推奨", re.I)


def drop_prediction_sections(site, page, text, start):
    """無預測頁（非已知用途產生器的頁）：只留概覽表、上市資訊起到結論前的段落（上市、安全性）、免責聲明。
    上市資訊段＝第一個出現本藥許可證字號的段（不靠各語言標題字面）；結論＝免責聲明前一段。"""
    lines = text.split("\n")
    h1 = next((i for i in range(start, len(lines)) if is_title(lines, i)), None)
    if h1 is None:
        return text
    heads = [i for i in range(h1 + 1, len(lines)) if lines[i].startswith("## ")]
    if not heads:
        return text
    bounds = [(h, (heads[k + 1] if k + 1 < len(heads) else len(lines))) for k, h in enumerate(heads)]
    fc = ck.facts(site).get(page) or ck.facts(site).get(page.replace("-", "_")) or ck.facts(site).get(page.replace("_", "-")) or {}
    ids = [re.escape(x) for x in (fc.get("licenses") or {})]
    lic_rx = re.compile("|".join(ids)) if ids else None
    st_rx = re.compile(r"\|[^|\n]*\|")
    ov_sec = next((k for k, (a, z) in enumerate(bounds) if any(l.startswith("|") for l in lines[a:z])), None)
    mkt = next((k for k, (a, z) in enumerate(bounds) if k != ov_sec and lic_rx and any(lic_rx.search(l) for l in lines[a:z])), None)
    disc = next((k for k, (a, z) in enumerate(bounds) if fs.DISCLAIMER.search(lines[a])), len(bounds))
    keep = set()
    if ov_sec is not None:
        keep.add(ov_sec)
    if mkt is not None:
        keep |= set(range(mkt, max(mkt + 1, disc - 1)))
    keep |= set(range(disc, len(bounds)))
    keep |= {k for k, (a, z) in enumerate(bounds) if any("<!-- brand-names:start -->" in l for l in lines[a:z])}  # Jp 販売名區塊不刪
    drop = set()
    for k, (a, z) in enumerate(bounds):
        if k not in keep:
            drop |= set(range(a, z))
    # 概覽表的「建議決策」列也拿掉（決策是針對預測）
    if ov_sec is not None:
        a, z = bounds[ov_sec]
        for i in range(a, z):
            if lines[i].startswith("|") and DECISION.search(lines[i].strip().strip("|").split("|")[0]):
                drop.add(i)
    # H1 到第一段之間的導言（多半在講預測）也拿掉
    drop |= {i for i in range(h1 + 1, heads[0]) if lines[i].strip() and not lines[i].startswith(("<", "{:"))}
    return "\n".join(l for i, l in enumerate(lines) if i not in drop)


PCT_ANY = re.compile(r"(?<![\d.,])(9\d[.,]\d{2,4})\s?[%％٪]")


def pct_to_decimal(text, kept_sc):
    """解說裡寫成百分比、但數值對得上 kept 分數的 → 4 位小數（快速總覽由程式另填）；對不上的留給 checker 判、整句刪"""
    def rep(m):
        v = float(m.group(1).replace(",", ".")) / 100
        k = next((x for x in kept_sc if abs(x - v) < 0.00006 or abs(round(x * 100, 2) - v * 100) < 0.005), None)
        return f"{k:.4f}" if k is not None else m.group(0)
    lines = text.split("\n")
    fm_end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0) + 1
    return "\n".join(l if i < fm_end else PCT_ANY.sub(rep, ck.norm_digits(l) if PCT_ANY.search(ck.norm_digits(l)) else l)
                     for i, l in enumerate(lines))


def is_title(lines, i):
    """報告標題：`# `，或降級後的「`## ` ＋下一行 {: .text-alpha }」"""
    l = lines[i]
    return l.startswith("# ") or (l.startswith("## ") and i + 1 < len(lines) and lines[i + 1].strip() == "{: .text-alpha }")


def title_line(old, text):
    return ("## " if old.startswith("## ") else "# ") + text


def minimal(site, f, cls, pmap):
    """精簡版事實層：原適應症格由程式填、checker 報的違規句整句刪；H1、主預測、description 不動"""
    t0, t1, crlf = ap.transform(site, f, cls, pmap)
    b = ck.amf.load_bundle(BASE / site, f.stem)
    lines = t1.split("\n")
    start = next((i for i, l in enumerate(lines) if 'id="pharmacist"' in l), 0)
    ov = overview_rows(lines, start)
    for i in ov:
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if len(cells) >= 2 and ck.ORIG_ROW.search(cells[0]):
            v = orig_value(site, b, f.stem)
            if v is not None:
                set_row(lines, i, v)
    t2 = "\n".join(lines)
    return strip_by_checker(site, t2, cls, f.name, overview_rows(t2.split("\n"), start))


def transform(site, f, cls, pmap):
    t0, t1, crlf = ap.transform(site, f, cls, pmap)  # 步驟 1（讀本機檔：--local 由 ap.LOCAL 決定）
    b = ck.amf.load_bundle(BASE / site, f.stem)
    kept = ck.kf.kept_predictions(BASE / site, b) if cls not in ("no_pred_keep", "no_pred_noindex") else []
    if not kept or cls in ("known_use", "no_pred_keep", "no_pred_noindex"):
        return transform_nopred(site, f, cls, pmap)
    d = b.get("drug") or {}
    preds = {ck.norm_name(p["disease_name"]): p for p in d.get("predicted_indications") or [] if p.get("disease_name")}
    k0 = preds.get(ck.norm_name(kept[0]))
    lines = t1.split("\n")
    fm_end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0) + 1
    # 報告本體從 pharmacist div 之後開始
    start = next((i for i, l in enumerate(lines) if 'id="pharmacist"' in l), fm_end)
    ov = overview_rows(lines, start)
    # Sg／My／Ph 舊版型：概覽表「KG Predictions／Ramalan KG」列＝把知識圖譜當預測（P5）→ 整列拿掉
    kg_rows = {i for i in ov if KG_PRED_ROW.search(lines[i].strip().strip("|").split("|")[0])}
    if kg_rows:
        lines = [l for i, l in enumerate(lines) if i not in kg_rows]
        ov = overview_rows(lines, start)
    for i in ov:
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        if ck.ORIG_ROW.search(cells[0]):
            ov_ = orig_value(site, b, f.stem)
            if ov_ is not None:
                set_row(lines, i, ov_)
        elif ck.PRED_ROW.search(cells[0]) or dm.PRED_LABEL.search(cells[0]):
            set_row(lines, i, pred_display(site, kept[0], cells[1]))
        elif SCORE_LABEL.search(cells[0]) and not ck.LEVEL_ROW.search(cells[0]) and k0:
            set_row(lines, i, f"{k0['txgnn_score']:.4f}")
    # 報告 H1（pharmacist div 之後第一個 `# `）
    pcell = next((lines[i] for i in ov if (ck.PRED_ROW.search(lines[i].strip().strip("|").split("|")[0]) or dm.PRED_LABEL.search(lines[i].strip().strip("|").split("|")[0]))), "")
    pdisp = pcell.strip().strip("|").split("|")[1].strip() if pcell else pred_display(site, kept[0], "")
    title = (re.search(r"^title:\s*(.+?)\s*$", "\n".join(lines[:fm_end]), re.M) or [None, f.stem])[1].strip('"').strip("'")
    has_title = False
    for i in range(start, len(lines)):
        if is_title(lines, i):
            lines[i] = title_line(lines[i], f"{title}: {pdisp}")
            has_title = True
            break
    if not has_title:  # 報告沒寫標題（直接從摘要開始）：補一個，每頁仍只有頁首一個 h1
        at = next((i for i in range(start, len(lines)) if lines[i].startswith("## ") and i > start + 2), None)
        if at is not None:
            lines[at:at] = [f"## {title}: {pdisp}", "{: .text-alpha }", ""]
    # 預測表（快速總覽以外）說明欄提到已排除病名：該格清空（病名與分數欄保留）
    ex_names = [x for x in (p.get("disease_name") for p in d.get("predicted_indications") or []) if x and ck.norm_name(x) not in {ck.norm_name(k) for k in kept}]
    ex_rx = [rx for x in ex_names for rx in ck.name_regexes(site, x)]
    keep_rx = [rx for k in kept for rx in ck.name_regexes(site, k)]
    ovs = set(overview_rows(lines, start))
    for i, l in enumerate(lines):
        if i in ovs or not l.startswith("|") or not ck.score_tokens(l):
            continue
        cells = l.strip().strip("|").split("|")
        changed_row = False
        for j in range(2, len(cells)):
            if any(rx.search(cells[j]) for rx in ex_rx) and not ck.score_tokens(cells[j]) and not any(rx.search(cells[j]) for rx in keep_rx):
                cells[j] = " — "; changed_row = True
        if changed_row:
            lines[i] = "|" + "|".join(cells) + "|"
    t2 = "\n".join(lines)
    # 違規句刪除
    excluded = [x for x in (p.get("disease_name") for p in d.get("predicted_indications") or []) if x and ck.norm_name(x) not in {ck.norm_name(k) for k in kept}]
    kept_sc = [preds[ck.norm_name(k)]["txgnn_score"] for k in kept if ck.norm_name(k) in preds]
    facts = ck.facts(site).get(f.stem) or ck.facts(site).get(f.stem.replace("-", "_")) or ck.facts(site).get(f.stem.replace("_", "-"))
    t2 = pct_to_decimal(t2, kept_sc)
    t2 = strip_sentences(site, t2, kept, excluded, kept_sc, cls, (), facts)
    ovl = overview_rows(t2.split("\n"), next((i for i, l in enumerate(t2.split("\n")) if 'id="pharmacist"' in l), 0))
    drop = excluded_score_rows(site, t2, cls, excluded, kept, set(ovl))
    if drop:
        t2 = "\n".join(l for i, l in enumerate(t2.split("\n")) if i not in drop)
        ovl = overview_rows(t2.split("\n"), next((i for i, l in enumerate(t2.split("\n")) if 'id="pharmacist"' in l), 0))
    t2 = strip_by_checker(site, t2, cls, f.name, ovl)
    t2 = ensure_status_rows(site, f.stem, t2, start)
    # 主預測換成 kept[0] 後，證據等級（P4）等要依新的主預測重判：同一套 apply_programmatic 再跑一次
    tmp = OUT / "_pass2" / site / f.name
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(t2, encoding="utf-8")
    t2 = ap.transform(site, tmp, cls, pmap)[1]
    # description 依概覽表重算
    m = re.match(r"---\n(.*?)\n---\n", t2, re.S)
    if m:
        fm, body = m.group(1), t2[m.end():]
        lv = (re.search(r'^evidence_level:\s*"?(L[1-5])', fm, re.M) or [None, ""])[1]
        r = dm.summary_rows(body)
        if r and lv:
            tpl = dm.T.get(dm.site_lang(BASE / site), dm.T["en"])
            orig = dm.clean(r[0][1], 70) if r[0][1] else ""
            pred_txt = r[1][1].strip()
            desc = dm.render(tpl, title, pred_txt if len(pred_txt) > 120 else dm.clean(pred_txt, 120), lv, orig)
            if len(desc) > 199:
                desc = dm.render(tpl, title, pred_txt if len(pred_txt) > 120 else dm.clean(pred_txt, 120), lv, "")
            newl = "description: " + json.dumps(desc if len(desc) <= 300 else desc[:299] + "…", ensure_ascii=False)
            fl = [l for l in fm.split("\n") if not l.startswith("description:")] + [newl]
            t2 = "---\n" + "\n".join(fl) + "\n---\n" + body
    return t0, t2, crlf


def main(argv):
    apply_ = "--apply" in argv
    ap.LOCAL = True
    pages = None
    if "--pages" in argv:
        pages = {tuple(x.split(":", 1)) for x in argv[argv.index("--pages") + 1].split(",") if x}
    sites = [a for a in argv if a.endswith("TxGNN")] or sorted({p[0] for p in pages} if pages else (p.name for p in BASE.glob("*TxGNN")))
    OUT.mkdir(parents=True, exist_ok=True)
    cl = ck.classification()
    diffs, rows, summ = [], [], Counter()
    for s in sites:
        pmap = ap.parent_map(s)
        files = sorted((BASE / s / "docs/_drugs").glob("*.md"))
        for f in files:
            if pages is not None and (s, f.stem) not in pages:
                continue
            head = f.read_text(encoding="utf-8", errors="replace")[:3000]
            if 'http-equiv="refresh"' in head or "layout: id_redirect" in head:
                continue
            cls = cl.get((s, f.stem), "keep")
            if (s, f.stem) not in cl and "--any-scope" not in argv:  # 稽核範圍外（多為早已 noindex 的頁）不動；sync 呼叫時帶 --any-scope
                continue
            try:
                before = sorted({e[0] for e in ck.check_page(s, f, cls, False) if e[0] != "P7"})
                if not before and "--force" not in argv:  # 已經可以發佈的頁一字不動（--force：指定頁強制重套，例如規則修正後）
                    summ["pages"] += 1; summ["skipped_clean"] += 1
                    rows.append((s, f.stem, "", "", "skip_clean"))
                    continue
                t0, t2, crlf = transform(s, f, cls, pmap)
            except Exception as e:
                rows.append((s, f.stem, "X", f"處理失敗：{str(e)[:100]}", "")); summ["error"] += 1
                continue
            tmp = OUT / "_tmp" / s / f.name
            tmp.parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text(t2, encoding="utf-8")
            after = sorted({e[0] for e in ck.check_page(s, tmp, cls, False) if e[0] != "P7"})
            if set(after) - set(before):  # 改後多出新錯 → 改用精簡版（只填原適應症＋刪 checker 報的違規句，不動 H1／主預測／description）再試
                t2m = minimal(s, f, cls, pmap)
                tmp.write_text(t2m, encoding="utf-8")
                after_m = sorted({e[0] for e in ck.check_page(s, tmp, cls, False) if e[0] != "P7"})
                if not (set(after_m) - set(before)) and t2m != t0:
                    t2, after = t2m, after_m
            if set(after) - set(before):  # 不准讓頁面多出原本沒有的錯：退回原檔
                rows.append((s, f.stem, ",".join(before), ",".join(before), "reverted_regress")); summ["reverted_regress"] += 1
                summ["pages"] += 1; summ["nonzero_before"] += 1; summ["nonzero_after"] += 1
                continue
            if t2 != t0:
                summ["changed"] += 1
                diffs += difflib.unified_diff(t0.splitlines(True), t2.splitlines(True), f"a/{s}/{f.name}", f"b/{s}/{f.name}", n=0)
                today = __import__("datetime").datetime.now(__import__("datetime").timezone(__import__("datetime").timedelta(hours=8))).strftime("%Y-%m-%d")
                if re.search(r"^last_modified_at:", t2[:3000], re.M):
                    t2 = re.sub(r"^last_modified_at:.*$", f"last_modified_at: {today}", t2, count=1, flags=re.M)
                else:
                    t2 = t2.replace("\n---\n", f"\nlast_modified_at: {today}\n---\n", 1)
                if apply_:
                    f.write_bytes((t2.replace("\n", "\r\n") if crlf else t2).encode("utf-8"))
            summ["pages"] += 1
            summ["nonzero_before"] += bool(before)
            summ["nonzero_after"] += bool(after)
            rows.append((s, f.stem, ",".join(before), ",".join(after), "changed" if t2 != t0 else ""))
    (OUT / "changes.diff").write_text("".join(diffs), encoding="utf-8")
    with open(OUT / "results.tsv", "w", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t"); w.writerow(["site", "page", "before", "after", "changed"]); w.writerows(rows)
    print(dict(summ), "after:", Counter(c for r in rows for c in r[3].split(",") if c and r[2] != "X"))


if __name__ == "__main__":
    main(sys.argv[1:])
