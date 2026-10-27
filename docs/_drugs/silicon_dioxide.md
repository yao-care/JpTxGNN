---
layout: default
title: Silicon Dioxide
parent: 中エビデンス (L3-L4)
nav_order: 155
evidence_level: L4
indication_count: 1
last_modified_at: 2026-09-17
description: "Silicon Dioxide：予測新適応症はActive Peptic Ulcer Disease（活動性消化性潰瘍）（エビデンスレベル L4）。既存適応症：日本の承認適応症は本サイトのデータに未収載、peptic esophagitis、dyspepsia）"
---

# Silicon Dioxide
{: .fs-9 }

エビデンスレベル: **L4** | 予測適応症: **1** 件
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

## Silicon Dioxide：賦形剤から消化性潰瘍の探索へ
{: .text-alpha }

## 一言まとめ

Silicon Dioxide（二酸化ケイ素）は、主に医薬品の賦形剤および制酸剤として使用されています。
TxGNN モデルは、本剤が**活動性消化性潰瘍 (Active Peptic Ulcer Disease)** に有効である可能性を予測しており、
現在 **12 件の文献**がこの方向性を支持していますが、直接的な臨床試験による裏付けはありません。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：peptic ulcer disease、gastroesophageal reflux disease、esophagitis (disease)、peptic esophagitis、dyspepsia） |
| 予測新適応症 | Active Peptic Ulcer Disease（活動性消化性潰瘍） |
| TxGNN 予測スコア | 99.93% |
| エビデンスレベル | L4 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | さらなる探索が可能 |

## この予測が妥当な理由

Silicon Dioxide は医薬の分野では主に賦形剤として使用されますが、そのケイ酸塩化合物は消化管保護に用いられてきました。
文献によると、ケイ酸系化合物は保護的なバリアを形成し、粘膜保護機能を高めうるとされています。

**TxGNN が予測した新適応症：**

| 順位 | 予測適応症 | 予測スコア | TxGNN 順位 | 文献数 |
|------|-----------|---------|-----------|--------|
| 1 | Active Peptic Ulcer Disease（活動性消化性潰瘍） | 99.93% | 1,971 | 12 件 |
| 2 | Gastrojejunal Ulcer（胃空腸吻合部潰瘍） | 99.92% | 2,330 | 15 件 |

活動性消化性潰瘍という予測には、合理的な作用機序上の根拠があります：
- ケイ酸系制酸剤は胃酸を中和し、粘膜を保護しうる
- 中空メソポーラスシリカナノ粒子は、胃潰瘍の薬物送達システムとして研究されている

## 臨床試験エビデンス

現在、Silicon Dioxide による消化性潰瘍の直接治療を対象とした臨床試験の登録はありません。

## 文献エビデンス

| PMID | 年 | 種類 | 雑誌 | 主な知見 |
|------|-----|------|------|---------|
| [2986275](https://pubmed.ncbi.nlm.nih.gov/2986275/) | 1985 | RCT | Scand J Gastroenterol | 逆流性食道炎におけるスクラルファートとアルギン酸/制酸剤の比較研究 |
| [6095236](https://pubmed.ncbi.nlm.nih.gov/6095236/) | 1983 | Review | Polimery w medycynie | オルトケイ酸およびその誘導体の生物活性と抗潰瘍特性 |
| [2877526](https://pubmed.ncbi.nlm.nih.gov/2877526/) | 1986 | Review | Z Gastroenterol | 制酸剤療法を含む、胃食道逆流の治療戦略 |
| [7604597](https://pubmed.ncbi.nlm.nih.gov/7604597/) | 1994 | Clinical | Likars'ka sprava | Smecta（ケイ酸アルミニウム含有）による消化管疾患の臨床効果 |
| [38767185](https://pubmed.ncbi.nlm.nih.gov/38767185/) | 2024 | Research | Adv Healthc Mater | 胃内滞留型いかだ形成システムと中空メソポーラスシリカナノ粒子を組み合わせた胃潰瘍治療 |
| [39541155](https://pubmed.ncbi.nlm.nih.gov/39541155/) | 2024 | Research | Nano Lett | 抗生物質で増強した化学動力学療法によるヘリコバクター・ピロリ感染症の治療 |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **一般的な安全性**：
  - 賦形剤として使用する場合の安全性は良好
  - ケイ酸系制酸剤を経口で長期使用する場合は、電解質バランスのモニタリングが必要

- **薬物相互作用**：
  - 既知の重大な薬物相互作用なし

安全性情報は添付文書をご参照ください。

## 結論と次のステップ

**判断：さらなる探索が可能**

**理由：**
TxGNN が予測した消化性潰瘍の適応症は、Silicon Dioxide 関連化合物の制酸作用および粘膜保護作用の機序と整合しています。
文献では、ケイ酸系化合物が消化管保護の分野で応用の可能性を持つことが示されており、さらに最新の研究では、中空メソポーラスシリカナノ粒子が
胃潰瘍治療薬の送達担体になりうることが示されています。

**推進に必要な事項：**
- Silicon Dioxide とケイ酸塩含有制酸剤との作用の違いを明らかにする
- 胃潰瘍に対する保護作用についての前臨床研究を行う
- 薬物送達担体としてのシリカナノ粒子の臨床的実現可能性を探る
- 長期経口投与時の安全性を評価する


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
