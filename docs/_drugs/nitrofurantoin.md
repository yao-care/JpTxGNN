---
layout: default
title: Nitrofurantoin
parent: 僅模型預測 (L5)
nav_order: 114
evidence_level: L5
indication_count: 1
---

# Nitrofurantoin
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

# Nitrofurantoin：從 尿路感染 到 類風濕性關節炎

## 一句話總結

Nitrofurantoin（淋可輸）是一種合成抗菌劑，專門用於治療尿路感染。TxGNN 模型預測它對**類風濕性關節炎 (rheumatoid arthritis)** 有潛在關聯，但文獻證據顯示這主要是共病關係或藥物不良反應報告，而非治療效果。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 尿路感染（膀胱炎、腎盂炎、尿道炎） |
| 預測新適應症 | 類風濕性關節炎 (rheumatoid arthritis) |
| TxGNN 預測分數 | 99.89% |
| 證據等級 | L5 |
| 台灣上市 | 已上市 |
| 許可證數 | 多張 |
| 建議決策 | Hold |

## 為什麼這個預測可能是偽相關？

Nitrofurantoin 通過損傷細菌 DNA 和抑制酶活性發揮殺菌作用，對革蘭氏陽性和陰性菌均有效。其作用局限於尿路，全身吸收有限。

**文獻回顧顯示：**
- 多篇文獻提及 nitrofurantoin 與類風濕性關節炎的關係，但主要是：
  1. **藥物性肺纖維化**：Nitrofurantoin 是已知可導致肺纖維化的藥物，這也是類風濕性關節炎的併發症
  2. **共病報告**：類風濕性關節炎患者使用 nitrofurantoin 治療尿路感染的病例報告
  3. **抗生素與 RA 惡化**：研究顯示某些抗生素可能觸發 RA 惡化

**缺乏治療證據：**
- 無證據顯示 nitrofurantoin 對 RA 有抗發炎或免疫調節作用
- Nitrofurantoin 主要局限於尿路，不適合全身性疾病治療

## 臨床試驗證據

無相關臨床試驗登記。

## 文獻證據

| PMID | 年份 | 類型 | 主要發現 |
|------|-----|------|---------|
| [31222078](https://pubmed.ncbi.nlm.nih.gov/31222078/) | 2019 | Journal Article | 抗生素使用與 RA 惡化的關係，nitrofurantoin 被列為研究藥物之一 |
| [35145797](https://pubmed.ncbi.nlm.nih.gov/35145797/) | 2022 | Case Report | Methotrexate 和 nitrofurantoin 交互作用導致不可逆肺纖維化 |
| [3335140](https://pubmed.ncbi.nlm.nih.gov/3335140/) | 1988 | Journal Article | RA 患者住院治療間質性肺纖維化，部分與 nitrofurantoin 相關 |

這些文獻顯示 nitrofurantoin 與 RA 的關聯主要是**不良反應**（肺纖維化）或**共病治療**，而非治療效果。

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 |
|---------|------|------|-----------|
| 多張許可證 | 淋可輸片等 | 錠劑/膠囊 | 腎盂炎、膀胱炎、尿道炎、尿路感染症 |

## 安全性考量

**重要警告：**
- **肺毒性**：急性、亞急性和慢性肺反應，包括肺纖維化
- 長期使用（>6個月）增加肺纖維化風險
- 肝毒性（罕見）
- 神經病變（長期使用）

**RA 患者注意：**
- RA 本身可導致間質性肺疾病
- 合併使用 methotrexate 會增加肺毒性風險
- 不建議 RA 患者長期使用 nitrofurantoin

## 結論與下一步

**決策：Hold**

**理由：**
文獻分析顯示 nitrofurantoin 與類風濕性關節炎的關聯來自：（1）兩者共同導致肺纖維化的副作用/併發症，（2）RA 患者使用 nitrofurantoin 治療尿路感染的病例報告。這是知識圖譜中的偽相關，而非真正的治療關係。此外，nitrofurantoin 的全身分布有限，不適合用於全身性自體免疫疾病。

**若要推進需要：**
- 不建議進一步探索此適應症
- 此預測反映的是共病/不良反應關係，而非治療潛力


---

