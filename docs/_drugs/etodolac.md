---
layout: default
title: Etodolac
parent: モデル予測のみ
nav_order: 125
evidence_level: L5
indication_count: 6
last_modified_at: 2026-11-24
description: "Etodolac：予測新適応症は肢端中間部異形成症 Hunter-Thompson 型 (acromesomelic dysplasia…（エビデンスレベル L5）。既存適応症：鎮痛薬、抗炎症薬、シクロオキシゲナーゼ2阻害薬（関節リウマチ）"
monitor_inn: "Etodolac"
predicted_indications: ["acromesomelic dysplasia, Hunter-Thompson type", "brachyolmia-amelogenesis imperfecta syndrome", "myosclerosis", "brachyolmia", "pseudoachondroplasia", "hypermobility of coccyx"]
---

# Etodolac
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **6** 件
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

## エトドラク：関節リウマチから先端中間異形成 Hunter-Thompson 型へ
{: .text-alpha }

## 一言要約

エトドラクは COX-2 を選択的に阻害する鎮痛・抗炎症薬で、元々関節リウマチの治療に使用されていました。
TxGNN モデルは **肢端中間部異形成症 Hunter-Thompson 型 (acromesomelic dysplasia, Hunter-Thompson type)** に有効である可能性を予測していますが、この疾患に関する臨床試験・文献は **0 件** で、モデル予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 鎮痛薬、抗炎症薬、シクロオキシゲナーゼ2阻害薬（関節リウマチ） |
| 予測新規適応症 | 肢端中間部異形成症 Hunter-Thompson 型 (acromesomelic dysplasia, Hunter-Thompson type) |
| TxGNN 予測スコア | 0.9997 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 5 件／全 12 件） |
| 承認番号数 | 12 件（有効 5 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Etodolac の添付文書（Prescribing Information）の「Clinical Pharmacology」の項によると（非公式訳）、「エトドラク徐放錠の作用機序は、他のNSAIDsと同様に完全には解明されていないが、プロスタグランジン合成酵素阻害に関連している可能性がある。」英語原文："The mechanism of action of etodolac extended-release tablets, like that of other NSAIDs, is not completely understood, but may be related to prostaglandin synthetase inhibition."（[DailyMed: Etodolac Er (etodolac) prescribing information, Advanced Rx Pharmacy of Tennessee, LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=baebdfb2-17f6-9081-e053-2a95a90ab331)、版 2024-12-31、参照日 2026-11-19）。既知の情報によると、エトドラクは COX-2 選択性の高い非ステロイド性抗炎症薬（NSAID）で、プロスタグランジン合成を抑えて炎症と痛みを軽減し、関節リウマチなどで使用されてきました。

ただし、予測された肢端中間部異形成症は GDF5（CDMP1）の異常による遺伝性骨格異形成症で、炎症が主因の疾患ではありません。そのため機序的な裏付けは乏しく、このスコアは TxGNN モデル（深層学習）によるもので、関連する疾患間でモデルが学習した類似性を反映している可能性があり、生物学的な証拠ではありません。

上位 5 件のうち、機序的にもっともらしいのは 4 位の脊椎関節症感受性（NSAID は脊椎関節炎の第一選択薬）です。ただしこれは遺伝的感受性を表す用語で、エトドラク固有の試験や文献はありません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

