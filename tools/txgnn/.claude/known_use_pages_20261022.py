"""已知用途頁（2026-10-22，用戶決定）：證據包的預測經 known_use_filter 排除後一個都不剩的頁，改寫成
「目前沒有新預測，以下是本藥已知用途與當地上市狀況」，保持可收錄。

事實全部由程式準備（模型只負責寫成該站語言）：
  - 被排除的已知用途（證據包前 10 名預測）與來源：KG／本國許可證／他國許可證／人工補充（known_use_extra.json）
  - 市場狀態：.claude/cache/license_facts（修正後 reviewer；部分紀錄寫「至少」）
寫入 data/notes/<藥>/drug_pharmacist_notes.md（帶 <!-- known-uses-page --> 標記，sync 據此：證據等級 N/A、預測數 0、
不套 L5 noindex、description 取 <!-- description: --> ），舊 notes 先備份到 .claude/cache/notes_backup_20261021/。
驗收（不過就還原舊 notes）：H1／description 不得出現該語言的「預測新適應症」；每個被排除的已知用途（英文名）都要出現；
數字只能來自事實；不得出現 L1–L5。
用法（母目錄）：python3 .claude/known_use_pages_20261022.py --list site:page,... | --all [--part i/n] [--dry]
"""
import csv
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BK = BASE / ".claude/cache/notes_backup_20261021"
RES = BASE / ".claude/audit_20261016/known_use_pages_results.tsv"


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


kf = _load("kf", BASE / ".claude/known_use_filter.py")
dm = _load("dm", BASE / ".claude/drug_meta_description.py")
mv2 = _load("mv2", BASE / ".claude/rewrite_market_v2_20261021.py")
COUNTRY = {"ARTxGNN": "Argentina", "AuTxGNN": "Australia", "BrTxGNN": "Brazil", "CHTxGNN": "Switzerland", "COTxGNN": "Colombia",
           "CaTxGNN": "Canada", "DETxGNN": "Germany", "DkTxGNN": "Denmark", "ESTxGNN": "Spain", "EuTxGNN": "the European Union",
           "FITxGNN": "Finland", "FRTxGNN": "France", "HkTxGNN": "Hong Kong", "ITTxGNN": "Italy", "InTxGNN": "India",
           "JpTxGNN": "Japan", "KrTxGNN": "South Korea", "MyTxGNN": "Malaysia", "NOTxGNN": "Norway", "NZTxGNN": "New Zealand",
           "NlTxGNN": "the Netherlands", "PhTxGNN": "the Philippines", "SATxGNN": "Saudi Arabia", "SETxGNN": "Sweden",
           "SgTxGNN": "Singapore", "ThTxGNN": "Thailand", "TwTxGNN": "Taiwan", "UkTxGNN": "the United Kingdom",
           "UsTxGNN": "the United States", "ZaTxGNN": "South Africa"}
LANGNAME = {"en": "English", "zh": "Traditional Chinese", "ja": "Japanese", "ko": "Korean", "es": "Spanish", "pt": "Brazilian Portuguese",
            "de": "German", "fr": "French", "it": "Italian", "fi": "Finnish", "no": "Norwegian Bokmål", "sv": "Swedish", "da": "Danish",
            "nl": "Dutch", "ar": "Arabic", "ms": "Malay", "th": "Thai"}
COMMON_RULES = """Rules:
- Use only the facts. Never call a "knowledge graph relation" or "same disease category" item approved or licensed; only zone "approved" items are approved, and give their source (and matched_term when it differs).
- Write {{drug}} exactly as given (Latin name) in the description and H1; in Japanese pages add the katakana name in parentheses at its first mention in the body only.
- Disease names: "<local-language name> (<English name exactly as given>)"; if the local name is the same as the English name, write it once.
- If combination_only is true, say in the summary that in {{country}} the drug is available only in combination products.
- Never write evidence levels L1–L5; no preamble, no code fence; do not write a market or licence section (it is added separately)."""

