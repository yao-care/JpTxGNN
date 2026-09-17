#!/usr/bin/env python3
"""Sync notes from data/notes/ to docs/_drugs/ for Jekyll.

This script reads pharmacist notes and creates Jekyll-compatible drug pages
with proper front matter for the documentation site.

Localization: UI strings come from LANG_BY_PROJECT + STRINGS; the evidence-tier
parent titles are read from the station's own docs/evidence-{high,medium,low}.md
so the front matter always matches an existing Jekyll parent page.

Usage:
    uv run python scripts/sync_notes_to_docs.py
"""

import json
import re
from pathlib import Path


LANG_BY_PROJECT = {
    "ARTxGNN": "es", "AuTxGNN": "en", "BrTxGNN": "pt", "CaTxGNN": "en",
    "CHTxGNN": "de", "COTxGNN": "es", "DETxGNN": "de", "DkTxGNN": "da",
    "ESTxGNN": "es", "EuTxGNN": "en", "FITxGNN": "fi", "FRTxGNN": "fr",
    "HkTxGNN": "zh", "InTxGNN": "en", "ITTxGNN": "it", "JpTxGNN": "ja",
    "KrTxGNN": "ko", "MyTxGNN": "ms", "NlTxGNN": "nl", "NOTxGNN": "no",
    "NZTxGNN": "en", "PhTxGNN": "en", "SATxGNN": "ar", "SETxGNN": "sv",
    "SgTxGNN": "en", "ThTxGNN": "th", "TwTxGNN": "zh", "UkTxGNN": "en",
    "UsTxGNN": "en", "ZaTxGNN": "en",
}

STRINGS = {
    "en": {"evidence": "Evidence Level", "indications": "Predicted Indications",
           "unit": "", "toc": "Table of Contents", "report": "Pharmacist Assessment Report"},
    "zh": {"evidence": "證據等級", "indications": "預測適應症",
           "unit": "個", "toc": "目錄", "report": "藥師評估報告"},
    "es": {"evidence": "Nivel de evidencia", "indications": "Indicaciones predichas",
           "unit": "", "toc": "Índice", "report": "Informe de evaluación farmacéutica"},
    "pt": {"evidence": "Nível de evidência", "indications": "Indicações previstas",
           "unit": "", "toc": "Índice", "report": "Relatório de avaliação farmacêutica"},
    "de": {"evidence": "Evidenzniveau", "indications": "Vorhergesagte Indikationen",
           "unit": "", "toc": "Inhaltsverzeichnis", "report": "Pharmazeutischer Bewertungsbericht"},
    "da": {"evidence": "Evidensniveau", "indications": "Forudsagte indikationer",
           "unit": "stk.", "toc": "Indholdsfortegnelse", "report": "Farmaceutens vurderingsrapport"},
    "fi": {"evidence": "Näytön taso", "indications": "Ennustetut käyttöaiheet",
           "unit": "kpl", "toc": "Sisällysluettelo", "report": "Farmaseutin arviointiraportti"},
    "fr": {"evidence": "Niveau de preuve", "indications": "Indications prédites",
           "unit": "", "toc": "Table des matières", "report": "Rapport d'évaluation pharmaceutique"},
    "it": {"evidence": "Livello di evidenza", "indications": "Indicazioni previste",
           "unit": "", "toc": "Indice", "report": "Relazione di valutazione farmaceutica"},
    "ja": {"evidence": "エビデンスレベル", "indications": "予測適応症",
           "unit": "件", "toc": "目次", "report": "薬剤師評価レポート"},
    "ko": {"evidence": "근거 수준", "indications": "예측 적응증",
           "unit": "건", "toc": "목차", "report": "약사 평가 보고서"},
    "ms": {"evidence": "Tahap bukti", "indications": "Indikasi diramal",
           "unit": "", "toc": "Isi kandungan", "report": "Laporan penilaian ahli farmasi"},
    "nl": {"evidence": "Bewijsniveau", "indications": "Voorspelde indicaties",
           "unit": "", "toc": "Inhoudsopgave", "report": "Farmaceutisch beoordelingsrapport"},
    "no": {"evidence": "Evidensnivå", "indications": "Predikerte indikasjoner",
           "unit": "stk.", "toc": "Innholdsfortegnelse", "report": "Farmasøytens vurderingsrapport"},
    "sv": {"evidence": "Evidensnivå", "indications": "Förutsagda indikationer",
           "unit": "st", "toc": "Innehållsförteckning", "report": "Apotekarens bedömningsrapport"},
    "ar": {"evidence": "مستوى الأدلة", "indications": "دواعي الاستعمال المتوقعة",
           "unit": "", "toc": "جدول المحتويات", "report": "تقرير التقييم الصيدلاني"},
    "th": {"evidence": "ระดับหลักฐาน", "indications": "ข้อบ่งใช้ที่คาดการณ์",
           "unit": "รายการ", "toc": "สารบัญ", "report": "รายงานการประเมินโดยเภสัชกร"},
}

