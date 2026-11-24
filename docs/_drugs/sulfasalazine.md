---
layout: default
title: Sulfasalazine
parent: モデル予測のみ
nav_order: 288
evidence_level: L5
indication_count: 8
last_modified_at: 2026-11-24
monitor_inn: "Sulfasalazine"
predicted_indications: ["brachydactyly-syndactyly syndrome", "colobomatous microphthalmia-rhizomelic dysplasia syndrome", "congenital hypotrichosis with juvenile macular dystrophy", "osteoarthritis", "WHIM syndrome", "acromesomelic dysplasia, Hunter-Thompson type", "brachyolmia-amelogenesis imperfecta syndrome", "myosclerosis"]
description: "Sulfasalazine：予測新適応症は合指（趾）症を伴う短指症候群 (brachydactyly-syndactyly syndrome)（エビデンスレベル L5）。薬価基準の品目：11 件（現在収載 6 件）"
---

# Sulfasalazine
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

## Sulfasalazine: 合指（趾）症を伴う短指症候群 (brachydactyly-syndactyly syndrome)
{: .text-alpha }

## 一言要約

サラゾスルファピリジン（Sulfasalazine）は、関節リウマチや潰瘍性大腸炎などの炎症性疾患の治療に使われてきた薬です。
TxGNN モデルは、先天性の発生異常である**合指（趾）症を伴う短指症候群 (Brachydactyly-syndactyly syndrome)** に有効である可能性を予測しています。
ただし、この予測を支持する臨床試験・文献は **0 件**で、モデル予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 合指（趾）症を伴う短指症候群 (brachydactyly-syndactyly syndrome) |
| TxGNN 予測スコア | 0.9994 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 6 件／全 11 件） |
| 承認番号数 | 11 件（有効 6 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Sulfasalazine の添付文書（Prescribing Information）の「Clinical Pharmacology」の項によると（非公式訳）、「スルファサラジン（SSZ）又はその代謝物である5-アミノサリチル酸（5-ASA）及びスルファピリジン（SP）の作用機序は、動物及びin vitroモデルで認められている抗炎症作用及び／又は免疫調節作用、結合組織に対する親和性、並びに／又は動物における オートラジオグラフィー試験で示されたように、漿液、肝臓及び腸壁において比較的高濃度に達することに関連している可能性がある。潰瘍性大腸炎において、SSZ、SP及び5-ASAの直腸内投与を用いた臨床試験により、主たる治療作用は5-ASA部分に存在する可能性が示されている。」英語原文："The mode of action of sulfasalazine (SSZ) or its metabolites, 5-aminosalicylic acid (5-ASA) and sulfapyridine (SP), may be related to the anti-inflammatory and/or immunomodulatory properties that have been observed in animal and in vitro models, to its affinity for connective tissue, and/or to the relatively high concentration it reaches in serous fluids, the liver and intestinal walls, as demonstrated in autoradiographic studies in animals. In ulcerative colitis, clinical studies utilizing rectal administration of SSZ, SP and 5-ASA have indicated that the major therapeutic action may reside in the 5-ASA moiety."（[DailyMed: Azulfidine En-Tabs (sulfasalazine) prescribing information, Pfizer Laboratories Div Pfizer Inc](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=b9ef541a-93c8-4428-ba45-398aa0b327d1)、版 2026-10-27、参照日 2026-11-19）。既知の情報では、サラゾスルファピリジンは炎症性腸疾患や関節炎で有効性が示されている抗炎症薬です。作用は NF-κB 抑制やプロスタグランジン・ロイコトリエンの産生抑制によると考えられています。

一方、合指（趾）症を伴う短指症候群は、四肢の形成異常を特徴とする発生性の疾患です。上記の抗炎症作用との間に、確立した機序上の関連は見つかっていません。

そのため、この予測の妥当性を裏付ける根拠は現時点でありません。TxGNN の高スコアは、ネットワーク上の類似性に基づく仮説にとどまります。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

## 日本市販情報

