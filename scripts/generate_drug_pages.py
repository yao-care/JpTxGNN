#!/usr/bin/env python3
"""
Generate individual drug pages for Jekyll from repurposing predictions.

Creates markdown pages for each drug with predicted indications.

Output: docs/_drugs/{drug-slug}.md
"""

import pandas as pd
from datetime import datetime
from pathlib import Path

# Project configuration
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
DRUGS_DIR = DOCS_DIR / "_drugs"
DATA_DIR = PROJECT_ROOT / "data" / "processed"

# Country-specific settings
COUNTRY_CODE = "BR"
COUNTRY_NAME = "Brazil"
LANGUAGE = "pt-BR"
REGULATORY_AGENCY = "ANVISA"
SITE_URL = "https://artxgnn.yao.care"


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    import re
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")


def generate_drug_page(drugbank_id: str, drug_name: str, indications: list) -> str:
    """Generate markdown content for a drug page."""
    slug = slugify(drugbank_id)

    content = f"""---
layout: default
nav_exclude: true
title: {drug_name}
drugbank_id: {drugbank_id}
evidence_level: L5
permalink: /drugs/{slug}/
---

# {drug_name}

## Basic Information

| Item | Value |
|------|-------|
| DrugBank ID | [{drugbank_id}](https://go.drugbank.com/drugs/{drugbank_id}) |
| Evidence Level | L5 (Computational Prediction) |
| Number of Predicted Indications | {len(indications)} |

## Predicted Indications (TxGNN)

The following are potential new indications predicted by the TxGNN model. Higher scores indicate higher predicted relevance.

| # | Indication | Source |
|---|------------|--------|
"""

    for i, ind in enumerate(indications[:50], 1):
        ind_name = ind.get("indication", "")
        source = ind.get("source", "KG")
        content += f"| {i} | {ind_name} | {source} |\n"

    if len(indications) > 50:
        content += f"\n*(Showing top 50 of {len(indications)} predictions)*\n"

    content += f"""
## Disclaimer

These predictions are for research purposes only and do not constitute medical advice.
Clinical validation is required before any clinical application.

---

[← Back to Drug Search](/drugs/)
"""

    return content


def main():
    print("=" * 60)
    print(f"BrTxGNN - Generate Drug Pages")
    print("=" * 60)
    print()

    # Load prediction data
    candidates_path = DATA_DIR / "repurposing_candidates.csv.gz"

    if not candidates_path.exists():
        print(f"Error: {candidates_path} not found")
        print("Please run run_kg_prediction.py first")
        return

    print(f"1. Loading predictions from {candidates_path}...")
    candidates = pd.read_csv(candidates_path)
    print(f"   Loaded {len(candidates)} predictions")

    # Group by drug
    def pick(*names):
        """回傳第一個實際存在的欄名。"""
        for n in names:
            if n in candidates.columns:
                return n
        return None

    # 本站候選檔的欄名是在地化的（藥物成分／潛在新適應症／來源）。
    # 只認英文欄名時 indication 與藥名會整欄取不到值，頁面就會變成
    # title 只有 DrugBank ID、適應症欄全空。
    drug_col = pick("drugbank_id") or candidates.columns[0]
    indication_col = pick("potential_indication", "潛在新適應症", "disease_name")
    source_col = pick("source", "來源")
    ingredient_col = pick("drug_ingredient", "藥物成分")

    print()
    print("2. Grouping by drug...")
    drugs = {}
    for _, row in candidates.iterrows():
        drug_id = row.get(drug_col, "")
        if pd.isna(drug_id):
            continue
        drug_id = str(drug_id)

        if drug_id not in drugs:
            # Try to get drug name from ingredient column
            drug_name = drug_id
            if ingredient_col:
                val = row.get(ingredient_col)
                if pd.notna(val) and str(val).strip():
                    drug_name = str(val).strip().title()
            drugs[drug_id] = {
                "name": drug_name,
                "indications": []
            }

        indication = row.get(indication_col, "")
        if pd.isna(indication):
            continue

        source = row.get(source_col, "KG") if source_col else "KG"
        drugs[drug_id]["indications"].append({
            "indication": str(indication),
            "source": str(source) if not pd.isna(source) else "KG"
        })

    print(f"   Found {len(drugs)} unique drugs")

    # Create output directory
    DRUGS_DIR.mkdir(parents=True, exist_ok=True)

    print()
    print("3. Generating drug pages...")
    pages_created = 0
    skipped = 0
    for drug_id, drug_data in drugs.items():
        slug = slugify(drug_id)
        page_path = DRUGS_DIR / f"{slug}.md"

        # Skip if a pharmacist report page already exists.
        # 只有實際含藥師報告的頁面要保護；純粹由本腳本產出的舊頁必須能被覆蓋，
        # 否則修好生成器也重跑不掉既有的錯誤內容。
        if page_path.exists():
            existing = page_path.read_text(encoding="utf-8")
            if "pharmacist" in existing or "藥師評估報告" in existing:
                skipped += 1
                continue

        content = generate_drug_page(drug_id, drug_data["name"], drug_data["indications"])
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(content)
        pages_created += 1

    print(f"   Created {pages_created} drug pages (skipped {skipped} existing)")
    print()
    print("=" * 60)
    print("Done!")
    print(f"Output: {DRUGS_DIR}")


if __name__ == "__main__":
    main()
