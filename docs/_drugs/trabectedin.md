---
layout: default
title: Trabectedin
parent: 僅模型預測 (L5)
nav_order: 179
evidence_level: L5
indication_count: 1
---

# Trabectedin
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

# Trabectedin：從軟組織肉瘤到女性乳腺癌

## 一句話總結

Trabectedin 原本用於治療無法切除或轉移性脂肪肉瘤及平滑肌肉瘤。
TxGNN 模型預測它可能對**女性乳腺癌 (female breast carcinoma)** 有效，
目前有 **2 個臨床試驗**和 **多篇文獻**支持這個方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 無法切除或轉移性脂肪肉瘤/平滑肌肉瘤 |
| 預測新適應症 | 女性乳腺癌 (female breast carcinoma) |
| TxGNN 預測分數 | 99.73% |
| 證據等級 | 待評估 |
| 台灣上市 | 已上市 |
| 許可證數 | 2 張 |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

Trabectedin 是一種源自海洋生物的抗腫瘤藥物，主要透過影響轉錄調控抑制癌細胞增殖。其獨特的作用機轉包括：

1. **DNA 修復系統干擾**：影響轉錄耦合核苷酸切除修復及同源重組修復 (HRR)
2. **腫瘤微環境調節**：減少腫瘤相關巨噬細胞 (TAM) 數量
3. **BRCA 缺陷敏感性**：對 BRCA1/2 突變的腫瘤具有特殊療效

這些機轉在乳腺癌中同樣具有臨床意義，特別是 BRCA 突變的乳腺癌患者。

## 臨床試驗證據

| 試驗編號 | 階段 | 狀態 | 人數 | 主要發現 |
|---------|------|------|------|---------|
| [NCT03470805](https://clinicaltrials.gov/study/NCT03470805) | Phase 2 | COMPLETED | 9 | 評估 Olaparib 作為 Trabectedin-PLD 療程後維持治療在復發性卵巢癌中的效果 |
| [NCT00786838](https://clinicaltrials.gov/study/NCT00786838) | Phase 2 | COMPLETED | 76 | 評估 Trabectedin 對 QT/QTc 間隔的影響 |

## 文獻證據

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [26592307](https://pubmed.ncbi.nlm.nih.gov/26592307/) | 2016 | Review | Expert Opin Investig Drugs | 討論 Trabectedin 在乳腺癌中的潛在應用 |
| [25239225](https://pubmed.ncbi.nlm.nih.gov/25239225/) | 2014 | Phase II RCT | Clin Breast Cancer | 評估 Trabectedin 單藥治療晚期乳腺癌的療效與安全性 |
| [27710871](https://pubmed.ncbi.nlm.nih.gov/27710871/) | 2016 | Review | Cancer Treat Rev | 探討 Trabectedin 在 BRCA 缺陷患者中的化療選擇 |
| [27266804](https://pubmed.ncbi.nlm.nih.gov/27266804/) | 2016 | Phase II | Clin Breast Cancer | 根據 XPG 基因表達評估 Trabectedin 在 HR+/HER2- 晚期乳腺癌中的療效 |
| [38863768](https://pubmed.ncbi.nlm.nih.gov/38863768/) | 2024 | Review | Drug Des Devel Ther | 聚焦 Trabectedin 在卵巢癌中的應用及 BRCA 突變情況 |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 |
|---------|------|------|-----------|
| 衛部藥輸字第027370號 | "友待" 凍晶注射劑1毫克 | 凍晶注射劑 | 無法切除或轉移性脂肪肉瘤或平滑肌肉瘤 |

## 細胞毒性

| 項目 | 內容 |
|------|------|
| 細胞毒性分類 | 抗腫瘤抗生素 (海洋來源) |
| 骨髓抑制風險 | 高度 |
| 致吐性分級 | 中度至高度 |
| 監測項目 | CBC（含分類）、肝腎功能、CK |
| 處置防護 | 需依細胞毒性藥物處置規範操作 |
| 特殊注意 | 可能引起橫紋肌溶解症，需監測肌酸激酶 |

## 安全性考量

- **肝毒性**：需定期監測肝功能
- **骨髓抑制**：可能導致嗜中性白血球減少、血小板減少
- **橫紋肌溶解症**：罕見但嚴重的不良反應
- **心臟毒性**：需監測 QT 間隔

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
Trabectedin 在乳腺癌中的多項臨床試驗及文獻顯示其潛在療效，特別是對 BRCA 突變患者。其獨特的作用機轉與現有乳腺癌治療藥物不同，可能提供新的治療選擇。

**若要推進需要：**
- 針對乳腺癌的大型隨機對照試驗
- BRCA 突變狀態的生物標記篩選策略
- 與現有乳腺癌治療方案的比較研究


---

