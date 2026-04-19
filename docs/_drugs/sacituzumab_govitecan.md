---
layout: default
title: Sacituzumab Govitecan
parent: モデル予測のみ (L5)
nav_order: 151
evidence_level: L5
indication_count: 1
---

# Sacituzumab Govitecan
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **1** 件
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

# Sacituzumab Govitecan：從三陰性乳癌到新適應症探索

## 一言まとめ

Sacituzumab govitecan 原本用於治療晚期三陰性乳癌及 HR+/HER2- 乳癌。TxGNN 模型預測它可能對**藥物誘發性骨質疏鬆症 (drug-induced osteoporosis)** 有效，但目前僅有模型預測支持，缺乏臨床證據。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 晚期三陰性乳癌、HR+/HER2- 乳癌 |
| 予測新適応症 | 藥物誘發性骨質疏鬆症 (drug-induced osteoporosis) |
| TxGNN 予測スコア | 99.78% |
| エビデンスレベル | L5 |
| 日本上市 | 已上市 |
| 承認数 | 3 張 |
| 推奨判断 | Hold |

## この予測が妥当な理由

Sacituzumab govitecan 是一種抗體藥物複合體（ADC），由抗 Trop-2 抗體與 SN-38（irinotecan 的活性代謝物）連結：

1. **Trop-2 靶點**：Trop-2（tumor-associated calcium signal transducer 2）主要在上皮細胞表達，在多種實體腫瘤中過度表達。

2. **細胞毒性機轉**：SN-38 是拓撲異構酶 I 抑制劑，主要用於抗腫瘤治療。

3. **預測適應症的合理性存疑**：藥物誘發性骨質疏鬆症與 Trop-2 或拓撲異構酶 I 抑制劑的作用機轉缺乏明確關聯，此預測的生物學合理性較低。

## 臨床試験エビデンス

目前無 Sacituzumab govitecan 用於藥物誘發性骨質疏鬆症的臨床試驗登記。

## 文献エビデンス

目前無相關文獻支持。

## 日本上市情報

| 承認番号 | 品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 衛部菌疫輸字第001206號 | 拓達維注射劑 | 凍晶注射劑 | 1. 適用於治療先前已接受兩次以上全身性治療無效之無法切除的局部晚期或轉移性三陰性乳癌成年病人。2. 適用於治療 HR+/HER2- 乳癌，過去曾接受至少2次轉移性乳癌全身性治療的成年病人。 |

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 抗體藥物複合體 (ADC) |
| 骨髓抑制風險 | 高 - 中性粒細胞減少症是常見嚴重不良反應 |
| 致吐性分級 | 中度 |
| 監測項目 | 完整血球計數、肝腎功能、腹瀉症狀 |
| 處置防護 | 需遵循細胞毒性藥物處理標準 |

## 安全性に関する考慮事項

### 重大な薬物相互作用

| 交互作用藥物 | 嚴重程度 | 來源 |
|-------------|---------|------|
| Deferiprone | 重大 | DDInter |
| Irinotecan | 重大 | DDInter |
| Leflunomide | 重大 | DDInter |
| Natalizumab | 重大 | DDInter |
| Adalimumab | 重大 | DDInter |
| Infliximab | 重大 | DDInter |
| Etanercept | 重大 | DDInter |
| Fingolimod | 重大 | DDInter |
| Apalutamide | 重大 | DDInter |

### 藥理學標靶

| 標靶 | 基因名稱 | 說明 |
|-----|---------|------|
| TROP-2 (tumor associated calcium signal transducer 2) | TACSTD2 | Sacituzumab govitecan 的抗體部分與 TROP-2 結合 |

### 重要な警告

- **嚴重中性粒細胞減少症**：可能導致發熱性中性粒細胞減少症
- **嚴重腹瀉**：SN-38 可引起嚴重腹瀉
- **過敏反應**：輸注相關反應
- **UGT1A1 多型性**：UGT1A1*28 同型合子患者可能有更高毒性風險

## 結論と次のステップ

**判断：Hold**

**理由：**
1. 預測適應症（藥物誘發性骨質疏鬆症）與藥物作用機轉缺乏生物學合理性
2. 無臨床試驗或文獻證據支持
3. 作為細胞毒性藥物，用於非惡性疾病的安全性堪慮
4. 成本效益比不適合骨質疏鬆症適應症

**推進に必要な事項：**
- 發現 Trop-2 在骨代謝中的相關作用
- 基礎研究證明機轉合理性
- 考慮到毒性，此適應症不建議進一步探索


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
