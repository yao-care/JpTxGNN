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
    slug = slugify(drug_name)

    content = f"""---
layout: drug
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
    drug_col = "drugbank_id" if "drugbank_id" in candidates.columns else candidates.columns[0]
    indication_col = "potential_indication" if "potential_indication" in candidates.columns else "disease_name"
    source_col = "source" if "source" in candidates.columns else None

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
            if "drug_ingredient" in row:
                drug_name = row["drug_ingredient"] or drug_id
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
        slug = slugify(drug_data["name"])
        page_path = DRUGS_DIR / f"{slug}.md"

        # Skip if a pharmacist report page already exists
        if page_path.exists():
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
