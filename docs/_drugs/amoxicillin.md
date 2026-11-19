---
layout: default
title: Amoxicillin
parent: モデル予測のみ
nav_order: 25
evidence_level: L5
indication_count: 8
monitor_inn: "Amoxicillin"
predicted_indications: ["polyclonal hyperviscosity syndrome", "hyperamylasemia", "congenital analbuminemia", "blood group incompatibility", "premalignant hematological system disease", "monoclonal gammopathy", "hematological disease associated with an acquired peripheral neuropathy", "septicemic plague"]
last_modified_at: 2026-11-17
description: "Amoxicillin：予測新適応症はポリクローナル高粘稠度症候群 (polyclonal hyperviscosity syndrome)（エビデンスレベル L5）。既存適応症：淋菌感染症、梅毒、歯周組織炎、猩紅熱、ヘリコバクター・ピロリ感染症"
---

# Amoxicillin
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

## アモキシシリン：細菌感染症から多クローン性高粘稠度症候群へ
{: .text-alpha }

## 一言要約

アモキシシリンはβ-ラクタム系の抗生物質（細胞壁合成阻害薬）で、日本では淋菌感染症、梅毒、歯周組織炎、猩紅熱、ヘリコバクター・ピロリ感染症などの治療に使用されています。
TxGNN モデルは**ポリクローナル高粘稠度症候群 (polyclonal hyperviscosity syndrome)** に有効である可能性を予測していますが、この疾患を直接検討した臨床試験・文献はなく、**モデル予測のみ**の段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 淋菌感染症、梅毒、歯周組織炎、猩紅熱、ヘリコバクター・ピロリ感染症 |
| 予測新規適応症 | ポリクローナル高粘稠度症候群 (polyclonal hyperviscosity syndrome) |
| TxGNN 予測スコア | 0.9963 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 13 件／全 15 件） |
| 承認番号数 | 15 件（有効 13 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Amoxicillin の添付文書（Prescribing Information）の「Mechanism of Action」および「Microbiology」の項によると（非公式訳）、「アモキシシリンは抗菌薬である。[…] アモキシシリンは、活発な増殖期にある感受性菌に対してペニシリンと同様の殺菌作用を示す。細胞壁生合成を阻害することにより作用し、細菌を死滅させる。」英語原文："Amoxicillin is an antibacterial drug. […] Amoxicillin is similar to penicillin in its bactericidal action against susceptible bacteria during the stage of active multiplication. It acts through the inhibition of cell wall biosynthesis that leads to the death of the bacteria."（[DailyMed: amoxicillin prescribing information, PD-Rx Pharmaceuticals, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=98e9274c-c02e-44d9-8cc5-17536ef03a77)、版 2026-11-13、参照日 2026-11-19）。既知の情報によると、アモキシシリンはβ-ラクタム系抗生物質で、細菌の細胞壁合成を阻害して抗菌作用を示します。

一方、多クローン性高粘稠度症候群は、免疫グロブリンが過剰に増えることで血液の粘度が上がる病態です。細菌感染が原因ではないため、アモキシシリンの抗菌作用との機序的な接点は見当たりません。この予測のスコアはTxGNNモデル(ディープラーニング)によるもので、関連する疾患間でモデルが学習した類似性を反映している可能性があり、生物学的な根拠ではありません。臨床的・文献的な裏付けもありません。

なお、今回のデータでは他の予測候補（モノクローナル ガンマグロブリン血症、敗血症性ペストなど）にも文献や試験が見られますが、いずれも本疾患とは別の疾患に関するもので、本疾患の根拠にはなりません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 616130132 | サワシリン錠２５０ | 錠 250 mg | （記載なし） |
| 620006920 | サワシリン細粒１０％ | 細粒 10％ | （記載なし） |
| 622066602 | アモキシシリン細粒１０％「ＴＣＫ」 | 細粒 10％ | 淋菌感染症、梅毒、歯周組織炎、猩紅熱、ヘリコバクター・ピロリ感染症 |
| 621073001 | ワイドシリン細粒２０％ | 細粒 20％ | 淋菌感染症、梅毒、歯周組織炎、猩紅熱、ヘリコバクター・ピロリ感染症 |
| 622066502 | アモキシシリンカプセル１２５ｍｇ「ＴＣＫ」 | カプセル 125 mg | 淋菌感染症、梅毒、歯周組織炎、猩紅熱、ヘリコバクター・ピロリ感染症 |

承認は合計 15 件で、すべて単剤です。うち有効は 13 件です（2 件は薬価基準から削除済み）。上記は主要な 5 件を記載しています。

<!-- review:begin jp-lic-20261117-amoxicillin-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「承認は合計 15 件で、すべて単剤、有効な承認です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、データ上の 15 件のうち有効（収載中）は 13 件で、2 件は経過措置期間満了などにより薬価基準から削除されています（622899900（廃止年月日 2026-03-31）、622745300（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-amoxicillin-1 -->

## 安全性に関する考慮事項

- **知識グラフ上の禁忌関連疾患**（添付文書の記載ではなく、知識グラフの関係です）：QT延長症候群、トルサード・ド・ポワンツ、心室頻拍、肝不全・肝疾患・胆汁うっ滞、ポルフィリン症、腎疾患、クロストリジオイデス・ディフィシル大腸炎、重症筋無力症、骨粗鬆症・骨折、伝染性単核球症など。
- **薬物相互作用**（全 100 件中の一部）：
  - 重大（Major）：メトトレキサート、コレラ生ワクチン（Vibrio cholerae CVD 103-HgR 株）
  - 中等度（Moderate）：ドキシサイクリン、ミノサイクリン、エチニルエストラジオール、エストラジオール、ミコフェノール酸モフェチル、エンテカビルなど
  - 軽微（Minor）：アロプリノール、アジスロマイシン、クラリスロマイシン、エリスロマイシンなど

詳細は添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
本疾患を直接検討した臨床試験・文献はなく、機序的な根拠もないため、モデル予測のみ（L5）の段階です。現時点で開発を進める根拠はありません。

**進める場合に必要なもの：**
- 添付文書（PMDA）の警告・禁忌情報の取得
- 詳細な作用機序データ（DrugBank）の確認
- 本疾患との機序的関連を示す前臨床データ、または臨床的な報告の収集

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正 | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: amoxicillin prescribing information, PD-Rx Pharmaceuticals, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=98e9274c-c02e-44d9-8cc5-17536ef03a77) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：サワシリン、ワイドシリン

**販売名（規格別）**：アモキシシリン125mgカプセル、アモキシシリン250mgカプセル、アモキシシリンカプセル125mg、アモキシシリンカプセル250mg、アモキシシリン細粒10% 100mg、アモキシシリン細粒20% 200mg、サワシリンカプセル125 125mg、サワシリンカプセル250 250mg、サワシリン細粒10% 100mg、サワシリン錠250 250mg、ワイドシリン細粒20% 200mg
<!-- brand-names:end -->

