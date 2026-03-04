---
layout: default
title: Acetazolamide
parent: 高證據等級 (L1-L2)
nav_order: 11
evidence_level: L2
indication_count: 1
---

# Acetazolamide
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

# Acetazolamide：從青光眼利尿到心肌病變探索

## 一句話總結

Acetazolamide 原本用於青光眼及利尿。
TxGNN 模型預測它可能對**心肌病變 (cardiomyopathy)** 及**肥厚性心肌病變 (hypertrophic cardiomyopathy)** 有效，
目前有 **3 個臨床試驗**和 **10 篇文獻**支持這個方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 青光眼、癲癇、充血性心衰竭水腫 |
| 預測新適應症 | 心肌病變 (cardiomyopathy) |
| TxGNN 預測分數 | 99.83% |
| 證據等級 | L2 |
| 台灣上市 | 已上市 |
| 許可證數 | 22 張（部分已註銷） |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

Acetazolamide 是碳酸酐酶抑制劑，傳統上用於青光眼和利尿。近年研究發現其在急性失代償性心衰竭中的應用價值顯著提升。

ADVOR 試驗 (2022) 顯示，acetazolamide 加上 loop diuretics 可顯著改善急性心衰竭患者的去鬱血效果。其機轉包括：
1. 抑制近端腎小管碳酸酐酶，增加鈉離子排泄
2. 克服利尿劑抵抗
3. 調節電解質平衡（特別是氯離子）

對於心肌病變患者，常伴隨心衰竭症狀，acetazolamide 作為輔助利尿劑的角色已獲臨床驗證。此外，2018 年日本個案報告顯示，acetazolamide 可用於治療肥厚性心肌病變合併低氯血症患者。

## 臨床試驗證據

| 試驗編號 | 階段 | 狀態 | 人數 | 主要發現 |
|---------|------|------|------|---------|
| [NCT05802849](https://clinicaltrials.gov/study/NCT05802849) | Phase 4 | RECRUITING | 400 | 評估 acetazolamide 口服在失代償性心衰竭（包括心肌病變）中的療效 |
| [NCT06166654](https://clinicaltrials.gov/study/NCT06166654) | Phase 4 | RECRUITING | 939 | 比較 loop diuretics 合併 Metolazone 或 Acetazolamide 在急性心衰竭容量過負荷的效果 |
| [NCT06092437](https://clinicaltrials.gov/study/NCT06092437) | N/A | RECRUITING | 466 | TAILOR-AHF：尿鈉導向的利尿劑演算法研究 |

## 文獻證據

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [38806171](https://pubmed.ncbi.nlm.nih.gov/38806171/) | 2025 | Review | ESC heart failure | 2024 心衰竭更新：肯定 acetazolamide 加 loop diuretics 的聯合療法 |
| [37169875](https://pubmed.ncbi.nlm.nih.gov/37169875/) | 2023 | Journal Article | Eur Heart J Cardiovasc Pharmacother | 2022 年心血管藥理進展回顧，acetazolamide 聯合 loop diuretics 被納入標準治療 |
| [30279861](https://pubmed.ncbi.nlm.nih.gov/30279861/) | 2018 | Case Report | J Cardiol Cases | 肥厚性心肌病變合併低氯血症，使用 acetazolamide 成功矯正電解質 |
| [742352](https://pubmed.ncbi.nlm.nih.gov/742352/) | 1978 | Journal Article | Acta Neurol Scand | 低鉀週期性麻痺與心肌病變之關聯研究 |
| [7324871](https://pubmed.ncbi.nlm.nih.gov/7324871/) | 1981 | Case Report | Acta Neurol Scand | 家族性低鉀週期性麻痺中發現心肌疾病證據 |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 核准適應症 |
|---------|------|------|-----------|
| 內衛藥製字第007548號 | "人人" 乙醯偶氮胺錠 | 錠劑 | 青光眼及水腫、癲癇輔助治療 |
| 衛部藥輸字第027543號 | 乙醯偶氮胺 | 粉劑 | 碳酸酐酶抑制藥 |
| 衛署藥製字第023932號 | "新喜" 壓作錠 | 錠劑 | 青光眼、充血性心不全之水腫 |
| 衛署藥製字第007819號 | 安賜他明錠 | 錠劑 | 青光眼及水腫、癲癇輔助治療 |

## 安全性考量

### 重要藥物交互作用

**Major 交互作用：**
- Aspirin（高劑量）：增加 acetazolamide 毒性風險，可能引起代謝性酸中毒

**Moderate 交互作用：**
- 降血糖藥物（各類口服降糖藥、胰島素）：可能影響血糖控制
- Amphotericin B：增加低鉀血症風險
- 類固醇（Betamethasone、Budesonide 等）：增加低鉀血症風險
- Bisacodyl：電解質失衡風險
- Digoxin：低鉀可能增加毛地黃毒性
- Lithium：可能增加鋰毒性
- Metformin：可能增加乳酸酸中毒風險
- Carbamazepine、Phenytoin：可能影響抗癲癇藥血中濃度
- Topiramate：增加代謝性酸中毒和腎結石風險

### 禁忌症
- 磺胺類藥物過敏
- 嚴重肝功能不全
- 低鈉血症或低鉀血症
- 代謝性酸中毒
- 艾迪森氏症

安全性資訊請參考原廠仿單。

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
Acetazolamide 在急性失代償性心衰竭的輔助利尿角色已有高品質 RCT 證據支持（ADVOR 試驗），且目前有多個第四期臨床試驗正在進行中。對於心肌病變合併心衰竭的患者，acetazolamide 可作為克服利尿劑抵抗的有效選擇。

**若要推進需要：**
- 密切監測電解質（特別是鉀、鈉、氯、碳酸氫根）
- 避免與高劑量 aspirin 併用
- 監測腎功能及酸鹼平衡
- 評估是否有磺胺類過敏史


---

