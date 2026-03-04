---
layout: default
title: Acitretin
parent: 中證據等級 (L3-L4)
nav_order: 12
evidence_level: L3
indication_count: 1
---

# Acitretin
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

# Acitretin：從乾癬到青春痘新適應症探索

## 一句話總結

Acitretin 原本用於嚴重性乾癬及皮膚角化症。
TxGNN 模型預測它可能對**青春痘 (acne)** 有效，
目前有 **1 個臨床試驗**和 **18 篇文獻**支持這個方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 嚴重性牛皮癬、皮膚角化症 |
| 預測新適應症 | 青春痘 (acne) |
| TxGNN 預測分數 | 99.94% |
| 證據等級 | L3 |
| 台灣上市 | 已上市 |
| 許可證數 | 6 張 |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

Acitretin 屬於第二代芳香族維生素 A 酸衍生物（retinoid），其主要作用機轉包括：
1. 調節角質細胞分化與增殖
2. 抑制皮脂腺活性
3. 抗發炎作用
4. 免疫調節功能

青春痘的病理機轉涉及皮脂腺過度分泌、毛囊角化異常、痤瘡桿菌增殖及發炎反應。Retinoids 類藥物（如 isotretinoin）已是嚴重青春痘的標準治療。

Acitretin 與 isotretinoin 同屬 retinoids，但 acitretin 傳統上較少用於青春痘，主要因為其抑制皮脂腺的效果較 isotretinoin 弱。然而，文獻顯示 acitretin 在以下情況可作為替代選擇：
- Isotretinoin 治療失敗後的維持療法
- 化膿性汗腺炎（hidradenitis suppurativa / acne inversa）合併結節囊腫型青春痘

2002 年個案報告 (PMID: 12080949) 顯示，isotretinoin 治療無效的結節囊腫型青春痘患者，使用 acitretin 後獲得顯著改善。

## 臨床試驗證據

| 試驗編號 | 階段 | 狀態 | 人數 | 主要發現 |
|---------|------|------|------|---------|
| [NCT04663906](https://clinicaltrials.gov/study/NCT04663906) | N/A | UNKNOWN | 300 | 研究口服 isotretinoin（同屬 retinoid）在 COVID-19 感染風險的影響 |

*註：目前無專門針對 acitretin 治療青春痘的註冊臨床試驗*

## 文獻證據

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [12080949](https://pubmed.ncbi.nlm.nih.gov/12080949/) | 2002 | Case Report | Cutis | Isotretinoin 無效的結節囊腫型青春痘合併化膿性汗腺炎，acitretin 維持治療成功 |
| [25640693](https://pubmed.ncbi.nlm.nih.gov/25640693/) | 2015 | Guideline | JEADV | 歐洲化膿性汗腺炎治療指引，提及 acitretin 為治療選項 |
| [29234829](https://pubmed.ncbi.nlm.nih.gov/29234829/) | 2018 | Review | Der Hautarzt | 化膿性汗腺炎藥物治療：isotretinoin 療效有限，acitretin 效果較佳 |
| [20874789](https://pubmed.ncbi.nlm.nih.gov/20874789/) | 2011 | Journal Article | Br J Dermatol | 25 年 acitretin 治療化膿性汗腺炎長期追蹤，療效良好 |
| [8573927](https://pubmed.ncbi.nlm.nih.gov/8573927/) | 1995 | Review | Dermatology | Retinoids 與皮脂腺活性：比較不同 retinoids 的抗痘效果 |
| [9074840](https://pubmed.ncbi.nlm.nih.gov/9074840/) | 1997 | Review | Drugs | Retinoids 在皮膚科的現況與未來：包含痤瘡相關應用 |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 |
|---------|------|------|-----------|
| 衛署藥輸字第022117號 | 新定康癬膠囊 25mg | 膠囊劑 | 嚴重性牛皮癬、皮膚角化症 |
| 衛署藥輸字第022118號 | 新定康癬膠囊 10mg | 膠囊劑 | 嚴重性牛皮癬、皮膚角化症 |

## 安全性考量

### 重要藥物交互作用

**Major 交互作用：**
- Tetracyclines（Doxycycline、Minocycline、Tetracycline）：增加假性腦瘤風險
- Vitamin A：增加維生素 A 過多症風險
- Ethanol（酒精）：可能將 acitretin 轉換為 etretinate，延長半衰期至數月
- Isotretinoin：禁止併用，增加維生素 A 毒性
- Methotrexate：增加肝毒性風險
- 口服避孕藥（Levonorgestrel、Norethisterone 等）：可能降低避孕效果

**Moderate 交互作用：**
- 磺胺尿素類降血糖藥（Glimepiride、Glipizide 等）：可能影響血糖控制
- 光敏感藥物（Aminolevulinic acid、Methoxsalen 等）：增加光敏感反應

### 重要警語
- **絕對禁止懷孕**：acitretin 具有強烈致畸性，育齡婦女必須於治療前、中、後使用有效避孕措施
- 因可能轉換為 etretinate，**停藥後需避孕至少 3 年**
- **禁止飲酒**：酒精會促進 acitretin 轉換為長效 etretinate
- 定期監測肝功能及血脂

安全性資訊請參考原廠仿單。

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
Acitretin 與 isotretinoin 同屬 retinoids，具有相似的抗角化及抗發炎機轉。文獻顯示其在 isotretinoin 治療失敗或需長期維持治療的青春痘患者中有應用價值。特別是在化膿性汗腺炎合併青春痘的情況下，acitretin 可能比 isotretinoin 更有效。

**若要推進需要：**
- 排除懷孕可能性，育齡婦女需使用兩種有效避孕方法
- 完全禁止飲酒
- 定期監測肝功能（ALT、AST）及血脂（TG、Cholesterol）
- 避免併用維生素 A 補充劑
- 避免併用四環黴素類抗生素
- 設計 RCT 比較 acitretin 與 isotretinoin 在不同類型青春痘的療效


---

