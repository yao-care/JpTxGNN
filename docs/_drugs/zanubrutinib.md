---
layout: default
title: Zanubrutinib
parent: 高證據等級 (L1-L2)
nav_order: 200
evidence_level: L2
indication_count: 1
---

# Zanubrutinib
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

# Zanubrutinib：從 B 細胞淋巴瘤到骨髓性白血病

## 一句話總結

Zanubrutinib 原本用於治療被套細胞淋巴瘤、華氏巨球蛋白血症等 B 細胞惡性腫瘤。
TxGNN 模型預測它可能對**骨髓性白血病 (myeloid leukemia)** 有效，
有 **2 個臨床試驗**和 **9 篇文獻**支持這個方向。

## 快速總覽

| 項目 | 內容 |
|------|------|
| 原適應症 | 被套細胞淋巴瘤 (MCL)、華氏巨球蛋白血症 (WM)、CLL/SLL、邊緣區淋巴瘤、濾泡性淋巴瘤 |
| 預測新適應症 | 骨髓性白血病 (myeloid leukemia) |
| TxGNN 預測分數 | 99.65% |
| 證據等級 | L2 (有臨床試驗支持) |
| 台灣上市 | 已上市 |
| 許可證數 | 1 張 (有效) |
| 建議決策 | Proceed with Guardrails |

## 為什麼這個預測合理？

Zanubrutinib 是高選擇性的布魯頓酪氨酸激酶 (BTK) 抑制劑。
BTK 在 B 細胞受體 (BCR) 訊號傳遞中扮演關鍵角色，抑制 BTK 可阻斷惡性 B 細胞的增殖與存活。

**作用機轉：**
- 抑制 BTK (Bruton tyrosine kinase)，IC50 約 20 nM
- 相較於 ibrutinib，具有更高的 BTK 選擇性
- 較少 off-target 效應，心房顫動等副作用較低

雖然 BTK 主要表現於 B 細胞，但近年研究發現 BTK 在某些骨髓性惡性腫瘤中也有表現，
這可能是預測 zanubrutinib 對骨髓性白血病有效的機轉基礎。

## 臨床試驗證據

| 試驗編號 | 階段 | 狀態 | 人數 | 主要發現 |
|---------|------|------|------|---------|
| [NCT05665530](https://clinicaltrials.gov/study/NCT05665530) | Phase 1 | COMPLETED | 86 | PRT2527 (CDK9 抑制劑) 與 zanubrutinib 併用治療復發/難治性血液惡性腫瘤 |
| [NCT04477291](https://clinicaltrials.gov/study/NCT04477291) | Phase 1a/b | TERMINATED | 45 | CG-806 (luxeptinib) 治療復發/難治性急性骨髓性白血病或高風險 MDS |

## 文獻證據

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [39647999](https://pubmed.ncbi.nlm.nih.gov/39647999/) | 2025 | RCT Phase 3 | J Clin Oncol | SEQUOIA 試驗 5 年追蹤：zanubrutinib vs BR 在初治 CLL/SLL |
| [40334067](https://pubmed.ncbi.nlm.nih.gov/40334067/) | 2025 | Phase 2 | Blood Advances | Zanubrutinib 在 ibrutinib/acalabrutinib 不耐受患者中耐受性良好 |
| [40829104](https://pubmed.ncbi.nlm.nih.gov/40829104/) | 2026 | 跨試驗分析 | Blood Advances | Zanubrutinib 在 del(17p)/TP53 突變 CLL/SLL 患者中的療效分析 |
| [34959482](https://pubmed.ncbi.nlm.nih.gov/34959482/) | 2021 | 回顧 | Pharmaceutics | TKI 時代的慢性白血病：BTK 抑制劑在 CLL 中的角色 |
| [36402930](https://pubmed.ncbi.nlm.nih.gov/36402930/) | 2023 | 回顧 | Leukemia | BTK 抑制劑在華氏巨球蛋白血症中的應用 |

## 台灣上市資訊

| 許可證號 | 品名 | 劑型 | 許可證持有者 | 核准日期 |
|---------|------|------|-------------|---------|
| 衛部藥輸字第028160號 | 百悅澤膠囊 80 毫克 | 膠囊劑 | 臺灣百濟神州有限公司 | 2021/09/15 |

**核准適應症：**
1. 先前曾接受至少一種治療的被套細胞淋巴瘤 (MCL) 成人病人
2. 華氏巨球蛋白血症 (WM) 成人病人
3. 先前曾接受至少一種抗 CD20 療法的復發或頑固型邊緣區淋巴瘤 (MZL) 成人病人
4. 慢性淋巴球性白血病 (CLL)/小淋巴球性淋巴瘤 (SLL) 成人病人
5. 併用 obinutuzumab 適用於先前曾接受至少 2 種治療的濾泡性淋巴瘤 (FL) 成人病人

## 細胞毒性

| 項目 | 內容 |
|------|------|
| 細胞毒性分類 | 標靶治療藥物 (非傳統細胞毒性) |
| 骨髓抑制風險 | 中度 (嗜中性白血球減少、血小板減少) |
| 出血風險 | 需注意，尤其與抗凝血劑併用時 |
| 監測項目 | CBC (含分類)、肝功能、出血徵兆 |
| 處置防護 | 口服藥物，依一般藥物處置規範操作 |

## 安全性考量

**主要藥物交互作用 (Major)：**

| 藥物類別 | 代表藥物 | 交互作用機轉 |
|---------|---------|-------------|
| 抗凝血劑/抗血小板 | Warfarin, Apixaban, Clopidogrel, Aspirin | 增加出血風險 |
| CYP3A 強效抑制劑 | Ketoconazole, Clarithromycin, Cobicistat | 增加 zanubrutinib 血中濃度 |
| CYP3A 強效誘導劑 | Enzalutamide, Apalutamide, Mitotane | 降低 zanubrutinib 血中濃度 |
| 其他 BTK 抑制劑 | Ibrutinib, Acalabrutinib | 藥理作用重疊 |
| 免疫抑制劑 | Adalimumab, Etanercept, Infliximab | 增加感染風險 |

**注意事項：**
- 接受手術前需暫停使用 (術前至少 3-7 天)
- B 型肝炎再活化風險，需監測 HBsAg/anti-HBc
- 心房顫動風險較 ibrutinib 低，但仍需監測

## 結論與下一步

**決策：Proceed with Guardrails**

**理由：**
雖然 zanubrutinib 的主要作用在 B 細胞，但其在血液惡性腫瘤中的廣泛療效已獲證實。
針對骨髓性白血病的預測有初步臨床試驗支持，但這些試驗主要探討聯合用藥而非單獨使用。

**若要推進需要：**
- 確認 BTK 在骨髓性白血病中的表現與功能
- 設計專門針對骨髓性白血病的 Phase 1/2 臨床試驗
- 評估與現有骨髓性白血病治療藥物的聯合效果
- 建立生物標記預測可能受益的患者亞群


---

