---
layout: default
title: Prednisolone
parent: 高エビデンスレベル
nav_order: 253
evidence_level: L2
indication_count: 9
last_modified_at: 2026-11-24
description: "Prednisolone：予測新適応症は円形脱毛症 (Alopecia Areata)（エビデンスレベル L2）。既存適応症：乾癬、掌蹠膿疱症（外用製剤）／関節リウマチ、全身性エリテマトーデス、ネフローゼ症候群、気管支喘息など多数（内服製剤）"
monitor_inn: "Prednisolone"
predicted_indications: ["alopecia areata", "alopecia mucinosa", "telogen effluvium", "Quinquaud's folliculitis decalvans", "hereditary hypotrichosis with recurrent skin vesicles", "alopecia antibody deficiency", "alopecia-intellectual disability-hypergonadotropic hypogonadism syndrome", "atrichia with papular lesions", "prolapse of lacrimal gland"]
---

# Prednisolone
{: .fs-9 }

エビデンスレベル: **L2** | 予測適応症: **9** 件
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

## プレドニゾロン：乾癬・掌蹠膿疱症などから円形脱毛症へ
{: .text-alpha }

## 一言要約

プレドニゾロンはグルココルチコイド受容体作動薬で、元々関節リウマチ、膠原病、ネフローゼ症候群、皮膚疾患など幅広い炎症・自己免疫疾患の治療に使用されています。
TxGNN モデルは**円形脱毛症 (alopecia areata)** に有効である可能性を予測しており、現在 **20 編の文献**（RCT 1 件、ネットワークメタアナリシス・システマティックレビューを含む）がこの方向性を支持しています。登録された臨床試験はありません。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 乾癬、掌蹠膿疱症（外用製剤）／関節リウマチ、全身性エリテマトーデス、ネフローゼ症候群、気管支喘息など多数（内服製剤） |
| 予測新規適応症 | 円形脱毛症 (Alopecia Areata) |
| TxGNN 予測スコア | 0.9999 |
| エビデンスレベル | L2 |
| 日本市販状況 | 販売中（有効な承認 38 件以上） |
| 承認番号数 | 39 件以上 |
| 推奨決定 | Proceed with Guardrails |

## この予測が妥当である理由

米国 FDA が承認した Prednisolone の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「プレドニゾロンは、主として糖質コルチコイド作用を有する合成副腎皮質ステロイド薬である。これらの作用の一部は内因性糖質コルチコステロイドの生理作用を再現するが、その他の作用は必ずしも副腎ホルモンの正常な機能を反映するものではなく、本剤の高用量の治療量を投与した後にのみ認められる。」英語原文："Prednisolone is a synthetic adrenocortical steroid drug with predominantly glucocorticoid properties. Some of these properties reproduce the physiological actions of endogenous glucocorticosteroids, but others do not necessarily reflect any of the adrenal hormones' normal functions; they are seen only after administration of large therapeutic doses of the drug."（[DailyMed: Orapred Odt (prednisolone sodium phosphate) prescribing information, Advanz Pharma (US) Corp.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=1e379543-c4cf-4e72-953b-db15b7f0c2a1)、版 2025-06-03、参照日 2026-11-19）。既知の情報によると、プレドニゾロンはグルココルチコイド受容体作動薬で、抗炎症・免疫抑制作用を持ち、多数の自己免疫疾患・炎症性疾患で有効性が確立されています。

円形脱毛症は、T 細胞が毛包を攻撃する自己免疫性の非瘢痕性脱毛症です。グルココルチコイドは T 細胞性の自己免疫攻撃を抑え、毛包の免疫特権の破綻に伴う炎症を鎮めると考えられます。そのため、既存の自己免疫疾患への適応と機序的に整合します。

