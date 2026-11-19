---
layout: default
title: Flurbiprofen
parent: モデル予測のみ
nav_order: 138
evidence_level: L5
indication_count: 8
last_modified_at: 2026-11-17
monitor_inn: "Flurbiprofen"
predicted_indications: ["acromesomelic dysplasia, Hunter-Thompson type", "brachydactyly-syndactyly syndrome", "colobomatous microphthalmia-rhizomelic dysplasia syndrome", "brachyolmia-amelogenesis imperfecta syndrome", "myosclerosis", "brachyolmia", "pseudoachondroplasia", "hypermobility of coccyx"]
description: "Flurbiprofen：予測新適応症は先端中間肢異形成症 ハンター・トンプソン型 (acromesomelic dysplasia, Hunter-Thompson type)（エビデンスレベル L5）。薬価基準の品目：10 件（現在収載 6 件）"
---

# Flurbiprofen
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

## Flurbiprofen: 先端中間肢異形成症 ハンター・トンプソン型 (acromesomelic dysplasia, Hunter-Thompson type)
{: .text-alpha }

## 一言要約

フルルビプロフェンは、シクロオキシゲナーゼ（COX）を阻害する鎮痛・抗炎症薬で、日本ではテープ剤として市販されています。
TxGNN モデルは **先端中間肢異形成症 ハンター・トンプソン型 (acromesomelic dysplasia, Hunter-Thompson type)** に有効である可能性を予測しています。ただし、この疾患を直接検討した臨床試験や文献は現在ありません。エビデンスはモデル予測のみ（L5）です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 先端中間肢異形成症 ハンター・トンプソン型 (acromesomelic dysplasia, Hunter-Thompson type) |
| TxGNN 予測スコア | 0.9999 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 6 件／全 10 件） |
| 承認番号数 | 10 件（有効 6 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Flurbiprofen の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「フルルビプロフェンは鎮痛、抗炎症及び解熱作用を有する。フルルビプロフェンの作用機序は、他のNSAIDsと同様に完全には解明されていないが、シクロオキシゲナーゼ（COX-1及びCOX-2）の阻害が関与している。」英語原文："Flurbiprofen has analgesic, anti-inflammatory, and antipyretic properties. The mechanism of action of flurbiprofen, like that of other NSAIDs, is not completely understood but involves inhibition of cyclooxygenase (COX-1 and COX-2)."（[DailyMed: Lurbiro (flurbiprofen) prescribing information, IPG Pharmaceuticals, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=7ebf7427-eaae-4035-a6b2-0ea6381e8763)、版 2026-10-05、参照日 2026-11-19）。フルルビプロフェンは非選択的COX阻害薬に分類され、プロスタグランジン産生を抑えることで鎮痛・抗炎症作用を示します。

予測された疾患は、GDF5 遺伝子（CDMP1）に関連する遺伝性の骨格形成異常です。COX 阻害との機序的なつながりは知られておらず、今回の予測の根拠はモデルのスコアのみです。炎症や痛みの症状緩和という対症的な使い方は理論上あり得ますが、骨格形成そのものへの効果を支持する情報は見つかっていません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

## 日本市販情報

承認 10 件はすべて単剤のテープ剤（外用）で、うち有効は 6 件です（4 件は薬価基準から削除済み）。主要なものを示します。

<!-- review:begin jp-lic-20261117-flurbiprofen-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「有効な承認は 10 件で、すべて単剤のテープ剤（外用）です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、データ上の 10 件のうち有効（収載中）は 6 件で、4 件は経過措置期間満了などにより薬価基準から削除されています（670008249（廃止年月日 2026-03-31）、670647301（廃止年月日 2026-03-31）、670008250（廃止年月日 2026-03-31）、671415301（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-flurbiprofen-1 -->

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 620008249 | ゼポラステープ２０ｍｇ　７ｃｍ×１０ｃｍ | テープ | 関節リウマチ（鎮痛・抗炎症） |
| 620008250 | ゼポラステープ４０ｍｇ　１０ｃｍ×１４ｃｍ | テープ | 関節リウマチ（鎮痛・抗炎症） |
| 621415301 | ヤクバンテープ２０ｍｇ　７ｃｍ×１０ｃｍ | テープ | 関節リウマチ（鎮痛・抗炎症） |
| 620647301 | ヤクバンテープ４０ｍｇ　１０ｃｍ×１４ｃｍ | テープ | 関節リウマチ（鎮痛・抗炎症） |
| 622082902 | フルルビプロフェンテープ２０ｍｇ「ＱＱ」　７ｃｍ×１０ｃｍ | テープ | 関節リウマチ（鎮痛・抗炎症） |

全承認の剤形がテープ剤であるため、全身性の骨格疾患に使う場合は投与経路の適合性を別途検討する必要があります。

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用データは 100 件あり、そのうち主なものは次のとおりです。
  - 中等度：ステロイド類（ヒドロコルチゾン、デキサメタゾン、ベタメタゾン、トリアムシノロン、ブデソニド）、メトホルミン、グリメピリド、クロルプロパミド、アスピリン、メサラジン、バルサラジド、アプレピタント
  - 軽度：ファモチジン、シメチジン、リナクロチド
- 添付文書の警告・禁忌の内容は今回のデータでは確認できていません。使用前に添付文書を確認してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- この疾患を直接検討した臨床試験・文献がなく、機序的な根拠も見当たりません。予測はモデルスコアのみに依拠しているため、現時点では開発を進める根拠が不十分です。

**進める場合に必要なもの：**
- 詳細な薬物作用機序データの取得と、GDF5 関連の病態との機序的関連性の検証
- 前臨床研究（細胞・動物モデル）による効果の確認
- 添付文書の警告・禁忌の確認と安全性評価
- 全身性疾患への適用を想定した投与経路・剤形の検討

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正 | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Lurbiro (flurbiprofen) prescribing information, IPG Pharmaceuticals, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=7ebf7427-eaae-4035-a6b2-0ea6381e8763) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：アドフィード、ゼポラス、フロベン、ヤクバン

**販売名（規格別）**：ゼポラステープ20mg 7cm×10cm、ゼポラステープ40mg 10cm×14cm、フルルビプロフェンテープ20mg 7cm×10cm、フルルビプロフェンテープ40mg 10cm×14cm、ヤクバンテープ20mg 7cm×10cm、ヤクバンテープ40mg 10cm×14cm
<!-- brand-names:end -->

