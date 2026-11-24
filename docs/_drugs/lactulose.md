---
layout: default
title: Lactulose
parent: モデル予測のみ
nav_order: 199
evidence_level: L5
indication_count: 8
monitor_inn: "Lactulose"
predicted_indications: ["acute urate nephropathy", "nephrolithiasis", "obstructive jaundice", "bile duct disease", "biliary tract disease", "hyperphosphatemia (disease)", "exercise-induced malignant hyperthermia", "bile duct neoplasm"]
last_modified_at: 2026-11-24
description: "Lactulose：予測新適応症は急性尿酸性腎症 (acute urate nephropathy)（エビデンスレベル L5）。薬価基準の品目：7 件（現在収載 5 件）"
---

# Lactulose
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **8** 件
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

## ラクツロース：浸透圧性の合成二糖類（腸内アンモニア低減作用） → 急性尿酸性腎症 (acute urate nephropathy)
{: .text-alpha }

## 一言要約

ラクツロースは、消化管で吸収されにくい合成二糖類で、浸透圧作用と腸内でのアンモニア低減作用を持つ薬です。
TxGNN モデルは**急性尿酸性腎症 (acute urate nephropathy)** に有効である可能性を予測していますが、今回まとめたデータには、この疾患を直接検討した臨床試験や文献は **0 件**です。現時点ではモデル予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 急性尿酸性腎症 (acute urate nephropathy) |
| TxGNN 予測スコア | 0.9989 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 5 件／全 7 件） |
| 承認番号数 | 7 件（有効 5 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Lactulose の添付文書（Prescribing Information）の「Clinical Pharmacology」の項によると（非公式訳）、「ラクツロースは血中アンモニア濃度を低下させ、門脈大循環性脳症の程度を軽減する。これらの作用は以下によるものと考えられている：結腸内でのラクツロースの細菌による分解により結腸内容物が酸性化される。」英語原文："Lactulose causes a decrease in blood ammonia concentration and reduces the degree of portalsystemic encephalopathy. These actions are considered to be results of the following: Bacterial degradation of lactulose in the colon acidifies the colonic contents."（[DailyMed: Enulose (lactulose) prescribing information, Bryant Ranch Prepack](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=fa3aae7c-6f98-4fbb-85dc-32affe9874d5)、版 2024-12-18、参照日 2026-11-19）。一般に、ラクツロースは大腸で腸内細菌に分解されて浸透圧作用と腸内の酸性化をもたらし、アンモニアの吸収を抑えると考えられています。

急性尿酸性腎症は、尿酸が腎尿細管に沈着して起こる急性の腎障害です。この病態とラクツロースの作用（浸透圧性の腸管作用、腸内アンモニアの捕捉）の間に、直接的で妥当な機序的つながりは見当たりません。今回のスコアは、モデル上の関連性を示すだけで、機序や臨床データで裏付けられたものではありません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 622654601 | ラグノスＮＦ経口ゼリー分包１２ｇ ５４．１６７％ | 有効 |
| 622741500 | ラクツロース６５％シロップ | 有効 |
| 622498401 | ラクツロース・シロップ６０％分包１５ｍＬ「コーワ」 | 薬価削除（2026-03-31） |
| 620007126 | ラクツロース・シロップ６０％「コーワ」 | 有効 |
| 620881402 | ラクツロースシロップ６５％「タカタ」 | 有効 |

上表はデータ上の 7 件のうち 5 件です。

<!-- licenses:end -->

承認は単剤のものです。

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用データベースで 100 件の相互作用が検出されました。大半は「中等度 (Moderate)」で、例として次の薬剤が挙がっています。
  - アビラテロン
  - トラマドール
  - アセタゾラミド
  - ヒドロコルチゾン
  - サルブタモール
  - ヒドロクロロチアジド
  - アミロライド
  - アミオダロン
  - プロポフォール
  - アルセニック・トリオキシド

  「軽微 (Minor)」の例はクエン酸ナトリウムです。腎疾患を対象とする場合は、併用する利尿薬や電解質に影響する薬剤に特に注意が必要です。

その他の警告・禁忌については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 急性尿酸性腎症を直接検討した臨床試験・文献がなく、機序的なつながりも明確でないため、エビデンスレベルは L5（モデル予測のみ）です。この段階で開発や臨床応用に進める根拠はありません。

**進める場合に必要なもの：**
- 急性尿酸性腎症との機序的関連を示す前臨床データ（尿酸代謝・腎尿細管障害への影響など）
- 詳細な作用機序データ（MOA）の補充
- 添付文書の警告・禁忌の確認（安全性評価を進めるための必須情報）
- 上記で関連性が示された場合に限り、小規模な探索的研究の検討

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Enulose (lactulose) prescribing information, Bryant Ranch Prepack](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=fa3aae7c-6f98-4fbb-85dc-32affe9874d5) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：モニラック、ラグノスNF経口ゼリー分包

**販売名（規格別）**：ラクツロース65%シロップ、ラクツロースシロップ65%、ラクツロース・シロップ60%、ラクツロース・シロップ60%分包10mL、ラクツロース・シロップ60%分包15mL、ラグノスNF経口ゼリー分包12g 54.167%
<!-- brand-names:end -->

