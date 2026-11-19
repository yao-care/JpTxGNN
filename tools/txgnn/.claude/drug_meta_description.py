"""藥物頁 meta description 與 title（2026-10-16，SEO 稽核 #4）。

description：用頁面第一張摘要表（第 1 列＝原適應症、第 2 列＝預測新適應症）加上 front matter 的
evidence_level，以該站語言組成一句，最長約 160 字元。已有 description 的頁不動；轉址頁、noindex 頁不寫。
title：全大寫的藥名（PIMOZIDE、EZETIMIBA）改成首字大寫；縮寫 HCl 等保留。

用法：python3 .claude/drug_meta_description.py [站 ...]

在地化句尾（2026-11-19 用戶決定「藥物頁簡述在地化」，見檔尾 LOCAL 一節）：
  description 句尾「原適應症：本地資料未記載」（各語言 NOT_RECORDED）沒有資訊、30 站一樣，換成本站許可證快照事實層
  （snapshots/*_licenses.json.gz，各站 src/<套件>/regulatory/licenses.py 的 snapshot()）的品項數句子，用該站語言與資料名稱。
  python3 .claude/drug_meta_description.py --check [--site 站 ...]   只檢查，有要改的 exit 1
  python3 .claude/drug_meta_description.py --apply [--site 站 ...]   改頁＋寫 docs/_data/description_local_log.json
  python3 tools/txgnn/.claude/drug_meta_description.py --check --root .   站上 gate 用（站名讀 tools/txgnn/SITE）
"""
import sys as _sys, pathlib as _pl; _sys.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import site_registry as _site_registry  # noqa: E402  # 30 站名單（不含 CnTxGNN）
import json, re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
FM = re.compile(rb"^(?:\xef\xbb\xbf)?---\r?\n(.*?)\r?\n---\r?\n", re.S)

T = {
    "en": "{title}: predicted new indication {pred} (evidence level {lv}). Approved use: {orig}",
    "zh": "{title}：預測新適應症為{pred}（證據等級 {lv}）。原適應症：{orig}",
    "ja": "{title}：予測新適応症は{pred}（エビデンスレベル {lv}）。既存適応症：{orig}",
    "ko": "{title}: 예측 신규 적응증 {pred} (근거 수준 {lv}). 기존 적응증: {orig}",
    "es": "{title}: nueva indicación predicha, {pred} (nivel de evidencia {lv}). Indicación original: {orig}",
    "pt": "{title}: nova indicação prevista, {pred} (nível de evidência {lv}). Indicação original: {orig}",
    "de": "{title}: vorhergesagte neue Indikation {pred} (Evidenzstufe {lv}). Ursprüngliche Indikation: {orig}",
    "fr": "{title} : nouvelle indication prédite, {pred} (niveau de preuve {lv}). Indication d'origine : {orig}",
    "it": "{title}: nuova indicazione prevista, {pred} (livello di evidenza {lv}). Indicazione originale: {orig}",
    "fi": "{title}: ennustettu uusi käyttöaihe {pred} (näytön taso {lv}). Alkuperäinen käyttöaihe: {orig}",
    "no": "{title}: predikert ny indikasjon {pred} (evidensnivå {lv}). Opprinnelig indikasjon: {orig}",
    "sv": "{title}: predikterad ny indikation {pred} (evidensnivå {lv}). Ursprunglig indikation: {orig}",
    "da": "{title}: forudsagt ny indikation {pred} (evidensniveau {lv}). Oprindelig indikation: {orig}",
    "nl": "{title}: voorspelde nieuwe indicatie {pred} (bewijsniveau {lv}). Oorspronkelijke indicatie: {orig}",
    "ar": "{title}: الاستطباب الجديد المتوقع {pred} (مستوى الدليل {lv}). الاستطباب الأصلي: {orig}",
    "ms": "{title}: indikasi baharu diramal {pred} (tahap bukti {lv}). Indikasi asal: {orig}",
    "th": "{title}: ข้อบ่งใช้ใหม่ที่คาดการณ์ {pred} (ระดับหลักฐาน {lv}) ข้อบ่งใช้เดิม: {orig}",
}
KEEP_UPPER = {"Hcl": "HCl", "Hbr": "HBr", "Iv": "IV", "Ii": "II", "Iii": "III", "Dna": "DNA", "Rna": "RNA"}


