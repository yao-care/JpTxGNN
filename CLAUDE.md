# TxGNN 國際化 SOP - 從初始化包建立地區藥品老藥新用預測系統

## 目標

將此初始化包轉換為您國家的藥品老藥新用預測系統。

**使用方式**：
1. 解壓縮 TxGNN_init.zip
2. 閱讀本文件，按照階段化流程執行
3. 將 `.template` 檔案改名並填入當地資訊
4. 執行預測流程

---

## 一、元件分類總覽

### 1.1 通用元件（直接使用，約 60-70%）

| 類別 | 檔案 | 說明 |
|------|------|------|
| **TxGNN 知識圖譜** | `data/node.csv`, `data/kg.csv` | 知識圖譜基礎資料（需下載） |
| **詞彙表提取** | `scripts/prepare_external_data.py` | 從 TxGNN 提取 DrugBank/疾病詞彙 |
| **藥名正規化** | `src/{country}txgnn/mapping/normalizer.py` | 通用藥名標準化 |
| **DrugBank 映射** | `src/{country}txgnn/mapping/drugbank_mapper.py` | 成分 → DrugBank ID |
| **KG 預測** | `src/{country}txgnn/predict/repurposing.py` | 知識圖譜方法 |
| **DL 預測** | `src/{country}txgnn/predict/txgnn_model.py` | 深度學習方法（見第七節） |
| **通用收集器** | `src/{country}txgnn/collectors/` | 全球資料來源 |
| **收集器基類** | `src/{country}txgnn/collectors/base.py` | 收集器介面 |

### 1.2 需在地化元件（約 30-40%）

| 類別 | 模板檔案 | 需修改內容 |
|------|----------|------------|
| **專案設定** | `pyproject.toml.template` | 專案名稱 |
| **欄位映射** | `config/fields.yaml.template` | 藥監局資料欄位對應 |
| **資料載入** | `src/{country}txgnn/data/loader.py.template` | 載入邏輯 |
| **疾病映射** | `src/{country}txgnn/mapping/disease_mapper.py.template` | DISEASE_DICT（當地語言→英文） |
| **資料處理** | `scripts/process_fda_data.py.template` | ZIP/JSON 解析 |
| **預測腳本** | `scripts/run_kg_prediction.py.template` | 微調欄位名稱 |
| **FHIR 生成** | `scripts/generate_fhir_resources.py.template` | URL 和管轄區域 |
| **新聞同義詞** | `data/news/synonyms.json.template` | 疾病/藥物同義詞 |
| **網站設定** | `docs/_config.yml.template` | 標題、URL |
| **SMART App** | `docs/smart/launch.html.template` | Client ID |
| **CI/CD** | `.github/workflows/pages.yml.template` | 部署設定 |

---

## 二、階段化實施流程

### Phase 0：專案初始化

**目標**：設定專案基礎

#### 步驟：

1. **重新命名專案**
   ```bash
   # 建議命名：{Country}TxGNN
   # 例：JpTxGNN, KrTxGNN, ThTxGNN
   mv TxGNN_init {Country}TxGNN
   cd {Country}TxGNN
   ```

2. **設定 pyproject.toml**
   ```bash
   mv pyproject.toml.template pyproject.toml
   # 編輯 pyproject.toml，修改 name 和 description
   ```

3. **下載 TxGNN 資料**
   ```bash
   mkdir -p data
   curl -L -o data/node.csv "https://dataverse.harvard.edu/api/access/datafile/7144482"
   curl -L -o data/kg.csv "https://dataverse.harvard.edu/api/access/datafile/7144484"
   ```

4. **安裝依賴**
   ```bash
   uv sync
   ```

**品質檢查點**：
- [ ] 專案已重新命名
- [ ] `pyproject.toml` 已修改
- [ ] `uv sync` 執行成功
- [ ] TxGNN 資料下載完成（node.csv ~15MB, kg.csv ~500MB）

---

### Phase 1：FDA 資料整合

**目標**：整合當地藥監局資料

#### 1.1 調查資料來源

常見藥監局資料來源：

| 國家 | 藥監局 | 資料來源 |
|------|--------|----------|
| 日本 | PMDA | https://www.pmda.go.jp/ |
| 韓國 | MFDS | https://nedrug.mfds.go.kr/ |
| 泰國 | Thai FDA | https://www.fda.moph.go.th/ |

**產出**：記錄資料來源 URL、格式、欄位說明

#### 1.2 建立欄位映射設定

```bash
mv config/fields.yaml.template config/fields.yaml
# 編輯 fields.yaml，填入欄位對應
```

**fields.yaml 範例（日本 PMDA）**：
```yaml
country_code: JP
language: ja
regulatory_agency: PMDA

field_mapping:
  license_id: "承認番号"
  brand_name_local: "販売名"
  brand_name_en: "一般名"
  ingredients: "有効成分"
  indication: "効能・効果"
  dosage_form: "剤形"
  status: "承認状況"

withdrawn_statuses:
  - "取消"
  - "回収"
```

#### 1.3 實作資料載入器

```bash
mv src/{country}txgnn/data/loader.py.template src/{country}txgnn/data/loader.py
# 編輯 loader.py，實作載入邏輯
```

#### 1.4 實作資料處理腳本

```bash
mv scripts/process_fda_data.py.template scripts/process_fda_data.py
# 編輯並執行
uv run python scripts/process_fda_data.py
```

**品質檢查點**：
- [ ] `config/fields.yaml` 建立完成
- [ ] `loader.py` 能正確載入資料
- [ ] `process_fda_data.py` 執行成功
- [ ] `data/raw/{country}_fda_drugs.json` 產生

---

### Phase 2：疾病映射

**目標**：建立當地語言 → 英文疾病對照

#### 2.1 建立 DISEASE_DICT

```bash
mv src/{country}txgnn/mapping/disease_mapper.py.template src/{country}txgnn/mapping/disease_mapper.py
# 編輯 disease_mapper.py，填入 DISEASE_DICT
```

**目標數量**：150-200 個疾病詞條

**分類建議**：

| 分類 | 建議數量 |
|------|----------|
| 心血管系統 | 15-20 |
| 呼吸系統 | 10-15 |
| 消化系統 | 15-20 |
| 神經系統 | 10-15 |
| 精神疾病 | 8-12 |
| 內分泌系統 | 10-15 |
| 肌肉骨骼 | 10-15 |
| 皮膚疾病 | 10-15 |
| 泌尿系統 | 8-12 |
| 眼科 | 5-8 |
| 耳鼻喉 | 5-8 |
| 感染症 | 10-15 |
| 過敏 | 5-8 |
| 婦科 | 8-12 |
| 腫瘤/癌症 | 10-15 |
| 一般症狀 | 15-20 |

