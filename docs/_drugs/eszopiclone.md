---
layout: default
title: Eszopiclone
parent: モデル予測のみ
nav_order: 121
evidence_level: L5
indication_count: 10
last_modified_at: 2026-10-15
description: "Eszopiclone：予測新適応症は入眠・睡眠維持障害 (sleep disorder, initiating and maintaining sleep)（エビデンスレベル L5）。既存適応症：催眠鎮静薬（不眠症）"
monitor_inn: "Eszopiclone"
predicted_indications: ["sleep disorder, initiating and maintaining sleep", "acute encephalopathy with biphasic seizures and late reduced diffusion", "restless legs syndrome", "benign paroxysmal torticollis of infancy", "agoraphobia", "hyperparathyroidism, primary, caused by water clear cell hyperplasia", "mitral valve prolapse, myxomatous", "fibrosis of extraocular muscles, congenital, with synergistic divergence", "triphalangeal thumb, Nonopposable", "sella turcica, bridged"]
---

# Eszopiclone
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

# エスゾピクロン：不眠症から入眠・睡眠維持障害へ

## 一言要約

エスゾピクロンは非ベンゾジアゼピン系の催眠鎮静薬（Z-drug）で、元々不眠症の治療に使用されていました。
TxGNN モデルは**入眠・睡眠維持障害 (sleep disorder, initiating and maintaining sleep)** に有効である可能性を予測しており、現在 **20 編の文献**がこの方向性を支持しています（臨床試験の登録はありません）。
ただし、この予測は既存適応症である不眠症とほぼ同じ領域のため、実質的には「新規適応症」というより既存適応の再確認に近い結果です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 催眠鎮静薬（不眠症） |
| 予測新規適応症 | 入眠・睡眠維持障害 (sleep disorder, initiating and maintaining sleep) |
| TxGNN 予測スコア | 97.93% |
| エビデンスレベル | L3（システマティックレビュー／メタ解析あり。完了した Phase 2/3 RCT のデータはなし） |
| 日本市販状況 | 販売中の承認なし（20 件すべて整理・取消済み） |
| 承認番号数 | 20 件（有効 0 件、取消 20 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。既知の薬理学によると、エスゾピクロンは非ベンゾジアゼピン系の Z-drug で、GABA-A 受容体を正に調節して抑制性神経伝達を高め、入眠と睡眠維持を促すと考えられています。

予測された「入眠・睡眠維持障害」は、既存適応症の不眠症とほぼ同じ病態を指します。そのため機序的な整合性は高く、スコアが高いのも自然です。ただし、これは新しい適応の発見ではなく、既存適応と重なる予測と考えるべきです。

なお、2 位以下の予測（急性脳症、むずむず脚症候群、広場恐怖症など）は、エビデンスが乏しいか、機序的な関連が確認できず、いずれも Hold 相当です。

## 文献エビデンス

