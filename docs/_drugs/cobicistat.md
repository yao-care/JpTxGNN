---
layout: default
title: Cobicistat
parent: 僅模型預測 (L5)
nav_order: 50
evidence_level: L5
indication_count: 1
---

# Cobicistat
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

# Cobicistat 藥師筆記

## 一句話總結

Cobicistat 是一種藥動學增強劑（pharmacokinetic enhancer），專門用於 HIV 治療中增加蛋白酶抑制劑的血中濃度，TxGNN 預測其對其他免疫缺乏病毒感染有療效，但這些預測臨床意義有限且缺乏實際應用價值。

---

## 快速總覽

| 項目 | 內容 |
|------|------|
| 藥物名稱 | Cobicistat |
| DrugBank ID | DB09065 |
| 台灣商品名 | 信澤力膜衣錠 (Symtuza)、捷扶康膜衣錠 (Genvoya)、普澤力膜衣錠 (Prezcobix) |
| 原核准適應症 | HIV-1 感染（與其他抗反轉錄病毒藥物併用） |
| 預測新適應症 | 猴免疫缺乏病毒感染、貓免疫缺乏症候群、神經發育障礙 |
| 最高預測分數 | 0.999 (simian/feline immunodeficiency) |
| 證據等級 | L5 (僅預測，無臨床意義) |

---

## 為什麼這個預測合理（或不合理）

### Cobicistat 的特殊藥理角色

Cobicistat 本身 **不具有抗病毒活性**，其作用是：

1. **CYP3A 抑制**：強效抑制 CYP3A 酵素，延緩蛋白酶抑制劑（如 darunavir、atazanavir）及整合酶抑制劑（如 elvitegravir）的代謝
2. **藥動學增強**：使併用藥物維持有效血中濃度，減少給藥頻率

### 預測分析

| 預測適應症 | 分析 |
|------------|------|
| Simian immunodeficiency virus (SIV) | 知識圖譜基於 HIV 關聯推斷，但 cobicistat 本身無抗病毒作用 |
| Feline acquired immunodeficiency syndrome (FIV) | 同上，且獸醫領域無此應用 |
| 神經發育障礙 | 與 cobicistat 作用機轉完全無關，屬誤判 |

**結論**：這些預測反映了知識圖譜方法的局限性 - 它基於關聯性而非因果性，未能區分「藥動學增強劑」與「抗病毒藥物」的本質差異。

---

## 臨床試驗證據

**無** 針對預測適應症的臨床試驗。

所有 cobicistat 相關試驗都是關於其在 HIV 治療中作為藥動學增強劑的角色。

---

## 文獻證據

**無** 支持預測適應症的文獻。

Cobicistat 的所有文獻都聚焦於其藥動學增強作用，而非直接治療效果。

---

## 台灣上市資訊

| 許可證字號 | 商品名 | 成分組成 | 適應症 | 狀態 |
|------------|--------|----------|--------|------|
| 衛部藥輸字第027613號 | 信澤力膜衣錠 (Symtuza) | Darunavir + Cobicistat + Emtricitabine + Tenofovir alafenamide | HIV-1 感染 | 有效 |
| 衛部藥輸字第027001號 | 捷扶康膜衣錠 (Genvoya) | Elvitegravir + Cobicistat + Emtricitabine + Tenofovir alafenamide | HIV-1 感染 | 有效 |
| 衛部藥輸字第027263號 | 普澤力膜衣錠 (Prezcobix) | Darunavir + Cobicistat | HIV-1 感染 | 有效 |

**重點**：Cobicistat 在台灣僅以複方形式上市，不作為單方藥品使用。

---

## 安全性考量

### 重要藥物交互作用

Cobicistat 是強效 CYP3A 抑制劑，藥物交互作用極為廣泛且複雜：

| 交互作用類型 | 代表藥物 | 嚴重程度 |
|--------------|----------|----------|
| **禁忌併用** | Simvastatin, Alfuzosin, Cisapride | Major |
| 類固醇 | Triamcinolone, Budesonide | Major (可能導致庫欣症候群) |
| 鎮痛劑 | Fentanyl, Alfentanil, Hydrocodone | Major |
| 心血管藥物 | Amiodarone, Apixaban | Major |
| 抗癲癇藥 | Fosphenytoin | Major |
| 鎮靜安眠藥 | Alprazolam, Triazolam | Moderate |

### 特別警語

1. **腎功能監測**：Cobicistat 會影響肌酸酐分泌，可能造成血清肌酸酐假性上升
2. **骨質密度**：長期使用需監測骨密度
3. **脂質代謝**：可能影響血脂

---

## 結論與下一步

### 預測評估

| 評估項目 | 結果 |
|----------|------|
| 機轉合理性 | 不合理 - Cobicistat 無直接抗病毒活性 |
| 臨床證據 | 無 |
| 文獻支持 | 無 |
| 整體證據等級 | **L5 (僅預測，無臨床意義)** |

### 方法學反思

此藥物的預測結果凸顯了知識圖譜方法的重要限制：

1. **未區分藥物角色**：將藥動學增強劑誤判為具有直接治療作用
2. **關聯性 vs 因果性**：cobicistat 與 HIV 藥物的關聯被錯誤延伸至其他免疫缺乏症
3. **動物疾病預測**：SIV 和 FIV 的預測在人類醫學無實際應用價值

### 建議

1. **不建議任何臨床延伸使用**：預測結果無科學依據
2. **方法改進方向**：未來知識圖譜模型應納入藥物作用類型標註，區分直接治療效果與輔助增強作用
3. **維持現有適應症**：Cobicistat 應繼續僅用於其核准的 HIV 治療藥動學增強角色

---

*本筆記僅供研究參考，不構成醫療建議。任何用藥決策應諮詢專業醫療人員。*

*最後更新：2026-02-11*


---

