---
layout: default
title: Etanercept
parent: 僅模型預測 (L5)
nav_order: 66
evidence_level: L5
indication_count: 1
---

# Etanercept
{: .fs-9 }

證據等級: **L5** | 預測適應症: **1** 個
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

# Etanercept 藥師評估筆記

## 一句話總結

Etanercept 是一種 TNF-alpha 抑制劑，TxGNN 預測其可能用於多種神經退化性疾病，但目前缺乏臨床試驗支持。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 藥物名稱 | Etanercept (恩博) |
| DrugBank ID | DB00005 |
| 台灣商品名 | 爾瑞易注射液 |
| 原核准適應症 | 類風濕性關節炎、乾癬性關節炎、僵直性脊椎炎、中重度乾癬 |
| 預測新適應症 | 多發性硬化症(primary progressive)、視神經脊髓炎、肌萎縮性脊髓側索硬化症 |
| 最高預測分數 | 0.9986 (primary progressive multiple sclerosis) |
| 證據等級 | L5 (僅預測) |

## 為什麼這個預測合理

Etanercept 透過抑制 TNF-alpha 發揮免疫調節作用。TNF-alpha 在神經退化性疾病中的角色已被廣泛研究：

1. **發炎機轉關聯**：TNF-alpha 參與中樞神經系統的發炎反應，而神經發炎是多發性硬化症和視神經脊髓炎的重要病理機制
2. **血腦屏障通透性**：TNF-alpha 可增加血腦屏障通透性，理論上抑制 TNF-alpha 可能減少神經損傷
3. **免疫調節重疊**：Etanercept 已核准用於多種自體免疫疾病，這些疾病與神經自體免疫疾病有部分機轉重疊

然而需注意：Etanercept 為大分子生物製劑，難以穿透血腦屏障，這對中樞神經系統疾病的治療構成挑戰。

## 臨床試驗證據

目前在 ClinicalTrials.gov 和 ICTRP 資料庫中，**未發現** Etanercept 用於以下預測適應症的臨床試驗：
- Primary progressive multiple sclerosis
- Neuromyelitis optica
- Amyotrophic lateral sclerosis
- Huntington disease

**證據等級：L5 (僅預測)**

## 文獻證據

PubMed 文獻搜尋結果：

| 預測適應症 | 相關文獻數 | 關鍵發現 |
|-----------|-----------|---------|
| Primary progressive MS | 0 | 無直接相關研究 |
| Neuromyelitis optica | 0 | 無直接相關研究 |
| ALS | 0 | 無直接相關研究 |
| Huntington disease | 0 | 無直接相關研究 |

目前缺乏直接支持這些預測的文獻證據。

## 台灣上市資訊

| 項目 | 內容 |
|------|------|
| 許可證字號 | 衛署菌疫輸字第000876號 |
| 中文品名 | 爾瑞易注射液 |
| 英文品名 | Enbrel Solution for Injection |
| 許可證持有者 | 輝瑞大藥廠股份有限公司 |
| 劑型 | 注射劑 |
| 核准日期 | 2012/03/26 |
| 有效期限 | 2027/03/26 |
| 狀態 | 有效 |

## 安全性考量

### 已知風險
- **感染風險增加**：包括嚴重細菌、病毒、真菌感染
- **結核病再活化**：使用前需篩檢潛伏性結核
- **惡性腫瘤風險**：長期使用可能增加淋巴瘤風險
- **注射部位反應**：常見局部反應

### 藥物交互作用
根據 DDInter 資料庫，Etanercept 與以下藥物有交互作用：
- Anakinra (Major)：不建議併用，增加嚴重感染風險
- Abatacept (Major)：不建議併用
- 活疫苗：禁止併用

### 特殊族群
- **孕婦**：C 級，權衡利弊後使用
- **哺乳**：少量分泌至乳汁
- **肝腎功能不全**：無需調整劑量

## 結論與下一步

### 整體評估
此預測目前**不建議臨床應用**，原因如下：
1. 缺乏任何臨床試驗或觀察性研究支持
2. Etanercept 為大分子藥物，中樞神經系統滲透性差
3. 部分預測適應症(如 MS)實際上可能因 TNF 抑制而惡化

### 建議行動
- [ ] 需要更多基礎研究探討 TNF-alpha 抑制在神經退化性疾病中的角色
- [ ] 若要進行臨床研究，需先解決藥物遞送至中樞神經系統的問題
- [ ] 密切監測已使用 Etanercept 患者是否出現神經系統症狀

### 風險等級
**高風險** - 不建議超適應症使用

---

*報告生成日期：2026-02-11*
*資料來源：TxGNN 預測、ClinicalTrials.gov、PubMed、TFDA*


---

