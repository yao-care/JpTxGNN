#!/usr/bin/env python3
"""Generate search-index.json from repurposing candidates

This script creates a search index for the docs site and FHIR resource generation.
"""

import json
import re
from pathlib import Path

import pandas as pd


def slugify(text: str) -> str:
    """Convert text to URL-safe slug"""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def main():
    print("=" * 60)
    print("Generate search-index.json from repurposing candidates")
    print("=" * 60)

    project_root = Path(__file__).parent.parent
    candidates_file = project_root / "data" / "processed" / "repurposing_candidates.csv"
    output_dir = project_root / "docs" / "data"
    output_file = output_dir / "search-index.json"

    if not candidates_file.exists():
        print(f"Error: Candidates file not found: {candidates_file}")
        print("Run: uv run python scripts/run_kg_prediction.py")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    # Load candidates
    df = pd.read_csv(candidates_file)
    print(f"Loaded {len(df)} candidates")

    # Group by drug
    drugs_data = []

    # Detect column names (Taiwan vs Japan)
    license_col = "承認番号" if "承認番号" in df.columns else "許可證字號"
    name_col = "販売名" if "販売名" in df.columns else "中文品名"

    for (license_id, name), group in df.groupby([license_col, name_col]):
        drug_name = group["藥物成分"].iloc[0]
        drug_slug = slugify(drug_name)

        # Get all indications for this drug
        indications = []
        for _, row in group.iterrows():
            ind_name = row["潛在新適應症"]
            indications.append({
                "name": ind_name,
                "slug": slugify(ind_name),
                "source": row.get("來源", "TxGNN Knowledge Graph"),
                "score": 50,  # Default score
                "level": "L5",  # Evidence level (predicted)
            })

        # Remove duplicates
        seen = set()
        unique_indications = []
        for ind in indications:
            if ind["name"] not in seen:
                seen.add(ind["name"])
                unique_indications.append(ind)

        drugs_data.append({
            "license_id": str(license_id),
            "name": str(name),
            "slug": drug_slug,
            "drugbank_id": group["drugbank_id"].iloc[0] if "drugbank_id" in group.columns else None,
            "original": "",  # No original indication from SSK data
            "brands": [],
            "indications": unique_indications,
        })

    print(f"Grouped into {len(drugs_data)} drugs")

    # Create search index
    search_index = {
        "version": "1.0",
        "generated": pd.Timestamp.now().isoformat(),
        "drugs": drugs_data,
        "stats": {
            "total_drugs": len(drugs_data),
            "total_indications": sum(len(d["indications"]) for d in drugs_data),
        }
    }

    # Save
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)

    print(f"Generated: {output_file}")
    print(f"  - {search_index['stats']['total_drugs']} drugs")
    print(f"  - {search_index['stats']['total_indications']} indications")


if __name__ == "__main__":
    main()
