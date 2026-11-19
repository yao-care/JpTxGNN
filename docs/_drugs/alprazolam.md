---
layout: default
title: Alprazolam
parent: 中エビデンスレベル
nav_order: 21
evidence_level: L3
indication_count: 2
last_modified_at: 2026-11-20
monitor_inn: "Alprazolam"
predicted_indications: ["insomnia (disease)", "benign paroxysmal torticollis of infancy"]
description: "Alprazolam：予測新適応症は不眠症 (insomnia (disease))（エビデンスレベル L3）。薬価基準の品目：14 件（現在収載 12 件）"
---

# Alprazolam
{: .fs-9 }

エビデンスレベル: **L3** | 予測適応症: **2** 件
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

## Alprazolam: 不眠症 (insomnia (disease))
{: .text-alpha }

## 一言要約

アルプラゾラムはベンゾジアゼピン系の薬で、日本では複数の製剤が市販されています。
TxGNN モデルは**不眠症 (insomnia (disease))** に有効である可能性を予測しています。
関連する臨床試験の登録はなく、不眠症を直接扱った文献は**観察研究 1 件**のみです（収集した文献は 18 編）。エビデンスレベルは **L3** です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 不眠症 (insomnia (disease)) |
| TxGNN 予測スコア | 0.9981 |
| エビデンスレベル | L3 |
| 日本市販状況 | 販売中（有効な承認 12 件／全 14 件） |
| 承認番号数 | 14 件（有効 12 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Alprazolam の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「アルプラゾラムは1,4-ベンゾジアゼピン系薬剤である。アルプラゾラムは、脳内のγ-アミノ酪酸A（GABA A ）受容体のベンゾジアゼピン結合部位に結合し、GABAを介したシナプス抑制を増強することにより、パニック障害の治療効果を発揮する。」英語原文："Alprazolam is a 1,4 benzodiazepine. Alprazolam exerts its effect for the treatment of panic disorder through binding to the benzodiazepine site of gamma‑aminobutyric acid-A (GABA A ) receptors in the brain and enhances GABA-mediated synaptic inhibition."（[DailyMed: Alprazolam Xr (alprazolam) prescribing information, Mylan Pharmaceuticals Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=1338d1c9-7c75-42ed-95f3-9eb1b6fc51d3)、版 2025-02-11、参照日 2026-11-19）。ただしアルプラゾラムはベンゾジアゼピン系に属し、一般に GABA-A 受容体を介した抑制性神経伝達を増強します。この作用により鎮静・催眠作用が生じるため、機序的には不眠症にも適用できる可能性があります。

一方、収集できた文献の大半は、使用実態、安全性、併存疾患に関する間接的な研究です。不眠症に対する有効性を検証する専用の試験は見当たりません。冠動脈疾患と不眠症を併発した患者でアルプラゾラムを使った観察研究が 1 件あり、これが最も直接的な根拠です。予測は妥当な方向性にありますが、有効性の確認は今後の課題です。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [39183410](https://pubmed.ncbi.nlm.nih.gov/39183410/) | 2024 | 観察研究（後ろ向き） | Medicine | 冠動脈疾患と不眠症の患者 116 例で、アルプラゾラム単独の対照群と、督脈灸・耳鍼を併用した群を比較し、症状、心機能、神経伝達物質への影響を検討 |
| [36692463](https://pubmed.ncbi.nlm.nih.gov/36692463/) | 2023 | メタ解析 | Acta Pharm | 慢性非感染性疾患をもつ高齢者への鎮静薬について、用量、転帰、有害事象を整理 |
| [23330992](https://pubmed.ncbi.nlm.nih.gov/23330992/) | 2013 | Review | Expert Opin Drug Metab Toxicol | 抗不安薬の薬物動態を概説 |
| [37984023](https://pubmed.ncbi.nlm.nih.gov/37984023/) | 2024 | コホート/予測モデル | Value Health Reg Issues | ベンゾジアゼピン使用の動向と経済的負担を検討。長期使用に伴う依存、転倒、記憶障害のリスクを指摘 |
| [15341891](https://pubmed.ncbi.nlm.nih.gov/15341891/) | 2004 | 処方実態調査 | Sleep Med | 大規模マネージドケア集団における不眠症治療薬の処方パターンを解析 |
| [37801512](https://pubmed.ncbi.nlm.nih.gov/37801512/) | 2023 | 基礎研究（マウス） | Aging | アルプラゾラムの反復投与がミトコンドリア機能障害を介して海馬依存性記憶を低下させることを示した |

## 日本市販情報

有効な承認は 12 件（ほかに 2 件が薬価基準から削除済み）で、いずれも単剤製剤です。主なものを示します。

<!-- review:begin jp-lic-20261117-alprazolam-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「有効な承認は 14 件で、すべて単剤製剤です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、データ上の 14 件のうち有効（収載中）は 12 件で、2 件は経過措置期間満了などにより薬価基準から削除されています（671170508（廃止年月日 2026-03-31）、671170499（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-alprazolam-1 -->

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 611170508 | ソラナックス0.4mg錠 | 錠 | 抗不安薬、マイナートランキライザー、催眠鎮静薬 |
| 611170509 | ソラナックス0.8mg錠 | 錠 | 抗不安薬、マイナートランキライザー、催眠鎮静薬 |
| 611170499 | コンスタン0.4mg錠 | 錠 | 抗不安薬、マイナートランキライザー、催眠鎮静薬 |
| 620006836 | アルプラゾラム錠0.4mg「トーワ」 | 錠 | 抗不安薬、マイナートランキライザー、催眠鎮静薬 |
| 620049901 | アルプラゾラム錠0.4mg「サワイ」 | 錠 | 抗不安薬、マイナートランキライザー、催眠鎮静薬 |

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用は 100 件が記録されています。
  - **重大（Major）**：モルヒネ、リポソーム化モルヒネ。中枢抑制作用が重なるおそれがあります。
  - **中等度（Moderate）**：アプレピタント、ブプロピオン、シメチジン、クラリスロマイシン、クロトリマゾール、ミコナゾール、ドロナビノール、エリグルスタット、メトクロプラミドなど。
  - **軽度（Minor）**：水酸化アルミニウム、炭酸カルシウム、マグネシウム系制酸薬、ベタメタゾン、デキサメタゾンなど。

警告・禁忌については、添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 不眠症を直接扱った根拠は後ろ向き観察研究 1 件のみで、臨床試験の登録もなく、エビデンスレベルは L3 にとどまります。
- 不眠症に対する有効性と安全性を示す専用の研究が必要です。

**進める場合に必要なもの：**
- 不眠症に対する有効性を検証する無作為化比較試験の計画、または既存の観察データの再解析
- 詳細な作用機序データの補充
- 添付文書の警告・禁忌の確認と、安全性評価（依存、認知機能、転倒リスク、高齢者への影響）
- モルヒネなど中枢抑制薬との併用管理方針の整理

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正 | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Alprazolam Xr (alprazolam) prescribing information, Mylan Pharmaceuticals Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=1338d1c9-7c75-42ed-95f3-9eb1b6fc51d3) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：コンスタン、ソラナックス

**販売名（規格別）**：アルプラゾラム0.4mg錠、アルプラゾラム0.8mg錠、アルプラゾラム錠0.4mg、アルプラゾラム錠0.8mg、コンスタン0.4mg錠、コンスタン0.8mg錠、ソラナックス0.4mg錠、ソラナックス0.8mg錠
<!-- brand-names:end -->

