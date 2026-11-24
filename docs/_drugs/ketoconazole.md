---
layout: default
title: Ketoconazole
parent: 中エビデンスレベル
nav_order: 170
evidence_level: L4
indication_count: 1
last_modified_at: 2026-11-24
description: "Ketoconazole：予測新適応症は尋常性ざ瘡 (acne)（エビデンスレベル L4）。既存適応症：白癬、カンジダ症、癜風、脂漏性皮膚炎"
monitor_inn: "ketoconazole"
predicted_indications: ["acne (disease)"]
---

# Ketoconazole
{: .fs-9 }

エビデンスレベル: **L4** | 予測適応症: **1** 件
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

## ケトコナゾール：ニキビ (acne)
{: .text-alpha }

## 一言要約

ケトコナゾールは外用抗真菌薬（エルゴステロール合成阻害薬）で、元々白癬・カンジダ症・癜風・脂漏性皮膚炎の治療に使用されていました。
TxGNN モデルは**尋常性ざ瘡 (acne)** に有効である可能性を予測しています。
現在 **1 件の臨床試験**（結果未報告）と、**機序を示す in vitro 研究を含む文献**がありますが、エビデンスは限定的です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 白癬、カンジダ症、癜風、脂漏性皮膚炎 |
| 予測新規適応症 | 尋常性ざ瘡 (acne) |
| TxGNN 予測スコア | 0.9980 |
| エビデンスレベル | L4 |
| 日本市販状況 | 販売中（有効な承認 6 件／全 7 件） |
| 承認番号数 | 7 件（有効 6 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

ケトコナゾールは真菌のエルゴステロール合成を阻害するアゾール系抗真菌薬です。米国 FDA が承認した Ketoconazole の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「ケトコナゾールは、真菌細胞膜においてラノステロールからエルゴステロールへの変換を担うチトクロムP-450依存性酵素ラノステロール14α-脱メチル化酵素を阻害することにより、真菌細胞膜の主要構成成分であるエルゴステロールの合成を阻害する。その結果、メチル化ステロール前駆体が蓄積するとともに細胞膜内のエルゴステロールが枯渇し、真菌細胞膜の構造及び機能が脆弱化する。」英語原文："Ketoconazole blocks the synthesis of ergosterol, a key component of the fungal cell membrane, through the inhibition of cytochrome P-450 dependent enzyme lanosterol 14α-demethylase responsible for the conversion of lanosterol to ergosterol in the fungal cell membrane. This results in an accumulation of methylated sterol precursors and a depletion of ergosterol within the cell membrane thus weakening the structure and function of the fungal cell membrane."（[DailyMed: ketoconazole prescribing information, Bryant Ranch Prepack](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=4baebcab-a237-42c0-9183-6f447a44e371)、版 2025-11-18、参照日 2026-11-19）。ただし、既知の薬理学的知見として、全身投与ではステロイド合成酵素（CYP17A1 など）も阻害し、皮脂産生を促すアンドロゲンを低下させる可能性があります。

既存適応症の脂漏性皮膚炎は、マラセチア（Malassezia）属の酵母が関与する疾患です。ざ瘡に似た毛包炎（マラセチア毛包炎）もこの酵母が原因で、ざ瘡と誤診されることがあります。そのため、抗真菌作用が毛包の炎症を抑える可能性があります。

