---
layout: default
title: Entecavir
parent: 中エビデンスレベル
nav_order: 111
evidence_level: L4
indication_count: 10
monitor_inn: "entecavir"
predicted_indications: ["chronic hepatitis C virus infection", "hepatitis B virus infection", "HIV infectious disease", "hepatitis C virus infection", "feline acquired immunodeficiency syndrome", "simian immunodeficiency virus infection", "neurodevelopmental disorder with ataxic gait, absent speech, and decreased cortical white matter", "hepatitis, viral, animal", "hepatitis E virus infection", "hepatitis A virus infection"]
last_modified_at: 2026-10-17
description: "Entecavir：予測新適応症は慢性C型肝炎ウイルス感染 (chronic hepatitis C virus infection)（エビデンスレベル L4）。既存適応症：B型肝炎（抗ウイルス薬、逆転写酵素阻害薬）"
---

# Entecavir
{: .fs-9 }

エビデンスレベル: **L4** | 予測適応症: **10** 件
{: .fs-6 .fw-300 }

---

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist">

## 薬剤師評価レポート

</div>

# エンテカビル：B型肝炎から慢性C型肝炎ウイルス感染へ

## 一言要約

エンテカビルは逆転写酵素阻害薬で、元々B型肝炎の治療に使用されていました。
TxGNN モデルは**慢性C型肝炎ウイルス感染 (chronic hepatitis C virus infection)** に有効である可能性を予測していますが、エンテカビル自体に抗HCV作用は期待できません。関連する **2 件の臨床試験**はいずれも HCV/HBV 重複感染患者における HBV 再活性化の予防が主題で、文献も大半が総説です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | B型肝炎（抗ウイルス薬、逆転写酵素阻害薬） |
| 予測新規適応症 | 慢性C型肝炎ウイルス感染 (chronic hepatitis C virus infection) |
| TxGNN 予測スコア | 99.98% |
| エビデンスレベル | L4 |
| 日本市販状況 | 現在有効な承認なし（承認 14 件はすべて整理・失効済み） |
| 承認番号数 | 14 件 |
| 推奨決定 | Hold |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。既知の情報によると、エンテカビルはグアノシン類似体で、三リン酸体が dGTP と競合し、HBV ポリメラーゼのプライミング、逆転写、DNA 合成を阻害します。

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

現在有効な承認はなく、下記はすべて整理・失効済みの承認です（代表的な 5 件）。

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 620004355 | バラクルード錠０．５ｍｇ | 錠 | B型肝炎（抗ウイルス薬、逆転写酵素阻害薬） |
| 670004355 | バラクルード錠０．５ｍｇ（選） | 錠 | B型肝炎（抗ウイルス薬、逆転写酵素阻害薬） |
| 622545901 | エンテカビル錠０．５ｍｇ「ＹＤ」 | 錠 | B型肝炎（抗ウイルス薬、逆転写酵素阻害薬） |
| 622547802 | エンテカビル錠０．５ｍｇ「ＮＩＧ」 | 錠 | B型肝炎（抗ウイルス薬、逆転写酵素阻害薬） |
| 622564401 | エンテカビル錠０．５ｍｇ「サンド」 | 錠 | B型肝炎（抗ウイルス薬、逆転写酵素阻害薬） |

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
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---



<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：エンテカビル、バラクルード

**販売名（規格別）**：エンテカビル0.5mg口腔内崩壊錠、エンテカビル0.5mg錠、エンテカビルOD錠0.5mg、エンテカビル錠0.5mg、バラクルード錠0.5mg
<!-- brand-names:end -->

