#!/usr/bin/env python3
"""
Generate data exports for downloads page.

Creates public data files:
- docs/data/repurposing_candidates.csv
- docs/data/drugs.json (already created)
- docs/data/search-index.json (already created)

Output: docs/data/
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DATA_DIR = PROJECT_ROOT / "docs" / "data"


def export_repurposing_candidates():
    """Export repurposing candidates CSV to docs/data."""
    source_path = DATA_DIR / "processed" / "repurposing_candidates.csv"
    dest_path = DOCS_DATA_DIR / "repurposing_candidates.csv"

    if not source_path.exists():
        print(f"  警告: {source_path} が見つかりません")
        return 0

    # Read and clean up the CSV
    df = pd.read_csv(source_path)

    # Select and rename columns for public export
    export_cols = {
        "承認番号": "approval_number",
        "販売名": "brand_name",
        "藥物成分": "ingredient",
        "drugbank_id": "drugbank_id",
        "潛在新適應症": "predicted_indication",
        "來源": "source",
    }

    # Filter to existing columns
    existing_cols = {k: v for k, v in export_cols.items() if k in df.columns}
    df_export = df[list(existing_cols.keys())].copy()
    df_export.columns = [existing_cols[c] for c in df_export.columns]

    # Save
    df_export.to_csv(dest_path, index=False)
    print(f"  - repurposing_candidates.csv: {len(df_export)} 行")
    return len(df_export)


def export_drug_mapping():
    """Export drug mapping CSV to docs/data."""
    source_path = DATA_DIR / "processed" / "drug_mapping.csv"
    dest_path = DOCS_DATA_DIR / "drug_mapping.csv"

    if not source_path.exists():
        print(f"  警告: {source_path} が見つかりません")
        return 0

    # Read and export
    df = pd.read_csv(source_path)

    # Select columns for public export
    export_cols = ["承認番号", "販売名", "drugbank_id", "映射成功"]
    existing_cols = [c for c in export_cols if c in df.columns]
    df_export = df[existing_cols].copy()

    # Save
    df_export.to_csv(dest_path, index=False)
    print(f"  - drug_mapping.csv: {len(df_export)} 行")
    return len(df_export)


def generate_statistics():
    """Generate statistics JSON for the website."""
    stats = {
        "generated": datetime.now().isoformat(),
        "data": {}
    }

    # Drug statistics
    drugs_path = DOCS_DATA_DIR / "drugs.json"
    if drugs_path.exists():
        with open(drugs_path, "r", encoding="utf-8") as f:
            drugs_data = json.load(f)
        stats["data"]["drugs"] = {
            "total": drugs_data.get("total_count", 0),
            "with_indication": sum(1 for d in drugs_data.get("drugs", []) if d.get("original_indication")),
        }

    # Candidates statistics
    candidates_path = DATA_DIR / "processed" / "repurposing_candidates.csv"
    if candidates_path.exists():
        df = pd.read_csv(candidates_path)
        stats["data"]["candidates"] = {
            "total": len(df),
            "unique_drugs": df["drugbank_id"].nunique() if "drugbank_id" in df.columns else 0,
            "unique_indications": df["潛在新適應症"].nunique() if "潛在新適應症" in df.columns else 0,
        }

    # Search index statistics
    search_index_path = DOCS_DATA_DIR / "search-index.json"
    if search_index_path.exists():
        with open(search_index_path, "r", encoding="utf-8") as f:
            search_data = json.load(f)
        stats["data"]["search_index"] = {
            "drugs": len(search_data.get("drugs", [])),
        }

    # News statistics
    news_index_path = DOCS_DATA_DIR / "news-index.json"
    if news_index_path.exists():
        with open(news_index_path, "r", encoding="utf-8") as f:
            news_data = json.load(f)
        stats["data"]["news"] = {
            "matched": news_data.get("count", 0),
        }

    # Save statistics
    stats_path = DOCS_DATA_DIR / "statistics.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"  - statistics.json: 生成完了")
    return stats


def main():
    print("データエクスポートを生成中...")

    # Ensure output directory exists
    DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Export files
    print("\nファイルをエクスポート:")
    candidates_count = export_repurposing_candidates()
    mapping_count = export_drug_mapping()

    # Generate statistics
    print("\n統計を生成:")
    stats = generate_statistics()

    # Summary
    print("\n完了！")
    print(f"  出力ディレクトリ: {DOCS_DATA_DIR}")
    print(f"  リポジショニング候補: {candidates_count} 行")
    print(f"  薬物マッピング: {mapping_count} 行")


if __name__ == "__main__":
    main()