STRUCT_ALL_KNOWN = """For this drug the TxGNN deep-learning model (score ≥ 0.99) produced candidates, but every candidate that can be traced to a source is already a KNOWN use, so there is NO new predicted indication.

Output exactly (keep HTML comments; translate headings into {lang}):
<!-- known-uses-page -->
<!-- description: <≤150 characters: "{{drug}}: known uses and market status in {{country}}; currently no new candidate indication". Do not use the phrase "predicted new indication".> -->
# {{drug}}: <"Known uses and market status in {{country}}">

## <"Summary">
<2–3 sentences: the model's candidates for this drug are all known uses, so there is currently no new predicted indication.>

## <"Quick overview">
| <"Item"> | <"Content"> |
|------|------|
| <"New predicted indications"> | <"None (all traceable model candidates are known uses)"> |
| <"Known uses among model candidates"> | <known_use_count> |
| <"Evidence level"> | <"Not applicable"> |
| <"Market status in {{country}}"> | <market_status_text, verbatim> |

## <"Known uses among the model's candidates">"""

STRUCT_NO_CAND = """For this drug the TxGNN deep-learning model produced NO candidate indication with a score of 0.99 or higher, so there is NO new predicted indication. The known uses in the facts are the drug's own recorded uses, NOT model candidates; never call them model candidates.

Output exactly (keep HTML comments; translate headings into {lang}):
<!-- known-uses-page -->
<!-- description: <≤150 characters: "{{drug}}: known uses and market status in {{country}}; currently no new candidate indication". Do not use the phrase "predicted new indication".> -->
# {{drug}}: <"Known uses and market status in {{country}}">

## <"Summary">
<2–3 sentences: the TxGNN model has no candidate with a score of 0.99 or higher for this drug, so there is currently no new predicted indication; the drug's recorded uses are listed below.>

## <"Quick overview">
| <"Item"> | <"Content"> |
|------|------|
| <"New predicted indications"> | <"None (no model candidate scored 0.99 or higher)"> |
| <"Known uses recorded for this drug"> | <known_use_count> |
| <"Evidence level"> | <"Not applicable"> |
| <"Market status in {{country}}"> | <market_status_text, verbatim> |

## <"Known uses recorded for this drug">"""

TABLES = """
### <"Approved (supported by a licence or label)">
| <"Indication"> | <"Source"> |
|------|------|
<rows for zone "approved": disease name | source (add "approved indication: <matched_term>" when matched_term differs from the English name)>
### <"Related to an approved indication (same disease category)">
| <"Indication"> | <"Approved category"> |
|------|------|
<rows for zone "related": disease name | matched_term>
### <"Relations recorded in the knowledge graph (no approval found)">
| <"Indication"> |
|------|
<rows for zone "kg">
(If a group has no rows, keep its heading and write one row saying "none" in {lang}.)"""

SYSTEM = """You write one page of a drug-repurposing website for pharmacists, in {lang}.

Facts (use only these):
{facts}

{struct}
{tables}

{rules}"""


