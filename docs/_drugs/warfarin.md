---
layout: default
title: Warfarin
parent: モデル予測のみ (L5)
nav_order: 195
evidence_level: L5
indication_count: 1
---

# Warfarin
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

# Warfarin：從抗凝血劑到 Heparin Cofactor 2 Deficiency

## 一言まとめ

Warfarin 原本用於抗凝血治療。
TxGNN 模型預測它可能對**Heparin Cofactor 2 Deficiency** 有效，
目前有 **5 篇文獻**支持這個方向，但缺乏臨床試驗的支持。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 抗凝血劑 |
| 予測新適応症 | Heparin Cofactor 2 Deficiency |
| TxGNN 予測スコア | 99.87% |
| エビデンスレベル | L5 |
| 日本上市 | ✓ 已上市 |
| 承認数 | 20 張 |
| 推奨判断 | Hold |

## この予測が妥当な理由

目前缺乏詳細的作用機轉資料。根據已知資訊，Warfarin 是一種抗凝劑，
其成分在抗凝血治療中的療效已被證實，但與 Heparin Cofactor 2 Deficiency 的直接機轉關聯不明確。
Warfarin 透過抑制維生素K依賴性凝血因子的合成來減少血栓形成，這可能與新適應症有潛在關聯。

## 臨床試験エビデンス

目前無相關臨床試驗登記

## 文献エビデンス

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [11177584](https://pubmed.ncbi.nlm.nih.gov/11177584/) | 2001 | Review | AIDS patient care and STDs | HIV感染患者的血栓事件報導，涉及抗磷脂抗體和狼瘡抗凝物的異常。 |
| [2214444](https://pubmed.ncbi.nlm.nih.gov/2214444/) | 1990 | Case report | Kyobu geka. The Japanese journal of thoracic surgery | 家族性heparin cofactor II缺乏症患者的右心室血栓。 |
| [3778142](https://pubmed.ncbi.nlm.nih.gov/3778142/) | 1986 | In vitro | Archives of pathology & laboratory medicine | heparin cofactor II的實驗室測定方法。 |
| [11570053](https://pubmed.ncbi.nlm.nih.gov/11570053/) | 2001 | Case report | Journal of UOEH | 一家族多發性血栓的報導，其中一名患者使用Warfarin治療。 |
| [2033902](https://pubmed.ncbi.nlm.nih.gov/2033902/) | 1991 | Case report | Nihon Kyobu Shikkan Gakkai zasshi | 先天性抗凝血酶II缺乏症患者的肺梗塞病例。 |

## 日本上市情報

| 承認番号 | 品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 內衛藥輸字第002494號 | 活福寧鈉片 | 錠劑 | 抗凝血劑 |
| 內衛藥輸字第002938號 | 安汝命－Ｋ | 錠劑 | 血管栓塞、手術後栓塞性靜脈炎、肺栓塞等 |
| 衛部藥輸字第026478號 | 苯甲香豆醇鈉籠晶 | （粉） | 抗凝血劑 |
| 衛署藥製字第050068號 | 欣服寧 錠 1 毫克 | 錠劑 | 預防及/或治療靜脈栓塞症及其相關疾病，以及肺栓塞。 |

## 安全性に関する考慮事項

- **藥物交互作用**：
  - **主要交互作用**：Acetylsalicylic acid（重大）
  - **其他交互作用**：Ranitidine、Rabeprazole、Doxycycline、Hydrocortisone、Metformin 等（中度）

## 結論と次のステップ

**判断：Hold**

**理由：**
目前缺乏足夠的臨床試驗和詳細的作用機轉資料來支持 Warfarin 用於 Heparin Cofactor 2 Deficiency。

**推進に必要な事項：**
- 更詳細的藥物作用機轉資料
- 針對 Heparin Cofactor 2 Deficiency 的臨床試驗數據
- 進一步探索 Warfarin 在此適應症中的安全性與有效性

---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
