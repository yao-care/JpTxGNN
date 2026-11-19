---
layout: default
title: Panitumumab
parent: モデル予測のみ
nav_order: 235
evidence_level: L5
indication_count: 2
monitor_inn: "Panitumumab"
predicted_indications: ["drug-induced osteoporosis", "severe nonproliferative diabetic retinopathy"]
last_modified_at: 2026-11-20
description: "Panitumumab：予測新適応症は薬剤性骨粗鬆症 (Drug-induced Osteoporosis)（エビデンスレベル L5）。既存適応症：転移性結腸癌"
---

# Panitumumab
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

## パニツムマブ：転移性結腸癌から薬剤性骨粗鬆症へ
{: .text-alpha }

## 一言要約

パニツムマブは抗 EGFR モノクローナル抗体で、元々転移性結腸癌の治療に使用されていました。
TxGNN モデルは**薬剤性骨粗鬆症 (Drug-induced Osteoporosis)** に有効である可能性を予測していますが、
現在、関連する臨床試験や文献は **0 件**で、モデル予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 転移性結腸癌 |
| 予測新規適応症 | 薬剤性骨粗鬆症 (Drug-induced Osteoporosis) |
| TxGNN 予測スコア | 0.9913 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 2 件／全 2 件） |
| 承認番号数 | 2 件（有効 2 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Panitumumab の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「EGFR は膜貫通型糖タンパク質であり、EGFR、HER2、HER3 及び HER4 を含む I 型受容体チロシンキナーゼのサブファミリーの一員である。EGFR は、皮膚及び毛包を含む正常上皮組織において恒常的に発現している。[…] パニツムマブは正常細胞及び腫瘍細胞の両方の EGFR に特異的に結合し、EGFR に対するリガンドの結合を競合的に阻害する。」英語原文："The EGFR is a transmembrane glycoprotein that is a member of a subfamily of type I receptor tyrosine kinases, including EGFR, HER2, HER3, and HER4. EGFR is constitutively expressed in normal epithelial tissues, including the skin and hair follicle. […] Panitumumab binds specifically to EGFR on both normal and tumor cells, and competitively inhibits the binding of ligands for EGFR."（[DailyMed: Vectibix (panitumumab) prescribing information, Amgen, Inc](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=e0fa4bca-f245-4d92-ae29-b0c630a315c2)、版 2026-06-23、参照日 2026-11-19）。既知の情報によると、パニツムマブは抗 EGFR モノクローナル抗体であり、転移性結腸癌での使用が知られています。

EGFR シグナルは骨芽細胞の分化や骨リモデリングに関与するとされますが、この関連は間接的で推測の域を出ません。むしろ EGFR 阻害により、低マグネシウム血症や低カルシウム血症が生じ、骨の健康を悪化させる可能性も考えられます。

したがって、この適応症は TxGNN の予測のみに基づいており、機序的な裏付けは弱いと評価されます。

なお、2 番目の予測候補は**重症非増殖性糖尿病網膜症**（スコア 0.9905、エビデンスレベル L5、推奨 Hold）です。EGFR 阻害が VEGF 依存の血管新生や炎症経路と相互作用する可能性はありますが、仮説の段階です。全身投与の大型抗体であり眼への確立した投与経路がなく、EGFR 阻害薬には眼毒性のリスクもあります。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 622086201（取消） | ベクティビックス点滴静注400mg 20mL | 注射剤 400mg 20mL | 記載なし |
| 621985901（取消） | ベクティビックス点滴静注100mg 5mL | 注射剤 100mg 5mL | 記載なし |

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 分子標的薬（抗 EGFR モノクローナル抗体） |
| 骨髄抑制リスク | 添付文書の警告および注意事項を参照してください |
| 催吐性分類 | 添付文書の警告および注意事項を参照してください |
| モニタリング項目 | 電解質（特にマグネシウム、カルシウム）、皮膚・眼症状の観察 |
| 取り扱い防護 | 添付文書の警告および注意事項を参照してください |

## 安全性に関する考慮事項

- **薬物相互作用**：27 件の相互作用が報告されています（DDInter）。主なものは以下の通りです。
  - **Major**：ベバシズマブ、イリノテカン（リポソーム製剤を含む）、アミオダロン、三酸化ヒ素、ドフェチリド、ドロネダロン、ドロペリドール、アミノレブリン酸、レバセチルメサドール
  - **Moderate**：プロトンポンプ阻害薬（ラベプラゾール、オメプラゾール、デクスランソプラゾール、エソメプラゾール、ランソプラゾール、パントプラゾール）、メトキサレン、ジソピラミド、イデラリシブ など

警告・禁忌については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測は TxGNN モデルのみに基づき、臨床試験・文献のエビデンスがありません。EGFR 阻害による電解質異常（低マグネシウム・低カルシウム血症）が骨代謝を悪化させる懸念もあります。なお、日本では販売されており、2件の承認のうち2件が有効です。

**進める場合に必要なもの：**
- 添付文書（PMDA）の警告・禁忌情報の取得と安全性評価
- 詳細な薬物作用機序データ（MOA）の補完
- EGFR 経路と骨代謝の関連を示す前臨床・機序研究
- 薬剤性骨粗鬆症に対する観察研究または臨床試験の有無の確認
- 既存の注射剤の日本での再供給可否の確認

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Vectibix (panitumumab) prescribing information, Amgen, Inc](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=e0fa4bca-f245-4d92-ae29-b0c630a315c2) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：ベクティビックス

**販売名（規格別）**：ベクティビックス点滴静注100mg 5mL、ベクティビックス点滴静注400mg 20mL
<!-- brand-names:end -->

