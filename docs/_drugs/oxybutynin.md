---
layout: default
title: Oxybutynin
parent: モデル予測のみ
nav_order: 231
evidence_level: L5
indication_count: 3
monitor_inn: "Oxybutynin"
predicted_indications: ["restless legs syndrome", "gastroduodenitis", "peptic ulcer disease"]
last_modified_at: 2026-11-24
description: "Oxybutynin：予測新適応症は下肢静止不能症候群 (Restless Legs Syndrome)（エビデンスレベル L5）。既存適応症：頻尿治療薬、過活動膀胱用薬、ムスカリン受容体拮抗薬"
---

# Oxybutynin
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

## オキシブチニン：過活動膀胱から下肢静止不能症候群（レストレスレッグス症候群）へ
{: .text-alpha }

## 一言要約

オキシブチニンはムスカリン受容体拮抗薬で、元々は頻尿・過活動膀胱の治療に使用されていました。
TxGNN モデルは**下肢静止不能症候群 (Restless Legs Syndrome)** に有効である可能性を高いスコアで予測しています。
ただし、この予測を支持する臨床試験・文献は**現時点でありません**。モデル予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 頻尿治療薬、過活動膀胱用薬、ムスカリン受容体拮抗薬 |
| 予測新規適応症 | 下肢静止不能症候群 (Restless Legs Syndrome) |
| TxGNN 予測スコア | 0.9974 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 9 件／全 12 件） |
| 承認番号数 | 12 件（有効 9 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Oxybutynin の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「オキシブチニンは膀胱平滑筋を弛緩させる。オキシブチニン塩酸塩は平滑筋に対して直接的な鎮痙作用を示し、平滑筋に対するアセチルコリンのムスカリン様作用を阻害する。骨格筋の神経筋接合部又は自律神経節における遮断作用（抗ニコチン作用）は認められない。」英語原文："Oxybutynin relaxes bladder smooth muscle. Oxybutynin chloride exerts a direct antispasmodic effect on smooth muscle and inhibits the muscarinic action of acetylcholine on smooth muscle. No blocking effects occur at skeletal neuromuscular junctions or autonomic ganglia (antinicotinic effects)."（[DailyMed: Oxybutynin Chloride Extended Release (oxybutynin chloride) prescribing information, PD-Rx Pharmaceuticals, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=b5653b7e-1e3b-4da3-b3a2-33318f448c67)、版 2026-11-11、参照日 2026-11-19）。既知の情報によると、オキシブチニンはムスカリン受容体拮抗薬に分類され、過活動膀胱や頻尿での使用実績があります。

一方、下肢静止不能症候群は、主にドパミン系の機能異常や鉄代謝の異常が関わる疾患とされています。オキシブチニンにはこれらの経路への作用が知られていません。そのため、既存適応症との機序的な関連性は確認できません。

TxGNN モデル（深層学習）のスコアは非常に高い（0.9974）ものの、このスコアは関連する疾患間でモデルが学習した類似性を反映している可能性があり、生物学的な根拠ではありません。裏付けとなる臨床・文献データがないため、現時点では**仮説段階**として扱うのが適切です。

## 日本市販情報

承認には有効なものと薬価基準から削除済みのものがあります（件数はクイック概要を参照）。主な承認は以下のとおりです。

<!-- review:begin jp-lic-20261117-oxybutynin-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「12 件の承認はすべて有効です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（622737100（廃止年月日 2026-03-31）、622736900（廃止年月日 2026-03-31）、622737000（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-oxybutynin-1 -->

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 620567705 | オキシブチニン塩酸塩錠３ｍｇ「サワイ」 | 有効 |
| 622737100 | オキシブチニン塩酸塩１ｍｇ錠 | 薬価削除（2026-03-31） |
| 672590050 | ポラキス錠１ １ｍｇ（選） | 有効 |
| 672590043 | ポラキス錠２ ２ｍｇ（選） | 有効 |
| 622736900 | オキシブチニン塩酸塩２ｍｇ錠 | 薬価削除（2026-03-31） |

上表はデータ上の 12 件のうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **知識グラフ上の禁忌関連疾患**（添付文書の記載ではなく、モデルの知識グラフに基づく参考情報）：
  - 眼・神経：閉塞隅角緑内障、重症筋無力症
  - 消化器：麻痺性イレウス、腸閉塞、中毒性巨大結腸、潰瘍性大腸炎・炎症性腸疾患、胃食道逆流症・食道炎、食道裂孔ヘルニア
  - 泌尿器：前立腺肥大症、膀胱頸部閉塞
  - 循環器：冠動脈疾患、心伝導障害、高血圧
  - 内分泌：甲状腺機能亢進症
  - 臓器障害：腎疾患、肝疾患、胆嚢疾患
- **薬物相互作用**（100 件を検出。主なもの）：
  - **重大 (Major)**：塩化カリウム、クエン酸カリウム
  - **中等度 (Moderate)**：他の抗コリン薬（アトロピン、ヒヨスチアミン、グリコピロニウム、ジシクロミン、トロスピウムなど）、モルヒネ、ロペラミド、メトクロプラミド、アプレピタント、エルクサドリン、プラムリンチド

添付文書の警告・禁忌については、別途確認してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
下肢静止不能症候群に対する臨床試験も文献もなく、エビデンスはモデル予測のみ (L5) です。さらに、オキシブチニンの作用機序はこの疾患の病態と結びつきません。現時点で開発を進める根拠はありません。

**進める場合に必要なもの：**
- 下肢静止不能症候群に対する抗ムスカリン作用の機序的根拠（前臨床研究など）
- 関連する臨床試験・文献の探索と評価
- 添付文書（PMDA）の警告・禁忌の取得と安全性スクリーニング
- 詳細な薬物作用機序データの補充

<!-- review:begin jp-lic-20261106-oxybutynin-1 -->

> **確認による訂正（2026-11-06）**：元の記載は「詳細な薬物作用機序データの補充／日本での承認が全て整理済みである点を踏まえた、供給・開発方針の確認」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。最新の件数はクイック概要と日本市販情報にあります。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-oxybutynin-1 -->

**参考：**
同じ薬物の他の予測候補には、より裏付けのあるものがあります。特に「低コンプライアンス膀胱」は、システマティックレビューや RCT が存在します。ただし、この候補は元の適応症（過活動膀胱）に近く、再利用の新規性は限定的です。

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-06 | 削除：「日本での承認が全て整理済みである点を踏まえた、供給・開発方針の確認」 | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Oxybutynin Chloride Extended Release (oxybutynin chloride) prescribing information, PD-Rx Pharmaceuticals, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=b5653b7e-1e3b-4da3-b3a2-33318f448c67) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：アポハイド、ネオキシ、ポラキス

**販売名（規格別）**：オキシブチニン塩酸塩1mg錠、オキシブチニン塩酸塩2mg錠、オキシブチニン塩酸塩3mg錠、オキシブチニン塩酸塩錠1mg、オキシブチニン塩酸塩錠2mg、オキシブチニン塩酸塩錠3mg、ポラキス錠1 1mg、ポラキス錠2 2mg、ポラキス錠3 3mg
<!-- brand-names:end -->

