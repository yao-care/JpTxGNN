#!/usr/bin/env python3
"""Generate search-index.json from repurposing candidates

This script creates a search index for the docs site and FHIR resource generation.
Integrates both KG predictions and DL predictions.
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


def load_dl_predictions(dl_file: Path) -> dict:
    """Load DL predictions and create a lookup dictionary.

    Returns:
        dict: {drugbank_id: {disease_name: score}}
    """
    if not dl_file.exists():
        print(f"DL predictions not found: {dl_file}")
        return {}

    df = pd.read_csv(dl_file)
    print(f"Loaded {len(df)} DL predictions")

    # Create lookup: {drugbank_id: {disease: score}}
    dl_lookup = {}
    for _, row in df.iterrows():
        db_id = row["drugbank_id"]
        disease = row["潛在新適應症"]
        score = row["txgnn_score"]

        if db_id not in dl_lookup:
            dl_lookup[db_id] = {}
        dl_lookup[db_id][disease] = score

    return dl_lookup


def main():
    print("=" * 60)
    print("Generate search-index.json (KG + DL predictions)")
    print("=" * 60)

    project_root = Path(__file__).parent.parent
    kg_file = project_root / "data" / "processed" / "repurposing_candidates.csv"
    dl_file = project_root / "data" / "processed" / "txgnn_dl_predictions.csv"
    output_dir = project_root / "docs" / "data"
    output_file = output_dir / "search-index.json"

    if not kg_file.exists():
        print(f"Error: KG candidates file not found: {kg_file}")
        print("Run: uv run python scripts/run_kg_prediction.py")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    # Load KG candidates
    df_kg = pd.read_csv(kg_file)
    print(f"Loaded {len(df_kg)} KG candidates")

    # Load DL predictions
    dl_lookup = load_dl_predictions(dl_file)
    dl_drug_count = len(dl_lookup)
    dl_total_predictions = sum(len(v) for v in dl_lookup.values())
    print(f"DL predictions: {dl_drug_count} drugs, {dl_total_predictions} disease pairs")

    # Detect column names (Taiwan vs Japan)
    license_col = "承認番号" if "承認番号" in df_kg.columns else "許可證字號"
    name_col = "販売名" if "販売名" in df_kg.columns else "中文品名"

    # Group by drug
    drugs_data = []
    total_dl_enhanced = 0
    total_dl_only = 0

    for (license_id, name), group in df_kg.groupby([license_col, name_col]):
        drug_name = group["藥物成分"].iloc[0]
        drug_slug = slugify(drug_name)
        drugbank_id = group["drugbank_id"].iloc[0] if "drugbank_id" in group.columns else None

        # Get DL predictions for this drug
        dl_diseases = dl_lookup.get(drugbank_id, {}) if drugbank_id else {}

        # Build indications from KG predictions
        indications = []
        kg_diseases = set()

        for _, row in group.iterrows():
            ind_name = row["潛在新適應症"]
            kg_diseases.add(ind_name)

            # Check if we have DL score for this indication
            dl_score = dl_diseases.get(ind_name)

            if dl_score is not None:
                # Use DL score (convert to 0-100 scale)
                score = int(dl_score * 100)
                source = "TxGNN Deep Learning Model"
                total_dl_enhanced += 1
            else:
                # KG prediction only
                score = 50  # Default score for KG
                source = row.get("來源", "TxGNN Knowledge Graph")

            indications.append({
                "name": ind_name,
                "slug": slugify(ind_name),
                "source": source,
                "score": score,
                "level": "L5",  # Evidence level (predicted)
            })

        # Add DL-only predictions (not in KG) - high confidence only
        for disease, dl_score in dl_diseases.items():
            if disease not in kg_diseases:
                # Only include very high-confidence DL predictions (>= 90%)
                if dl_score >= 0.9:
                    indications.append({
                        "name": disease,
                        "slug": slugify(disease),
                        "source": "TxGNN Deep Learning Model",
                        "score": int(dl_score * 100),
                        "level": "L5",
                    })
                    total_dl_only += 1

        # Remove duplicates and sort by score, limit to top 100 per drug
        seen = set()
        unique_indications = []
        for ind in sorted(indications, key=lambda x: -x["score"]):
            if ind["name"] not in seen:
                seen.add(ind["name"])
                unique_indications.append(ind)
                if len(unique_indications) >= 100:  # Limit per drug
                    break

        drugs_data.append({
            "license_id": str(license_id),
            "name": str(name),
            "slug": drug_slug,
            "drugbank_id": drugbank_id,
            "original": "",  # No original indication from SSK data
            "brands": [],
            "indications": unique_indications,
        })

    print(f"\nGrouped into {len(drugs_data)} drugs")
    print(f"DL-enhanced KG predictions: {total_dl_enhanced}")
    print(f"DL-only predictions (>=90%): {total_dl_only}")

    # Create search index
    search_index = {
        "version": "2.0",  # Version bump for DL integration
        "generated": pd.Timestamp.now().isoformat(),
        "drugs": drugs_data,
        "stats": {
            "total_drugs": len(drugs_data),
            "total_indications": sum(len(d["indications"]) for d in drugs_data),
            "kg_predictions": len(df_kg),
            "dl_enhanced": total_dl_enhanced,
            "dl_only": total_dl_only,
        }
    }

    # Save
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)

    print(f"\nGenerated: {output_file}")
    print(f"  - {search_index['stats']['total_drugs']} drugs")
    print(f"  - {search_index['stats']['total_indications']} indications")


if __name__ == "__main__":
    main()
