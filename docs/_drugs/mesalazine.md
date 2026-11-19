---
layout: default
title: Mesalazine
parent: モデル予測のみ
nav_order: 203
evidence_level: L5
indication_count: 6
monitor_inn: "mesalazine"
predicted_indications: ["congenital hypotrichosis with juvenile macular dystrophy", "osteoarthritis", "rheumatoid arthritis", "seborrheic keratosis", "vulvar inverted follicular keratosis", "pseudoachondroplasia"]
last_modified_at: 2026-11-17
description: "Mesalazine：予測新適応症は若年性黄斑ジストロフィーを伴う先天性乏毛症 (Congenital Hypotrichosis with Juvenile Macular…（エビデンスレベル L5）。既存適応症：潰瘍性大腸炎、クローン病（抗炎症薬）"
---

# Mesalazine
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **6** 件
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

## メサラジン：潰瘍性大腸炎・クローン病から若年性黄斑ジストロフィーを伴う先天性乏毛症へ
{: .text-alpha }

## 一言要約

メサラジン（5-ASA）は抗炎症薬で、元々は潰瘍性大腸炎とクローン病の治療に使用されていました。
TxGNN モデルは**若年性黄斑ジストロフィーを伴う先天性乏毛症 (Congenital Hypotrichosis with Juvenile Macular Dystrophy)** に有効である可能性を予測しています。
ただし、この予測を支持する臨床試験・文献は **0 件**で、モデル予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 潰瘍性大腸炎、クローン病（抗炎症薬） |
| 予測新規適応症 | 若年性黄斑ジストロフィーを伴う先天性乏毛症 (Congenital Hypotrichosis with Juvenile Macular Dystrophy) |
| TxGNN 予測スコア | 0.9965 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 12 件／全 13 件） |
| 承認番号数 | 13 件（有効 12 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Mesalazine の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「メサラミンの作用機序は完全には解明されていないが、結腸上皮細胞に対して局所的な抗炎症作用を示すと考えられる。潰瘍性大腸炎患者では、シクロオキシゲナーゼ経路及びリポキシゲナーゼ経路の両方を介した粘膜におけるアラキドン酸代謝物の産生が増加しており、メサラミンはシクロオキシゲナーゼを遮断し、結腸におけるプロスタグランジン産生を阻害することにより炎症を軽減する可能性がある。」英語原文："The mechanism of action of mesalamine is not fully understood, but it appears to have a topical anti-inflammatory effect on the colonic epithelial cells. Mucosal production of arachidonic acid metabolites, both through the cyclooxygenase and lipoxygenase pathways, is increased in patients with ulcerative colitis, and it is possible that mesalamine diminishes inflammation by blocking cyclooxygenase and inhibiting prostaglandin production in the colon."（[DailyMed: Lialda (mesalamine) prescribing information, Takeda Pharmaceuticals America, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=3098a080-be86-4265-9818-7fc4beab77b7)、版 2026-10-26、参照日 2026-11-19）。既知の情報によると、メサラジンは COX／リポキシゲナーゼ阻害や PPAR-γ 活性化を介した抗炎症作用を持つ薬剤で、潰瘍性大腸炎とクローン病での有効性が確立しています。

一方、予測された疾患は CDH3 遺伝子に関連する遺伝性疾患です。メサラジンの抗炎症作用との間に妥当な機序的関連は見当たりません。高い TxGNN スコアは TxGNN モデル（深層学習）が出力したもので、関連する疾患間でモデルが学習した類似性を反映している可能性があり、生物学的な根拠ではありません。
既存適応症（腸管の炎症性疾患）との類似性も未評価です。現時点では、機序的に適用可能とは言えません。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 620506801 | ペンタサ錠２５０ｍｇ | 錠２５０ｍｇ | 抗炎症薬。潰瘍性大腸炎、クローン病 |
| 621867201 | ペンタサ錠５００ｍｇ | 錠５００ｍｇ | 抗炎症薬。潰瘍性大腸炎、クローン病 |
| 660470002 | ペンタサ注腸１ｇ | 注腸１ｇ | 抗炎症薬。潰瘍性大腸炎、クローン病 |
| 622924101 | メサラジン徐放錠２５０ｍｇ「トーワ」 | 錠２５０ｍｇ「トーワ」 | 抗炎症薬。潰瘍性大腸炎、クローン病 |
| 622065002 | メサラジン錠５００ｍｇ「ケミファ」 | 錠５００ｍｇ「ケミファ」 | 抗炎症薬。潰瘍性大腸炎、クローン病 |

