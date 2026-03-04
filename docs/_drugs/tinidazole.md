---
layout: default
title: Tinidazole
parent: 僅模型預測 (L5)
nav_order: 173
evidence_level: L5
indication_count: 1
---

# Tinidazole
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

# Tinidazole (梯尼達諾) - 藥師評估報告

## 一句話總結

Tinidazole 是一種 5-硝基咪唑類抗原蟲藥物，TxGNN 預測多項婦科與感染相關新適應症，其中 AIDS 相關感染治療已有臨床試驗與文獻支持，值得進一步關注。

---

## 快速總覽

| 項目 | 內容 |
|------|------|
| 藥物名稱 | Tinidazole (梯尼達諾) |
| DrugBank ID | DB00911 |
| 原適應症 | 陰道滴蟲症、阿米巴症、梨形鞭毛蟲症 |
| 預測新適應症 | 停經後萎縮性陰道炎、外陰潰瘍、外陰腫瘤、乳房纖維囊腫、AIDS 等 |
| 最高 TxGNN 分數 | 0.999 (停經後萎縮性陰道炎，排名 2,039) |
| 證據等級 | AIDS：1 項臨床試驗、17 篇相關文獻 |
| 台灣上市狀態 | 有效許可證（生達、政德、信東等廠） |

---

## 為什麼預測合理？

### 機轉分析

Tinidazole 屬於 5-硝基咪唑類藥物，具有廣效抗原蟲與厭氧菌活性。其預測用途的合理性分析如下：

1. **停經後萎縮性陰道炎 (分數 0.999)**：可能與共病感染相關，但萎縮性陰道炎本質為荷爾蒙缺乏
2. **外陰潰瘍 (分數 0.999)**：Trichomonas vaginalis 感染確實可導致外陰潰瘍（有文獻支持）
3. **AIDS 相關感染 (分數 0.997)**：HIV 患者常合併寄生蟲感染，Tinidazole 可用於治療阿米巴症、梨形鞭毛蟲症

---

## 臨床試驗

### AIDS 相關臨床試驗

| 試驗編號 | 標題 | 階段 | 狀態 | 收案數 |
|---------|------|------|------|-------|
| NCT03412071 | Testing the Ability of a Microbiome-Focused Intervention to Reduce HIV Susceptibility in Ugandan Men | N/A | Unknown | 125 |

**試驗摘要**：評估包含 Tinidazole 在內的抗菌介入對包皮微生物組及 HIV 易感性的影響。

---

## 文獻證據

### AIDS 相關文獻 (共 17 篇)

**重要文獻精選**：

1. **Gupta S et al. (2022)** - *Amebiasis and Amebic Liver Abscess in Children*
   - AIDS/HIV 患者為高風險族群，Tinidazole 是阿米巴症的推薦治療藥物

2. **Watanabe K et al. (2011)** - *Amebiasis in HIV-1-infected Japanese men*
   - 170 例 HIV 合併阿米巴感染，Tinidazole 治療成功率高

3. **Rossignol JF (2010)** - *Cryptosporidium and Giardia: treatment options*
   - Tinidazole 對梨形鞭毛蟲症有效，可單劑量給藥

4. **Mitchell L et al. (2010)** - *Trichomonas vaginalis: an unusual presentation*
   - 報告 Tinidazole 成功治療表現為外陰潰瘍的滴蟲感染

---

## 台灣上市情形

Tinidazole 在台灣有多張有效許可證：

| 許可證字號 | 品名 | 許可證持有者 | 效期 |
|-----------|------|-------------|------|
| 衛署藥製字第019786號 | 淨樂膠衣錠 | 生達化學製藥 | 2029/12/14 |
| 衛署藥製字第012341號 | 立舒朗膠囊 | 政德製藥 | 2028/04/15 |
| 衛署藥製字第032122號 | 沙特靜脈點滴注射液 | 信東生技 | 2030/02/01 |

---

## 安全性考量

### 重要藥物交互作用

| 嚴重度 | 交互作用藥物 | 臨床意義 |
|--------|-------------|---------|
| Major | 霍亂活疫苗 (Vibrio cholerae vaccine) | 可能降低疫苗效果 |
| Moderate | Ethanol | 雙硫侖樣反應 |
| Moderate | Paclitaxel | 可能增加毒性 |
| Moderate | Warfarin | 增強抗凝血作用 |
| Moderate | Levodopa | 可能影響療效 |

### 一般注意事項

1. 服藥期間及停藥後 72 小時內禁止飲酒
2. 可能引起金屬味、噁心、頭痛
3. 孕婦不建議使用（尤其是第一孕期）

---

## 結論

### 預測適應症評估

| 適應症 | TxGNN 分數 | 臨床試驗 | 文獻 | 建議 |
|-------|-----------|---------|------|------|
| 停經後萎縮性陰道炎 | 0.999 | 無 | 無 | 不建議 |
| 外陰潰瘍 | 0.999 | 無 | 有相關病例報告 | 可考慮（合併感染時） |
| AIDS 相關感染 | 0.997 | 1 項 | 17 篇 | **建議（已有證據）** |

### 臨床建議

1. **AIDS 患者合併寄生蟲感染**：Tinidazole 是合理的治療選擇，有充足文獻支持
2. **停經後萎縮性陰道炎**：不建議，應使用荷爾蒙療法
3. **外陰潰瘍**：若懷疑滴蟲感染，可作為診斷性治療選擇

---

*報告產生日期：2026-02-11*
*資料來源：TxGNN 知識圖譜預測、ClinicalTrials.gov、PubMed、台灣 FDA*


---

