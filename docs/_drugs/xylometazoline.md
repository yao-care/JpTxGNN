---
layout: default
title: Xylometazoline
parent: 中證據等級 (L3-L4)
nav_order: 199
evidence_level: L3
indication_count: 1
---

# Xylometazoline
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

# Xylometazoline：從過敏性鼻炎到鼻腔疾病的廣泛應用

## 一句話總結

Xylometazoline 原本用於緩解鼻塞、過敏性鼻炎等症狀。
TxGNN 模型預測它可能對**鼻腔疾病 (nasal cavity disease)** 和**急性咽喉炎 (acute laryngopharyngitis)** 有效，
有 **2 個臨床試驗**和 **7 篇文獻**支持鼻腔疾病方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 感冒、鼻塞、過敏性鼻炎 |
| 預測新適應症 | 鼻腔疾病、急性咽喉炎 |
| TxGNN 預測分數 | 99.91% (鼻腔疾病)、99.89% (急性咽喉炎) |
| 證據等級 | L3 (有文獻支持) |
| 台灣上市 | 已上市 |
| 許可證數 | 24 張 (多張有效) |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

Xylometazoline 是一種 alpha 腎上腺素受體激動劑，作用於鼻黏膜血管，
使血管收縮而達到減少鼻腔充血的效果。其作用標靶包括：

- **alpha-1D 腎上腺素受體** (ADRA1D)
- **alpha-2A 腎上腺素受體** (ADRA2A)
- **alpha-2B 腎上腺素受體** (ADRA2B)
- **alpha-2C 腎上腺素受體** (ADRA2C)

由於其本身就是作用於鼻腔的血管收縮劑，預測其對鼻腔疾病有效在機轉上完全合理。
這個預測更像是確認現有適應症的延伸，而非真正的「老藥新用」。

## 臨床試驗證據

| 試驗編號 | 階段 | 狀態 | 人數 | 主要發現 |
|---------|------|------|------|---------|
| [NCT05072392](https://clinicaltrials.gov/study/NCT05072392) | N/A | UNKNOWN | 80 | 研究 Foley 導管輔助鼻腔插管對成人患者鼻出血的影響 |
| [NCT06443255](https://clinicaltrials.gov/study/NCT06443255) | Phase 3 | COMPLETED | 16 | 比較 cocaine、lidocaine/xylometazoline 和生理食鹽水在鼻腔鎮痛的效果 |

## 文獻證據

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [24023995](https://pubmed.ncbi.nlm.nih.gov/24023995/) | 2013 | 臨床研究 | Korean J Anesthesiol | Xylometazoline 噴霧可有效擴張鼻腔 |
| [8740084](https://pubmed.ncbi.nlm.nih.gov/8740084/) | 1996 | RCT | Arzneimittel-Forschung | 比較 tuaminoheptane/NAC 與 xylometazoline 在減少鼻阻力的效果 |
| [34783482](https://pubmed.ncbi.nlm.nih.gov/34783482/) | 2021 | 回顧 | Vestn Otorinolaringol | 0.1% xylometazoline 結合 5% dexpanthenol 可改善老年人鼻腔黏膜再生 |
| [22427029](https://pubmed.ncbi.nlm.nih.gov/22427029/) | 2013 | RCT | Eur Arch Otorhinolaryngol | 比較棉塞填塞與局部噴霧在鼻內視鏡前準備的效果 |
| [1281924](https://pubmed.ncbi.nlm.nih.gov/1281924/) | 1992 | 臨床研究 | Rhinology | Xylometazoline 可顯著降低鼻氣道阻力並消除不對稱性 |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 許可證持有者 | 狀態 |
|---------|------|------|-------------|------|
| 衛部藥製字第061432號 | 大豐克敏通噴鼻液 0.1% | 鼻用噴液劑 | 大豐製藥 | 有效 |
| 衛部藥製字第059249號 | 強生欣鼻通噴鼻液 0.1% | 鼻用噴液劑 | 強生化學製藥 | 有效 |
| 衛署藥製字第043631號 | 斯斯鼻通噴鼻液 0.1% | 鼻用噴液劑 | 五洲製藥 | 有效 |
| 衛署藥輸字第024654號 | 歐治鼻噴鼻液 0.1% | 鼻用噴液劑 | 英商赫力昂 | 有效 |
| 衛署藥製字第047345號 | 大正百保能噴鼻液 0.1% | 鼻用噴液劑 | 台灣大正製藥 | 有效 |

## 安全性考量

- **藥物交互作用**：作用於 alpha-腎上腺素受體，與其他交感神經藥物併用需謹慎。
- **使用限制**：連續使用不宜超過 7 天，以避免藥物性鼻炎 (rhinitis medicamentosa)。
- **禁忌**：閉角型青光眼、嚴重高血壓患者應謹慎使用。

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
Xylometazoline 在鼻腔疾病中的應用與其原適應症高度相關，機轉明確且有充足的臨床證據支持。
預測的「鼻腔疾病」實際上是原適應症的泛化表述，臨床上已廣泛應用。

**若要推進需要：**
- 對於急性咽喉炎適應症，需要額外的臨床證據
- 針對特定鼻腔疾病亞型的療效評估
- 長期使用安全性監測


---

