---
layout: default
title: Clobazam
parent: モデル予測のみ
nav_order: 90
evidence_level: L5
indication_count: 10
monitor_inn: "Clobazam"
predicted_indications: ["febrile infection-related epilepsy syndrome", "perioral myoclonia with absences", "atypical childhood epilepsy with centrotemporal spikes", "photosensitive occipital lobe epilepsy", "cryptogenic late-onset epileptic spasms", "childhood onset epileptic encephalopathy", "benign occipital epilepsy", "early-onset epileptic encephalopathy and intellectual disability due to GRIN2A mutation", "restless legs syndrome", "polymicrogyria with optic nerve hypoplasia"]
last_modified_at: 2026-11-24
description: "Clobazam：予測新適応症は熱性感染症関連てんかん症候群 (febrile infection-related epilepsy syndrome)（エビデンスレベル L5）。薬価基準の品目：3 件（現在収載 3 件）"
---

# Clobazam
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **10** 件
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

## クロバザム：ベンゾジアゼピン系抗てんかん薬（GABA-A 受容体調節）→ 熱性感染症関連てんかん症候群 (febrile infection-related epilepsy syndrome)
{: .text-alpha }

## 一言要約

クロバザムは 1,5-ベンゾジアゼピン系の薬で、日本ではマイスタンの商品名で流通した記録があります。
TxGNN モデルは**熱性感染症関連てんかん症候群 (febrile infection-related epilepsy syndrome)** に有効である可能性を予測しています。
ただし、臨床試験の登録はなく、文献は他の薬剤（ロラゼパム、ミダゾラム、ペランパネル）を扱った症例報告 2 編のみで、クロバザム自体を検討した研究はありません。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 熱性感染症関連てんかん症候群 (febrile infection-related epilepsy syndrome) |
| TxGNN 予測スコア | 0.9982 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 3 件／全 3 件） |
| 承認番号数 | 3 件（有効 3 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Clobazam の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「1,5-ベンゾジアゼピン系薬剤であるクロバザムの正確な作用機序は完全には解明されていないが、GABA A 受容体のベンゾジアゼピン結合部位への結合によりGABA作動性神経伝達が増強されることが関与していると考えられている。」英語原文："The exact mechanism of action for clobazam, a 1,5-benzodiazepine, is not fully understood but is thought to involve potentiation of GABAergic neurotransmission resulting from binding at the benzodiazepine site of the GABA A receptor."（[DailyMed: Onfi (clobazam) prescribing information, Lundbeck Pharmaceuticals LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=de03bd69-2dca-459c-93b4-541fd3e9571c)、版 2026-10-16、参照日 2026-11-19）。既知の情報では、クロバザムは 1,5-ベンゾジアゼピン系で、GABA-A 受容体を正に調節して神経の抑制を強めます。このため、難治性のけいれんを抑える可能性があります。

熱性感染症関連てんかん症候群 (FIRES) は、従来の抗てんかん薬が効きにくく、麻酔薬の大量投与が必要になることの多い重症のてんかんです。GABA 系を介した発作抑制は理屈の上では適用可能です。

ただし、収集された FIRES の文献が扱っているのはロラゼパム、ミダゾラム、ペランパネルです。クロバザム自体の有効性を示す直接的な研究は確認できていません。そのため、エビデンスレベルは L5 と判定しました。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [35770765](https://pubmed.ncbi.nlm.nih.gov/35770765/) | 2022 | 症例集積 | Epileptic Disord | ミダゾラム反応性の FIRES で、経腸ロラゼパムが減量時の代替薬として有望（クロバザムは対象外） |
| [39958143](https://pubmed.ncbi.nlm.nih.gov/39958143/) | 2025 | 症例報告 | Cureus | 13 歳男児の FIRES で、ペランパネルがバルビツール酸依存の低減に寄与する可能性（クロバザムは対象外） |

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 620000139 | マイスタン細粒１％ | 有効 |
| 610443012 | マイスタン錠１０ｍｇ | 有効 |
| 610443011 | マイスタン錠５ｍｇ | 有効 |

<!-- licenses:end -->

## 安全性に関する考慮事項

- **薬物相互作用**：100 件の相互作用が登録されています。重大（Major）なものには、モルヒネ（リポソーム製剤を含む）とエリグルスタットがあります。中等度のものには、ブプロピオン、アプレピタント、オメプラゾール、シメチジン、クラリスロマイシンなどがあります。
- 警告および禁忌の詳細については、添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測スコアは高いものの、クロバザムを FIRES で検討した臨床試験も文献もなく、根拠はモデル予測と一般的な GABA-A 調節の機序に限られます。

**進める場合に必要なもの：**
- FIRES におけるクロバザムの使用経験を調べる文献検索、または症例集積
- 作用機序データ（MOA）の補充
- 添付文書の警告・禁忌の取得と、安全性評価
- 併用薬の多い小児での相互作用管理計画

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Onfi (clobazam) prescribing information, Lundbeck Pharmaceuticals LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=de03bd69-2dca-459c-93b4-541fd3e9571c) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：マイスタン

**販売名（規格別）**：マイスタン細粒1%、マイスタン錠10mg、マイスタン錠5mg
<!-- brand-names:end -->

