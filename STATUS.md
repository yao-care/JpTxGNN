# JpTxGNN 專案狀態記錄

**最後更新**: 2026-03-04 15:00 JST

---

## 已完成功能

### 1. 網站結構 ✅

| 項目 | 狀態 | 說明 |
|------|------|------|
| Jekyll 網站 | ✅ 完成 | https://jptxgnn.yao.care/ |
| 導覽列結構 | ✅ 完成 | 7 個主選單，子頁面正確嵌套 |
| SMART on FHIR | ✅ 完成 | 11 個技術文件頁面 |
| 健康ニュース | ✅ 完成 | 新聞監測頁面 |
| 医薬品レポート | ✅ 完成 | 191 個藥物報告 |
| 安全性データ | ✅ 完成 | 4 個藥物交互作用頁面 |
| リソース | ✅ 完成 | 3 個資源頁面 |
| 説明 | ✅ 完成 | 4 個說明頁面 |

### 2. 藥物報告系統 ✅

| 項目 | 數量 | 說明 |
|------|------|------|
| 總藥物數 | 191 | 從 TwTxGNN 移植 |
| L1 (強證據) | 13 | 多個 RCT / 系統性回顧 |
| L2 (中強證據) | 23 | 單一 RCT / Phase 2 試驗 |
| L3 (初步證據) | 33 | 觀察性研究 |
| L4 (前臨床) | 25 | 前臨床 / 機轉研究 |
| L5 (預測) | 97 | 僅模型預測 |

**關鍵檔案**:
- `docs/_drugs/*.md` - 191 個藥物報告頁面
- `data/notes/*/drug_pharmacist_notes.md` - LLM 評估原始檔
- `scripts/build_docs.py` - 轉換 notes 到 Jekyll 頁面

### 3. 證據等級頁面 ✅

| 頁面 | URL | 內容 |
|------|-----|------|
| 高エビデンスレベル | `/evidence-high/` | L1 + L2 = 36 藥物 |
| 中エビデンスレベル | `/evidence-medium/` | L3 + L4 = 58 藥物 |
| モデル予測のみ | `/evidence-low/` | L5 = 97 藥物 |

### 4. 自動證據檢查 ✅

**Workflow**: `.github/workflows/check-new-evidence.yml`

| 項目 | 設定 |
|------|------|
| 執行時間 | 每日 09:00, 21:00 JST |
| 檢查來源 | ClinicalTrials.gov, PubMed |
| Issue 建立條件 | ≥2 個新項目 |
| Issue 標籤 | `auto-detected`, `needs-review` |

**相關腳本**:
- `scripts/check_clinicaltrials.py` - 檢查新臨床試驗
- `scripts/check_pubmed.py` - 檢查新文獻
- `scripts/extract_drug_list.py` - 提取藥物清單
- `scripts/github_utils.py` - GitHub API 工具

**Cache 檔案**:
- `data/cache/clinicaltrials_cache.json` - 已見臨床試驗
- `data/cache/pubmed_cache.json` - 已見 PubMed 文章

### 5. GitHub Actions ✅

| Workflow | 功能 | 狀態 |
|----------|------|------|
| pages.yml | Jekyll 部署 | ✅ |
| check-new-evidence.yml | 證據檢查 | ✅ |
| link-check.yml | 連結檢查 | ✅ |
| news-monitor.yml | 新聞監測 | ✅ |
| indexnow.yml | 搜尋引擎通知 | ✅ |

---

## 待處理項目

### 優先度高

1. **PMDA 收集器** - `src/jptxgnn/collectors/pmda.py` 尚未實作
   - 目前只有佔位程式碼
   - 需要研究 PMDA API 或網頁爬蟲方式

2. **JPRN 收集器** - `src/jptxgnn/collectors/jprn.py` 尚未實作
   - 日本臨床試驗註冊 (UMIN-CTR, JapicCTI)
   - 需要研究 API 存取方式

### 優先度中

3. **日文藥物報告** - 目前報告內容為繁體中文
   - 可考慮使用 LLM 翻譯
   - 或重新執行評估流程生成日文版

4. **新聞同義詞** - `data/news/synonyms.json`
   - 需要加入日文疾病/藥物同義詞
   - 用於新聞關鍵字匹配

### 優先度低

5. **DL 預測** - 深度學習模型預測
   - 需要 TxGNN conda 環境
   - 需要 `model_ckpt/` 預訓練模型

---

## 常用命令

```bash
# 進入專案目錄
cd /Users/lightman/yao.care/JpTxGNN

# 重新生成藥物頁面
uv run python scripts/build_docs.py

# 本地預覽網站
cd docs && bundle exec jekyll serve

# 手動觸發證據檢查
gh workflow run "Check New Evidence"

# 查看最近的 workflow 執行
gh run list --limit 5

# 查看自動建立的 Issue
gh issue list --label "auto-detected"

# 查看藥物證據等級分布
grep "evidence_level:" docs/_drugs/*.md | sed 's/.*evidence_level: //' | sort | uniq -c
```

---

## 專案結構

```
JpTxGNN/
├── docs/                    # Jekyll 網站
│   ├── _drugs/              # 191 個藥物報告頁面
│   ├── evidence-high.md     # L1-L2 頁面
│   ├── evidence-medium.md   # L3-L4 頁面
│   ├── evidence-low.md      # L5 頁面
│   └── nav-*.md             # 導覽頁面
├── data/
│   ├── notes/               # 191 個 LLM 評估
│   ├── cache/               # 證據檢查 cache
│   └── news/                # 新聞資料
├── scripts/
│   ├── build_docs.py        # 轉換 notes → Jekyll
│   ├── check_clinicaltrials.py
│   ├── check_pubmed.py
│   ├── extract_drug_list.py
│   └── github_utils.py
├── src/jptxgnn/
│   ├── collectors/          # 證據收集器
│   ├── reviewer/            # LLM 評估模組
│   └── writer/              # 報告生成模組
└── .github/workflows/       # GitHub Actions
```

---

## 下次繼續工作

重新開啟 Claude CLI 時，可以說：

```
請閱讀 STATUS.md 了解專案狀態，然後繼續 [具體任務]
```

或者：

```
請查看 JpTxGNN 專案的 STATUS.md，告訴我有哪些待處理項目
```

---

## 相關連結

- 網站: https://jptxgnn.yao.care/
- GitHub: https://github.com/yao-care/JpTxGNN
- Issues: https://github.com/yao-care/JpTxGNN/issues
- TwTxGNN (參考): https://github.com/yao-care/TwTxGNN
