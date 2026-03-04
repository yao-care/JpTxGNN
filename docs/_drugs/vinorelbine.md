---
layout: default
title: Vinorelbine
parent: 中證據等級 (L3-L4)
nav_order: 190
evidence_level: L3
indication_count: 1
---

# Vinorelbine
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

# Vinorelbine：從非小細胞肺癌到 Ewing 肉瘤

## 一句話總結

Vinorelbine 原本用於治療非小細胞肺癌和轉移性乳癌。
TxGNN 模型預測它可能對 **Ewing 肉瘤 (Ewing sarcoma)** 有效，
目前有 **4 個臨床試驗**支持這個方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 非小細胞肺癌、轉移性乳癌 |
| 預測新適應症 | Ewing 肉瘤 (Ewing sarcoma) |
| TxGNN 預測分數 | 99.999% |
| 證據等級 | L3 |
| 台灣上市 | 已上市 |
| 許可證數 | 19 張 |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

Vinorelbine 是半合成的長春花生物鹼（Vinca alkaloid），透過阻斷微管蛋白聚合抑制有絲分裂。Ewing 肉瘤是一種高度增殖的惡性腫瘤，對微管抑制劑具有敏感性。Vinorelbine 在多項兒童難治性腫瘤的臨床試驗中展現活性，包括 Ewing 肉瘤。

## 臨床試驗證據

| 試驗編號 | 階段 | 狀態 | 人數 | 主要發現 |
|---------|------|------|------|---------|
| [NCT06451302](https://clinicaltrials.gov/study/NCT06451302) | N/A | ACTIVE_NOT_RECRUITING | 100 | 評估中國兒童 Ewing 肉瘤風險分層導向治療的療效和安全性 |
| [NCT00003234](https://clinicaltrials.gov/study/NCT00003234) | Phase 2 | COMPLETED | 50 | 研究 Vinorelbine 在復發/難治性兒童惡性腫瘤中的效果，包括 Ewing 肉瘤 |
| [NCT00180947](https://clinicaltrials.gov/study/NCT00180947) | Phase 2 | UNKNOWN | 210 | 評估 Vinorelbine 與 Cyclophosphamide 組合在難治性腫瘤中的抗腫瘤活性 |
| [NCT05999994](https://clinicaltrials.gov/study/NCT05999994) | Phase 2 | RECRUITING | 105 | CAMPFIRE 兒童和青少年創新研究主協議 |

## 文獻證據

目前無專門針對 Vinorelbine 用於 Ewing 肉瘤的 PubMed 文獻收錄，但有相關的兒科腫瘤研究文獻支持其在難治性肉瘤中的應用。

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 |
|---------|------|------|-----------|
| 衛署藥輸字第022215號 | 溫諾平注射液10公絲/公撮 | 注射劑 | 非小細胞肺癌，轉移性乳癌 |
| 衛署藥輸字第024268號 | 溫諾平30毫克軟膠囊 | 軟膠囊劑 | 非小細胞肺癌、轉移性乳癌 |
| 衛署藥輸字第024269號 | 溫諾平20毫克軟膠囊 | 軟膠囊劑 | 非小細胞肺癌、轉移性乳癌 |
| 衛部藥製字第060608號 | 威若賓30毫克軟膠囊 | 軟膠囊劑 | 非小細胞肺癌、轉移性乳癌 |
| 衛署藥輸字第025489號 | 維諾拜注射液 | 注射劑 | 非小細胞肺癌、轉移性乳癌 |

## 細胞毒性

| 項目 | 內容 |
|------|------|
| 細胞毒性分類 | 傳統細胞毒性藥物（Vinca alkaloid） |
| 骨髓抑制風險 | 高度（嗜中性白血球減少為劑量限制毒性） |
| 致吐性分級 | 低度 |
| 監測項目 | CBC（含分類）、肝功能、神經毒性評估 |
| 處置防護 | 需依細胞毒性藥物處置規範操作；靜脈注射需注意外滲風險 |

## 安全性考量

### 重大藥物交互作用（Major）

| 交互作用藥物 | 機轉說明 |
|-------------|---------|
| Clarithromycin | CYP3A4 抑制劑，增加 vinorelbine 血中濃度和毒性 |

### 中度藥物交互作用（Moderate）

| 交互作用藥物 | 機轉說明 |
|-------------|---------|
| Aprepitant | CYP3A4 抑制 |
| Dexamethasone | 可能影響代謝 |
| Simvastatin | CYP3A4 競爭 |
| Rosuvastatin | 藥物轉運體交互作用 |

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
Vinorelbine 在多項兒童腫瘤臨床試驗中顯示對 Ewing 肉瘤具有潛在療效，且作用機轉（微管抑制）對高增殖性腫瘤具有合理的生物學基礎。

**若要推進需要：**
- 收集專門針對 Ewing 肉瘤的療效數據
- 確定適當的兒科劑量和給藥方案
- 與現有 Ewing 肉瘤標準治療方案的比較評估
- 骨髓抑制和神經毒性的密切監測計畫


---

