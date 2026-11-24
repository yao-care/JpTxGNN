---
layout: default
title: Desloratadine
parent: モデル予測のみ
nav_order: 106
evidence_level: L5
indication_count: 4
monitor_inn: "Desloratadine"
predicted_indications: ["nasal cavity disease", "recalcitrant atopic dermatitis", "IgE responsiveness, atopic", "rosacea conjunctivitis"]
last_modified_at: 2026-11-24
description: "Desloratadine：予測新適応症は鼻腔疾患 (nasal cavity disease)（エビデンスレベル L5）。薬価基準の品目：1 件（現在収載 1 件）"
---

# Desloratadine
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

## デスロラタジン：ヒスタミンH1受容体拮抗薬 → 鼻腔疾患 (nasal cavity disease)
{: .text-alpha }

## 一言要約

デスロラタジンは抗ヒスタミン薬（H1受容体拮抗薬）で、日本ではデザレックス錠として承認されています。
TxGNN モデルは**鼻腔疾患 (nasal cavity disease)** に有効である可能性を予測しています（予測スコア 0.9987）。
ただし、この疾患を直接検討した臨床試験は 0 件で、関連文献は動物実験の **2 編**にとどまります。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 鼻腔疾患 (nasal cavity disease) |
| TxGNN 予測スコア | 0.9987 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 1 件／全 1 件） |
| 承認番号数 | 1 件（有効 1 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Desloratadine の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「デスロラタジンは、選択的なヒスタミンH1受容体拮抗作用を有する長時間作用型の三環系ヒスタミン拮抗薬である。受容体結合データから、2-3 ng/mL（7ナノモーラー）の濃度において、デスロラタジンはヒトヒスタミンH1受容体と顕著な相互作用を示すことが示されている。」英語原文："Desloratadine is a long-acting tricyclic histamine antagonist with selective H1-receptor histamine antagonist activity. Receptor binding data indicates that at a concentration of 2-3 ng/mL (7 nanomolar), desloratadine shows significant interaction with the human histamine H1-receptor."（[DailyMed: Desloratadine Oral Solution (desloratadine) prescribing information, INA Pharmaceutics, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=41d5e0d4-6188-847b-e063-6294a90a2e2f)、版 2025-10-23、参照日 2026-11-19）。ただし、デスロラタジンは H1 受容体を遮断する抗ヒスタミン薬です。ヒスタミンによる鼻閉、鼻汁、粘膜の炎症を抑える作用が機序的に想定されます。

鼻腔疾患は非常に広い概念で、ヒスタミンが関与する病態もあれば、関与しない病態もあります。そのため、機序面の裏付けは間接的で、どの病態に効くかは特定できません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [30488351](https://pubmed.ncbi.nlm.nih.gov/30488351/) | 2019 | 動物実験 | Eur Arch Otorhinolaryngol | ラットのオボアルブミン誘発アレルギー性鼻炎モデルで、ヘスペリジンとチモールの効果を検討（デスロラタジンの試験ではない） |
| [19769798](https://pubmed.ncbi.nlm.nih.gov/19769798/) | 2009 | 動物実験 | Am J Rhinol Allergy | ネコの鼻閉モデルで、ロラタジンとモンテルカストの併用による鼻閉改善を検討。デスロラタジンは偽エフェドリンとの併用でも評価された |

いずれも関連病態を対象とした動物実験で、鼻腔疾患そのものを直接検討したヒト試験ではありません。

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 622514901 | デザレックス錠５ｍｇ | 有効 |

<!-- licenses:end -->

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用の候補が 100 件確認されました。例はカルシトリオール、フェンテルミン、パントプラゾール、ドキシサイクリン、モルヒネ、メトホルミン、オメプラゾール、シメチジン、エピネフリンなどです。重要度の分類はすべて未確定のため、臨床的な重みづけはできません。

警告・禁忌については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 鼻腔疾患を直接検討した臨床試験や文献がなく、動物実験が 2 編あるだけです。そのため、エビデンスレベルは L5（モデル予測が中心）と判断しました。
- 「鼻腔疾患」は範囲が広く、対象とする病態を絞り込めていません。

**進める場合に必要なもの：**
- 対象とする具体的な鼻腔疾患の絞り込み
- その疾患でのヒト臨床試験または観察研究の文献調査
- 詳細な作用機序データ（MOA）の補充
- 添付文書（PMDA）の警告・禁忌の確認と、安全性評価の実施
- 相互作用の重要度分類の確認

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Desloratadine Oral Solution (desloratadine) prescribing information, INA Pharmaceutics, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=41d5e0d4-6188-847b-e063-6294a90a2e2f) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：デザレックス

**販売名（規格別）**：デザレックス錠5mg
<!-- brand-names:end -->

