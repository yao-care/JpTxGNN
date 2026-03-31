# JpTxGNN - 日本：ドラッグリポジショニング予測

[![Website](https://img.shields.io/badge/Website-jptxgnn.yao.care-blue)](https://jptxgnn.yao.care)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

TxGNNモデルを使用した日本の医薬品に対するドラッグリポジショニング（既存薬再利用）予測。

## 注意事項

- 本プロジェクトの結果は研究目的のみであり、医療アドバイスを構成するものではありません。
- ドラッグリポジショニング候補は適用前に臨床検証が必要です。

## プロジェクト概要

| 項目 | 数値 |
|------|------|
| **医薬品レポート** | 191 |
| **予測総数** | 12,395,216 |

## 予測方法

### 知識グラフ法（Knowledge Graph）
TxGNN知識グラフにおける薬物-疾患関係を直接クエリし、生物医学ネットワークの既存の接続に基づいて潜在的なリポジショニング候補を特定します。

### 深層学習法（Deep Learning）
TxGNN事前学習済みニューラルネットワークモデルを使用して予測スコアを計算し、承認済み医薬品の新しい治療適応症の可能性を評価します。

## リンク

- ウェブサイト: https://jptxgnn.yao.care
- TxGNN論文: https://doi.org/10.1038/s41591-023-02233-x
