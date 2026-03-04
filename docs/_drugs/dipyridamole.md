---
layout: default
title: Dipyridamole
parent: 僅模型預測 (L5)
nav_order: 57
evidence_level: L5
indication_count: 1
---

# Dipyridamole
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

# Dipyridamole (待乙妥) - 藥師評估報告

## 一句話總結

Dipyridamole 是一種磷酸二酯酶抑制劑和腺苷再攝取抑制劑，用於心絞痛和血栓預防；TxGNN 預測其對變異型心絞痛和中風有潛在療效，有豐富的臨床試驗和文獻支持，但變異型心絞痛預測與原適應症高度重疊。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 藥物名稱 | Dipyridamole (待乙妥/雙乙妥) |
| DrugBank ID | DB00975 |
| 台灣商品名 | 百心康、Aggrenox（與 aspirin 複方） |
| 原適應症 | 慢性狹心症、冠狀動脈不全、血小板凝集降低、心肌灌流造影替代運動試驗 |
| 預測新適應症 | 變異型心絞痛 (Prinzmetal angina)、中風 |
| 最高 TxGNN 分數 | 0.9999 (Prinzmetal angina) |
| 臨床試驗支持 | **豐富** (中風預防) |
| 文獻支持 | **豐富** |

## 為什麼預測合理

### 機轉分析

1. **變異型心絞痛 (Prinzmetal angina)**：
   - TxGNN 分數 0.9999，排名 438
   - Dipyridamole 是冠狀動脈血管擴張劑
   - 理論上可緩解冠狀動脈痙攣
   - 但文獻顯示其對變異型心絞痛的效果不一，部分研究甚至指出無效或可能加重症狀
   - **注意**：此預測與原適應症「慢性狹心症」高度重疊

2. **中風 (stroke disorder)**：
   - TxGNN 分數 0.9995，排名 1695
   - Dipyridamole 抑制血小板凝集
   - 與 aspirin 合用已被廣泛用於缺血性中風的二級預防
   - **重要**：Aggrenox (dipyridamole + aspirin) 已是核准適應症

### 預測品質評估

- 預測準確但與現有適應症重疊度高
- 變異型心絞痛的文獻證據矛盾
- 中風預防已有核准適應症（複方製劑）

## 臨床試驗

### 中風相關重要試驗

1. **PRoFESS (NCT00153062)** - 已完成
   - 設計：雙盲、活性藥物與安慰劑對照
   - 比較：Aggrenox (dipyridamole + aspirin) vs Clopidogrel
   - 受試者：20,332 人
   - 贊助者：Boehringer Ingelheim
   - 結果：兩組在預防再發中風方面效果相當

2. **ESPRIT (NCT00161070)** - 已完成
   - 設計：歐洲/澳洲多國試驗
   - 比較：Aspirin + dipyridamole vs Aspirin alone
   - 受試者：4,500 人
   - 結果：複方治療優於單獨 aspirin

3. **GORE REDUCE (NCT00738894)** - 已完成
   - 設計：PFO 封堵術 + 抗血小板治療（包含 dipyridamole）vs 單純藥物治療
   - 受試者：664 人
   - 結果：PFO 封堵術可降低隱源性中風復發

4. **EARLY (NCT00562588)** - 已完成
   - 研究急性中風 24 小時內開始 Aggrenox 的療效
   - 受試者：551 人

### 其他相關試驗

- **NCT02966119** (RESTART-FR)：腦出血後重啟抗血小板藥物的研究
- **NCT01781611**：Dipyridamole 用於系統性紅斑性狼瘡的研究

## 文獻證據

### 變異型心絞痛相關文獻

1. **Yasue H et al. (1978)** - Jpn Circ J
   - 研究各種藥物對靜止型心絞痛的效果
   - 發現：Dipyridamole 對 Prinzmetal 變異型心絞痛**無效**
   - 相對而言，Diltiazem 對所有病例都有效

2. **Picano E et al. (1988)** - Am J Cardiol
   - 報告 aminophylline 終止 dipyridamole 壓力測試可能誘發變異型心絞痛患者的冠狀動脈痙攣
   - 警示：使用 dipyridamole 進行壓力測試時需注意

3. **多項 dipyridamole 壓力測試研究**
   - Dipyridamole 主要作為診斷工具而非治療藥物用於變異型心絞痛

### 中風預防相關文獻

- 大量支持 dipyridamole + aspirin 複方用於缺血性中風二級預防的證據
- 這已是確立的適應症

## 台灣上市狀態

| 許可證號 | 商品名 | 劑型 | 適應症 | 狀態 |
|----------|--------|------|--------|------|
| 多項 | 百心康等 | 錠劑/膠囊 | 慢性狹心症、血小板凝集降低 | 部分有效 |

**備註**：Aggrenox（dipyridamole + aspirin 複方）國際上用於中風預防，台灣需確認是否有上市。

## 安全性

### 藥物交互作用

Dipyridamole 的主要交互作用與其腺苷再攝取抑制作用相關：

| 併用藥物 | 注意事項 |
|----------|----------|
| Adenosine | 增強腺苷作用，需調整劑量 |
| 抗凝血劑 | 增加出血風險 |
| 抗血小板藥物 | 出血風險加成 |

### 重要警語

- 不穩定型心絞痛或急性心肌梗塞期間應謹慎使用
- 低血壓風險
- 可能引起頭痛、頭暈

## 結論

### 整體評估：已有成熟適應症

Dipyridamole 的 TxGNN 預測雖然分數很高，但兩項主要預測都與現有適應症高度重疊：

1. **變異型心絞痛**：文獻證據矛盾，且部分研究顯示無效
2. **中風預防**：Dipyridamole + aspirin 複方已是確立的二級預防方案

### 建議

1. **不需要**進行新適應症研究，因為預測的適應症已是現有用途或其延伸
2. 對於變異型心絞痛，現有證據不支持將 dipyridamole 作為首選治療
3. 中風預防應優先考慮 Aggrenox 複方或其他已證實有效的抗血小板方案

### 證據等級總結

| 預測適應症 | TxGNN 分數 | 臨床試驗 | 文獻支持 | 機轉合理性 | 綜合評估 |
|------------|------------|----------|----------|------------|----------|
| Prinzmetal angina | 0.9999 | 診斷用途 | 有（但矛盾） | 中等 | 與原適應症重疊，效果存疑 |
| 中風 | 0.9995 | **豐富** | **豐富** | 高 | 已為適應症（複方） |

---
*報告產生日期：2026-02-11*
*資料來源：TxGNN 預測、ClinicalTrials.gov、PubMed、台灣 FDA*


---