#### 2.2 建立新聞同義詞

```bash
mv data/news/synonyms.json.template data/news/synonyms.json
# 編輯 synonyms.json，填入當地語言同義詞
```

**品質檢查點**：
- [ ] DISEASE_DICT 有 150+ 詞條
- [ ] 涵蓋所有主要疾病分類
- [ ] `synonyms.json` 建立完成

---

### Phase 3：KG 預測流程

**目標**：執行知識圖譜預測

#### 執行步驟：

```bash
# 1. 準備詞彙表
uv run python scripts/prepare_external_data.py

# 2. 設定預測腳本
mv scripts/run_kg_prediction.py.template scripts/run_kg_prediction.py
# 編輯並執行

# 3. 執行預測
uv run python scripts/run_kg_prediction.py
```

#### 預期產出：

| 檔案 | 預期內容 |
|------|----------|
| `data/external/drugbank_vocab.csv` | ~7,958 個藥物 |
| `data/external/disease_vocab.csv` | ~17,081 個疾病 |
| `data/external/drug_disease_relations.csv` | ~80,127 個關係 |
| `data/processed/repurposing_candidates.csv` | 視藥品數量而定 |

**品質檢查點**：
- [ ] 詞彙表正確產生
- [ ] `repurposing_candidates.csv` 產生
- [ ] DrugBank 映射率 > 30%
- [ ] 疾病映射率 > 20%

---

### Phase 4：網站與 FHIR

**目標**：部署文件網站與 FHIR API

#### 4.1 Jekyll 設定

```bash
mv docs/_config.yml.template docs/_config.yml
# 編輯 _config.yml，修改標題、URL、語言
```

#### 4.2 FHIR 資源設定

```bash
mv scripts/generate_fhir_resources.py.template scripts/generate_fhir_resources.py
# 編輯 BASE_URL 和 JURISDICTION
uv run python scripts/generate_fhir_resources.py
```

#### 4.3 SMART App 設定

```bash
mv docs/smart/launch.html.template docs/smart/launch.html
# 編輯 CLIENT_ID
```

#### 4.4 本地測試

```bash
cd docs
bundle install
bundle exec jekyll serve
# 訪問 http://localhost:4000
```

**品質檢查點**：
- [ ] Jekyll 本地建置成功
- [ ] `/fhir/metadata` 可存取
- [ ] FHIR 資源正確產生

---

### Phase 5：證據收集

**目標**：設定證據收集器

#### 5.1 建立當地 FDA 收集器

建立 `src/{country}txgnn/collectors/{country}fda.py`：

```python
from .base import BaseCollector, CollectorResult

class {Country}FDACollector(BaseCollector):
    source_name = "{country}fda"

    def search(self, drug: str, disease: str | None = None) -> CollectorResult:
        # 實作搜尋邏輯
        pass
```

#### 5.2 區域臨床試驗註冊

ICTRP 涵蓋的區域註冊：
- 日本：JPRN (UMIN-CTR, JapicCTI)
- 韓國：CRIS
- 泰國：TCTR

**品質檢查點**：
- [ ] 當地 FDA 收集器建立
- [ ] ClinicalTrials.gov 收集器正常
- [ ] PubMed 收集器正常

---

### Phase 6：新聞監測

**目標**：設定健康新聞監測

#### 6.1 設定關鍵字模式

建立 `scripts/generate_news_keywords.py`，參考 TwTxGNN 版本。

#### 6.2 新增當地新聞來源

建立 `scripts/fetchers/{country}_news.py`

**品質檢查點**：
- [ ] `keywords.json` 產生
- [ ] 新聞爬蟲正常運作

---

### Phase 7：驗證與部署

**目標**：端對端驗證並部署

#### 7.1 設定 GitHub Actions

```bash
mv .github/workflows/pages.yml.template .github/workflows/pages.yml
# 編輯部署設定
```

#### 7.2 完整流程測試

```bash
uv run python scripts/process_fda_data.py
uv run python scripts/prepare_external_data.py
uv run python scripts/run_kg_prediction.py
uv run python scripts/generate_fhir_resources.py
```

#### 7.3 品質指標

| 指標 | 台灣參考值 | 目標 |
|------|-----------|------|
| FDA 藥品總數 | 71,552 | 記錄 |
| 有效藥品比例 | 33% | > 20% |
| DrugBank 映射率 | 73.87% | > 50% |
| 疾病映射率 | 44.85% | > 30% |
| 預測候選數 | 142,328 | 記錄 |

**品質檢查點**：
- [ ] 端對端流程通過
- [ ] GitHub Pages 部署成功
- [ ] SMART App 可從 SMART Launcher 啟動

---

## 三、關鍵檔案詳解

### 3.1 `config/fields.yaml`

欄位映射設定檔，定義藥監局資料欄位與標準欄位的對應關係。

### 3.2 `src/{country}txgnn/data/loader.py`

資料載入器，根據 `fields.yaml` 載入並過濾藥品資料。

### 3.3 `src/{country}txgnn/mapping/disease_mapper.py`

疾病映射模組，包含 `DISEASE_DICT`（當地語言→英文對照表）。

### 3.4 `scripts/process_fda_data.py`

資料處理腳本，將原始資料轉換為標準 JSON 格式。

---

## 四、GitHub Actions 設定

### 需設定的 Workflow：

| Workflow | 功能 | 需修改 |
|----------|------|--------|
| `pages.yml` | Jekyll 部署 | URL |
| `link-check.yml` | 連結檢查 | 無 |
| `check-new-evidence.yml` | 證據檢查 | 無 |

### 需設定的 Secrets：

| Secret | 用途 |
|--------|------|
| `GITHUB_TOKEN` | 自動提供 |
| `NCBI_API_KEY` | PubMed API（可選，提高速率限制） |

---

## 五、驗證清單

### 總體完成檢查

- [ ] Phase 0：專案初始化完成
- [ ] Phase 1：FDA 資料整合完成
- [ ] Phase 2：疾病映射完成
- [ ] Phase 3：KG 預測完成
- [ ] Phase 4：網站與 FHIR 完成
- [ ] Phase 5：證據收集完成
- [ ] Phase 6：新聞監測完成
- [ ] Phase 7：驗證與部署完成

