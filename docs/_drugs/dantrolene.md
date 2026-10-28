---
layout: default
title: Dantrolene
parent: モデル予測のみ
nav_order: 102
evidence_level: L5
indication_count: 7
monitor_inn: "Dantrolene"
predicted_indications: ["moderate multiminicore disease with hand involvement", "King-Denborough syndrome", "congenital multicore myopathy with external ophthalmoplegia", "central core myopathy", "hypokalemic periodic paralysis", "thyrotoxic periodic paralysis", "myopathy, centronuclear"]
last_modified_at: 2026-10-27
description: "Dantrolene：予測新適応症は手の障害を伴う中等度マルチミニコア病 (moderate multiminicore disease with hand involvement)（エビデンスレベル L5）。既存適応症：日本の承認情報に適応症の記載なし"
---

# Dantrolene
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

## ダントロレン：骨格筋弛緩薬（RyR1 阻害） → 手の障害を伴う中等度マルチミニコア病 (moderate multiminicore disease with hand involvement)
{: .text-alpha }

## 一言要約

ダントロレンは、骨格筋の小胞体にあるリアノジン受容体 1 (RyR1) の阻害が想定される骨格筋弛緩薬です。日本ではカプセル剤と静注用製剤が承認されています。
TxGNN モデルは **手の障害を伴う中等度マルチミニコア病 (moderate multiminicore disease with hand involvement)** に有効である可能性を予測しています。
ただし、この疾患を直接検討した臨床試験と文献は **0 件**で、根拠はモデル予測のみです。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 手の障害を伴う中等度マルチミニコア病 (moderate multiminicore disease with hand involvement) |
| TxGNN 予測スコア | 0.9990 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 2 件／全 2 件） |
| 承認番号数 | 2 件（有効 2 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。ただし、ダントロレンは RyR1 を介した小胞体からのカルシウム放出を抑える薬剤として知られています。

マルチミニコア病は、RYR1 または SEPN1 の変異と関連することが多い先天性ミオパチーです。RYR1 の異常があるタイプでは、カルシウム放出の調節障害が病態に関わると考えられます。このため、RyR1 を阻害するダントロレンには機序的に検討する余地があります。

ただし、これは仮説の段階です。今回まとめたデータには、この疾患を直接対象とした研究は含まれていません。臨床的な有効性や安全性は未検証です。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

## 日本市販情報

| 承認番号 | 商品名 | 剤形 |
|---------|------|------|
| 620003574 | ダントリウムカプセル２５ｍｇ | カプセル２５ｍｇ |
| 620003753 | ダントリウム静注用２０ｍｇ | 注用２０ｍｇ |

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用データベースで 72 件の相互作用が登録されています。主なものは次のとおりです。
  - **重大 (Major)**：モルヒネ、モルヒネ（リポソーム製剤）
  - **中等度 (Moderate)**：ドロナビノール、メトクロプラミド、ナビロン、ナルトレキソン、アヘン、シブトラミン、エタノール、プロメタジン

その他の警告・禁忌については、添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測スコアは高いものの、この疾患を直接検討した臨床試験や文献がなく、根拠はモデル予測のみ（L5）です。現時点では研究課題として位置づけ、投資や開発を進める段階ではありません。

**進める場合に必要なもの：**
- 手の障害を伴う中等度マルチミニコア病における RYR1 / SEPN1 変異との関連を示す、疾患特異的な文献調査
- 前臨床研究（患者由来細胞でのカルシウム放出に対するダントロレンの効果）
- 詳細な作用機序 (MOA) データの整備
- 添付文書の警告・禁忌の確認と、安全性評価（肝機能、筋力低下、併用薬との相互作用）
- 対象疾患の患者数と、既存製剤の剤形・投与経路の適合性の評価
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**販売名（規格別）**：ダントリウムカプセル25mg、ダントリウム静注用20mg
<!-- brand-names:end -->

