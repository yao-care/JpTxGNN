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