### YMYL 檢查（醫療內容必檢）

- [ ] 免責聲明：「僅供研究參考，不構成醫療建議」
- [ ] 預測結果標註：「需經臨床驗證」
- [ ] 資料來源標註完整

---

## 六、附錄：區域特殊考量

### 日本 (PMDA)
- 資料格式：可能有 Shift-JIS 編碼
- 藥名：漢字/平假名/片假名混用
- 臨床試驗：JPRN (UMIN-CTR, JapicCTI, JMACCT)

### 韓國 (MFDS)
- 資料格式：UTF-8
- 藥名：韓文 + 英文音譯
- 臨床試驗：CRIS

### 泰國 (Thai FDA)
- 資料格式：UTF-8
- 藥名：泰文 + 英文
- 臨床試驗：TCTR

### 常見挑戰

1. **成分名稱變異**：同一藥物可能有不同鹽類形式
2. **品牌名映射**：當地品牌名需對應到國際名稱
3. **適應症文字解析**：不同語言的標點符號慣例不同
4. **日期格式**：各地區日期格式不同
5. **狀態碼**：有效/註銷的術語不同

---

## 常用命令

```bash
# 安裝依賴
uv sync

# 處理 FDA 資料
uv run python scripts/process_fda_data.py

# 準備詞彙表資料
uv run python scripts/prepare_external_data.py

# 執行知識圖譜預測
uv run python scripts/run_kg_prediction.py

# 生成 FHIR 資源
uv run python scripts/generate_fhir_resources.py

# 本地測試網站
cd docs && bundle exec jekyll serve

# 執行測試
uv run pytest tests/ -v
```

---

## 七、兩種預測模式

本專案支援兩種老藥新用預測方法：

### 7.1 KG 預測（知識圖譜）

| 項目 | 說明 |
|------|------|
| 檔案 | `src/{country}txgnn/predict/repurposing.py` |
| 方法 | 直接查詢 TxGNN 知識圖譜中已知的藥物-疾病關係 |
| 依賴 | 無額外依賴，使用 pandas 即可 |
| 速度 | 快（數分鐘） |
| 輸出 | 來源標記為 `TxGNN Knowledge Graph` |

**執行方式**：
```bash
uv run python scripts/run_kg_prediction.py
```

### 7.2 DL 預測（深度學習）

| 項目 | 說明 |
|------|------|
| 檔案 | `src/{country}txgnn/predict/txgnn_model.py` |
| 方法 | 使用 TxGNN 深度學習模型預測藥物-疾病關聯分數 |
| 依賴 | PyTorch, DGL, TxGNN 套件（需 conda 環境） |
| 速度 | 慢（CPU 數小時，GPU 較快） |
| 輸出 | 包含信心分數 (0-1)，來源標記為 `TxGNN Deep Learning Model` |

**額外資料需求**：
- `data/edges.csv` - TxGNN 邊資料
- `model_ckpt/model.pt` - 預訓練模型

若已有 TwTxGNN，可直接複製：
```bash
cp /path/to/TwTxGNN/data/edges.csv data/
cp -r /path/to/TwTxGNN/model_ckpt .
```

**執行方式**：
```bash
source ~/miniforge3/bin/activate txgnn
cd /path/to/JpTxGNN
PYTHONPATH=src python -m jptxgnn.predict.txgnn_model
```

**參數選項**：
- `--min-score 0.5` - 只保留分數 > 0.5 的結果
- `--top-k 100` - 每個藥物保留前 100 個疾病
- `--restart` - 忽略之前進度，重新開始

**中斷續算**：DL 預測支援中斷續算，每處理完一個藥物會儲存 checkpoint，重新執行會自動跳過已處理的藥物。

### 7.3 兩種方法的差異

| 比較項目 | KG 預測 | DL 預測 |
|----------|---------|---------|
| 資料來源 | 已知關係 | 模型推論 |
| 能發現新關係 | 否 | 是 |
| 有信心分數 | 否 | 是 |
| 執行速度 | 快 | 慢 |
| 環境需求 | 簡單 | 需 conda + GPU/CPU |

**建議**：先執行 KG 預測取得基礎結果，再執行 DL 預測補充潛在候選。兩者結果可合併。

---

## 八、重要經驗教訓

### 8.1 套件命名衝突

**問題**：本地套件名稱 `txgnn` 會與安裝的 TxGNN 套件衝突，導致 `from txgnn import TxData, TxGNN` 匯入錯誤。

**解決方案**：本地套件必須使用國家代碼命名，例如：
- 日本：`jptxgnn`
- 台灣：`twtxgnn`
- 韓國：`krtxgnn`

**需修改的檔案**：
1. 重新命名目錄：`src/txgnn/` → `src/{country}txgnn/`
2. `pyproject.toml` 中的 `packages = ["src/{country}txgnn"]`
3. 所有 `from txgnn import` → `from {country}txgnn import`
4. **例外**：`txgnn_model.py` 中匯入外部 TxGNN 套件的程式碼要保持 `from txgnn import TxData, TxGNN`

### 8.2 Conda 環境路徑

不同系統的 conda 可能安裝在不同位置：
- miniconda3: `~/miniconda3/bin/activate`
- miniforge3: `~/miniforge3/bin/activate`
- anaconda3: `~/anaconda3/bin/activate`

啟動環境前需確認正確路徑：
```bash
# 查找 conda 位置
ls ~/miniconda3/bin/conda 2>/dev/null || ls ~/miniforge3/bin/conda 2>/dev/null

# 列出可用環境
~/miniforge3/bin/conda info --envs
```

### 8.3 DGL 不支援 Apple MPS

DGL (Deep Graph Library) 目前不支援 Apple Silicon 的 MPS 加速，在 Mac 上只能使用 CPU 模式。預測會較慢但功能正常。

---

## 注意事項

- 本專案結果僅供研究參考，不構成醫療建議
- 老藥新用候選需經過臨床驗證才能應用
- 所有網站頁面需包含 YMYL 免責聲明

---

## 藥物頁查核機制（2026-11-12 起）

用戶 2026-11-12 決定：30 站各有自己的查核機制，核心流程比照 TwTxGNN（Tw 的 CLAUDE.md「藥物頁人工查核紀錄」「藥物頁許可證表與張數」兩節）；
UsTxGNN 是第一個試做站（做法見 UsTxGNN/CLAUDE.md 同名一節）。本站的規則與程式都在本 repo，頁面文字用日文，依據是医薬品マスター（薬価基準収載品目；事實層只涵蓋收載品目）與 PMDA。
本站的在地字樣、頁首規則細節、歷史刪改的提交清單集中在 `src/jptxgnn/regulatory/site.py`。

