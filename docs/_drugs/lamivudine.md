---
layout: default
title: Lamivudine
parent: モデル予測のみ
nav_order: 200
evidence_level: L5
indication_count: 5
monitor_inn: "Lamivudine"
predicted_indications: ["simian immunodeficiency virus infection", "feline acquired immunodeficiency syndrome", "neurodevelopmental disorder with ataxic gait, absent speech, and decreased cortical white matter", "obsolete familial combined hyperlipidemia", "chronic hepatitis C virus infection"]
last_modified_at: 2026-10-28
description: "Lamivudine：予測新適応症はサル免疫不全ウイルス感染症 (simian immunodeficiency virus infection)（エビデンスレベル L5）。既存適応症：日本の承認情報に適応症の記載なし"
---

# Lamivudine
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

## ラミブジン：逆転写酵素阻害薬 → サル免疫不全ウイルス感染症 (simian immunodeficiency virus infection)
{: .text-alpha }

## 一言要約

ラミブジンはヌクレオシド系逆転写酵素阻害薬です。
TxGNN モデルは**サル免疫不全ウイルス感染症 (simian immunodeficiency virus infection)** に有効である可能性を予測しています。
関連する臨床試験の登録はなく、**15 編の文献**（主にマカクを用いた動物実験や in vitro 研究）が間接的に支持しているのみです。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | サル免疫不全ウイルス感染症 (simian immunodeficiency virus infection) |
| TxGNN 予測スコア | 0.9993 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 3 件／全 3 件） |
| 承認番号数 | 3 件（有効 3 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。既知の情報として、ラミブジンはヌクレオシド系逆転写酵素阻害薬であり、レトロウイルスの逆転写酵素を阻害します。SIV の逆転写酵素も阻害するため、マカクモデルで活性が確認されています。

SIV はヒト免疫不全ウイルス (HIV) の動物モデルとして用いられるウイルスです。逆転写酵素の構造が似ているため、機序的には適用可能と考えられます。ただし、SIV はヒトの疾患ではなく、このエビデンスはヒトへの再利用には間接的です。

なお、収載された文献は SIV を研究対象とする動物実験が中心です。ただし、ヒトの SIV 感染症に対する臨床的な治療を直接検討した研究ではありません。このためエビデンスレベルは L5 としています。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [12021341](https://pubmed.ncbi.nlm.nih.gov/12021341/) | 2002 | 動物実験 | Journal of Virology | ラミブジンまたはエムトリシタビン投与の新生仔マカクで M184V 変異が 5 週以内に出現。変異ウイルスは適応度が低下 |
| [19240457](https://pubmed.ncbi.nlm.nih.gov/19240457/) | 2009 | 動物実験 | AIDS | ジドブジン・ラミブジン・インジナビルによる曝露後予防の、マカクでの経腟 SIV 感染に対する効果を評価 |
| [16973590](https://pubmed.ncbi.nlm.nih.gov/16973590/) | 2006 | 動物実験 | Journal of Virology | SIV 感染マカクへの 4 剤併用療法でのウイルス量の急速な減少 |
| [12502828](https://pubmed.ncbi.nlm.nih.gov/12502828/) | 2003 | 動物実験 | Journal of Virology | ラミブジン併用下でもテノホビルにより SIV の M184V 変異の復帰が選択される |
| [15919889](https://pubmed.ncbi.nlm.nih.gov/15919889/) | 2005 | 動物実験 | Journal of Virology | エファビレンツ・ラミブジン・テノホビル併用が RT-SHIV 感染マカクのウイルス量を抑制 |
| [11689641](https://pubmed.ncbi.nlm.nih.gov/11689641/) | 2001 | 動物実験 | Journal of Virology | SHIV 感染マカクで、HAART によるウイルス血症の抑制後も骨髄造血障害が持続 |
| [31658118](https://pubmed.ncbi.nlm.nih.gov/31658118/) | 2020 | レビュー | Current Opinion in HIV and AIDS | イスラトラビルの HIV-1 の治療・予防における役割を論じたレビュー（ラミブジン自体は主題ではない） |
| [39509655](https://pubmed.ncbi.nlm.nih.gov/39509655/) | 2024 | レビュー | AIDS Reviews | コートジボワールの HIV-1・HIV-2 流行の実態。SIV は HIV の生物学的前駆体として言及 |
| [15040537](https://pubmed.ncbi.nlm.nih.gov/15040537/) | 2004 | 記載なし | Antiviral Therapy | HIV-2、SIV、SHIV の各種抗 HIV-1 薬への感受性を評価 |
| [12163615](https://pubmed.ncbi.nlm.nih.gov/12163615/) | 2002 | 記載なし | Journal of Virology | M184V 変異が弱毒化 SIV の復帰を遅らせる |

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 622699101 | ラバミコム配合錠「アメル」 | 錠「アメル」 | 記載なし |
| 671657001 | エプジコム配合錠（選） | 錠（選） | 記載なし |
| 621657001 | エプジコム配合錠 | 錠 | 記載なし |

上記はいずれも配合錠の承認です。ラミブジン単剤の承認状況を示すものではありません。

## 安全性に関する考慮事項

- **薬物相互作用**：DDI データベースで 100 件の相互作用が確認されています。主なものは、中等度のラクチトール、マンニトール、ナルトレキソン、オルリスタット、ソルビトールです。そのほか、メトホルミン、オメプラゾール、シメチジンなどが「重症度不明」として挙がっています。

それ以外の警告・禁忌については、添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
SIV は動物のウイルスであり、ヒトの疾患に対する再利用としては直接的な臨床試験がありません。予測疾患そのものを直接検討した臨床的な研究もなく、エビデンスはモデル予測と間接的な動物研究にとどまります。

**進める場合に必要なもの：**
- 日本の添付文書（警告・禁忌・適応症）の取得と確認
- 詳細な作用機序データ（DrugBank など）
- ヒトへの再利用としての意義の整理（SIV は動物モデルであり、ヒトでの対象疾患の再定義が必要）
- ラミブジン単剤の日本での承認・市販状況の確認
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**配合剤（この成分を含む）**：エプジコム配合錠、ラバミコム配合錠
<!-- brand-names:end -->

