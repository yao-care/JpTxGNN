#!/usr/bin/env python3
"""知識グラフ手法 - 医薬品リポジショニング予測

TxGNN 知識グラフを使用した薬物-疾病関係予測。
高速で、深層学習環境不要。

使用方法:
    uv run python scripts/run_kg_prediction.py
"""

import sys
from pathlib import Path

# src をパスに追加
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from jptxgnn.data import load_fda_drugs, filter_active_drugs
from jptxgnn.mapping import (
    map_fda_drugs_to_drugbank,
    map_fda_indications_to_diseases,
    get_mapping_stats,
    get_indication_mapping_stats,
)
from jptxgnn.predict import find_repurposing_candidates, generate_repurposing_report


def main():
    print("=" * 60)
    print("知識グラフ手法 - 日本 PMDA 医薬品リポジショニング予測")
    print("=" * 60)
    print()

    base_dir = Path(__file__).parent.parent
    processed_dir = base_dir / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    # 1. 薬品データ読み込み
    print("ステップ 1/5: PMDA 医薬品データを読み込み中...")
    df = load_fda_drugs()
    print(f"  総医薬品数: {len(df)}")

    # 2. 有効医薬品のフィルタリング
    print("ステップ 2/5: 有効医薬品をフィルタリング中...")
    active = filter_active_drugs(df)
    print(f"  有効医薬品数: {len(active)}")

    # 3. 成分マッピング
    print("ステップ 3/5: 成分を DrugBank にマッピング中...")
    drug_mapping = map_fda_drugs_to_drugbank(
        active,
        ingredient_field="有効成分",
        license_field="承認番号",
        name_field="販売名",
    )
    drug_mapping.to_csv(processed_dir / "drug_mapping.csv", index=False)
    stats = get_mapping_stats(drug_mapping)
    print(f"  成分マッピング率: {stats['mapping_rate']:.2%}")
    print(f"  DrugBank マッピング数: {stats['unique_drugbank_ids']}")

    # 4. 適応症マッピング
    print("ステップ 4/5: 適応症を疾病にマッピング中...")
    indication_mapping = map_fda_indications_to_diseases(
        active,
        indication_field="効能・効果",
        license_field="承認番号",
        brand_field="販売名",
    )
    indication_mapping.to_csv(processed_dir / "indication_mapping.csv", index=False)
    ind_stats = get_indication_mapping_stats(indication_mapping)
    print(f"  適応症マッピング率: {ind_stats['mapping_rate']:.2%}")
    print(f"  疾病マッピング数: {ind_stats['unique_diseases']}")

    # 5. リポジショニング予測
    print("ステップ 5/5: リポジショニング予測を実行中...")
    candidates = find_repurposing_candidates(
        drug_mapping,
        indication_mapping,
        license_field="承認番号",
        name_field="販売名",
    )
    output_path = processed_dir / "repurposing_candidates.csv"
    candidates.to_csv(output_path, index=False)

    # レポート生成
    report = generate_repurposing_report(candidates)

    print()
    print("=" * 60)
    print("予測完了！")
    print("=" * 60)
    print()
    print(f"結果ファイル: {output_path}")
    print()
    print("統計サマリー:")
    print(f"  リポジショニング候補数: {report['total_candidates']}")
    print(f"  対象薬物数: {report['unique_drugs']}")
    print(f"  潜在的新適応症数: {report['unique_diseases']}")


if __name__ == "__main__":
    main()