LIC_TABLE = {  # 許可證表（程式產生）：表頭（字號、品名、劑型、狀態）、狀態字樣（有效、註銷、核准未上市）、部分紀錄註記
    "en": (("Licence", "Product", "Dosage form", "Status"), ("Valid", "Cancelled", "Approved, not marketed"), "Only part of the licence list is held in the data; the list may be incomplete."),
    "es": (("Registro", "Producto", "Forma farmacéutica", "Estado"), ("Vigente", "Cancelado", "Autorizado, no comercializado"), "Los datos solo contienen parte de los registros; la lista puede estar incompleta."),
    "pt": (("Registro", "Produto", "Forma farmacêutica", "Situação"), ("Ativo", "Cancelado", "Registrado, não comercializado"), "Os dados contêm apenas parte dos registros; a lista pode estar incompleta."),
    "de": (("Zulassung", "Produkt", "Darreichungsform", "Status"), ("Gültig", "Erloschen", "Zugelassen, nicht im Handel"), "Die Daten enthalten nur einen Teil der Zulassungen; die Liste kann unvollständig sein."),
    "fr": (("AMM", "Produit", "Forme", "Statut"), ("Active", "Annulée", "Autorisée, non commercialisée"), "Les données ne contiennent qu'une partie des autorisations ; la liste peut être incomplète."),
    "it": (("Autorizzazione", "Prodotto", "Forma farmaceutica", "Stato"), ("Valida", "Revocata", "Autorizzata, non in commercio"), "I dati contengono solo una parte delle autorizzazioni; l'elenco può essere incompleto."),
    "nl": (("Registratie", "Product", "Toedieningsvorm", "Status"), ("Geldig", "Ingetrokken", "Geregistreerd, niet in de handel"), "De gegevens bevatten slechts een deel van de registraties; de lijst kan onvolledig zijn."),
    "da": (("Tilladelse", "Produkt", "Lægemiddelform", "Status"), ("Gyldig", "Afmeldt", "Godkendt, ikke markedsført"), "Dataene indeholder kun en del af tilladelserne; listen kan være ufuldstændig."),
    "no": (("Tillatelse", "Produkt", "Legemiddelform", "Status"), ("Gyldig", "Avregistrert", "Godkjent, ikke markedsført"), "Dataene inneholder bare en del av tillatelsene; listen kan være ufullstendig."),
    "sv": (("Godkännande", "Produkt", "Läkemedelsform", "Status"), ("Giltigt", "Avregistrerat", "Godkänt, ej marknadsfört"), "Data innehåller bara en del av godkännandena; listan kan vara ofullständig."),
    "fi": (("Myyntilupa", "Valmiste", "Lääkemuoto", "Tila"), ("Voimassa", "Peruttu", "Hyväksytty, ei markkinoilla"), "Aineisto sisältää vain osan myyntiluvista; luettelo voi olla puutteellinen."),
    "zh": (("許可證字號", "品名", "劑型", "狀態"), ("有效", "已註銷", "已核准未上市"), "資料只收錄部分許可證，清單可能不完整。"),
    "ja": (("承認番号", "販売名", "剤形", "状態"), ("有効", "取消", "承認済み・未発売"), "データには承認の一部のみが含まれており、一覧は不完全な可能性があります。"),
    "ko": (("허가번호", "제품명", "제형", "상태"), ("유효", "취소", "허가됨·미시판"), "데이터에는 허가의 일부만 포함되어 있어 목록이 불완전할 수 있습니다."),
    "ms": (("No. pendaftaran", "Produk", "Bentuk dos", "Status"), ("Sah", "Dibatalkan", "Diluluskan, tidak dipasarkan"), "Data hanya mengandungi sebahagian pendaftaran; senarai mungkin tidak lengkap."),
    "ar": (("رقم الترخيص", "المنتج", "الشكل الصيدلاني", "الحالة"), ("ساري", "ملغى", "معتمد وغير مسوَّق"), "تتضمن البيانات جزءاً فقط من التراخيص؛ قد تكون القائمة غير مكتملة."),
    "th": (("เลขทะเบียน", "ผลิตภัณฑ์", "รูปแบบยา", "สถานะ"), ("ยังมีผล", "ยกเลิก", "อนุมัติแต่ยังไม่วางจำหน่าย"), "ข้อมูลมีเพียงบางส่วนของทะเบียนยา รายการอาจไม่ครบถ้วน"),
}


def _plain(s):
    return {x for x in s if not x.startswith(("cat:", "text:"))}


def _sources_of(site, bundle):
    d = bundle["drug"]
    db, inn = d.get("drugbank_id") or "", (d.get("inn") or d.get("name") or "")
    kg = kf.known_set(BASE / site, db) | kf.known_set(BASE / site, inn.lower())
    local_all = kf.license_terms(BASE / site, bundle)
    extra = json.loads((BASE / ".claude/known_use_extra.json").read_text()).get(db, {})
    ext = set(extra.get("terms", []))
    glob_all = kf._global_license().get(db, set()) - ext
    return kg, local_all, glob_all, ext, extra


def classify(site, bundle, x):
    """一個病名 → (區, 依據)。核准＝本國／他國許可證或人工補充仿單的條文本身或其子型；related＝只是同一疾病類別；kg＝KG 真有該邊（或其子型）。
    都對不上就回 None（不列，不捏造來源）。"""
    kg, local_all, glob_all, ext, extra = _sources_of(site, bundle)
    for zone, terms in (("approved:local", _plain(local_all)), ("approved:curated", _plain(ext)), ("approved:other", _plain(glob_all) - _plain(local_all))):
        hit = next((k for k in sorted(terms, key=len) if kf._n(x) == k or kf.is_known_variant(x, {k})), None)
        if hit:
            return zone, hit
    kgh = next((k for k in sorted(kg, key=len) if kf._n(x) == k or kf.is_known_variant(x, {k})), None)
    if kgh:
        return "kg", kgh
    lic_cats = {c[4:] for c in local_all | glob_all | ext if c.startswith("cat:")} | set().union(*(kf._cats(k) for k in _plain(local_all | glob_all | ext)))
    cat = kf._cats(x) & lic_cats
    if cat:
        return "related", sorted(cat)[0]
    return None