| 環節 | 本站檔案 | 說明 |
|------|----------|------|
| 查核紀錄 | `docs/_data/drug_reviews.json` | 單一真實來源，欄位同 Tw（correct／annotate／rereview／rereview_result／header_level／description_level、history、status） |
| 套用 | `scripts/apply_drug_reviews.py` | 套到 `docs/_drugs/*.md`：查核框 `<!-- review:begin id -->`、每頁在免責聲明前的查核紀錄表；可重複執行；`--check` 只檢查、`--touch` 連 last_modified_at 一起改 |
| 頁首等級 | `src/jptxgnn/regulatory/page_format.py` | 頁首＝快速總覽「エビデンスレベル」格的**第一個**等級（主預測；2026-11-12 實測 296 頁全部符合，不照 Tw 整格取最高）；頁首已是 N/A 的頁不重算；列表頁標題沒有等級範圍，parent 依檔名對應（evidence-high＝L1–L2、medium＝L3–L4、low＝L5）。「日本での販売名」區塊（brand-names）是受管區塊，查核框不插進去 |
| 撤回預測 | `src/jptxgnn/regulatory/withdrawn.py` | verdict=withdraw 的預測不進證據監測（`scripts/extract_drug_list.py`）、搜尋索引與 FHIR（母目錄 `.claude/rebuild_search_index.py`、`.claude/sync_fhir_levels.py` 會讀本站這支） |
| 許可證 | `snapshots/jp_licenses.json.gz`、`scripts/build_license_snapshot.py`、`src/jptxgnn/regulatory/licenses.py` | 快照存本藥許可證號與事實層；gate 依快照驗市場段落表格的許可證號屬於本藥、狀態列與張數列＝事實層寫法、表格列狀態不跟事實相反（本站沒有程式產生的許可證表，不驗表格列內容） |
| 刪改轉紀錄 | `scripts/reviews_from_edits.py` | 依 git 前後版本（或改寫前後目錄）把正文刪改轉成 correct 紀錄 |
| 待查清單 | `docs/_data/drug_reviews_uncertain.json`、`scripts/check_original_indications.py` | 原適應症交叉驗證與待重審項目；證據包沒有許可證適應症文字時照實回報可比對 0 頁 |
| gate | `scripts/check_seo_docs.py` 最後 4 項 | 紀錄都已套用、許可證＝快照、頁首＝快速總覽等級、撤回預測沒有對外發布 |

原則（同 Tw）：基本事實照主管機關資料更正；模型預測原文不刪不改寫，只加註；證據等級與決策只經重審（rereview → rereview_result）變更。

改頁之後要跑：

```bash
python3 scripts/apply_drug_reviews.py          # 重套查核紀錄（sync_notes_to_docs.py、每週排程結尾都會自動跑）
python3 scripts/build_license_snapshot.py --ws <工作目錄>   # 證據包或事實層變了才要（每週排程會自動跑）
python3 scripts/check_seo_docs.py              # 必須 exit 0
```

2026-10-31～11-06 依新事實直接刪掉的矛盾子句，2026-11-12 已用 `scripts/reviews_from_edits.py --git` 轉成 215 筆紀錄（148 頁）。
`scripts/sync_notes_to_docs.py` 依 notes 重寫整頁後會重套紀錄，notes 裡的舊錯句會被紀錄再更正一次。

2026-11-12 正文許可狀態對事實層掃描：5 頁（bimatoprost、dapagliflozin、tocilizumab、lorazepam、droxidopa）在 11 月 AI 重產時照證據包（local_regulatory 全標 Cancelled only，狀態對應壞掉）寫成「取消済み／市販が取り消されている」，bundle 與事實層都是「有効」；以 5 筆 `jp-lic-20261112-*` 紀錄更正（能照事實改的改成「有効」，整條建立在錯誤前提上的次步驟條目刪除）。
2026-11-12 表格列狀態對事實層（母目錄 `check_drug_page.py --row-status`）：ethosuximide 620006918（表格寫「失効」）、istradefylline 622245801（表格寫「取消済み」）在医薬品マスター與證據包 pmda.records 都是「有効」；以 `jp-row-20261112-*` 刪掉狀態註記。

## 新資料查不到的許可證（2026-11-17）

11-16 每週排程「新資料查不到」431 張（證據包 4,755 張的 9.1%；本站門檻 85% 所以沒開 issue）。本站的號碼是医薬品マスター的医薬品コード（9 碼レセ電コード，不是承認番号），
主檔只收薬価基準収載品目，コード在廃止年月日（経過措置期間満了）過後就從全件ファイル消失——所以這是「薬価基準から削除」，不是承認取消（承認情報不在這份資料裡）。
2026-11-17 用戶要求確認實際狀態：下載同一頁上的全件ファイル（2026-03-05／03-12／03-17／03-19／11-12）、改定分ファイル（2026-04-14～11-12 共 13 份）與令和8年度経過措置一覧逐號比對，
431 張全部有主檔自己記錄的廃止年月日：340 張 2026-03-31（03-05／03-12 全件標変更区分 9；其中 141 張 02-19 版就已記経過措置 20260331）、91 張 2026-09-30（09-11 改定分＋経過措置一覧「製薬会社において製造中止又は販売名変更を行った商品名医薬品」）；
91 張在経過措置一覧記有收載中的後継コード（販売名變更等，status 一併寫出），340 張主檔沒記後継コード。沒有找到「其實還在別份現行清單上」的號，也沒有判斷不了的號。
- `scripts/license_adapter.py`：fetch() 另收集主檔的廃止紀錄（HAISHI）、最新全件的コード記成 CURRENT（少於 15,000 或任一份下載失敗就不判定）；preprocess 對不在 CURRENT 且廃止年月日已過的コード標
  `license_status: cancelled`＋`yakka_deleted`（廃止日）＋`ssk_not_listed`（第一次發現日），status 改「薬価削除（YYYY-MM-DD[、後継コード N]）」（原值存 `status_before_yakka_deleted`），又出現在全件就還原；
  主檔沒有廃止紀錄的不推定。`confirmed_absent()` 讓排程把這些列成「主管機關現行清單確認已不列」，不算「查不到」。
