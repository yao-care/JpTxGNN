---
layout: default
title: Fenofibrate
parent: モデル予測のみ
nav_order: 132
evidence_level: L5
indication_count: 1
monitor_inn: "Fenofibrate"
predicted_indications: ["cholesterol-ester transfer protein deficiency"]
last_modified_at: 2026-11-24
description: "Fenofibrate：予測新適応症はコレステロールエステル転送蛋白欠損症（エビデンスレベル L5）。既存適応症：高脂血症、家族性高脂血症"
---

# Fenofibrate
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

## フェノフィブラート：脂質異常症からコレステロールエステル転送蛋白欠損症へ
{: .text-alpha }

## 一言要約

フェノフィブラートは PPARα 作動薬で、日本では高脂血症・家族性高脂血症の治療に使用されています。
TxGNN モデルは**コレステロールエステル転送蛋白欠損症 (cholesterol-ester transfer protein deficiency)** に有効である可能性を予測していますが、この疾患を直接検討した臨床試験や文献はなく、動物・機序に関する文献 3 編があるのみです。エビデンスはモデル予測の段階（L5）にとどまります。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 高脂血症、家族性高脂血症 |
| 予測新規適応症 | コレステロールエステル転送蛋白欠損症 |
| TxGNN 予測スコア | 0.9961 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 10 件／全 12 件） |
| 承認番号数 | 12 件（有効 10 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Fenofibrate の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「Antaraの活性本体はフェノフィブリン酸である。動物及びヒトにおけるフェノフィブリン酸の薬理作用は、フェノフィブラートの経口投与により検討されている。臨床で認められるフェノフィブリン酸の脂質改善作用は、in vivoではトランスジェニックマウスにおいて、in vitroではヒト肝細胞培養において、PPARα受容体の活性化により説明されている。」英語原文："The active moiety of Antara is fenofibric acid. The pharmacological effects of fenofibric acid in both animals and humans have been studied through oral administration of fenofibrate. The lipid-modifying effects of fenofibric acid seen in clinical practice have been explained in vivo in transgenic mice and in vitro in human hepatocyte cultures by the activation of PPAR alpha receptor."（[DailyMed: Antara (fenofibrate) prescribing information, Lupin Pharmaceuticals, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=24790a18-0291-4b88-a724-acac43b616ce)、版 2025-10-01、参照日 2026-11-19）。既知の情報によると、フェノフィブラートはペルオキシソーム増殖因子活性化受容体α（PPARα）作動薬、かつトリグリセリド合成阻害薬に分類され、脂質異常症での有効性が確立されています。

データ上の機序的な手がかりとして、PPARα の活性化は HDL コレステロールを上昇させ、リン脂質転送蛋白（PLTP）の遺伝子発現を誘導し、CETP 経路と重なる形でリポ蛋白代謝に影響すると考えられています。ただしこれは間接的な裏付けにとどまります。

CETP 欠損症は HDL コレステロールが高値となる稀な遺伝性疾患です。フェノフィブラートはさらに HDL を上げる方向に働くため、治療上の意義は明確ではありません。ヒトでの臨床的根拠は確認されていません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

いずれも動物研究で、CETP 欠損症そのものを対象にした研究ではありません。

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [20332533](https://pubmed.ncbi.nlm.nih.gov/20332533/) | 2010 | 動物研究 | J Cardiovasc Pharmacol Ther | ヒト ApoB100/CETP トランスジェニックマウスで、CETP 阻害薬と PPARα 作動薬（フェノフィブラート）の脂質プロファイルへの影響を検討 |
| [11342537](https://pubmed.ncbi.nlm.nih.gov/11342537/) | 2001 | 動物研究 | J Biol Chem | フェノフィブラート投与マウスで PLTP 遺伝子の誘導により HDL が大型化 |
| [30271349](https://pubmed.ncbi.nlm.nih.gov/30271349/) | 2018 | 動物研究 | Front Physiol | HDL 値と糞中コレステロール排泄・コレステロール引き抜き能の相関がなく、HDL の機能性が重要であることを示唆 |

## 日本市販情報

フェノフィブラート単剤の承認が 12 件あります。

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 622090701 | リピディル錠５３．３ｍｇ | 有効 |
| 622096801 | トライコア錠５３．３ｍｇ | 有効 |
| 622090801 | リピディル錠８０ｍｇ | 有効 |
| 622096901 | トライコア錠８０ｍｇ | 有効 |
| 622590601 | フェノフィブラート錠８０ｍｇ「武田テバ」 | 有効 |

上表はデータ上の 12 件のうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **知識グラフ上の禁忌関連（添付文書の記載ではありません）**：肝不全・肝疾患、膵炎、胆嚢疾患・胆石症、ミオパチー・横紋筋融解症、腎機能障害、血小板減少・白血球減少・好中球減少などの血液疾患が、知識グラフ上で禁忌の関係として記録されています。
- **薬物相互作用**：データ上 100 件が検出されています。中等度として、スルホニル尿素系薬（アセトヘキサミド、クロルプロパミド、グリメピリド、グリピジド、グリブリド）、各種インスリン製剤、エソメプラゾール、ケノデオキシコール酸などが挙げられます。血糖降下薬との併用では血糖管理に注意が必要です。

警告・禁忌の正式な内容については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測スコアは高いものの、CETP 欠損症そのものを直接検討した臨床試験・文献はなく、動物・機序研究による間接的な示唆のみです。また CETP 欠損症では HDL がすでに高値であり、HDL をさらに上げるフェノフィブラートの治療上の利点は不明です。

**進める場合に必要なもの：**
- 添付文書（PMDA）の警告・禁忌の取得と確認
- 詳細な作用機序データ（DrugBank 等）の補充
- CETP 欠損症における治療上の必要性と目標アウトカムの整理
- ヒトでの症例報告や観察研究などの直接的エビデンスの探索

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Antara (fenofibrate) prescribing information, Lupin Pharmaceuticals, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=24790a18-0291-4b88-a724-acac43b616ce) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：トライコア、リピディル

**販売名（規格別）**：トライコア錠53.3mg、トライコア錠80mg、フェノフィブラート53.3mg錠、フェノフィブラート80mg錠、フェノフィブラート錠53.3mg、フェノフィブラート錠80mg、リピディル錠53.3mg、リピディル錠80mg
<!-- brand-names:end -->

