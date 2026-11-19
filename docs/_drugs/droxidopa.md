---
layout: default
title: Droxidopa
parent: モデル予測のみ
nav_order: 103
evidence_level: L5
indication_count: 1
monitor_inn: "Droxidopa"
predicted_indications: ["variably protease-sensitive prionopathy"]
last_modified_at: 2026-11-20
description: "Droxidopa：予測新適応症は変異プロテアーゼ感受性プリオノパチー (Variably protease-sensitive prionopathy)（エビデンスレベル L5）。既存適応症：パーキンソン病治療薬、ノルアドレナリン補充薬（パーキンソン病、シャイ・ドレーガー症候群、家族性アミロイドポリニューロパチー）"
---

# Droxidopa
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **1** 件
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

## ドロキシドパ：パーキンソン病から変異プロテアーゼ感受性プリオノパチーへ
{: .text-alpha }

## 一言要約

ドロキシドパは体内でノルアドレナリンに変換される補充薬で、元々パーキンソン病、シャイ・ドレーガー症候群、家族性アミロイドポリニューロパチーの治療に使用されていました。
TxGNN モデルは**変異プロテアーゼ感受性プリオノパチー (Variably protease-sensitive prionopathy)** に有効である可能性を予測しています。
ただし、裏付けとなる臨床試験や文献は **0 件**で、モデル予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | パーキンソン病治療薬、ノルアドレナリン補充薬（パーキンソン病、シャイ・ドレーガー症候群、家族性アミロイドポリニューロパチー） |
| 予測新規適応症 | 変異プロテアーゼ感受性プリオノパチー (Variably protease-sensitive prionopathy) |
| TxGNN 予測スコア | 0.9933 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 4 件／全 7 件） |
| 承認番号数 | 7 件（有効 4 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Droxidopa の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「神経原性起立性低血圧の治療におけるNORTHERAの正確な作用機序は不明である。NORTHERAは合成アミノ酸類似体であり、全身に広く分布するドパ脱炭酸酵素によって直接ノルエピネフリンに代謝される。」英語原文："The exact mechanism of action of NORTHERA in the treatment of neurogenic orthostatic hypotension is unknown. NORTHERA is a synthetic amino acid analog that is directly metabolized to norepinephrine by dopa­-decarboxylase, which is extensively distributed throughout the body."（[DailyMed: Northera (droxidopa) prescribing information, Lundbeck Pharmaceuticals LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=2179f02c-48d7-48eb-8007-5ae43d8d16bc)、版 2019-07-01、参照日 2026-11-19）。既知の情報によると、ドロキシドパは芳香族 L-アミノ酸脱炭酸酵素によってノルアドレナリンに変換されるプロドラッグで、神経原性起立性低血圧や自律神経障害の治療に用いられてきました。

変異プロテアーゼ感受性プリオノパチーは、稀で致死的な神経変性プリオン病です。ノルアドレナリン補充という機序と、この疾患の病態との間に、確立した機序的なつながりはありません。関連があるとしても、自律神経症状に対する対症的な支持にとどまります。

TxGNN のスコアは高いものの、この予測を支持する臨床試験も文献も確認されていません。妥当性は現時点で検証されておらず、慎重な解釈が必要です。

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 620004009 | ドロキシドパカプセル200mg「アメル」 | カプセル | パーキンソン病治療薬、ノルアドレナリン補充薬（パーキンソン病、シャイ・ドレーガー症候群、家族性アミロイドポリニューロパチー） |
| 620004007 | ドロキシドパカプセル100mg「アメル」 | カプセル | パーキンソン病治療薬、ノルアドレナリン補充薬（パーキンソン病、シャイ・ドレーガー症候群、家族性アミロイドポリニューロパチー） |
| 622061101 | ドプスOD錠100mg | 錠 | （記載なし） |
| 622061201 | ドプスOD錠200mg | 錠 | （記載なし） |
| 620005046 | ドプス細粒20% | 細粒 | （記載なし） |

7 件の承認のうち 4 件が有効な状態です（販売中。3 件は薬価基準から削除済み）。

<!-- review:begin jp-lic-20261117-droxidopa-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「7 件の承認はすべて有効な状態です（販売中）。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、データ上の 7 件のうち有効（収載中）は 4 件で、3 件は経過措置期間満了などにより薬価基準から削除されています（622711000（廃止年月日 2026-03-31）、620005046（廃止年月日 2026-03-31）、622710900（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-droxidopa-1 -->

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用データは 32 件です。うち重要度が高い（Major）ものは、コカイン（外用・経鼻）との併用です。
  - 中等度（Moderate）では、交感神経刺激薬や昇圧薬との併用が目立ちます。エピネフリン、エフェドリン、フェニレフリン、プソイドエフェドリン、イソプレナリンなどが該当し、昇圧作用の増強に注意が必要です。
  - そのほか、β2 刺激薬（サルブタモール、ホルモテロール、インダカテロール）、食欲抑制薬（フェンテルミン、フェンフルラミン、マジンドール、ジエチルプロピオン）、イソメテプテン、メチレンブルーも中等度の相互作用として挙げられています。

警告・禁忌については、添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測スコアは高い一方、臨床試験・文献が一件もなく、機序的な関連も不明確です（エビデンスレベル L5）。

<!-- review:begin jp-lic-20261106-droxidopa-1 -->

> **確認による訂正（2026-11-06）**：元の記載は「予測スコアは高い一方、臨床試験・文献が一件もなく、機序的な関連も不明確です（エビデンスレベル L5）。現在は国内で市販されておらず、警告・禁忌の情報も不足しているため、現時点で進めるのは適切ではありません。」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。データ上の収載は 7 件、うち有効 7 件です。最新の件数はクイック概要と日本市販情報にあります。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-droxidopa-1 -->

**進める場合に必要なもの：**
- 添付文書（PMDA）の警告・禁忌情報の取得と確認
- 詳細な作用機序データ（MOA）の取得（DrugBank など）
- ノルアドレナリン補充とプリオン病の病態を結ぶ機序仮説の検討
- 前臨床研究（細胞・動物モデル）または症例報告による裏付けの探索

<!-- review:begin jp-lic-20261112-droxidopa-1 -->

> **確認による訂正（2026-11-12）**：元の記載は「前臨床研究（細胞・動物モデル）または症例報告による裏付けの探索／市販が整理済みである点を踏まえた、供給・剤形面の実現可能性の確認」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-05 のデータ）。データ上の収載は 7 件、うち有効 7 件です。最新の件数はクイック概要と日本市販情報にあります。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261112-droxidopa-1 -->

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-06 | 削除：「現在は国内で市販されておらず、警告・禁忌の情報も不足しているため、現時点で進めるのは適切ではありません」 | 訂正 | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-12 | 削除：「市販が整理済みである点を踏まえた、供給・剤形面の実現可能性の確認」 | 訂正 | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正 | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Northera (droxidopa) prescribing information, Lundbeck Pharmaceuticals LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=2179f02c-48d7-48eb-8007-5ae43d8d16bc) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：ドプス

**販売名（規格別）**：ドプスOD錠100mg、ドプスOD錠200mg、ドプス細粒20%、ドロキシドパ100mgカプセル、ドロキシドパ200mgカプセル、ドロキシドパカプセル100mg、ドロキシドパカプセル200mg
<!-- brand-names:end -->

