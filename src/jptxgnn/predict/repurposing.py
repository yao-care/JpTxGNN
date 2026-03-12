"""老藥新用預測 - 基於 TxGNN 知識圖譜"""

from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import pandas as pd


def load_drug_disease_relations(filepath: Optional[Path] = None) -> pd.DataFrame:
    """載入 TxGNN 藥物-疾病關係

    Args:
        filepath: CSV 檔案路徑

    Returns:
        藥物-疾病關係 DataFrame
    """
    if filepath is None:
        filepath = Path(__file__).parent.parent.parent.parent / "data" / "external" / "drug_disease_relations.csv"

    return pd.read_csv(filepath)


def build_drug_indication_map(relations_df: pd.DataFrame) -> Dict[str, Set[str]]:
    """建立藥物 -> 適應症集合的映射

    Args:
        relations_df: 藥物-疾病關係 DataFrame

    Returns:
        {drug_name: {disease1, disease2, ...}}
    """
    # 只取 indication 和 off-label use
    indications = relations_df[relations_df["relation"].isin(["indication", "off-label use"])]

    drug_map = {}
    for _, row in indications.iterrows():
        drug = row["x_name"].upper()
        disease = row["y_name"]

        if drug not in drug_map:
            drug_map[drug] = set()
        drug_map[drug].add(disease)

    return drug_map


def find_repurposing_candidates(
    drug_mapping_df: pd.DataFrame,
    indication_mapping_df: pd.DataFrame,
    relations_df: Optional[pd.DataFrame] = None,
    license_field: str = "承認番号",
    name_field: str = "販売名",
) -> pd.DataFrame:
    """找出老藥新用候選

    比較藥品的現有適應症與 TxGNN 知識圖譜中的適應症，
    找出可能的新適應症。

    Args:
        drug_mapping_df: 藥品 DrugBank 映射結果
        indication_mapping_df: 適應症疾病映射結果
        relations_df: TxGNN 藥物-疾病關係
        license_field: 許可證欄位名稱
        name_field: 品名欄位名稱

    Returns:
        老藥新用候選 DataFrame
    """
    if relations_df is None:
        relations_df = load_drug_disease_relations()

    # 建立 TxGNN 藥物適應症映射
    kg_drug_map = build_drug_indication_map(relations_df)

    # 建立藥品的現有適應症（向量化操作）
    current_drug_diseases = {}
    if len(indication_mapping_df) > 0 and "disease_name" in indication_mapping_df.columns:
        diseases_df = indication_mapping_df[
            indication_mapping_df["disease_name"].notna()
        ][["license_id", "disease_name"]].copy()
        if len(diseases_df) > 0:
            diseases_df["disease_lower"] = diseases_df["disease_name"].str.lower()
            current_drug_diseases = diseases_df.groupby("license_id")["disease_lower"].apply(set).to_dict()

    # 建立藥品資訊索引
    valid_drugs = drug_mapping_df[drug_mapping_df["drugbank_id"].notna()].copy()
    if len(valid_drugs) == 0:
        return pd.DataFrame()

    # 確保有同義詞欄位（英語藥名）
    if "同義詞" not in valid_drugs.columns:
        valid_drugs["同義詞"] = ""

    # 取得唯一的 (許可證, 藥物成分) 組合
    unique_pairs = valid_drugs[[license_field, "標準化成分", name_field, "drugbank_id", "同義詞"]].drop_duplicates()

    candidates = []

    for _, row in unique_pairs.iterrows():
        license_no = row[license_field]
        drug_name_jp = row["標準化成分"]

        # 使用英語藥名（同義詞）查詢 TxGNN KG
        # 同義詞可能包含多個，以分號分隔，取第一個作為主要英語名
        synonyms = str(row.get("同義詞", "")).strip()
        if synonyms:
            drug_name_en = synonyms.split(";")[0].strip().upper()
        else:
            drug_name_en = drug_name_jp.upper()

        # 查詢 TxGNN 中該藥物的所有適應症（使用英語名）
        kg_diseases = kg_drug_map.get(drug_name_en, set())
        if not kg_diseases:
            continue

        # 取得現有適應症
        current_diseases = current_drug_diseases.get(license_no, set())

        # 找出潛在新適應症
        for disease in kg_diseases:
            disease_lower = disease.lower()

            # 檢查是否已存在（如果沒有現有適應症，則所有 KG 適應症都是候選）
            if current_diseases:
                is_new = all(
                    tw_d not in disease_lower and disease_lower not in tw_d
                    for tw_d in current_diseases
                )
            else:
                is_new = True  # 沒有現有適應症資料，所有 KG 適應症都是候選

            if is_new:
                candidates.append({
                    license_field: license_no,
                    name_field: row[name_field],
                    "藥物成分": drug_name_en,
                    "藥物成分_原名": drug_name_jp,
                    "drugbank_id": row["drugbank_id"],
                    "潛在新適應症": disease,
                    "來源": "TxGNN Knowledge Graph",
                })

    result_df = pd.DataFrame(candidates)

    # 去重
    if len(result_df) > 0:
        # First: remove exact duplicates per license
        result_df = result_df.drop_duplicates(
            subset=[license_field, "藥物成分", "潛在新適應症"]
        )

        # Second: for DL prediction efficiency, keep only unique (drugbank_id, disease) pairs
        # This prevents redundant DL predictions for the same drug-disease combination
        # We keep the first occurrence (arbitrary license_id as representative)
        result_df = result_df.drop_duplicates(
            subset=["drugbank_id", "潛在新適應症"],
            keep="first"
        )

    return result_df


def generate_repurposing_report(candidates_df: pd.DataFrame) -> dict:
    """生成老藥新用報告統計

    Args:
        candidates_df: 候選藥物 DataFrame

    Returns:
        統計報告字典
    """
    if len(candidates_df) == 0 or "藥物成分" not in candidates_df.columns:
        return {
            "total_candidates": 0,
            "unique_drugs": 0,
            "unique_diseases": 0,
            "top_diseases": [],
            "top_drugs": [],
        }

    unique_drugs = candidates_df["藥物成分"].nunique()
    unique_diseases = candidates_df["潛在新適應症"].nunique()

    # 最常見的潛在新適應症
    top_diseases = candidates_df["潛在新適應症"].value_counts().head(10).to_dict()

    # 最多潛在新適應症的藥物
    drug_counts = candidates_df.groupby("藥物成分")["潛在新適應症"].nunique()
    top_drugs = drug_counts.sort_values(ascending=False).head(10).to_dict()

    return {
        "total_candidates": len(candidates_df),
        "unique_drugs": unique_drugs,
        "unique_diseases": unique_diseases,
        "top_diseases": top_diseases,
        "top_drugs": top_drugs,
    }