- 後継コード補收（同日）：91 張有後継コード的薬価削除コード中，43 張的後継コード（共 34 個コード）不在某些同一個證據包（含 22 個有藥物頁的證據包），有效張數少算。
  本站沒有依成分重建證據包的程式，改由 `scripts/license_adapter.py` 的 preprocess 依最新全件ファイル那一列補一筆紀錄（欄位照 `scripts/convert_ssk_to_json.py` 的轉法，記 `yakka_successor_of`、`source`；收齊的證據包 total_matches 同步加），
  每週排程會跟著做。ネオレスタミンコーワ散１％（620008671，クロルフェニラミン製劑，當初依片假名子字串誤收進 diphenhydramine 等證據包）的後継コード不補（NO_SUCCESSOR）。
  238 個證據包補 377 筆；21 頁狀態列／張數列由排程同步（例：sertraline 有効 14→17 件以上、pitavastatin 16→19 件以上），都是部分收錄頁，正文沒有因此變成矛盾的句子。
- 頁面照「薬価削除」寫，不寫承認取消：母目錄 check_drug_page.py 加 JP 的 SCOPE_CANCELLED（全部削除的頁狀態列＝「薬価基準収載品目なし（…すべて薬価基準から削除済み、国内の承認状況は未確認）」，troxipide 1 頁），
  ja 的 all_valid 排除「有効性」（loperamide 的「いずれも有効性を支持するものではありません」不是承認狀態）；本站 tools/txgnn 同步同一份。
- 160 頁狀態列／張數列、25 格許可證表狀態格照事實層同步；正文寫「N 件すべて有効」而相反的 50 頁以 63 筆 `jp-lic-20261117-*`、表格列寫有効（troxipide 寫「取消」）的 10 列以 `jp-row-20261117-*` 更正
  （注記：薬価基準からの削除は承認の取消しを意味しない）。

## 作用機轉段的資料來源與查核機制（2026-11-19）

用戶 2026-11-19 決定把 NZTxGNN 同日的作法推到各站（seo-ops 轉交：搜「<藥名> mechanism of action」落在藥物頁排名 30–99，因為頁面寫「作用機轉資料不可得」）。
2026-11-19 量測：本站公開藥物頁（排除 noindex、轉址頁）有 272 頁在正文章節寫這種句子（證據包 drugbank.source＝vocab_only、沒有作用機轉文字，AI 照實寫「沒有資料」；本站最常見的寫法：「現在、詳細な作用機序データはありません。」）。
作用機轉是藥物本身的基本藥理事實、不是模型預測，所以照查核機制補：每段都節錄官方仿單或資料庫原文、附可點的出處與取用日期，不自己寫。

- 來源（理由同 NZTxGNN/CLAUDE.md 同名一節）：美國 FDA 核准仿單（openFDA drug label，連結到 NLM DailyMed 同一份 SPL setid；FDA 仿單是美國政府公開資料），美國沒有仿單時用 ChEMBL drug mechanism 表（CC BY-SA 3.0）；證據包的 DrugBank 欄位只有 vocab，DrugBank 文字授權也不允許轉載，不用。
  2026-11-19 這次用 openFDA 的 drug label 全量下載檔（download.open.fda.gov，同一批資料，只留 human prescription 仿單；`--fda-bulk <目錄>`），不吃 API 每日 1,000 次配額；之後少量重跑可直接用 API（不給 `--fda-bulk`）。快取目錄各站共用。
- `scripts/build_mechanism_reviews.py --cache <目錄> [--fda-bulk <目錄>]`：掃公開頁正文章節（排除結論／下一步的待辦、安全性、摘要、總覽表、查核紀錄、免責聲明等）裡同時有「作用機轉」「資料」「沒有」字樣的短句（本站語言的字樣在檔內 L 的 KW／DATA／NEG／EXCL）→ 依 front matter monitor_inn（INN 另對 USAN，表在 US_NAME）查 openFDA，選仿單規則同 NZ：只用單一成分、主成分名（去鹽類；酯類要相同）跟本頁相同的處方藥仿單；排序全身給藥→節錄夠長→有 12.1→有品牌名→版本新；美國只有複方仿單的只節錄 12.1 裡講本藥成分的句子並寫明是複方；節錄照原文 2～4 句、不改寫。
  紀錄寫進 `docs/_data/drug_reviews.json`（action＝mechanism，id `jp-moa-<日期>-<藥>-1`，sources 附 url、accessed、excerpt、label_version、section、set_id 或 chembl_id）；仿單與 ChEMBL 都沒有的，列進 `docs/_data/drug_reviews_uncertain.json`（source＝mechanism of action，附原因）。已有紀錄或已列待查的頁不重抓。`--list` 只列仍寫「不可得」的頁。
- 替換句格式：本站語言（日本語）的出處句＋節錄的忠實翻譯（標明「非官方翻譯」）＋英文原文（照引、為準）＋DailyMed 連結、仿單版本、取用日期（用戶 2026-11-19 決定「當地語言摘要＋英文原文」）。只換「不可得」那一句（英文站句首子句後接 so／but 的後半句是 AI 推論，保留），不加框；查核紀錄表列原句與出處。模型預測與其他正文不動。
- 翻譯：節錄的翻譯是 AI 輔助的忠實翻譯（不增不減，藥名、基因與受體符號、數字、「[…]」照原文），2026-11-19 批次產生，存在紀錄 sources 的 translation（translation_lang、translation_note 註明非官方、英文原文為準）；頁面上同時列英文原文。`--translations <檔>` 讀翻譯、`--need <檔>` 列出還沒翻的節錄（這些頁那次不寫紀錄，gate 會擋，翻好再跑）。
- 2026-11-19 結果：249 頁寫入紀錄（美國仿單 226、ChEMBL 23），23 頁列待查（美國沒有單一成分處方藥仿單、仿單段落不是作用機轉，且 ChEMBL 沒有已核准分子的機轉紀錄；多是胺基酸、維生素、礦物質、賦形劑、生物製劑或只在別國上市的藥）。
- `scripts/apply_drug_reviews.py` 支援 mechanism；gate 第 21 項（`scripts/check_seo_docs.py`，函式在 build_mechanism_reviews.gate_errors）：公開頁仍寫「不可得」、既沒有 mechanism 紀錄也沒列待查的，擋下；有紀錄沒套上的由查核紀錄那一項擋。
- 注意：節錄的是美國仿單，劑型與適應症可能跟本站市場的產品不同（例如取到外用仿單）；文字上已寫明是美國 FDA 核准仿單。`sync_notes_to_docs.py` 整頁重寫後會重套紀錄（claim 是頁面原句）；報告重產、原句改寫後要再跑 build_mechanism_reviews.py。
- 2026-11-20 補做：程式更新：同頁不只一句「不可得」時每句各一筆紀錄（-1、-2…）；同頁別筆紀錄的更正文字、錨點與已套上的節錄不再當成「不可得」句；gate 改成公開頁仍寫「不可得」、又沒列待查就擋（不再只看該頁有沒有紀錄）；ChEMBL 譯文（詞組清單）後補句號 23 筆；同 id 重發，前版 replacement 存 history。
- 2026-11-20 試跑母目錄「交付前驗證」規則時補做：偵測改成原條件不動、另加新增寫法（L2，比中的再用 NOT 排除以缺資料為前提的模型推論），字樣用獨立、更寬的偵測全量掃出的候選句逐句標註校準（A 沒有漏、B 沒有誤中）；節錄後面接著 AI 說明「上面描述依據」的句子（會讀成美國仿單的出處）1 筆改成那句在節錄前（原文不改，只換順序）；以上同 id 重發，前版存 history。程式另加 reorder_src_tail、同頁已引用同一段節錄時改指向上方（產生器 txgnn/.claude/moa_rollout_20261119/fix_20261120/）。

