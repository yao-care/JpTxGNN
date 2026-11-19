---
layout: default
title: Methylprednisolone
parent: モデル予測のみ
nav_order: 206
evidence_level: L5
indication_count: 8
last_modified_at: 2026-11-03
monitor_inn: "Methylprednisolone"
predicted_indications: ["alopecia mucinosa", "telogen effluvium", "Quinquaud's folliculitis decalvans", "alopecia antibody deficiency", "hereditary hypotrichosis with recurrent skin vesicles", "alopecia-intellectual disability-hypergonadotropic hypogonadism syndrome", "atrichia with papular lesions", "alopecia universalis onychodystrophy vitiligo"]
description: "Methylprednisolone：予測新適応症はムチン沈着性脱毛症 (alopecia mucinosa)（エビデンスレベル L5）。薬価基準の品目：9 件（現在収載 9 件）"
---

# Methylprednisolone
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **8** 件
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

## Methylprednisolone: ムチン沈着性脱毛症 (alopecia mucinosa)
{: .text-alpha }

## 一言要約

メチルプレドニゾロンは、抗炎症作用と免疫抑制作用を持つ合成グルココルチコイドで、日本では注射剤、経口剤、外用剤として市販されています。
TxGNN モデルは**ムチン沈着性脱毛症 (alopecia mucinosa)** に有効である可能性を予測しています。ただし、現時点で関連する臨床試験や文献は見つかっておらず、エビデンスはモデル予測のみ（L5）です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | ムチン沈着性脱毛症 (alopecia mucinosa) |
| TxGNN 予測スコア | 0.9999 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 9 件／全 9 件） |
| 承認番号数 | 9 件（有効 9 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Methylprednisolone の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「天然に存在する糖質コルチコイド（ヒドロコルチゾン及びコルチゾン）は、塩類貯留作用も有しており、副腎皮質機能不全状態における補充療法に用いられる。それらの合成類似体は、主として多くの器官系の疾患における強力な抗炎症作用を目的として用いられる。」英語原文："Naturally occurring glucocorticoids (hydrocortisone and cortisone), which also have salt-retaining properties, are used as replacement therapy in adrenocortical deficiency states. Their synthetic analogs are primarily used for their potent anti-inflammatory effects in disorders of many organ systems."（[DailyMed: methylprednisolone prescribing information, American Health Packaging](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=97256c7e-5694-4148-926f-594b9d5c34f4)、版 2026-07-01、参照日 2026-11-19）。一般にグルココルチコイドは、炎症性サイトカインの産生を抑え、リンパ球などの免疫細胞の活動を抑制する薬剤群です。

ムチン沈着性脱毛症は、毛包にムチンが沈着し、炎症を伴う疾患です。そのため、グルココルチコイドの抗炎症作用が炎症反応を和らげる可能性は、機序的には考えられます。ただし、これは推論の域を出ません。この疾患に対する臨床データは今回の調査では確認できず、根拠はモデルの予測のみです。

## 臨床試験・文献エビデンス

本予測疾患について、現在、関連する臨床試験の登録および関連する文献はありません。そのため、エビデンスレベルは L5 と判定しました。

## 日本市販情報

日本では 9 件の承認がすべて有効で、市販中です。主な製品は次のとおりです。

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 620007358 | ソル・メドロール静注用500mg（溶解液付） | 注射用 | 記載なし（承認有効） |
| 620007357 | ソル・メドロール静注用125mg（溶解液付） | 注射用 | 記載なし（承認有効） |
| 620007356 | ソル・メドロール静注用40mg（溶解液付） | 注射用 | 記載なし（承認有効） |
| 620005125 | メドロール錠2mg | 錠剤 | 記載なし（承認有効） |
| 620007382 | デポ・メドロール水懸注40mg 1mL | 注射剤 | 記載なし（承認有効） |

局所投与が想定される疾患のため、軟膏や局所注射剤などの剤形が既に存在する点は、今後の検討で有利になり得ます。ただし、投与経路の適合性はまだ評価されていません。

## 安全性に関する考慮事項

**薬物相互作用**（今回のデータでは 100 件を確認。主なものは以下のとおり）

- **Major**：ブプロピオン、クラリスロマイシン
- **Moderate**：
  - 血糖降下薬（メトホルミン、ピオグリタゾン、アカルボース、SGLT2 阻害薬、DPP-4 阻害薬、GLP-1 受容体作動薬など）。ステロイドによる血糖上昇で、効果が弱まる可能性があります。
  - アムホテリシン B、アプレピタント、アセチルサリチル酸、ビサコジルなど

全身投与では、高血糖、高血圧、感染症などへの注意が一般に必要です。具体的な警告や禁忌については、添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 予測の根拠は TxGNN モデルのスコアのみで、この疾患を直接検討した臨床試験や文献がありません。
- 現段階では、開発や適応拡大の判断に進める材料が不足しています。

**進める場合に必要なもの：**
- ムチン沈着性脱毛症に対するグルココルチコイド使用の症例報告や治療成績の文献調査
- 詳細な作用機序データの補充
- 添付文書の警告・禁忌情報の取得と、局所投与を含む投与経路の適合性評価
- 小規模な探索的研究の可否の検討

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: methylprednisolone prescribing information, American Health Packaging](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=97256c7e-5694-4148-926f-594b9d5c34f4) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：デポ・メドロール水懸、メドロール

**販売名（規格別）**：デポ・メドロール水懸注20mg 1mL、デポ・メドロール水懸注40mg 1mL、メドロール錠2mg、メドロール錠4mg

**配合剤（この成分を含む）**：ネオメドロールEE軟膏
<!-- brand-names:end -->

