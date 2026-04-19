---
layout: default
title: Scopolamine
parent: モデル予測のみ (L5)
nav_order: 154
evidence_level: L5
indication_count: 1
---

# Scopolamine
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

# Scopolamine：從解痙劑到神經及眼科疾病探索

## 一言まとめ

Scopolamine 主要用於胃腸道、膽道及尿路痙攣的緩解。
TxGNN 模型預測它可能對**馬尾症候群 (Cauda Equina Syndrome)** 及**神經源性膀胱**有效，
但目前缺乏臨床試驗及文獻支持這些新適應症。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 胃腸痙攣、膽管痙攣、尿路痙攣、女性生殖器痙攣 |
| 予測新適応症 | Cauda Equina Syndrome（馬尾症候群） |
| TxGNN 予測スコア | 99.99% |
| エビデンスレベル | L5 |
| 日本上市 | 已上市 |
| 承認数 | 317 張 |
| 推奨判断 | Hold |

## この予測が妥当な理由

Scopolamine（東莨菪鹼）是一種抗膽鹼藥物，作為毒蕈鹼受體拮抗劑，
能抑制副交感神經活動，達到解痙及減少分泌的效果。

**TxGNN 預測的新適應症與機轉關聯性分析：**

| 排名 | 預測適應症 | 預測分數 | TxGNN 排名 | 機轉關聯性 |
|------|-----------|---------|-----------|----------|
| 1 | Cauda Equina Syndrome（馬尾症候群） | 99.99% | 548 | 可能緩解神經壓迫引起的膀胱痙攣 |
| 2 | Neurogenic Bladder（神經源性膀胱） | 99.98% | 909 | 抗膽鹼作用可緩解膀胱過動 |
| 3 | Papillary Conjunctivitis（乳頭狀結膜炎） | 99.98% | 1,025 | 關聯性不明確 |
| 4 | Atopic Conjunctivitis（異位性結膜炎） | 99.80% | 4,736 | 關聯性不明確 |
| 5 | Rosacea Conjunctivitis（酒糟結膜炎） | 99.40% | 11,144 | 關聯性不明確 |
| 6 | Vernal Conjunctivitis（春季結膜炎） | 99.08% | 15,822 | 關聯性不明確 |

馬尾症候群及神經源性膀胱的預測較為合理，因為 Scopolamine 的抗膽鹼作用可緩解膀胱過動及痙攣症狀。
然而，結膜炎相關預測與已知機轉關聯性較弱。

## 臨床試験エビデンス

目前無針對預測適應症的相關臨床試驗登記。

## 文献エビデンス

目前無針對預測適應症的相關 PubMed 文獻。

## 日本上市情報

| 承認番号 | 品名 | 剤形 | 承認適応症 | 狀態 |
|---------|------|------|-----------|------|
| 內衛藥製字第000509號 | 保賜康膠囊 | 膠囊劑 | 胃潰瘍、膽囊炎、膽結石、尿路結石、膀胱痙攣、痙攣性月經困難等 | 有效 |
| 內衛藥製字第002211號 | 強生舒胃糖衣錠10毫克 | 錠劑 | 胃炎、腸疝痛、膽管痙攣、膽石疝痛 | 有效 |
| 內衛藥製字第009840號 | 勿賜痛注射液 | 注射劑 | 腸疝痛、膽管痙攣、膽石疝痛、痙攣性月經困難症 | 有效 |
| 內衛藥製字第010222號 | 南光胃使可胖注射液 | 注射劑 | 胃腸痙攣、膽管痙攣、尿路痙攣、女性生殖器痙攣 | 有效 |
| 內衛藥製字第001758號 | 攣怕斯糖衣片 | 糖衣錠 | 胃腸痙攣、膽管痙攣、尿路痙攣 | 有效 |

## 安全性に関する考慮事項

- **主要藥物交互作用（重大）**：
  - Topiramate、Zonisamide：可能增加體溫調節障礙風險

- **中度藥物交互作用**：
  - 鴉片類藥物：Fentanyl、Morphine、Codeine、Hydrocodone、Tramadol、Buprenorphine 等
  - 抗膽鹼藥物：Atropine、Hyoscyamine、Glycopyrronium、Benzatropine 等
  - 抗精神病藥物：Aripiprazole、Asenapine、Brexpiprazole 等
  - 抗組織胺藥物：Chlorpheniramine、Brompheniramine 等
  - 乙型阻斷劑：Atenolol、Bisoprolol、Acebutolol 等
  - 其他：Ethanol、Amantadine、Amitriptyline、Loperamide

- **輕度藥物交互作用**：
  - Acetaminophen、Hydrochlorothiazide

安全性情報は添付文書をご参照ください。

## 結論と次のステップ

**判断：Hold**

**理由：**
TxGNN 預測的馬尾症候群及神經源性膀胱適應症與 Scopolamine 的抗膽鹼作用機轉有一定關聯，
但目前缺乏臨床試驗及文獻支持。結膜炎相關預測則與已知機轉關聯性較弱。

**推進に必要な事項：**
- 針對神經源性膀胱的臨床試驗數據
- 探索 Scopolamine 在馬尾症候群相關膀胱功能障礙的應用
- 評估長期使用的安全性，特別是與其他抗膽鹼藥物併用時


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
