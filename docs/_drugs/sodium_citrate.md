---
layout: default
title: Sodium Citrate
parent: 僅模型預測 (L5)
nav_order: 158
evidence_level: L5
indication_count: 1
---

# Sodium Citrate
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

# Sodium Citrate（檸檬酸鈉）：從抗凝血劑到胃部疾病輔助治療之探索

## 一句話總結

Sodium Citrate 主要作為抗凝血劑及袪痰劑使用，TxGNN 預測其可能對胃部疾病具有輔助治療潛力，並有多篇文獻支持其在胃癌抑制及胃黏膜保護方面的作用。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 抗凝血劑、袪痰劑、促進利尿、制酸 |
| 預測新適應症 | 胃部疾病（stomach disease）、胃十二指腸炎（gastroduodenitis） |
| TxGNN 預測分數 | 0.999（stomach disease） |
| 證據等級 | L3（有多篇 PubMed 文獻及臨床試驗） |
| 台灣上市 | 有效許可證存在 |
| 許可證數 | 多張（含已註銷） |
| 建議決策 | Watch |

## 為什麼這個預測合理？

### 胃部疾病（Stomach Disease）- TxGNN 分數 0.999

**機轉假說：**
Sodium Citrate 透過抑制糖解作用（glycolysis）來抑制腫瘤細胞生長。研究顯示其可抑制磷酸果糖激酶（phosphofructokinase, PFK）活性，減少 ATP 和乳酸生成，並誘導粒線體介導的凋亡途徑。

**文獻支持：**
1. **2016 年 Biochemical and Biophysical Research Communications（PMID: 27163639）**：研究證實 Sodium Citrate 可抑制人類胃癌細胞株 MGC-803 的增殖，透過阻斷糖解作用並促進粒線體凋亡途徑。

2. **2016 年 Oncology Reports（PMID: 26708213）**：在胃癌原位移植瘤模型中，Sodium Citrate 可抑制腫瘤生長、誘導細胞凋亡，並下調抗凋亡蛋白 Survivin。

3. **2018 年 Oncology Reports（PMID: 29115645）**：利用 18F-FDG PET/CT 影像證實 Sodium Citrate 在活體內可抑制胃癌糖解代謝及腫瘤生長。

### 胃十二指腸炎（Gastroduodenitis）- TxGNN 分數 0.996

**機轉假說：**
Sodium Citrate 可調節胃內 pH 值，對胃黏膜具有保護作用。

**文獻支持：**
- 1991 年研究（PMID: 1777551）顯示 Sodium Citrate 與 glucose 的配方可減少非類固醇消炎藥引起的胃腸道損傷。
- 1999 年研究（PMID: 10499455）指出含有 monosodium citrate 的發泡錠具有制酸能力，可快速緩解胃酸逆流症狀。

## 臨床試驗

與 Sodium Citrate 及胃部疾病相關的臨床試驗眾多，主要集中在：

| 試驗編號 | 標題 | 階段 | 狀態 |
|---------|------|------|------|
| NCT03050359 | TAK-438 vs Lansoprazole 治療十二指腸潰瘍 | Phase 3 | 完成 |
| NCT03050307 | TAK-438 vs Lansoprazole 治療胃潰瘍 | Phase 3 | 完成 |
| NCT02891447 | 胃癌細胞減積術與 HIPEC | Phase 2 | 完成 |
| NCT05753306 | 機器人輔助胃癌 HIPEC 手術 | Phase 2 | 招募中 |

## 相關文獻

| PMID | 標題 | 年份 | 相關性 |
|------|------|------|--------|
| 27163639 | 3-Bromopyruvate and sodium citrate induce apoptosis in gastric cancer | 2016 | 高 |
| 26708213 | Sodium citrate target glycolysis in gastric cancer cells | 2016 | 高 |
| 29115645 | 18F-FDG PET/CT evaluation of glycolysis-targeted therapy | 2018 | 高 |
| 35934181 | 5-ALA and sodium ferrous citrate in gastric cancer | 2022 | 中 |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 | 狀態 |
|---------|------|------|-----------|------|
| 衛部藥輸字第027649號 | "萬益特"局部抗凝檸檬酸血液過濾用溶液 | 透析用液劑 | 連續性腎功能替代治療 | 有效 |
| 衛署藥製字第039569號 | "信東" 抗凝血劑枸櫞酸鈉溶液4% | 注射劑 | 輸血抗凝血劑 | 有效 |
| 內衛藥製字第002962號 | 輸血用枸櫞酸鈉針 | 注射劑 | 輸血用抗凝結劑 | 有效 |

## 安全性考量

- **警語與禁忌症**：尚無詳細仿單資訊
- **藥物交互作用**：未發現已知的重大藥物交互作用資料
- **特殊族群**：
  - 高劑量可能導致代謝性鹼中毒
  - 需注意與其他電解質的交互作用

**備註**：Sodium Citrate 作為抗凝血劑及輔助劑安全性良好，但在抗腫瘤應用上需進一步評估劑量及給藥途徑。

## 結論與下一步

**決策：Watch**

**理由：**
TxGNN 預測分數極高（0.999），且有多篇高品質體外及動物實驗文獻支持 Sodium Citrate 抑制胃癌細胞的機轉。然而，目前證據仍限於基礎研究階段，尚無針對此適應症的人體臨床試驗。

**若要推進需要：**
- 確立人體安全的抗腫瘤劑量
- 評估口服或靜脈給藥的可行性
- 設計 Phase I 安全性試驗
- 探索與現有胃癌化療藥物的協同作用
- 考慮作為化療增敏劑而非單一療法的定位


---