## 說明頁與證據等級頁的在地資料（2026-11-19）

用戶 2026-11-19 決定的第一批改版（母目錄 `.claude/gen_local_pages_20261119.py` 產生，不逐站手改）：說明頁（about／guide／sources／downloads／methodology，自有結構站只有證據等級頁與隱私頁）加本站資料區塊（`<!-- local-facts -->`）、證據等級頁的事實段與藥名表（`<!-- tier-facts -->`、`<!-- tier-table -->`）、隱私頁的適用法律／權利／著作權與資料來源段（`<!-- privacy-law -->`）；en／es／de 樣板站的共用長段落縮成一段（`<!-- local-condensed -->`）。
資料檔 `docs/_data/local_facts.json`、`docs/_data/evidence_tier_facts.json` 由 `scripts/local_facts.py`（＝母目錄 `.claude/local_facts_lib.py`）依藥物頁、許可證快照、查核紀錄、FHIR 算；`apply_drug_reviews.py`、許可證快照程式結尾會自動 `--write`，`check_seo_docs.py` 跑 `--check` 擋過期。跨站欄位（cross：本站獨有預測、30 站中位數）與頁面區塊只由母目錄產生器更新；藥物頁改等級、noindex 或預測後要在母目錄重跑。

## 藥物頁 description 句尾在地化（2026-11-19）

用戶 2026-11-19 決定（「藥物頁簡述在地化」，SEO 工具判定 30 站藥物頁近似重複，原因之一是 description 句尾都是同一句「原適應症：本地資料未記載」）：公開藥物頁（排除 noindex、轉址頁）front matter description 句尾的「既存適応症：日本の承認情報に適応症の記載なし」換成本站許可證快照事實層（`snapshots/*_licenses.json.gz`，經 `src/*/regulatory/licenses.py` 的 snapshot()）的品項數句子，資料名稱照本站口徑：薬価基準の品目（現在収載；不寫承認）。藥名、預測新適應症、等級字樣不動（母目錄 sync_description_levels.py 照舊對得到）；已有原適應症原文的頁不動。
例：abatacept「既存適応症：日本の承認情報に適応症の記載なし」→「薬価基準の品目：3 件（現在収載 3 件）」；2026-11-19 改了 129 頁。
由母目錄 `.claude/drug_meta_description.py --apply --site JpTxGNN` 產生（站上複本 `tools/txgnn/.claude/drug_meta_description.py --apply --root .`），改動記在 `docs/_data/description_local_log.json`（pages＝目前句尾與原字樣、entries＝每次改動前後整行，可還原）。快照數字變了重跑會換新數字；`apply_drug_reviews.py`、`build_license_snapshot.py` 結尾會自動 --apply，`check_seo_docs.py` 跑 --check 擋「還是未記載句尾」或「數字跟快照不符」。只改 front matter，lastmod_fix 不算正文改動、last_modified_at 不動。
同日修：`apply_drug_reviews.py`、`build_license_snapshot.py` 結尾重算 local_facts 的 atexit 掛鉤在結束時取不到 `__file__`（NameError，之前其實沒跑成），改成先算好路徑。

## 許可證表與正文件數由程式維護（2026-11-24）

用戶 2026-11-24 決定（各站同日，第二波）：每週許可證排程只改得到概覽表狀態列／張數列，市場段落 AI 寫的自由格式許可證表（「| 承認番号 | 商品名 | 剤形 | 承認適応症 |」；號碼其實是医薬品マスターの医薬品コード，適応症欄是 AI 依 KEGG 寫的）與正文寫死的件數跟著医薬品マスター（薬価削除）過期、checker 擋頁；改成程式產生、每週自動同步。
- A. `scripts/sync_license_tables.py`：「## 日本市販情報」段落的第一張表換成程式依證據包 pmda.records 產生的表「| 医薬品コード | 医薬品名・規格名 | 状態 |」（欄位照医薬品マスター原文，名稱＝漢字名称；狀態＝有効／薬価削除（YYYY-MM-DD[、後継コード N]），照證據包 status，不寫取消）。
  選列照換表當時原表依序列出的医薬品コード（`config/license_table_pins.json`，327 頁；正文「上記は主要な 5 件」「残りの…」才對得上），其餘有効在前；列數＝原表列數（最多 20），沒有表的頁補 min(5, 總數) 列；
  總數多於列數時表下「上表はデータ上の M 件のうち N 件です。」，證據包只收一部分時「データには承認の一部のみが含まれています。上表はそのうち N 件です。」；known_use_pages 舊程式表的部分紀錄註記一併拿掉。
  前後 `<!-- licenses:begin/end -->`；快照存 rows／nrows／tpart／mix（單剤／配合剤依品名「配合」，事實層 single_total 每張都算單剤）；gate 第 18 項（licenses.py program_block_problems）擋程式區塊≠快照重算、市場段落有程式區塊以外的表。
  接上：`scripts/license_adapter.py` 的 `sync_tables`＋`PAGE_NOTE`（每週排程重排、3b 放行說明句）、`scripts/build_license_snapshot.py` 結尾（不帶 --ws 也能跑；`--no-rewrite` 不跑）、`scripts/sync_notes_to_docs.py`（carry_block 移植程式區塊、新頁重排）。
