---
layout: default
title: Benzoyl Peroxide
parent: モデル予測のみ
nav_order: 52
evidence_level: L5
indication_count: 4
monitor_inn: "Benzoyl peroxide"
predicted_indications: ["vulvar inverted follicular keratosis", "2-hydroxyethyl methacrylate sensitization", "acrodermatitis chronica atrophicans", "acne keloid"]
last_modified_at: 2026-11-24
description: "Benzoyl Peroxide：予測新適応症は外陰逆性毛包性角化症 (vulvar inverted follicular keratosis)（エビデンスレベル L5）。薬価基準の品目：3 件（現在収載 3 件）"
---

# Benzoyl Peroxide
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **4** 件
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

## ベンゾイルパーオキサイド：外用の角質溶解・抗菌・面皰溶解薬 → 外陰逆性毛包性角化症 (vulvar inverted follicular keratosis)
{: .text-alpha }

## 一言要約

ベンゾイルパーオキサイドは、角質溶解作用・抗菌作用・面皰溶解作用をもつ外用薬で、日本ではゲルやローションとして流通しています。
TxGNN モデルは**外陰逆性毛包性角化症 (vulvar inverted follicular keratosis)** に有効である可能性を予測していますが、この疾患を直接検討した臨床試験や文献は、現時点ではありません。
エビデンスはモデル予測のみ（L5）です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 外陰逆性毛包性角化症 (vulvar inverted follicular keratosis) |
| TxGNN 予測スコア | 0.9992 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 3 件／全 3 件） |
| 承認番号数 | 3 件（有効 3 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Benzoyl Peroxide の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「過酸化ベンゾイルは殺菌作用及び角質溶解作用を有する酸化剤であるが、酒さの治療における正確な作用機序は不明である。」英語原文："Benzoyl peroxide is an oxidizing agent with bactericidal and keratolytic effects but the precise mechanism of action in the treatment of rosacea is unknown."（[DailyMed: Epsolay (benzoyl peroxide) prescribing information, Mayne Pharma Commercial LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=641981e6-460b-44dd-8146-306c47e5367c)、版 2025-08-11、参照日 2026-11-19）。ベンゾイルパーオキサイドは角質溶解作用、抗菌作用、面皰溶解作用を併せもつことが知られており、毛包の角化に影響しうると考えられます。

逆性毛包性角化症は毛包に関連した角化性病変であるため、毛包角化への作用という点で機序的な接点が想定されます。ただし、この関連は推測の域を出ず、TxGNN の予測のみに基づいています。臨床的・文献的な裏付けはありません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 622403601 | ベピオゲル２．５％ | 有効 |
| 622987801 | ベピオウォッシュゲル５％ | 有効 |
| 622940901 | ベピオローション２．５％ | 有効 |

<!-- licenses:end -->

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。薬物相互作用の登録情報も確認できませんでした。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測スコアは高いものの、外陰逆性毛包性角化症を直接検討した臨床試験・文献がなく、エビデンスはモデル予測のみ（L5）です。添付文書の安全性情報も未確認のため、現段階では保留が妥当です。

**進める場合に必要なもの：**
- 外陰逆性毛包性角化症に対する症例報告・観察研究などの文献調査
- 添付文書（PMDA）の警告・禁忌・相互作用情報の取得と確認
- 作用機序データの補充と、本疾患の病態との機序的関連の検討
- 外陰部など粘膜に近い部位への外用の安全性（刺激性・感作性）評価

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Epsolay (benzoyl peroxide) prescribing information, Mayne Pharma Commercial LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=641981e6-460b-44dd-8146-306c47e5367c) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：ベピオ、ベピオウォッシュ、ベピオローション

**販売名（規格別）**：ベピオウォッシュゲル5%、ベピオゲル2.5%、ベピオローション2.5%

**配合剤（この成分を含む）**：エピデュオゲル
<!-- brand-names:end -->

