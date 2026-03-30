---
layout: default
title: Gemcitabine
parent: 高エビデンス (L1-L2)
nav_order: 76
evidence_level: L2
indication_count: 1
---

# Gemcitabine
{: .fs-9 }

エビデンスレベル: **L2** | 予測適応症: **1** 件
{: .fs-6 .fw-300 }

---

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist">

## 薬剤師評価レポート

</div>

# Gemcitabine：從轉移性大腸直腸癌到女性乳腺癌

## 一言まとめ

Gemcitabine 原本用於治療多種癌症，包括轉移性大腸直腸癌。
TxGNN 模型預測它可能對**女性乳腺癌 (female breast carcinoma)** 有效，
目前有 **10 個臨床試驗**和 **12 篇文獻**支持這個方向。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 轉移性大腸直腸癌 |
| 予測新適応症 | 女性乳腺癌 (female breast carcinoma) |
| TxGNN 予測スコア | 99.98% |
| エビデンスレベル | L2 |
| 日本上市 | ✓ 已上市 |
| 承認数 | 20 張 |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

目前缺乏詳細的作用機轉資料。根據已知資訊，Gemcitabine 是抗癌藥物的一部分，
其成分在轉移性大腸直腸癌中的療效已被證實，機轉上可能適用於女性乳腺癌。

## 臨床試験エビデンス

| 試驗編號 | 階段 | 狀態 | 人數 | 主要發現 |
|---------|------|------|------|---------|
| [NCT06027268](https://clinicaltrials.gov/study/NCT06027268) | Phase 2 | ACTIVE_NOT_RECRUITING | 36 | 測試 trilaciclib、pembrolizumab、gemcitabine 和 carboplatin 在局部晚期不可切除或轉移性三陰性乳腺癌中的組合效果 |
| [NCT00561119](https://clinicaltrials.gov/study/NCT00561119) | Phase 3 | COMPLETED | 326 | 比較 gemcitabine 和 paclitaxel 在轉移性乳腺癌中的維持治療效果 |
| [NCT02139358](https://clinicaltrials.gov/study/NCT02139358) | Phase 1/2 | COMPLETED | 15 | 評估 gemcitabine 與 trastuzumab 和 pertuzumab 在 HER2+ 乳腺癌中的安全性和活性 |
| [NCT00006459](https://clinicaltrials.gov/study/NCT00006459) | Phase 3 | COMPLETED | N/A | 比較 gemcitabine 和 paclitaxel 在不可切除的局部復發或轉移性乳腺癌中的效果 |
| [NCT00003540](https://clinicaltrials.gov/study/NCT00003540) | Phase 2 | COMPLETED | 30 | 研究 gemcitabine 在先前接受過 Adriamycin 和 Taxol 治療的轉移性乳腺癌患者中的效果 |

## 文献エビデンス

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [40779028](https://pubmed.ncbi.nlm.nih.gov/40779028/) | 2025 | RCT | Breast cancer research and treatment | 研究 mifepristone、carboplatin 和 gemcitabine 在 GR-positive 乳腺癌中的效果 |
| [24824628](https://pubmed.ncbi.nlm.nih.gov/24824628/) | 2015 | RCT | International journal of cancer | 評估 cisplatin 和 gemcitabine 在轉移性三陰性乳腺癌中的第一線療效 |
| [12057039](https://pubmed.ncbi.nlm.nih.gov/12057039/) | 2002 | In vitro | Clinical breast cancer | 研究 gemcitabine 和 trastuzumab 在乳腺和肺癌細胞中的作用 |
| [15685819](https://pubmed.ncbi.nlm.nih.gov/15685819/) | 2004 | Review | Oncology (Williston Park, N.Y.) | 分析 gemcitabine 和 paclitaxel 在轉移性乳腺癌中的療效 |
| [14754469](https://pubmed.ncbi.nlm.nih.gov/14754469/) | 2004 | Review | Clinical breast cancer | 討論 gemcitabine 和 trastuzumab 在 HER2/neu 過度表現的乳腺癌中的組合療效 |

## 日本上市情報

| 承認番号 | 品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 衛部菌疫輸字第001117號 | 艾法施注射液 | 注射液劑 | 轉移性大腸直腸癌、轉移性乳癌、惡性神經膠質瘤、非鱗狀非小細胞肺癌、子宮頸癌、卵巢上皮細胞癌 |

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 傳統細胞毒性藥物 |
| 骨髓抑制風險 | 中度 |
| 致吐性分級 | 中度 |
| 監測項目 | CBC（含分類）、肝腎功能 |
| 處置防護 | 需依細胞毒性藥物處置規範操作 |

## 安全性に関する考慮事項

- **藥物交互作用**：與 Naltrexone 可能有中度交互作用，與 Levofloxacin 有輕微交互作用。

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
Gemcitabine 在乳腺癌中的多項臨床試驗顯示出潛在療效，且有多篇文獻支持其在乳腺癌中的應用。

**推進に必要な事項：**
- 更詳細的作用機轉資料（MOA）
- 特定族群的安全性監測計畫

---

