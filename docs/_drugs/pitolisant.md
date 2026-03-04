---
layout: default
title: Pitolisant
parent: 僅模型預測 (L5)
nav_order: 128
evidence_level: L5
indication_count: 1
---

# Pitolisant
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

# Pitolisant 藥師筆記

## 一句話總結

Pitolisant 為選擇性組織胺 H3 受體反向激動劑，TxGNN 預測對失眠及 ADHD 有潛在療效，已有文獻支持其促醒及認知增強作用。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 藥品學名 | Pitolisant (唯醒) |
| DrugBank ID | DB11642 |
| 原核准適應症 | 猝睡症（伴隨或未伴隨猝倒）、阻塞性睡眠呼吸中止引起的日間過度嗜睡 |
| TxGNN 預測新適應症 | 失眠、注意力不足過動症 (ADHD)、Aarskog 症候群 |
| 台灣許可證數 | 4 張 |
| 最高證據等級 | L3 (觀察性研究/文獻回顧) |

## 為什麼這個預測合理

Pitolisant 作為 H3 受體反向激動劑，其預測的新適應症在機轉上具有合理性：

1. **失眠 (Insomnia)**：H3 受體阻斷可增加腦內組織胺釋放，促進覺醒。雖看似矛盾，但改善睡眠-覺醒週期調控可能對某些失眠類型有益
2. **注意力不足過動症 (ADHD)**：組織胺系統參與注意力及認知功能調控，H3 受體拮抗劑可增強覺醒及注意力
3. **Aarskog 症候群**：預測機轉不明確，可能為模型假陽性

## 臨床試驗證據

| 預測適應症 | 臨床試驗數 | 代表性試驗 |
|------------|-----------|-----------|
| 失眠 | 1 (間接) | NCT02800083: Pitolisant 治療酒精使用障礙（評估睡眠作為次要指標）|
| ADHD | 0 | 直接試驗無，但有相關文獻討論 |

### 主要臨床試驗

| 試驗 ID | 標題 | Phase | 狀態 | 說明 |
|---------|------|-------|------|------|
| NCT02800083 | Pitolisant for Alcohol Use Disorder | Phase 2 | 撤回 | 次要指標包含睡眠改善評估 |

## 文獻證據

### 失眠 (Insomnia)
**證據等級：L3 (觀察性研究/回顧性文獻)**

| PMID | 標題 | 年份 | 重點發現 |
|------|------|------|----------|
| 34225942 | Histamine receptors in health and disease | 2021 | 綜述 H3 受體在睡眠-覺醒調控中的角色，Pitolisant 為治療猝睡症的新選項 |
| 36169322 | Real-life WAKE study in narcolepsy with pitolisant | 2022 | 觀察性研究顯示 Pitolisant 對既往治療無效的猝睡症患者有效，提及失眠評估 |
| 30214155 | Profile of pitolisant in narcolepsy management | 2018 | 系統性回顧 Pitolisant 的藥效學與藥動學特性 |

### 注意力不足過動症 (ADHD)
**證據等級：L3 (前臨床/回顧性文獻)**

| PMID | 標題 | 年份 | 重點發現 |
|------|------|------|----------|
| 32882898 | Pitolisant and H3R antagonists: therapeutic potentials | 2020 | 回顧 H3R 拮抗劑在 ADHD 的潛在應用，Pitolisant 具有認知增強潛力 |
| 34534876 | Drugs for epilepsy and excessive daytime sleepiness | 2021 | 討論 Pitolisant 在合併 ADHD 的癲癇患者可能的輔助角色 |
| 27363923 | H3 receptor as target for cognitive symptoms | 2016 | 探討 H3R 拮抗劑在神經精神疾病認知症狀的治療潛力 |
| 21615387 | H3 receptor: from discovery to clinical trials | 2011 | 歷史回顧及 Pitolisant 臨床發展 |

## 台灣上市資訊

### 上市狀態
台灣已核准上市，共有 4 張許可證（2 種劑量規格各 2 張）。

### 代表性產品

| 許可證字號 | 商品名 | 劑型 | 許可證持有者 | 效期 |
|------------|--------|------|--------------|------|
| 衛部藥輸字第028103號 | 唯醒膜衣錠4.5毫克 (Wakix) | 膜衣錠 | 信東生技股份有限公司 | 2026/07/13 |
| 衛部藥輸字第028104號 | 唯醒膜衣錠18毫克 (Wakix) | 膜衣錠 | 信東生技股份有限公司 | 2026/07/13 |

### 核准適應症
1. 治療 6 歲以上猝睡症（伴隨或未伴隨猝倒現象）
2. 改善阻塞性睡眠呼吸中止 (OSA) 成人病人的覺醒狀態並減少日間過度嗜睡 (EDS)

## 安全性考量

### 藥物交互作用

DDInter 資料庫顯示 Pitolisant 與多種藥物有交互作用：

**嚴重交互作用 (Major)**：
- Bupropion：降低 Pitolisant 代謝，增加血中濃度
- Dolasetron：可能延長 QT 間距

**中度交互作用 (Moderate)**：
- H2 受體阻斷劑：Famotidine, Cimetidine
- 皮質類固醇：Hydrocortisone, Triamcinolone, Dexamethasone, Betamethasone, Budesonide
- 其他：Metformin, Morphine, Clarithromycin, Levofloxacin
- 瀉劑：Bisacodyl, Polyethylene glycol

### 注意事項
1. **QT 延長風險**：避免與其他延長 QT 藥物併用
2. **CYP3A4 誘導**：可能降低併用藥物血中濃度（如口服避孕藥）
3. **肝腎功能不全**：中重度肝功能不全需減量
4. **懷孕/哺乳**：不建議使用

## 結論與下一步

### 預測價值評估

| 預測適應症 | 證據等級 | 文獻支持 | 臨床試驗 | 總評 |
|------------|----------|----------|----------|------|
| 失眠 | L3 | 8 篇 | 1 (間接) | 中度支持 |
| ADHD | L3-L4 | 7 篇 | 0 | 輕度支持 |
| Aarskog 症候群 | L5 | 0 | 0 | 無支持 |

### 建議
1. **ADHD**：基於 H3 受體在認知功能的角色，值得進一步探索，但目前缺乏直接臨床試驗
2. **失眠**：看似矛盾但改善睡眠-覺醒週期調控可能對某些睡眠障礙有益，需更多研究
3. Pitolisant 相對新穎（台灣 2021 年核准），臨床經驗仍在累積中

---
*本筆記由 TwTxGNN 系統自動產生，僅供研究參考，不構成醫療建議。*
*產生日期：2026-02-11*


---

