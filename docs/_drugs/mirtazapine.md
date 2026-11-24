---
layout: default
title: Mirtazapine
parent: モデル予測のみ
nav_order: 212
evidence_level: L5
indication_count: 3
last_modified_at: 2026-11-24
monitor_inn: "Mirtazapine"
predicted_indications: ["Ohdo syndrome and variants", "blepharophimosis - intellectual disability syndrome, Ohdo type", "benign paroxysmal torticollis of infancy"]
description: "Mirtazapine：予測新適応症はOhdo 症候群および関連型 (Ohdo syndrome and variants)（エビデンスレベル L5）。薬価基準の品目：20 件以上"
---

# Mirtazapine
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **3** 件
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

## Mirtazapine: Ohdo 症候群および関連型 (Ohdo syndrome and variants)
{: .text-alpha }

## 一言要約

ミルタザピンは、日本でうつ病治療に使用されてきた抗うつ薬（セロトニン受容体拮抗薬）です。
TxGNN モデルの予測スコア第 1 位は **Ohdo 症候群および関連型 (Ohdo syndrome and variants)** ですが、臨床試験・文献はなく、モデル予測のみの段階です。

> 補足：第 1 位は機序的な裏付けがなく、実質的な検討価値は低いと考えられます。評価の中心は、エビデンスのある気分・不安関連の予測です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | Ohdo 症候群および関連型 (Ohdo syndrome and variants) |
| TxGNN 予測スコア | 0.9942 |
| エビデンスレベル | L5（第 1 位予測）。参考：恐怖症性障害 L2、気分変調性障害・メランコリー L3 |
| 日本市販状況 | 販売中（有効な承認 20 件以上） |
| 承認番号数 | 20 件以上 |
| 推奨決定 | Hold（第 1 位予測について） |

## この予測が妥当である理由

米国 FDA が承認した Mirtazapine の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「大うつ病性障害の治療におけるミルタザピンの作用機序は明らかではない。しかしながら、その有効性は、中枢のシナプス前α 2アドレナリン抑制性自己受容体及びヘテロ受容体に対する拮抗作用、並びに中枢のノルアドレナリン作動性及びセロトニン作動性活性の増強を介している可能性がある。」英語原文："The mechanism of action of mirtazapine for the treatment of major depressive disorder, is unclear. However, its efficacy could be mediated through its activity as an antagonist at central presynaptic α 2 -adrenergic inhibitory autoreceptors and heteroreceptors and enhancing central noradrenergic and serotonergic activity."（[DailyMed: Remeronsoltab (mirtazapine) prescribing information, Organon LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=98ad1917-a094-44f5-a28f-a64a8cfcd887)、版 2025-08-06、参照日 2026-11-19）。ただし、ミルタザピンは中枢のα2 自己受容体・ヘテロ受容体の遮断と、5-HT2/5-HT3/H1 受容体拮抗を通じて、ノルアドレナリンとセロトニンの神経伝達を高める抗うつ薬と整理されています。

第 1 位の Ohdo 症候群（KAT6B 関連の遺伝性神経発達障害）には、この受容体薬理との機序的なつながりが見当たりません。予測は TxGNN モデルのシグナルのみに基づいています。第 2 位（Ohdo 型眼瞼狭小・知的障害症候群）、第 4 位（木質性結膜炎：プラスミノーゲン欠損が原因）、第 5 位（小児発語失行）も同様です。第 3 位（乳児良性発作性斜頸）は片頭痛の類縁としてセロトニン調節が推測されますが、裏付けとなる研究はなく、小児での安全性も未検討です。

一方、気分変調性障害、メランコリー、神経症性うつ病は、既存適応症（うつ病）と近縁の疾患です。同じ抗うつ機序が当てはまり、機序的な妥当性は高いといえます。

## 臨床試験エビデンス

第 1 位予測の Ohdo 症候群には、関連する臨床試験の登録はありません。参考として、エビデンスのある予測（気分変調性障害、メランコリー）の試験を示します。

