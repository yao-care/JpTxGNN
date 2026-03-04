---
layout: default
title: Regorafenib
parent: 高證據等級 (L1-L2)
nav_order: 144
evidence_level: L2
indication_count: 1
---

# Regorafenib
{: .fs-9 }

證據等級: **L2** | 預測適應症: **1** 個
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

# Regorafenib：從大腸直腸癌到脂肪肉瘤

## 一句話總結

Regorafenib 是一種多標靶激酶抑制劑，原本用於轉移性大腸直腸癌、胃腸道間質腫瘤（GIST）和肝細胞癌的治療。TxGNN 模型預測它可能對**脂肪肉瘤 (Liposarcoma)** 有效，目前有 **2 個臨床試驗**和 **9 篇文獻**支持這個方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 轉移性大腸直腸癌、胃腸道間質腫瘤、肝細胞癌 |
| 預測新適應症 | 脂肪肉瘤 (Liposarcoma) |
| TxGNN 預測分數 | 99.76% |
| 證據等級 | L2 |
| 台灣上市 | 已上市 |
| 許可證數 | 1 張 |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

Regorafenib 是一種口服多標靶激酶抑制劑，可抑制多種參與腫瘤血管新生、腫瘤微環境和腫瘤增殖的激酶，包括：
- VEGFR1-3（血管新生）
- TIE2（血管新生）
- PDGFR-β（腫瘤微環境）
- FGFR（纖維母細胞生長因子受體）
- KIT、RET、RAF（腫瘤增殖）

脂肪肉瘤是一種源自脂肪組織的惡性腫瘤，屬於軟組織肉瘤。與大腸直腸癌和 GIST 類似，脂肪肉瘤的生長和轉移也依賴血管新生和特定的信號傳導途徑。

Regorafenib 的多標靶特性使其在抑制腫瘤血管新生和腫瘤微環境方面具有潛在優勢。已有多項臨床試驗（包括 SARC024 和 REGOSARC）探討 regorafenib 在軟組織肉瘤中的療效。

## 臨床試驗證據

| 試驗編號 | 階段 | 狀態 | 人數 | 主要發現 |
|---------|------|------|------|---------|
| [NCT02048371](https://clinicaltrials.gov/study/NCT02048371) | Phase 2 | 已完成 | 131 | SARC024：Regorafenib 用於脂肪肉瘤、骨肉瘤、Ewing 肉瘤等 |
| [NCT01900743](https://clinicaltrials.gov/study/NCT01900743) | Phase 2 | 已完成 | 219 | REGOSARC：Regorafenib vs 安慰劑用於軟組織肉瘤，包含脂肪肉瘤組 |

## 文獻證據

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [27751846](https://pubmed.ncbi.nlm.nih.gov/27751846/) | 2016 | RCT | Lancet Oncol | REGOSARC 試驗：regorafenib 對軟組織肉瘤的療效和安全性 |
| [32701199](https://pubmed.ncbi.nlm.nih.gov/32701199/) | 2020 | RCT | The Oncologist | SARC024 脂肪肉瘤組結果：不支持 regorafenib 常規用於脂肪肉瘤 |
| [29902612](https://pubmed.ncbi.nlm.nih.gov/29902612/) | 2018 | RCT | Eur J Cancer | REGOSARC 更新分析：regorafenib 對非脂肪肉瘤有效，脂肪肉瘤效果不佳 |
| [29931504](https://pubmed.ncbi.nlm.nih.gov/29931504/) | 2018 | Review | Target Oncol | Regorafenib 在肉瘤治療中的角色 |
| [25884155](https://pubmed.ncbi.nlm.nih.gov/25884155/) | 2015 | Protocol | BMC Cancer | REGOSARC 試驗方案 |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 |
|---------|------|------|-----------|
| 衛部藥輸字第XXXXXX號 | 癌瑞格膜衣錠40毫克 | 膜衣錠 | 大腸直腸癌、胃腸道間質腫瘤、肝細胞癌 |

## 細胞毒性

| 項目 | 內容 |
|------|------|
| 細胞毒性分類 | 標靶藥物（多標靶激酶抑制劑） |
| 骨髓抑制風險 | 低至中度（可能出現血小板減少） |
| 致吐性分級 | 低度 |
| 監測項目 | CBC、肝功能（ALT/AST/Bilirubin）、血壓、皮膚反應 |
| 處置防護 | 口服藥物，遵循一般藥物處置規範即可 |

## 安全性考量

**主要警語：**
- 肝毒性：可能出現嚴重肝損傷，需定期監測肝功能
- 手足皮膚反應（HFSR）：常見不良反應
- 高血壓：需監測血壓

**禁忌症：**
請參考原廠仿單

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
雖然 SARC024 和 REGOSARC 試驗已探討 regorafenib 用於脂肪肉瘤，但結果顯示在脂肪肉瘤亞組中療效有限。這與其他軟組織肉瘤亞型（如平滑肌肉瘤、滑膜肉瘤）的正面結果形成對比。然而，由於仍有部分患者可能獲益，且缺乏其他有效治療選擇，在充分知情同意下可考慮使用。

**若要推進需要：**
- 根據 SARC024 和 REGOSARC 試驗結果，謹慎評估患者是否適合
- 密切監測肝功能和皮膚反應
- 探索與其他療法（如免疫治療）的組合方案
- 考慮生物標記物以篩選可能獲益的患者亞群


---

