---
layout: default
title: Oteracil
parent: 高證據等級 (L1-L2)
nav_order: 117
evidence_level: L2
indication_count: 1
---

# Oteracil
{: .fs-9 }

證據等級: **L2** | 預測適應症: **1** 個
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

# Oteracil：從胃癌到大腸腫瘤

## 一句話總結

Oteracil 是 S-1 複方的成分之一，原本用於胃癌治療。
TxGNN 模型預測它可能對**大腸腫瘤 (Colonic Neoplasm)** 有效，
目前有 **7 個臨床試驗**和 **10 篇文獻**支持這個方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 胃癌用藥。 |
| 預測新適應症 | 大腸腫瘤 (Colonic Neoplasm) |
| TxGNN 預測分數 | 99.99% |
| 證據等級 | L2 |
| 台灣上市 | ✓ 已上市 |
| 許可證數 | 8 張 |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

目前缺乏詳細的作用機轉資料。根據已知資訊，Oteracil 是 S-1 複方的一部分，其成分在胃癌中的療效已被證實，機轉上可能適用於大腸腫瘤。S-1 包含的 tegafur 是 5-FU 的前驅藥，已知能夠抑制快速分裂的癌細胞中的 DNA 合成，這在大腸腫瘤中可能有效。

## 臨床試驗證據

| 試驗編號 | 階段 | 狀態 | 人數 | 主要發現 |
|---------|------|------|------|---------|
| [NCT00524706](https://clinicaltrials.gov/study/NCT00524706) | Phase 1/2 | 未知 | 42 | S-1 與 Oxaliplatin 組合治療顯示出對未治療之轉移性大腸癌的良好活性和可接受的毒性。 |
| [NCT02618356](https://clinicaltrials.gov/study/NCT02618356) | Phase 2 | 未知 | 82 | 評估轉移性大腸癌患者的中位疾病無進展生存期 (mPFS)。 |
| [NCT00974389](https://clinicaltrials.gov/study/NCT00974389) | Phase 2 | 未知 | 40 | S-1 與 Bevacizumab 組合用於不可切除或復發性大腸癌。 |
| [NCT01918852](https://clinicaltrials.gov/study/NCT01918852) | Phase 3 | 完成 | 161 | 比較 S-1 與 Capecitabine 在轉移性大腸癌患者中的效果。 |
| [NCT03448549](https://clinicaltrials.gov/study/NCT03448549) | Phase 3 | 未知 | 1191 | 比較 S-1 與 Capecitabine 作為 III 期大腸癌患者的輔助化療。 |
| [NCT06255379](https://clinicaltrials.gov/study/NCT06255379) | Phase 2 | 未開始招募 | 52 | Fuquinitinib 與 S-1 組合用於晚期轉移性結直腸癌的三線治療。 |
| [NCT00660894](https://clinicaltrials.gov/study/NCT00660894) | Phase 3 | 完成 | 1535 | 比較 S-1 與其他治療在 III 期結腸癌患者中的效果。 |

## 文獻證據

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [31917122](https://pubmed.ncbi.nlm.nih.gov/31917122/) | 2020 | RCT | Clin Colorectal Cancer | S-1 與 Oxaliplatin 作為高風險 III 期結腸癌患者術後輔助化療的效果尚未確立。 |
| [25209093](https://pubmed.ncbi.nlm.nih.gov/25209093/) | 2014 | Review | Clin Colorectal Cancer | 亞洲轉移性結直腸癌治療指引。 |
| [20500514](https://pubmed.ncbi.nlm.nih.gov/20500514/) | 2010 | Animal | Cancer Science | 開發了一種新的淋巴結轉移模型，並比較了 S-1 和 UFT/LV 的抗轉移效果。 |
| [26805106](https://pubmed.ncbi.nlm.nih.gov/26805106/) | 2015 | Case report | Gan to Kagaku Ryoho | 成功治療結腸癌轉移及復發的病例報告。 |
| [26036466](https://pubmed.ncbi.nlm.nih.gov/26036466/) | 2015 | RCT | BMC Cancer | ACTS-CC 試驗確認 S-1 在 III 期結直腸癌術後輔助化療中的非劣效性。 |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 |
|---------|------|------|-----------|
| 衛部藥製字第061956號 | "杏輝"氮尿嘧啶酸鉀鹽 | （粉） | 胃癌用藥。 |
| 衛部藥製字第058552號 | "台耀"歐特拉西兒 | 粉劑 | 胃癌用藥。 |
| 衛署藥輸字第025243號 | 愛斯萬膠囊20毫克 | 膠囊劑 | 胃癌、胰臟癌、大腸直腸癌、非小細胞肺癌、膽道癌、早期乳癌 |

## 細胞毒性

| 項目 | 內容 |
|------|------|
| 細胞毒性分類 | 傳統細胞毒性藥物（Fluoropyrimidine 類） |
| 骨髓抑制風險 | 中度 |
| 致吐性分級 | 低至中度 |
| 監測項目 | CBC（含分類）、肝腎功能、電解質 |
| 處置防護 | 需依細胞毒性藥物處置規範操作 |

## 安全性考量

安全性資訊請參考原廠仿單。

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
有多個 Phase 2/3 臨床試驗支持 S-1 用於結直腸癌的療效，且 S-1 複方已在台灣取得大腸直腸癌適應症，證據充分。

**若要推進需要：**
- 詳細的藥物作用機轉資料（MOA）
- 特定族群的安全性監測計畫

---

