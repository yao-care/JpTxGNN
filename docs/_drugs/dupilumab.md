---
layout: default
title: Dupilumab
parent: 中證據等級 (L3-L4)
nav_order: 63
evidence_level: L3
indication_count: 1
---

# Dupilumab
{: .fs-9 }

證據等級: **L3** | 預測適應症: **1** 個
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

# Dupilumab：從異位性皮膚炎到支氣管炎

## 一句話總結

Dupilumab 原本用於治療中至重度異位性皮膚炎、氣喘及慢性鼻竇炎合併鼻息肉。
TxGNN 模型預測它可能對**支氣管炎 (bronchitis)** 有效，
目前有 **1 個臨床試驗**和 **多篇文獻**支持這個方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 異位性皮膚炎、氣喘、慢性鼻竇炎合併鼻息肉、嗜伊紅性食道炎 |
| 預測新適應症 | 支氣管炎 (bronchitis) |
| TxGNN 預測分數 | 99.92% |
| 證據等級 | L3 |
| 台灣上市 | 已上市 |
| 許可證數 | 2 張 |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

Dupilumab 是一種人源化單株抗體，可阻斷 IL-4 和 IL-13 的訊號傳遞，
這兩種細胞因子是第二型發炎反應的關鍵介質。支氣管炎，特別是嗜酸性支氣管炎，
涉及類似的發炎機轉。Dupilumab 已核准用於嗜酸性白血球表現型的氣喘，
其對下呼吸道發炎的抑制作用可能延伸至支氣管炎的治療。

## 臨床試驗證據

| 試驗編號 | 階段 | 狀態 | 人數 | 主要發現 |
|---------|------|------|------|---------|
| [NCT04362501](https://clinicaltrials.gov/study/NCT04362501) | Phase 2 | COMPLETED | 33 | 評估 dupilumab 在無鼻息肉的慢性鼻竇炎患者的療效 |
| [NCT03346434](https://clinicaltrials.gov/study/NCT03346434) | Phase 2/3 | COMPLETED | 202 | 評估 dupilumab 在 6 個月至 6 歲異位性皮膚炎兒童的藥動學和療效 |
| [NCT01949311](https://clinicaltrials.gov/study/NCT01949311) | Phase 3 | COMPLETED | 2733 | Dupilumab 在異位性皮膚炎成人患者的長期安全性研究 |
| [NCT04287621](https://clinicaltrials.gov/study/NCT04287621) | N/A | ACTIVE_NOT_RECRUITING | 718 | RAPID 登記研究：氣喘患者使用 dupilumab 的真實世界數據 |
| [NCT02277769](https://clinicaltrials.gov/study/NCT02277769) | Phase 3 | COMPLETED | 708 | 確認 dupilumab 單藥治療中至重度異位性皮膚炎的療效 |

## 文獻證據

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [34597534](https://pubmed.ncbi.nlm.nih.gov/34597534/) | 2022 | RCT extension | Lancet Respir Med | TRAVERSE 研究：dupilumab 在中至重度氣喘的長期安全性和療效 |
| [30273510](https://pubmed.ncbi.nlm.nih.gov/30273510/) | 2019 | Meta-analysis | J Asthma | Dupilumab 在控制不佳氣喘的療效和安全性系統性回顧 |
| [38488768](https://pubmed.ncbi.nlm.nih.gov/38488768/) | 2024 | Case report | Pediatr Pulmonol | Dupilumab 用於兒童嗜酸性塑型性支氣管炎的新療法 |
| [30196731](https://pubmed.ncbi.nlm.nih.gov/30196731/) | 2018 | Review | Expert Opin Pharmacother | 吸菸相關氣道疾病合併氣喘的治療挑戰 |
| [32428511](https://pubmed.ncbi.nlm.nih.gov/32428511/) | 2020 | Clinical study | Chest | 抗 T2 生物製劑治療對類固醇依賴型氣喘肺通氣的影響 |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 |
|---------|------|------|-----------|
| 2 張許可證 | 杜避炎注射劑300毫克 | 注射劑 | 異位性皮膚炎、氣喘、慢性鼻竇炎合併鼻息肉、嗜伊紅性食道炎、COPD、慢性自發性蕁麻疹 |

## 安全性考量

- **常見不良反應**：注射部位反應、結膜炎、口唇皰疹
- **重要注意事項**：開始治療前應評估寄生蟲感染，不建議與活病毒疫苗同時使用
- **特殊族群**：兒童使用需按體重調整劑量

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
Dupilumab 抑制 IL-4/IL-13 的機轉適用於嗜酸性發炎相關的支氣管炎，
已有病例報告支持其在嗜酸性塑型性支氣管炎的療效。需區分支氣管炎的亞型。

**若要推進需要：**
- 區分嗜酸性與非嗜酸性支氣管炎的生物標記
- 針對慢性支氣管炎患者的前瞻性臨床試驗
- 與 COPD 合併嗜酸性白血球增高患者的治療效益評估


---