def site_lang(proj: Path) -> str:
    cfg = (proj / "docs/_config.yml").read_text(encoding="utf-8")
    m = re.search(r'^lang:\s*"?([A-Za-z]+)', cfg, re.M)
    code = (m.group(1) if m else "en").lower()
    return {"nb": "no"}.get(code, code)


def clean(cell: str, limit: int) -> str:
    cell = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cell)          # markdown 連結
    cell = re.sub(r"[*_`]", "", cell)
    cell = re.sub(r"^\s*(.+?)\s*[（(]\s*\1\s*[)）]\s*$", r"\1", cell, flags=re.I)  # 2026-10-27：「X (X)」英文頁重複病名 → X
    # 去掉說明性括號（資料來源、排名、證據註記），保留疾病英文名這類短括號
    cell = re.sub(r"[（(][^）)]*(資料|data|knowledge|graph|licen|registr|許可|圖譜|グラフ|그래프|ARTG|record|rank|排名|順位|순위|證據|証拠|evidence|selected|best|see |見|参照)[^）)]*[）)]", "", cell, flags=re.I)
    cell = re.sub(r"[；;].*$", "", cell)  # 分號後多半是補充說明
    cell = re.sub(r"\s+", " ", cell).strip(" ；;，,。.")
    if len(cell) > limit:
        cut = cell[:limit]
        cell = cut[: max(cut.rfind("、"), cut.rfind(","), cut.rfind("，"), cut.rfind(";"), cut.rfind("；"))] or cut
        cell = cell.rstrip(" 、,，;；") + "…"
    return cell


PRED_LABEL = re.compile(r"New Indication|新適應症|新適応症|新規適応症|Nueva Indicacion|uusi indikaatio|neue Indikation|Nova Indicação|nueva indicación|Nueva indicación|nouvelle indication|Nouvelle indication|nuova indicazione|Nuova indicazione|uusi käyttöaihe|Uusi käyttöaihe|ny indikasjon|Ny indikasjon|ny indikation|Ny indikation|nieuwe indicatie|Nieuwe indicatie|الجديد|신규 적응증|baharu|ใหม่", re.I)
ORIG_LABEL = re.compile(r"Original|Alkuperäinen indikaatio|原適應症|既存適応症|Ursprüngliche|origen|d.origine|originale|Alkuperäinen|Opprinnelig|Ursprunglig|Oprindelig|Oorspronkelijke|الأصلي|기존 적응증|asal|เดิม", re.I)
BAD_VALUE = re.compile(r"^\s*([0-9.,]+\s*%|DB\d{5}|L[1-5])", re.I)


def summary_rows(body: str):
    """依欄名找「原適應症」與「預測新適應症」兩列（2026-10-17：原本按列順序取，表格順序不同的頁會抓到分數或 DrugBank ID）。"""
    rows = re.findall(r"^\|([^|\n]+)\|([^|\n]+)\|", body, re.M)
    orig = pred = None
    for a, b in rows:
        a, b = a.strip(), b.strip()
        if pred is None and PRED_LABEL.search(a):
            pred = b
        elif orig is None and ORIG_LABEL.search(a):
            orig = b
        if orig and pred:
            break
    if not pred or BAD_VALUE.match(pred) or (orig and BAD_VALUE.match(orig)):
        return None
    return [("", orig or ""), ("", pred)]


def render(tpl: str, title: str, pred: str, lv: str, orig: str) -> str:
    """沒有原適應症時，去掉句尾的「原適應症：…」那一段。"""
    if not orig:
        tpl = re.sub(r"[.。]?\s*[^.。()（）]*\{orig\}$", "", tpl)
        tpl += "。" if re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", tpl[-3:]) else "."
    return tpl.format(title=title, pred=pred, lv=lv, orig=orig)


def nice_title(t: str) -> str:
    if t != t.upper() or not re.search(r"[A-Z]", t) or re.fullmatch(r"DB\d+", t):
        return t
    out = " ".join(w.capitalize() if not re.search(r"\d", w) else w for w in t.lower().split(" "))
    for k, v in KEEP_UPPER.items():
        out = re.sub(rf"\b{k}\b", v, out)
    return out