日本では販売されており、承認には有効なものと薬価基準から削除済みのものがあります（件数はクイック概要を参照）。主な承認は以下のとおりです。承認適応症の記載はデータにありませんでした。

<!-- review:begin jp-lic-20261117-sulfasalazine-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「日本では販売されており、11 件の承認のうち 11 件が有効です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（622746900（廃止年月日 2026-03-31）、621442802（廃止年月日 2026-03-31）、622039002（廃止年月日 2026-03-31）、670004897（廃止年月日 2026-03-31）、622982400（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-sulfasalazine-1 -->

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 610463004 | アザルフィジンＥＮ錠２５０ｍｇ | 有効 |
| 620004897 | アザルフィジンＥＮ錠５００ｍｇ | 有効 |
| 670004897 | アザルフィジンＥＮ錠５００ｍｇ（選） | 薬価削除（2026-03-31） |
| 622161402 | サラゾスルファピリジン腸溶錠２５０ｍｇ「ＣＨ」 | 有効 |
| 621442905 | サラゾスルファピリジン腸溶錠５００ｍｇ「ＣＨ」 | 有効 |

上表はデータ上の 11 件のうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **禁忌・慎重を要する疾患（ナレッジグラフ上の情報。添付文書の記載ではありません）**：ポルフィリン症（遺伝性を含む）、腎疾患、肝疾患、胆嚢疾患、膿尿管症、尿路閉塞、喘息（内因性・アレルギー性）、好中球減少症、無顆粒球症、再生不良性貧血、G6PD 欠損症、アセチル化能低下、糖原病、シスチン尿症、ガラクトース血症
- **薬物相互作用**：100 件の相互作用が登録されています。
  - 重大（Major）：プリロカイン（外用）、ヒト免疫グロブリン G（静注）、メテナミン
  - 中等度（Moderate）：ケトロラク、イブプロフェン、セレコキシブなどの NSAIDs、アザチオプリン、エストラジオール、エチニルエストラジオール、アムホテリシン B、アミカシン、アシクロビル、アルペリシブ、アパルタミド
  - 軽微（Minor）：葉酸

## 結論と次のステップ

**決定：Hold**

**理由：**
- 予測新規適応症には臨床試験も文献もなく、機序上の関連も見つかっていません。エビデンスは L5（モデル予測のみ）です。

<!-- review:begin jp-lic-20261106-sulfasalazine-1 -->

> **確認による訂正（2026-11-06）**：元の記載は「エビデンスは L5（モデル予測のみ）です。／日本では現在有効な承認がなく、国内での開発・使用の前提も整っていません。」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。最新の件数はクイック概要と日本市販情報にあります。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-sulfasalazine-1 -->

**進める場合に必要なもの：**
- 疾患の病態（発生異常に関わる経路）とサラゾスルファピリジンの作用との機序的な関連の検証
- 前臨床研究による裏付け
- 添付文書にある警告・禁忌の確認（今回のデータには含まれていません）
- 日本の承認状況の再確認

**参考：** 同じ予測リストのうち、**変形性関節症 (Osteoarthritis)**（予測スコア 0.9964）には、軟骨破壊の抑制を示す動物実験・in vitro の文献があり、エビデンスレベルは L4 です。ただし臨床試験はありません。優先順位を検討する際は、こちらの方向性も併せて確認する価値があります。

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-06 | 削除：「日本では現在有効な承認がなく、国内での開発・使用の前提も整っていません」 | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Azulfidine En-Tabs (sulfasalazine) prescribing information, Pfizer Laboratories Div Pfizer Inc](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=b9ef541a-93c8-4428-ba45-398aa0b327d1) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：アザルフィジンEN

**販売名（規格別）**：アザルフィジンEN錠250mg、アザルフィジンEN錠500mg、サラゾスルファピリジン250mg腸溶錠、サラゾスルファピリジン500mg腸溶錠、サラゾスルファピリジン腸溶錠250mg、サラゾスルファピリジン腸溶錠500mg
<!-- brand-names:end -->

