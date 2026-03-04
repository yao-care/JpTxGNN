"""TxGNN 深度學習模型本地執行模組

提供在本地環境（包括 macOS）執行 TxGNN 預測的功能。
自動偵測可用的運算裝置（CUDA/MPS/CPU）。
支援中斷續算功能。
"""

import csv
import os
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import pandas as pd
from tqdm import tqdm


def detect_device() -> str:
    """自動偵測最佳運算裝置

    Returns:
        裝置字串: 'cuda:0' 或 'cpu'
        注意：DGL 不支援 Apple MPS，所以在 Mac 上只能用 CPU
    """
    try:
        import torch

        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            print(f"✓ 偵測到 CUDA GPU: {device_name}")
            return "cuda:0"
        else:
            # DGL 不支援 Apple MPS，強制使用 CPU
            print("✓ 使用 CPU 模式（DGL 不支援 MPS）")
            return "cpu"
    except ImportError:
        print("⚠ PyTorch 未安裝，使用 CPU 模式")
        return "cpu"


def check_dependencies() -> Tuple[bool, List[str]]:
    """檢查必要的依賴套件

    Returns:
        (是否全部安裝, 缺少的套件列表)
    """
    missing = []

    try:
        import torch
    except ImportError:
        missing.append("torch")

    try:
        import dgl
    except ImportError:
        missing.append("dgl")

    try:
        import jptxgnn
    except ImportError:
        missing.append("TxGNN")

    return len(missing) == 0, missing


def print_install_instructions(missing_packages: List[str], device: str = "cpu"):
    """印出安裝指示

    Args:
        missing_packages: 缺少的套件列表
        device: 目標裝置類型
    """
    print("\n" + "=" * 60)
    print("請設定 conda 環境以執行 TxGNN 預測:")
    print("=" * 60)

    print("\n# 建立並啟動 conda 環境")
    print("conda create -n txgnn python=3.11 -y")
    print("conda activate txgnn")

    if device == "cpu":
        # CPU 版本
        print("\n# CPU 版本（適用於 macOS / Linux）")
        print("pip install torch==2.2.2 torchvision==0.17.2")
        print("pip install dgl==1.1.3")
    else:
        # CUDA 版本
        print("\n# CUDA 版本（適用於 Linux/Windows with NVIDIA GPU）")
        print("pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118")
        print("pip install dgl -f https://data.dgl.ai/wheels/cu118/repo.html")

    print("\n# 安裝 TxGNN 和其他依賴")
    print("pip install git+https://github.com/mims-harvard/TxGNN.git")
    print("pip install pandas tqdm pyyaml pydantic ogb")

    print("\n" + "=" * 60)


