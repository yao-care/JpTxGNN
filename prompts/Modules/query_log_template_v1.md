# Query Log Template Module v1

本模組定義資料收集日誌的格式，確保所有查詢過程可追溯。

---

## 1. 目的

每份報告必須附加「資料收集日誌」，用於：
- 證明已執行必要的資料查詢
- 記錄查詢條件與結果
- 支持未來的資料更新與稽核
- 明確標示未查詢項目及原因

---

## 2. 查詢日誌完整模板

```markdown
## 附錄：資料收集日誌

### 查詢總覽
| 統計項目 | 數量 |
|---------|------|
| 已完成查詢 | {N} |
| 未完成查詢 | {N} |
| 找到結果 | {N} |
| 未找到結果 | {N} |

### 詳細查詢記錄

| # | 資料來源 | 查詢日期 | 查詢條件 | 結果狀態 | 結果數量 | 備註 |
|---|---------|---------|---------|---------|---------|------|
| 1 | PMDA 藥品許可證 | {YYYY-MM-DD} | drug_name={name} | ✅ 找到 | {N} 筆 | |
| 2 | PMDA 仿單 | {YYYY-MM-DD} | license_no={no} | ❌ 未找到 | 0 筆 | PDF 不可得 |
| 3 | DrugBank | {YYYY-MM-DD} | drugbank_id={id} | ✅ 找到 | 1 筆 | |
| 4 | ClinicalTrials.gov | {YYYY-MM-DD} | {drug} AND {disease} | ✅ 找到 | {N} 筆 | Phase 2-3 |
| 5 | PubMed | {YYYY-MM-DD} | {drug}[Title] AND {disease} | ✅ 找到 | {N} 筆 | Tier 1-2 |
| 6 | Unified DDI | {YYYY-MM-DD} | {drug} interactions | ⏸️ 未查 | - | 系統未整合 |

### 未查項目說明

| 資料來源 | 未查原因 | 對報告的影響 | 是否為 Blocking |
|---------|---------|-------------|----------------|
| Unified DDI | 系統尚未整合，無法查詢 | 無法完成 DDI 評估 | 🛑 是 |
| EMA SmPC | 非優先來源 | 可用 FDA 暫代 | ⚠️ 否 |
```

---

## 3. 各資料來源查詢格式

### PMDA 藥品許可證
```markdown
| 欄位 | 內容 |
|------|------|
| 資料來源 | PMDA 藥品許可證資料庫 |
| 查詢日期 | {YYYY-MM-DD} |
| 查詢條件 | 藥品名稱 = {name}（英文/中文） |
| 結果狀態 | ✅ 找到 / ❌ 未找到 |
| 結果數量 | {N} 筆許可證 |
| 結果摘要 | {列出許可證號與品名} |
```

### PMDA 仿單
```markdown
| 欄位 | 內容 |
|------|------|
| 資料來源 | PMDA 仿單（PDF） |
| 查詢日期 | {YYYY-MM-DD} |
| 查詢條件 | 許可證號 = {license_no} |
| 結果狀態 | ✅ 取得 / ❌ 未取得 |
| 解析完整度 | 禁忌✅ 警語✅ 孕哺❌ ADR✅ |
| 未取得原因 | {原因，如：PDF 連結失效} |
```

### DrugBank
```markdown
| 欄位 | 內容 |
|------|------|
| 資料來源 | DrugBank |
| 查詢日期 | {YYYY-MM-DD} |
| 查詢條件 | DrugBank ID = {DB00XXX} |
| 結果狀態 | ✅ 找到 / ❌ 未找到 |
| 取得欄位 | MOA✅ Targets✅ Pathways✅ Interactions⚠️ |
```

### ClinicalTrials.gov
```markdown
| 欄位 | 內容 |
|------|------|
| 資料來源 | ClinicalTrials.gov |
| 查詢日期 | {YYYY-MM-DD} |
| 查詢條件 | ({drug}) AND ({disease}) |
| 篩選條件 | Phase: 2-4, Status: Completed/Recruiting |
| 結果狀態 | ✅ 找到 / ❌ 未找到 |
| 結果數量 | {N} 筆（篩選後 {M} 筆） |
| 納入試驗 | {NCT 編號列表} |
```

