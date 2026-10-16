---
layout: default
title: Felbinac
parent: モデル予測のみ
nav_order: 130
evidence_level: L5
indication_count: 10
last_modified_at: 2026-10-15
description: "Felbinac：予測新適応症はbrachyolmia-amelogenesis imperfecta syndrome（エビデンスレベル L5）。既存適応症：鎮痛薬、抗炎症薬、シクロオキシゲナーゼ阻害薬"
monitor_inn: "felbinac"
predicted_indications: ["brachyolmia-amelogenesis imperfecta syndrome", "acromesomelic dysplasia, Hunter-Thompson type", "myosclerosis", "brachyolmia", "pseudoachondroplasia", "spondyloarthropathy, susceptibility to", "rheumatoid nodulosis", "combined immunodeficiency due to moesin deficiency", "rheumatoid factor-positive polyarticular juvenile idiopathic arthritis", "juvenile idiopathic arthritis"]
---

# Felbinac
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **10** 件
{: .fs-6 .fw-300 }

---

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist">

## 薬剤師評価レポート

</div>

# フェルビナク：鎮痛・抗炎症から先天性骨系統疾患（brachyolmia-amelogenesis imperfecta syndrome）へ

## 一言要約

フェルビナクは、シクロオキシゲナーゼ（COX）阻害作用を持つ鎮痛・抗炎症薬で、日本では貼付剤（テープ）として使用されてきました。
TxGNN モデルは **brachyolmia-amelogenesis imperfecta syndrome** に有効である可能性を予測していますが、現時点で裏付けとなる**臨床試験・文献はありません**（モデル予測のみ）。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 鎮痛薬、抗炎症薬、シクロオキシゲナーゼ阻害薬 |
| 予測新規適応症 | brachyolmia-amelogenesis imperfecta syndrome |
| TxGNN 予測スコア | 99.99% |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売なし（承認はすべて整理済み） |
| 承認番号数 | 9 件（すべて整理済み） |
| 推奨決定 | Hold |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。既知の情報によると、フェルビナクは NSAID（COX 阻害薬）で、疼痛や炎症の症状緩和に使われてきた外用薬です。

一方、予測された brachyolmia-amelogenesis imperfecta syndrome は、骨格と歯のエナメル質に影響する遺伝性の形成異常です。COX 阻害と、この疾患の病態との間に確立された関連は見つかっておらず、**この予測は機序的に裏付けられていません**。

参考として、同じ上位スコア群（brachyolmia、acromesomelic dysplasia、pseudoachondroplasia など）も、ほとんどが遺伝性骨格異形成です。これらは症状（関節痛など）の緩和以外に、フェルビナクが病態に作用する根拠はありません。一方、下位の候補である脊椎関節症や若年性特発性関節炎は、NSAID が症状管理に使われるため間接的な妥当性はありますが、フェルビナク固有のエビデンスはありません。

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 621521801 | フェルビナクテープ70mg「久光」 10cm×14cm | テープ | 鎮痛薬、抗炎症薬、シクロオキシゲナーゼ阻害薬 |
| 622036801 | セルタッチテープ70 10cm×14cm | テープ | 鎮痛薬、抗炎症薬、シクロオキシゲナーゼ阻害薬 |
| 621478701 | フェルビナクテープ35mg「三笠」 7cm×10cm | テープ | 鎮痛薬、抗炎症薬、シクロオキシゲナーゼ阻害薬 |
| 621981802 | フェルビナクテープ35mg「NP」 7cm×10cm | テープ | 鎮痛薬、抗炎症薬、シクロオキシゲナーゼ阻害薬 |
| 620646303 | フェルビナクテープ70mg「NP」 10cm×14cm | テープ | 鎮痛薬、抗炎症薬、シクロオキシゲナーゼ阻害薬 |

上記を含む 9 件の承認はすべて整理済みで、現在有効な承認はありません。

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 予測はモデルスコアのみに基づき、臨床試験も文献もありません（L5）。
- 上位候補は遺伝性骨格異形成で、COX 阻害との機序的関連が認められません。
- 国内の承認もすべて整理済みです。

**進める場合に必要なもの：**
- 詳細な薬物作用機序データ（MOA）
- 添付文書に基づく警告・禁忌情報の取得と安全性評価
- 予測疾患とフェルビナクの関連を示す前臨床または臨床の根拠
- 外用（貼付）という投与経路が対象疾患に適合するかの検証
- 機序的妥当性がより高い候補（脊椎関節症、若年性特発性関節炎など）の個別評価
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