- B. `scripts/rewrite_license_counts.py`＋`src/jptxgnn/regulatory/count_prose.py`（照 Kr／My／Hk 移植，日文句型：「X 件の承認のうち Y 件が有効」「承認 X 件中、有効なものは Y 件」「有効な承認は N 件」「Z 件は薬価基準から削除済み」）；
  有保留（少なくとも、以上、一部、可能性、他に、残り）、劑型或廠商子集、顯示筆數（上記は主要な N 件）、partial 頁不動；「有効な承認は合計 N 件」checker 讀成總數，不當有效數改；單剤／配合剤只驗不改；同一行有判斷不了的整行不動。
  `apply_drug_reviews.py`（非 --check）與 `build_license_snapshot.py` 結尾自動跑；gate 第 22 項擋「再跑一次會變」。
- 2026-11-24 套用（資料 data-20261117-111616）：程式表 333 頁（公開頁有市場段落 326 頁全部＋noindex；原有 AI 表 327 頁取代、沒有表的 6 頁補表）；正文件數程式改寫 4 句（amantadine 19→18、cephalexin うち有効 12→11、ibuprofen 10→8、nicardipine 12→11）；判斷不了而列待查 0 句。
  錨在舊表列上的 12 筆 `jp-row-*` 標 superseded。查核紀錄更正文字裡的件數（用戶同日決定）：65 筆 replacement 改成不寫件數的寫法（「有効なものと薬価基準から削除済みのものがあります（件數はクイック概要を参照）」；只講舊表筆數的 bosentan、bromperidol 刪掉），
  223 筆 note 拿掉「データ上の収載は N 件、うち有効 M 件です。」與「データ上の X 件のうち有効（収載中）は Y 件で、」，哪幾張薬価削除照留；同 id 重發，前版存 history。`jp-lic-20261112-bimatoprost-1`（「残りの 3 件も有効」）依新事實改寫：「わかもと」2026-03-31 薬価削除。
  單剤／配合剤標籤：正文說「すべて単剤」而依品名有配合剤的 0 句。site.py 的 FIGURES（reviews_from_edits 寫紀錄說明用）改成不寫件數。
  獨立寬偵測（數字不等於事實層總數／有效／削除、程式表列數、紀錄數任一者，或「すべて有効」而有效≠總數）：剩 3 句，都是「他に N 件」「このほかに N 件」的相對數，數字正確。checker 前後都是 P5 1（sulfasalazine，原有、無關）；gate exit 0。
- 已知問題：lithium_citrate 的證據包收的是炭酸リチウム產品，概覽與程式表都列 4 件，正文寫「クエン酸リチウムの承認は確認できません」，原本就矛盾（證據包對照問題，未處理）。checker 的 ja 列狀態字（ROW_WORDS）不認得「薬価削除…」，程式表的削除列 checker 判不出狀態（排程照證據包原文寫，不影響同步）。

## 第二輪：表件數說明句、劑型說法、缺表頁（2026-11-24）

用戶 2026-11-24 第二輪決定（處理第一輪剩下的事）。待查清單裡 11-24 第一輪新增的 open 項目 0 筆（第一輪列待查 0 句），所以這輪處理的是派工點名的句子與全站掃描。
- 表件數說明句：AI 正文裡只講舊表列了幾筆的句子（「上記は 8 件のうち主要な 5 件です」「主要な承認 5 件を示します」「（主要な 5 件を記載）」），跟程式表下的「上表はデータ上の M 件のうち N 件です。」重複、件數也會過期；
  另有舊 AI 表有承認適応症欄時寫的「適応症の記載がある主な承認は次のとおり」（程式表沒有適応症欄）。逐句列在 `config/license_caption_trims.json`（52 頁 52 組 [原文, 改寫後]，空＝整句刪），
  `scripts/sync_license_tables.py` 的 process／carry_block 套用（trim_captions；比照 FR 的 --captions，不寫查核框），gate 第 18 項（caption_problems）擋原文仍在頁面。
  查核紀錄更正文字所在的句子不列：atenolol 只拿掉後面的「以下は主要な 5 件です。」，`jp-lic-20261117-atenolol-1` 同 id 重發補句尾；losartan 的同類句是 `jp-lic-20261106-losartan-1` 的更正文字，同 id 重發改寫。
- 劑型說法：全站掃「すべて／いずれも／のみ／として市販」＋劑形字樣的句子，逐句對照證據包全部品項與医薬品マスター 2026-11-12 全件ファイル（同成分依品名、一般名處方名、YJ 碼前 7 碼）。
  不成立的 10 句寫紀錄（`jp-lic-20261124b-*`：bisoprolol（另有ビソノテープ）、flurbiprofen 2 句（另有フロベン錠・パップ）、beclomethasone_dipropionate（點鼻粉末＋キュバール吸入エアゾール）、budesonide（另有ゼンタコート、コレチメント、レクタブル）、
  cromoglicic_acid（另有吸入液）、menatetrenone（另有ケイツーシロップ・Ｎ静注）、vidarabine（另有點滴静注用）、moxifloxacin（另有アベロックス錠）；另 `jp-lic-20261117-flurbiprofen-1`、`jp-lic-20261106-cromoglicic_acid-1` 同 id 重發、`-2` 改錨）。
  下一步條目只改括號裡的前提。成立而保留：anastrozole、fluconazole、fluvastatin、galantamine、naftopidil、pirfenidone、sennosides、allopurinol、flutamide、lorlatinib、nadifloxacin、sertraline、alimemazine、methylprednisolone、danazol、lornoxicam、pazopanib、lamivudine／levodopa（表上都是配合錠）等。
  多數不成立的原因是證據包（drug_mapping.csv 依一般名對 DrugBank ID）沒收到同成分的其他劑型品目，頁面上的「上表」只是部分品目。
- 缺表頁：公開頁沒有「## 日本市販情報」段落、證據包卻有紀錄的 32 頁（已知用途頁 27、預測頁 5）補段落與程式表（sync_license_tables.add_section：放在「安全性に関する考慮事項」→「結論と次のステップ」→「免責事項」之前；noindex 不補），gate 擋公開頁缺段落；
  已有表的頁正文說「別途提示される許諾情報を参照」「表はサイト側のプログラムが掲載します」的 3 句（cabergoline、carboplatin、etanercept）寫紀錄改成指向上表。