def main(argv):
    sites = argv or [p.name for p in sorted(_site_registry.glob_sites(BASE))]
    for s in sites:
        proj = BASE / s
        lang = site_lang(proj)
        tpl = T.get(lang, T["en"])
        nd = nt = 0
        for f in sorted((proj / "docs/_drugs").glob("*.md")):
            b = f.read_bytes()
            m = FM.match(b)
            if not m or b'http-equiv="refresh"' in b:
                continue
            fm = m.group(1).decode("utf-8")
            if re.search(r"^noindex:\s*true", fm, re.M):
                continue
            nl = "\r\n" if b"\r\n" in b[:300] else "\n"
            lines = fm.split(nl) if nl in fm else fm.split("\n")
            changed = False
            tm = re.search(r"^title:\s*(.+?)\s*$", fm, re.M)
            title = tm.group(1).strip('"').strip("'") if tm else f.stem
            nt_ = nice_title(title)
            if nt_ != title:
                lines = [f"title: {nt_}" if l.startswith("title:") else l for l in lines]
                title, changed = nt_, True
                nt += 1
            if not re.search(r"^description:", fm, re.M):
                rows = summary_rows(b[m.end():].decode("utf-8", "replace"))
                lv = (re.search(r"^evidence_level:\s*\"?(L[1-5])", fm, re.M) or [None, ""])[1]
                if rows and lv:
                    orig, pred = clean(rows[0][1], 70) if rows[0][1] else "", clean(rows[1][1], 120)
                    if pred and pred not in ("無", "None", "-", "なし"):
                        desc = render(tpl, title, pred, lv, orig)
                        if len(desc) > 200:
                            desc = desc[:199] + "…"
                        lines.append("description: " + json.dumps(desc, ensure_ascii=False))
                        changed = True
                        nd += 1
            if changed:
                f.write_bytes(b[:m.start(1)] + nl.join(lines).encode("utf-8") + b[m.end(1):])
        print(f"{s} ({lang}): description {nd}、title {nt}")




# ---------------------------------------------------------------------------------------------------------------
# LOCAL：description 句尾在地化（2026-11-19，用戶決定「藥物頁簡述在地化」）
#
# SEO 稽核：30 站藥物頁 description 很多只差藥名，句尾都是「Approved use: Not recorded in the local data」之類的同一句。
# 規則（不用 AI、不讀網路）：
#   - 只改公開藥物頁（排除 layout: id_redirect、meta refresh、noindex: true）。
#   - description 裡「<原適應症標籤><NOT_RECORDED>」（標籤取 T 模板 {orig} 前的字樣）換成 LOCAL[站](事實層) 產生的句子；
#     其他文字（藥名、預測新適應症、等級字樣）一個字不動，sync_description_levels.py 的等級字樣照舊找得到。
#   - 已有真的原適應症文字的頁不動。事實層＝快照 drugs[<頁檔名>].facts（total／valid／partial／not_marketed…，
#     跟頁面概覽表狀態列、張數列同一份，gate 第 18 項左右的 licenses.site_problems 保證一致）。
#   - 改過的頁記在 docs/_data/description_local_log.json：pages[頁]＝{tail：目前產生的句子, original：原本被換掉的字樣, date}；
#     entries 追加每次改動的前後整行（from／to，含原文，可還原）。快照變了重跑會把 description 結尾的舊 tail
#     換成新 tail（可重複執行；內容一樣就不寫檔）。
#   - --check：還有「本地資料未記載」句尾、或 tail 跟事實層重算不同的頁 → exit 1（各站 check_seo_docs.py 的 gate 項目）。
#   - Tw 不做：Tw 的 description 只能經 drug_reviews.json 的 description_level 紀錄改（TwTxGNN/CLAUDE.md）。
# ---------------------------------------------------------------------------------------------------------------
NOT_RECORDED = {
    "en": "Not recorded in the local data", "es": "No consta en los datos locales", "pt": "Não consta nos dados locais",
    "de": "In den lokalen Daten nicht erfasst", "da": "Ikke registreret i de lokale data", "fi": "Ei kirjattu paikallisiin tietoihin",
    "fr": "Non renseignée dans les données locales", "it": "Non riportata nei dati locali", "ja": "日本の承認情報に適応症の記載なし",
    "ko": "국내 허가 자료에 적응증 기재 없음", "ms": "Tidak direkodkan dalam data tempatan", "nl": "Niet vermeld in de lokale gegevens",
    "no": "Ikke registrert i de lokale dataene", "sv": "Inte angiven i de lokala uppgifterna", "th": "ไม่มีบันทึกในข้อมูลท้องถิ่น",
    "zh": "本地許可證資料未記載適應症", "ar": "غير مسجل في البيانات المحلية",
}  # 同 factlayer_20261028.py／regen_writer_20261027.py 填「原適應症」格的字樣
LOCAL_LOG = "docs/_data/description_local_log.json"
SKIP_SITES = {"TwTxGNN"}


