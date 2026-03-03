"""處理 TxGNN Colab 預測結果"""

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


def load_txgnn_predictions(filepath: Path) -> pd.DataFrame:
    """載入 TxGNN Colab 預測結果

    Args:
        filepath: txgnn_predictions.csv 檔案路徑

    Returns:
        預測結果 DataFrame
    """
    return pd.read_csv(filepath)


def filter_by_score_threshold(
    predictions_df: pd.DataFrame,
    threshold: float = 0.5,
    score_column: str = "txgnn_score",
) -> pd.DataFrame:
    """依信心分數篩選預測結果

    Args:
        predictions_df: 預測結果 DataFrame
        threshold: 分數閾值 (0-1)
        score_column: 分數欄位名稱

    Returns:
        篩選後的 DataFrame
    """
    filtered = predictions_df[predictions_df[score_column] >= threshold].copy()
    filtered = filtered.sort_values(score_column, ascending=False)
    filtered["rank"] = range(1, len(filtered) + 1)
    return filtered


def merge_with_kg_candidates(
    txgnn_predictions: pd.DataFrame,
    kg_candidates: pd.DataFrame,
) -> pd.DataFrame:
    """將 TxGNN 預測分數合併到知識圖譜候選中

    Args:
        txgnn_predictions: TxGNN 預測結果
        kg_candidates: 知識圖譜候選結果 (from find_repurposing_candidates)

    Returns:
        合併後的 DataFrame
    """
    # 標準化欄位名稱以便合併
    txgnn_cols = {
        "drugbank_id": "drugbank_id",
        "潛在新適應症": "disease_name",
        "disease_name": "disease_name",
        "txgnn_score": "txgnn_score",
    }

    # 取得 TxGNN 分數對照
    if "潛在新適應症" in txgnn_predictions.columns:
        txgnn_predictions = txgnn_predictions.rename(columns={"潛在新適應症": "disease_name"})

    score_map = txgnn_predictions.set_index(
        ["drugbank_id", "disease_name"]
    )["txgnn_score"].to_dict()

    # 在知識圖譜候選中加入分數
    kg_candidates = kg_candidates.copy()

    def get_score(row):
        key = (row["drugbank_id"], row["潛在新適應症"])
        return score_map.get(key, None)

    kg_candidates["txgnn_score"] = kg_candidates.apply(get_score, axis=1)

    # 有分數的排在前面
    kg_candidates = kg_candidates.sort_values(
        ["txgnn_score", "藥物成分"],
        ascending=[False, True],
        na_position="last",
    )

    # 加入排名
    has_score = kg_candidates["txgnn_score"].notna()
    kg_candidates.loc[has_score, "rank"] = range(1, has_score.sum() + 1)

    return kg_candidates


def generate_txgnn_report(predictions_df: pd.DataFrame) -> dict:
    """生成 TxGNN 預測報告統計

    Args:
        predictions_df: 包含 txgnn_score 的預測結果

    Returns:
        統計報告字典
    """
    if len(predictions_df) == 0:
        return {
            "total_predictions": 0,
            "unique_drugs": 0,
            "unique_diseases": 0,
            "avg_score": 0,
            "max_score": 0,
            "min_score": 0,
            "score_distribution": {},
            "top_predictions": [],
        }

    # 基本統計
    total = len(predictions_df)
    unique_drugs = predictions_df["drugbank_id"].nunique() if "drugbank_id" in predictions_df.columns else 0

    disease_col = "潛在新適應症" if "潛在新適應症" in predictions_df.columns else "disease_name"
    unique_diseases = predictions_df[disease_col].nunique() if disease_col in predictions_df.columns else 0

    # 分數統計
    score_col = "txgnn_score"
    if score_col in predictions_df.columns:
        valid_scores = predictions_df[predictions_df[score_col].notna()][score_col]
        avg_score = valid_scores.mean() if len(valid_scores) > 0 else 0
        max_score = valid_scores.max() if len(valid_scores) > 0 else 0
        min_score = valid_scores.min() if len(valid_scores) > 0 else 0

        # 分數分布
        bins = [0, 0.25, 0.5, 0.75, 1.0]
        labels = ["0-0.25", "0.25-0.5", "0.5-0.75", "0.75-1.0"]
        score_dist = pd.cut(valid_scores, bins=bins, labels=labels, include_lowest=True)
        score_distribution = score_dist.value_counts().to_dict()
    else:
        avg_score = max_score = min_score = 0
        score_distribution = {}

    # Top 預測
    drug_col = "藥物成分" if "藥物成分" in predictions_df.columns else "drug_name"
    if score_col in predictions_df.columns and drug_col in predictions_df.columns:
        top_df = predictions_df.nlargest(10, score_col)
        top_predictions = [
            {
                "drug": row[drug_col],
                "disease": row[disease_col],
                "score": row[score_col],
            }
            for _, row in top_df.iterrows()
        ]
    else:
        top_predictions = []

    return {
        "total_predictions": total,
        "unique_drugs": unique_drugs,
        "unique_diseases": unique_diseases,
        "avg_score": float(avg_score),
        "max_score": float(max_score),
        "min_score": float(min_score),
        "score_distribution": {str(k): int(v) for k, v in score_distribution.items()},
        "top_predictions": top_predictions,
    }


def export_high_confidence_predictions(
    predictions_df: pd.DataFrame,
    output_path: Optional[Path] = None,
    threshold: float = 0.7,
) -> Path:
    """匯出高信心度預測結果

    Args:
        predictions_df: 預測結果 DataFrame
        output_path: 輸出檔案路徑
        threshold: 信心度閾值

    Returns:
        輸出檔案路徑
    """
    if output_path is None:
        output_path = (
            Path(__file__).parent.parent.parent.parent
            / "data"
            / "processed"
            / f"high_confidence_predictions_{threshold}.csv"
        )

    high_conf = filter_by_score_threshold(predictions_df, threshold)
    high_conf.to_csv(output_path, index=False, encoding="utf-8-sig")

    return output_path


def compare_with_existing_indications(
    predictions_df: pd.DataFrame,
    indication_mapping_df: pd.DataFrame,
) -> pd.DataFrame:
    """比較預測結果與現有適應症

    檢查 TxGNN 預測的適應症是否已經是該藥品的現有適應症。

    Args:
        predictions_df: TxGNN 預測結果
        indication_mapping_df: 適應症映射結果

    Returns:
        加入 is_novel 欄位的 DataFrame
    """
    # 建立現有適應症集合 (許可證字號 -> {disease_name})
    existing = indication_mapping_df[indication_mapping_df["disease_name"].notna()]
    existing_map = existing.groupby("許可證字號")["disease_name"].apply(
        lambda x: set(d.lower() for d in x)
    ).to_dict()

    predictions = predictions_df.copy()
    disease_col = "潛在新適應症" if "潛在新適應症" in predictions.columns else "disease_name"

    def check_novel(row):
        license_no = row.get("許可證字號")
        if not license_no or license_no not in existing_map:
            return True

        pred_disease = row[disease_col].lower() if pd.notna(row[disease_col]) else ""
        existing_diseases = existing_map[license_no]

        # 檢查是否有包含關係
        for existing_d in existing_diseases:
            if pred_disease in existing_d or existing_d in pred_disease:
                return False
        return True

    predictions["is_novel"] = predictions.apply(check_novel, axis=1)
    return predictions
