#!/usr/bin/env python3
"""準備 external 資料檔案

從下載的 TxGNN 資料（node.csv, kg.csv）提取出知識圖譜方法所需的詞彙表和關係資料。

使用方法:
    uv run python scripts/prepare_external_data.py

前置條件:
    需要先下載以下檔案到 data/ 目錄：
    - node.csv: https://dataverse.harvard.edu/api/access/datafile/7144482
    - kg.csv: https://dataverse.harvard.edu/api/access/datafile/7144484

產生檔案:
    - data/external/drugbank_vocab.csv    - DrugBank 藥品詞彙表
    - data/external/disease_vocab.csv     - 疾病詞彙表
    - data/external/drug_disease_relations.csv - 藥物-疾病關係
"""

import sys
from pathlib import Path

# 將 src 加入 Python 路徑
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pandas as pd


def load_node_csv(filepath: Path) -> pd.DataFrame:
    """載入 TxGNN node.csv"""
    if not filepath.exists():
        raise FileNotFoundError(
            f"找不到 node.csv: {filepath}\n"
            f"請先下載: https://dataverse.harvard.edu/api/access/datafile/7144482"
        )
    df = pd.read_csv(filepath, sep="\t")
    # 移除 node_id 欄位中的引號
    df["node_id"] = df["node_id"].astype(str).str.strip('"')
    return df


def load_kg_csv(filepath: Path) -> pd.DataFrame:
    """載入 TxGNN kg.csv"""
    if not filepath.exists():
        raise FileNotFoundError(
            f"找不到 kg.csv: {filepath}\n"
            f"請先下載: https://dataverse.harvard.edu/api/access/datafile/7144484"
        )
    return pd.read_csv(filepath, low_memory=False)


def extract_drugbank_vocab(nodes_df: pd.DataFrame) -> pd.DataFrame:
    """從 node.csv 提取 DrugBank 藥品詞彙表

    Args:
        nodes_df: TxGNN node.csv DataFrame

    Returns:
        DataFrame with columns: drugbank_id, drug_name, drug_name_upper
    """
    drug_nodes = nodes_df[nodes_df["node_type"] == "drug"].copy()

    if len(drug_nodes) == 0:
        return pd.DataFrame(columns=["drugbank_id", "drug_name", "drug_name_upper"])

    result = pd.DataFrame({
        "drugbank_id": drug_nodes["node_id"],
        "drug_name": drug_nodes["node_name"],
        "drug_name_upper": drug_nodes["node_name"].str.upper(),
    })

    return result.drop_duplicates().reset_index(drop=True)


def extract_disease_vocab(nodes_df: pd.DataFrame) -> pd.DataFrame:
    """從 node.csv 提取疾病詞彙表

    Args:
        nodes_df: TxGNN node.csv DataFrame

    Returns:
        DataFrame with columns: disease_id, disease_name, disease_name_upper
    """
    disease_nodes = nodes_df[nodes_df["node_type"] == "disease"].copy()

    if len(disease_nodes) == 0:
        return pd.DataFrame(columns=["disease_id", "disease_name", "disease_name_upper"])

    result = pd.DataFrame({
        "disease_id": disease_nodes["node_id"],
        "disease_name": disease_nodes["node_name"],
        "disease_name_upper": disease_nodes["node_name"].str.upper(),
    })

    return result.drop_duplicates().reset_index(drop=True)


def extract_drug_disease_relations(kg_df: pd.DataFrame) -> pd.DataFrame:
    """從 kg.csv 提取藥物-疾病關係

    Args:
        kg_df: TxGNN kg.csv DataFrame

    Returns:
        DataFrame with columns: relation, x_id, x_name, y_id, y_name
    """
    # 過濾 indication 和 contraindication 關係
    relations = kg_df[kg_df["relation"].isin(["indication", "contraindication"])].copy()

    result = pd.DataFrame({
        "relation": relations["relation"],
        "x_id": relations["x_id"],
        "x_name": relations["x_name"],
        "y_id": relations["y_id"],
        "y_name": relations["y_name"],
    })

    return result.drop_duplicates().reset_index(drop=True)


def main():
    print("=" * 60)
    print("準備 external 資料檔案")
    print("=" * 60)
    print()

    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"
    external_dir = data_dir / "external"
    external_dir.mkdir(parents=True, exist_ok=True)

    # 載入原始資料
    print("步驟 1/4: 載入 node.csv...")
    node_path = data_dir / "node.csv"
    nodes_df = load_node_csv(node_path)
    print(f"  節點數: {len(nodes_df)}")

    print("步驟 2/4: 載入 kg.csv...")
    kg_path = data_dir / "kg.csv"
    kg_df = load_kg_csv(kg_path)
    print(f"  關係數: {len(kg_df)}")

    # 提取詞彙表
    print("步驟 3/4: 提取詞彙表...")

    drugbank_vocab = extract_drugbank_vocab(nodes_df)
    drugbank_path = external_dir / "drugbank_vocab.csv"
    drugbank_vocab.to_csv(drugbank_path, index=False)
    print(f"  DrugBank 藥品數: {len(drugbank_vocab)} -> {drugbank_path}")

    disease_vocab = extract_disease_vocab(nodes_df)
    disease_path = external_dir / "disease_vocab.csv"
    disease_vocab.to_csv(disease_path, index=False)
    print(f"  疾病數: {len(disease_vocab)} -> {disease_path}")

    # 提取藥物-疾病關係
    print("步驟 4/4: 提取藥物-疾病關係...")
    relations = extract_drug_disease_relations(kg_df)
    relations_path = external_dir / "drug_disease_relations.csv"
    relations.to_csv(relations_path, index=False)
    print(f"  藥物-疾病關係數: {len(relations)} -> {relations_path}")

    print()
    print("=" * 60)
    print("完成！")
    print("=" * 60)
    print()
    print("產生的檔案:")
    print(f"  - {drugbank_path}")
    print(f"  - {disease_path}")
    print(f"  - {relations_path}")
    print()
    print("下一步: 執行知識圖譜方法預測")
    print("  uv run python scripts/run_kg_prediction.py")


if __name__ == "__main__":
    main()
