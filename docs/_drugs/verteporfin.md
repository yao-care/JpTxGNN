---
layout: default
title: Verteporfin
parent: 僅模型預測 (L5)
nav_order: 188
evidence_level: L5
indication_count: 1
---

# Verteporfin
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

# Verteporfin 藥師評估報告

## 一句話總結

Verteporfin 是一種用於光動力療法的感光劑，TxGNN 預測其可能對粒線體氧化磷酸化障礙具有潛在療效，但目前缺乏臨床試驗及文獻證據支持。

---

## 快速總覽

| 項目 | 內容 |
|------|------|
| 藥物名稱 | Verteporfin (維視達) |
| DrugBank ID | DB00460 |
| 原核准適應症 | 黃斑部退化病變引起之脈絡膜血管新生 |
| 預測新適應症數量 | 1 項 |
| 最高預測分數適應症 | 粒線體氧化磷酸化障礙 (核 DNA 異常)，分數 0.995 |
| 臨床試驗支持 | 無 |
| 文獻證據 | 無直接相關文獻 |
| 台灣上市狀態 | 有效 (衛署藥輸字第023479號) |

---

## 為什麼預測合理

### 預測機制分析

**粒線體氧化磷酸化障礙 (核 DNA 異常)**
- TxGNN 分數: 0.995
- TxGNN 排名: 9,882

**可能的機制連結**：
1. Verteporfin 的光動力作用涉及活性氧 (ROS) 生成
2. 粒線體是細胞內主要的 ROS 來源和氧化磷酸化場所
3. 知識圖譜可能透過氧化還原相關路徑建立連結

**評估**：
- 此預測的藥理學合理性較弱
- Verteporfin 主要為眼科局部光動力療法使用
- 對於全身性粒線體疾病的治療效益不明

### 知識圖譜連結

預測可能基於：
- 紫質類化合物與粒線體代謝的間接關聯
- 氧化還原反應路徑的共享特徵

---

## 臨床試驗

### 預測適應症相關臨床試驗

**直接相關：無**

針對 "Verteporfin + 粒線體氧化磷酸化障礙" 的搜尋結果：
- ClinicalTrials.gov：0 筆
- ICTRP：0 筆

---

## 文獻證據

### 預測適應症相關 PubMed 文獻

**直接相關：0 篇**

針對 "Verteporfin + mitochondrial oxidative phosphorylation disorder" 的搜尋結果：
- PubMed：0 筆

**證據等級評估：極弱**
- 無任何直接支持證據
- 預測僅基於知識圖譜的統計關聯

---

## 台灣上市資訊

### 有效許可證

| 許可證字號 | 中文品名 | 英文品名 | 劑型 |
|------------|----------|----------|------|
| 衛署藥輸字第023479號 | 維視達凍晶注射劑15毫克 | VISUDYNE | 凍晶注射劑 |

### 許可證詳細資訊

| 項目 | 內容 |
|------|------|
| 核准日期 | 2002/07/01 |
| 效期 | 2027/07/01 |
| 許可證持有者 | 裕利股份有限公司 |
| 適應症 | 因年齡相關性黃斑部退化病變引起之主要典型或潛隱性視網膜下中央凹脈絡膜血管新生，病理性近視(PM)或疑似眼組織漿菌症引起之視網膜下中央凹脈絡膜血管新生 |

---

## 安全性資訊

### 藥物交互作用 (DDI)

**重大交互作用 (Major)：1 項**
- Aminolevulinic acid (5-ALA) - 另一種感光劑，可能增加光敏感性

**中度交互作用 (Moderate)：95+ 項**

主要類別包括：

**光敏感藥物類**：
- 四環黴素類：Doxycycline、Tetracycline、Minocycline、Demeclocycline
- 磺胺類：Sulfasalazine、Sulfamethizole
- Quinolone 類：Levofloxacin
- 維生素 A 衍生物：Isotretinoin、Tretinoin、Acitretin、Adapalene
- 其他：Methoxsalen、Porfimer sodium、Griseofulvin

**抗凝血/抗血小板藥物**：
- Warfarin、Heparin、Enoxaparin、Dalteparin
- Apixaban、Rivaroxaban、Edoxaban、Dabigatran
- Clopidogrel、Ticagrelor、Prasugrel
- Aspirin (Acetylsalicylic acid)

**降血糖藥物**：
- Glimepiride、Glipizide、Glyburide、Tolbutamide、Tolazamide

**抗腫瘤藥物**：
- Imatinib、Erlotinib、Gefitinib、Afatinib、Lapatinib
- Vemurafenib、Dabrafenib、Vandetanib

**血管擴張劑**：
- Diazoxide、Phentolamine、Minoxidil、Papaverine

**未知交互作用 (Unknown)：15+ 項**
- Metformin、Omeprazole、Lansoprazole、Simvastatin、Rosuvastatin 等常用藥物

### 使用注意事項

1. **光敏感性**
   - 治療後 48 小時內應避免直接陽光或強光照射
   - 避免併用其他光敏感藥物

2. **注射部位反應**
   - 可能出現注射部位疼痛、水腫、出血

3. **視力相關**
   - 可能短暫視力下降、視覺障礙
   - 需由眼科專科醫師執行

4. **出血風險**
   - 與抗凝血藥物併用需謹慎監測

5. **肝功能**
   - 主要經肝臟代謝，肝功能不全患者需調整

---

## 結論

### 整體評估

Verteporfin 針對粒線體氧化磷酸化障礙的預測缺乏藥理學合理性和臨床證據支持。此預測可能為知識圖譜中的統計假象，不建議進行臨床探索。

### 建議

1. **不建議進行老藥新用探索** - 預測缺乏合理機制基礎
2. **維持現有眼科適應症使用** - 光動力療法治療濕性 AMD
3. **注意光敏感性藥物交互作用** - 臨床使用時需特別警覺

### 證據等級

| 類別 | 評級 |
|------|------|
| 預測可信度 | 低 (缺乏機制支持) |
| 臨床證據 | 極弱 (無相關試驗或文獻) |
| 安全性顧慮 | 中等 (光敏感性、多重 DDI) |
| 老藥新用潛力 | 極低 |

### 其他考量

Verteporfin 近年來在非眼科領域有一些新興研究方向值得關注：
- YAP/TAZ 訊號通路抑制
- 抗纖維化作用
- 腫瘤光動力療法

這些研究方向與本次預測的粒線體疾病無直接關聯，但可能提供未來老藥新用研究的參考。

---

*報告產生日期：2026-02-11*
*資料來源：TxGNN 知識圖譜、PubMed、ClinicalTrials.gov、台灣 FDA*


---

