---
layout: default
title: Celecoxib
parent: モデル予測のみ
nav_order: 81
evidence_level: L5
indication_count: 7
monitor_inn: "Celecoxib"
predicted_indications: ["acromesomelic dysplasia, Hunter-Thompson type", "brachyolmia-amelogenesis imperfecta syndrome", "myosclerosis", "hypermobility of coccyx", "brachyolmia", "rheumatoid nodulosis", "WHIM syndrome"]
last_modified_at: 2026-10-27
description: "Celecoxib：予測新適応症は先端中間肢異形成症 Hunter-Thompson 型 (acromesomelic dysplasia, Hunter-Thompson type)（エビデンスレベル L5）。既存適応症：日本の承認情報に適応症の記載なし"
---

# Celecoxib
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **7** 件
{: .fs-6 .fw-300 }

---

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist" markdown="1">

## 薬剤師評価レポート

</div>

## セレコキシブ：COX-2 阻害薬 → 先端中間肢異形成症 Hunter-Thompson 型 (acromesomelic dysplasia, Hunter-Thompson type)
{: .text-alpha }

## 一言要約

セレコキシブは、選択的シクロオキシゲナーゼ2（COX-2）阻害作用をもつ鎮痛・抗炎症薬です。
TxGNN モデルは**先端中間肢異形成症 Hunter-Thompson 型 (acromesomelic dysplasia, Hunter-Thompson type)** に有効である可能性を予測していますが、関連する臨床試験・文献は **0 件**で、予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 先端中間肢異形成症 Hunter-Thompson 型 (acromesomelic dysplasia, Hunter-Thompson type) |
| TxGNN 予測スコア | 0.9988 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 20 件以上） |
| 承認番号数 | 20 件以上 |
| 推奨決定 | Hold |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。公知の情報では、セレコキシブは選択的 COX-2 阻害薬で、プロスタグランジンを介した炎症を抑える薬剤です。

一方、この疾患は CDMP1/GDF5 に関連する遺伝性の骨格異形成で、炎症性の要素はほとんどありません。COX-2 阻害との機序的なつながりは見当たらず、今回のスコアはデータ上の関連性に基づくもので、生物学的な裏付けは乏しいと考えられます。

## 安全性に関する考慮事項

- **薬物相互作用**：データ上、100 件の相互作用が登録されています。主なものは次のとおりです。
  - 重大（Major）：エリグルスタット
  - 中等度（Moderate）：ヒドロコルチゾン、メトホルミン、シメチジン、レボフロキサシン、メトロニダゾール、ナルトレキソン、メサラジン、および複数のスルホニル尿素系血糖降下薬（グリメピリド、グリピジド、グリベンクラミドなど）

その他の警告・禁忌については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 裏付けとなる臨床試験も文献もなく、エビデンスはモデル予測のみ（L5）です。
- 疾患の成因（遺伝性骨格異形成）と COX-2 阻害の間に妥当な機序的関連が見いだせません。

**進める場合に必要なもの：**
- 疾患の病態と COX-2 経路の関連を示す前臨床研究・機序研究
- 詳細な作用機序データ（MOA）の補完
- 添付文書の警告・禁忌情報の確認（PMDA）
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：セレコックス

**販売名（規格別）**：セレコキシブ100mg錠、セレコキシブ200mg錠、セレコキシブ錠100mg、セレコキシブ錠200mg、セレコックス錠100mg、セレコックス錠200mg
<!-- brand-names:end -->

