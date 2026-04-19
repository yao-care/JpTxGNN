---
layout: default
title: Inclisiran
parent: モデル予測のみ (L5)
nav_order: 85
evidence_level: L5
indication_count: 1
---

# Inclisiran
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

# Inclisiran：從高膽固醇血症到 Potassium Deficiency Disease

## 一言まとめ

Inclisiran 原本用於原發性高血脂症的 LDL-C 降低治療。
TxGNN 模型預測它可能對 **Potassium Deficiency Disease** 有效，
但目前缺乏臨床試驗和文獻支持這個方向。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 原發性高血脂症(含異合子家族性高膽固醇血症)之 LDL-C 降低 |
| 予測新適応症 | Potassium Deficiency Disease |
| TxGNN 予測スコア | 99.93% |
| エビデンスレベル | L5 |
| 日本上市 | 已上市 |
| 承認数 | 1 張(3筆重複記錄) |
| 推奨判断 | Hold |

## この予測が妥当な理由

Inclisiran 是一種小干擾 RNA (siRNA) 藥物，透過抑制肝臟中 PCSK9 蛋白的合成來增加 LDL 受體的表現，進而降低血液中的 LDL 膽固醇濃度。

與鉀缺乏症的關聯目前缺乏明確的機轉解釋：
1. Inclisiran 的主要作用靶點為 PCSK9，與鉀代謝無直接關聯
2. 目前沒有臨床或臨床前研究探討 Inclisiran 對鉀代謝的影響
3. 此預測可能源於知識圖譜中的間接關聯，需要進一步驗證

## 臨床試験エビデンス

目前無相關臨床試驗登記

**注意**：有 2 項進行中的 Inclisiran 兒童家族性高膽固醇血症試驗([NCT06597006](https://clinicaltrials.gov/study/NCT06597006)、[NCT06597019](https://clinicaltrials.gov/study/NCT06597019))，但與鉀缺乏症無關。

## 文献エビデンス

目前無相關文獻

## 日本上市情報

| 承認番号 | 品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 衛部藥輸字第028761號 | 樂脂益注射劑 | 注射液劑 | 原發性高血脂症(含異合子家族性高膽固醇血症)作為飲食及降血脂藥品的輔助治療 |

## 安全性に関する考慮事項

- **藥物交互作用**：目前 DDI 資料庫中未發現顯著交互作用

- **已知副作用**：注射部位反應、上呼吸道感染、肌肉骨骼疼痛

## 結論と次のステップ

**判断：Hold**

**理由：**
Inclisiran 用於鉀缺乏症的預測缺乏明確的機轉支持和臨床證據。目前無任何臨床試驗或文獻探討此關聯性。

**推進に必要な事項：**
- 進行機轉層面的研究，探討 PCSK9 抑制與鉀代謝的潛在關聯
- 分析 Inclisiran 臨床試驗中的電解質變化數據
- 建立假說並設計探索性臨床研究


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
