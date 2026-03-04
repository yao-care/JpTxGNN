---
layout: default
title: Alfacalcidol
parent: 中證據等級 (L3-L4)
nav_order: 13
evidence_level: L3
indication_count: 1
---

# Alfacalcidol
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

# Alfacalcidol：從骨質疏鬆到腎小管酸中毒探索

## 一句話總結

Alfacalcidol 原本用於骨質疏鬆症及維生素 D 缺乏相關疾病。
TxGNN 模型預測它可能對**腎小管酸中毒 (renal tubular acidosis)** 有效，
目前有 **8 篇文獻**支持這個方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 骨質疏鬆症、慢性腎不全低血鈣症、副甲狀腺機能低下症、佝僂病、骨軟化症 |
| 預測新適應症 | 腎小管酸中毒 (renal tubular acidosis) |
| TxGNN 預測分數 | 99.27% |
| 證據等級 | L3 |
| 台灣上市 | 已上市 |
| 許可證數 | 多張（部分已註銷） |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

Alfacalcidol（1α-hydroxycholecalciferol）是活性維生素 D3 前驅物，在肝臟轉換為活性形式 1,25(OH)2D3（calcitriol）。其主要作用包括：
1. 促進腸道鈣磷吸收
2. 調節骨代謝
3. 抑制副甲狀腺素分泌
4. 維持鈣磷恆定

腎小管酸中毒 (RTA) 常導致慢性代謝性酸中毒，進而造成：
- 骨骼礦物質流失
- 骨軟化症
- 生長遲緩（兒童）
- 低血鈣及低磷血症

在 RTA 的治療中，除了鹼劑補充外，維生素 D 類藥物是重要的輔助治療，用於：
1. 預防及治療骨軟化症
2. 改善鈣磷代謝異常
3. 促進骨質恢復

多篇文獻顯示 alfacalcidol 在 RTA 合併骨軟化症的患者中可有效改善骨密度及臨床症狀。

## 臨床試驗證據

目前無針對 alfacalcidol 與腎小管酸中毒的註冊臨床試驗。

## 文獻證據

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [33398781](https://pubmed.ncbi.nlm.nih.gov/33398781/) | 2021 | Case Report | CEN Case Rep | 非典型 RTA 合併維生素 D 缺乏導致骨軟化症，alfacalcidol 劑量需增加 |
| [22740247](https://pubmed.ncbi.nlm.nih.gov/22740247/) | 2013 | Case Report | Mod Rheumatol | 乾燥症候群合併 RTA 骨軟化症，risedronate + alfacalcidol + 類固醇治療 24 個月後骨密度恢復正常 |
| [28509074](https://pubmed.ncbi.nlm.nih.gov/28509074/) | 2012 | Case Report | CEN Case Rep | 乾燥症候群合併 RTA 骨軟化症，alfacalcidol 為治療組合之一 |
| [11518137](https://pubmed.ncbi.nlm.nih.gov/11518137/) | 2001 | Case Report | Intern Med | 乾燥症候群合併 RA 及 RTA-1，alfacalcidol + 鈣劑 + elcatonin 治療後骨密度明顯改善 |
| [9134837](https://pubmed.ncbi.nlm.nih.gov/9134837/) | 1997 | Case Report | Nihon Jinzo Gakkai Shi | 成人特發性 Fanconi 症候群，鹼劑 + alfacalcidol 治療 30 個月後骨密度恢復至 82% |
| [6893175](https://pubmed.ncbi.nlm.nih.gov/6893175/) | 1980 | Case Reports | Contrib Nephrol | 不同類型 Fanconi 症候群中 1α-OHVD3 的生物及治療效果，療效為 VD2 的 200-250 倍 |
| [6709109](https://pubmed.ncbi.nlm.nih.gov/6709109/) | 1984 | Case Report | Neth J Med | 原發性膽汁性肝硬化合併 RTA 患者使用 1α-hydroxyvitamin D |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 |
|---------|------|------|-----------|
| 衛署藥製字第044609號 | 阿法鈣斯多 "台耀" | 粉劑 | 維他命 D 缺乏症 |
| 衛署藥製字第040333號 | "漁人" 腎骨全軟膠囊 0.25ug | 軟膠囊劑 | 骨質疏鬆症、慢性腎不全低血鈣症、副甲狀腺機能低下症、維生素 D 抵抗性佝僂病、骨軟化症 |
| 衛署藥輸字第024916號 | 萬乃補軟膠囊 | 軟膠囊劑 | 骨質疏鬆症、維他命 D 缺乏症 |
| 衛署藥輸字第023050號 | 骨精鈣膠囊 1.0ug | 軟膠囊劑 | 骨質疏鬆症、慢性腎不全低血鈣症、副甲狀腺機能低下症 |

## 安全性考量

### 重要藥物交互作用

**Moderate 交互作用：**
- 含鈣制酸劑（Calcium carbonate 等）：可能增加高鈣血症風險
- Digoxin：高鈣血症可增加毛地黃毒性
- Thiazide 利尿劑：增加高鈣血症風險
- Cholestyramine：減少 alfacalcidol 吸收
- Phenytoin、Phenobarbital：加速維生素 D 代謝
- Magnesium 類制酸劑（慢性腎病患者）：增加高鎂血症風險

### 監測項目
- 血清鈣（初期每週，穩定後每月）
- 血清磷
- 腎功能（Creatinine、BUN）
- 24 小時尿鈣（必要時）

### 高鈣血症症狀
- 噁心、嘔吐、便秘
- 多尿、口渴
- 肌肉無力
- 意識改變

安全性資訊請參考原廠仿單。

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
Alfacalcidol 在腎小管酸中毒合併骨軟化症的治療中已有多篇個案報告支持其療效。作為活性維生素 D 衍生物，其能有效改善 RTA 患者因慢性酸中毒導致的鈣磷代謝異常及骨病變。在臨床實務上，alfacalcidol 常與鹼劑（如 sodium bicarbonate、potassium citrate）併用，作為 RTA 的標準治療組合。

**若要推進需要：**
- 同時補充鹼劑矯正代謝性酸中毒
- 密切監測血鈣，避免高鈣血症
- 監測腎功能及尿鈣排泄
- 考慮合併使用雙磷酸鹽類藥物改善骨密度
- 設計前瞻性研究，探討最佳劑量及治療時程


---

