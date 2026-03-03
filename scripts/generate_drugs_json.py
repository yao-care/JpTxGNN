#!/usr/bin/env python3
"""
Generate drugs.json for the website.

Aggregates drug information from:
- jp_fda_drugs.json (merged SSK + KEGG data)
- repurposing_candidates.csv (KG predictions)

Output: docs/data/drugs.json
"""

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import pandas as pd

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DATA_DIR = PROJECT_ROOT / "docs" / "data"


def load_fda_drugs() -> dict:
    """Load FDA drugs data as a dictionary keyed by approval number."""
    fda_path = DATA_DIR / "raw" / "jp_fda_drugs.json"
    with open(fda_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Index by approval number
    drugs_by_id = {}
    for drug in data:
        approval_no = drug.get("承認番号", "")
        if approval_no:
            drugs_by_id[approval_no] = drug

    return drugs_by_id


def load_repurposing_candidates() -> pd.DataFrame:
    """Load repurposing candidates."""
    candidates_path = DATA_DIR / "processed" / "repurposing_candidates.csv"
    return pd.read_csv(candidates_path)


def extract_original_indication(kegg_indication: str) -> str:
    """Extract clean indication text from KEGG format."""
    if not kegg_indication:
        return ""

    # KEGG format: "Category\n疾患        Disease1 [DS:xxx]\nDisease2 [DS:xxx]"
    # Extract disease names
    lines = kegg_indication.split("\n")
    diseases = []

    for line in lines:
        # Skip category lines
        if not line.strip() or "受容体" in line or "薬" in line:
            continue

        # Remove KEGG disease codes [DS:xxx]
        clean = re.sub(r'\[DS:[^\]]+\]', '', line)
        # Remove leading whitespace and "疾患" prefix
        clean = re.sub(r'^疾患\s*', '', clean.strip())
        clean = clean.strip()

        if clean and len(clean) >= 2:
            diseases.append(clean)

    return "、".join(diseases) if diseases else ""


def slugify(name: str) -> str:
    """Convert drug name to URL slug."""
    # Use lowercase English name
    slug = name.lower()
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Remove special characters
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    # Remove multiple hyphens
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')


def main():
    print("Loading data...")

    # Load data
    fda_drugs = load_fda_drugs()
    candidates_df = load_repurposing_candidates()

    print(f"  - FDA drugs: {len(fda_drugs)}")
    print(f"  - Repurposing candidates: {len(candidates_df)}")

    # Group candidates by drug (using drugbank_id as key)
    drugs_data = defaultdict(lambda: {
        "indications": [],
        "approval_numbers": set(),
        "brand_names": set(),
        "ingredient": "",
        "drugbank_id": "",
        "original_indication": "",
    })

    for _, row in candidates_df.iterrows():
        drugbank_id = row.get("drugbank_id", "")
        if not drugbank_id:
            continue

        ingredient = row.get("藥物成分", "")
        slug = slugify(ingredient)

        if not slug:
            continue

        drug = drugs_data[slug]
        drug["ingredient"] = ingredient
        drug["drugbank_id"] = drugbank_id
        drug["indications"].append(row.get("潛在新適應症", ""))
        # Convert approval number to string
        approval_no = str(row.get("承認番号", ""))
        drug["approval_numbers"].add(approval_no)
        drug["brand_names"].add(row.get("販売名", ""))

    print(f"  - Unique drugs: {len(drugs_data)}")

    # Build final drugs list
    drugs_list = []

    for slug, drug_info in sorted(drugs_data.items()):
        # Get original indication from FDA data
        original_indication = ""
        for approval_no in drug_info["approval_numbers"]:
            if approval_no in fda_drugs:
                fda_drug = fda_drugs[approval_no]
                kegg_indication = fda_drug.get("効能・効果", "")
                original_indication = extract_original_indication(kegg_indication)
                if original_indication:
                    break

        # Get unique indications
        unique_indications = list(set(drug_info["indications"]))

        # Format predicted indications (top 3 for display)
        predicted_display = "、".join(unique_indications[:3])
        if len(unique_indications) > 3:
            predicted_display += f"（他 {len(unique_indications) - 3} 件）"

        # Get brand names (top 3)
        brand_names = sorted(drug_info["brand_names"])[:3]

        drugs_list.append({
            "slug": slug,
            "name": drug_info["ingredient"],
            "drugbank_id": drug_info["drugbank_id"],
            "evidence_level": "L5",  # All predictions are computational
            "indication_count": len(unique_indications),
            "original_indication": original_indication,
            "predicted_indication": predicted_display,
            "brand_names": brand_names,
            "japan_approved": True,
            "url": f"/drugs/{slug}/"
        })

    # Sort by indication count (descending)
    drugs_list.sort(key=lambda x: x["indication_count"], reverse=True)

    # Output
    output = {
        "generated": datetime.now().strftime("%Y-%m-%d"),
        "total_count": len(drugs_list),
        "source": "JpTxGNN - https://jptxgnn.yao.care/",
        "drugs": drugs_list
    }

    # Ensure output directory exists
    DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = DOCS_DATA_DIR / "drugs.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nOutput: {output_path}")
    print(f"  - Total drugs: {len(drugs_list)}")
    print(f"  - With original indication: {sum(1 for d in drugs_list if d['original_indication'])}")

    # Show top 5 drugs by indication count
    print("\nTop 5 drugs by indication count:")
    for drug in drugs_list[:5]:
        print(f"  - {drug['name']}: {drug['indication_count']} indications")


if __name__ == "__main__":
    main()