登録されている承認 13 件のうち 12 件が有効です（1 件は薬価基準から削除済み）。上記は主要な 5 件のみを記載しています。

<!-- review:begin jp-lic-20261117-mesalazine-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「登録されている承認 13 件はすべて有効です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、データ上の 13 件のうち有効（収載中）は 12 件で、1 件は経過措置期間満了などにより薬価基準から削除されています（622167101（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-mesalazine-1 -->

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用データは 100 件あります。主なものは次のとおりです。
  - 重大（Major）：ボツリヌス抗毒素免疫グロブリン、シドホビル
  - 中等度（Moderate）：NSAIDs（ケトロラク、イブプロフェン、セレコキシブ、ブロムフェナク）、アシクロビル、アミノグリコシド（アミカシン）、アムホテリシン B 製剤、アザチオプリン、シスプラチン、バシトラシン、カプレオマイシン、スルホニル尿素系薬（クロルプロパミド、アセトヘキサミド）。腎毒性や血液毒性の増強が懸念されるものが目立ちます。
- **知識グラフ上の禁忌関連疾患**：腎疾患、間質性腎炎、肝疾患、胆嚢疾患、好中球減少症、無顆粒球症、貧血（大球性貧血を含む）、幽門狭窄などが挙がっています。

警告・禁忌の正式な内容は添付文書で確認してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
臨床試験も文献もなく、エビデンスはモデル予測のみ（L5）です。メサラジンの作用機序と、CDH3 関連の遺伝性疾患との間に妥当な機序的関連も見当たりません。現時点で再利用を進める根拠はありません。

**進める場合に必要なもの：**
- 詳細な作用機序データ（MOA）の取得と、疾患の病態との機序的関連の検証
- 前臨床研究による裏付け
- 添付文書（警告・禁忌）の確認と安全性評価

<!-- review:begin jp-lic-20261106-mesalazine-1 -->

> **確認による訂正（2026-11-06）**：元の記載は「添付文書（警告・禁忌）の確認と安全性評価／日本で現在有効な承認がないため、販売・供給状況の確認」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。データ上の収載は 13 件、うち有効 13 件です。最新の件数はクイック概要と日本市販情報にあります。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-mesalazine-1 -->

なお、予測順位 3 位の**関節リウマチ**には、サラゾスルファピリジン（メサラジンを活性代謝物とする既存の抗リウマチ薬）に関する文献があり、L4 の研究課題候補です。ただし、抗リウマチ作用はスルファピリジン部分によるとされ、メサラジン単独での裏付けは間接的です。優先的に検討するなら、この候補の方が現実的です。

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-06 | 削除：「日本で現在有効な承認がないため、販売・供給状況の確認」 | 訂正 | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正 | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Lialda (mesalamine) prescribing information, Takeda Pharmaceuticals America, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=3098a080-be86-4265-9818-7fc4beab77b7) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：アサコール、ペンタサ、リアルダ

**販売名（規格別）**：アサコール錠400mg、ペンタサ注腸1g、ペンタサ錠250mg、ペンタサ錠500mg、メサラジン徐放錠250mg、メサラジン徐放錠500mg、メサラジン注腸1g、メサラジン腸溶錠400mg、メサラジン錠250mg、メサラジン錠500mg
<!-- brand-names:end -->

