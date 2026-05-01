---
layout: default
title: Azithromycin
parent: 僅模型預測 (L5)
nav_order: 22
evidence_level: L5
indication_count: 10
---

# Azithromycin
{: .fs-9 }

證據等級: **L5** | 預測適應症: **10** 個
{: .fs-6 .fw-300 }

---

## 目錄
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist">

## 藥師評估報告

</div>

# アジスロマイシン：細菌感染症 から 高アミラーゼ血症 (Hyperamylasemia) へ

## 一言要約

アジスロマイシン（Azithromycin, DB00207）はマクロライド系広域抗菌薬として世界的に広く使用されていますが、本評価の日本 PMDA クエリでは承認記録が検出されませんでした（データ欠損の可能性あり）。TxGNN モデルは **高アミラーゼ血症 (Hyperamylasemia)** を第 1 位の予測適応症（スコア 99.81%）として提示していますが、この適応症に対する臨床試験・文献エビデンスは存在せず、エビデンスレベルは L5 にとどまります。本レポートは TxGNN 上位 10 件の適応症を包括評価する複合レポート（multi）であり、最有望な研究候補は **先天性血液疾患（Congenital Hematological Disorder）** で、唯一 L3 エビデンスが確認されています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 細菌感染症（PMDA 承認データ未検出） |
| 予測新規適応症（第 1 位） | 高アミラーゼ血症 (Hyperamylasemia) |
| TxGNN 予測スコア | 99.81% |
| エビデンスレベル | L5 |
| 日本市販状況 | PMDA クエリ 0 件（要確認） |
| 承認番号数 | 0 件 |
| 推奨決定 | Hold |

---

## この予測が妥当である理由

本 Evidence Pack には詳細な作用機序（MOA）データが含まれていません。既知の薬理学的知見によれば、アジスロマイシンはマクロライド系抗菌薬として細菌 50S リボソームサブユニットへの結合によるタンパク合成阻害を主要機序とします。加えて、IL-8・TNF-α 産生の抑制、好中球遊走阻害、自噬フラックス（autophagy flux）の阻害を含む幅広い抗炎症・免疫調節作用を有することが in vitro・in vivo 研究で報告されており、抗菌以外の治療応用が注目されています。

高アミラーゼ血症は急性膵炎・慢性膵炎・唾液腺炎などに続発するアミラーゼ値上昇の状態です。感染性膵炎の文脈では、アジスロマイシンの抗菌・抗炎症特性が炎症を制御することでアミラーゼ値を間接的に正常化する可能性は概念的に示唆されます。しかし、この関連性を支持する前臨床モデル・臨床試験・文献エビデンスは現時点で一切存在せず、本予測は TxGNN 知識グラフの構造的特性に基づく純粋なモデル予測に留まります。

---

## 臨床試験エビデンス

現在、高アミラーゼ血症に関連する臨床試験の登録はありません。

---

## 文献エビデンス

現在、高アミラーゼ血症に関連する文献はありません。

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 全予測適応症サマリー（TxGNN 上位 10 件）

| 順位 | 疾患名 | TxGNN スコア | エビデンスレベル | 臨床試験 | 文献 | 推奨 |
|------|--------|:----------:|:--------------:|:------:|:--:|------|
| 1 | 高アミラーゼ血症 | 99.81% | L5 | 0 | 0 | Hold |
| 2 | 多クローン性高粘稠度症候群 | 99.81% | L5 | 0 | 0 | Hold |
| 3 | 先天性無アルブミン血症 | 99.79% | L5 | 0 | 0 | Hold |
| 4 | 点状表層角結膜炎 | 99.78% | L4 | 0 | 1 | Hold |
| 5 | 血液型不適合 | 99.70% | L5 | 0 | 0 | Hold |
| 6 | 前悪性血液疾患 | 99.64% | L5 | 0 | 0 | Hold |
| 7 | **単クローン性免疫グロブリン血症** | 99.61% | L4 | 0 | 7 | Research Question |
| 8 | 後天性末梢神経障害を伴う血液疾患 | 99.56% | L5 | 0 | 0 | Hold |
| 9 | **敗血症性ペスト** | 99.52% | L4 | 0 | 5 | Research Question |
| 10 | **先天性血液疾患** | 99.40% | **L3** | **4** | **2** | **Research Question** |

---

## 有望候補の詳細分析

### 候補 A：先天性血液疾患 (Congenital Hematological Disorder)｜順位 10・L3・最有望

