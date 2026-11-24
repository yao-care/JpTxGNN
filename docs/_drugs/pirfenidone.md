---
layout: default
title: Pirfenidone
parent: モデル予測のみ
nav_order: 247
evidence_level: L5
indication_count: 10
monitor_inn: "pirfenidone"
predicted_indications: ["extracutaneous mastocytoma", "dermatofibrosarcoma protuberans", "aggressive systemic mastocytosis", "heart fibrosarcoma", "conventional fibrosarcoma", "autosomal recessive familial Mediterranean fever", "kidney fibrosarcoma", "hepatic infarction", "fibroblastic neoplasm", "low grade fibromyxoid sarcoma"]
last_modified_at: 2026-11-24
description: "Pirfenidone：予測新適応症は肥満細胞腫 (Extracutaneous mastocytoma)（予測スコア第 1 位）。文献で裏付けが得られた候補は線維芽細胞性腫瘍…（エビデンスレベル L5）。既存適応症：特発性肺線維症"
---

# Pirfenidone
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **10** 件
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

## ピルフェニドン：特発性肺線維症から肥満細胞腫（extracutaneous mastocytoma）へ
{: .text-alpha }

## 一言要約

ピルフェニドンは抗線維化薬で、元々特発性肺線維症の治療に使用されていました。
TxGNN モデルの予測スコア第 1 位は**肥満細胞腫（extracutaneous mastocytoma）**ですが、裏付けとなる研究は見つかっていません。実際の研究が確認できた中で最も有望な候補は**線維芽細胞性腫瘍 (Fibroblastic neoplasm)** で、**6 編の文献**（主に in vitro 研究と症例報告）があります。臨床試験の登録はなく、エビデンスは限定的です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 特発性肺線維症 |
| 予測新規適応症 | 肥満細胞腫 (Extracutaneous mastocytoma)（予測スコア第 1 位）。文献で裏付けが得られた候補は線維芽細胞性腫瘍 (Fibroblastic neoplasm) |
| TxGNN 予測スコア | 0.9971（第 1 位）／線維芽細胞性腫瘍：0.9923（第 9 位） |
| エビデンスレベル | 第 1 位：L5／線維芽細胞性腫瘍：L4 |
| 日本市販状況 | 販売中（有効な承認 3 件／全 3 件） |
| 承認番号数 | 3 件（有効 3 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Pirfenidone の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「IPF の治療におけるピルフェニドンの作用機序は確立されていない。」英語原文："The mechanism of action of pirfenidone in the treatment of IPF has not been established."（[DailyMed: Esbriet (pirfenidone) prescribing information, Genentech, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=2e8c3537-36d7-4de5-9b5c-7a624b9a9e6e)、版 2025-12-05、参照日 2026-11-19）。ただし文献によると、ピルフェニドンは TGF-β、PDGF、FGF、EGF などの増殖因子シグナルを抑え、線維芽細胞の増殖とコラーゲン産生を減らす非細胞毒性の経口抗線維化薬とされています。

第 1 位の肥満細胞腫、第 3 位の侵攻性全身性肥満細胞症は、KIT 変異が主な原因とされます。ピルフェニドンの機序との関連を示す根拠はなく、予測はモデルのスコアだけに基づいています。

線維芽細胞由来の腫瘍（線維肉腫、線維芽細胞性腫瘍など）は、抗線維芽細胞作用との概念的な関連があります。デュピュイトラン病由来の線維芽細胞では、TGF-β1 による筋線維芽細胞化と非 SMAD シグナルの抑制が in vitro で示されています。ただし抗線維化作用が抗腫瘍効果を意味するわけではありません。隆起性皮膚線維肉腫（DFSP）は COL1A1-PDGFB 融合が原因で、ピルフェニドンを支持する証拠はありません。

## 文献エビデンス

対象は線維芽細胞性腫瘍（第 9 位）です。臨床試験の登録はありません。

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [12907346](https://pubmed.ncbi.nlm.nih.gov/12907346/) | 2003 | 症例集積（パイロット） | Am J Gastroenterol | 家族性大腸腺腫症に伴うデスモイド腫瘍に対するピルフェニドンの有効性を評価したパイロット試験 |
| [27835939](https://pubmed.ncbi.nlm.nih.gov/27835939/) | 2016 | In vitro | BMC Musculoskelet Disord | デュピュイトラン病由来線維芽細胞で TGF-β1 を介した作用を抑制 |
| [30927912](https://pubmed.ncbi.nlm.nih.gov/30927912/) | 2019 | In vitro | BMC Musculoskelet Disord | TGF-β1 刺激による非 SMAD シグナル経路への影響を検討 |
| [35129055](https://pubmed.ncbi.nlm.nih.gov/35129055/) | 2022 | In vitro | Pharm Dev Technol | デュピュイトラン病に対する局所注射用抗線維化薬としての可能性 |
| [29702057](https://pubmed.ncbi.nlm.nih.gov/29702057/) | 2018 | 症例報告 | Perm J | ピルフェニドン使用後に未分化多形肉腫が発生した症例（安全性上の注意） |
| [32572469](https://pubmed.ncbi.nlm.nih.gov/32572469/) | 2020 | 症例報告 | Rheumatology (Oxford) | 全身性強皮症患者で、ミコフェノール酸モフェチルとピルフェニドンにより多発性皮膚線維腫が悪化 |

## 日本市販情報

3 件の承認はすべて有効で、日本で販売されています。

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 620008559 | ピレスパ錠２００ｍｇ | 有効 |
| 670008559 | ピレスパ錠２００ｍｇ（選） | 有効 |
| 622788201 | ピルフェニドン錠２００ｍｇ「日医工」 | 有効 |

<!-- licenses:end -->

## 安全性に関する考慮事項

- **薬物相互作用**：100 件の相互作用が報告されており、リストの上位はいずれも中等度（Moderate）です。主なものは次のとおりです。
  - CYP 関連：シメチジン、オメプラゾール、ランソプラゾール、エソメプラゾール、ブプロピオン、チクロピジン
  - 抗真菌薬など：ミコナゾール
  - その他：エリグルスタット、オベチコール酸、ナルトレキソン、ニチシノン、ジスルフィラム、プリマキン、イバカフトル
- **腫瘍に関する安全性の注意**：ピルフェニドン使用後に肉腫が発生した症例報告（PMID 29702057）と、皮膚線維腫が悪化した症例報告（PMID 32572469）があります。因果関係は未確認ですが、腫瘍領域への応用では注意が必要です。

警告・禁忌については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 予測上位の疾患（肥満細胞腫、線維肉腫など）には臨床試験も文献もなく、エビデンスは L5（モデル予測のみ）です。
- 線維芽細胞性腫瘍には L4 の前臨床・小規模パイロット研究がありますが、腫瘍発生に関する症例報告もあり、現段階で臨床開発に進める根拠は不十分です。
- 日本では販売されており、3 件の承認すべてが有効です。

**進める場合に必要なもの：**
- 添付文書の警告・禁忌の確認（現在データなし）と、安全性スクリーニングの実施
- 詳細な作用機序データの取得
- 線維芽細胞性腫瘍およびデスモイド腫瘍での前臨床データ（腫瘍細胞株、動物モデル）の追加
- 腫瘍発生リスクに関する安全性の精査
- 剤形・投与経路の適合性評価（現在は経口錠のみ）

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Esbriet (pirfenidone) prescribing information, Genentech, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=2e8c3537-36d7-4de5-9b5c-7a624b9a9e6e) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：ピレスパ

**販売名（規格別）**：ピルフェニドン錠200mg、ピレスパ錠200mg
<!-- brand-names:end -->

