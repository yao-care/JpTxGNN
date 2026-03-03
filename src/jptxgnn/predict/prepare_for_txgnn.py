"""準備 TxGNN 預測所需的資料格式"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd


def load_txgnn_nodes(filepath: Optional[Path] = None) -> pd.DataFrame:
    """載入 TxGNN 節點資料

    Args:
        filepath: node.csv 檔案路徑（TxGNN 使用 node.csv，沒有 s）

    Returns:
        節點 DataFrame

    Raises:
        FileNotFoundError: 找不到 node.csv 檔案。請先下載 TxGNN 資料，
            參考 README.md「手動下載資料」章節。
    """
    if filepath is None:
        filepath = Path(__file__).parent.parent.parent.parent / "data" / "node.csv"

    if not filepath.exists():
        raise FileNotFoundError(
            f"找不到 TxGNN 節點檔案: {filepath}\n"
            f"請先下載 node.csv 並放到 data/ 目錄。\n"
            f"下載連結: https://dataverse.harvard.edu/api/access/datafile/7144482"
        )

    df = pd.read_csv(filepath, sep="\t")
    # 移除 node_id 欄位中的引號
    df["node_id"] = df["node_id"].astype(str).str.strip('"')
    return df


def build_drugbank_to_node_index(nodes_df: pd.DataFrame) -> Dict[str, int]:
    """建立 DrugBank ID 到 node_index 的映射

    Args:
        nodes_df: TxGNN 節點 DataFrame

    Returns:
        {drugbank_id: node_index}
    """
    drug_nodes = nodes_df[nodes_df["node_type"] == "drug"]
    return dict(zip(drug_nodes["node_id"], drug_nodes["node_index"]))


def build_disease_node_mappings(nodes_df: pd.DataFrame) -> Tuple[Dict[int, str], Dict[int, str]]:
    """建立疾病 node_index 到名稱/ID 的映射

    Args:
        nodes_df: TxGNN 節點 DataFrame

    Returns:
        (node_index -> disease_name, node_index -> disease_id)
    """
    disease_nodes = nodes_df[nodes_df["node_type"] == "disease"]
    idx_to_name = dict(zip(disease_nodes["node_index"], disease_nodes["node_name"]))
    idx_to_id = dict(zip(disease_nodes["node_index"], disease_nodes["node_id"]))
    return idx_to_name, idx_to_id


def prepare_drug_list_for_txgnn(
    drug_mapping_df: pd.DataFrame,
    nodes_df: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """準備用於 TxGNN 預測的藥物清單

    將台灣藥品的 DrugBank ID 映射到 TxGNN 的 node_index，
    以便在 Colab 環境中執行預測。

    Args:
        drug_mapping_df: 藥品 DrugBank 映射結果 (from map_fda_drugs_to_drugbank)
        nodes_df: TxGNN 節點 DataFrame

    Returns:
        包含 node_index 的藥物清單 DataFrame
    """
    if nodes_df is None:
        nodes_df = load_txgnn_nodes()

    # 建立 DrugBank -> node_index 映射
    drugbank_to_idx = build_drugbank_to_node_index(nodes_df)

    # 取得唯一的藥品-DrugBank 對應
    valid_drugs = drug_mapping_df[drug_mapping_df["drugbank_id"].notna()].copy()
    unique_drugs = valid_drugs[["drugbank_id", "標準化成分"]].drop_duplicates()

    # 加入 node_index
    results = []
    for _, row in unique_drugs.iterrows():
        drugbank_id = row["drugbank_id"]
        if drugbank_id in drugbank_to_idx:
            results.append({
                "drugbank_id": drugbank_id,
                "drug_name": row["標準化成分"],
                "node_index": drugbank_to_idx[drugbank_id],
            })

    result_df = pd.DataFrame(results)
    return result_df


def get_drug_node_mapping_stats(
    drug_mapping_df: pd.DataFrame,
    nodes_df: Optional[pd.DataFrame] = None,
) -> dict:
    """計算藥品節點映射統計

    Args:
        drug_mapping_df: 藥品映射結果
        nodes_df: TxGNN 節點 DataFrame

    Returns:
        統計字典
    """
    if nodes_df is None:
        nodes_df = load_txgnn_nodes()

    drugbank_to_idx = build_drugbank_to_node_index(nodes_df)

    valid_drugs = drug_mapping_df[drug_mapping_df["drugbank_id"].notna()]
    unique_drugbank_ids = valid_drugs["drugbank_id"].unique()

    found_count = sum(1 for db_id in unique_drugbank_ids if db_id in drugbank_to_idx)

    return {
        "total_unique_drugbank_ids": len(unique_drugbank_ids),
        "found_in_txgnn": found_count,
        "not_found_in_txgnn": len(unique_drugbank_ids) - found_count,
        "mapping_rate": found_count / len(unique_drugbank_ids) if unique_drugbank_ids.size > 0 else 0,
        "txgnn_total_drugs": len(drugbank_to_idx),
    }


def export_for_colab(
    drug_mapping_df: pd.DataFrame,
    output_path: Optional[Path] = None,
) -> Path:
    """匯出用於 Colab 的藥品資料

    Args:
        drug_mapping_df: 藥品映射結果
        output_path: 輸出檔案路徑

    Returns:
        輸出檔案路徑
    """
    if output_path is None:
        output_path = Path(__file__).parent.parent.parent.parent / "data" / "processed" / "drug_mapping_for_colab.csv"

    # 只保留有 DrugBank ID 的藥品
    valid_drugs = drug_mapping_df[drug_mapping_df["drugbank_id"].notna()].copy()

    # 選擇需要的欄位
    export_cols = ["許可證字號", "中文品名", "標準化成分", "drugbank_id"]
    available_cols = [col for col in export_cols if col in valid_drugs.columns]

    export_df = valid_drugs[available_cols].drop_duplicates()
    export_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return output_path