| 試験番号 | 対象予測 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|---------|--------|------|----------|---------|
| [NCT00080158](https://clinicaltrials.gov/study/NCT00080158) | 気分変調性障害 | Phase 2/3 | 完了 | 120 | 自殺企図のあるうつ病の青年に対する 3 種類の治療の比較。気分変調症やミルタザピンに特化した試験ではない |
| [NCT01916824](https://clinicaltrials.gov/study/NCT01916824) | メランコリー | Phase 4 | 完了 | 53 | 大うつ病における治療が意思決定に与える影響。メランコリー亜型に特化した試験ではない |

## 文献エビデンス

第 1 位予測の Ohdo 症候群には、関連する文献はありません。

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [20715300](https://pubmed.ncbi.nlm.nih.gov/20715300/) | 2010 | RCT | Int Clin Psychopharmacol | 全般性社交不安障害 60 例でミルタザピン（30〜45 mg/日）とプラセボを 12 週間比較 |
| [16282842](https://pubmed.ncbi.nlm.nih.gov/16282842/) | 2005 | RCT | J Clin Psychopharmacol | 女性の社交恐怖 66 例でミルタザピンとプラセボを比較 |
| [11593305](https://pubmed.ncbi.nlm.nih.gov/11593305/) | 2001 | RCT | Braz J Med Biol Res | パニック障害でミルタザピンとフルオキセチンを 8 週間比較（27 例） |
| [21527126](https://pubmed.ncbi.nlm.nih.gov/21527126/) | 2011 | Meta-analysis | J Clin Psychiatry | 気分変調症に対する抗うつ薬のプラセボ対照 RCT のメタ解析 |
| [10569129](https://pubmed.ncbi.nlm.nih.gov/10569129/) | 1999 | Case series | Depress Anxiety | 気分変調性障害患者 15 例にミルタザピン 15〜45 mg を投与 |
| [12490773](https://pubmed.ncbi.nlm.nih.gov/12490773/) | 2003 | Cohort | Int Clin Psychopharmacol | パニック障害 45 例（広場恐怖の有無を含む）のオープン試験 |
| [11712626](https://pubmed.ncbi.nlm.nih.gov/11712626/) | 2001 | Cohort | Int Clin Psychopharmacol | パニック障害 28 例のオープンラベル予備試験 |
| [17419001](https://pubmed.ncbi.nlm.nih.gov/17419001/) | 2008 | Cohort | J Anxiety Disord | 社交恐怖の小児・青年 18 例のオープン試験。10 例（56%）が反応 |
| [36999619](https://pubmed.ncbi.nlm.nih.gov/36999619/) | 2023 | Meta-analysis | Cochrane Database Syst Rev | がん患者のうつ病に対する抗うつ薬 |
| [33424664](https://pubmed.ncbi.nlm.nih.gov/33424664/) | 2020 | Review | Front Psychiatry | 不安障害の薬物療法（承認・適応外を含む）の総説 |

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 672482601 | レメロン錠３０ｍｇ（選） | 有効 |
| 672497001 | リフレックス錠３０ｍｇ（選） | 有効 |
| 622656101 | ミルタザピン錠３０ｍｇ「サワイ」 | 有効 |
| 622660302 | ミルタザピン錠１５ｍｇ「ＫＭＰ」 | 有効 |
| 622667901 | ミルタザピン錠３０ｍｇ「明治」 | 有効 |

データには承認の一部のみが含まれています。上表はそのうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **知識グラフ上の禁忌関連疾患**（添付文書の記載ではなく、モデルの知識グラフに基づく）：てんかん、躁病（双極性障害）、肝疾患、胆嚢疾患、好中球減少、無顆粒球症、起立性低血圧、高トリグリセリド血症、肥満、脳卒中・脳梗塞、心筋梗塞、腎機能障害、セロトニン症候群、薬剤性アカシジアなど。
- **主な薬物相互作用**（合計 100 件のうち一部）：
  - 重大（Major）：ブプロピオン、ロルカセリン、ドラセトロン、パロノセトロン
  - 中等度（Moderate）：ファモチジン、シメチジン、クラリスロマイシン、モルヒネ、デキサメタゾン、アプレピタント、レボフロキサシンなど
- **文献で報告された副作用**：白血球減少、関節痛、膵炎、過量服用時の低体温など。
- 警告・禁忌の添付文書情報は、本レポートの作成時点では確認できていません。詳細は添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**（第 1 位の Ohdo 症候群予測について）

**理由：**
- 臨床試験・文献がなく、機序的な裏付けもないため、モデル予測のみの L5 です。
- 気分変調性障害・メランコリーは L3 で「Proceed with Guardrails」と評価されていますが、既存適応症（うつ病）に近く、真に新しい再利用とは言いにくい面があります。

<!-- review:begin jp-lic-20261106-mirtazapine-1 -->

> **確認による訂正（2026-11-06）**：元の記載は「さらに日本では販売中の承認がありません。／気分変調性障害・メランコリーは L3 で「Proceed with Guardrails」と評価されていますが、既存適応症（うつ病）に近く、真に新しい再利用とは言いにくい面があります。」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-mirtazapine-1 -->

**進める場合に必要なもの：**
- 添付文書（PMDA）の警告・禁忌の取得と解析（現在は未確認で、安全性スクリーニングに進めない）
- 作用機序データの補完（DrugBank）
- 検討対象を、エビデンスのある気分変調性障害・恐怖症性障害・メランコリーに絞り直すこと
- 小児・高齢者を含む対象集団別の安全性モニタリング計画（無顆粒球症、肝機能、セロトニン症候群、併用薬の相互作用）

<!-- review:begin jp-lic-20261106-mirtazapine-2 -->

> **確認による訂正（2026-11-06）**：元の記載は「小児・高齢者を含む対象集団別の安全性モニタリング計画（無顆粒球症、肝機能、セロトニン症候群、併用薬の相互作用）／日本での販売承認が整理済みである点を踏まえた、再申請または他国の承認状況の確認」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-mirtazapine-2 -->

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-06 | 削除：「さらに日本では販売中の承認がありません」 | 訂正 | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-06 | 削除：「日本での販売承認が整理済みである点を踏まえた、再申請または他国の承認状況の確認」 | 訂正 | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Remeronsoltab (mirtazapine) prescribing information, Organon LLC](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=98ad1917-a094-44f5-a28f-a64a8cfcd887) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：リフレックス、レメロン

**販売名（規格別）**：ミルタザピン15mg口腔内崩壊錠、ミルタザピン15mg錠、ミルタザピン30mg口腔内崩壊錠、ミルタザピン30mg錠、ミルタザピンOD錠15mg、ミルタザピンOD錠30mg、ミルタザピン錠15mg、ミルタザピン錠30mg、リフレックス錠15mg、リフレックス錠30mg、レメロン錠15mg、レメロン錠30mg
<!-- brand-names:end -->

