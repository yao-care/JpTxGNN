---
layout: default
title: Prednisolone Acetate
parent: 中エビデンス (L3-L4)
nav_order: 138
evidence_level: L4
indication_count: 1
last_modified_at: 2026-09-17
description: "Prednisolone Acetate：予測新適応症は寄生虫性結膜炎 (Parasitic Conjunctivitis)（エビデンスレベル L4）。既存適応症：日本の承認適応症は本サイトのデータに未収載、conjunctivitis、acute contagious conjunctivitis）"
---

# Prednisolone Acetate
{: .fs-9 }

エビデンスレベル: **L4** | 予測適応症: **1** 件
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

## Prednisolone Acetate：眼部アレルギーから寄生虫性結膜炎へ
{: .text-alpha }

## 一言まとめ

Prednisolone acetate（酢酸プレドニゾロン） は眼科用の副腎皮質ステロイドで、もともと眼瞼炎、結膜炎、角膜炎などのアレルギー性眼疾患に用いられています。TxGNN モデルは、本剤が**寄生虫性結膜炎 (Parasitic Conjunctivitis)** に有効である可能性を予測しており、現時点でこの方向性を支持する文献が **1 件**あります。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：uveitis、iris disease、ciliary body disease、panuveitis (disease)、conjunctivitis、acute contagious conjunctivitis） |
| 予測新適応症 | 寄生虫性結膜炎 (Parasitic Conjunctivitis) |
| TxGNN 予測スコア | 99.74% |
| エビデンスレベル | L4 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Prednisolone acetate は局所用の副腎皮質ステロイドで、強力な抗炎症作用と免疫調節作用を有します。主に結膜炎、角膜炎、虹彩毛様体炎など、各種のアレルギー性・炎症性眼疾患の治療に用いられます。

寄生虫性結膜炎は寄生虫感染によって生じる結膜の炎症であり、感染のコントロール後には、持続する炎症反応を抑える目的で局所ステロイドを用いることがあります。文献報告によると、Dirofilaria repens（眼部の寄生虫症）の治療では、局所の炎症反応を抑えるためにステロイドが抗菌薬と併用されることが多いとされています。

既存の適応症（各種の結膜炎）と新たに予測された適応症（寄生虫性結膜炎）は、いずれも結膜の炎症反応を伴う点で病態が類似しています。そのため、副腎皮質ステロイドの抗炎症作用は、作用機序の面から、寄生虫感染後の炎症の抑制にも適用できる可能性があります。

## 臨床試験エビデンス

| 試験番号 | 相 | 状態 | 人数 | 主な所見 |
|---------|------|------|------|---------|
| [NCT04705584](https://clinicaltrials.gov/study/NCT04705584) | N/A | 不明 | 180 | 春季カタル性結膜炎に対する免疫抑制薬の治療を検討 |
| [NCT01437982](https://clinicaltrials.gov/study/NCT01437982) | Phase 4 | 完了 | 140 | Lotemax 点眼懸濁液の安全性および有効性の評価 |

## 文献エビデンス

| PMID | 発表年 | 種類 | 雑誌 | 主な所見 |
|------|-----|------|------|---------|
| [26846596](https://pubmed.ncbi.nlm.nih.gov/26846596/) | 2016 | Case Report | Eye | Dirofilaria repens による眼部感染に対し、ステロイドと抗菌薬を併用して治療 |
| [29801089](https://pubmed.ncbi.nlm.nih.gov/29801089/) | 2018 | Case Report | JAMA Ophthalmology | 慢性濾胞性結膜炎の治療報告 |
| [26984315](https://pubmed.ncbi.nlm.nih.gov/26984315/) | 2016 | Review | Advances in Therapy | Loteprednol etabonate の眼圧への影響 |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

安全性情報は添付文書をご参照ください。

眼科用副腎皮質ステロイドの一般的な注意事項は以下のとおりです。
- 長期使用により眼圧が上昇する可能性がある
- 感染リスクが高まる可能性がある
- 真菌性またはウイルス性の眼感染症には推奨されない

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
Prednisolone acetate は眼科用の副腎皮質ステロイドであり、その抗炎症作用は、寄生虫感染のコントロール後の炎症管理において、合理的な適用根拠を有します。寄生虫性の眼感染症でステロイドを併用した症例が、文献ですでに報告されています。

**推進に必要な事項：**
- 寄生虫感染が有効にコントロールされていることを確認する
- 眼圧の変化をモニタリングする
- 抗寄生虫薬の併用が必要かどうかを評価する


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
