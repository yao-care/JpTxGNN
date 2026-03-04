---
layout: default
title: Hydroxyurea
parent: 高證據等級 (L1-L2)
nav_order: 82
evidence_level: L2
indication_count: 1
---

# Hydroxyurea
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

# Hydroxyurea：從血液腫瘤到女性乳腺癌

## 一句話總結

Hydroxyurea 原本用於治療慢性骨髓性白血病、骨髓纖維化及真性紅血球增多症。
TxGNN 模型預測它可能對**女性乳腺癌 (female breast carcinoma)** 有效，
目前有 **超過 20 篇文獻**支持這個研究方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 慢性骨髓性白血病、骨髓纖維化、真性紅血球增多症、卵巢癌、頭頸癌 |
| 預測新適應症 | 女性乳腺癌 (female breast carcinoma) |
| TxGNN 預測分數 | 99.97% |
| 證據等級 | L2 |
| 台灣上市 | 有效許可證 |
| 許可證數 | 多張 |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

Hydroxyurea 是一種核糖核苷酸還原酶抑制劑，透過阻斷 DNA 合成發揮抗腫瘤作用。
它可以抑制細胞從 G1 期進入 S 期，並增加細胞對放射線的敏感性。

**預測合理性分析：**
- Hydroxyurea 已核准用於多種實體腫瘤（卵巢癌、頭頸癌）
- 在乳癌的高劑量化療方案中已有使用經驗
- 可作為放射增敏劑，與放射治療合併使用
- 研究顯示可與其他藥物（如 valproic acid）產生協同作用

**機轉支持：**
- 抑制 DNA 合成和修復
- 誘導複製壓力，增加 DNA 雙股斷裂
- 與 valproic acid 合併可抑制同源重組修復（PMID: 28837865）
- 脂質藥物複合體可提高細胞攝取率（PMID: 38211596）

## 臨床試驗證據

文獻中報告的臨床經驗包括：

| 研究類型 | 年份 | 期刊 | 主要發現 |
|---------|------|------|---------|
| Phase I | 1991 | Am J Clin Oncol | FU-LV-HU 組合方案在晚期乳癌中的 Phase I 試驗 |
| Phase I/II | 1994 | Bone Marrow Transplant | 高劑量 CY-Thiotepa-HU 配合自體幹細胞移植用於轉移性乳癌 |
| Phase I | 1992 | Cancer Chemother Pharmacol | 5-FU、LV、HU 與 cisplatin 合併放療的臨床藥理學研究 |

## 文獻證據

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [38211596](https://pubmed.ncbi.nlm.nih.gov/38211596/) | 2024 | 電腦模擬 | Drug Res | HU 脂質藥物複合體設計，靶向 PI3K/AKT/mTOR 通路 |
| [28837865](https://pubmed.ncbi.nlm.nih.gov/28837865/) | 2017 | 體外研究 | DNA Repair | Valproic acid 增敏乳癌細胞對 HU 的反應 |
| [32795962](https://pubmed.ncbi.nlm.nih.gov/32795962/) | 2020 | 體外研究 | DNA Repair | 2-hexyl-4-pentynoic acid 與 HU 聯合抑制乳癌 |
| [7914447](https://pubmed.ncbi.nlm.nih.gov/7914447/) | 1994 | Phase I/II | Bone Marrow Transplant | 高劑量 CY-Thiotepa-HU 用於轉移性乳癌的鞏固治療 |
| [21730979](https://pubmed.ncbi.nlm.nih.gov/21730979/) | 2011 | 體外研究 | Br J Cancer | ATR 抑制劑與 HU 在乳癌和卵巢癌細胞中的效果 |

## 細胞毒性

| 項目 | 內容 |
|------|------|
| 細胞毒性分類 | 傳統細胞毒性藥物 |
| 骨髓抑制風險 | 高度 |
| 致吐性分級 | 低度 |
| 監測項目 | CBC（含分類）、肝腎功能、MCV |
| 處置防護 | 需依細胞毒性藥物處置規範操作 |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 |
|---------|------|------|-----------|
| - | 捷可衛錠 | 錠劑 | 骨髓纖維化、真性紅血球增多症、GvHD |
| - | Hydroxyurea 膠囊 | 膠囊 | 慢性骨髓性白血病、卵巢癌、頭頸癌 |

## 安全性考量

- **藥物交互作用**：文獻中多與其他化療藥物合併使用
- **注意事項**：
  - 骨髓抑制是最主要的劑量限制毒性
  - 長期使用可能增加繼發性白血病風險
  - 皮膚毒性（色素沉著、潰瘍）
  - 巨球性貧血
- **乳癌適用考量**：
  - 目前多用於高劑量化療方案
  - 需考量與現有標準治療的比較

安全性資訊請參考原廠仿單。

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
- 豐富的體外研究支持 HU 在乳癌中的活性
- 已有 Phase I/II 臨床經驗，尤其在高劑量化療方案中
- 新穎的藥物傳遞系統（如脂質複合體）可能改善療效
- 與其他藥物的協同作用提供聯合治療機會

**若要推進需要：**
- 評估 HU 在現代乳癌治療中的角色（與 CDK4/6 抑制劑、免疫治療的比較或聯合）
- 開發更有效的藥物傳遞系統以提高腫瘤靶向性
- 確定最適合的乳癌亞型（如三陰性乳癌）
- 設計與 valproic acid 或其他增敏劑的聯合用藥方案


---

