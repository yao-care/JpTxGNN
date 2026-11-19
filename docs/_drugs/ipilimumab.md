---
layout: default
title: Ipilimumab
parent: モデル予測のみ
nav_order: 188
evidence_level: L5
indication_count: 1
monitor_inn: "Ipilimumab"
predicted_indications: ["choroideremia"]
last_modified_at: 2026-10-28
description: "Ipilimumab：予測新適応症は脈絡膜欠損症 (choroideremia)（エビデンスレベル L5）。薬価基準の品目：2 件（現在収載 2 件）"
---

# Ipilimumab
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

## イピリムマブ：抗CTLA-4抗体 → 脈絡膜欠損症 (choroideremia)
{: .text-alpha }

## 一言要約

イピリムマブは、T細胞の活性化を高める抗CTLA-4抗体です。
TxGNN モデルは**脈絡膜欠損症 (choroideremia)** に有効である可能性を予測していますが、関連する臨床試験・文献は現在ありません。予測はモデル上のものにとどまります。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 脈絡膜欠損症 (choroideremia) |
| TxGNN 予測スコア | 0.9906 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 2 件／全 2 件） |
| 承認番号数 | 2 件（有効 2 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Ipilimumab の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「CTLA-4はT細胞活性の負の調節因子である。イピリムマブはCTLA-4に結合し、CTLA-4とそのリガンドであるCD80/CD86との相互作用を阻害するモノクローナル抗体である。CTLA-4の阻害により、腫瘍浸潤エフェクターT細胞の活性化及び増殖を含め、T細胞の活性化及び増殖が増強されることが示されている。」英語原文："CTLA-4 is a negative regulator of T-cell activity. Ipilimumab is a monoclonal antibody that binds to CTLA-4 and blocks the interaction of CTLA-4 with its ligands, CD80/CD86. Blockade of CTLA-4 has been shown to augment T-cell activation and proliferation, including the activation and proliferation of tumor infiltrating T-effector cells."（[DailyMed: Yervoy (ipilimumab) prescribing information, E.R. Squibb & Sons, L.L.C.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=2265ef30-253e-11df-8a39-0800200c9a66)、版 2026-08-20、参照日 2026-11-19）。イピリムマブは抗CTLA-4抗体であり、T細胞の活性化を促進して抗腫瘍免疫を高める薬剤です。

一方、脈絡膜欠損症は CHM/REP1 遺伝子の変異による単一遺伝子性の遺伝性網膜変性症です。免疫活性化を主作用とするイピリムマブとの間に、機序上の妥当な接点は見いだせません。

TxGNN のスコアは高い値ですが、これを裏付ける臨床試験や文献はありません。現時点では、モデル予測の域を出ない仮説として扱うべきです。

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 622440501 | ヤーボイ点滴静注液５０ｍｇ　１０ｍＬ | 注液５０ｍｇ　１０ｍＬ | 記載なし |
| 629917301 | ヤーボイ点滴静注液２０ｍｇ　４ｍＬ | 注液２０ｍｇ　４ｍＬ | 記載なし |

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 免疫療法（免疫チェックポイント阻害薬） |
| 骨髄抑制リスク | 添付文書の警告および注意事項を参照してください |
| 催吐性分類 | 添付文書の警告および注意事項を参照してください |
| モニタリング項目 | 添付文書の警告および注意事項を参照してください |
| 取り扱い防護 | 添付文書の警告および注意事項を参照してください |

## 安全性に関する考慮事項

- **薬物相互作用**：本レポート用にまとめたデータでは、相互作用が100件報告されています。主なものは次のとおりです。
  - 重要度「Major」：抗凝固薬（アピキサバン、エドキサバン、ダルテパリン、アルガトロバン、ベトリキサバン、ビバリルジン、デシルジン、ダナパロイドなど）
  - 重要度「Moderate」：副腎皮質ステロイド（ヒドロコルチゾン、デキサメタゾン、プレドニゾロン、プレドニゾン、トリアムシノロン、ベタメタゾン、ブデソニド）、メトロニダゾール、チニダゾール、ナルトレキソン、ロスバスタチン、シンバスタチン

  ステロイドは免疫抑制作用により、イピリムマブの効果に影響する可能性があります。併用時は注意が必要です。

警告・禁忌の詳細は、添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 予測スコアは高いものの、脈絡膜欠損症を直接調べた臨床試験・文献がなく、機序上の接点も見いだせません。エビデンスはモデル予測のみ（L5）です。

**進める場合に必要なもの：**
- 脈絡膜欠損症とCTLA-4経路を結ぶ機序的根拠（前臨床研究など）
- 詳細な作用機序データ（MOA）
- 添付文書の警告・禁忌情報の取得と安全性評価
- 眼科領域への投与経路の適合性の検討

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Yervoy (ipilimumab) prescribing information, E.R. Squibb & Sons, L.L.C.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=2265ef30-253e-11df-8a39-0800200c9a66) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：ヤーボイ

**販売名（規格別）**：ヤーボイ点滴静注液20mg 4mL、ヤーボイ点滴静注液50mg 10mL
<!-- brand-names:end -->

