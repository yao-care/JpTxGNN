# JpTxGNN - 日本医療用医薬品ドラッグリポジショニング予測

[![Website](https://img.shields.io/badge/Website-jptxgnn.yao.care-blue)](https://jptxgnn.yao.care)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

TxGNN 知識グラフと深層学習モデルを使用した日本医療用医薬品のドラッグリポジショニング（既存薬再利用）予測システム。

## 注意事項

- 本プロジェクトの結果は**研究参考のみ**を目的としており、医療アドバイスを構成するものではありません
- ドラッグリポジショニング候補は臨床検証を経て初めて適用できます

## プロジェクト成果概要

### 予測統計

| 項目 | 数値 |
|------|------|
| **対象医薬品** | 3,824 種 |
| **DrugBank マッピング** | 142 種 |
| **KG 予測候補** | 33,901 件 |
| **DL 予測候補** | 2,419,822 件 |
| **統合予測（≥90%信頼度）** | 155,638 件 |

### データソース

| データ | ソース | 説明 |
|--------|--------|------|
| 医薬品データ | 日本 SSK 医療用医薬品 | 19,317 件 |
| 薬効分類 | KEGG DRUG | 効能・効果情報 |
| 知識グラフ | Harvard TxGNN | 17,080 疾患、7,957 薬物 |

---

## 予測方法

TxGNN は2種類の予測方法を提供します：

| 方法 | 速度 | 精度 | 環境要件 |
|------|------|------|----------|
| 知識グラフ法 | 速い（数分） | 中 | 特別な要件なし |
| 深層学習法 | 遅い（数時間） | 高 | Conda + PyTorch + DGL |

### 知識グラフ法（KG）

```bash
uv run python scripts/run_kg_prediction.py
```

TxGNN 知識グラフ内の既知の薬物-疾患関係を直接クエリします。

**出力ファイル**：`data/processed/repurposing_candidates.csv`

### 深層学習法（DL）

```bash
# conda 環境で実行（PyTorch + DGL が必要）
source ~/miniforge3/bin/activate txgnn
PYTHONPATH=src python -m jptxgnn.predict.txgnn_model
```

TxGNN 事前学習済みニューラルネットワークモデルで予測スコアを計算します。

**出力ファイル**：`data/processed/txgnn_dl_predictions.csv`

### TxGNN スコアの解釈

TxGNN スコアは「薬物-疾患」ペアに対するモデルの予測信頼度を表し、範囲は 0-1 です。

| 閾値 | 意味 | 推奨用途 |
|------|------|----------|
| ≥ 0.99 | 非常に高い信頼度 | 優先的に検証 |
| ≥ 0.90 | 高い信頼度 | 詳細調査推奨 |
| ≥ 0.50 | 中程度の信頼度 | 参考情報 |
| < 0.50 | 低い信頼度 | 追加検証必要 |

---

## クイックスタート

### ステップ 1：データのダウンロード

| ファイル | ダウンロード | 配置場所 | 用途 |
|----------|--------------|----------|------|
| node.csv | [Harvard Dataverse](https://dataverse.harvard.edu/api/access/datafile/7144482) | `data/node.csv` | ノードデータ |
| kg.csv | [Harvard Dataverse](https://dataverse.harvard.edu/api/access/datafile/7144484) | `data/kg.csv` | 知識グラフ |
| edges.csv | [Harvard Dataverse](https://dataverse.harvard.edu/api/access/datafile/7144483) | `data/edges.csv` | エッジデータ（DL用） |
| model_ckpt.zip | [Google Drive](https://drive.google.com/uc?id=1fxTFkjo2jvmz9k6vesDbCeucQjGRojLj) | `model_ckpt/` に解凍 | 事前学習モデル（DL用） |

### ステップ 2：環境のセットアップ

```bash
# 依存関係のインストール
uv sync

# テストの実行
uv run pytest tests/
```

### ステップ 3：FDA データの処理

```bash
uv run python scripts/process_fda_data.py
```

### ステップ 4：語彙データの準備

```bash
uv run python scripts/prepare_external_data.py
```

### ステップ 5：KG 予測の実行

```bash
uv run python scripts/run_kg_prediction.py
```

### ステップ 6：深層学習環境のセットアップ（オプション）

```bash
# 1. conda 環境の作成
conda create -n txgnn python=3.11 -y
conda activate txgnn

# 2. PyTorch のインストール
pip install torch==2.2.2 torchvision==0.17.2

# 3. DGL のインストール
pip install dgl==1.1.3

# 4. TxGNN のインストール
pip install git+https://github.com/mims-harvard/TxGNN.git

# 5. その他の依存関係
pip install pandas tqdm pyyaml pydantic ogb

# 6. インストールの確認
python -c "import torch; import dgl; import txgnn; print('インストール成功！')"
```

**注意**：Apple Silicon (M1/M2/M3) では DGL は MPS をサポートしていないため、CPU モードで動作します。

### ステップ 7：DL 予測の実行（オプション）

```bash
conda activate txgnn
PYTHONPATH=src python -m jptxgnn.predict.txgnn_model
```

中断後も再開可能（チェックポイント対応）。

---

## FHIR API

本プロジェクトは HL7 FHIR R4 準拠の API を提供します。

### エンドポイント

| リソース | URL |
|----------|-----|
| CapabilityStatement | `https://jptxgnn.yao.care/fhir/metadata` |
| MedicationKnowledge | `https://jptxgnn.yao.care/fhir/MedicationKnowledge/{id}.json` |
| ClinicalUseDefinition | `https://jptxgnn.yao.care/fhir/ClinicalUseDefinition/{id}.json` |
| Bundle | `https://jptxgnn.yao.care/fhir/Bundle/all-predictions.json` |

### 統計

| リソースタイプ | 数量 |
|---------------|------|
| MedicationKnowledge | 3,824 |
| ClinicalUseDefinition | 155,638 |

---

## ディレクトリ構造

```
JpTxGNN/
├── README.md                    # プロジェクト文書
├── CLAUDE.md                    # AI アシスタントガイド
├── pyproject.toml               # Python パッケージ設定
│
├── data/                        # データディレクトリ
│   ├── kg.csv                   # 🟡 TxGNN 知識グラフ
│   ├── node.csv                 # 🟡 TxGNN ノードデータ
│   ├── edges.csv                # 🟡 TxGNN エッジデータ
│   ├── raw/
│   │   ├── jp_fda_drugs.json    # 🟢 日本医薬品データ（SSK + KEGG）
│   │   ├── jp_ssk_drugs.json    # 🟢 SSK 医療用医薬品
│   │   └── jp_kegg_drugs.json   # 🟢 KEGG 薬効情報
│   ├── external/                # 🔵 prepare_external_data.py により生成
│   │   ├── drugbank_vocab.csv
│   │   ├── disease_vocab.csv
│   │   └── drug_disease_relations.csv
│   ├── processed/
│   │   ├── drug_mapping.csv             # 🔵 日本医薬品→DrugBank マッピング
│   │   ├── indication_mapping.csv       # 🔵 適応症→疾患マッピング
│   │   ├── repurposing_candidates.csv   # 🔵 KG 法結果
│   │   └── txgnn_dl_predictions.csv     # 🔵 DL 法結果
│   └── news/
│       ├── keywords.json
│       └── matched_news.json
│
├── model_ckpt/                  # 🟡 TxGNN 事前学習モデル
│
├── src/jptxgnn/                 # 🔵 コアコード
│   ├── data/
│   │   └── loader.py
│   ├── mapping/
│   │   ├── normalizer.py
│   │   ├── drugbank_mapper.py
│   │   └── disease_mapper.py
│   ├── predict/
│   │   ├── repurposing.py
│   │   └── txgnn_model.py
│   └── collectors/
│
├── scripts/                     # 🔵 実行スクリプト
│   ├── process_fda_data.py
│   ├── prepare_external_data.py
│   ├── run_kg_prediction.py
│   ├── generate_search_index.py
│   ├── generate_fhir_resources.py
│   └── generate_drug_pages.py
│
├── docs/                        # 🔵 Jekyll ウェブサイト
│   ├── _config.yml
│   ├── drugs/
│   ├── fhir/
│   └── data/
│
└── tests/                       # 🔵 テスト
```

**凡例**：🔵 プロジェクト開発 | 🟢 日本データ | 🟡 TxGNN データ

---

## 関連リソース

- [TxGNN 論文](https://www.nature.com/articles/s41591-024-03233-x)
- [TxGNN GitHub](https://github.com/mims-harvard/TxGNN)
- [TxGNN Explorer](http://txgnn.org) - インタラクティブ予測クエリ
- [TwTxGNN](https://twtxgnn.yao.care) - 台湾版 TxGNN

---

## 引用

本データセットまたはソフトウェアを使用する場合は、以下を引用してください：

```bibtex
@software{jptxgnn2026,
  author       = {Yao.Care},
  title        = {JpTxGNN: Drug Repurposing Predictions for Japanese Medicines},
  year         = 2026,
  url          = {https://github.com/yao-care/JpTxGNN}
}
```

また、TxGNN の原著論文も引用してください：

```bibtex
@article{huang2024txgnn,
  title={A foundation model for clinician-centered drug repurposing},
  author={Huang, Kexin and Chandak, Payal and Wang, Qianwen and Haber, Shreyas and Zitnik, Marinka},
  journal={Nature Medicine},
  year={2024},
  doi={10.1038/s41591-024-03233-x}
}
```

---

## ライセンス

MIT License - 研究目的での使用を推奨します。

**免責事項**：本プロジェクトの予測結果は研究参考のみを目的としており、臨床決定に直接使用することは推奨されません。
