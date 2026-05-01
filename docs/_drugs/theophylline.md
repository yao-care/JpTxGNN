---
layout: default
title: Theophylline
parent: 僅模型預測 (L5)
nav_order: 138
evidence_level: L5
indication_count: 10
---

# Theophylline
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

Using `txgnn-pipeline` skill to understand the report generation context for TxGNN drug repurposing outputs. The skill confirms the standard TxGNN pipeline workflow. Now generating the report from the Evidence Pack.

---

# テオフィリン：気管支喘息・COPD から 血栓性疾患 へ

## 一言要約

テオフィリンは 80 年以上にわたり気管支拡張薬として気管支喘息や COPD の治療に広く使用されてきた古典的薬物ですが、現在 PMDA データベースには登録が確認されていません。
TxGNN モデルは**血栓性疾患 (Thrombotic Disease)** への有効性を予測しており、現在 **0 件の臨床試験**と **19 編の文献**が存在しますが、その大半は間接的・方法論的研究に留まっています。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 気管支喘息・COPD（PMDA 未登録） |
| 予測新規適応症 | 血栓性疾患 (Thrombotic Disease) |
| TxGNN 予測スコア | 99.62% |
| エビデンスレベル | L4 |
| 日本市販状況 | ✗ 未上市（PMDA 未登録） |
| 承認番号数 | 0 件 |
| 推奨決定 | Hold |

## この予測が妥当である理由

テオフィリンは非選択的ホスホジエステラーゼ（PDE）阻害薬であり、特に PDE3 と PDE4 を阻害することで細胞内 cAMP 濃度を上昇させます。また、腺苷 A1/A2A 受容体のアンタゴニストとしても機能します。なお、本 Evidence Pack には詳細な MOA データは収録されておらず（Data Gap）、DrugBank API からの補充が推奨されます。

血小板内の cAMP 上昇は血小板の活化・凝集を抑制することが広く知られており、PDE3 は血小板において cAMP の主要な分解酵素です。テオフィリンによる PDE3 阻害が血小板凝集を間接的に抑制し、血栓形成を防ぐという機序的仮説は理論的に成立します。事実、血小板第4因子（PF4）の精密 in vivo 測定では採血時の血小板活化防止のためにテオフィリンを含む抗凝固カクテルが標準的に使用されており（PMID: [749930](https://pubmed.ncbi.nlm.nih.gov/749930/)、[29220362](https://pubmed.ncbi.nlm.nih.gov/29220362/)）、これはその薬理作用の副次的な活用例といえます。

ただし、現在確認された 19 編の文献は、血栓性バイオマーカーの測定方法論研究、血小板活化機序の基礎研究、あるいはテオフィリンとは無関係の薬物を主体とした研究が大半を占めています。テオフィリンを直接の介入薬として血栓性疾患に用いた臨床試験は確認されておらず、エビデンスレベルは機序・背景研究（L4）に留まります。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [749930](https://pubmed.ncbi.nlm.nih.gov/749930/) | 1978 | Case series | Br J Haematology | 血小板第4因子 RIA 測定法の確立；採血時の血小板活化防止に EDTA・テオフィリン・PGE1 複合抗凝固剤が必要と報告 |
| [6241135](https://pubmed.ncbi.nlm.nih.gov/6241135/) | 1984 | Cohort | Cor et vasa | 心筋梗塞・血栓静脈炎患者でテオフィリン耐性 T ヘルパー細胞（E[Thr] / T[M]）が有意に増加；免疫-血栓連関を示唆 |
| [29220362](https://pubmed.ncbi.nlm.nih.gov/29220362/) | 2017 | Cohort | PLoS One | 血漿中血小板由来分子の正確な定量にはテオフィリン配合抗凝固カクテルが不可欠と実証 |
| [8981060](https://pubmed.ncbi.nlm.nih.gov/8981060/) | 1996 | Cohort | General Pharmacology | PDE3 阻害薬ミルリノンとアデノシンの cAMP 経路による相乗的血小板凝集抑制；テオフィリンとの機序的類似性を示す背景研究 |
| [32824700](https://pubmed.ncbi.nlm.nih.gov/32824700/) | 2020 | Cohort | Cells | 抗凝固処理・検体保存条件が血中 microRNA 定量に影響；テオフィリン含有抗凝固剤の有用性を確認 |
| [25856065](https://pubmed.ncbi.nlm.nih.gov/25856065/) | 2015 | Cohort | Platelets | 血栓性疾患リスク患者モニタリング用の可溶性 CLEC-2 測定法を確立；既存の PF4 マーカーより安定性が高い可能性 |
| [29956444](https://pubmed.ncbi.nlm.nih.gov/29956444/) | 2018 | In vitro | J Thromb Haemost | 内皮細胞 Weibel-Palade 体からの止血・炎症関連分子の選択的放出機序；アゴニスト依存的な分泌制御の解明 |
| [21719422](https://pubmed.ncbi.nlm.nih.gov/21719422/) | 2011 | Cohort | Rheumatology | Behçet 病患者の血小板・好中球活化；若年男性で重症度が高く疾患活動性と血小板活化が連関 |
| [6771102](https://pubmed.ncbi.nlm.nih.gov/6771102/) | 1980 | Review | CRC Crit Rev Biochem | トロンボキサン A2 と PGI2 の相反作用；cAMP を介した血小板凝集抑制機序の基礎的解説 |
| [29254574](https://pubmed.ncbi.nlm.nih.gov/29254574/) | 2018 | In vitro | Analytica Chimica Acta | テオフィリン検出用 RNA アプタマー・金ナノ粒子電気化学バイオセンサーの開発；狭い治療域での血中濃度管理の重要性を強調 |

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
テオフィリンの PDE3 阻害による血小板内 cAMP 上昇という理論的機序は存在するものの、血栓性疾患を直接対象とした臨床試験は皆無であり、現行文献は方法論・背景研究に留まります（L4）。

**進める場合に必要なもの：**
- テオフィリンの血小板凝集抑制効果を直接評価した in vitro / 前臨床研究の系統的実施
- 治療域（5–15 µg/mL）での血栓抑制効果と出血リスクを評価するパイロット臨床試験の設計
- 詳細な作用機序データ（MOA）の補充（DrugBank API 照会）
- 安全性情報（警語・禁忌・DDI）の取得（PMDA 仿単 PDF 解析）
---