def _dedupe(items):
    seen, out = set(), []
    for x, z in items:
        k = re.sub(r"\s*\((disease|disorder)\)", "", kf._n(x))
        if k not in seen:
            seen.add(k); out.append((x, z))
    return out


def dl_candidates(site, page, bundle):
    """證據包已清空（全部是已知用途）的藥：候選改從 DL 檔取（≥0.99、依病名去重、前 10），2026-10-23 pm 同意。
    藥名對應依序用 inn、頁名、DrugBank ID（與刷新腳本同一套）。"""
    import gzip
    d = bundle["drug"]
    keys = [str(d.get("inn") or "").lower(), page.replace("_", " ").replace("-", " ").lower(), page.lower()]
    dbid = (d.get("drugbank_id") or kf._dl_dbid(BASE / site).get(str(d.get("inn") or d.get("name") or "").lower(), "")).upper()
    rows = []
    f = BASE / site / "data/processed/txgnn_dl_predictions.csv.gz"
    with gzip.open(f, "rt", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            if float(r["txgnn_score"]) >= kf.SCORE_MIN and (r["drug_name"].lower() in keys or (dbid and r["drugbank_id"].upper() == dbid)):
                rows.append((float(r["txgnn_score"]), r["潛在新適應症"]))
    seen, out = set(), []
    for sc, x in sorted(rows, reverse=True):
        if x.lower() not in seen:
            seen.add(x.lower()); out.append(x)
    return out[:10]


def candidate_known_uses(site, bundle, cands=None):
    """全部已知頁：前 10 名中 ≥0.99、非 susceptibility 的候選，只列找得到來源的。cands 給定時用它（DL 檔候選）。"""
    if cands is None:
        cands = [p["disease_name"] for p in bundle["drug"].get("predicted_indications", [])
                 if p.get("disease_name") and (p.get("txgnn_score") or 0) >= kf.SCORE_MIN][:10]
    cands = [c for c in cands if "susceptibility" not in c.lower()]
    rows, dropped = [], []
    for x in cands:
        z = classify(site, bundle, x)
        (rows if z else dropped).append((x, z) if z else x)
    return _dedupe(rows), dropped


def own_known_uses(site, bundle, cap=15):
    """無新預測頁：本藥自己的已知用途（許可證／仿單核准優先，再 KG），不含 susceptibility。"""
    kg, local_all, glob_all, ext, extra = _sources_of(site, bundle)
    rows = []
    for zone, terms in (("approved:local", _plain(local_all)), ("approved:curated", _plain(ext)),
                        ("approved:other", _plain(glob_all) - _plain(local_all)), ("kg", kg)):
        for x in sorted(terms):
            if 4 <= len(x) <= 80 and "susceptibility" not in x:
                rows.append((x, (zone, x)))
    return _dedupe(rows)[:cap]


def combination_only(bundle):
    recs = [r for v in bundle.values() if isinstance(v, dict) and isinstance(v.get("records"), list) for r in v["records"] if isinstance(r, dict)]
    ings = [len([i for i in str(r.get("ingredients") or r.get("主成分略述") or "").split(";;") if i.strip()]) for r in recs]
    return bool(ings) and all(n > 1 for n in ings)


def license_section(site, page, bundle, fa, heading):
    """許可證表與市場段落：依 license_facts（軌 5 v4 同口徑）程式產生，不沿用舊報告的表。"""
    lang = mv2.LANG.get(site, "en")
    lang = "en" if lang == "en-us" else lang
    (h1, h2, h3, h4), (sv, sc, snm), note = LIC_TABLE.get(lang, LIC_TABLE["en"])
    word = {"valid": sv, "cancelled": sc, "not_marketed": snm}
    seen, rows = set(), []
    for v in bundle.values():
        if isinstance(v, dict) and isinstance(v.get("records"), list):
            for r in v["records"]:
                if not isinstance(r, dict):
                    continue
                lid = r.get("license_id") or r.get("許可證字號") or r.get("reg_no") or r.get("registration_number") or ""
                if not lid or lid in seen:
                    continue
                seen.add(lid)
                name = r.get("brand_name_en") or r.get("product_name") or r.get("product") or r.get("brand_name_zh") or ""
                form = r.get("dosage_form") or ""
                st = (fa.get("licenses") or {}).get(lid, "valid")
                rows.append(f"| {lid} | {str(name).replace('|', '/')[:60]} | {str(form).replace('|', '/')[:40]} | {word.get(st, sv)} |")
    out = [heading, "", f"| {h1} | {h2} | {h3} | {h4} |", "|------|------|------|------|"] + rows[:30]
    if fa.get("partial") or len(rows) > 30:
        out += ["", note]
    return "\n".join(out) if rows else ""


def facts_for(site, page):
    b = json.load(open(BASE / site / "data/bundles" / page / "drug_bundle.json", encoding="utf-8"))
    title = re.search(r"^title:\s*(.+)$", (BASE / site / "docs/_drugs" / f"{page}.md").read_text(encoding="utf-8"), re.M).group(1).strip()
    fa = json.loads((BASE / ".claude/cache/license_facts" / f"{site}.json").read_text()).get(page, {})
    lang = mv2.LANG.get(site, "en")
    if fa.get("market_status") == "Marketed":
        mk = (mv2.T[lang][1].format(v=fa["valid"]) if fa.get("partial") else mv2.T[lang][0].format(v=fa["valid"], n=fa.get("total")))
    elif fa.get("market_status") == "Cancelled only":
        mk = f"Cancelled only: {fa.get('total')} licence(s) on record, none valid"
    elif fa.get("market_status") == "Approved, not marketed":  # 與 check_drug_page.NOT_MKT 同一份字彙
        mk = _ck().NOT_MKT.get(lang, _ck().NOT_MKT["en"]).format(n=fa.get("total"))
    elif site == "KrTxGNN" or str(fa.get("market_status", "")).startswith("Unknown"):
        mk = _ck().KR_UNKNOWN if site == "KrTxGNN" else "Unknown (the data source does not record cancellation status)"
    else:
        mk = "No licence found in this site's data"
    hi = [x for x in b["drug"].get("predicted_indications", []) if (x.get("txgnn_score") or 0) >= kf.SCORE_MIN
          and "susceptibility" not in str(x.get("disease_name", "")).lower()]
    dl = [] if hi else dl_candidates(site, page, b)
    dl = [x for x in dl if "susceptibility" not in x.lower()]
    if not hi and not dl:  # 無新預測頁：DL 檔沒有任何 ≥0.99 候選 → 列本藥已知用途
        rows, dropped, mode = own_known_uses(site, b), [], "no_candidate"
    elif not hi:  # 證據包已清空、但 DL 有 ≥0.99 候選且全是已知用途
        (rows, dropped), mode = candidate_known_uses(site, b, dl), "all_candidates_known"
    else:
        (rows, dropped), mode = candidate_known_uses(site, b), "all_candidates_known"
    zname = {"approved:local": f"licence in {COUNTRY[site]}", "approved:other": "licence in another country",
             "approved:curated": "official label (curated)", "related": "same disease category as an approved indication", "kg": "knowledge graph relation"}
    kus = [{"english_name": x, "zone": ("approved" if z[0].startswith("approved") else z[0]), "source": zname[z[0]],
            "matched_term": z[1]} for x, z in rows]
    return {"mode": mode, "drug": title, "country": COUNTRY[site], "market_status_text": mk, "combination_only": combination_only(b),
            "known_use_count": len(kus), "known_uses": kus, "_dropped_no_source": dropped}, (b, fa)


_CK = None


def _ck():
    global _CK
    if _CK is None:
        _CK = _load("ck", BASE / ".claude/check_drug_page.py")
    return _CK


LIMIT_RX = re.compile(r"usage limit|rate.?limit|\b429\b|overloaded|limit reached|hit your limit|limit.{0,40}resets", re.I)  # 2026-10-23 pm：撞額度要退避重試，不算失敗


def call(system, text):
    cmd = ["claude", "-p", "--output-format", "text", "--tools", "", "--strict-mcp-config", "--mcp-config",
           '{"mcpServers":{}}', "--model", "sonnet", "--system-prompt", system]
    attempt = 0
    while attempt < 5:
        r = subprocess.run(cmd, input=text, capture_output=True, text=True, timeout=1200)
        if r.returncode == 0 and r.stdout.strip() and not LIMIT_RX.search(r.stdout[:300]):
            o = r.stdout.strip()
            m = re.match(r"^\s*```(?:markdown|md)?\s*\n(.*)\n```\s*$", o, re.S)
            return m.group(1) if m else o
        if LIMIT_RX.search((r.stderr or "") + (r.stdout or "")[:300]):
            print("額度退避 300s", file=sys.stderr, flush=True); time.sleep(300); continue
        time.sleep(30 * 2 ** attempt); attempt += 1
    raise RuntimeError((r.stderr or r.stdout)[:200])


def gate(site, out, facts):
    errs = []
    lang = dm.site_lang(BASE / site)
    phrase = re.split(r"\{pred\}|,", dm.T.get(lang, dm.T["en"]).split(":", 1)[-1].split("：", 1)[-1])[0].strip(" ：:")
    head = "\n".join(l for l in out.split("\n") if l.startswith("# ") or "<!-- description:" in l)
    if phrase and phrase.lower() in head.lower():
        errs.append(f"H1/description 出現「{phrase}」")
    if re.search(r"predicted new indication|new predicted indication|預測新適應症|新預測適應症|予測新適応症|新規予測適応症", head, re.I):
        errs.append("H1/description 出現「預測新適應症」類字樣")
    if "<!-- known-uses-page -->" not in out or "<!-- description:" not in out:
        errs.append("缺少標記")
    for k in facts["known_uses"]:
        if k["english_name"].lower() not in out.lower():
            errs.append(f"缺少已知用途 {k['english_name']}")
    allowed = set(re.findall(r"\d+", json.dumps(facts, ensure_ascii=False))) | {"0", "99", "0.99", "1", "2", "3", "4", "5", "10"}
    extra = set(re.findall(r"\d+", out)) - allowed
    if extra:
        errs.append(f"出現事實以外的數字 {sorted(extra)[:4]}")
    if re.search(r"\bL[1-5]\b", out):
        errs.append("出現 L1–L5")
    return errs


KEEP_H = re.compile(r"^## .*(safety|sicherheit|sécurité|securite|sicurezza|seguridad|segurança|turvallisuus|sikkerhet|säkerhet|sikkerhed|veiligheid|"
                    r"安全|السلامة|keselamatan|ความปลอดภัย|안전|cytotox|zytotox|citotox|sytotoks|cytotoks|細胞毒性|السمية الخلوية|sitotoksik|ความเป็นพิษ|세포독성)", re.I)
MARKET_H = re.compile(r"^## .*(market|markt|marché|marche|mercado|mercato|markkina|marknad|marked|市販|上市|販売|시판|السوق|การวางจำหน่าย|pasaran)", re.I)


def old_notes(site, page):
    src = BK / site / page / "drug_pharmacist_notes.md"
    if not src.exists():
        src = BASE / site / "data/notes" / page / "drug_pharmacist_notes.md"
    if not src.exists():
        return ""
    t_ = src.read_text(encoding="utf-8")
    return "" if "<!-- known-uses-page -->" in t_ else t_


def kept_sections(site, page, old_pred_names):
    """保留舊報告的安全性與 Cytotoxicity 段落；段落裡提到舊預測（英文病名）的行刪掉。"""
    old = old_notes(site, page)
    out, keep = [], False
    for line in old.split("\n"):
        if line.startswith("## ") or line.startswith("# "):
            keep = bool(KEEP_H.match(line))
        if keep and not any(n and n.lower() in line.lower() for n in old_pred_names):
            out.append(line)
    return "\n".join(out).strip()


def run(site, page, dry=False):
    facts, (b, fa) = facts_for(site, page)
    lang = LANGNAME[dm.site_lang(BASE / site)]
    struct = STRUCT_NO_CAND if facts["mode"] == "no_candidate" else STRUCT_ALL_KNOWN
    shown = {k: v for k, v in facts.items() if not k.startswith("_")}
    sysmsg = SYSTEM.format(lang=lang, facts=json.dumps(shown, ensure_ascii=False, indent=1),
                           struct=struct.format(lang=lang), tables=TABLES.format(lang=lang), rules=COMMON_RULES)
    out = call(sysmsg, "Write the page now.")
    errs = gate(site, out, facts)
    old = old_notes(site, page)
    mh = next((l for l in old.split("\n") if MARKET_H.match(l)), "## " + {"Japanese": "国内販売情報"}.get(lang, "Market information"))
    lic = license_section(site, page, b, fa, mh)
    old_preds = [p["disease_name"] for p in b["drug"].get("predicted_indications", [])]
    keep = kept_sections(site, page, old_preds)
    out = out.rstrip() + ("\n\n" + lic if lic else "") + ("\n\n" + keep if keep else "")
    notes = BASE / site / "data/notes" / page / "drug_pharmacist_notes.md"
    if not errs and not dry:
        if notes.parent.exists() and not (BK / site / page).exists():
            (BK / site).mkdir(parents=True, exist_ok=True); shutil.copytree(notes.parent, BK / site / page)
        notes.parent.mkdir(parents=True, exist_ok=True)
        notes.write_text(out + "\n", encoding="utf-8")
    return errs, out


def resolve_tw_reviews(pages):
    """Tw 查核紀錄：已知用途頁改寫後原句已不存在的紀錄，依 drug_reviews.json 規則標 resolved_by_regeneration。"""
    import datetime
    f = BASE / "TwTxGNN/docs/_data/drug_reviews.json"
    d = json.loads(f.read_text(encoding="utf-8"))
    n = 0
    for r in d["records"]:
        if r.get("drug") not in pages or r.get("status") in ("resolved_by_regeneration", "withdrawn", "resolved_by_program", "superseded"):
            continue
        notes = (BASE / "TwTxGNN/data/notes" / r["drug"] / "drug_pharmacist_notes.md").read_text(encoding="utf-8")
        probe = [x for x in (r.get("anchor"), r.get("claim"), r.get("replacement")) if x]
        if not any(x in notes for x in probe):
            r["status"] = "resolved_by_regeneration"
            r["resolved_on"] = datetime.date.today().isoformat()
            r["resolved_note"] = "2026-10-22 本頁改寫為已知用途頁（模型候選全部屬已知用途，無新預測），原句與原等級已不存在。"
            n += 1
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")  # 原檔 indent=1
    print(f"Tw 查核紀錄標 resolved_by_regeneration：{n} 筆", flush=True)


def main(argv):
    if "--list" in argv:
        items = [tuple(x.split(":")) for x in argv[argv.index("--list") + 1].split(",")]
    elif "--no-pred" in argv:
        with open(BASE / ".claude/audit_20261016/no_prediction_099.tsv", encoding="utf-8") as f:
            items = [(r["site"], r["page"]) for r in csv.DictReader(f, delimiter="\t") if r["action"].startswith("保留收錄")]
    else:
        with open(BASE / ".claude/audit_20261016/track4/all_known.tsv", encoding="utf-8") as f:
            items = [(r["site"], r["page"]) for r in csv.DictReader(f, delimiter="\t")]
    if "--part" in argv:
        i, n = map(int, argv[argv.index("--part") + 1].split("/")); items = items[i::n]
    dry = "--dry" in argv
    ok = {}
    for s, pg in items:
        t0 = time.time()
        try:
            errs, out = run(s, pg, dry)
        except Exception as e:
            errs, out = [f"例外：{str(e)[:120]}"], ""
        if dry or errs:
            d = BASE / ".claude/cache/known_use_pages_out" / s; d.mkdir(parents=True, exist_ok=True)
            (d / f"{pg}.md").write_text(out, encoding="utf-8")
        with open(RES, "a", encoding="utf-8") as f:
            f.write(f"{s}\t{pg}\t{'OK' if not errs else 'FAIL'}\t{'；'.join(errs)}\t{time.time() - t0:.0f}\n")
        print(f"{'✓' if not errs else '✗'} {s}:{pg} ({time.time() - t0:.0f}s) {'；'.join(errs)[:150]}", flush=True)
        if not errs and not dry:
            ok.setdefault(s, []).append(pg)
    if "TwTxGNN" in ok:
        resolve_tw_reviews(ok["TwTxGNN"])
    for s, ds in ok.items():
        r = subprocess.run(["uv", "run", "python", "scripts/sync_notes_to_docs.py"], cwd=BASE / s,
                           env=dict(os.environ, SYNC_ONLY=",".join(ds)), capture_output=True, text=True)
        print(f"sync {s}: {len(ds)} 頁 {'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[-150:]}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
