---
layout: default
title: Propranolol
parent: モデル予測のみ
nav_order: 258
evidence_level: L5
indication_count: 4
last_modified_at: 2026-11-24
description: "Propranolol：予測新適応症は遠位型ミオパチー・舘山型 (distal myopathy, Tateyama type)（エビデンスレベル L5）。既存適応症：本態性高血圧症、狭心症、期外収縮、頻拍性心房細動、新鮮心房細動、乳児血管腫"
monitor_inn: "Propranolol"
predicted_indications: ["distal myopathy, Tateyama type", "congenital myopathy with excess of thin filaments", "chondroma", "cirrhotic cardiomyopathy"]
---

# Propranolol
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

## プロプラノロール：本態性高血圧症・不整脈から遠位型ミオパチー（舘山型）へ
{: .text-alpha }

## 一言要約

プロプラノロールは非選択的β遮断薬で、日本では本態性高血圧症、狭心症、期外収縮、頻拍性心房細動、乳児血管腫などに使われてきました。
TxGNN モデルは**遠位型ミオパチー（舘山型）(distal myopathy, Tateyama type)** に有効である可能性を高スコアで予測しています。
ただし、この予測を支持する臨床試験・文献は **0 件**で、エビデンスはモデル予測のみ（L5）です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 本態性高血圧症、狭心症、期外収縮、頻拍性心房細動、新鮮心房細動、乳児血管腫 |
| 予測新規適応症 | 遠位型ミオパチー・舘山型 (distal myopathy, Tateyama type) |
| TxGNN 予測スコア | 0.9940 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 7 件／全 8 件） |
| 承認番号数 | 8 件（有効 7 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Propranolol の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「プロプラノロールの降圧作用の機序は確立されていない。降圧作用に寄与する因子として、心拍出量の減少、腎臓からのレニン放出の阻害、及び脳の血管運動中枢からの持続的な交感神経出力の減弱が挙げられる。」英語原文："The mechanism of the antihypertensive effect of propranolol has not been established. Among factors that contribute to the antihypertensive action are: decreased cardiac output, inhibition of renin release by the kidneys, and diminution of tonic sympathetic nerve outflow from vasomotor centers in the brain."（[DailyMed: Inderal Xl (propranolol hydrochloride) prescribing information, ANI Pharmaceuticals, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=ac196ff5-9215-402b-bc57-69aa87f8bade)、版 2026-08-27、参照日 2026-11-19）。既知の情報では、プロプラノロールはβ₁/β₂受容体を非選択的に遮断し、心拍数・心収縮力・交感神経刺激を抑える薬です。この作用が高血圧、狭心症、頻脈性不整脈での有効性の基盤になっています。

一方、舘山型遠位型ミオパチーはカベオリン-3 に関連する筋疾患で、既存適応症の循環器疾患とは病態が大きく異なります。β遮断がこの疾患の病態に作用するという機序的な関連は、現時点で見当たりません。高スコアは TxGNN モデル（ディープラーニング）が学習した関連疾患間の類似性を反映している可能性があり、生物学的な裏付けではなく、機序面の裏付けは乏しいと考えます。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

## 日本市販情報

現在、承認には有効なものと薬価基準から削除済みのものがあり（件数はクイック概要を参照）、有効なものには下記を含みます。

<!-- review:begin jp-lic-20261117-propranolol-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「現在、8 件の承認のうち 8 件が有効で、下記を含みます。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（672120016（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-propranolol-1 -->

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 622890300 | プロプラノロール塩酸塩１０ｍｇ錠 | 有効 |
| 620252712 | プロプラノロール塩酸塩錠１０ｍｇ「ツルハラ」 | 有効 |
| 620252713 | プロプラノロール塩酸塩錠１０ｍｇ「日医工」 | 有効 |
| 612120016 | インデラル錠１０ｍｇ | 有効 |
| 620252707 | プロプラノロール塩酸塩錠１０ｍｇ「トーワ」 | 有効 |

上表はデータ上の 8 件のうち 5 件です。

<!-- licenses:end -->

このほか、インデラル注射液2mg、徐放カプセル60mg「サワイ」の承認も有効です（インデラル錠10mg（選）は薬価基準から削除済み）。

