---
layout: default
title: Entecavir
parent: 中エビデンスレベル
nav_order: 111
evidence_level: L4
indication_count: 9
last_modified_at: 2026-11-24
description: "Entecavir：予測新適応症は慢性C型肝炎ウイルス感染 (chronic hepatitis C virus infection)（エビデンスレベル L4）。既存適応症：B型肝炎（抗ウイルス薬、逆転写酵素阻害薬）"
monitor_inn: "entecavir"
predicted_indications: ["chronic hepatitis C virus infection", "HIV infectious disease", "hepatitis C virus infection", "feline acquired immunodeficiency syndrome", "simian immunodeficiency virus infection", "neurodevelopmental disorder with ataxic gait, absent speech, and decreased cortical white matter", "hepatitis, viral, animal", "hepatitis E virus infection", "hepatitis A virus infection"]
---

# Entecavir
{: .fs-9 }

エビデンスレベル: **L4** | 予測適応症: **9** 件
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

## エンテカビル：B型肝炎から慢性C型肝炎ウイルス感染へ
{: .text-alpha }

## 一言要約

エンテカビルは逆転写酵素阻害薬で、元々B型肝炎の治療に使用されていました。
TxGNN モデルは**慢性C型肝炎ウイルス感染 (chronic hepatitis C virus infection)** に有効である可能性を予測していますが、エンテカビル自体に抗HCV作用は期待できません。関連する **2 件の臨床試験**はいずれも HCV/HBV 重複感染患者における HBV 再活性化の予防が主題で、文献も大半が総説です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | B型肝炎（抗ウイルス薬、逆転写酵素阻害薬） |
| 予測新規適応症 | 慢性C型肝炎ウイルス感染 (chronic hepatitis C virus infection) |
| TxGNN 予測スコア | 0.9998 |
| エビデンスレベル | L4 |
| 日本市販状況 | 販売中（有効な承認 11 件／全 14 件） |
| 承認番号数 | 14 件（有効 11 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Entecavir の添付文書（Prescribing Information）の「Mechanism of Action」および「Microbiology」の項によると（非公式訳）、「エンテカビルはB型肝炎ウイルスに対する抗ウイルス薬である。[…] エンテカビルはHBV逆転写酵素（rt）に対する活性を有するデオキシグアノシンヌクレオシド類似体であり、効率的にリン酸化されて活性型の三リン酸体となる。この三リン酸体の細胞内半減期は15時間である。エンテカビル三リン酸は天然基質であるデオキシグアノシン三リン酸と競合することにより、HBV逆転写酵素の3つの活性、すなわち塩基プライミング、プレゲノムメッセンジャーRNAからのマイナス鎖の逆転写、及びHBV DNAのプラス鎖の合成のすべてを機能的に阻害する。」英語原文："Entecavir is an antiviral drug against hepatitis B virus. […] Entecavir, a deoxyguanosine nucleoside analogue with activity against HBV reverse transcriptase (rt), is efficiently phosphorylated to the active triphosphate form, which has an intracellular half-life of 15 hours. By competing with the natural substrate deoxyguanosine triphosphate, entecavir triphosphate functionally inhibits all three activities of the HBV reverse transcriptase: base priming, reverse transcription of the negative strand from the pregenomic messenger RNA, and synthesis of the positive strand of HBV DNA."（[DailyMed: Baraclude (entecavir) prescribing information, E.R. Squibb & Sons, L.L.C.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=046e61c9-9298-4b2e-b76e-b26b81fecd20)、版 2019-11-06、参照日 2026-11-19）。既知の情報によると、エンテカビルはグアノシン類似体で、三リン酸体が dGTP と競合し、HBV ポリメラーゼのプライミング、逆転写、DNA 合成を阻害します。

HCV は NS5B RNA 依存性 RNA ポリメラーゼで複製する RNA ウイルスです。エンテカビルに HCV への直接作用は知られておらず、機序的な裏付けは乏しいと考えられます。予測された有用性は、HCV/HBV 重複感染患者で、HCV 治療（直接作用型抗ウイルス薬、DAA）中に起こる HBV 再活性化を抑える間接的なものに限られます。

