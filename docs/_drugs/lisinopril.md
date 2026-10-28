---
layout: default
title: Lisinopril
parent: モデル予測のみ
nav_order: 216
evidence_level: L5
indication_count: 6
monitor_inn: "Lisinopril"
predicted_indications: ["pulmonary hypertension with unclear multifactorial mechanism", "pulmonary hypertension owing to lung disease and/or hypoxia", "malignant hypertensive renal disease", "Braddock syndrome", "chronic pulmonary heart disease", "autosomal dominant familial hematuria-retinal arteriolar tortuosity-contractures syndrome"]
last_modified_at: 2026-10-27
description: "Lisinopril：予測新適応症は原因が不明確な多因子性の肺高血圧症 (pulmonary hypertension with unclear multifactorial mechanism)（エビデンスレベル L5）。既存適応症：日本の承認情報に適応症の記載なし"
---

# Lisinopril
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

## リシノプリル：ACE阻害薬 → 肺高血圧症（原因が不明確な多因子性、pulmonary hypertension with unclear multifactorial mechanism）
{: .text-alpha }

## 一言要約

リシノプリルはアンジオテンシン変換酵素（ACE）阻害薬に分類される降圧薬です。
TxGNN モデルは**原因が不明確な多因子性の肺高血圧症 (pulmonary hypertension with unclear multifactorial mechanism)** に有効である可能性を予測しています。
ただし、この疾患を直接検討した臨床試験・文献は現時点でなく、エビデンスはモデル予測のみ（L5）です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 原因が不明確な多因子性の肺高血圧症 (pulmonary hypertension with unclear multifactorial mechanism) |
| TxGNN 予測スコア | 0.9989 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 18 件／全 18 件） |
| 承認番号数 | 18 件（有効 18 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。既知の情報によると、リシノプリルは ACE 阻害薬に分類され、レニン・アンジオテンシン系（RAS）を抑えることで血圧を下げる薬です。

RAS を遮断すると、アンジオテンシン II による血管収縮や血管リモデリングが弱まる可能性があります。肺循環でも同様の作用が働けば、肺高血圧症に関与する血管の緊張や構造変化を和らげる可能性があると考えられます。

ただし、この考え方は予測に基づく仮説にとどまります。この疾患を対象とした臨床試験や文献は提供されておらず、機序の妥当性は実際の研究で確認されていません。

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 620006158 | リシノプリル錠１０ｍｇ「トーワ」 | 錠 | 高血圧症 |
| 672140651 | ロンゲス錠１０ｍｇ（選） | 錠 | 高血圧症 |
| 622102303 | リシノプリル錠２０ｍｇ「ＮＩＧ」 | 錠 | 高血圧症 |
| 622325000 | リシノプリル２０ｍｇ錠 | 錠 | 高血圧症 |
| 621945501 | リシノプリル錠２０ｍｇ「トーワ」 | 錠 | 高血圧症 |

ほかにも同一成分の承認が複数あり、上記は主要な 5 件のみです。

## 安全性に関する考慮事項

- **薬物相互作用**：重要度「Major」として、クエン酸カリウムおよび炭酸水素カリウムとの併用が挙げられています（高カリウム血症のリスクに注意）。また、副腎皮質ステロイド（ヒドロコルチゾン、デキサメタゾンなど）、糖尿病治療薬（メトホルミン、SGLT2 阻害薬、DPP-4 阻害薬など）、アスピリン、モルヒネなどとの併用は「Moderate」とされています。

安全性の詳細（警告・禁忌）については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
この疾患を直接検討した臨床試験や文献がなく、根拠は TxGNN の予測のみです。現時点では再利用の可否を判断できません。

**進める場合に必要なもの：**
- この疾患におけるリシノプリルの有効性を検討する臨床研究または前臨床研究の収集
- 詳細な薬物作用機序データ（MOA）の補充
- 添付文書の警告・禁忌情報の確認
- 肺高血圧症患者における低血圧・腎機能・カリウム値への影響の評価計画
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：ロンゲス

**販売名（規格別）**：リシノプリル10mg錠、リシノプリル20mg錠、リシノプリル5mg錠、リシノプリル錠10mg、リシノプリル錠20mg、リシノプリル錠5mg、ロンゲス錠10mg、ロンゲス錠20mg、ロンゲス錠5mg
<!-- brand-names:end -->