アジスロマイシンの抗炎症・免疫調節作用と非典型病原体（Mycoplasma pneumoniae、Chlamydia pneumoniae）への広域抗菌活性が、鐮刀型細胞疾患（SCD）患者における急性胸部症候群（ACS）の発症予防に有効である可能性が示唆されています。ACS は SCD の入院第 2 位の原因かつ主要な死亡原因であり、未充足医療ニーズが高い領域です。ただし、ACS 予防を目的とした 2 件の Phase 1/2 試験はいずれも入組前に撤回されており、実際の臨床データは現時点で空白です。

**臨床試験エビデンス**

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|:------:|---------|
| [NCT02630394](https://clinicaltrials.gov/study/NCT02630394) | Phase 1 | 撤回 | 0 | SCD における ACS 予防目的の Azithromycin 予防投与パイロット試験。入組前撤回。 |
| [NCT02960503](https://clinicaltrials.gov/study/NCT02960503) | Phase 1/2 | 撤回 | 0 | SCD 成人の肺機能（FEV1）改善を目的とした大環内酯療法フィージビリティ試験。入組前撤回。 |
| [NCT04294641](https://clinicaltrials.gov/study/NCT04294641) | Phase 2 | 完了 | 10 | 新規診断 cGVHD への Ibrutinib 一次治療研究。主要介入薬は Ibrutinib であり、間接的関連にとどまる。 |
| [NCT04278404](https://clinicaltrials.gov/study/NCT04278404) | N/A | 募集中 | 5,000 | 小児への複数薬剤の PK/PD・安全性プラットフォーム研究。Azithromycin 薬動学情報を間接提供。 |

**文献エビデンス**

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|:--:|:----:|-----------|---------|
| [26408070](https://pubmed.ncbi.nlm.nih.gov/26408070/) | 2015 | Meta-analysis | Cochrane Database Syst Rev | 高リスク 12 歳以下小児における下気道感染症予防目的の抗菌薬投与に関するコクランレビュー。 |
| [34471086](https://pubmed.ncbi.nlm.nih.gov/34471086/) | 2021 | Case series | Am J Case Rep | SARS-CoV-2 陽性乳児の免疫性血小板減少症（ITP）症例報告。血液疾患背景のみ関連。 |

---

### 候補 B：単クローン性免疫グロブリン血症 (Monoclonal Gammopathy)｜順位 7・L4

In vitro 研究において、アジスロマイシン（AZM）を含むマクロライド系薬が自噬フラックスを阻害し、内質網ストレス（ER stress）介在性 CHOP 誘導により多発性骨髄腫（MM）細胞の bortezomib 感受性を増強することが報告されています（PMID 23546223）。さらに、骨髓腫患者に合併しやすい Legionella・Bartonella 感染症への治療使用例も記録されており、感染症合併管理の観点からも関連性があります。

**文献エビデンス**

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|:--:|:----:|-----------|---------|
| [23546223](https://pubmed.ncbi.nlm.nih.gov/23546223/) | 2013 | In vitro | Int J Oncol | AZM が MM 細胞の自噬フラックスを阻害し、bortezomib との併用で細胞毒性を有意に増強。 |
| [22825522](https://pubmed.ncbi.nlm.nih.gov/22825522/) | 2012 | Case series | Tumori | 骨髓腫患者の顎骨壊死（ONJ）に対してオゾン療法と Azithromycin 500 mg/day を併用投与した症例。 |
| [17609324](https://pubmed.ncbi.nlm.nih.gov/17609324/) | 2007 | Case series | J Clin Microbiol | サリドマイド投与中の骨髓腫患者に発症した Legionella micdadei 市中肺炎の症例報告。 |
| [33389938](https://pubmed.ncbi.nlm.nih.gov/33389938/) | 2020 | Case series | Turk J Ophthalmol | POEMS 症候群（MG 含む）患者における Bartonella henselae 神経網膜炎の症例報告。 |
| [32708858](https://pubmed.ncbi.nlm.nih.gov/32708858/) | 2020 | Case series | Medicina | クリオグロブリン血症 MPGN 患者の COVID-19 症例報告。透析・移植患者における Azithromycin 使用を言及。 |
| [15526516](https://pubmed.ncbi.nlm.nih.gov/15526516/) | 2003 | Case series | Rom J Intern Med | 骨髓腫寛解後に骨髓肉芽腫を合併した症例。トキソプラズマ感染が疑われ、治療に Azithromycin が使用。 |
| [18355359](https://pubmed.ncbi.nlm.nih.gov/18355359/) | 2008 | Review | Clin Exp Dermatol | 表皮下膿疱性皮膚症（Sneddon-Wilkinson disease）の 50 年間の知見レビュー。MG との関連を記述。 |

---

### 候補 C：敗血症性ペスト (Septicemic Plague)｜順位 9・L4

アジスロマイシンは高い組織・貪食細胞内蓄積性（血清濃度の 200〜2,000 倍）を持ち、理論上は Yersinia pestis への胞内殺菌が期待されます。しかし、最も直接的な in vitro データ（PMID 8540736）では Azithromycin は Y. pestis 全株に対して **活性が低い（poor activity）** と報告されており、この予測の機序的根拠は弱いと評価すべきです。ペスト動物モデルや臨床データは現時点で存在しません。

**文献エビデンス**

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|:--:|:----:|-----------|---------|
| [8540736](https://pubmed.ncbi.nlm.nih.gov/8540736/) | 1995 | In vitro | Antimicrob Agents Chemother | 78 株の Y. pestis に対し 14 剤の抗菌活性を比較。**Azithromycin は全株で poor activity**。Ceftriaxone・Ciprofloxacin が最活性。 |
| [12698575](https://pubmed.ncbi.nlm.nih.gov/12698575/) | 2002 | Animal | Antibiotiki i Khimioterapiya | 実験的ブルセラ症モデルで Azithromycin の高い有効性を報告。同属菌（グラム陰性）への間接的な参考知見。 |
| [19392866](https://pubmed.ncbi.nlm.nih.gov/19392866/) | 2009 | Meta-analysis | Aliment Pharmacol Ther | 旅行者下痢症の疫学と臨床特徴のシステマティックレビュー。Azithromycin の適応症の一つとして言及。 |
| [31778198](https://pubmed.ncbi.nlm.nih.gov/31778198/) | 2019 | Review | Mil Med | 米軍における薬剤耐性淋菌・性感染症に対する Azithromycin の役割をレビュー。 |

---

### 候補 D：点状表層角結膜炎 (Punctate Epithelial Keratoconjunctivitis)｜順位 4・L4

アジスロマイシンは微孢子虫（Microsporidia）、特に Encephalitozoon hellem に対する抗感染活性を有し、感染性角結膜炎の文脈では治療選択肢となりえます。ただし、点状表層角結膜炎の病因は感染以外にもドライアイ・毒性・アレルギーなど多岐にわたり、感染性病因が確認された症例に限定して適用が想定されます。

**文献エビデンス**

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|:--:|:----:|-----------|---------|
| [32826651](https://pubmed.ncbi.nlm.nih.gov/32826651/) | 2021 | Case series | Cornea | 免疫正常成人における鳥類由来 Encephalitozoon hellem 角結膜炎の症例報告。メタゲノミクス深部シーケンシングで診断確定。Azithromycin 使用が記録。 |

---

## 結論と次のステップ

**決定：Hold**

**理由：**
TxGNN 上位 10 件の適応症はすべて Hold または Research Question の段階にあり、最高スコアの高アミラーゼ血症（L5）を含む 6 件は機序的関連性・裏付けデータともに不足しています。最有望候補の先天性血液疾患（L3、SCD/ACS 予防）は概念的妥当性があり Phase 1/2 試験が設計されましたが、いずれも入組前に撤回されており、実際の臨床エビデンスは空白です。単クローン性免疫グロブリン血症に対しては in vitro での bortezomib 増感作用（PMID 23546223）という具体的な機序的根拠があるものの、現時点では前臨床ステージに留まります。

**進める場合に必要なもの：**

- **PMDA 承認データの再取得**：クエリ 0 件はデータ欠損の可能性が高い（アジスロマイシンは世界 100 カ国超で承認済みの必須医薬品）。PMDA 直接照会または医薬品データベース（KEGG DRUG, 添付文書情報センター）からの再取得が必要
- **MOA・安全性データの補完**：DrugBank API から作用機序・薬物標的・分類情報を取得し、機序的適合性分析を再実施。PMDA 仿単から主要警告・禁忌・薬物相互作用を収集
- **SCD/ACS 領域の撤回理由調査**：NCT02630394・NCT02960503 の撤回理由（資金不足か安全性懸念か）を確認し、継続研究の可能性を評価
- **骨髓腫併用療法の前臨床深掘り**：PMID 23546223 の知見に基づき、AZM + bortezomib 併用の MM 動物モデルデータおよび後続臨床試験の有無を探索
- **ペスト適応の機序再評価**：PMID 8540736 は Azithromycin の Y. pestis への活性が低いと明示しており、この適応の Research Question ステータスは機序的根拠が弱く、エビデンスレベルの下方修正（L4→L5）を推奨
---

