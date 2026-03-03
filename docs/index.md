---
layout: home
title: JpTxGNN
---

# JpTxGNN - 日本医薬品リポジショニング予測システム

TxGNN 知識グラフを使用した日本の医薬品リポジショニング（ドラッグリポジショニング）予測システムです。

## 概要

本プロジェクトは、既存の承認医薬品に対する新たな適応症（効能・効果）の候補を、知識グラフ技術を用いて予測します。

### 主な機能

- **医薬品データベース**: PMDA/SSK 医薬品マスターとKEGG DRUGを統合
- **DrugBank マッピング**: 日本医薬品を国際標準識別子にマッピング
- **知識グラフ予測**: TxGNN を使用した薬物-疾病関係の予測
- **FHIR R4 API**: 標準化された医療情報交換フォーマット

### 統計

| 指標 | 数値 |
|------|------|
| 総医薬品数 | 19,317 |
| 適応症あり | 7,880 (40.8%) |
| DrugBankマッピング | 4,305 (22.5%) |
| 予測候補数 | 37,686 |

## 免責事項

**重要**: 本プロジェクトの結果は研究参考のみを目的としており、医療アドバイスを構成するものではありません。医薬品リポジショニング候補は臨床検証を経て初めて適用できます。

## クイックスタート

```bash
# リポジトリをクローン
git clone https://github.com/your-org/JpTxGNN.git
cd JpTxGNN

# 依存関係をインストール
uv sync

# 予測を実行
uv run python scripts/run_kg_prediction.py
```

## リンク

- [医薬品検索](/drugs/)
- [FHIR API](/fhir/metadata)
- [GitHub リポジトリ](https://github.com/your-org/JpTxGNN)

---

*TxGNN: Therapeutic knowledge graph neural network*