def download_pretrained_model(
    model_dir: Optional[Path] = None,
    force: bool = False,
) -> Path:
    """下載 TxGNN 預訓練模型

    Args:
        model_dir: 模型儲存目錄
        force: 是否強制重新下載

    Returns:
        模型目錄路徑
    """
    if model_dir is None:
        model_dir = Path(__file__).parent.parent.parent.parent / "model_ckpt"

    model_dir = Path(model_dir)

    # 檢查是否已存在
    if model_dir.exists() and not force:
        # 檢查是否有必要的檔案
        if (model_dir / "model.pt").exists() or any(model_dir.glob("*.pt")):
            print(f"✓ 預訓練模型已存在: {model_dir}")
            return model_dir

    print("下載 TxGNN 預訓練模型...")

    try:
        import gdown
    except ImportError:
        raise ImportError("請先安裝 gdown: pip install gdown")

    # 建立目錄
    model_dir.parent.mkdir(parents=True, exist_ok=True)

    # 下載模型 (TxGNN official release)
    zip_path = model_dir.parent / "model_ckpt.zip"
    gdown.download(
        "https://drive.google.com/uc?id=1fxTFkjo2jvmz9k6vesDbCeucQjGRojLj",
        str(zip_path),
        quiet=False,
    )

    # 解壓縮
    print("解壓縮模型...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(model_dir.parent)

    # 清理 zip 檔
    zip_path.unlink()

    print(f"✓ 模型下載完成: {model_dir}")
    return model_dir


def download_kg_data(
    data_dir: Optional[Path] = None,
    force: bool = False,
) -> Path:
    """下載 TxGNN 知識圖譜資料

    Args:
        data_dir: 資料儲存目錄
        force: 是否強制重新下載

    Returns:
        資料目錄路徑
    """
    if data_dir is None:
        data_dir = Path(__file__).parent.parent.parent.parent / "data" / "external"

    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    files_to_download = {
        "nodes.csv": "https://dataverse.harvard.edu/api/access/datafile/6180617",
        "kg.csv": "https://dataverse.harvard.edu/api/access/datafile/6180620",
    }

    import requests

    for filename, url in files_to_download.items():
        filepath = data_dir / filename
        if filepath.exists() and not force:
            print(f"✓ {filename} 已存在")
            continue

        print(f"下載 {filename}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✓ {filename} 下載完成")

    return data_dir


class CheckpointManager:
    """Checkpoint 管理器 - 支援中斷續算

    每處理完一個藥物就儲存結果，允許中斷後繼續執行。
    """

    COLUMNS = ["drugbank_id", "drug_name", "disease_name", "txgnn_score"]

    def __init__(self, checkpoint_path: Path):
        """初始化 Checkpoint 管理器

        Args:
            checkpoint_path: checkpoint 檔案路徑
        """
        self.checkpoint_path = Path(checkpoint_path)
        self.processed_drugs: Set[str] = set()
        self._file_exists = self.checkpoint_path.exists()

    def load(self) -> Set[str]:
        """載入已處理的藥物 ID

        Returns:
            已處理的 drugbank_id 集合
        """
        if not self._file_exists:
            return set()

        try:
            df = pd.read_csv(self.checkpoint_path)
            self.processed_drugs = set(df["drugbank_id"].unique())
            print(f"✓ 從 checkpoint 載入 {len(self.processed_drugs)} 個已處理藥物")
            return self.processed_drugs
        except Exception as e:
            print(f"⚠ 無法載入 checkpoint: {e}")
            return set()

    def append(self, predictions: List[dict]):
        """追加預測結果到 checkpoint

        Args:
            predictions: 預測結果列表
        """
        if not predictions:
            return

        # 確保目錄存在
        self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

        # 追加寫入 CSV
        write_header = not self._file_exists
        with open(self.checkpoint_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.COLUMNS)
            if write_header:
                writer.writeheader()
                self._file_exists = True
            writer.writerows(predictions)

        # 更新已處理清單
        for pred in predictions:
            self.processed_drugs.add(pred["drugbank_id"])

    def get_results(self) -> pd.DataFrame:
        """取得所有已儲存的結果

        Returns:
            結果 DataFrame
        """
        if not self._file_exists:
            return pd.DataFrame(columns=self.COLUMNS)

        return pd.read_csv(self.checkpoint_path)

    def clear(self):
        """清除 checkpoint 檔案"""
        if self.checkpoint_path.exists():
            self.checkpoint_path.unlink()
            print("✓ Checkpoint 已清除")
        self.processed_drugs = set()
        self._file_exists = False

    def is_processed(self, drugbank_id: str) -> bool:
        """檢查藥物是否已處理

        Args:
            drugbank_id: DrugBank ID

        Returns:
            是否已處理
        """
        return drugbank_id in self.processed_drugs


class TxGNNPredictor:
    """TxGNN 預測器包裝類別

    提供簡化的 API 來執行 TxGNN 藥物-疾病預測。
    """

    def __init__(
        self,
        model_dir: Optional[Path] = None,
        data_dir: Optional[Path] = None,
        device: Optional[str] = None,
    ):
        """初始化 TxGNN 預測器

        Args:
            model_dir: 預訓練模型目錄
            data_dir: TxGNN 知識圖譜資料目錄
            device: 運算裝置 ('cuda:0', 'mps', 'cpu')，None 為自動偵測
        """
        self.device = device or detect_device()
        self.model_dir = Path(model_dir) if model_dir else None
        self.data_dir = Path(data_dir) if data_dir else None

        self.model = None
        self.tx_data = None
        self.nodes_df = None
        self.drugbank_to_name = None
        self.drugbank_to_idx = None
        self.disease_idx_to_name = None
        self.all_disease_indices = None

    def setup(self, download_if_missing: bool = True):
        """設定模型與資料

        Args:
            download_if_missing: 如果資料/模型不存在是否自動下載
        """
        # 檢查依賴
        deps_ok, missing = check_dependencies()
        if not deps_ok:
            print_install_instructions(missing, self.device)
            raise ImportError(f"缺少必要套件: {', '.join(missing)}")

        # 設定資料目錄（不自動下載，請手動下載資料）
        base_dir = Path(__file__).parent.parent.parent.parent
        if self.data_dir is None:
            self.data_dir = base_dir / "data"
        if self.model_dir is None:
            self.model_dir = base_dir / "model_ckpt"

        # 檢查必要檔案是否存在
        required_files = ["kg.csv", "node.csv", "edges.csv"]
        missing_files = [f for f in required_files if not (self.data_dir / f).exists()]
        if missing_files:
            raise FileNotFoundError(
                f"缺少必要檔案: {missing_files}\n"
                f"請手動下載並放到 {self.data_dir}/ 目錄\n"
                f"參考 README.md 的「手動下載資料」章節"
            )

        if not (self.model_dir / "model.pt").exists():
            raise FileNotFoundError(
                f"缺少預訓練模型: {self.model_dir}/model.pt\n"
                f"請手動下載並解壓縮到 {self.model_dir}/ 目錄\n"
                f"參考 README.md 的「手動下載資料」章節"
            )

        # 載入 TxGNN (外部套件)
        from txgnn import TxData, TxGNN

        print("載入 TxGNN 資料集...")
        self.tx_data = TxData(data_folder_path=str(self.data_dir))
        self.tx_data.prepare_split(split="complex_disease", seed=42)

        print(f"節點數: {self.tx_data.G.number_of_nodes()}")
        print(f"邊數: {self.tx_data.G.number_of_edges()}")

        print("載入預訓練模型...")
        self.model = TxGNN(
            data=self.tx_data,
            weight_bias_track=False,
            proj_name="JpTxGNN",
            exp_name="taiwan_drug_repurposing",
            device=self.device,
        )
        self.model.load_pretrained(str(self.model_dir))

        # 載入節點映射
        self._load_node_mappings()

        print("✓ TxGNN 設定完成！")

    def _load_node_mappings(self):
        """載入節點映射資料

        注意：TxGNN 使用兩種索引系統：
        1. node.csv 的 node_index 是全局索引
        2. tx_data.df 的 x_idx/y_idx 是類型特定索引（用於模型預測）

        我們需要從 tx_data.df 取得正確的類型特定索引。
        """
        # 從 TxGNN 的處理後資料取得正確的索引映射
        df = self.tx_data.df

        # 確保 ID 是字串格式
        from txgnn.utils import convert2str
        df = df.copy()
        df["x_id"] = df.x_id.apply(lambda x: convert2str(x))
        df["y_id"] = df.y_id.apply(lambda x: convert2str(x))

        # 藥物映射（從 x_type='drug' 取得）
        drug_rows = df[df.x_type == "drug"][["x_id", "x_idx"]].drop_duplicates()
        self.drugbank_to_idx = dict(zip(drug_rows["x_id"], drug_rows["x_idx"].astype(int)))

        # 也從 y_type='drug' 補充（有些藥物可能只出現在 y 端）
        drug_rows_y = df[df.y_type == "drug"][["y_id", "y_idx"]].drop_duplicates()
        self.drugbank_to_idx.update(dict(zip(drug_rows_y["y_id"], drug_rows_y["y_idx"].astype(int))))

        # 讀取 node.csv 取得藥物名稱
        nodes_path = self.data_dir / "node.csv"
        self.nodes_df = pd.read_csv(nodes_path, sep="\t")
        drug_nodes = self.nodes_df[self.nodes_df["node_type"] == "drug"].copy()
        drug_nodes["node_id"] = drug_nodes["node_id"].str.strip('"')
        self.drugbank_to_name = dict(zip(drug_nodes["node_id"], drug_nodes["node_name"]))

        # 疾病映射（從 y_type='disease' 取得類型特定索引）
        disease_rows = df[df.y_type == "disease"][["y_id", "y_idx"]].drop_duplicates()
        self.all_disease_indices = sorted(disease_rows["y_idx"].astype(int).unique().tolist())

        # 從 kg.csv 取得疾病名稱
        kg_path = self.data_dir / "kg.csv"
        kg_df = pd.read_csv(kg_path)
        kg_df["y_id"] = kg_df.y_id.apply(lambda x: convert2str(x))
        disease_names = kg_df[kg_df.y_type == "disease"][["y_id", "y_name"]].drop_duplicates()
        disease_id_to_name = dict(zip(disease_names["y_id"], disease_names["y_name"]))

        # 建立 disease_idx -> name 映射
        disease_idx_to_id = dict(zip(disease_rows["y_idx"].astype(int), disease_rows["y_id"]))
        self.disease_idx_to_name = {
            idx: disease_id_to_name.get(disease_idx_to_id.get(idx, ""), f"disease_{idx}")
            for idx in self.all_disease_indices
        }

        print(f"  藥物數: {len(self.drugbank_to_idx)}")
        print(f"  疾病數: {len(self.all_disease_indices)}")

    def predict_drug(
        self,
        drugbank_id: str,
        top_k: Optional[int] = None,
    ) -> Dict[str, float]:
        """預測單一藥物對所有疾病的分數

        Args:
            drugbank_id: DrugBank ID
            top_k: 只返回前 k 個結果

        Returns:
            {disease_name: score}
        """
        if self.model is None:
            raise RuntimeError("請先呼叫 setup() 方法")

        try:
            import torch

            # 取得藥物索引
            if drugbank_id not in self.drugbank_to_idx:
                return {}
            drug_idx = self.drugbank_to_idx[drugbank_id]

            # 建立預測用的 DataFrame（藥物 x 所有疾病）
            df_predict = pd.DataFrame({
                "x_idx": [drug_idx] * len(self.all_disease_indices),
                "relation": ["indication"] * len(self.all_disease_indices),
                "y_idx": self.all_disease_indices,
            })

            # 執行預測
            with torch.no_grad():
                pred_scores = self.model.predict(df_predict)

            # 取得 indication 類型的預測分數
            etype = ("drug", "indication", "disease")
            if etype not in pred_scores:
                return {}

            scores_tensor = torch.sigmoid(pred_scores[etype]).cpu().numpy()

            # 建立 disease_name -> score 映射
            scores = {}
            for i, disease_idx in enumerate(self.all_disease_indices):
                disease_name = self.disease_idx_to_name.get(disease_idx, f"disease_{disease_idx}")
                scores[disease_name] = float(scores_tensor[i])

            if top_k is not None:
                sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                scores = dict(sorted_scores[:top_k])

            return scores
        except Exception as e:
            print(f"預測 {drugbank_id} 時發生錯誤: {e}")
            import traceback
            traceback.print_exc()
            return {}

    def predict_batch(
        self,
        drug_mapping_df: pd.DataFrame,
        drugbank_col: str = "drugbank_id",
        top_k_per_drug: Optional[int] = None,
        min_score: float = 0.0,
        checkpoint_manager: Optional[CheckpointManager] = None,
    ) -> pd.DataFrame:
        """批次預測多個藥物

        Args:
            drug_mapping_df: 包含 DrugBank ID 的藥品映射 DataFrame
            drugbank_col: DrugBank ID 欄位名稱
            top_k_per_drug: 每個藥物保留前 k 個疾病
            min_score: 最低分數門檻
            checkpoint_manager: Checkpoint 管理器（用於中斷續算）

        Returns:
            預測結果 DataFrame
        """
        if self.model is None:
            raise RuntimeError("請先呼叫 setup() 方法")

        # 取得唯一的 DrugBank ID
        valid_drugs = drug_mapping_df[drug_mapping_df[drugbank_col].notna()]
        unique_ids = valid_drugs[drugbank_col].unique()

        # 找出在 TxGNN 中存在的藥物
        drugs_to_predict = []
        skipped_count = 0
        for db_id in unique_ids:
            if db_id in self.drugbank_to_name:
                # 如果有 checkpoint，跳過已處理的藥物
                if checkpoint_manager and checkpoint_manager.is_processed(db_id):
                    skipped_count += 1
                    continue
                drugs_to_predict.append({
                    "drugbank_id": db_id,
                    "drug_name": self.drugbank_to_name[db_id],
                })

        total_in_txgnn = len(drugs_to_predict) + skipped_count
        print(f"共 {total_in_txgnn} 個藥物在 TxGNN 中存在")
        if skipped_count > 0:
            print(f"  - 已處理（從 checkpoint 載入）: {skipped_count}")
            print(f"  - 待處理: {len(drugs_to_predict)}")

        if not drugs_to_predict:
            print("所有藥物已處理完畢！")
            if checkpoint_manager:
                result_df = checkpoint_manager.get_results()
                if len(result_df) > 0:
                    result_df = result_df.sort_values("txgnn_score", ascending=False)
                    if top_k_per_drug is not None:
                        result_df = result_df.groupby("drugbank_id").head(top_k_per_drug)
                    result_df["rank"] = range(1, len(result_df) + 1)
                return result_df
            return pd.DataFrame()

        # 執行預測
        predictions = []
        for drug_info in tqdm(drugs_to_predict, desc="預測中"):
            drug_predictions = []
            try:
                # 使用 predict_drug 方法取得預測分數
                scores = self.predict_drug(
                    drugbank_id=drug_info["drugbank_id"],
                    top_k=top_k_per_drug,
                )

                for disease_name, score in scores.items():
                    if score >= min_score:
                        pred = {
                            "drugbank_id": drug_info["drugbank_id"],
                            "drug_name": drug_info["drug_name"],
                            "disease_name": disease_name,
                            "txgnn_score": score,
                        }
                        drug_predictions.append(pred)
                        predictions.append(pred)

                # 每個藥物處理完後儲存 checkpoint
                if checkpoint_manager:
                    checkpoint_manager.append(drug_predictions)

            except Exception as e:
                print(f"Error predicting for {drug_info['drug_name']}: {e}")
                continue

        # 如果有 checkpoint，從 checkpoint 取得完整結果
        if checkpoint_manager:
            result_df = checkpoint_manager.get_results()
        else:
            result_df = pd.DataFrame(predictions)

        if len(result_df) > 0:
            # 排序
            result_df = result_df.sort_values("txgnn_score", ascending=False)

            # 如果需要，每個藥物只保留前 k 個
            if top_k_per_drug is not None:
                result_df = result_df.groupby("drugbank_id").head(top_k_per_drug)

            result_df["rank"] = range(1, len(result_df) + 1)

        return result_df


def main():
    """命令列入口點"""
    import argparse

    parser = argparse.ArgumentParser(
        description="TxGNN 台灣藥品老藥新用預測",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  # 使用預設設定執行預測（支援中斷續算）
  python scripts/run_txgnn_prediction.py

  # 指定 CPU 模式
  python scripts/run_txgnn_prediction.py --device cpu

  # 只保留分數 > 0.5 的結果
  python scripts/run_txgnn_prediction.py --min-score 0.5

  # 每個藥物只保留前 100 個疾病
  python scripts/run_txgnn_prediction.py --top-k 100

  # 忽略之前的進度，重新開始
  python scripts/run_txgnn_prediction.py --restart

  # 中斷後繼續執行
  # （直接重新執行即可，會自動從上次中斷處繼續）
  python scripts/run_txgnn_prediction.py
        """,
    )

    parser.add_argument(
        "--drug-mapping",
        type=str,
        help="藥品映射 CSV 路徑 (預設: data/processed/drug_mapping.csv)",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="輸出結果路徑 (預設: data/processed/txgnn_dl_predictions.csv)",
    )
    parser.add_argument(
        "--device",
        type=str,
        choices=["cuda:0", "mps", "cpu"],
        help="運算裝置 (預設: 自動偵測)",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.0,
        help="最低分數門檻 (預設: 0.0)",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        help="每個藥物保留前 k 個疾病",
    )
    parser.add_argument(
        "--restart",
        action="store_true",
        help="忽略之前的進度，重新開始預測",
    )
    parser.add_argument(
        "--checkpoint-file",
        type=str,
        help="Checkpoint 檔案路徑 (預設: data/processed/txgnn_checkpoint.csv)",
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="只檢查依賴套件是否已安裝",
    )

    args = parser.parse_args()

    # 只檢查依賴
    if args.check_deps:
        deps_ok, missing = check_dependencies()
        device = detect_device()
        if deps_ok:
            print("✓ 所有依賴套件已安裝")
        else:
            print(f"✗ 缺少套件: {', '.join(missing)}")
            print_install_instructions(missing, device)
        return

    # 執行預測
    run_taiwan_drug_prediction(
        drug_mapping_path=Path(args.drug_mapping) if args.drug_mapping else None,
        output_path=Path(args.output) if args.output else None,
        device=args.device,
        min_score=args.min_score,
        top_k_per_drug=args.top_k,
        restart=args.restart,
        checkpoint_path=Path(args.checkpoint_file) if args.checkpoint_file else None,
    )


def run_taiwan_drug_prediction(
    drug_mapping_path: Optional[Path] = None,
    output_path: Optional[Path] = None,
    device: Optional[str] = None,
    min_score: float = 0.0,
    top_k_per_drug: Optional[int] = None,
    restart: bool = False,
    checkpoint_path: Optional[Path] = None,
) -> pd.DataFrame:
    """執行台灣藥品老藥新用預測

    支援中斷續算：每處理完一個藥物就儲存進度，
    中斷後重新執行會跳過已處理的藥物。

    Args:
        drug_mapping_path: 藥品映射 CSV 路徑
        output_path: 輸出結果路徑
        device: 運算裝置
        min_score: 最低分數門檻
        top_k_per_drug: 每個藥物保留前 k 個疾病
        restart: 是否忽略之前的進度重新開始
        checkpoint_path: Checkpoint 檔案路徑

    Returns:
        預測結果 DataFrame
    """
    base_dir = Path(__file__).parent.parent.parent.parent

    # 預設路徑
    if drug_mapping_path is None:
        drug_mapping_path = base_dir / "data" / "processed" / "drug_mapping.csv"
    if output_path is None:
        output_path = base_dir / "data" / "processed" / "txgnn_dl_predictions.csv"
    if checkpoint_path is None:
        checkpoint_path = base_dir / "data" / "processed" / "txgnn_checkpoint.csv"

    # 初始化 checkpoint 管理器
    checkpoint_manager = CheckpointManager(checkpoint_path)

    # 如果指定重新開始，清除 checkpoint
    if restart:
        checkpoint_manager.clear()
        print("已清除之前的進度，將從頭開始預測")
    else:
        # 載入之前的進度
        checkpoint_manager.load()

    # 載入藥品映射
    print(f"載入藥品映射: {drug_mapping_path}")
    drug_mapping = pd.read_csv(drug_mapping_path)
    print(f"共 {len(drug_mapping)} 筆藥品資料")

    # 初始化預測器
    predictor = TxGNNPredictor(device=device)
    predictor.setup()

    # 執行預測（使用 checkpoint 管理器）
    predictions = predictor.predict_batch(
        drug_mapping,
        min_score=min_score,
        top_k_per_drug=top_k_per_drug,
        checkpoint_manager=checkpoint_manager,
    )

    print(f"\n預測完成！共 {len(predictions)} 筆結果")

    # 直接輸出預測結果（不展開台灣藥品對照，節省記憶體）
    if len(predictions) > 0:
        result = predictions.rename(columns={
            "disease_name": "潛在新適應症",
        })
        result["來源"] = "TxGNN Deep Learning Model"

        # 儲存結果
        result.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"結果已儲存至: {output_path}")

        # 印出統計
        print("\n" + "=" * 50)
        print("TxGNN 深度學習預測統計摘要")
        print("=" * 50)
        print(f"總預測數: {len(result)}")
        print(f"涉及藥物數: {result['drugbank_id'].nunique()}")
        print(f"涉及適應症數: {result['潛在新適應症'].nunique()}")
        print(f"平均信心分數: {result['txgnn_score'].mean():.4f}")
        print(f"最高信心分數: {result['txgnn_score'].max():.4f}")
        print(f"\n提示：可用 drug_mapping.csv 查詢 drugbank_id 對應的台灣藥品")

        return result

    return predictions


if __name__ == "__main__":
    main()
