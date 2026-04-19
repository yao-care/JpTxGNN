---
layout: default
title: Vigabatrin
parent: モデル予測のみ (L5)
nav_order: 189
evidence_level: L5
indication_count: 1
---

# Vigabatrin
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

# Vigabatrin：抗癲癇輔助療法

## 一言まとめ

Vigabatrin 是一種用於抗癲癇輔助療法的藥物。
TxGNN 模型**未預測**出任何新的適應症。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 抗癲癇之輔助療法 |
| 予測新適応症 | 無 |
| TxGNN 予測スコア | N/A |
| エビデンスレベル | N/A |
| 日本上市 | 已上市 |
| 承認数 | 6 張（2 張有效） |
| 推奨判断 | 無老藥新用候選 |

## 新しい適応症が予測されない理由

Vigabatrin 是一種選擇性 GABA 轉胺酶（GABA-T）不可逆抑制劑，透過抑制 4-aminobutyrate aminotransferase 增加腦內 GABA 濃度。其作用機轉高度專一，主要針對癲癇相關的神經傳導異常，因此在 TxGNN 知識圖譜分析中未發現與其他疾病的顯著關聯。

## 臨床試験エビデンス

無相關新適應症的臨床試驗。

## 文献エビデンス

無相關新適應症的文獻證據。

## 日本上市情報

| 承認番号 | 品名 | 剤形 | 承認適応症 | 狀態 |
|---------|------|------|-----------|------|
| 衛部藥輸字第028723號 | 必抗癲口服溶液用粉劑500毫克 | 口服溶液用粉劑 | 抗癲癇之輔助療法 | 有效 |
| 衛署藥輸字第021847號 | 赦癲易膜衣錠500公絲 | 膜衣錠 | 抗癲癇之輔助療法 | 有效 |
| 衛署藥輸字第021691號 | 膜衣錠500公絲 | 膜衣錠 | 抗癲癇之輔助療法 | 已註銷 |
| 衛署藥輸字第020477號 | 赦癲易錠500公絲 | 外用錠劑 | 抗癲癇之輔助療法 | 已註銷 |

## 安全性に関する考慮事項

### 重大な薬物相互作用（Major）

| 交互作用藥物 | 嚴重度 |
|-------------|--------|
| Hydrocortisone | Major |
| Triamcinolone | Major |
| Dexamethasone | Major |
| Betamethasone | Major |
| Budesonide | Major |
| Prednisone | Major |
| Prednisolone | Major |
| Methylprednisolone | Major |
| Deflazacort | Major |
| Deferoxamine | Major |
| Chloroquine | Major |
| Hydroxychloroquine | Major |
| Quinine | Major |
| Tamoxifen | Major |

### 中度藥物交互作用（Moderate）

與多種鎮靜劑、抗組織胺藥物及類鴉片藥物有中度交互作用，可能增加中樞神經抑制作用。常見包括：Morphine、Codeine、Cetirizine、Diphenhydramine、Ethanol 等。

### 作用標靶

- Vesicular inhibitory amino acid transporter (SLC32A1)
- 4-aminobutyrate aminotransferase (ABAT)

## 結論と次のステップ

**判断：無老藥新用候選**

**理由：**
Vigabatrin 的作用機轉高度專一於 GABA 能神經傳導，TxGNN 模型未發現具有足夠證據支持的新適應症候選。

**注意事項：**
- Vigabatrin 可能導致不可逆的視野缺損，需定期監測視力
- 與皮質類固醇併用需特別注意交互作用


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
