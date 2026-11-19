---
layout: default
title: Luliconazole
parent: モデル予測のみ
nav_order: 198
evidence_level: L5
indication_count: 2
last_modified_at: 2026-11-20
monitor_inn: "Luliconazole"
predicted_indications: ["endothrix infectious disease", "ectothrix infectious disease"]
description: "Luliconazole：予測新適応症は毛内菌感染症 (endothrix infectious disease)（エビデンスレベル L5）。薬価基準の品目：1 件（現在収載 1 件）"
---

# Luliconazole
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **2** 件
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

## Luliconazole: 毛内菌感染症 (endothrix infectious disease)
{: .text-alpha }

## 一言要約

ルリコナゾールは外用のアゾール系抗真菌薬です。
TxGNN モデルは**毛内菌感染症 (endothrix infectious disease)** に有効である可能性を予測していますが、現時点で関連する臨床試験も文献も見つかっておらず、エビデンスはモデル予測のみです。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 毛内菌感染症 (endothrix infectious disease) |
| TxGNN 予測スコア | 0.9910 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 1 件／全 1 件） |
| 承認番号数 | 1 件（有効 1 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Luliconazole の添付文書（Prescribing Information）の「Mechanism of Action」および「Microbiology」の項によると（非公式訳）、「LUZUクリーム1%はアゾール系抗真菌薬である。[…] ルリコナゾールはアゾール系に属する抗真菌薬である。皮膚糸状菌に対する正確な作用機序は不明であるが、ルリコナゾールはラノステロール脱メチル化酵素を阻害することによりエルゴステロール合成を阻害すると考えられる。」英語原文："LUZU Cream, 1% is an azole antifungal. […] Luliconazole is an antifungal that belongs to the azole class. Although the exact mechanism of action against dermatophytes is unknown, luliconazole appears to inhibit ergosterol synthesis by inhibiting the enzyme lanosterol demethylase."（[DailyMed: Luzu (luliconazole) prescribing information, Bausch Health US, LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=a7016010-ce43-4c09-8d21-aeb697ffed31)、版 2020-04-01、参照日 2026-11-19）。ルリコナゾールはアゾール系の抗真菌薬に分類され、皮膚糸状菌に対する外用薬として用いられています。アゾール系は一般に真菌の細胞膜合成を阻害することで抗真菌作用を示します。

毛内菌感染症は、Trichophyton tonsurans などの皮膚糸状菌が毛幹の内部で増殖する感染症です。原因菌がアゾール系薬剤に感受性を示す可能性があるため、機序的には適用可能と考えられます。

ただし、感染部位が毛包内の毛幹であるため、外用剤では薬物が十分に浸透しない可能性があります。今回のデータには、この点を裏付ける試験や文献はありません。投与経路との適合性も未評価です。

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 620002498（取消） | ルリコン液１％ | 液１％ | 記載なし |

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
関連する臨床試験も文献もなく、根拠は TxGNN の予測と薬剤クラスの機序のみです。毛包内感染に対する外用剤の浸透性にも懸念があります。

**進める場合に必要なもの：**
- 毛内菌感染症に対する臨床試験または文献の収集
- 詳細な作用機序データ（MOA）の取得
- 添付文書の警告・禁忌情報の確認
- 外用剤の毛包内への浸透性と投与経路の適合性の評価

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Luzu (luliconazole) prescribing information, Bausch Health US, LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=a7016010-ce43-4c09-8d21-aeb697ffed31) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：ルコナック、ルリコン

**販売名（規格別）**：ルリコナゾールクリーム1%、ルリコナゾール軟膏1%、ルリコンクリーム1%、ルリコン液1%、ルリコン軟膏1%
<!-- brand-names:end -->

