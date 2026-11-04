#!/usr/bin/env python3
"""
Generate data exports for downloads page.

Creates public data files:
- docs/data/repurposing_candidates.csv（downloads.md 有連結；只想更新這個檔就單獨呼叫 export_repurposing_candidates()）
- docs/data/drugs.json (already created)
- docs/data/search-index.json (already created)

Output: docs/data/
"""

from pathlib import Path

import pandas as pd

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DATA_DIR = PROJECT_ROOT / "docs" / "data"


def export_repurposing_candidates():
    """Export repurposing candidates CSV to docs/data."""
    source_path = DATA_DIR / "processed" / "repurposing_candidates.csv.gz"
    # downloads.md 連的是 /data/repurposing_candidates.csv（未壓縮）；原本寫成 .csv.gz，網站上的檔一直沒更新（2026-11-04）
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


def main():
    print("データエクスポートを生成中...")

    # Ensure output directory exists
    DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # docs/data/drug_mapping.csv と statistics.json はどのページからも参照されず、
    # 2026-03 の古いファイルのまま残っていたため 2026-11-04 に削除。ここでも生成しない。
    print("\nファイルをエクスポート:")
    candidates_count = export_repurposing_candidates()

    # Summary
    print("\n完了！")
    print(f"  出力ディレクトリ: {DOCS_DATA_DIR}")
    print(f"  リポジショニング候補: {candidates_count} 行")


if __name__ == "__main__":
    main()
