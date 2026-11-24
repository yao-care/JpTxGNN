---
layout: default
title: Dextromethorphan
parent: モデル予測のみ
nav_order: 91
evidence_level: L5
indication_count: 5
last_modified_at: 2026-11-24
description: "Dextromethorphan：予測新適応症は鼻腔疾患 (nasal cavity disease)（エビデンスレベル L5）。既存適応症：鎮咳薬（気管支拡張症）"
monitor_inn: "Dextromethorphan"
predicted_indications: ["nasal cavity disease", "faucial diphtheria", "trigeminal autonomic cephalalgia", "cervical disc degenerative disorder", "allergic urticaria"]
---

# Dextromethorphan
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

## デキストロメトルファン：鎮咳薬（気管支拡張症）から鼻腔疾患へ
{: .text-alpha }

## 一言要約

デキストロメトルファンは、日本で鎮咳薬として使われてきた薬で、承認適応症は気管支拡張症に伴う咳です。
TxGNN モデルは**鼻腔疾患 (nasal cavity disease)** に有効である可能性を予測していますが、関連する臨床試験と文献は **0 件**で、予測スコアのみが根拠です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 鎮咳薬（気管支拡張症） |
| 予測新規適応症 | 鼻腔疾患 (nasal cavity disease) |
| TxGNN 予測スコア | 0.9998 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 7 件／全 7 件） |
| 承認番号数 | 7 件（有効 7 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した dextromethorphan hydrobromide, bupropion hydrochloride（Dextromethorphanを含む配合剤） の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「デキストロメトルファンは、NMDA受容体（イオンチャネル型グルタミン酸受容体）の不競合的拮抗薬であり、シグマ-1受容体作動薬である。MDD及びアルツハイマー病による認知症に伴う激越の治療におけるデキストロメトルファンの作用機序は明らかではない。」英語原文："Dextromethorphan is an uncompetitive antagonist of the NMDA receptor (an ionotropic glutamate receptor) and a sigma-1 receptor agonist. The mechanism of dextromethorphan in the treatment of MDD and agitation associated with dementia due to Alzheimer’s disease is unclear."（[DailyMed: Auvelity (dextromethorphan hydrobromide, bupropion hydrochloride) prescribing information, Axsome Therapeutics, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=dcefda7c-9a68-278e-e053-2995a90aec79)、版 2026-08-17、参照日 2026-11-19）。ただし、デキストロメトルファンは NMDA 受容体拮抗作用とシグマ-1 受容体作動作用を持ち、脳幹の咳中枢に働いて咳反射を抑える中枢性鎮咳薬として知られています。

既存適応症は気管支拡張症に伴う咳で、予測された鼻腔疾患は同じ上気道・呼吸器領域にあります。ただし、鼻腔病変そのものに作用する機序を示すデータは、今回まとめたデータの中にありません。

そのため、この予測は TxGNN スコアのみに依存しており、機序面の裏付けは弱いと判断します。

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 621369301 | デキストロメトルファン臭化水素酸塩細粒１０％「ツルハラ」 | 有効 |
| 612220325 | メジコン錠１５ｍｇ | 有効 |
| 620374001 | デキストロメトルファン臭化水素酸塩錠１５ｍｇ「ツルハラ」 | 有効 |
| 620374101 | デキストロメトルファン臭化水素酸塩錠１５ｍｇ「トーワ」 | 有効 |
| 620374204 | デキストロメトルファン臭化水素酸塩錠１５ｍｇ「ＮＰ」 | 有効 |

上表はデータ上の 7 件のうち 5 件です。

<!-- licenses:end -->

7 件の承認のうち 7 件が有効です。

## 安全性に関する考慮事項

- **薬物相互作用（重大）**：デキスフェンフルラミン、ドラセトロン、フェンフルラミン、グラニセトロン、ロルカセリン、オンダンセトロン、パロノセトロン、シブトラミン。セロトニン系やQT延長に関わる薬剤が中心です。
- **薬物相互作用（中等度）**：ブプロピオン、モルヒネ、シメチジン、ドロナビノール、エリグルスタット、メトクロプラミド、オピウム、フェンテルミンなど。
- **知識グラフ上の禁忌関連疾患**（添付文書の記載ではありません）：高血圧、QT延長症候群、torsades de pointes、肝不全・肝疾患、てんかん、COPD、腎疾患、膵炎、消化性潰瘍、糖尿病、甲状腺機能低下症、副腎皮質機能不全、前立腺肥大症、血小板減少症など。

警告・禁忌の正式な情報は、添付文書で確認してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測スコアは高いものの、鼻腔疾患に関する臨床試験・文献がなく、機序的な裏付けもありません。エビデンスはモデル予測のみ（L5）です。なお、スコアは TxGNN モデル（深層学習）によるもので、モデルが学習した関連疾患間の類似性を反映している可能性があり、生物学的エビデンスではありません。日本では市販されており、7 件の承認すべてが有効です。

**進める場合に必要なもの：**
- 鼻腔疾患に対する作用機序の検討と、関連する前臨床・臨床データの収集
- PMDA 添付文書の警告・禁忌の取得と、安全性評価
- 作用機序（MOA）データの補完
- 剤形・投与経路の適合性の確認
- 販売再開の可否を含む、日本での規制上の位置づけの確認

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Auvelity (dextromethorphan hydrobromide, bupropion hydrochloride) prescribing information, Axsome Therapeutics, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=dcefda7c-9a68-278e-e053-2995a90aec79) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：メジコン

**販売名（規格別）**：デキストロメトルファン臭化水素酸塩細粒10%、デキストロメトルファン臭化水素酸塩錠15mg、メジコン散10%、メジコン錠15mg

**配合剤（この成分を含む）**：メジコン配合シロップ
<!-- brand-names:end -->

