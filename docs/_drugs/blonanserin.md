---
layout: default
title: Blonanserin
parent: モデル予測のみ
nav_order: 43
evidence_level: L5
indication_count: 9
---

# Blonanserin
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **9** 件
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

# ブロナンセリン：抗精神病薬から遺伝性網膜ジストロフィーへ

## 一言要約

ブロナンセリンはドパミン D2/D3 受容体とセロトニン 5-HT2A 受容体を拮抗する抗精神病薬で、日本ではテープ剤が市販されています。
TxGNN モデルは**網膜ジストロフィー（眼外異常を伴う場合を含む）(retinal dystrophy with or without extraocular anomalies)** に有効である可能性を予測しています。
ただし、**臨床試験は 0 件**です。収集した 15 編の文献はいずれも眼窩・外眼筋・先天性眼疾患の一般的な総説や症例報告で、ブロナンセリンには一切触れていません。根拠はモデルのスコアだけです。

## クイック概要

| 項目 | 内容 |
|------|------|
| 予測新規適応症 | 網膜ジストロフィー（眼外異常を伴う場合を含む） (retinal dystrophy with or without extraocular anomalies) |
| TxGNN 予測スコア | 99.98% |
| エビデンスレベル | L5 |
| 日本市販状況 | ✓ 市販中 |
| 承認番号数 | 3 件 |
| 推奨決定 | Hold |

## この予測が妥当である理由

現時点では、この予測の妥当性を支持する材料はほとんどありません。

詳細な作用機序データは取得できていません。既知の情報では、ブロナンセリンは D2/D3 受容体と 5-HT2A 受容体の拮抗薬です。遺伝性の網膜変性との間に、確立した機序的なつながりは見当たりません。

スコアは非常に高い（99.98%）ものの、TxGNN が知識グラフ上の関連性から算出した値にすぎません。実際の研究で裏づけられたものではありません。網膜ジストロフィーは主に遺伝子変異による疾患で、受容体拮抗薬が病態を改善する根拠は示されていません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

収集された文献のうち関連性が比較的高いものを示します。いずれも関連性の判定は未実施（pending）で、ブロナンセリンへの言及はありません。RCT はなく、総説を優先し、次に症例報告・症例集積を載せています。

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [20127583](https://pubmed.ncbi.nlm.nih.gov/20127583/) | 2010 | Review | Seminars in Neurology | 複視の系統的な問診・診察法と鑑別診断 |
| [9416661](https://pubmed.ncbi.nlm.nih.gov/9416661/) | 1997 | Review | Seminars in Ultrasound, CT, and MR | 眼窩感染症の原因（副鼻腔炎が最多）と臨床所見 |
| [22241537](https://pubmed.ncbi.nlm.nih.gov/22241537/) | 2012 | Review | Klinische Monatsblätter für Augenheilkunde | 先天性眼瞼下垂の分類と診察の要点 |
| [38249493](https://pubmed.ncbi.nlm.nih.gov/38249493/) | 2023 | Review | Taiwan Journal of Ophthalmology | 水晶体の形状に関する先天異常 |
| [38321238](https://pubmed.ncbi.nlm.nih.gov/38321238/) | 2024 | Review | Pediatric Radiology | 小児の眼球病変の鑑別診断と画像所見 |
| [10192514](https://pubmed.ncbi.nlm.nih.gov/10192514/) | 1999 | Review | Progress in Retinal and Eye Research | 外眼筋の固有受容器と固有感覚の役割 |
| [30196776](https://pubmed.ncbi.nlm.nih.gov/30196776/) | 2018 | Review | Journal of Binocular Vision and Ocular Motility | 先天性脳神経脱神経疾患（CCDD）と眼球運動障害 |
| [109006](https://pubmed.ncbi.nlm.nih.gov/109006/) | 1979 | Case report | American Journal of Ophthalmology | 片側性の潜伏眼球の 2 症例 |
| [19826317](https://pubmed.ncbi.nlm.nih.gov/19826317/) | 2009 | Case series | Optometry and Vision Science | 先天性外眼筋線維症にみられる共同性外斜視の症例 |
| [30747268](https://pubmed.ncbi.nlm.nih.gov/30747268/) | 2019 | Case series | Neuroradiology | 眼筋麻痺の神経放射線学的・臨床的特徴 |

## 日本市販情報

3 件とも経皮吸収型のテープ剤です。承認適応症のテキストは取得できていません。

| 承認番号 | 商品名 | 剤形 |
|---------|------|------|
| 622687801 | ロナセンテープ20mg | テープ20mg |
| 622687901 | ロナセンテープ30mg | テープ30mg |
| 622688001 | ロナセンテープ40mg | テープ40mg |

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
臨床試験がなく、文献にもブロナンセリンと網膜疾患を結びつけるものがありません。機序的な根拠も見当たらないため、モデル予測のみ（L5）の段階です。現時点で開発を進める根拠はありません。順位 2〜9 の他の予測（眼疾患や先天性疾患など）も同じく L5 で、同様に保留が妥当です。

**進める場合に必要なもの：**
- ブロナンセリンの詳細な作用機序データ（MOA）の取得
- 網膜における D2/D3・5-HT2A 受容体の関与を示す前臨床研究の有無の調査
- ブロナンセリンと網膜ジストロフィーを直接扱う文献の再検索
- PMDA の添付文書に基づく警告・禁忌の確認（安全性スクリーニングの前提）
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

