---
noindex: true
sitemap: false
layout: default
title: Levamisole
parent: モデル予測のみ (L5)
nav_order: 96
evidence_level: L5
indication_count: 1
last_modified_at: 2026-09-17
---

# Levamisole
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **1** 件
{: .fs-6 .fw-300 }

---

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist" markdown="1">

## 薬剤師評価レポート

</div>

## Levamisole：抗腫瘍補助療法から薬剤性骨粗鬆症へ
{: .text-alpha }

## 一言まとめ

Levamisole（レバミゾール） は本来、抗腫瘍補助療法および駆虫薬として用いられてきました。
TxGNN モデルは、本薬が**薬剤性骨粗鬆症 (drug-induced osteoporosis)** に有効である可能性を予測していますが、
現時点ではモデルによる予測のみが根拠であり、臨床試験や文献のエビデンスはありません。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：ascaridiasis、ancylostomiasis） |
| 予測新適応症 | 薬剤性骨粗鬆症 (drug-induced osteoporosis) |
| TxGNN 予測スコア | 99.9993% |
| エビデンスレベル | L5 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Hold |

## この予測が妥当な理由

現時点では、詳細な作用機序に関する資料がありません。既知の情報によれば、Levamisole は抗腫瘍補助療法および駆虫薬の一部であり、
これらの適応症における有効性は確認されていますが、作用機序の面では薬剤性骨粗鬆症には当てはまらない可能性があります。

## 臨床試験エビデンス

現時点で関連する臨床試験の登録はありません

## 文献エビデンス

現時点で関連する文献はありません

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **薬物相互作用**：
  - Ethanol と中等度の相互作用あり
  - Deferiprone と重大な相互作用あり
  - Palifermin と中等度の相互作用あり
  - Samarium (153Sm) lexidronam と重大な相互作用あり
  - Strontium chloride Sr-89 と中等度の相互作用あり
  - Warfarin と中等度の相互作用あり
  - Zidovudine と中等度の相互作用あり
  - Clostridium tetani toxoid antigen (formaldehyde inactivated) と中等度の相互作用あり
  - Adalimumab と重大な相互作用あり
  - Alefacept と中等度の相互作用あり

## 結論と次のステップ

**判断：Hold**

**理由：**
現時点では、Levamisole の薬剤性骨粗鬆症への使用を支持する根拠はモデルによる予測のみであり、臨床試験や文献のエビデンスがありません。

**推進に必要な事項：**
- 詳細な薬物の作用機序（MOA）に関する資料
- さらなる臨床試験の設計と実施
- 薬剤性骨粗鬆症に関連する作用機序の研究

---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
