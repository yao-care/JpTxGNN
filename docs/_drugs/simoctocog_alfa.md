---
layout: default
title: Simoctocog Alfa
parent: モデル予測のみ (L5)
nav_order: 156
evidence_level: L5
indication_count: 1
---

# Simoctocog Alfa
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

# Simoctocog Alfa：從 A 型血友病到其他出血性疾病探索

## 一言まとめ

Simoctocog Alfa（寧衛 Nuwiq）是治療 A 型血友病的基因工程第八凝血因子。
TxGNN 模型預測它可能對**類乙型威勒布蘭氏病 (Pseudo-von Willebrand Disease)** 及其他血小板/凝血功能異常疾病有效，
但目前缺乏臨床試驗及文獻支持這些新適應症。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 治療與預防 A 型血友病（先天性第八凝血因子缺乏）病人的出血 |
| 予測新適応症 | Pseudo-von Willebrand Disease（類乙型威勒布蘭氏病） |
| TxGNN 予測スコア | 99.997% |
| エビデンスレベル | L5 |
| 日本上市 | 已上市 |
| 承認数 | 9 張（250/500/1000 IU 三種規格） |
| 推奨判断 | Hold |

## この予測が妥当な理由

Simoctocog Alfa 是一種重組第八凝血因子（FVIII），由人類胚胎腎細胞（HEK293）生產，
用於補充 A 型血友病患者缺乏的凝血因子。其作用機轉為：
- 作為輔因子與活化的第九因子（FIXa）結合
- 加速第十因子（FX）的活化
- 最終促進凝血級聯反應完成止血

**TxGNN 預測的前十名新適應症：**

| 排名 | 預測適應症 | 預測分數 | TxGNN 排名 | 機轉關聯性 |
|------|-----------|---------|-----------|----------|
| 1 | Pseudo-von Willebrand Disease（類乙型威勒布蘭氏病） | 99.997% | 164 | 中等 |
| 2 | Primary Release Disorder of Platelets（血小板原發性釋放障礙） | 99.997% | 179 | 低 |
| 3 | Glanzmann Thrombasthenia（葛蘭茲曼血小板無力症） | 99.995% | 307 | 低 |
| 4 | Scott Syndrome（斯科特症候群） | 99.969% | 1,244 | 中等 |
| 5 | Acquired Coagulation Factor Deficiency（後天性凝血因子缺乏） | 99.952% | 1,615 | 高 |
| 6 | Bleeding Diathesis due to Collagen Receptor Defect | 99.921% | 2,285 | 低 |
| 7 | Hemorrhagic Disorder due to Constitutional Thrombocytopenia | 99.917% | 2,394 | 低 |
| 8 | Fetal and Neonatal Alloimmune Thrombocytopenia | 99.845% | 3,964 | 低 |
| 9 | Hemophilia A with Vascular Abnormality | 99.779% | 5,200 | 高 |
| 10 | Thrombotic Thrombocytopenic Purpura（血栓性血小板減少性紫斑症） | 99.724% | 6,173 | 低 |

**機轉分析：**
- 類乙型威勒布蘭氏病、後天性凝血因子缺乏、合併血管異常的 A 型血友病：與 FVIII 補充療法有較強關聯
- 血小板功能障礙類疾病（葛蘭茲曼病、斯科特症候群等）：FVIII 補充療法的效益不明確，因這些疾病主要為血小板本身缺陷

## 臨床試験エビデンス

目前無針對預測適應症的相關臨床試驗登記。

## 文献エビデンス

目前無針對預測適應症的相關 PubMed 文獻。

## 日本上市情報

| 承認番号 | 品名 | 剤形 | 承認適応症 | 效期 |
|---------|------|------|-----------|------|
| 衛部菌疫輸字第001068號 | 寧衛 基因工程第八凝血因子注射劑 250 IU | 凍晶注射劑 | 治療與預防 A 型血友病病人的出血 | 2028/03/19 |
| 衛部菌疫輸字第001069號 | 寧衛 基因工程第八凝血因子注射劑 500 IU | 凍晶注射劑 | 治療與預防 A 型血友病病人的出血 | 2028/03/19 |
| 衛部菌疫輸字第001070號 | 寧衛 基因工程第八凝血因子注射劑 1000 IU | 凍晶注射劑 | 治療與預防 A 型血友病病人的出血 | 2028/03/19 |

**許可證持有者**：艾科索股份有限公司
**核准日期**：2018/03/19

## 安全性に関する考慮事項

- **已知不良反應**：
  - 抑制性抗體（FVIII inhibitors）的產生
  - 過敏反應
  - 注射部位反應

- **藥物交互作用**：
  - 無已知重大藥物交互作用

- **特殊族群**：
  - 劑量需依據體重及出血嚴重程度調整
  - 詳見仿單

安全性情報は添付文書をご参照ください。

## 結論と次のステップ

**判断：Hold**

**理由：**
TxGNN 預測的新適應症中，後天性凝血因子缺乏及合併血管異常的 A 型血友病與 Simoctocog Alfa 的作用機轉有直接關聯。
然而，血小板功能障礙類疾病的預測與 FVIII 補充療法的機轉關聯性較弱，目前缺乏臨床證據支持。

**推進に必要な事項：**
- 針對後天性 FVIII 缺乏症的臨床數據收集
- 探索 Simoctocog Alfa 在類乙型威勒布蘭氏病中的應用
- 評估在抑制性抗體產生風險較低的情況下，擴展至其他出血性疾病的可行性
- 與其他 FVIII 製劑的比較研究


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