<!-- review:begin jp-lic-20261117-propranolol-3 -->

> **確認による訂正（2026-11-17）**：元の記載は「このほか、インデラル錠10mg（選）、インデラル注射液2mg、徐放カプセル60mg「サワイ」の承認もあり、いずれも有効です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（672120016（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-propranolol-3 -->

## 安全性に関する考慮事項

- **知識グラフ上の禁忌シグナル**（添付文書の記載ではなく、TxGNN 知識グラフの薬物・疾患関係に基づく）：
  - **筋疾患関連**：ミオパチー、筋疾患、骨格筋疾患、家族性周期性四肢麻痺、重症筋無力症。予測された新規適応症が筋疾患であるため、特に重要です。
  - **代謝・内分泌**：糖尿病、糖尿病性ケトアシドーシス、カリウム欠乏症、高尿酸血症、痛風、副甲状腺機能亢進症、高カルシウム血症
  - **肝・腎・消化器**：肝疾患、肝性昏睡、肝性脳症、腎疾患、無尿、膵炎、胆嚢疾患
  - **その他**：気管支炎、不安障害、全身性エリテマトーデス
- **薬物相互作用**（併用薬 100 件の検索結果から主要なもの）：
  - **重大 (Major)**：エピネフリン
  - **中等度 (Moderate)**：副腎皮質ステロイド（ヒドロコルチゾン、デキサメタゾン、ベタメタゾン、ブデソニド、トリアムシノロン）、抗コリン薬（アトロピン、ヒヨスチアミン、メスコポラミン）、ブプロピオン、モルヒネ、ロルカセリン、シメチジン、カナグリフロジン、クロルプロパミド、カルシウム製剤

警告・禁忌の添付文書情報は今回取得できていません。必ず添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 予測スコアは高いものの、臨床試験・文献が一切なく、β遮断と筋疾患の病態との機序的な関連も見いだせません。
- 知識グラフ上、筋疾患が禁忌シグナルとして挙がっているため、現時点で進める根拠はありません。

**進める場合に必要なもの：**
- 詳細な作用機序データの取得（DrugBank など）
- 添付文書の警告・禁忌情報の取得と安全性評価（PMDA）
- カベオリン-3 関連ミオパチーとβ遮断の関係を示す前臨床データまたは症例報告の調査
- 筋疾患に対する禁忌シグナルの妥当性確認
- 日本で販売されており、有効な承認があること（件数はクイック概要を参照）を踏まえた、供給・剤形の確認

<!-- review:begin jp-lic-20261117-propranolol-2 -->

> **確認による訂正（2026-11-17）**：元の記載は「日本で販売されており、8 件の承認がすべて有効であることを踏まえた、供給・剤形の確認」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（672120016（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-propranolol-2 -->

**参考：同じ予測リストでエビデンスのある候補**

予測リストの下位には、文献が確認できる候補があります。優先度の再検討に使えます。

| 予測疾患 | エビデンスレベル | 備考 |
|------|------|------|
| 肝硬変性心筋症 | L3 | コホート研究 3 編。QT 延長の補正が示唆される一方、進行した肝硬変では循環・腎機能への悪影響の報告もあり、利益とリスクの慎重な評価が必要 |
| 心筋症 | L4 | 文献の大半が総説で、心筋症に特化した RCT はなし。病型が不明確 |
| 筋肉内血管腫、乳腺類上皮血管腫、乳腺毛細血管腫 | L4 | 乳児血管腫の文献（日本で既承認）からの間接的な外挿。各疾患に特化したエビデンスはない |

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Inderal Xl (propranolol hydrochloride) prescribing information, ANI Pharmaceuticals, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=ac196ff5-9215-402b-bc57-69aa87f8bade) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：インデラル、ヘマンジオル

**販売名（規格別）**：インデラル注射液2mg 0.1%2mL、インデラル錠10mg、プロプラノロール塩酸塩10mg錠、プロプラノロール塩酸塩徐放カプセル60mg、プロプラノロール塩酸塩錠10mg
<!-- brand-names:end -->