さらに in vitro 研究では、ケトコナゾールがざ瘡の原因菌（*Propionibacterium acnes*）の増殖とリパーゼ活性を阻害することが報告されています。ただし、これらは前臨床段階の知見であり、ヒトでの有効性を直接示すものではありません。

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT07237763](https://clinicaltrials.gov/study/NCT07237763) | 区分なし (NA) | 実施中（募集終了） | 52 | 軽症の面皰型・丘疹膿疱型ざ瘡で、ケトコナゾール 2% クリームとアダパレン 2% クリームを 12 週間比較する無作為化試験。結果は未報告 |

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [28111792](https://pubmed.ncbi.nlm.nih.gov/28111792/) | 2017 | 前臨床（in vitro） | Microbiol Immunol | ケトコナゾールがざ瘡の原因菌のリパーゼ活性と増殖を阻害し、代替治療となる可能性を示唆 |
| [20045949](https://pubmed.ncbi.nlm.nih.gov/20045949/) | 2010 | 前臨床（in vitro） | Biol Pharm Bull | ざ瘡患者から分離した菌に対するアゾール系抗真菌薬の in vitro 活性を評価 |
| [8593718](https://pubmed.ncbi.nlm.nih.gov/8593718/) | 1995 | 臨床研究 | Clin Exp Dermatol | マラセチア毛包炎はしばしばざ瘡と誤診される。患者 62 例の診断と治療試験 |
| [8629828](https://pubmed.ncbi.nlm.nih.gov/8629828/) | 1996 | Case series | Arch Dermatol | 新生児の丘疹膿疱性発疹（新生児ざ瘡と呼ばれるもの）とマラセチア感染との関連を示唆 |
| [8255067](https://pubmed.ncbi.nlm.nih.gov/8255067/) | 1993 | Review | Keio J Med | *Pityrosporum ovale* と癜風、毛包炎、脂漏性皮膚炎などの皮膚疾患との関連を概説 |
| [12566804](https://pubmed.ncbi.nlm.nih.gov/12566804/) | 2003 | Review | Dermatology | 中等症〜重症ざ瘡に対する全身治療の概説（ケトコナゾール自体の検討ではない） |

※ ざ瘡に直接関連する RCT や、ケトコナゾールの有効性を示すヒト対象の確立した研究は確認できませんでした。

## 日本市販情報

現在、日本国内で市販されており、承認には有効なものと薬価基準から削除済みのものがあります（件数はクイック概要を参照）。

<!-- review:begin jp-lic-20261117-ketoconazole-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「7件の承認のうち7件が有効です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（622781200（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-ketoconazole-1 -->

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 622781200 | ケトコナゾール２％クリーム | 薬価削除（2026-03-31） |
| 670005277 | ニゾラールクリーム２％（選） | 有効 |
| 622024501 | ケトコナゾールクリーム２％「ＪＧ」 | 有効 |
| 620005277 | ニゾラールクリーム２％ | 有効 |
| 621654304 | ケトコナゾールクリーム２％「ＮＲ」 | 有効 |

上表はデータ上の 7 件のうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **知識グラフ上の禁忌関連疾患**（添付文書の記載ではありません）：QT延長症候群（先天性を含む）、torsades de pointes、肝疾患、胆嚢疾患、副腎皮質機能不全（アジソン病）、皮膚萎縮、毛細血管拡張症、遺伝性出血性毛細血管拡張症、末梢血管疾患（間欠性跛行、末梢動脈疾患を含む）、無酸症。これらは主に全身投与での懸念を反映している可能性があります。
- **薬物相互作用**（全 100 件中、上位の例）：
  - 重大（Major）：ロペラミド、トリアムシノロン、ブデソニド
  - 中等度（Moderate）：ファモチジン、ラニチジン、ラベプラゾール、オメプラゾール、ヒドロコルチゾン、デキサメタゾン、ベタメタゾン、ピオグリタゾン、アロセトロン、アプレピタント ほか
  - 軽微（Minor）：アムホテリシン B

外用での全身曝露は限られますが、詳細は添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測スコアは高いものの、エビデンスは前臨床研究と、結果未報告の小規模試験 1 件（52 例）にとどまります（L4）。

<!-- review:begin jp-lic-20261106-ketoconazole-1 -->

> **確認による訂正（2026-11-06）**：元の記載は「予測スコアは高いものの、エビデンスは前臨床研究と、結果未報告の小規模試験 1 件（52 例）にとどまります（L4）。また、日本では現在市販中の承認がなく、添付文書に基づく安全性評価も未完了です。」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。最新の件数はクイック概要と日本市販情報にあります。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-ketoconazole-1 -->

**進める場合に必要なもの：**
- NCT07237763 の結果確認（アダパレンとの比較での有効性と安全性）
- 添付文書の警告・禁忌の入手と安全性スクリーニング
- 詳細な作用機序データの補完
- 日本での販売再開または新規承認申請の可能性の検討
- ざ瘡に対する追加のヒト対象 RCT の確認

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-06 | 削除：「また、日本では現在市販中の承認がなく、添付文書に基づく安全性評価も未完了です」 | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: ketoconazole prescribing information, Bryant Ranch Prepack](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=4baebcab-a237-42c0-9183-6f447a44e371) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：ニゾラール

**販売名（規格別）**：ケトコナゾール2%クリーム、ケトコナゾール2%ローション、ケトコナゾールクリーム2%、ニゾラールクリーム2%
<!-- brand-names:end -->