DISCLAIMERS = {
    "en": "\n## Disclaimer\n\nThis content is for research purposes only and does not constitute medical advice.\nClinical validation is required before any clinical application.\n",
    "zh": "\n## 免責聲明\n\n本內容僅供研究參考，不構成醫療建議。\n所有老藥新用預測結果需經過臨床驗證才能應用。\n",
    "es": "\n## Descargo de responsabilidad\n\nEste contenido es solo con fines de investigación y no constituye asesoramiento médico.\nSe requiere validación clínica antes de cualquier aplicación clínica.\n",
    "pt": "\n## Aviso de isenção de responsabilidade\n\nEste conteúdo é apenas para fins de pesquisa e não constitui aconselhamento médico.\nÉ necessária validação clínica antes de qualquer aplicação clínica.\n",
    "de": "\n## Haftungsausschluss\n\nDiese Inhalte dienen ausschließlich Forschungszwecken und stellen keine medizinische Beratung dar.\nVor jeder klinischen Anwendung ist eine klinische Validierung erforderlich.\n",
    "da": "\n## Ansvarsfraskrivelse\n\nDette indhold er kun til forskningsformål og udgør ikke medicinsk rådgivning.\nKlinisk validering er påkrævet før enhver klinisk anvendelse.\n",
    "fi": "\n## Vastuuvapauslauseke\n\nTämä sisältö on tarkoitettu ainoastaan tutkimuskäyttöön eikä se ole lääketieteellistä neuvontaa.\nKliininen validointi vaaditaan ennen kliinistä käyttöä.\n",
    "fr": "\n## Avertissement\n\nCe contenu est uniquement destiné à la recherche et ne constitue pas un avis médical.\nUne validation clinique est requise avant toute application clinique.\n",
    "it": "\n## Avvertenza\n\nQuesto contenuto è solo a scopo di ricerca e non costituisce un parere medico.\nÈ necessaria una validazione clinica prima di qualsiasi applicazione clinica.\n",
    "ja": "\n## 免責事項\n\n本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。\n臨床応用の前に臨床的検証が必要です。\n",
    "ko": "\n## 면책 조항\n\n본 콘텐츠는 연구 목적으로만 제공되며 의학적 조언을 구성하지 않습니다.\n임상 적용 전에 임상적 검증이 필요합니다.\n",
    "ms": "\n## Penafian\n\nKandungan ini adalah untuk tujuan penyelidikan sahaja dan bukan nasihat perubatan.\nPengesahan klinikal diperlukan sebelum sebarang aplikasi klinikal.\n",
    "nl": "\n## Disclaimer\n\nDeze inhoud is uitsluitend bedoeld voor onderzoeksdoeleinden en vormt geen medisch advies.\nKlinische validatie is vereist vóór elke klinische toepassing.\n",
    "no": "\n## Ansvarsfraskrivelse\n\nDette innholdet er kun til forskningsformål og utgjør ikke medisinsk rådgivning.\nKlinisk validering kreves før enhver klinisk anvendelse.\n",
    "sv": "\n## Ansvarsfriskrivning\n\nDetta innehåll är endast avsett för forskningsändamål och utgör inte medicinsk rådgivning.\nKlinisk validering krävs före klinisk tillämpning.\n",
    "ar": "\n## إخلاء المسؤولية\n\nهذا المحتوى لأغراض البحث فقط ولا يشكل نصيحة طبية.\nيلزم التحقق السريري قبل أي تطبيق سريري.\n",
    "th": "\n## ข้อจำกัดความรับผิดชอบ\n\nเนื้อหานี้จัดทำขึ้นเพื่อการวิจัยเท่านั้น และไม่ถือเป็นคำแนะนำทางการแพทย์\nจำเป็นต้องมีการตรวจสอบทางคลินิกก่อนนำไปใช้ทางคลินิก\n",
}

# Localized "evidence level" row labels used inside pharmacist reports.
EVIDENCE_LABELS = [s["evidence"] for s in STRINGS.values()] + [
    "Evidence Level", "Evidence level", "Nivel de Evidencia", "Evidenzlevel",
]
_LABEL_RE = re.compile(
    r"\|\s*(?:%s)\s*\|\s*(L[1-5])\s*\|" % "|".join(re.escape(x) for x in sorted(set(EVIDENCE_LABELS))),
    re.IGNORECASE,
)
# Language-agnostic fallback: any two-cell row whose second cell is just L1-L5.
_ROW_RE = re.compile(r"^\|[^|\n]{1,40}\|\s*(L[1-5])\s*\|", re.M)


def get_lang(base_dir: Path) -> str:
    return LANG_BY_PROJECT.get(base_dir.name, "en")


def extract_evidence_level(content: str) -> str:
    """Extract evidence level from note content, in any supported language."""
    match = _LABEL_RE.search(content) or _ROW_RE.search(content)
    if match:
        return match.group(1).upper()
    return "L5"


