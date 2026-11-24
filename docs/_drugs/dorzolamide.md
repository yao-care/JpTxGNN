---
layout: default
title: Dorzolamide
parent: モデル予測のみ
nav_order: 117
evidence_level: L5
indication_count: 7
monitor_inn: "dorzolamide"
predicted_indications: ["hypotrichosis simplex of the scalp", "congenital hypotrichosis milia", "alopecia", "diffuse alopecia areata", "congestive heart failure", "acute pulmonary heart disease", "respiratory failure"]
last_modified_at: 2026-11-24
description: "Dorzolamide：予測新適応症は頭皮の単純性乏毛症 (hypotrichosis simplex of the scalp)（エビデンスレベル L5）。薬価基準の品目：2 件（現在収載 2 件）"
---

# Dorzolamide
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

## ドルゾラミド：炭酸脱水酵素阻害薬 → 頭皮の単純性乏毛症 (hypotrichosis simplex of the scalp)
{: .text-alpha }

## 一言要約

ドルゾラミドは炭酸脱水酵素を阻害する点眼薬です。
TxGNN モデルは**頭皮の単純性乏毛症 (hypotrichosis simplex of the scalp)** に有効である可能性を予測していますが、この予測を支持する臨床試験や文献はなく、**エビデンスはモデル予測のみ**です。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 頭皮の単純性乏毛症 (hypotrichosis simplex of the scalp) |
| TxGNN 予測スコア | 0.9995 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 2 件／全 2 件） |
| 承認番号数 | 2 件（有効 2 件） |
| 推奨決定 | Hold |

---

## この予測が妥当かどうか

米国 FDA が承認した Dorzolamide の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「炭酸脱水酵素（CA）は、眼を含む体内の多くの組織に存在する酵素である。CAは二酸化炭素の水和及び炭酸の脱水を伴う可逆反応を触媒する。[…] ドルゾラミド塩酸塩点眼液は、ヒト炭酸脱水酵素IIの阻害薬であるドルゾラミド塩酸塩を含有する。」英語原文："Carbonic anhydrase (CA) is an enzyme found in many tissues of the body including the eye. It catalyzes the reversible reaction involving the hydration of carbon dioxide and the dehydration of carbonic acid. […] Dorzolamide hydrochloride ophthalmic solution contains dorzolamide hydrochloride, an inhibitor of human carbonic anhydrase II."（[DailyMed: Dorzolamide Hydrochloride Ophthalmic Solution (dorzolamide hydrochloride) prescribing information, Micro Labs Limited](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=4698e4e1-c5f6-4db1-9328-74464a85afea)、版 2026-11-14、参照日 2026-11-19）。ドルゾラミドは炭酸脱水酵素（CA1、CA7、CA12、CA14 など）を標的とする薬理作用が確認されています。点眼液として使用される薬剤で、全身への曝露は少ないと考えられます。

一方、頭皮の単純性乏毛症は毛包の遺伝性疾患です。炭酸脱水酵素の阻害と毛包生物学との間に、現時点で明確な機序的関連は見当たりません。この予測は TxGNN モデルの出力のみに基づいており、機序面の裏付けはありません。

そのため、本予測は仮説の段階にとどまります。評価を進めるには、機序の検証と前臨床データが必要です。

---

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

---

## 文献エビデンス

現在、関連する文献はありません。

---

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 660432003 | トルソプト点眼液１％ | 有効 |
| 660432002 | トルソプト点眼液０．５％ | 有効 |

<!-- licenses:end -->

---

## 安全性に関する考慮事項

- **薬物相互作用**：薬理学的な標的として炭酸脱水酵素 1、7、12、14 が確認されています。薬物間の相互作用として具体的に記載できる情報はありません。

その他の安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Hold**

**理由：**
- 予測を支持する臨床試験・文献がなく、炭酸脱水酵素阻害と毛包生物学との間にも機序的な関連が見当たらないため、現時点では TxGNN の予測のみが根拠です。

**進める場合に必要なもの：**
- 添付文書の警告・禁忌情報の取得と確認
- 詳細な作用機序データ（MOA）の整備
- 炭酸脱水酵素と毛包の関連を検討する前臨床研究
- 点眼薬から頭皮への適用に向けた投与経路・剤形の検討

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Dorzolamide Hydrochloride Ophthalmic Solution (dorzolamide hydrochloride) prescribing information, Micro Labs Limited](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=4698e4e1-c5f6-4db1-9328-74464a85afea) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：トルソプト

**販売名（規格別）**：トルソプト点眼液0.5%、トルソプト点眼液1%

**配合剤（この成分を含む）**：コソプト配合点眼液、ドルモロール配合点眼液
<!-- brand-names:end -->

