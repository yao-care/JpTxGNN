"""藥物頁 meta description 與 title（2026-10-16，SEO 稽核 #4）。

description：用頁面第一張摘要表（第 1 列＝原適應症、第 2 列＝預測新適應症）加上 front matter 的
evidence_level，以該站語言組成一句，最長約 160 字元。已有 description 的頁不動；轉址頁、noindex 頁不寫。
title：全大寫的藥名（PIMOZIDE、EZETIMIBA）改成首字大寫；縮寫 HCl 等保留。

用法：python3 .claude/drug_meta_description.py [站 ...]
"""
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
    sites = argv or [p.name for p in sorted(BASE.glob("*TxGNN"))]
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


if __name__ == "__main__":
    main(sys.argv[1:])
