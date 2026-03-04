---
layout: default
title: Deoxycholic Acid
parent: 僅模型預測 (L5)
nav_order: 55
evidence_level: L5
indication_count: 1
---

# Deoxycholic Acid
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

# Deoxycholic Acid (去氧膽酸) - 藥師評估報告

## 一句話總結

Deoxycholic acid 是一種膽酸類藥物，用於膽結石溶解和皮下脂肪消除；TxGNN 預測其可能用於罕見遺傳性眼疾和糖尿病腎病，但這些預測的機轉連結薄弱，臨床轉化可能性低。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 藥物名稱 | Deoxycholic acid (去氧膽酸) |
| DrugBank ID | DB03619 |
| 台灣商品名 | 去氧熊膽酸、Deoxycholic acid 等 |
| 原適應症 | 膽固醇性膽結石溶解、原發性膽道肝硬化、頦下脂肪消除 |
| 預測新適應症 | 家族性血尿-視網膜動脈迂曲-攣縮症候群、腦小血管病變、糖尿病腎病 |
| 最高 TxGNN 分數 | 0.9948 |
| 臨床試驗支持 | 無 |
| 文獻支持 | 間接有 (糖尿病腎病相關) |

## 為什麼預測合理

### 機轉分析

1. **家族性血尿-視網膜動脈迂曲-攣縮症候群 (autosomal dominant familial hematuria-retinal arteriolar tortuosity-contractures syndrome)**：
   - 這是一種極為罕見的遺傳性疾病
   - TxGNN 分數 0.9948，但無任何文獻支持
   - 機轉連結極為薄弱

2. **腦小血管病變伴或不伴眼部異常 (brain small vessel disease 1)**：
   - TxGNN 分數 0.9948
   - 有多篇文獻涉及眼部發育異常，但與膽酸無直接關聯
   - 預測可能源於知識圖譜中的間接關聯

3. **糖尿病腎病 (diabetic nephropathy)**：
   - TxGNN 分數 0.9932
   - 有較多相關文獻支持膽酸在糖尿病腎病中的保護作用
   - 機轉：膽酸可作為 FXR (farnesoid X receptor) 和 TGR5 的配體，調節糖脂代謝和發炎反應

### 預測品質評估

- 前兩項預測為罕見遺傳疾病，臨床實用性極低
- 糖尿病腎病預測具有較好的機轉基礎
- 但主要研究使用的是 ursodeoxycholic acid (UDCA)，而非 deoxycholic acid

## 臨床試驗

**無相關臨床試驗**

目前未發現 deoxycholic acid 用於預測新適應症的臨床試驗。

## 文獻證據

### 糖尿病腎病相關文獻

1. **Wang XX et al. (2018)** - JASN
   - 標題：FXR/TGR5 雙重激動劑可預防糖尿病和肥胖症腎病進展
   - 發現：膽酸受體激動劑 INT-767 可改善糖尿病小鼠的蛋白尿和腎臟損傷
   - 相關性：機轉上支持膽酸類藥物對腎臟的保護作用

2. **Cao A et al. (2016)** - Biol Pharm Bull
   - 標題：Ursodeoxycholic acid 通過減輕高血糖介導的氧化壓力改善糖尿病腎病
   - 相關性：使用 UDCA（非 deoxycholic acid），但顯示膽酸類藥物的腎保護潛力

3. **Cao AL et al. (2016)** - Lab Invest
   - 標題：UDCA 和 4-PBA 可預防糖尿病腎病中內質網壓力誘導的足細胞凋亡
   - 相關性：膽酸類藥物的腎保護機轉研究

4. **Liu C et al. (2024)** - ACS Biomater Sci Eng
   - 研究使用 deoxycholic acid 修飾的奈米粒子用於糖尿病腎病治療
   - 相關性：deoxycholic acid 作為藥物傳遞載體而非活性成分

### 眼部疾病相關文獻

- 多篇文獻涉及先天性眼部異常，但與 deoxycholic acid 無直接治療關聯
- 僅為 MeSH 標籤共現，非實質治療證據

## 台灣上市狀態

| 許可證號 | 商品名 | 劑型 | 適應症 | 狀態 |
|----------|--------|------|--------|------|
| 多項 | 去氧熊膽酸等 | 粉劑/膠囊 | 膽結石溶解、利膽 | 部分有效 |

**備註**：多數許可證已註銷，目前主要以 ursodeoxycholic acid 產品為主流。

## 安全性

### 藥物交互作用

本次資料未包含 deoxycholic acid 的詳細 DDI 資訊。

### 一般注意事項

- 口服製劑：可能引起腹瀉
- 注射製劑（用於頦下脂肪消除）：
  - 注射部位反應（腫脹、疼痛、麻木）
  - 可能造成神經損傷
  - 吞嚥困難（罕見）

## 結論

### 整體評估：低優先級

Deoxycholic acid 的 TxGNN 預測多為罕見遺傳疾病，臨床實用性低。糖尿病腎病的預測雖有機轉支持，但現有研究主要使用 UDCA 而非 deoxycholic acid，且 deoxycholic acid 的溶解作用可能對腎臟反而有潛在風險。

### 建議

1. **不建議**優先研究此藥物的新適應症
2. 若對膽酸類藥物在糖尿病腎病的應用有興趣，應優先考慮 UDCA
3. 罕見遺傳眼疾的預測缺乏實證基礎，不建議追蹤

### 證據等級總結

| 預測適應症 | TxGNN 分數 | 臨床試驗 | 文獻支持 | 機轉合理性 | 綜合評估 |
|------------|------------|----------|----------|------------|----------|
| 家族性血尿-視網膜動脈迂曲-攣縮症候群 | 0.9948 | 無 | 無 | 極低 | 不推薦 |
| 腦小血管病變伴眼部異常 | 0.9948 | 無 | 無 | 極低 | 不推薦 |
| 糖尿病腎病 | 0.9932 | 無 | 間接有 | 中等 | 考慮 UDCA |

---
*報告產生日期：2026-02-11*
*資料來源：TxGNN 預測、ClinicalTrials.gov、PubMed、台灣 FDA*


---