def _pl(n, sg, pl=None):
    return f"{n} {sg if n == 1 else (pl or sg + 's')}"


def _k(fc):
    """部分紀錄（只收前 N 筆）的筆數：total 是 None 時用收到的號碼數"""
    return fc.get("total") if fc.get("total") is not None else len(fc.get("licenses") or {})


def _en(country, sg, pl=None, valid=None, nm=None, zero=None):
    """英文站：「In <country>: N <noun>s (V <valid>[, M <nm>])」；部分紀錄「at least N <noun>s」；0 筆用 zero 句"""
    def f(fc):
        n, v, m = fc.get("total") or 0, fc.get("valid") or 0, fc.get("not_marketed") or 0
        if fc.get("partial"):
            return f"In {country}: at least {_k(fc)} {pl or sg + 's'}"
        if not n:
            return f"In {country}: {zero}"
        extra = [f"{v} {valid}"] if valid else []
        if nm and m:
            extra.append(f"{m} {nm}")
        return f"In {country}: {_pl(n, sg, pl)}" + (f" ({', '.join(extra)})" if extra else "")
    return f


def _colon(prefix, valid, part, zero, nm=None, sep=": ", vsep=": ", open_="(", close=")", unit=""):
    """非英文站：「<prefix>: N[unit] (<valid>: V[; <nm>: M])」；不用單複數變化。part／zero 是整句模板（{k}）"""
    def f(fc):
        n, v, m = fc.get("total") or 0, fc.get("valid") or 0, fc.get("not_marketed") or 0
        if fc.get("partial"):
            return prefix + sep + part.format(k=_k(fc))
        if not n:
            return zero
        extra = f"{valid}{vsep}{v}"
        if nm and m:
            extra += f"; {nm}{vsep}{m}"
        return f"{prefix}{sep}{n}{unit} {open_}{extra}{close}"
    return f


def _us(fc):
    n, v, k = fc.get("total") or 0, fc.get("valid") or 0, fc.get("listed") or 0
    lst = f"{k} OTC monograph/unapproved NDC listing" + ("" if k == 1 else "s")
    if fc.get("partial"):
        return f"In the US: at least {_k(fc)} FDA applications"
    if n:
        return f"In the US: {_pl(n, 'FDA application')} ({v} active)" + (f", plus {lst}" if k else "")
    if k:
        return f"In the US: no FDA-approved application; {lst}"
    return "In the US: no FDA application or NDC listing in this data"


def _dk(fc):
    if not fc.get("partial") and not fc.get("total") and (fc.get("veterinary") or 0) > 0:
        return "I Danmark kun godkendt som veterinærlægemiddel"
    return _colon("I Danmark, markedsføringstilladelser", "gyldige", "mindst {k}",
                  "I Danmark ingen markedsføringstilladelse i disse data", nm="ikke markedsført")(fc)


def _ja(fc):
    n, v = fc.get("total") or 0, fc.get("valid") or 0
    if fc.get("partial"):
        return f"薬価基準の品目：{_k(fc)} 件以上"
    if not n:
        return "本サイトのデータに薬価基準収載品目なし"
    return f"薬価基準の品目：{n} 件（現在収載 {v} 件）"


def _zh_hk(fc):
    n, v = fc.get("total") or 0, fc.get("valid") or 0
    if not n and not fc.get("partial"):
        return "香港藥劑製品註冊：本站資料查無註冊"
    if fc.get("partial"):
        return f"香港藥劑製品註冊：至少 {_k(fc)} 張"
    return f"香港藥劑製品註冊：{n} 張（有效 {v} 張）"