予測 1 位の疾患(先端中間異形成 Hunter-Thompson 型)に関する文献はありません。以下は関連疾患の文献です。いずれもこの疾患に特化した試験ではなく、間接的なエビデンスです。

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [1717225](https://pubmed.ncbi.nlm.nih.gov/1717225/) | 1991 | Review | Drugs | エトドラクは関節リウマチ、変形性関節症、強直性脊椎炎、術後痛に有効で、他の NSAID と同等以上。有害事象は腹痛・消化不良が中心 |
| [17694363](https://pubmed.ncbi.nlm.nih.gov/17694363/) | 1997 | Review | Inflammopharmacology | COX-2 選択的作用を持つ多目的鎮痛薬としての臨床レビュー。強直性脊椎炎や痛風にも広く使用 |
| [2146130](https://pubmed.ncbi.nlm.nih.gov/2146130/) | 1990 | Review | Eur J Rheumatol Inflamm | 関節リウマチ、変形性関節症、強直性脊椎炎での無作為化二重盲検試験の概要。標準的 NSAID と同程度の有効性 |
| [22071858](https://pubmed.ncbi.nlm.nih.gov/22071858/) | 2011 | Review | Cochrane Database Syst Rev | メトトレキサート使用中の炎症性関節炎患者における NSAID 併用の安全性 |
| [20829199](https://pubmed.ncbi.nlm.nih.gov/20829199/) | 2011 | Review | Ann Rheum Dis | 体軸性脊椎関節炎の試験における NSAID 摂取量の収集・解析に関する ASAS 推奨 |
| [2525800](https://pubmed.ncbi.nlm.nih.gov/2525800/) | 1989 | Cohort | Rev Med Interne | リウマチ専門医 974 名、患者 4,947 名の非盲検試験での有効性と忍容性 |
| [2150569](https://pubmed.ncbi.nlm.nih.gov/2150569/) | 1990 | Cohort | Rheumatol Int | フランスの大規模非盲検試験（4,947 名）と市販後安全性調査（51,355 名） |
| [2150568](https://pubmed.ncbi.nlm.nih.gov/2150568/) | 1990 | Cohort | Rheumatol Int | 4 か国の市販後調査（計 8,334 名）で良好な安全性プロファイル |

## 日本市販情報

現在、承認には有効なものと薬価基準から削除済みのものがあります（件数はクイック概要を参照）。

<!-- review:begin jp-lic-20261117-etodolac-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「現在、有効な承認は 12 件中 12 件です（主要 5 件を記載）。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（622710600（廃止年月日 2026-03-31）、670406388（廃止年月日 2026-03-31）、670406383（廃止年月日 2026-03-31）、610406383（廃止年月日 2026-03-31）、610406382（廃止年月日 2026-03-31）、670406382（廃止年月日 2026-03-31）ほか）。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-etodolac-1 -->

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 670406387 | ハイペン錠１００ｍｇ（選） | 有効 |
| 622710600 | エトドラク２００ｍｇ錠 | 薬価削除（2026-03-31） |
| 621466202 | エトドラク錠２００ｍｇ「ＳＷ」 | 有効 |
| 622011102 | エトドラク錠１００ｍｇ「ＳＷ」 | 有効 |
| 670406383 | オステラック錠２００ ２００ｍｇ（選） | 薬価削除（2026-03-31） |

上表はデータ上の 12 件のうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **禁忌に関連しうる疾患（知識グラフ上の情報、添付文書の記載ではありません）**：高血圧、腎疾患、肝疾患、胆嚢疾患、消化性潰瘍（活動性を含む）、血液凝固障害、心筋梗塞、冠動脈血栓症、心血管疾患、心疾患、ヘモグロビン異常症、尿管膿瘍
- **薬物相互作用**：100 件が確認されています。主なものは次のとおりです。
  - 中等度：アセチルサリチル酸、副腎皮質ステロイド（ヒドロコルチゾン、デキサメタゾン、ベタメタゾン、トリアムシノロン、ブデソニド）、メトホルミン、スルホニル尿素薬（グリメピリド、クロルプロパミド）、レパグリニド、メサラジン、バルサラジド、クエン酸カリウム、重炭酸カリウム、ピコスルファート、ポリエチレングリコール製剤
  - 軽微：H2 受容体拮抗薬（ファモチジン、ラニチジン、シメチジン）、リナクロチド

添付文書の警告・禁忌の情報は未取得のため、使用前に添付文書を確認してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測 1 位の疾患は炎症が主因ではない遺伝性骨格異形成症で、臨床試験も文献もなく、モデル予測のみ（L5）です。日本では販売されており（有効な承認あり、件数はクイック概要を参照）、添付文書ベースの安全性情報は未確認です。

<!-- review:begin jp-lic-20261117-etodolac-2 -->

> **確認による訂正（2026-11-17）**：元の記載は「日本では販売されており（有効な承認は 12 件中 12 件）、」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（622710600（廃止年月日 2026-03-31）、670406388（廃止年月日 2026-03-31）、670406383（廃止年月日 2026-03-31）、610406383（廃止年月日 2026-03-31）、610406382（廃止年月日 2026-03-31）、670406382（廃止年月日 2026-03-31）ほか）。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-etodolac-2 -->

**進める場合に必要なもの：**
- 添付文書（警告・禁忌）の取得と安全性スクリーニング
- 詳細な作用機序（MOA）データの補充
- 日本での承認状況の確認（有効な承認と薬価基準から削除済みの承認があり、件数はクイック概要を参照）

<!-- review:begin jp-lic-20261117-etodolac-3 -->

> **確認による訂正（2026-11-17）**：元の記載は「日本での承認状況の確認（現在、有効な承認は 12 件中 12 件）」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（622710600（廃止年月日 2026-03-31）、670406388（廃止年月日 2026-03-31）、670406383（廃止年月日 2026-03-31）、610406383（廃止年月日 2026-03-31）、610406382（廃止年月日 2026-03-31）、670406382（廃止年月日 2026-03-31）ほか）。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-etodolac-3 -->

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Etodolac Er (etodolac) prescribing information, Advanced Rx Pharmacy of Tennessee, LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=baebdfb2-17f6-9081-e053-2a95a90ab331) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：オステラック、ハイペン

**販売名（規格別）**：エトドラク100mg錠、エトドラク200mg錠、エトドラク錠100mg、エトドラク錠200mg、オステラック錠100 100mg、オステラック錠200 200mg、ハイペン錠100mg、ハイペン錠200mg
<!-- brand-names:end -->

