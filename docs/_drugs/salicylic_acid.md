---
layout: default
title: Salicylic Acid
parent: モデル予測のみ (L5)
nav_order: 153
evidence_level: L5
indication_count: 1
---

# Salicylic Acid
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

# Salicylic Acid：從皮膚科用藥到眼科及骨骼疾病探索

## 一言まとめ

Salicylic Acid 主要用於皮膚角化劑、抗黴菌外用藥及鎮痛解熱。
TxGNN 模型預測它可能對**乳頭狀結膜炎 (Papillary Conjunctivitis)** 等眼科及骨骼疾病有效，
但目前缺乏臨床試驗及文獻支持這些新適應症。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 抗皮膚角化劑、殺菌、角質軟化、解熱鎮痛 |
| 予測新適応症 | Papillary Conjunctivitis |
| TxGNN 予測スコア | 99.88% |
| エビデンスレベル | L5 |
| 日本上市 | 已上市 |
| 承認数 | 326 張 |
| 推奨判断 | Hold |

## この予測が妥当な理由

目前缺乏詳細的作用機轉資料。根據已知資訊，Salicylic Acid 是一種廣泛使用的皮膚科藥物，
其角質軟化及抗發炎的作用機轉已被證實。Salicylic Acid 被認為可能透過抑制 COX 酶產生抗發炎效果，
同時對 ASIC3 離子通道有交互作用。

**TxGNN 預測的前五名新適應症：**

| 排名 | 預測適應症 | 預測分數 | TxGNN 排名 |
|------|-----------|---------|-----------|
| 1 | Papillary Conjunctivitis（乳頭狀結膜炎） | 99.88% | 3,238 |
| 2 | Colobomatous Microphthalmia-Rhizomelic Dysplasia Syndrome | 99.78% | 5,166 |
| 3 | Brachydactyly-Syndactyly Syndrome | 99.73% | 6,122 |
| 4 | Brachyolmia-Amelogenesis Imperfecta Syndrome | 99.55% | 9,127 |
| 5 | Rosacea Conjunctivitis（酒糟結膜炎） | 99.53% | 9,298 |

然而，這些預測主要為罕見遺傳性疾病或眼科疾病，與 Salicylic Acid 已知的皮膚科作用機轉關聯性不明確，
需進一步的機轉研究來驗證。

## 臨床試験エビデンス

目前無針對預測適應症的相關臨床試驗登記。

## 文献エビデンス

目前無針對預測適應症的相關 PubMed 文獻。

## 日本上市情報

| 承認番号 | 品名 | 剤形 | 承認適応症 | 狀態 |
|---------|------|------|-----------|------|
| 衛部藥陸輸字第000870號 | 乙醯水楊酸 | （粉） | 鎮痛藥、退熱藥、抗風濕藥 | 有效 |
| 衛部菌疫輸字第000965號 | 貝靈瑞利勁人體免疫球蛋白靜脈注射液10% | 注射液劑 | 川崎氏症（與乙醯水楊酸一起使用） | 有效 |
| 內衛成製字第000697號 | 癬治水 | 外用液劑 | 頑癬、濕癬、乾癬、疥癬 | 有效 |
| 內衛藥製字第003577號 | 柳酸絆創膏 | 硬膏劑 | 雞眼、疣贅、胼胝、角質剝離劑 | 已註銷 |
| 內衛藥輸字第007269號 | 柳酸 | （粉） | 抗皮膚角化劑 | 已註銷 |

## 安全性に関する考慮事項

- **藥物交互作用**：
  - 與 ASIC3（酸敏感離子通道3）有交互作用（來源：Guide to PHARMACOLOGY）

- **臨床使用注意**：
  - 廣泛用於痤瘡、乾癬、雞眼、疣等皮膚疾病的外用治療
  - CAS 號碼：69-72-7

安全性情報は添付文書をご参照ください。

## 結論と次のステップ

**判断：Hold**

**理由：**
TxGNN 預測的新適應症（乳頭狀結膜炎、罕見骨骼發育疾病）與 Salicylic Acid 已知的皮膚科作用機轉缺乏明確關聯。
目前無臨床試驗及文獻支持這些預測。

**推進に必要な事項：**
- 釐清 Salicylic Acid 對眼科疾病的可能作用機轉
- 針對結膜炎適應症的臨床前研究
- 探索其抗發炎機制在眼科應用的可行性


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
