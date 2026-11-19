---
layout: default
title: Atenolol
parent: モデル予測のみ
nav_order: 31
evidence_level: L5
indication_count: 5
monitor_inn: "Atenolol"
predicted_indications: ["malignant hypertensive renal disease", "pulmonary hypertension with unclear multifactorial mechanism", "pulmonary hypertension owing to lung disease and/or hypoxia", "Braddock syndrome", "chronic pulmonary heart disease"]
last_modified_at: 2026-11-17
description: "Atenolol：予測新適応症は悪性高血圧性腎疾患（エビデンスレベル L5）。既存適応症：本態性高血圧症、狭心症、期外収縮"
---

# Atenolol
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **5** 件
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

## アテノロール：本態性高血圧症・狭心症・期外収縮から悪性高血圧性腎疾患へ
{: .text-alpha }

## 一言要約

アテノロールは β1 選択的遮断薬で、日本では本態性高血圧症、狭心症、期外収縮の治療に使用されています。
TxGNN モデルは**悪性高血圧性腎疾患 (malignant hypertensive renal disease)** に有効である可能性を予測していますが、この疾患を直接検討した臨床試験・文献はなく、エビデンスはモデル予測のみ (L5) です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 本態性高血圧症、狭心症、期外収縮 |
| 予測新規適応症 | 悪性高血圧性腎疾患 |
| TxGNN 予測スコア | 0.9985 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 18 件／全 20 件） |
| 承認番号数 | 20 件（有効 18 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Atenolol の添付文書（Prescribing Information）の「Clinical Pharmacology」の項によると（非公式訳）、「TENORMINは、膜安定化作用および内因性交感神経刺激（部分作動）作用を有しないβ 1 選択性（心臓選択性）βアドレナリン受容体遮断薬である。ただし、この選択的作用は絶対的なものではなく、高用量では、TENORMINは主に気管支および血管の筋組織に存在するβ 2 アドレナリン受容体も阻害する。」英語原文："TENORMIN is a beta 1 -selective (cardioselective) beta-adrenergic receptor blocking agent without membrane stabilizing or intrinsic sympathomimetic (partial agonist) activities. This preferential effect is not absolute, however, and at higher doses, TENORMIN inhibits beta 2 -adrenoreceptors, chiefly located in the bronchial and vascular musculature."（[DailyMed: Tenormin (atenolol) prescribing information, Upsher-Smith Laboratories, LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=6e850b1e-28a4-4ff8-8ed7-bb0b29faa28a)、版 2025-09-18、参照日 2026-11-19）。既知の情報によると、アテノロールは β1 選択的遮断薬で、心拍数と心拍出量を低下させ、レニン分泌も抑制します。これらは血圧低下に寄与すると考えられます。

既存適応症の本態性高血圧症と、予測された悪性高血圧性腎疾患は、いずれも高血圧に関連する病態です。血圧を下げることで腎障害の進行を抑える可能性が、機序的には想定されます。

ただし、これは一般的な薬理学的推測にとどまります。この疾患に対する臨床試験や文献は、今回まとめたデータには含まれていません。予測は TxGNN のスコアのみに基づいています。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

なお、同じ薬物の他の予測候補（肺高血圧症、慢性肺性心など）には文献が紐づいていますが、いずれも悪性高血圧性腎疾患を直接検討したものではないため、本予測の根拠としては扱いません。

## 日本市販情報

日本では 20 件の単剤の承認（うち有効 18 件、2 件は薬価基準から削除済み）があり、以下は主要な 5 件です。

<!-- review:begin jp-lic-20261117-atenolol-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「日本では 20 件の単剤の承認（すべて有効）があり、」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、データ上の 20 件のうち有効（収載中）は 18 件で、2 件は経過措置期間満了などにより薬価基準から削除されています（620254560（廃止年月日 2026-09-30、後継コード 610461003）、620254424（廃止年月日 2026-09-30、後継コード 610461002））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-atenolol-1 -->

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 620002066 | テノーミン錠25 25mg | 錠 | 抗不整脈薬、血圧降下薬、血管拡張薬、β1遮断薬。本態性高血圧症、狭心症、期外収縮 |
| 620002067 | テノーミン錠50 50mg | 錠 | 抗不整脈薬、血圧降下薬、血管拡張薬、β1遮断薬。本態性高血圧症、狭心症、期外収縮 |
| 612120318 | アルセノール錠25 25mg | 錠 | 抗不整脈薬、血圧降下薬、血管拡張薬、β1遮断薬。本態性高血圧症、狭心症、期外収縮 |
| 620254411 | アテノロール錠25mg「サワイ」 | 錠 | 抗不整脈薬、血圧降下薬、血管拡張薬、β1遮断薬。本態性高血圧症、狭心症、期外収縮 |
| 620254560 | アテノロール錠50mg「JG」 | 錠 | 抗不整脈薬、血圧降下薬、血管拡張薬、β1遮断薬。本態性高血圧症、狭心症、期外収縮 |

## 安全性に関する考慮事項

- **知識グラフ上の禁忌関係**（添付文書の記載ではありません）：肝不全、喘息（内因性・アレルギー性を含む）、糖尿病（1 型・2 型）、糖尿病性ケトアシドーシス、房室ブロック、レイノー病、アナフィラキシー、乾癬、痛風、全身性エリテマトーデス、膵炎などが挙げられています。
- **薬物相互作用**（100 件の記録のうち主なもの）：
  - 中等度：エピネフリン、ヒドロコルチゾン、ヒヨスチアミン、ブプロピオン、トリアムシノロン、モルヒネ、アセトヘキサミド、アトロピン、ベタメタゾン、ブデソニド、各種カルシウム製剤
  - 軽度：アセチルサリチル酸、水酸化アルミニウム、アタパルジャイト

添付文書の警告・禁忌の詳細は今回のデータに含まれていません。必ず添付文書を参照してください。また、悪性高血圧では急激な降圧が腎機能を悪化させ得るため、この集団での安全性は別途の評価が必要です。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測スコアは高いものの、悪性高血圧性腎疾患を直接検討した臨床試験・文献がなく、エビデンスはモデル予測のみ (L5) です。機序の妥当性も一般的な降圧作用に基づく推測にとどまります。

**進める場合に必要なもの：**
- 添付文書（PMDA）の警告・禁忌情報の取得と確認
- 詳細な作用機序データ（DrugBank など）の補充
- 悪性高血圧性腎疾患に関する既存の臨床研究・ガイドラインの系統的な文献調査
- 急激な降圧リスクや併存疾患（喘息、糖尿病、房室ブロックなど）を考慮した安全性評価計画
- 他の降圧薬（レニン・アンジオテンシン系阻害薬など）との位置づけの比較

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正 | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Tenormin (atenolol) prescribing information, Upsher-Smith Laboratories, LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=6e850b1e-28a4-4ff8-8ed7-bb0b29faa28a) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：アルセノール、テノーミン

**販売名（規格別）**：アテノロール25mg錠、アテノロール50mg錠、アテノロール錠25mg、アテノロール錠50mg、アルセノール錠25 25mg、アルセノール錠50 50mg、テノーミン錠25 25mg、テノーミン錠50 50mg
<!-- brand-names:end -->

