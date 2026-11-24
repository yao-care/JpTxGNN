---
layout: default
title: Metoclopramide
parent: モデル予測のみ
nav_order: 234
evidence_level: L5
indication_count: 2
monitor_inn: "Metoclopramide"
predicted_indications: ["gastroduodenitis", "peptic ulcer perforation"]
last_modified_at: 2026-11-24
description: "Metoclopramide：予測新適応症は胃十二指腸炎 (gastroduodenitis)（エビデンスレベル L5）。薬価基準の品目：13 件（現在収載 12 件）"
---

# Metoclopramide
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **2** 件
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

## メトクロプラミド：ドパミンD2受容体拮抗薬（制吐薬・消化管運動改善薬） → 胃十二指腸炎 (gastroduodenitis)
{: .text-alpha }

## 一言要約

メトクロプラミドは、制吐作用と消化管運動改善作用をもつドパミンD2受容体拮抗薬です。
TxGNN モデルは**胃十二指腸炎 (gastroduodenitis)** に有効である可能性を予測しています。
ただし、この疾患そのものを直接検討した臨床試験や文献は確認されておらず、エビデンスはモデル予測の段階にとどまります。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 胃十二指腸炎 (gastroduodenitis) |
| TxGNN 予測スコア | 0.9990 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 12 件／全 13 件） |
| 承認番号数 | 13 件（有効 12 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Metoclopramide の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「メトクロプラミドは、胃液、胆汁又は膵液の分泌を刺激することなく、上部消化管の運動を刺激する。胃食道逆流並びに急性及び再発性の糖尿病性胃不全麻痺の治療におけるメトクロプラミドの正確な作用機序は完全には確立されていない。」英語原文："Metoclopramide stimulates motility of the upper gastrointestinal tract without stimulating gastric, biliary, or pancreatic secretions. The exact mechanism of action of metoclopramide in the treatment of gastroesophageal reflux and acute and recurrent diabetic gastroparesis has not been fully established."（[DailyMed: Reglan (metoclopramide hydrochloride) prescribing information, ANI Pharmaceuticals, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=de55c133-eb08-4a35-91a2-5dc093027397)、版 2026-02-09、参照日 2026-11-19）。ただし、メトクロプラミドはドパミンD2受容体拮抗薬に分類される制吐薬・消化管運動改善薬として知られています。文献では、ドパミン拮抗薬が胃十二指腸の運動を促進し、胃幽門部と十二指腸の協調運動に影響することが動物実験や生理学的研究で示されています。

こうした作用は、胃十二指腸の炎症に伴う消化不良症状（吐き気、胃排出の遅れなど）を和らげる可能性があります。ただし、これは症状緩和という機序上の推測です。胃十二指腸炎そのものの治療効果を直接示した研究は、今回の収集データにはありません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

胃十二指腸炎を直接対象とした研究はありません。以下は、胃十二指腸の運動や関連する場面でメトクロプラミドを検討した文献です。

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [42259699](https://pubmed.ncbi.nlm.nih.gov/42259699/) | 2026 | RCT | Revista de gastroenterologia de Mexico | 急性上部消化管出血での内視鏡観察に対する高用量メトクロプラミドとプラセボの比較（三重盲検） |
| [38059896](https://pubmed.ncbi.nlm.nih.gov/38059896/) | 2024 | Meta-analysis | Am J Gastroenterol | 活動性上部消化管出血での胃内観察に対するメトクロプラミドの有効性（二重盲検RCT） |
| [7886398](https://pubmed.ncbi.nlm.nih.gov/7886398/) | 1994 | Cohort | Scand J Gastroenterol | シサプリドとメトクロプラミドがヒトの食後・空腹期の胃十二指腸運動に与える影響 |
| [8179003](https://pubmed.ncbi.nlm.nih.gov/8179003/) | 1994 | In vitro | Am J Physiol | イヌで、シサプリド・メトクロプラミド・ドンペリドンが胃十二指腸の収縮と排出に働く機序を比較 |
| [6382574](https://pubmed.ncbi.nlm.nih.gov/6382574/) | 1984 | 不明 | Scand J Gastroenterol Suppl | ドパミン拮抗薬が上部消化管の運動を促進する作用の概説 |
| [7072665](https://pubmed.ncbi.nlm.nih.gov/7072665/) | 1982 | 不明 | Am J Dis Child | 小児9例で、メトクロプラミドが胃・十二指腸の運動を高め、症状が改善した報告 |
| [3776267](https://pubmed.ncbi.nlm.nih.gov/3776267/) | 1986 | Review | Z Gastroenterol | 胃幽門部と十二指腸の協調運動の概説 |
| [18321441](https://pubmed.ncbi.nlm.nih.gov/18321441/) | 2008 | Review | Curr Treat Options Gastroenterol | 悪心・嘔吐の原因と管理 |

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 620006100 | プリンペラン錠５ ５ｍｇ | 有効 |
| 620006099 | プリンペラン細粒２％ | 有効 |
| 620003796 | プリンペラン注射液１０ｍｇ ０．５％２ｍＬ | 有効 |
| 620006101 | プリンペランシロップ０．１％ | 有効 |
| 621279401 | メトクロプラミド錠５ｍｇ「トーワ」 | 有効 |

上表はデータ上の 13 件のうち 5 件です。

<!-- licenses:end -->

承認は全13件です（上記は主要な5件）。

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用データベースで100件が確認されています。主なものは次のとおりです。
  - 重大（Major）：トラマドール、アミスルプリド
  - 中等度（Moderate）：フェンタニル、コデイン、アルプラゾラム、アミトリプチリン、アマンタジン、エタノールなど

安全性情報の詳細（警告・禁忌）については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
胃十二指腸炎を直接検討した臨床試験や文献がなく、エビデンスはモデル予測のみ（L5）です。得られている RCT は上部消化管出血時の内視鏡観察に関するもので、胃十二指腸炎の治療効果を支持するものではありません。

**進める場合に必要なもの：**
- 胃十二指腸炎を直接対象とした臨床研究または観察研究
- 詳細な薬物作用機序データ（MOA）
- 添付文書（PMDA）に基づく警告・禁忌の確認
- 併用薬（特にトラマドール、アミスルプリドなど重大な相互作用薬）に関する安全性評価

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Reglan (metoclopramide hydrochloride) prescribing information, ANI Pharmaceuticals, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=de55c133-eb08-4a35-91a2-5dc093027397) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：プリンペラン

**販売名（規格別）**：プリンペランシロップ0.1%、プリンペラン注射液10mg 0.5%2mL、プリンペラン細粒2%、プリンペラン錠5 5mg、メトクロプラミド5mg錠、メトクロプラミド注10mg 0.5%2mL、メトクロプラミド細粒2%、メトクロプラミド錠5mg
<!-- brand-names:end -->