ただし、エビデンスは小規模なプラセボ対照パルス療法試験とシステマティックレビューが中心です。投与中止後の再発とステロイドの副作用が主な課題です。

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [15692475](https://pubmed.ncbi.nlm.nih.gov/15692475/) | 2005 | RCT | J Am Acad Dermatol | 円形脱毛症に対する経口プレドニゾロンパルス療法のプラセボ対照試験 |
| [37870096](https://pubmed.ncbi.nlm.nih.gov/37870096/) | 2023 | Meta-analysis | Cochrane Database Syst Rev | 円形脱毛症治療（免疫抑制薬、発毛促進薬、接触免疫療法）のネットワークメタアナリシス |
| [30191561](https://pubmed.ncbi.nlm.nih.gov/30191561/) | 2019 | Meta-analysis | Australas J Dermatol | 円形脱毛症に対する全身治療のシステマティックレビュー |
| [37992355](https://pubmed.ncbi.nlm.nih.gov/37992355/) | 2023 | Review | Dermatol Pract Concept | コルチコステロイドパルス療法の有効性、再発率、副作用、予後因子のレビュー |
| [36461625](https://pubmed.ncbi.nlm.nih.gov/36461625/) | 2023 | Review | Pediatr Dermatol | 小児におけるパルス用量コルチコステロイド療法の用量設定と副作用 |
| [28140540](https://pubmed.ncbi.nlm.nih.gov/28140540/) | 2017 | Cohort | J Dtsch Dermatol Ges | 重症小児円形脱毛症に対する高用量・低用量の逐次全身ステロイド療法 |
| [21572877](https://pubmed.ncbi.nlm.nih.gov/21572877/) | 2009 | Case series | Dermatoendocrinol | 円形脱毛症に対する中用量プレドニゾロンパルス療法。効果はあるが副作用で中止例あり |
| [26179196](https://pubmed.ncbi.nlm.nih.gov/26179196/) | 2015 | 追跡研究 | Dermatol Ther | 重症小児円形脱毛症に対する経口パルスと外用ステロイドの併用、長期追跡 |
| [32779249](https://pubmed.ncbi.nlm.nih.gov/32779249/) | 2020 | 後ろ向き研究 | J Eur Acad Dermatol Venereol | 慢性円形脱毛症におけるステロイド節約薬の継続率（138 例） |
| [30294905](https://pubmed.ncbi.nlm.nih.gov/30294905/) | 2019 | 機序研究 | J Cosmet Dermatol | 経口パルスステロイドの作用機序として TNF-α 値の変化を検討 |

## 日本市販情報

主な承認は以下のとおりです。

<!-- review:begin jp-lic-20261106-prednisolone-1 -->

> **確認による訂正（2026-11-06）**：元の記載は「現在、市販中の承認はなく、20 件すべてが取り消し済みです。主な承認は以下のとおりです。」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-prednisolone-1 -->

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 612450051 | プレドニゾロン錠 ５ｍｇ | 有効 |
| 620000125 | プレドニゾロン錠 ２．５ｍｇ | 有効 |
| 610454071 | プレドニゾロン散「タケダ」１％ | 有効 |
| 620620901 | リドメックスコーワ軟膏０．３％ | 有効 |
| 620615602 | プレドニゾロンクリーム０．５％「テイコク」 | 有効 |

データには承認の一部のみが含まれています。上表はそのうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用データは 100 件登録されています。主なものとして、アダリムマブ（Major）があります。このほか、ジドブジン、イソトレチノイン、アセタゾラミド、イブプロフェン、ニフェジピン、エチニルエストラジオール、アルデスロイキン、アレムツズマブなど（Moderate）、ホルモテロール、サルブタモール（Minor）が挙げられています。
- **ナレッジグラフ上の禁忌関連疾患**：高血圧、てんかん、高血糖、うっ血性心不全、麻疹、単純ヘルペスウイルス角膜炎、ポルフィリン症、下垂体機能低下症など。添付文書の記載ではなく、ナレッジグラフ由来の情報です。
- **文献上の懸念**：パルス療法では中止後の再発と、ステロイド全身投与に伴う副作用（小児では成長への影響を含む）が報告されています。

添付文書の警告・禁忌の詳細は取得できていないため、添付文書を参照してください。

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
円形脱毛症については、プラセボ対照のパルス療法 RCT 1 件とシステマティックレビューがあり、機序的にも自己免疫疾患への既存使用と整合します。一方で、試験規模は小さく、再発とステロイド毒性が課題です。

**進める場合に必要なもの：**
- 添付文書（PMDA）の警告・禁忌情報の取得と安全性スクリーニング
- 詳細な作用機序データ（DrugBank など）
- 再発予防と減量の方針、長期副作用（骨密度、血糖、血圧、感染症、小児の成長）のモニタリング計画
- JAK 阻害薬など代替治療との位置づけ整理
- 現行の供給・承認状況の確認

<!-- review:begin jp-lic-20261106-prednisolone-2 -->

> **確認による訂正（2026-11-06）**：元の記載は「日本では現在市販中の承認がないため、現行の供給・承認状況の確認」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-prednisolone-2 -->

## 参考：その他の予測候補

| 予測疾患 | スコア | エビデンスレベル | 決定 | 備考 |
|------|------|------|------|------|
| 粘液性脱毛症 (alopecia mucinosa) | 0.9999 | L5 | Hold | 症例報告のみで、シクロスポリンの使用例。プレドニゾロンの直接的根拠なし |
| 毛包炎性脱毛症 (folliculitis decalvans) | 0.9998 | L5 | Hold | 併用療法の症例報告 1 件のみ |
| 休止期脱毛 | 0.9998 | L5 | Hold | モデル予測のみ |
| 抗体欠損を伴う脱毛症 | 0.9998 | L5 | Hold | 間接的な症例報告のみ |
| 反復性皮膚水疱を伴う遺伝性乏毛症 | 0.9998 | L5 | Hold | モデル予測のみ |
| 脱毛・知的障害・高ゴナドトロピン性性腺機能低下症候群 | 0.9998 | L5 | Hold | モデル予測のみ |
| 丘疹性病変を伴う無毛症 | 0.9994 | L5 | Hold | モデル予測のみ |
| 涙腺脱出 | 0.9994 | L5 | Hold | モデル予測のみ |

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-06 | 削除：「現在、市販中の承認はなく、20 件すべてが取り消し済みです」 | 訂正 | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-06 | 削除：「日本では現在市販中の承認がないため」 | 訂正 | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Orapred Odt (prednisolone sodium phosphate) prescribing information, Advanz Pharma (US) Corp.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=1e379543-c4cf-4e72-953b-db15b7f0c2a1) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：スピラゾン、プレドニン、プレドネマ、リドメックス、リドメックスコーワ、水溶性プレドニン

**販売名（規格別）**：スピラゾンクリーム0.3%、スピラゾン軟膏0.3%、プレドニゾロン、プレドニゾロンクリーム0.5%、プレドニゾロン吉草酸エステル酢酸エステルクリーム0.3%TCK、プレドニゾロン吉草酸エステル酢酸エステルクリーム0.3%、プレドニゾロン吉草酸エステル酢酸エステル軟膏0.3%、プレドニゾロン散1%、プレドニゾロン軟膏0.5%、プレドニゾロン錠 1mg、プレドニゾロン錠 2.5mg、プレドニゾロン錠 5mg、プレドニゾロン錠1mg(旭化成)、プレドニゾロン錠1mg、プレドニゾロン錠2.5mg、プレドニゾロン錠5mg(旭化成)、プレドニゾロン錠5mg、プレドニン眼軟膏 0.25%、プレドニン錠5mg、プレドネマ注腸20mg、リドメックスコーワクリーム0.3%、リドメックスコーワ軟膏0.3%、水溶性プレドニン10mg、水溶性プレドニン20mg、水溶性プレドニン50mg
<!-- brand-names:end -->

