---
layout: default
title: Felbinac
parent: モデル予測のみ
nav_order: 130
evidence_level: L5
indication_count: 9
last_modified_at: 2026-11-24
description: "Felbinac：予測新適応症はbrachyolmia-amelogenesis imperfecta syndrome（エビデンスレベル L5）。既存適応症：鎮痛薬、抗炎症薬、シクロオキシゲナーゼ阻害薬"
monitor_inn: "felbinac"
predicted_indications: ["brachyolmia-amelogenesis imperfecta syndrome", "acromesomelic dysplasia, Hunter-Thompson type", "myosclerosis", "brachyolmia", "pseudoachondroplasia", "rheumatoid nodulosis", "combined immunodeficiency due to moesin deficiency", "rheumatoid factor-positive polyarticular juvenile idiopathic arthritis", "juvenile idiopathic arthritis"]
---

# Felbinac
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **9** 件
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

## フェルビナク：鎮痛・抗炎症から先天性骨系統疾患（brachyolmia-amelogenesis imperfecta syndrome）へ
{: .text-alpha }

## 一言要約

フェルビナクは、シクロオキシゲナーゼ（COX）阻害作用を持つ鎮痛・抗炎症薬で、日本では貼付剤（テープ）として使用されてきました。
TxGNN モデルは **brachyolmia-amelogenesis imperfecta syndrome** に有効である可能性を予測していますが、現時点で裏付けとなる**臨床試験・文献はありません**（モデル予測のみ）。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 鎮痛薬、抗炎症薬、シクロオキシゲナーゼ阻害薬 |
| 予測新規適応症 | brachyolmia-amelogenesis imperfecta syndrome |
| TxGNN 予測スコア | 0.9999 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 41 件／全 42 件） |
| 承認番号数 | 42 件（有効 41 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。既知の情報によると、フェルビナクは NSAID（COX 阻害薬）で、疼痛や炎症の症状緩和に使われてきた外用薬です。

一方、予測された brachyolmia-amelogenesis imperfecta syndrome は、骨格と歯のエナメル質に影響する遺伝性の形成異常です。COX 阻害と、この疾患の病態との間に確立された関連は見つかっておらず、**この予測は機序的に裏付けられていません**。

参考として、同じ上位スコア群（brachyolmia、acromesomelic dysplasia、pseudoachondroplasia など）も、ほとんどが遺伝性骨格異形成です。これらは症状（関節痛など）の緩和以外に、フェルビナクが病態に作用する根拠はありません。一方、下位の候補である脊椎関節症や若年性特発性関節炎は、NSAID が症状管理に使われるため間接的な妥当性はありますが、フェルビナク固有のエビデンスはありません。

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 621521801 | フェルビナクテープ７０ｍｇ「久光」 １０ｃｍ×１４ｃｍ | 有効 |
| 622036801 | セルタッチテープ７０ １０ｃｍ×１４ｃｍ | 有効 |
| 621478701 | フェルビナクテープ３５ｍｇ「三笠」 ７ｃｍ×１０ｃｍ | 有効 |
| 621981802 | フェルビナクテープ３５ｍｇ「ＮＰ」 ７ｃｍ×１０ｃｍ | 有効 |
| 620646303 | フェルビナクテープ７０ｍｇ「ＮＰ」 １０ｃｍ×１４ｃｍ | 有効 |

上表はデータ上の 42 件のうち 5 件です。

<!-- licenses:end -->

上記を含む承認には有効なものと薬価基準から削除済みのものがあります（件数はクイック概要を参照）。

<!-- review:begin jp-lic-20261117-felbinac-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「上記を含む 9 件の承認はすべて有効です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（672036801（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-felbinac-1 -->

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 予測はモデルスコアのみに基づき、臨床試験も文献もありません（L5）。
- 上位候補は遺伝性骨格異形成で、COX 阻害との機序的関連が認められません。
- 国内で販売されており、有効な承認があります（件数はクイック概要を参照）。

<!-- review:begin jp-lic-20261117-felbinac-2 -->

> **確認による訂正（2026-11-17）**：元の記載は「国内で販売されており、9 件の承認すべてが有効です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（672036801（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-felbinac-2 -->

**進める場合に必要なもの：**
- 詳細な薬物作用機序データ（MOA）
- 添付文書に基づく警告・禁忌情報の取得と安全性評価
- 予測疾患とフェルビナクの関連を示す前臨床または臨床の根拠
- 外用（貼付）という投与経路が対象疾患に適合するかの検証
- 機序的妥当性がより高い候補（脊椎関節症、若年性特発性関節炎など）の個別評価

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：セルタッチ、ナパゲルン

**販売名（規格別）**：セルタッチテープ70 10cm×14cm、セルタッチパップ140 20cm×14cm、セルタッチパップ70 10cm×14cm、フェルビナク(140mg)20cm×14cm貼付剤、フェルビナク(35mg)7cm×10cm貼付剤、フェルビナク3%ローション、フェルビナクテープ35mg 7cm×10cm、フェルビナクテープ70mg 10cm×14cm、フェルビナクパップ140mg 20cm×14cm、フェルビナクパップ70mg 10cm×14cm
<!-- brand-names:end -->

