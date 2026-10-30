# JpTxGNN - Japan: Drug Repurposing Predictions

> 本專案由 **藥提醒科技有限公司**（[yao.care](https://www.yao.care)）開發與維運。
> JpTxGNN 站台：<https://jptxgnn.yao.care/>｜產品總覽：<https://www.yao.care/medical/txgnn/>

[![Website](https://img.shields.io/badge/Website-jptxgnn.yao.care-blue)](https://jptxgnn.yao.care)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Japan PMDA承認医薬品のTxGNNモデルによるドラッグリポジショニング予測。

## 免責事項

- 本プロジェクトの結果は研究目的のみであり、医療アドバイスを構成するものではありません。
- ドラッグリポジショニング候補は、適用前に臨床検証が必要です。

## プロジェクト概要

### レポート統計

| 項目 | 数量 |
|------|------|
| **医薬品レポート** | 385 |
| **予測総数** | 12,395,216 |
| **ユニーク医薬品数** | 426 |
| **ユニーク適応症数** | 15,003 |
| **DDIデータ** | 302,516 |
| **DFIデータ** | 857 |
| **DHIデータ** | 35 |
| **DDSIデータ** | 8,359 |
| **FHIRリソース** | 124 MK / 1,204 CUD |

### エビデンスレベル分布

| エビデンスレベル | レポート数 | 説明 |
|---------|-------|------|
| **L1** | 13 | 複数のPhase 3 RCT |
| **L2** | 23 | 単一RCTまたは複数のPhase 2 |
| **L3** | 33 | 観察研究 |
| **L4** | 25 | 前臨床/メカニズム研究 |
| **L5** | 97 | 計算予測のみ |

### ソース別

| ソース | 予測数 |
|------|------|
| DL | 12,392,270 |
| KG + DL | 2,555 |
| KG | 391 |

### 信頼度別

| 信頼度 | 予測数 |
|------|------|
| very_high | 1,940 |
| high | 589,840 |
| medium | 1,079,027 |
| low | 10,724,409 |

---

## 予測方法

| 方法 | 速度 | 精度 | 要件 |
|------|------|--------|----------|
| 知識グラフ | 高速（秒単位） | 低い | 特別な要件なし |
| ディープラーニング | 低速（時間単位） | 高い | Conda + PyTorch + DGL |

### 知識グラフ方法

```bash
uv run python scripts/run_kg_prediction.py
```

| 指標 | 値 |
|------|------|
| PMDA 医薬品総数 | 19,148 |
| リポジショニング候補 | 2,946 |

### ディープラーニング方法

```bash
conda activate txgnn
PYTHONPATH=src python -m jptxgnn.predict.txgnn_model
```

| 指標 | 値 |
|------|------|
| DL予測総数 | 734,252 |
| ユニーク医薬品数 | 426 |
| ユニーク適応症数 | 15,003 |

### スコア解釈

TxGNNスコアは、医薬品-疾患ペアに対するモデルの信頼度を表し、0から1の範囲です。

| 閾値 | 意味 |
|-----|------|
| >= 0.9 | 非常に高い信頼度 |
| >= 0.7 | 高い信頼度 |
| >= 0.5 | 中程度の信頼度 |

#### スコア分布

| 閾値 | 意味 |
|-----|------|
| ≥ 0.9999 | 極めて高い信頼度、モデルの最も確信のある予測 |
| ≥ 0.99 | 非常に高い信頼度、検証の優先順位付けに値する |
| ≥ 0.9 | 高い信頼度 |
| ≥ 0.5 | 中程度の信頼度（シグモイド決定境界） |

#### エビデンスレベルの定義

| レベル | 定義 | 臨床的意義 |
|-----|------|---------|
| L1 | 第3相RCTまたはシステマティックレビュー | 臨床使用を支持できる |
| L2 | 第2相RCT | 使用を検討できる |
| L3 | 第1相または観察研究 | 更なる評価が必要 |
| L4 | 症例報告または前臨床研究 | まだ推奨されない |
| L5 | 計算予測のみ、臨床エビデンスなし | 更なる研究が必要 |

#### 重要な注意事項

1. **高スコアは臨床的有効性を保証しません：TxGNNスコアは知識グラフベースの予測であり、臨床試験による検証が必要です。**
2. **低スコアは無効を意味しません：モデルが特定の関連性を学習していない可能性があります。**
3. **検証パイプラインとの併用を推奨：本プロジェクトのツールを使用して、臨床試験、文献、その他のエビデンスを確認してください。**

### 検証パイプライン

```mermaid
flowchart TD
    A["TxGNN予測結果"] --> B
    subgraph B["Step 1: DrugBundle Collector"]
        B1["医薬品レベル: PMDA, DDI, DrugBank"]
        B2["適応症レベル: ClinicalTrials, PubMed, ICTRP"]
    end
    B --> |"drug_bundle.json"| C
    subgraph C["Step 2: Evidence Pack Generator"]
        C1["プログラマティックデータ転送 (100%)"]
        C2["+ LLM 分析 (L1-L5)"]
    end
    C --> |"drug_evidence_pack.json/md"| D
    subgraph D["Step 3: Notes Writer"]
        D1["drug_pharmacist_notes.md"]
        D2["drug_sponsor_notes.md"]
    end
```

---

## クイックスタート

### ステップ 1: データのダウンロード

| ファイル | ダウンロード |
|------|------|
| PMDA データ | データソース |
| node.csv | [Harvard Dataverse](https://dataverse.harvard.edu/api/access/datafile/7144482) |
| kg.csv | [Harvard Dataverse](https://dataverse.harvard.edu/api/access/datafile/7144484) |
| edges.csv | [Harvard Dataverse](https://dataverse.harvard.edu/api/access/datafile/7144483) |
| model_ckpt.zip | [Google Drive](https://drive.google.com/uc?id=1fxTFkjo2jvmz9k6vesDbCeucQjGRojLj) |

### ステップ 2: 依存関係のインストール

```bash
uv sync
```

### ステップ 3: 医薬品データの処理

```bash
uv run python scripts/process_fda_data.py
```

### ステップ 4: 語彙データの準備

```bash
uv run python scripts/prepare_external_data.py
```

### ステップ 5: 知識グラフ予測の実行

```bash
uv run python scripts/run_kg_prediction.py
```

### ステップ 6: ディープラーニング環境のセットアップ

```bash
conda create -n txgnn python=3.11 -y
conda activate txgnn
pip install torch==2.2.2 torchvision==0.17.2
pip install dgl==1.1.3
pip install git+https://github.com/mims-harvard/TxGNN.git
pip install pandas tqdm pyyaml pydantic ogb
```

### ステップ 7: ディープラーニング予測の実行

```bash
conda activate txgnn
PYTHONPATH=src python -m jptxgnn.predict.txgnn_model
```

---

## リソース

### TxGNN コア

- [TxGNN Paper](https://www.nature.com/articles/s41591-024-03233-x) - Nature Medicine, 2024
- [TxGNN GitHub](https://github.com/mims-harvard/TxGNN)
- [TxGNN Explorer](http://txgnn.org)

### データソース

| カテゴリ | データ | ソース | 備考 |
|------|------|------|------|
| **医薬品データ** | PMDA | - | Japan |
| **知識グラフ** | TxGNN KG | [Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IXA7BM) | 17,080 diseases, 7,957 drugs |
| **医薬品データベース** | DrugBank | [DrugBank](https://go.drugbank.com/) | 医薬品成分マッピング |
| **薬物相互作用** | DDInter 2.0 | [DDInter](https://ddinter2.scbdd.com/) | DDIペア |
| **薬物相互作用** | Guide to PHARMACOLOGY | [IUPHAR/BPS](https://www.guidetopharmacology.org/) | 承認薬物相互作用 |
| **臨床試験** | ClinicalTrials.gov | [CT.gov API v2](https://clinicaltrials.gov/data-api/api) | 臨床試験登録 |
| **臨床試験** | WHO ICTRP | [ICTRP API](https://apps.who.int/trialsearch/api/v1/search) | 国際臨床試験プラットフォーム |
| **文献** | PubMed | [NCBI E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/) | 医学文献検索 |
| **名称マッピング** | RxNorm | [RxNav API](https://rxnav.nlm.nih.gov/REST) | 医薬品名標準化ブリッジ |
| **名称マッピング** | PubChem | [PUG-REST API](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest) | 化学物質同義語検索 |
| **名称マッピング** | ChEMBL | [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data) | 生物活性データベース |
| **標準規格** | FHIR R4 | [HL7 FHIR](http://hl7.org/fhir/) | MedicationKnowledge, ClinicalUseDefinition |
| **標準規格** | SMART on FHIR | [SMART Health IT](https://smarthealthit.org/) | EHR統合、OAuth 2.0 + PKCE |

### モデルダウンロード

| ファイル | ダウンロード | 備考 |
|------|------|------|
| 事前学習済みモデル | [Google Drive](https://drive.google.com/uc?id=1fxTFkjo2jvmz9k6vesDbCeucQjGRojLj) | model_ckpt.zip |
| node.csv | [Harvard Dataverse](https://dataverse.harvard.edu/api/access/datafile/7144482) | ノードデータ |
| kg.csv | [Harvard Dataverse](https://dataverse.harvard.edu/api/access/datafile/7144484) | 知識グラフデータ |
| edges.csv | [Harvard Dataverse](https://dataverse.harvard.edu/api/access/datafile/7144483) | エッジデータ（DL用） |

## プロジェクト紹介

### ディレクトリ構造

```
JpTxGNN/
├── README.md
├── CLAUDE.md
├── pyproject.toml
│
├── config/
│   └── fields.yaml
│
├── data/
│   ├── kg.csv
│   ├── node.csv
│   ├── edges.csv
│   ├── raw/
│   ├── external/
│   ├── processed/
│   │   ├── drug_mapping.csv
│   │   ├── repurposing_candidates.csv
│   │   ├── txgnn_dl_predictions.csv.gz
│   │   └── integration_stats.json
│   ├── bundles/
│   └── collected/
│
├── src/jptxgnn/
│   ├── data/
│   │   └── loader.py
│   ├── mapping/
│   │   ├── normalizer.py
│   │   ├── drugbank_mapper.py
│   │   └── disease_mapper.py
│   ├── predict/
│   │   ├── repurposing.py
│   │   └── txgnn_model.py
│   ├── collectors/
│   └── paths.py
│
├── scripts/
│   ├── process_fda_data.py
│   ├── prepare_external_data.py
│   ├── run_kg_prediction.py
│   └── integrate_predictions.py
│
├── docs/
│   ├── _drugs/
│   ├── fhir/
│   │   ├── MedicationKnowledge/
│   │   └── ClinicalUseDefinition/
│   └── smart/
│
├── model_ckpt/
└── tests/
```

**凡例**: 🔵 プロジェクト開発 | 🟢 ローカルデータ | 🟡 TxGNNデータ | 🟠 検証パイプライン

### データフロー

```mermaid
flowchart TD
    FDA["PMDA データ"] --> proc["process_fda_data.py"]
    TxGNN["TxGNN データ"] --> prep["prepare_external_data.py"]

    proc --> json["jp_fda_drugs.json"]
    prep --> ext["data/external/"]

    json --> norm["normalizer.py"]
    ext --> norm

    norm --> drug_map["drug_mapping.csv"]
    drug_map --> ind_map["indication_mapping.csv"]

    ind_map --> KG["知識グラフ"]
    ind_map --> DL["ディープラーニング"]

    KG --> kg_out["repurposing_candidates.csv"]
    DL --> dl_out["txgnn_dl_predictions.csv"]
```

---

## 引用

このデータセットまたはソフトウェアを使用する場合は、以下を引用してください：

```bibtex
@software{jptxgnn2026,
  author       = {Yao.Care},
  title        = {JpTxGNN: Drug Repurposing Validation Reports for Japan PMDA Drugs},
  year         = 2026,
  publisher    = {GitHub},
  url          = {https://github.com/yao-care/JpTxGNN}
}
```

TxGNNの原著論文も引用してください：

```bibtex
@article{huang2023txgnn,
  title={A foundation model for clinician-centered drug repurposing},
  author={Huang, Kexin and Chandak, Payal and Wang, Qianwen and Haber, Shreyas and Zitnik, Marinka},
  journal={Nature Medicine},
  year={2024},
  doi={10.1038/s41591-024-03233-x}
}
```

<!-- txgnn-ops:start -->
## 維運：資料還原與許可證更新

### 完整還原

git 只放程式碼與網站頁面；許可證原始資料、證據包、藥師報告原稿、預測結果放在本 repo 的 Release。

```bash
git clone https://github.com/yao-care/jptxgnn.git && cd jptxgnn
uv sync                                  # Python 相依套件
bash scripts/restore_data.sh             # 取最新的 data-* Release，還原 data/（含校驗）
bash scripts/restore_data.sh --with-kg   # 另加共用知識圖譜與預測模型（只有重跑預測才需要）
```

需要 [GitHub CLI](https://cli.github.com/)（`gh auth login`）與 [uv](https://docs.astral.sh/uv/)。

### 改頁工具鏈

事實層、checker、許可證狀態計算等放在 `tools/txgnn/.claude/`，是母 repo `yao-care/txgnn` 的 `.claude/` 複本（版本見 `tools/txgnn/VERSION`）。
規則要改請改母 repo，再用 `python3 .claude/sync_site_tools.py JpTxGNN` 同步過來，不要直接改這裡的複本。
在本 repo 單獨使用時，先組工作目錄：

```bash
WS=$(bash scripts/txgnn_ws.sh)
cd "$WS"
python3 .claude/dump_license_facts_20261021.py JpTxGNN       # 依證據包算市場狀態（checker 要用）
python3 .claude/checker_trend.py --no-append JpTxGNN           # 全部藥物頁 checker，必須「非 0 0」
```

### 許可證排程更新（GitHub Actions）

`.github/workflows/license-refresh.yml` 每週一 UTC 03:17 自動執行，也可以在 Actions 頁手動觸發（可選只試跑）：

1. 從 Release 還原 `data/`（`scripts/restore_data.sh`）
2. 從主管機關下載最新許可證資料（`scripts/license_adapter.py`），檢查筆數與格式
3. 更新證據包的許可證狀態 → 重算市場狀態 → 同步許可證表 → 事實層改頁 → checker 全量必須 0 → 衍生檔 → gate
4. 全部通過才推上 `main` 並觸發部署；更新後的 `data/` 另存成新的 `data-YYYYMMDD` Release

以下情況一律不推、自動開 issue（label `license-refresh`）：下載失敗或格式改變、狀態變動超過兩成、
改到的藥物頁超過 min(200, 5%)、checker／gate／h1 沒過、有人工查核紀錄的頁會被改到。全程不使用 AI。
<!-- txgnn-ops:end -->
