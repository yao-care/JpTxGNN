---
layout: default
title: Aprepitant
parent: モデル予測のみ
nav_order: 28
evidence_level: L5
indication_count: 10
monitor_inn: "aprepitant"
predicted_indications: ["nephrogenic syndrome of inappropriate antidiuresis", "hypertrichosis (disease)", "pulmonary hypertension", "leprosy", "Ambras type hypertrichosis universalis congenita", "malformation syndrome with odontal and/or periodontal component", "kyphoscoliotic heart disease", "syndrome with a Dandy-Walker malformation as major feature", "subarachnoid hemorrhage (disease)", "isolated genetic hair shaft abnormality"]
last_modified_at: 2026-11-24
description: "Aprepitant：予測新適応症は腎性不適切抗利尿症候群 (nephrogenic syndrome of inappropriate antidiuresis)（エビデンスレベル L5）。既存適応症：制吐薬、抗うつ薬、統合失調症治療薬、NK1受容体拮抗薬"
---

# Aprepitant
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

## アプレピタント：制吐薬（NK1受容体拮抗薬）から腎性不適切抗利尿症候群へ
{: .text-alpha }

## 一言要約

アプレピタントは NK1 受容体拮抗薬で、元々は制吐薬として使用されていました。
TxGNN モデルは**腎性不適切抗利尿症候群 (nephrogenic syndrome of inappropriate antidiuresis, NSIAD)** に有効である可能性を予測していますが、現時点で関連する臨床試験・文献は**ありません**。エビデンスはモデル予測のみ（L5）です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 制吐薬、抗うつ薬、統合失調症治療薬、NK1受容体拮抗薬 |
| 予測新規適応症 | 腎性不適切抗利尿症候群 (nephrogenic syndrome of inappropriate antidiuresis) |
| TxGNN 予測スコア | 0.9997 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 6 件／全 12 件） |
| 承認番号数 | 12 件（有効 6 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Aprepitant の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「アプレピタントは、ヒトサブスタンスP/ニューロキニン1（NK 1 ）受容体の選択的かつ高親和性の拮抗薬である。アプレピタントはセロトニン（5-HT 3 ）受容体、ドパミン受容体および副腎皮質ステロイド受容体に対してほとんど、あるいは全く親和性を示さない。動物モデルにおいて、アプレピタントは中枢作用を介して、シスプラチンなどの細胞傷害性化学療法剤により誘発される嘔吐を抑制することが示されている。」英語原文："Aprepitant is a selective high-affinity antagonist of human substance P/neurokinin 1 (NK 1 ) receptors. Aprepitant has little or no affinity for serotonin (5-HT 3 ), dopamine, and corticosteroid receptors. Aprepitant has been shown in animal models to inhibit emesis induced by cytotoxic chemotherapeutic agents, such as cisplatin, via central actions."（[DailyMed: Cinvanti (aprepitant) prescribing information, Heron Therapeutics, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=4c218d3a-a508-4abc-9ed8-a6e8e191d1b4)、版 2026-04-01、参照日 2026-11-19）。既知の情報によると、アプレピタントは NK1 受容体拮抗薬であり、制吐薬として使われてきました。

NSIAD は V2 受容体の活性化変異によって起こる疾患です。サブスタンス P のシグナルとバソプレシン関連の水分バランスとの関連は推測の域を出ず、確立していません。モデル予測以外に直接的な機序上の根拠は見当たらないため、この予測の妥当性は限定的です。

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 622698301 | アプレピタントカプセルセット「サワイ」 | 有効 |
| 622695701 | アプレピタントカプセルセット「ＮＫ」 | 有効 |
| 621971101 | イメンドカプセルセット | 薬価削除（2026-03-31） |
| 622698101 | アプレピタントカプセル８０ｍｇ「サワイ」 | 有効 |
| 621970901 | イメンドカプセル８０ｍｇ | 薬価削除（2026-03-31） |

上表はデータ上の 12 件のうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **知識グラフ上の禁忌**：肝不全（添付文書の記載ではなく、知識グラフの薬物―疾患関係に基づく情報）
- **薬物相互作用**：100 件の相互作用が確認されています。主なものは次のとおりです。
  - **Major**：フェンタニル、アルフェンタニル、アカラブルチニブ
  - **Moderate**：パクリタキセル、アベマシクリブ、リドカイン、ニフェジピン、イブプロフェン、ヒドロコルチゾン、フルボキサミン、ゲフィチニブ など

添付文書の警告・禁忌については、添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測スコアは高いものの、臨床試験も文献もなく、機序上の裏付けも乏しいため、モデル予測のみの段階（L5）です。日本では販売されており（有効な承認と薬価基準から削除済みの承認があり、件数はクイック概要を参照）、現時点で開発を進める根拠は不足しています。

<!-- review:begin jp-lic-20261117-aprepitant-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「日本では販売されており（有効な承認12件/12件）、」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（621971101（廃止年月日 2026-03-31）、671971001（廃止年月日 2026-03-31）、671970901（廃止年月日 2026-03-31）、671971101（廃止年月日 2026-03-31）、621970901（廃止年月日 2026-03-31）、621971001（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-aprepitant-1 -->

**進める場合に必要なもの：**
- 詳細な作用機序データ（MOA）の取得
- 添付文書の警告・禁忌情報の取得と安全性スクリーニング
- NK1 経路と V2 受容体／バソプレシン系の関連を検討する前臨床・機序研究
- 他の予測候補（肺高血圧症、くも膜下出血など）との優先順位比較
- 日本での供給状況の確認

<!-- review:begin jp-lic-20261106-aprepitant-1 -->

> **確認による訂正（2026-11-06）**：元の記載は「日本での供給状況（承認取消）の確認」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。最新の件数はクイック概要と日本市販情報にあります。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-aprepitant-1 -->

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-06 | 削除：「承認取消」 | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-17 | 表：621971101 は有効ではなく薬価基準から削除済み | プログラム生成の承認情報表に置き換え（元の対応：訂正） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-17 | 表：621970901 は有効ではなく薬価基準から削除済み | プログラム生成の承認情報表に置き換え（元の対応：訂正） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Cinvanti (aprepitant) prescribing information, Heron Therapeutics, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=4c218d3a-a508-4abc-9ed8-a6e8e191d1b4) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：イメンド

**販売名（規格別）**：アプレピタントカプセル125mg、アプレピタントカプセル80mg、アプレピタントカプセルセット、イメンドカプセル125mg、イメンドカプセル80mg、イメンドカプセルセット
<!-- brand-names:end -->