したがって本予測は、HCV の治療そのものではなく、重複感染における HBV 管理としての位置づけで評価するのが適切です。

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT02555943](https://clinicaltrials.gov/study/NCT02555943) | Phase 2/3 | 完了 | 23 | HCV/HBV 重複感染患者で、抗HCV治療中の HBV 再活性化の発生率や関連因子を調べる前向き研究（エンテカビルは HBV 側のみに関与） |
| [NCT04405011](https://clinicaltrials.gov/study/NCT04405011) | フェーズ指定なし | 不明 | 60 | DAA 治療を受ける重複感染患者で、核酸アナログの予防投与が HBV 再活性化を防ぐか、12 週と 24 週を比較する 3 群無作為化試験 |

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [34864158](https://pubmed.ncbi.nlm.nih.gov/34864158/) | 2022 | 無作為化試験 | Clin Gastroenterol Hepatol | HCV/HBV 重複感染の DAA 治療中に、エンテカビルが HBV 再活性化を予防できるかを検証 |
| [36146665](https://pubmed.ncbi.nlm.nih.gov/36146665/) | 2022 | コホート | Viruses | 抗HCV抗体陽性のB型肝炎患者66例で、抗HBV治療後の HCV 再活性化を検討 |
| [24773464](https://pubmed.ncbi.nlm.nih.gov/24773464/) | 2014 | Review | Expert Opin Pharmacother | HBV/HCV 重複感染の治療の進歩を概説 |
| [25027705](https://pubmed.ncbi.nlm.nih.gov/25027705/) | 2014 | Review | Minerva Gastroenterol Dietol | B型・C型肝炎の抗ウイルス薬（エンテカビル含む）と腎機能への影響 |
| [32173307](https://pubmed.ncbi.nlm.nih.gov/32173307/) | 2020 | Review | Clin Res Hepatol Gastroenterol | 小児のB型・C型ウイルス性肝炎の現在と今後の管理 |
| [35327336](https://pubmed.ncbi.nlm.nih.gov/35327336/) | 2022 | Review | Biomedicines | 慢性ウイルス性肝炎の治療を概説 |

## 日本市販情報

承認には現在有効なものと薬価基準から削除済みのものがあります（件数はクイック概要を参照）。下記は代表的な 5 件です。

<!-- review:begin jp-lic-20261117-entecavir-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「現在有効な承認は 14 件中 14 件です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（622539701（廃止年月日 2026-03-31）、622690000（廃止年月日 2026-03-31）、622562603（廃止年月日 2026-09-30、後継コード 622611200））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-entecavir-1 -->

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 620004355 | バラクルード錠０．５ｍｇ | 有効 |
| 670004355 | バラクルード錠０．５ｍｇ（選） | 有効 |
| 622545901 | エンテカビル錠０．５ｍｇ「ＹＤ」 | 有効 |
| 622547802 | エンテカビル錠０．５ｍｇ「ＮＩＧ」 | 有効 |
| 622564401 | エンテカビル錠０．５ｍｇ「サンド」 | 有効 |

上表はデータ上の 14 件のうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **知識グラフ上の禁忌関連疾患**（添付文書の記載ではありません）：腎機能障害、脂肪肝、非アルコール性脂肪肝炎、乳酸アシドーシス
- **薬物相互作用**：44 件が登録されており、いずれも中等度です。主なものは以下のとおりです。
  - 腎排泄や腎毒性に関わる薬：アムホテリシンB（各製剤）、バンコマイシン、カナマイシン、ネオマイシン、ポリミキシンB、レボフロキサシン
  - 制酸薬・胃薬：ファモチジン、ラニチジン、シメチジン
  - 糖尿病薬：メトホルミン
  - 腸疾患治療薬：メサラジン、バルサラジド、オルサラジン、スルファサラジン
  - その他：アモキシシリン、オルリスタット

詳細な警告・禁忌は添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- エンテカビルには HCV への直接作用が期待できず、関連試験は重複感染での HBV 再活性化予防にとどまります。エビデンスはモデル予測と機序の推定が中心（L4）で、HCV 治療薬としての再利用候補とは言えません。
- 一方、HCV/HBV 重複感染における DAA 治療中の HBV 再活性化予防は、臨床的に意義のある別の問い（Research Question）です。

**進める場合に必要なもの：**
- 添付文書の警告・禁忌の確認（現時点では未取得）
- 作用機序データの補完
- 重複感染における HBV 再活性化予防を適応として位置づけ直すかの検討と、無作為化試験（NCT04405011、文献 PMID 34864158）の結果の精査
- 腎機能障害患者への投与量調整や、相互作用薬との併用リスクの評価

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Baraclude (entecavir) prescribing information, E.R. Squibb & Sons, L.L.C.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=046e61c9-9298-4b2e-b76e-b26b81fecd20) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：バラクルード

**販売名（規格別）**：エンテカビル0.5mg口腔内崩壊錠、エンテカビル0.5mg錠、エンテカビルOD錠0.5mg、エンテカビル錠0.5mg、バラクルード錠0.5mg
<!-- brand-names:end -->