def _ko(fc):
    n, v = fc.get("total") or 0, fc.get("valid") or 0
    if fc.get("partial"):
        return f"식약처 허가: 최소 {_k(fc)}건"
    if not n:
        return "식약처 허가: 본 사이트 자료에 허가 기록 없음"
    return f"식약처 허가: {n}건 (유효 {v}건)"


def _th(fc):
    n, v = fc.get("total") or 0, fc.get("valid") or 0
    if fc.get("partial"):
        return f"ทะเบียนตำรับยาในระบบของ อย.: อย่างน้อย {_k(fc)} รายการ"
    if not n:
        return "ไม่พบทะเบียนตำรับยาในระบบของ อย."
    return f"ทะเบียนตำรับยาในระบบของ อย.: {n} รายการ (ยังมีผล {v})"


def _ar_sa(fc):
    n, v = fc.get("total") or 0, fc.get("valid") or 0
    if fc.get("partial"):
        return f"المنتجات المسجلة لدى SFDA: {_k(fc)} على الأقل"
    if not n:
        return "لا توجد منتجات مسجلة لدى SFDA في هذه البيانات"
    return f"المنتجات المسجلة لدى SFDA: {n} (السارية: {v})"


# 各站資料名稱照該站 CLAUDE.md「藥物頁查核機制」的依據與概覽表狀態列的寫法（check_drug_page.py SOURCE_STATUS／SCOPE_CANCELLED）：
# AR＝PAMI 給付清單（不是 ANMAT）、AU＝PBS 品項（不是 ARTG）、UK＝NHSBSA BNF 處方代碼、NZ＝Pharmac Schedule、PH＝PNF、
# DE／FI／NO＝只有 EMA 集中許可、JP＝薬価基準（コード削除≠承認取消）、NL＝CBG、IN＝第三方整理的價格資料集。
# 清單類（UK／NZ／PH）只寫筆數，不寫「有效」（check_drug_page SOURCE_COUNT 的同一規則）。
LOCAL = {
    "ARTxGNN": _colon("En Argentina, productos en el listado de PAMI", "en el listado vigente", "al menos {k}",
                      "En Argentina, ningún producto en el listado de PAMI en estos datos"),
    "AuTxGNN": _en("Australia", "PBS item", valid="currently listed", zero="no PBS items in this data"),
    "BrTxGNN": _colon("No Brasil, registros na ANVISA", "ativos", "pelo menos {k}", "No Brasil, nenhum registro na ANVISA nestes dados"),
    "CHTxGNN": _colon("In der Schweiz, Swissmedic-Zulassungen", "gültig", "mindestens {k}",
                      "In der Schweiz keine Swissmedic-Zulassung in diesen Daten"),
    "COTxGNN": _colon("En Colombia, registros sanitarios del INVIMA", "vigentes", "al menos {k}",
                      "En Colombia, ningún registro sanitario del INVIMA en estos datos", nm="además, temporalmente no comercializados"),
    "CaTxGNN": _en("Canada", "DIN", valid="marketed", nm="dormant", zero="no DIN in this data"),
    "DETxGNN": _colon("Zentrale EU-Zulassungen (EMA)", "gültig", "mindestens {k}", "Keine zentrale EU-Zulassung (EMA) erfasst"),  # 0 筆＝頁面狀態列 NO_CENTRAL 的寫法
    "DkTxGNN": _dk,
    "ESTxGNN": _colon("En España, autorizaciones de la AEMPS", "comercializadas", "al menos {k}",
                      "En España, ninguna autorización de la AEMPS en estos datos", nm="autorizadas no comercializadas"),
    "EuTxGNN": _en("the EU", "EMA central authorisation", valid="valid", zero="no EMA central authorisation on record"),
    "FITxGNN": _colon("Keskitetyt EU-myyntiluvat (EMA)", "voimassa", "vähintään {k}", "Ei keskitettyä EU-myyntilupaa (EMA) näissä tiedoissa"),
    "FRTxGNN": _colon("En France, AMM dans la BDPM", "valides", "au moins {k}", "En France, aucune AMM dans la BDPM pour ces données",
                      sep=" : ", vsep=" : "),
    "HkTxGNN": _zh_hk,
    "ITTxGNN": _colon("In Italia, confezioni AIFA", "autorizzate", "almeno {k}", "In Italia, nessuna confezione AIFA in questi dati"),
    "InTxGNN": _en("India", "listed product", valid="not discontinued", zero="no listed product in this data"),
    "JpTxGNN": _ja,
    "KrTxGNN": _ko,
    "MyTxGNN": _colon("Di Malaysia, pendaftaran NPRA", "sah", "sekurang-kurangnya {k}", "Di Malaysia, tiada pendaftaran NPRA dalam data ini"),
    "NOTxGNN": _colon("Sentrale EU-godkjenninger (EMA)", "gyldige", "minst {k}", "Ingen sentral EU-godkjenning (EMA) i disse dataene"),
    "NZTxGNN": _en("New Zealand", "Pharmac Schedule item", zero="not on the Pharmac Schedule in this data"),
    "NlTxGNN": _colon("In Nederland, CBG-vergunningen", "geldig", "minstens {k}", "In Nederland geen CBG-vergunning in deze gegevens"),
    "PhTxGNN": _en("the Philippines", "PNF entry", "PNF entries", zero="not in the Philippine National Formulary in this data"),
    "SATxGNN": _ar_sa,
    "SETxGNN": _colon("I Sverige, godkännanden (Läkemedelsverket)", "giltiga", "minst {k}",
                      "I Sverige inget godkännande (Läkemedelsverket) i dessa uppgifter"),
    "SgTxGNN": _en("Singapore", "HSA registration", valid="valid", zero="not in the current HSA register"),
    "ThTxGNN": _th,
    "UkTxGNN": _en("the UK", "NHSBSA BNF presentation code", zero="no NHSBSA BNF presentation code in this data"),
    "UsTxGNN": _us,
    "ZaTxGNN": _en("South Africa", "SAHPRA registration", valid="valid", zero="no SAHPRA registration in this data"),
}


