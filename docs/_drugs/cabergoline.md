---
layout: default
title: Cabergoline
parent: モデル予測のみ
nav_order: 70
evidence_level: L5
indication_count: 4
monitor_inn: "Cabergoline"
predicted_indications: ["progeria-short stature-pigmented nevi syndrome", "pituitary cancer", "cerebral palsy, spastic quadriplegic", "glaucoma"]
last_modified_at: 2026-11-24
description: "Cabergoline：予測新適応症は早老症・低身長・色素性母斑症候群 (progeria-short stature-pigmented nevi syndrome)（エビデンスレベル L5）。薬価基準の品目：2 件（現在収載 2 件）"
---

# Cabergoline
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

## カベルゴリン：ドパミンD2受容体作動薬 → 早老症・低身長・色素性母斑症候群 (progeria-short stature-pigmented nevi syndrome)
{: .text-alpha }

## 一言要約

カベルゴリンは、ドパミンD2受容体に作用する麦角系の作動薬で、日本ではカバサール錠として販売されています。
TxGNN モデルは **早老症・低身長・色素性母斑症候群 (progeria-short stature-pigmented nevi syndrome)** に有効である可能性を予測しています。
ただし、この疾患を直接調べた臨床試験と文献は **0 件**で、エビデンスはモデル予測のみです。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 早老症・低身長・色素性母斑症候群 (progeria-short stature-pigmented nevi syndrome) |
| TxGNN 予測スコア | 0.9906 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 2 件／全 2 件） |
| 承認番号数 | 2 件（有効 2 件） |
| 推奨決定 | Hold |

## この予測が妥当かどうか

米国 FDA が承認した Cabergoline の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「カベルゴリンは麦角誘導体であり、D2受容体に高い親和性を有するドパミン受容体作動薬である。in vitro試験の結果から、カベルゴリンはラット下垂体プロラクチン産生細胞によるプロラクチン分泌に対して直接的な抑制作用を示すことが示されている。」英語原文："Cabergoline is an ergot derivative and dopamine receptor agonist with a high affinity for D2 receptors. Results of in vitro studies demonstrate that cabergoline exerts a direct inhibitory effect on the secretion of prolactin by rat pituitary lactotrophs."（[DailyMed: cabergoline prescribing information, Mylan Pharmaceuticals Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=e497366b-a124-4d7f-bd45-a883c392d4bb)、版 2026-06-30、参照日 2026-11-19）。カベルゴリンはドパミンD2受容体作動薬に分類され、D2受容体を介してホルモン分泌を抑える薬です。

今回の予測疾患とD2受容体作動作用を結びつける機序は、現時点で見いだせていません。この疾患に対する臨床試験や文献による裏付けもないため、予測の妥当性は確認できていません。スコアは高い値ですが、実際の研究で支持されたものではありません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 610432023 | カバサール錠０．２５ｍｇ | 有効 |
| 610432024 | カバサール錠１．０ｍｇ １ｍｇ | 有効 |

<!-- licenses:end -->

日本では「カバサール錠」(0.25 mg、1.0 mg の経口錠) として販売されています。承認番号と承認の詳細は、別途提示される許諾情報を参照してください。

## 安全性に関する考慮事項

- **薬物相互作用**：データ上は計 60 件の相互作用が登録されています。重要度の高いものは次のとおりです。
  - 重大 (Major)：ロルカセリン、クラリスロマイシン
  - 中等度 (Moderate)：メトクロプラミド
- 上記以外の相互作用は、重要度が不明の薬剤が大半です。

その他の安全性情報については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- この疾患を直接調べた試験や文献がなく、機序的な根拠も見いだせないため、エビデンスはモデル予測のみ (L5) です。現時点では開発や適応拡大の検討に進める根拠がありません。

**進める場合に必要なもの：**
- 予測疾患とD2受容体作動作用の関連を示す機序研究や前臨床データ
- 詳細な作用機序データ (MOA) の補充
- 添付文書の警告と禁忌の確認 (現時点では未取得)
- 当該疾患の患者を対象とした症例報告や小規模な探索的研究の有無の調査

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: cabergoline prescribing information, Mylan Pharmaceuticals Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=e497366b-a124-4d7f-bd45-a883c392d4bb) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：カバサール

**販売名（規格別）**：カバサール錠0.25mg、カバサール錠1.0mg 1mg
<!-- brand-names:end -->

