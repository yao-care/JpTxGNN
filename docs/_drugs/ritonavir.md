---
layout: default
title: Ritonavir
parent: 中證據等級 (L3-L4)
nav_order: 148
evidence_level: L4
indication_count: 1
---

# Ritonavir
{: .fs-9 }

證據等級: **L4** | 預測適應症: **1** 個
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

# Ritonavir：從 HIV 到猿免疫缺乏病毒感染

## 一句話總結

Ritonavir 是一種 HIV 蛋白酶抑制劑，原本用於人類免疫缺乏病毒（HIV）感染的治療。TxGNN 模型預測它可能對**猿免疫缺乏病毒感染 (Simian Immunodeficiency Virus Infection)** 有效，目前有 **多篇文獻**支持這個方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 人類免疫缺乏病毒（HIV）感染 |
| 預測新適應症 | 猿免疫缺乏病毒感染 (SIV Infection)、貓愛滋病 |
| TxGNN 預測分數 | 99.92% |
| 證據等級 | L4 |
| 台灣上市 | 已上市 |
| 許可證數 | 多張 |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

Ritonavir 是一種 HIV 蛋白酶抑制劑，主要用於 HIV 治療。目前它通常作為藥物動力學增強劑（booster）與其他蛋白酶抑制劑（如 darunavir、lopinavir）併用，以提高其他藥物的血中濃度。

猿免疫缺乏病毒（SIV）是 HIV 的近親病毒，在非人靈長類動物中引起類似 AIDS 的疾病。SIV 是研究 HIV 感染和抗病毒藥物的重要動物模型。由於 SIV 和 HIV 的蛋白酶具有結構相似性，針對 HIV 蛋白酶的抑制劑對 SIV 也可能具有活性。

文獻研究已證實：
1. Ritonavir 在體外對 SIVmac239 具有抑制活性
2. 包含 ritonavir-boosted lopinavir 的多藥組合療法可有效抑制 SIV 感染的恆河猴體內病毒載量
3. SIV/SHIV 動物模型是評估抗逆轉錄病毒藥物的重要工具

## 臨床試驗證據

目前無針對 SIV 感染的人類臨床試驗（SIV 不感染人類）。

## 文獻證據

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [12709355](https://pubmed.ncbi.nlm.nih.gov/12709355/) | 2003 | Journal Article | Antimicrob Agents Chemother | SIVmac239 對 ritonavir 的敏感性（EC50: 13 nM） |
| [16973590](https://pubmed.ncbi.nlm.nih.gov/16973590/) | 2006 | Journal Article | J Virol | 四藥抗逆轉錄病毒治療在 SIV 感染獼猴中的快速病毒衰減 |
| [22737073](https://pubmed.ncbi.nlm.nih.gov/22737073/) | 2012 | Journal Article | PLoS Pathog | 高強度 ART 可長期抑制 SIV 病毒載量並限制病毒儲存庫 |
| [34903055](https://pubmed.ncbi.nlm.nih.gov/34903055/) | 2021 | Journal Article | mBio | 儘管有效的 ART，慢病毒感染仍持續存在於腦中 |
| [17350308](https://pubmed.ncbi.nlm.nih.gov/17350308/) | 2007 | Journal Article | Microbes Infect | SHIV-pr 構建及其對蛋白酶抑制劑敏感性的體內評估 |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 |
|---------|------|------|-----------|
| 衛部藥輸字第XXXXXX號 | 普利他膜衣錠150毫克 | 膜衣錠 | 人類免疫缺乏病毒（HIV）感染 |

## 安全性考量

**主要警語：**
- 藥物交互作用：Ritonavir 是 CYP3A4 的強效抑制劑，與多種藥物有顯著交互作用
- 肝毒性
- 脂質代謝異常

**禁忌症：**
請參考原廠仿單

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
這個預測在科學上是合理的，因為 SIV 是 HIV 的近親病毒，ritonavir 對 SIV 蛋白酶的抑制活性已在體外和動物模型中得到證實。然而，由於 SIV 不感染人類，這個預測的主要應用是在獸醫學領域（靈長類動物）或作為 HIV 研究的動物模型工具。

**若要推進需要：**
- 這主要是獸醫學/動物研究的應用
- 評估在 SIV 感染的非人靈長類動物中的療效和安全性
- 作為 HIV 研究工具，已有充分的應用基礎
- 對於貓愛滋病（FIV），需進行額外的種間交叉反應研究


---