def _site_lang_code(root: Path) -> str:
    code = site_lang(root)
    return code if code in NOT_RECORDED else code.split("-")[0] if code.split("-")[0] in NOT_RECORDED else "en"


def _orig_label(lang):
    m = re.search(r"\{lv\}[)）][.。]?\s*(.*)\{orig\}$", T.get(lang, T["en"]))
    return m.group(1).strip() if m else ""


def _snapshot(root: Path) -> dict:
    """事實層：先用本站 src/<套件>/regulatory/licenses.py 的 snapshot()，載不到就直接讀 snapshots/*_licenses.json.gz"""
    import gzip, importlib.util as iu
    for lp in sorted(root.glob("src/*/regulatory/licenses.py")):
        try:
            spec = iu.spec_from_file_location(f"_lic_{root.name}", lp)
            mod = iu.module_from_spec(spec)
            spec.loader.exec_module(mod)
            d = mod.snapshot()
            if d:
                return d.get("drugs") or {}
        except Exception:  # noqa: BLE001 — 退回直接讀快照
            pass
    for sp in sorted(root.glob("snapshots/*_licenses.json.gz")):
        return (json.loads(gzip.open(sp).read().decode("utf-8")).get("drugs") or {})
    return {}


def _public(text: str):
    """(front matter, 是否公開頁)"""
    m = re.match(r"(?:﻿)?---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return None, False
    fm = m.group(1)
    if 'http-equiv="refresh"' in text or re.search(r"^layout:\s*id_redirect\b", fm, re.M) or re.search(r"^noindex:\s*true", fm, re.M):
        return fm, False
    return fm, True


def _esc(s):
    """description 都是雙引號 YAML／JSON 字串；tail 本身不含引號與反斜線，保險起見照 JSON 跳脫"""
    return json.dumps(s, ensure_ascii=False)[1:-1]


def localize_site(root: Path, site: str, apply: bool):
    """回傳 (要改的頁 [(頁, 舊 description, 新 description)], 問題 [字串])"""
    from datetime import date
    gen = LOCAL.get(site)
    if not gen or site in SKIP_SITES:
        return [], []
    lang = _site_lang_code(root)
    nr, label = NOT_RECORDED[lang], _orig_label(lang)
    pat = re.compile(r"(?:" + re.escape(_esc(label)) + r"\s*)?" + re.escape(_esc(nr)))
    snap = _snapshot(root)
    log_p = root / LOCAL_LOG
    log = json.loads(log_p.read_text(encoding="utf-8")) if log_p.exists() else {
        "_note": "藥物頁 front matter description 句尾「原適應症：本地資料未記載」換成本站許可證快照事實層品項數的紀錄（母目錄 "
                 ".claude/drug_meta_description.py --apply，2026-11-19 起）。pages＝目前產生的句尾（tail）與被換掉的原字樣（original）；"
                 "entries＝每次改動的前後整行（from／to，可還原：把第一筆的 from 寫回該頁 description）。",
        "pages": {}, "entries": []}
    pages_log = log.setdefault("pages", {})
    today = date.today().isoformat()
    changes, problems = [], []
    for f in sorted((root / "docs/_drugs").glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm, pub = _public(text)
        if not pub:
            continue
        dm_ = re.search(r"^description:[ \t]*(.*)$", fm, re.M)
        if not dm_:
            continue
        line = dm_.group(1).rstrip("\r")
        prev = pages_log.get(f.stem)
        fc = ((snap.get(f.stem) or {}).get("facts")) or None
        hit = pat.search(line)
        if hit:
            if fc is None:
                problems.append(f"{f.stem}：description 句尾是「{nr}」，快照沒有這個藥的事實層")
                continue
            tail = gen(fc)
            new_line = line[:hit.start()] + _esc(tail) + line[hit.end():]
            original = hit.group(0)
        elif prev and _esc(prev["tail"]) in line:
            if fc is None:
                problems.append(f"{f.stem}：快照沒有這個藥的事實層（description 句尾是先前產生的「{prev['tail']}」）")
                continue
            tail = gen(fc)
            if tail == prev["tail"]:
                continue
            i = line.rfind(_esc(prev["tail"]))
            new_line = line[:i] + _esc(tail) + line[i + len(_esc(prev["tail"])):]
            original = prev.get("original")
        else:
            continue
        if new_line == line:
            continue
        changes.append((f.stem, line, new_line))
        if apply:
            a = text.find(dm_.group(0))
            f.write_text(text[:a] + "description: " + new_line + text[a + len(dm_.group(0).rstrip("\r")):], encoding="utf-8")
            pages_log[f.stem] = {"tail": tail, "original": prev.get("original", original) if prev else original, "date": today}
            log.setdefault("entries", []).append({"page": f"docs/_drugs/{f.name}", "date": today, "from": line, "to": new_line,
                                                  "tool": ".claude/drug_meta_description.py --apply"})
    if apply and changes:
        log_p.parent.mkdir(parents=True, exist_ok=True)
        log["pages"] = dict(sorted(pages_log.items()))
        log_p.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changes, problems


def localize_main(argv):
    apply = "--apply" in argv
    roots = []
    if "--root" in argv:
        r = Path(argv[argv.index("--root") + 1]).resolve()
        sf = r / "tools/txgnn/SITE"
        roots = [(r, sf.read_text(encoding="utf-8").strip() if sf.exists() else r.name)]
    else:
        names = [a for a in argv[argv.index("--site") + 1:] if not a.startswith("--")] if "--site" in argv else []
        names = names or [p.name for p in sorted(_site_registry.glob_sites(BASE))]
        roots = [(BASE / s, s) for s in names]
    bad = 0
    for root, site in roots:
        ch, pr = localize_site(root, site, apply)
        if site in SKIP_SITES or site not in LOCAL:
            print(f"{site}: 不做（{'description 只經 drug_reviews.json 改' if site in SKIP_SITES else '沒有 LOCAL 設定'}）")
            continue
        verb = "已改" if apply else "要改"
        print(f"{site}: {verb} {len(ch)} 頁" + (f"，問題 {len(pr)}" if pr else ""))
        for stem, a, b in ch[: (0 if apply else 3)]:
            print(f"   {stem}\n     - {a}\n     + {b}")
        for p in pr[:5]:
            print("   ⚠ " + p)
        if (ch and not apply) or pr:
            bad += 1
    if not apply and bad:
        print("修法：母目錄 python3 .claude/drug_meta_description.py --apply --site <站>（description 句尾依 snapshots/*_licenses.json.gz 事實層重算）")
    sys.exit(1 if (bad and not apply) else 0)


if __name__ == "__main__":
    if any(a in sys.argv for a in ("--check", "--apply")):
        localize_main(sys.argv[1:])
    else:
        main(sys.argv[1:])
