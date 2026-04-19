---
layout: default
title: Human Immunoglobulin G
parent: 中エビデンス (L3-L4)
nav_order: 79
evidence_level: L3
indication_count: 1
---

# Human Immunoglobulin G
{: .fs-9 }

エビデンスレベル: **L3** | 予測適応症: **1** 件
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

# Human Immunoglobulin G：從免疫調節到糖尿病視網膜病變

## 一言まとめ

Human immunoglobulin G（IVIG）原本用於免疫不全症、ITP 及川崎氏症等免疫調節治療。
TxGNN 模型預測它可能對**糖尿病視網膜病變 (diabetic retinopathy)** 有效，
目前有 **3 個臨床試驗**和 **20 篇文獻**涉及相關研究。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 原發性免疫不全症、ITP、川崎氏症、GBS |
| 予測新適応症 | 糖尿病視網膜病變 (diabetic retinopathy) |
| TxGNN 予測スコア | 99.63% |
| エビデンスレベル | L3 |
| 日本上市 | 有效許可證 |
| 承認数 | 2 張 |
| 推奨判断 | Explore |

## この予測が妥当な理由

Human immunoglobulin G 是一種免疫調節生物製劑，透過多種機轉發揮作用，
包括中和自體抗體、調節補體系統、影響 Fc 受體功能等。

**預測合理性分析：**
- 糖尿病視網膜病變涉及慢性發炎和免疫失調
- 研究顯示 DR 患者血清中 IgG 醣化模式異常，提示 IgG 在疾病中的角色
- 自體抗體可能參與視網膜周細胞（pericyte）的損傷機轉
- 補體活化產物（C3a、C5a）在 DR 患者中升高

**機轉關聯：**
- IgG 醣化改變與 DR 嚴重程度相關（PMID: 33491329, 40204274）
- 視網膜周細胞反應性自體抗體透過補體介導損傷（PMID: 26839120）
- 玻璃體液中 IgG 水平在增殖性 DR 中升高（PMID: 32714992）

## 臨床試験エビデンス

| 試驗編號 | 階段 | 狀態 | 人數 | 主要發現 |
|---------|------|------|------|---------|
| [NCT01148225](https://clinicaltrials.gov/study/NCT01148225) | Phase 3 | COMPLETED | 424 | Adalimumab 用於非感染性葡萄膜炎（含 DR 相關併發症） |
| [NCT02924987](https://clinicaltrials.gov/study/NCT02924987) | Phase 4 | UNKNOWN | 40 | 抗 VEGF 治療糖尿病黃斑部水腫 |
| [NCT02443155](https://clinicaltrials.gov/study/NCT02443155) | Phase 2 | COMPLETED | 308 | 研究保護 beta 細胞功能的免疫調節治療 |

*註：上述試驗並非直接測試 IVIG 用於 DR，而是涉及免疫球蛋白相關藥物或糖尿病併發症*

## 文献エビデンス

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [40204274](https://pubmed.ncbi.nlm.nih.gov/40204274/) | 2025 | 研究 | Mol Cell Proteomics | 血清 IgG Fc 醣化可作為 DR 診斷生物標記 |
| [33491329](https://pubmed.ncbi.nlm.nih.gov/33491329/) | 2021 | 研究 | J Diabetes | IgG N-醣化模式與 DR 相關 |
| [26839120](https://pubmed.ncbi.nlm.nih.gov/26839120/) | 2016 | 研究 | Sci Rep | DR 患者存在視網膜周細胞反應性自體抗體 |
| [32714992](https://pubmed.ncbi.nlm.nih.gov/32714992/) | 2020 | 研究 | J Diabetes Res | 第二型糖尿病患者玻璃體液中 B 細胞抗體分析 |
| [33625683](https://pubmed.ncbi.nlm.nih.gov/33625683/) | 2021 | 研究 | Immunol Res | PDR 患者濾泡輔助 T 細胞失調，IgG 水平升高 |

## 日本上市情報

| 承認番号 | 品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 衛署菌疫輸字第000841號 | "國血製劑益康"人類免疫球蛋白靜脈注射劑 | 注射劑 | 原發性免疫不全症、ITP、骨髓移植、川崎氏症、GBS |

## 安全性に関する考慮事項

- **藥物交互作用**：未在 DDI 資料庫中找到重大交互作用
- **注意事項**：
  - 可能引起輸注反應（發燒、寒顫、頭痛）
  - 高劑量 IVIG 有血栓栓塞風險
  - 腎功能不全患者需謹慎使用
- **特殊族群**：糖尿病患者常合併腎病變，使用時需監測腎功能

安全性情報は添付文書をご参照ください。

## 結論と次のステップ

**判断：Explore**

**理由：**
- 多篇文獻支持 IgG 在糖尿病視網膜病變病理機轉中的角色
- 免疫調節在 DR 治療中是尚未被充分探索的方向
- 但目前無直接臨床試驗評估 IVIG 用於 DR 的療效
- IVIG 成本高昂，需進行成本效益評估

**推進に必要な事項：**
- 基礎研究確認 IVIG 對視網膜周細胞保護作用的機轉
- 小規模臨床試驗評估 IVIG 在 DR 患者中的安全性和初步療效
- 與現有抗 VEGF 治療進行比較或聯合治療研究
- 成本效益分析


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