### PubMed
```markdown
| 欄位 | 內容 |
|------|------|
| 資料來源 | PubMed |
| 查詢日期 | {YYYY-MM-DD} |
| 查詢條件 | {drug}[Title] AND {disease}[Title/Abstract] |
| 篩選條件 | Publication type: RCT/Systematic Review/Meta-Analysis |
| 結果狀態 | ✅ 找到 / ❌ 未找到 |
| 結果數量 | {N} 筆（Tier 1: {N}, Tier 2: {N}） |
| 納入文獻 | {PMID 列表} |
```

### DDI 資料庫
```markdown
| 欄位 | 內容 |
|------|------|
| 資料來源 | {DDInter / Guide to PHARMACOLOGY / DrugBank} |
| 查詢日期 | {YYYY-MM-DD} |
| 查詢條件 | {drug} interactions |
| 結果狀態 | ✅ 完成 / ⏸️ 未查 |
| 結果數量 | {N} 筆 DDI |
| 高風險 DDI | {Major 等級的數量} |
| 未查原因 | {若未查，說明原因} |
```

---

## 4. 查詢結果狀態定義

| 狀態 | 符號 | 定義 |
|------|------|------|
| 找到 | ✅ | 查詢成功且有相關結果 |
| 未找到 | ❌ | 查詢成功但無相關結果 |
| 未查 | ⏸️ | 未執行查詢（需說明原因） |
| 錯誤 | ⚠️ | 查詢失敗（技術問題） |
| 部分 | 🔶 | 僅取得部分資料 |

---

## 5. 未查項目處理

對於每個「未查」項目，必須記錄：

```markdown
### 未查項目：{資料來源}

| 欄位 | 內容 |
|------|------|
| **未查原因** | {具體原因} |
| **對報告的影響** | {哪些章節/欄位受影響} |
| **是否為 Blocking** | 🛑 是 / ⚠️ 否 |
| **替代方案** | {是否有替代來源} |
| **預計補查時間** | {日期或「待系統整合」} |
```

---

## 6. Pre-flight 檢查清單

在產生報告前，必須確認：

```markdown
## Pre-flight Checklist

### 資料來源查核
- [ ] PMDA 許可證查詢完成
- [ ] PMDA 仿單 PDF 下載/解析完成（或標記 Data Gap）
- [ ] DDI 資料庫查詢完成（或標記 Data Gap）
- [ ] ClinicalTrials.gov 查詢完成
- [ ] PubMed 查詢完成
- [ ] DrugBank MOA 查詢完成

### 必要欄位檢核
- [ ] 藥物基本資訊完整（或全部標記 Data Gap）
- [ ] 每個適應症有 ICD-10
- [ ] 每個適應症有證據等級
- [ ] 每個 Data Gap 有解鎖條件

### 一致性檢核
- [ ] Pharmacist Notes 與 Sponsor Notes 欄位狀態一致
- [ ] Evidence Pack JSON 與 Notes 內容一致
- [ ] 所有 Blocking Gap 都有對應補件追蹤項目
```

---

## 7. 版本鎖定與快照

```markdown
## 文件版本資訊

| 項目 | 內容 |
|------|------|
| 文件版本 | v{X.Y} |
| 產生日期 | {YYYY-MM-DD} |
| 資料截止日 | {YYYY-MM-DD} |
| Evidence Pack 版本 | {drug}_v{X}_{date}.json |
| 資料快照目錄 | data/snapshots/{drug}_{date}/ |

### 快照內容
| 檔案 | 大小 | 時間戳 |
|-----|------|-------|
| pmda_query_result.json | {size} | {timestamp} |
| clinicaltrials_query_result.json | {size} | {timestamp} |
| pubmed_query_result.json | {size} | {timestamp} |
| drugbank_query_result.json | {size} | {timestamp} |
```
