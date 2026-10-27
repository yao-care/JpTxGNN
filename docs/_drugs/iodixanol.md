---
noindex: true
sitemap: false
layout: default
title: Iodixanol
parent: モデル予測のみ (L5)
nav_order: 89
evidence_level: L5
indication_count: 1
last_modified_at: 2026-09-17
description: "Iodixanol：予測新適応症は変形性関節症 (osteoarthritis)（エビデンスレベル L5）。既存適応症：X線造影剤：心血管、脳血管、末梢動脈造影等"
---

# Iodixanol
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **1** 件
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

## Iodixanol：X線造影剤から変形性関節症へ
{: .text-alpha }

## 一言まとめ

Iodixanol（イオジキサノール）は等浸透圧性のヨード造影剤で、心血管、脳血管および尿路の造影に用いられます。TxGNN モデルは、本剤が**変形性関節症 (osteoarthritis)** に関連する可能性があると予測しており、現在その関連機序を検討した**文献が7件**ありますが、臨床試験による裏付けはありません。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載 |
| 予測新適応症 | 変形性関節症 (osteoarthritis) |
| TxGNN 予測スコア | 99.07% |
| エビデンスレベル | L5 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Hold |

## この予測が妥当な理由

Iodixanol は非イオン性の等浸透圧性ヨード造影剤で、主に画像検査に用いられます。現時点では、変形性関節症に対する治療的可能性を説明する直接的な薬理学的機序のデータはありません。

しかし、文献上のエビデンスを見ると、iodixanol は造影剤として関節軟骨の CT 造影研究に用いられています。複数の研究で、造影増強コンピュータ断層撮影（CECT）技術と iodixanol を組み合わせ、軟骨の構造や組成の変化を評価しており、これらの変化は早期の変形性関節症と関連しています。この用途は主に診断目的であり、治療目的ではありません。

TxGNN の予測は、薬剤と疾患が知識グラフ上で共起する関係（文献中で同時に言及されているなど）を反映している可能性があり、直接的な治療効果を示すものではありません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

| PMID | 年 | 種類 | 雑誌 | 主な知見 |
|------|-----|------|------|---------|
| [40155520](https://pubmed.ncbi.nlm.nih.gov/40155520/) | 2025 | Journal Article | Ann Biomed Eng | フォトンカウンティングCTと二重造影剤を用いた関節軟骨の健常性評価 |
| [28063646](https://pubmed.ncbi.nlm.nih.gov/28063646/) | 2017 | Journal Article | J Biomech | iodixanol を用いた骨軟骨界面における溶質輸送の検討 |
| [30145230](https://pubmed.ncbi.nlm.nih.gov/30145230/) | 2018 | Journal Article | Osteoarthr Cartil | ウマの下顎顆軟骨の加齢が圧縮剛性に影響しないことを検討 |
| [39012563](https://pubmed.ncbi.nlm.nih.gov/39012563/) | 2024 | Journal Article | Ann Biomed Eng | ナノ粒子拡散イメージングによる軟骨機能の解明 |
| [27793406](https://pubmed.ncbi.nlm.nih.gov/27793406/) | 2016 | Journal Article | J Biomech | 骨軟骨界面における中性溶質輸送の有限要素解析 |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

**薬物相互作用**：

主要な相互作用（Major）：
- Metformin：乳酸アシドーシスのリスクを増加させる可能性
- Amphotericin B：腎毒性を増加させる可能性
- Vancomycin、Aminoglycosides（Amikacin, Gentamicin, Kanamycin）：腎毒性を増加させる可能性
- Cyclosporine、Tacrolimus：腎毒性を増加させる可能性
- NSAIDs（Ketorolac, Ibuprofen, Naproxen, Celecoxib）：腎毒性を増加させる可能性
- Cisplatin：腎毒性を増加させる可能性

中等度の相互作用（Moderate）：
- Beta-blockers（Metoprolol, Atenolol など）
- 利尿薬（Furosemide, Hydrochlorothiazide など）

## 結論と次のステップ

**判断：Hold**

**理由：**
文献における iodixanol と変形性関節症の関連は主に診断目的の応用（軟骨造影における造影剤としての使用）に由来し、治療効果によるものではありません。機序面の裏付けや臨床試験のエビデンスが乏しいことから、この予測は知識グラフ上の偽相関である可能性があります。

**推進に必要な事項：**
- 治療的可能性を裏付ける明確な薬理機序の研究
- iodixanol の軟骨に対する直接的効果についての in vitro／in vivo 実験による検証
- 現時点では、この適応症についてこれ以上の探索は推奨されません


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
