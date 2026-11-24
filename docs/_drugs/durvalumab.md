---
layout: default
title: Durvalumab
parent: モデル予測のみ
nav_order: 124
evidence_level: L5
indication_count: 6
monitor_inn: "durvalumab"
predicted_indications: ["uterine ligament adenocarcinoma", "endocervical carcinoma", "adenoid cystic carcinoma of the cervix uteri", "uterine ligament serous adenocarcinoma", "signet ring cell variant cervical mucinous adenocarcinoma", "intestinal variant cervical mucinous adenocarcinoma"]
last_modified_at: 2026-11-24
description: "Durvalumab：予測新適応症は子宮靭帯腺癌 (uterine ligament adenocarcinoma)（エビデンスレベル L5）。薬価基準の品目：2 件（現在収載 2 件）"
---

# Durvalumab
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

## デュルバルマブ：PD-L1 阻害抗体 → 子宮靭帯腺癌 (uterine ligament adenocarcinoma)
{: .text-alpha }

## 一言要約

デュルバルマブは PD-L1 を阻害する抗体医薬で、日本では「イミフィンジ」として市販されています。
TxGNN モデルは**子宮靭帯腺癌 (uterine ligament adenocarcinoma)** に有効である可能性を予測していますが、この疾患を直接検討した臨床試験・文献は、今回まとめたデータには **0 件**です。現時点ではモデル予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 子宮靭帯腺癌 (uterine ligament adenocarcinoma) |
| TxGNN 予測スコア | 0.9992 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 2 件／全 2 件） |
| 承認番号数 | 2 件（有効 2 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

デュルバルマブは PD-L1 を遮断し、抑制されていた T 細胞の抗腫瘍活性を回復させる抗体です。米国 FDA が承認した Durvalumab の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「プログラム細胞死リガンド1（PD-L1）の発現は炎症シグナル（例：IFN-gamma）により誘導されることがあり、PD-L1は腫瘍微小環境において腫瘍細胞及び腫瘍関連免疫細胞の両方に発現しうる。PD-L1はPD-1及びCD80（B7.1）との相互作用を介してT細胞の機能及び活性化を阻害する。[…] デュルバルマブは、PD-L1に結合し、PD-L1とPD-1及びCD80（B7.1）との相互作用を阻害するヒト免疫グロブリンG1カッパ（IgG1κ）モノクローナル抗体である。」英語原文："Expression of programmed cell death ligand-1 (PD-L1) can be induced by inflammatory signals (e.g., IFN-gamma) and can be expressed on both tumor cells and tumor-associated immune cells in the tumor microenvironment. PD-L1 blocks T-cell function and activation through interaction with PD-1 and CD80 (B7.1). […] Durvalumab is a human immunoglobulin G1 kappa (IgG1κ) monoclonal antibody that binds to PD-L1 and blocks the interaction of PD-L1 with PD-1 and CD80 (B7.1)."（[DailyMed: Imfinzi (durvalumab) prescribing information, AstraZeneca Pharmaceuticals LP](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=8baba4ea-2855-42fa-9bd9-5a7548d4cec3)、版 2026-08-31、参照日 2026-11-19）。ただし、PD-L1 阻害は腫瘍免疫を介した広範な固形がんに共通する考え方です。

子宮靭帯腺癌は稀な婦人科腺癌で、デュルバルマブとの関連は TxGNN の予測のみに基づきます。この疾患に特化した PD-L1 発現の根拠や臨床データは、今回まとめたデータには含まれていません。そのため、機序的な適用可能性は仮説の段階です。

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 622633201 | イミフィンジ点滴静注１２０ｍｇ ２．４ｍＬ | 有効 |
| 622633301 | イミフィンジ点滴静注５００ｍｇ １０ｍＬ | 有効 |

<!-- licenses:end -->

## 細胞毒性

デュルバルマブは免疫チェックポイント阻害薬（免疫療法）に分類され、従来型の細胞毒性薬ではありません。

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 免疫療法（抗 PD-L1 抗体） |
| 骨髄抑制リスク | 添付文書の警告および注意事項を参照してください |
| 催吐性分類 | 添付文書の警告および注意事項を参照してください |
| モニタリング項目 | 添付文書の警告および注意事項を参照してください |
| 取り扱い防護 | 添付文書の警告および注意事項を参照してください |

## 安全性に関する考慮事項

- **薬物相互作用**：今回の検索で 81 件の相互作用が確認されました。主なものは次のとおりです。
  - **重大 (Major)**：アダリムマブ
  - **中等度 (Moderate)**：ヒドロコルチゾン、トリアムシノロン、デキサメタゾン、ベタメタゾン、ブデソニド、プレドニゾロン、プレドニゾン、メチルプレドニゾロン、デフラザコート（いずれも副腎皮質ステロイド）、ロフルミラスト、アレムツズマブ、アナキンラ、破傷風トキソイド
  - **軽度 (Minor)**：各種亜鉛製剤（酢酸亜鉛、グルコン酸亜鉛、硫酸亜鉛、塩化亜鉛）

警告・禁忌の詳細は添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 子宮靭帯腺癌を直接検討した臨床試験・文献がなく、根拠は TxGNN の予測のみ（L5）です。
- 添付文書の警告・禁忌情報も未取得で、安全性評価に進めません。

**進める場合に必要なもの：**
- 子宮靭帯腺癌における PD-L1 発現などの前臨床・病理学的データの収集
- この疾患を対象とした症例報告・臨床試験の調査
- PMDA 添付文書の警告・禁忌の取得と解析
- DrugBank からの作用機序データの補完

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Imfinzi (durvalumab) prescribing information, AstraZeneca Pharmaceuticals LP](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=8baba4ea-2855-42fa-9bd9-5a7548d4cec3) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：イミフィンジ

**販売名（規格別）**：イミフィンジ点滴静注120mg 2.4mL、イミフィンジ点滴静注500mg 10mL
<!-- brand-names:end -->

