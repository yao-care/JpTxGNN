---
layout: default
title: Lansoprazole
parent: モデル予測のみ
nav_order: 202
evidence_level: L5
indication_count: 1
monitor_inn: "Lansoprazole"
predicted_indications: ["duodenal obstruction"]
last_modified_at: 2026-11-24
description: "Lansoprazole：予測新適応症は十二指腸閉塞 (duodenal obstruction)（エビデンスレベル L5）。薬価基準の品目：20 件以上"
---

# Lansoprazole
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

## ランソプラゾール：プロトンポンプ阻害薬 → 十二指腸閉塞 (duodenal obstruction)
{: .text-alpha }

## 一言要約

ランソプラゾールは胃酸分泌を抑えるプロトンポンプ阻害薬です。
TxGNN モデルは**十二指腸閉塞 (duodenal obstruction)** に有効である可能性を予測していますが、現時点で関連する臨床試験と文献は **0 件**で、予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 十二指腸閉塞 (duodenal obstruction) |
| TxGNN 予測スコア | 0.9968 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 17 件以上） |
| 承認番号数 | 20 件以上 |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Lansoprazole の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「ランソプラゾールは、胃壁細胞の分泌面における（H +, K + ）-ATPase酵素系を特異的に阻害することにより胃酸分泌を抑制する抗分泌化合物の一群である置換ベンズイミダゾール類に属する。この酵素系は壁細胞内の酸（プロトン）ポンプとみなされていることから、ランソプラゾールは酸産生の最終段階を阻害するという点で、胃酸ポンプ阻害剤として特徴づけられている。」英語原文："Lansoprazole belongs to a class of antisecretory compounds, the substituted benzimidazoles, that suppress gastric acid secretion by specific inhibition of the (H +, K + )-ATPase enzyme system at the secretory surface of the gastric parietal cell. Because this enzyme system is regarded as the acid (proton) pump within the parietal cell, lansoprazole has been characterized as a gastric acid-pump inhibitor, in that it blocks the final step of acid production."（[DailyMed: Prevacid (lansoprazole) prescribing information, Takeda Pharmaceuticals America, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=71ba78cb-7e46-43eb-9425-fa130f537f84)、版 2025-07-08、参照日 2026-11-19）。ランソプラゾールはプロトンポンプ阻害薬に分類され、胃酸分泌を抑える薬剤として知られています。

酸分泌を抑えることで、閉塞部位付近に生じうる二次的な消化性粘膜障害を和らげる可能性は考えられます。ただし十二指腸閉塞は機械的な通過障害であり、酸抑制で閉塞そのものが改善するとは考えにくく、この関連性は TxGNN の予測のみに基づいています。支持する直接的な研究は今回のデータにはありません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

## 日本市販情報

日本の承認記録は一部のみの可能性があります。主要な承認を最大 5 件示します。

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 612320550 | タケプロンカプセル３０ ３０ｍｇ | 有効 |
| 612320549 | タケプロンカプセル１５ １５ｍｇ | 有効 |
| 610462011 | タケプロンＯＤ錠３０ ３０ｍｇ | 有効 |
| 610462010 | タケプロンＯＤ錠１５ １５ｍｇ | 有効 |
| 621693101 | ランソプラゾールカプセル１５ｍｇ「サワイ」 | 有効 |

データには承認の一部のみが含まれています。上表はそのうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用データベースに 100 件の登録があります。主なものとして、アカラブルチニブ、アタザナビルは **Major**（重大）に分類されています。ヒドロクロロチアジド、アトルバスタチン、フェノフィブラート、アンホテリシン B、アンピシリンなどは Moderate（中等度）です。併用薬の確認が必要です。

その他の警告・禁忌については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測スコアは高い（0.9968）ものの、十二指腸閉塞を直接検討した臨床試験や文献がなく、エビデンスはモデル予測のみ（L5）です。また、閉塞は機械的な問題であり、酸抑制との機序的なつながりも限定的です。

**進める場合に必要なもの：**
- 十二指腸閉塞に関する臨床試験・文献の調査（閉塞に伴う二次的な粘膜障害への有用性を含む）
- 詳細な作用機序データ（MOA）の補充
- 添付文書（警告・禁忌）の取得と安全性確認
- 投与経路の適合性評価

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Prevacid (lansoprazole) prescribing information, Takeda Pharmaceuticals America, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=71ba78cb-7e46-43eb-9425-fa130f537f84) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**販売名（規格別）**：タケプロンOD錠15 15mg、タケプロンOD錠30 30mg、タケプロンカプセル15 15mg、タケプロンカプセル30 30mg、タケプロン静注用30mg、ランソプラゾール15mg腸溶カプセル、ランソプラゾール15mg腸溶性口腔内崩壊錠、ランソプラゾール30mg腸溶カプセル、ランソプラゾール30mg腸溶性口腔内崩壊錠、ランソプラゾールOD錠15mg、ランソプラゾールOD錠30mg、ランソプラゾールカプセル15mg、ランソプラゾールカプセル30mg
<!-- brand-names:end -->

