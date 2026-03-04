---
layout: default
title: Trifluoperazine
parent: 中證據等級 (L3-L4)
nav_order: 184
evidence_level: L3
indication_count: 1
---

# Trifluoperazine
{: .fs-9 }

證據等級: **L3** | 預測適應症: **1** 個
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

# Trifluoperazine：從精神病狀態到躁鬱症躁症期

## 一句話總結

Trifluoperazine (三氟陪拉辛) 原本用於治療精神病狀態及行為障礙。
TxGNN 模型預測它可能對**躁鬱症躁症期 (manic bipolar affective disorder)** 有效，
目前有 **20 篇文獻**支持這個方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 精神病狀態、噁心嘔吐、攻擊性與破壞性行為障礙 |
| 預測新適應症 | 躁鬱症躁症期 (manic bipolar affective disorder) |
| TxGNN 預測分數 | 99.51% |
| 證據等級 | L3 (有間接文獻證據) |
| 台灣上市 | 已上市 |
| 許可證數 | 47 張 |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

Trifluoperazine 是一種典型抗精神病藥物（phenothiazine 類），其作用機轉支持在躁症期的應用：

1. **多巴胺 D2 受體阻斷**：抑制中腦邊緣系統的多巴胺過度活化
2. **鎮靜作用**：減少躁動、攻擊性行為
3. **抗精神病作用**：改善精神病性症狀（如妄想、幻覺）

躁症期常伴隨精神病性症狀，典型抗精神病藥物在非典型藥物問世前是躁症急性期的標準治療選擇之一。

## 臨床試驗證據

目前無針對躁鬱症躁症期的專門臨床試驗，但有多篇文獻支持其在躁症期的使用。

## 文獻證據

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [14309092](https://pubmed.ncbi.nlm.nih.gov/14309092/) | 1965 | Clinical Study | Int J Neuropsychiatry | 比較 Haloperidol 與 Trifluoperazine 在精神分裂症及躁症患者中的療效 |
| [24943390](https://pubmed.ncbi.nlm.nih.gov/24943390/) | 2014 | Survey | J Clin Psychopharmacol | 烏干達精神病院處方模式：Trifluoperazine 與 Carbamazepine 併用治療躁鬱症佔 45% |
| [17017818](https://pubmed.ncbi.nlm.nih.gov/17017818/) | 2006 | Review | J Clin Psychiatry | 典型與非典型抗精神病藥物在躁鬱症焦慮症狀的療效回顧 |
| [970489](https://pubmed.ncbi.nlm.nih.gov/970489/) | 1976 | Case Study | Am J Psychiatry | 探討多巴胺機轉在躁症中的角色 |
| [3935307](https://pubmed.ncbi.nlm.nih.gov/3935307/) | 1985 | Case Report | Can J Psychiatry | 青少年躁鬱症案例，使用 Trifluoperazine 治療 |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 |
|---------|------|------|-----------|
| 內衛藥輸字第002368號 | 福路新1公絲 | 錠劑 | 意識運動機能亢進引起之急慢性精神病 |
| 衛署藥製字第002672號 | 惠鎮寧糖衣錠 | 糖衣錠 | 精神病狀態、噁心嘔吐、攻擊性與破壞性行為障礙 |
| 衛署藥製字第032029號 | "強生"富祿靜膜衣錠5毫克 | 膜衣錠 | 精神病狀態、噁心嘔吐、攻擊性與破壞性行為障礙 |
| 衛署藥製字第035165號 | 福樂靜膠囊2公絲 | 膠囊劑 | 精神病狀態、噁心嘔吐、攻擊性與破壞性行為障礙 |

## 安全性考量

- **錐體外症候群 (EPS)**：典型抗精神病藥物的主要副作用
- **遲發性運動障礙 (Tardive dyskinesia)**：長期使用風險
- **神經惡性症候群 (NMS)**：罕見但嚴重的不良反應
- **主要交互作用 (Major)**：
  - Bupropion（降低癲癇閾值）
  - Morphine（增強中樞抑制）
  - Metoclopramide（增加錐體外症狀風險）
  - Potassium chloride、Potassium citrate（增加腸胃道潰瘍風險）
  - Dolasetron（QT 延長風險）
- **中度交互作用 (Moderate)**：
  - 糖尿病藥物（可能影響血糖控制）
  - 抗膽鹼藥物（增加抗膽鹼作用）
  - Levofloxacin（QT 延長風險）

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
Trifluoperazine 作為典型抗精神病藥物，在躁症期的使用有歷史性臨床經驗支持。多篇文獻顯示其在躁鬱症患者中的應用，特別是在資源有限的地區仍是重要的治療選擇。

**若要推進需要：**
- 與非典型抗精神病藥物的比較研究
- 評估 EPS 及代謝副作用的風險效益比
- 制定明確的劑量建議及監測計畫
- 考量作為急性期治療而非長期維持治療

**臨床提醒：**
現代躁症急性期治療首選通常為非典型抗精神病藥物（如 Olanzapine、Quetiapine、Risperidone），Trifluoperazine 可作為替代選擇，但需注意 EPS 風險。


---

