---
layout: default
title: Fenoprofen
parent: 僅模型預測 (L5)
nav_order: 70
evidence_level: L5
indication_count: 1
---

# Fenoprofen
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

# Fenoprofen 藥師評估筆記

## 一句話總結

Fenoprofen 是一種 NSAID 類止痛藥，TxGNN 預測其可用於多種骨骼肌肉疾病，其中僵直性脊椎炎的預測具有多項臨床試驗支持。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 藥物名稱 | Fenoprofen (芬諾普芬) |
| DrugBank ID | DB00573 |
| 台灣商品名 | 風諾保膠囊 |
| 原核准適應症 | 風濕性關節炎、骨關節炎、急性痛風、鎮痛、解熱 |
| 預測新適應症 | 僵直性脊椎炎、假性軟骨發育不全、WHIM 症候群 |
| 最高預測分數 | 0.9999 (acromesomelic dysplasia) |
| 證據等級 | L2 (僵直性脊椎炎有多個臨床試驗) |

## 為什麼這個預測合理

Fenoprofen 作為丙酸類 NSAID，其對預測適應症的機轉如下：

1. **COX 抑制作用**：同時抑制 COX-1 和 COX-2，減少前列腺素合成
2. **抗發炎效果**：對關節炎和脊椎炎的發炎有效
3. **止痛作用**：中樞和周邊的止痛機轉
4. **同類藥物比較**：屬於與 naproxen、ibuprofen 同類的丙酸類 NSAID

### 僵直性脊椎炎預測特別合理
- NSAIDs 是僵直性脊椎炎的一線治療藥物
- 部分原核准適應症已包含「關節強硬性脊椎炎」（即僵直性脊椎炎）

## 臨床試驗證據

### 僵直性脊椎炎相關試驗

雖然 ClinicalTrials.gov 未找到近期試驗，但 PubMed 文獻記載了多項歷史臨床試驗：

| 研究 | 設計 | 關鍵發現 |
|------|------|---------|
| Wordsworth 1980 | 雙盲交叉試驗 | Fenoprofen 600mg tid vs Phenylbutazone 100mg tid；Phenylbutazone 較優 |
| Wasner 1981 | 雙盲隨機試驗 | 比較 6 種 NSAIDs，fenoprofen 為僵直性脊椎炎的有效選擇之一 |
| Shipley 1980 | 雙盲交叉試驗 | Fenoprofen vs Indomethacin vs 安慰劑比較 |

**證據等級：L2 (多個臨床試驗)**

## 文獻證據

### 僵直性脊椎炎

| PMID | 年份 | 研究類型 | 關鍵發現 |
|------|------|----------|---------|
| 7010512 | 1980 | RCT | 30 位患者；fenoprofen 改善胸廓擴張，但整體效果不如 phenylbutazone |
| 7026817 | 1981 | RCT | 32 位患者；naproxen、indomethacin、fenoprofen 為最有效的三種 NSAIDs |
| 6996071 | 1980 | RCT | Fenoprofen 優於安慰劑，但不如 indomethacin |
| 324748 | 1977 | 綜述 | Fenoprofen 2.4g/day 用於僵直性脊椎炎的療效與安全性回顧 |

### 其他關節疾病

| PMID | 年份 | 研究類型 | 關鍵發現 |
|------|------|----------|---------|
| 387372 | 1979 | 綜述 | 比較 naproxen 和 fenoprofen 在類風濕性關節炎的效果 |
| 300118 | 1977 | 綜述 | Fenoprofen、naproxen、tolmetin 在風濕疾病的應用 |

### 重要歷史研究
Brogden et al. (1977) 的藥物回顧指出：
- Fenoprofen 2.4g/day 療效與 aspirin 3.6-4g/day 相當
- 胃腸道副作用較 aspirin 少且輕微
- 可用於類風濕性關節炎、退化性關節炎、僵直性脊椎炎和痛風

## 台灣上市資訊

| 許可證字號 | 中文品名 | 劑量 | 許可證持有者 | 狀態 |
|-----------|---------|------|-------------|------|
| 衛署藥製字第041435號 | 應元炎普朗膠囊 | 200mg | 應元化學製藥 | 有效 |
| 衛署藥製字第037862號 | 伏炎痛膠囊 | - | 西德有機化學藥品 | 有效 |
| 衛署藥製字第011765號 | 風諾保膠囊 | 300mg | 臺灣禮來 | 已註銷 |

**注意**：多數 fenoprofen 製劑已註銷，目前在台灣取得較困難。

## 安全性考量

### 已知風險
- **胃腸道風險**：潰瘍、出血、穿孔
- **心血管風險**：NSAIDs 類效應，可能增加心血管事件風險
- **腎臟風險**：可能導致急性腎損傷，尤其在脫水狀態
- **過敏反應**：aspirin 過敏者可能交叉過敏

### 藥物交互作用

根據 DDInter 資料庫：

| 交互作用藥物 | 嚴重度 | 說明 |
|-------------|--------|------|
| Acetylsalicylic acid | Moderate | 增加胃腸道出血風險 |
| Hydrocortisone | Moderate | 增加胃腸道副作用 |
| Metformin | Moderate | 可能增加乳酸中毒風險 |
| Triamcinolone | Moderate | 增加胃腸道副作用 |
| Famotidine | Minor | 可降低 NSAIDs 相關潰瘍風險 |
| Ranitidine | Minor | 可降低 NSAIDs 相關潰瘍風險 |

### 禁忌症
- 活動性胃腸道潰瘍或出血
- 嚴重心衰竭
- 冠狀動脈繞道手術前後
- 對 NSAIDs 或 aspirin 過敏

### 特殊族群
- **孕婦**：C 級(第三孕期 D 級)，避免使用
- **哺乳**：分泌至乳汁，不建議使用
- **老年人**：增加胃腸道出血風險，建議最低有效劑量
- **腎功能不全**：避免使用或減量

## 結論與下一步

### 整體評估
僵直性脊椎炎的預測**具有臨床價值**，原因如下：
1. 多個歷史 RCT 支持 fenoprofen 對僵直性脊椎炎的療效
2. NSAIDs 是僵直性脊椎炎的一線治療藥物
3. 部分原核准適應症已涵蓋此用途

其他預測（如罕見骨骼發育異常）缺乏證據，不建議應用。

### 建議行動
- [x] 僵直性脊椎炎可作為 fenoprofen 的合理使用適應症
- [ ] 考量到 fenoprofen 在台灣取得困難，可優先選用其他同類 NSAIDs
- [ ] 其他預測的罕見疾病需要進一步研究

### 臨床建議
對於僵直性脊椎炎患者：
1. NSAIDs 仍是一線藥物選擇
2. Fenoprofen 是有效選項之一，但療效可能不如 indomethacin 或 naproxen
3. 若 fenoprofen 不可得，可選用其他丙酸類 NSAIDs

### 風險等級
**中等風險** - 僵直性脊椎炎使用有證據支持，但需注意 NSAIDs 通用風險

---

*報告生成日期：2026-02-11*
*資料來源：TxGNN 預測、ClinicalTrials.gov、PubMed、TFDA*


---

