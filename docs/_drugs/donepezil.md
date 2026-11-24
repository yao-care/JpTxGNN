---
layout: default
title: Donepezil
parent: モデル予測のみ
nav_order: 116
evidence_level: L5
indication_count: 8
monitor_inn: "Donepezil"
predicted_indications: ["psychogenic movement disorders", "chronic tic disorder", "primary orthostatic tremor", "benign shuddering attacks", "extrapyramidal and movement disease", "tremor-nystagmus-duodenal ulcer syndrome", "benign paroxysmal tonic upgaze of childhood with ataxia", "lingual-facial-buccal dyskinesia"]
last_modified_at: 2026-11-24
description: "Donepezil：予測新適応症は心因性運動障害 (psychogenic movement disorders)（エビデンスレベル L5）。薬価基準の品目：20 件以上"
---

# Donepezil
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

## ドネペジル：アセチルコリンエステラーゼ阻害薬 → 心因性運動障害 (psychogenic movement disorders)
{: .text-alpha }

## 一言要約

ドネペジルはアセチルコリンエステラーゼ阻害薬に分類される薬剤です。
TxGNN モデルは**心因性運動障害 (psychogenic movement disorders)** に有効である可能性を予測していますが、この疾患を直接検討した臨床試験・文献は **0 件**です。
現時点の根拠はモデル予測のみです。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 心因性運動障害 (psychogenic movement disorders) |
| TxGNN 予測スコア | 0.9923 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 17 件以上） |
| 承認番号数 | 20 件以上 |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Donepezil の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「アルツハイマー病の認知に関する徴候及び症状の病因についての現在の理論では、その一部はコリン作動性神経伝達の欠乏に起因するとされている。ドネペジル塩酸塩は、コリン作動性機能を増強することにより治療効果を発揮すると推測されている。」英語原文："Current theories on the pathogenesis of the cognitive signs and symptoms of Alzheimer’s disease attribute some of them to a deficiency of cholinergic neurotransmission. Donepezil hydrochloride is postulated to exert its therapeutic effect by enhancing cholinergic function."（[DailyMed: Aricept (donepezil hydrochloride) prescribing information, Eisai Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=98e451e1-e4d7-4439-a675-c5457ba20975)、版 2021-12-30、参照日 2026-11-19）。ドネペジルはアセチルコリンエステラーゼを阻害してシナプスのアセチルコリン濃度を高める薬剤であり、大脳基底核のコリン作動性とドパミン作動性のバランスに影響し得ると考えられます。

ただし、心因性運動障害は機能性の疾患です。機序面でも臨床面でも、この予測を裏づける根拠は今回の収集データにはありません。したがって、この予測はモデル出力の段階にとどまり、機序的な妥当性は確認できていません。

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 621957801 | アリセプト内服ゼリー３ｍｇ | 有効 |
| 622095102 | ドネペジル塩酸塩ＯＤ錠５ｍｇ「ニプロ」 | 有効 |
| 622105601 | ドネペジル塩酸塩ＯＤ錠５ｍｇ「ＴＣＫ」 | 有効 |
| 622107501 | ドネペジル塩酸塩ＯＤ錠５ｍｇ「日新」 | 有効 |
| 622112601 | ドネペジル塩酸塩錠５ｍｇ「明治」 | 有効 |

データには承認の一部のみが含まれています。上表はそのうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **薬物相互作用**（DDInter 収載、総数 100 件のうち一部）：
  - 重大（Major）：ブプロピオン
  - 中等度（Moderate）：ファモチジン、ラニチジン、シメチジン、ヒヨスチアミン、アトロピン、グリコピロニウム、ジシクロミン、ロペラミド、デキサメタゾン、メトロニダゾール、ドラセトロン など
  - 軽微（Minor）：アプレピタント、アセチルサリチル酸、クラリスロマイシン など
  - 抗コリン薬とは作用が拮抗し得る点に注意が必要です。
- 添付文書上の警告・禁忌は今回のデータでは確認できていません。詳細は添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
心因性運動障害を直接検討した臨床試験・文献がなく、根拠は TxGNN の予測のみ（L5）です。機序面の裏づけもないため、現段階では開発を進めるべきではありません。

**進める場合に必要なもの：**
- 作用機序（MOA）データの補完
- 添付文書の警告・禁忌の取得と確認
- 心因性運動障害に対する前臨床または探索的臨床研究の有無の調査
- 心因性運動障害の病態に即した機序的仮説の整理

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Aricept (donepezil hydrochloride) prescribing information, Eisai Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=98e451e1-e4d7-4439-a675-c5457ba20975) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：アリセプト、アリセプトD、アリセプト内服ゼリー

**販売名（規格別）**：アリセプトD錠10mg、アリセプトD錠3mg、アリセプトD錠5mg、アリセプトドライシロップ1%、アリセプト内服ゼリー10mg、アリセプト内服ゼリー3mg、アリセプト内服ゼリー5mg、アリセプト細粒0.5%、アリセプト錠10mg、アリセプト錠3mg、アリセプト錠5mg、ドネペジル塩酸塩0.5%細粒、ドネペジル塩酸塩10mg5mL液、ドネペジル塩酸塩10mg口腔内崩壊錠、ドネペジル塩酸塩10mg錠、ドネペジル塩酸塩3mg1.5mL液、ドネペジル塩酸塩3mg口腔内崩壊錠、ドネペジル塩酸塩3mg錠、ドネペジル塩酸塩5mg2.5mL液、ドネペジル塩酸塩5mg口腔内崩壊錠、ドネペジル塩酸塩5mg錠、ドネペジル塩酸塩OD錠10mg、ドネペジル塩酸塩OD錠3mg、ドネペジル塩酸塩OD錠5mg、ドネペジル塩酸塩内服ゼリー10mg、ドネペジル塩酸塩内服ゼリー3mg、ドネペジル塩酸塩内服ゼリー5mg、ドネペジル塩酸塩内用液10mg 5mL、ドネペジル塩酸塩内用液3mg 1.5mL、ドネペジル塩酸塩内用液5mg 2.5mL、ドネペジル塩酸塩細粒0.5%、ドネペジル塩酸塩錠10mg、ドネペジル塩酸塩錠3mg、ドネペジル塩酸塩錠5mg
<!-- brand-names:end -->