def extract_indication_count(content: str, bundle_path: Path) -> int:
    """Extract indication count from bundle or content."""
    if bundle_path.exists():
        try:
            with open(bundle_path) as f:
                bundle = json.load(f)
                if "drug" in bundle and "predicted_indications" in bundle["drug"]:
                    return len(bundle["drug"]["predicted_indications"])
        except Exception:
            pass
    return 0


def get_parent_titles(base_dir: Path) -> dict:
    """Map evidence level -> Jekyll parent page title, read from the site's own pages.

    Each station's docs/evidence-{high,medium,low}.md already carries a localized
    title; the level ranges in that title (e.g. "(L3-L4)") decide the buckets, so
    stations with a non-standard split are handled correctly.
    """
    docs = base_dir / "docs"
    defaults = {"high": ["L1", "L2"], "medium": ["L3", "L4"], "low": ["L5"]}
    titles, ranges = {}, {}
    for key, fname in (("high", "evidence-high.md"), ("medium", "evidence-medium.md"), ("low", "evidence-low.md")):
        path = docs / fname
        if not path.exists():
            continue
        m = re.search(r"^title:\s*(.+?)\s*$", path.read_text(encoding="utf-8"), re.M)
        if not m:
            continue
        title = m.group(1).strip().strip('"').strip("'")
        titles[key] = title
        found = re.findall(r"L([1-5])", title)
        if found:
            lo, hi = int(found[0]), int(found[-1])
            ranges[key] = [f"L{n}" for n in range(lo, hi + 1)]

    level_map = {}
    for key in ("high", "medium", "low"):
        if key not in titles:
            continue
        for lvl in ranges.get(key, defaults[key]):
            level_map.setdefault(lvl, titles[key])
    # Any level the site does not declare falls back to the default bucket.
    for key, levels in defaults.items():
        for lvl in levels:
            if lvl not in level_map and key in titles:
                level_map[lvl] = titles[key]
    return level_map


def sync_notes_to_docs():
    """Main sync function."""
    base_dir = Path(__file__).parent.parent
    lang = get_lang(base_dir)
    t = STRINGS.get(lang, STRINGS["en"])
    disclaimer = DISCLAIMERS.get(lang, DISCLAIMERS["en"])
    parent_titles = get_parent_titles(base_dir)

    notes_dir = base_dir / "data" / "notes"
    bundles_dir = base_dir / "data" / "bundles"
    docs_drugs_dir = base_dir / "docs" / "_drugs"
    docs_drugs_dir.mkdir(parents=True, exist_ok=True)

    drug_dirs = sorted([d for d in notes_dir.iterdir() if d.is_dir()])
    print(f"Found {len(drug_dirs)} drug directories (lang={lang})")

    synced = 0
    errors = []
    missing_parent = set()

    for i, drug_dir in enumerate(drug_dirs, 1):
        drug_name = drug_dir.name
        notes_path = drug_dir / "drug_pharmacist_notes.md"

        if not notes_path.exists():
            errors.append(f"{drug_name}: notes not found")
            continue

        content = notes_path.read_text(encoding="utf-8")
        if not content.strip():
            errors.append(f"{drug_name}: notes file is empty")
            continue

        evidence_level = extract_evidence_level(content)
        bundle_path = bundles_dir / drug_name / "drug_bundle.json"
        indication_count = extract_indication_count(content, bundle_path)
        parent = parent_titles.get(evidence_level)
        if parent is None:
            missing_parent.add(evidence_level)
            parent = evidence_level

        title = drug_name.replace("_", " ").title()

        front_matter = f"""---
layout: default
title: {title}
parent: {parent}
nav_order: {i + 10}
evidence_level: {evidence_level}
indication_count: {indication_count}
---

# {title}
{{: .fs-9 }}

{t['evidence']}: **{evidence_level}** | {t['indications']}: **{indication_count}** {t['unit']}
{{: .fs-6 .fw-300 }}

---

## {t['toc']}
{{: .no_toc .text-delta }}

1. TOC
{{:toc}}

---

<div id="pharmacist">

## {t['report']}

</div>

"""

        full_content = front_matter + content + disclaimer + "\n---\n\n"
        (docs_drugs_dir / f"{drug_name}.md").write_text(full_content, encoding="utf-8")
        synced += 1

    print(f"\n{'='*60}")
    print(f"Synced: {synced} drugs")
    print(f"Errors: {len(errors)}")
    if missing_parent:
        print(f"WARNING: no parent page for levels: {sorted(missing_parent)}")
    if errors:
        print("\nErrors:")
        for err in errors[:20]:
            print(f"  - {err}")

    level_counts = {"L1": 0, "L2": 0, "L3": 0, "L4": 0, "L5": 0}
    for drug_file in docs_drugs_dir.glob("*.md"):
        match = re.search(r"evidence_level:\s*(L[1-5])", drug_file.read_text(encoding="utf-8"))
        if match:
            level_counts[match.group(1)] += 1
    print(f"\n{'='*60}")
    print("Evidence Level Distribution:")
    for level, count in sorted(level_counts.items()):
        print(f"  {level}: {count}")


if __name__ == "__main__":
    sync_notes_to_docs()