- lithium_citrate：證據包 4 張全是炭酸リチウム錠（drug_mapping.csv 以 drugbank_synonym「LITHIUM」把炭酸リチウム錠對到 DB14507 Lithium citrate；炭酸リチウムは DB14509），医薬品マスターにクエン酸リチウム製剤はない。
  正文「クエン酸リチウムの承認は確認できません」成立，「炭酸リチウム製剤は含めていません」跟表相反，以 `jp-lic-20261124b-lithium_citrate-1` 只改括號；`jp-lic-20261117-lithium_citrate-1`（「日本では販売中」）同 id 重發。證據包對照沒改（要母目錄決定）。
- 張數樣板：site.py 的 FIGURES 第一輪已改成不寫件數；有效紀錄的 replacement／note 裡寫死件數的 0 筆。
- 正文有變的 96 頁 last_modified_at 改 2026-11-24。checker 前後都是 P5 1（sulfasalazine，原有）；gate exit 0。

## 第三輪：證據包依成分補收、排除對照錯的品目（2026-11-24）

用戶 2026-11-24 第三輪決定（A：證據包成分對照修正）。證據包 pmda 區塊是 collectors/jpfda.py 依 data/processed/drug_mapping.csv（品目的一般名或カナ名→DrugBank ID）收的：沒有一般名處方名、カナ名只是商品名的品目對照失敗就收不到（ビソノテープ、フロベン錠、ゼンタコート、ケイツーＮ静注、アラセナ－Ａ点滴、カベルゴリン錠「サワイ」…），カナ轉英文偶爾對錯成分。
- `scripts/add_current_ingredient_items.py [--master y_ALL*.zip] [--dry-run] [--report]`：医薬品マスター最新全件ファイルの YJ コード前 7 碼（薬効分類＋投与経路・成分＝同一成分群）為單位。
  R1：群內有 drug_mapping 對照、且群內只對到一個 DrugBank ID＝本藥的，群內現行品目不在證據包（也不是原收集器已算進 total_matches）的補一筆；
  R2：drug_mapping 完全沒對照的群，群內每個品目的漢字名稱都以本藥的先發商品名（jp_fda_drugs.json「商品名一覧」裡「後発品」之前、三字以上）或一般名基本名開頭（後面不是片假名或是劑形字），而且只對得到一個證據包，整群補；
  人工對照 `config/ingredient_groups.json`（每筆附依據；drugbank_id null＝不屬本站任何證據包）優先，也覆寫 drug_mapping.csv 對該群的列；證據包裡屬於人工對照群、DrugBank ID 不是本藥的紀錄移到 pmda.excluded_records（附 reason），原收集器算進 total_matches 卻沒存成紀錄的同類品目從 total_matches 扣掉。
  離子類證據包（calcium、magnesium、zinc、iron）不處理；只處理有藥物頁（非轉址）的證據包；紀錄欄位同後継コード補收（另記 yj_group、source、added），不設筆數上限，total_matches 同步加；只加不刪、可重複執行。
  `.github/workflows/license-refresh.yml` 在 license_refresh 前先跑（下載失敗不擋排程），有補收／排除／覆寫就照常發新 Release。
- 人工對照（2026-11-24）：炭酸リチウム（YJ 1179017）DB14507→DB14509（lithium_citrate 證據包的 4 張炭酸リチウム錠移到 excluded_records，頁面概覽與程式表變 0 件；本站沒有 lithium carbonate 的頁或證據包，所以沒有移過去）；
  トポテシン（YJ 4240404，イリノテカン塩酸塩）DB01030→DB00762（topotecan 證據包的 2 張排除；本站沒有 irinotecan 頁），ハイカムチン（YJ 4240408，ノギテカン＝topotecan）補進 topotecan；
  レミフェンタニル（YJ 8219401）DB00813→DB00899（fentanyl 證據包 total_matches 扣 2）；ヘパリン類似物質（ヒルドイド等，YJ 3339950、2649950、2649865）原對到 heparin，改成不屬任何證據包（heparin 證據包排除 15 張、total_matches 扣 27）；
  ビソノテープ（2149700）→bisoprolol、ケイツーＮ静注（3160401）→menatetrenone。drug_mapping.csv 覆寫 76 列。
- 2026-11-24 套用（資料 data-20261117-111616＋全件ファイル y_ALL20261112）：126 個證據包補 987 筆（R1 907、R2 74、人工對照 6）、排除 21 筆；第二次跑 0 筆。
  證據包 local_regulatory 重算（refresh_pack_regulatory）126 個有變；概覽表狀態列／張數列 126 頁 267 格由程式同步（sync_market_rows）；程式表 90 頁重排；正文件數由 B 改寫 21 頁；description 句尾 38 頁；docs/_data/brand_names.json 3 頁（bisoprolol 加ビソノ、menatetrenone 加ケイツーＮ、topotecan トポテシン→ハイカムチン）與搜尋索引照重產。
  正文跟新事實矛盾的：`jp-lic-20261124b-lithium_citrate-1` 撤回（原句「炭酸リチウム製剤は別成分のため含めていません」又成立，頁面還原原句），`jp-lic-20261117-lithium_citrate-1`、`jp-lic-20261106-lithium_citrate-1`、`jp-lic-20261117-flurbiprofen-1` 與第二輪劑型紀錄 6 筆（bisoprolol、vidarabine、budesonide、menatetrenone、flurbiprofen-1／-2；說明裡「本ページのデータには含まれていない」不再成立）同 id 重發（前版存 history），
  新紀錄 `jp-lic-20261124c-lenalidomide-1`（「ジェネリックを含め 12 件あり、そのすべてが有効」→不寫件數，B 的句型認不得）。
  獨立寬偵測（補收證據包的頁，數字不等於事實層總數／有效／削除或程式表列數，或劑形全稱句）：剩下的都是查核框裡的原文引用、臨床試驗件數、或仍成立的「上表の品目はいずれも…」。checker 前後都是 P5 1（sulfasalazine，原有）；gate exit 0。正文有變的 127 頁 last_modified_at 改 2026-11-24。
- 沒處理：R1 會放大 drug_mapping 既有的群對照（群整個對錯時）——這次逐群看過 128 群，錯的只有上面幾個；チアミンジスルフィド（バイオゲン等）照本站既有對照算 thiamine，沒改。
