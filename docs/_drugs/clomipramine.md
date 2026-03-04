---
layout: default
title: Clomipramine
parent: 高證據等級 (L1-L2)
nav_order: 49
evidence_level: L1
indication_count: 1
---

# Clomipramine
{: .fs-9 }

證據等級: **L1** | 預測適應症: **1** 個
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

# Clomipramine 藥師筆記

## 一句話總結

Clomipramine 是經典的三環抗憂鬱劑，TxGNN 預測其對焦慮症有療效，這與其已知的藥理作用及豐富的臨床證據高度吻合，屬於證據充足的「老藥既有用途」。

---

## 快速總覽

| 項目 | 內容 |
|------|------|
| 藥物名稱 | Clomipramine (可洛米普明) |
| DrugBank ID | DB01242 |
| 台灣商品名 | 倍欣膜衣錠 25 公絲 等多種製劑 |
| 原核准適應症 | 憂鬱症、強迫症、恐懼症、驚懼發作 |
| 預測新適應症 | 焦慮症 (anxiety disorder) |
| 最高預測分數 | 0.999 (anxiety disorder) |
| 證據等級 | L1-L2 (多個 RCT/系統性回顧) |

---

## 為什麼這個預測合理

Clomipramine 的藥理機轉完全支持其對焦慮症的療效：

1. **血清素再吸收抑制**：Clomipramine 是三環抗憂鬱劑中血清素選擇性最高者，其活性代謝物 desmethylclomipramine 則抑制正腎上腺素再吸收
2. **抗焦慮機轉明確**：血清素系統失調是焦慮症的核心病理機轉，增加血清素傳導可改善焦慮症狀
3. **臨床經驗豐富**：Clomipramine 已廣泛用於強迫症 (OCD)、恐慌症等焦慮相關疾患，療效確立

實際上，「焦慮症」的預測反映的是 clomipramine 已知的治療譜系，而非真正的新適應症發現。

---

## 臨床試驗證據

### 代表性臨床試驗

| 試驗編號 | 標題 | 階段 | 狀態 | 主要發現 |
|----------|------|------|------|----------|
| NCT03299166 | Troriluzole 輔助治療 OCD | Phase 2/3 | 已完成 | 評估對 SSRI/clomipramine 反應不佳患者的輔助治療 |
| NCT00004310 | IV vs Oral Clomipramine in OCD | Phase 2 | 狀態不明 | 比較靜脈注射與口服 clomipramine 療效 |
| NCT00466609 | OCD 加強治療策略 | Phase 4 | 已完成 | 比較 fluoxetine + clomipramine vs fluoxetine + quetiapine |
| NCT00074815 | 兒童 OCD 的 SRI 部分反應者治療 | Phase 3 | 已完成 | 認知行為治療可改善 SRI 治療效果 |

**關鍵發現**：多項臨床試驗證實 clomipramine 對強迫症及相關焦慮疾患有效，是 OCD 治療的一線藥物選擇。

---

## 文獻證據

### 系統性回顧與 Meta 分析

| PMID | 標題 | 年份 | 主要結論 |
|------|------|------|----------|
| 38014714 | Pharmacological treatments in panic disorder - network meta-analysis | 2023 | Clomipramine 是恐慌症有效治療選項 |
| 34582562 | Pharmacotherapy for trichotillomania | 2021 | Clomipramine 對拔毛症有效 |
| 27663940 | SSRI and Clomipramine in Pediatric OCD - meta-analysis | 2016 | 確認 clomipramine 對兒童 OCD 有效 |
| 25681005 | OCD: Practical strategies for pharmacological treatment | 2015 | Clomipramine 與 SSRI 為 OCD 一線治療 |

### 臨床指引支持

- **國際 OCD 治療指引**：將 clomipramine 列為與 SSRI 並列的一線藥物治療
- **恐慌症治療指引**：認可 clomipramine 為有效的藥物選擇

---

## 台灣上市資訊

| 許可證字號 | 商品名 | 適應症 | 劑型 | 狀態 |
|------------|--------|--------|------|------|
| 多項許可證 | 倍欣膜衣錠等 | 憂鬱病、強迫症、恐懼症、驚懼發作 | 錠劑/膠囊 | 有效 |

**備註**：台灣核准適應症已包含「恐懼症」及「驚懼發作」，實質上涵蓋了焦慮症的主要類型。

---

## 安全性考量

### 重要警語

1. **心臟毒性**：可能延長 QT 間期，心臟病患者需謹慎使用
2. **抗膽鹼副作用**：口乾、便秘、尿滯留、視力模糊
3. **鎮靜作用**：可能影響駕駛及操作機械能力
4. **過量中毒風險**：三環抗憂鬱劑過量可能致命
5. **年輕人自殺風險**：18-24 歲患者初期治療需密切監測

### 藥物交互作用注意事項

- **MAO 抑制劑**：禁止併用，可能導致血清素症候群
- **CYP2D6 抑制劑**：可能增加 clomipramine 血中濃度
- **中樞神經抑制劑**：加強鎮靜作用
- **抗膽鹼藥物**：加重抗膽鹼副作用

### CYP450 代謝考量

Clomipramine 經由 CYP2C19 及 CYP2D6 代謝。文獻報告 (PMID: 28470111) 顯示，CYP2C19 及 CYP2D6 中間代謝者可能出現顯著升高的藥物血中濃度，建議考慮藥物基因檢測。

---

## 結論與下一步

### 預測評估

| 評估項目 | 結果 |
|----------|------|
| 機轉合理性 | 高 - 血清素/正腎上腺素再吸收抑制對焦慮症有明確療效 |
| 臨床證據 | 充足 - 多項 RCT 及 meta-analysis 支持 |
| 文獻支持 | 強 - 國際指引推薦 |
| 整體證據等級 | **L1-L2 (多個 RCT/系統性回顧)** |

### 臨床建議

1. **已可臨床使用**：Clomipramine 對焦慮相關疾患（特別是 OCD、恐慌症）的療效已獲確認
2. **適應症考量**：台灣核准適應症已涵蓋多種焦慮疾患，符合仿單適應症使用
3. **處方注意事項**：
   - 起始劑量宜低，緩慢調升
   - 監測心電圖，特別是有心臟病史者
   - 注意年輕患者的自殺風險
   - 避免突然停藥

### 結語

此預測驗證了 TxGNN 知識圖譜方法能準確識別藥物的已知治療潛力。Clomipramine 對焦慮症的療效已有堅實的證據基礎，屬於「再發現」而非「新發現」。

---

*本筆記僅供研究參考，不構成醫療建議。任何用藥決策應諮詢專業醫療人員。*

*最後更新：2026-02-11*


---