臨床試験の登録はありません。文献は以下のとおりです。

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [35843245](https://pubmed.ncbi.nlm.nih.gov/35843245/) | 2022 | メタ解析 | Lancet | 成人の不眠症に対する薬物療法の急性期・長期効果を比較したネットワークメタ解析 |
| [36701954](https://pubmed.ncbi.nlm.nih.gov/36701954/) | 2023 | メタ解析 | Sleep Med Rev | 原発性不眠症に対する 20 種の薬剤の有効性と忍容性を比較 |
| [34121443](https://pubmed.ncbi.nlm.nih.gov/34121443/) | 2021 | メタ解析 | J Manag Care Spec Pharm | レンボレキサントと他の不眠症治療薬の有効性・安全性を比較 |
| [30303519](https://pubmed.ncbi.nlm.nih.gov/30303519/) | 2018 | システマティックレビュー | Cochrane Database Syst Rev | エスゾピクロンの不眠症に対する RCT エビデンスを統合 |
| [40202618](https://pubmed.ncbi.nlm.nih.gov/40202618/) | 2025 | RCT | Psychiatr Q | PTSD 退役軍人の不眠症と閉塞性睡眠時無呼吸の併存例で、行動療法にエスゾピクロンを追加（53 名、パイロット試験） |
| [40110890](https://pubmed.ncbi.nlm.nih.gov/40110890/) | 2025 | メタ解析 | Psychiatry Clin Neurosci | 不眠症状を伴ううつ病で、睡眠薬（Z-drug を含む）の併用療法を評価 |
| [27998379](https://pubmed.ncbi.nlm.nih.gov/27998379/) | 2017 | ガイドライン | J Clin Sleep Med | 米国睡眠医学会による慢性不眠症の薬物療法ガイドライン |
| [28671376](https://pubmed.ncbi.nlm.nih.gov/28671376/) | 2017 | Review | Am Fam Physician | Z-drug は、メラトニンやドキセピンが無効の場合に使用を検討 |
| [39923608](https://pubmed.ncbi.nlm.nih.gov/39923608/) | 2025 | ガイドライン | Sleep Med | 慢性不眠症における睡眠薬の切り替え・減薬に関する欧州の専門家合意 |
| [41187937](https://pubmed.ncbi.nlm.nih.gov/41187937/) | 2025 | Review | Arq Neuropsiquiatr | Z-drug の乱用・依存の診断と管理に関するブラジルのガイドライン |

## 日本市販情報

現在、有効な承認はなく、20 件すべてが取消済みです。主なものは以下のとおりです。

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 622148901 | ルネスタ錠２ｍｇ | 錠２ｍｇ | 催眠鎮静薬（不眠症） |
| 672149001 | ルネスタ錠３ｍｇ（選） | 錠３ｍｇ | 催眠鎮静薬（不眠症） |
| 622844601 | エスゾピクロン錠１ｍｇ「ケミファ」 | 錠１ｍｇ | 催眠鎮静薬（不眠症） |
| 622857001 | エスゾピクロン錠２ｍｇ「日医工」 | 錠２ｍｇ | 催眠鎮静薬（不眠症） |
| 622858601 | エスゾピクロン錠３ｍｇ「サワイ」 | 錠３ｍｇ | 催眠鎮静薬（不眠症） |

## 安全性に関する考慮事項

- **知識グラフ上の禁忌関連疾患**（添付文書の記載ではありません）：肝不全、不安障害、神経症性障害、気分変調性障害
- **薬物相互作用**：88 件が登録されています。重要度が高い（Major）主なものは以下のとおりです。
  - モルヒネ（リポソーム製剤を含む）：中枢抑制の増強
  - クラリスロマイシン：代謝阻害による血中濃度上昇の可能性
  - コビシスタット：代謝阻害による血中濃度上昇の可能性
- 中等度（Moderate）の主な相互作用：ブプロピオン、アプレピタント、デキサメタゾン、エタノール、プロメタジン、ミコナゾールなど
- Z-drug は依存・乱用のリスクがあり、推奨使用期間が短いことがガイドラインで指摘されています。

警告・禁忌の添付文書情報は、今回のデータには含まれていません。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 予測された適応症は既存の不眠症とほぼ同一で、新規適応としての価値は限定的です。
- 日本では有効な承認がすべて取消されており、再利用の検討以前に市販状況の確認が必要です。
- 添付文書の警告・禁忌が未取得のため、安全性評価に進めません。
- 臨床試験の登録がなく、他の予測疾患にも裏付けとなるエビデンスはありません。

**進める場合に必要なもの：**
- PMDA 添付文書の警告・禁忌情報の取得と解析
- 作用機序（MOA）データの補完
- 取消の経緯（販売中止か、制度上の整理か）の確認
- 不眠症以外の真に新規な適応（例：不眠を伴う併存疾患）に絞った再評価と、関連臨床試験の探索
- 依存・乱用リスクと、中枢抑制薬・CYP3A4 阻害薬との相互作用に関する管理計画
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

