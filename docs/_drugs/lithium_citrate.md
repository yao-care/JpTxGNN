---
layout: default
title: Lithium Citrate
parent: モデル予測のみ
nav_order: 190
evidence_level: L5
indication_count: 1
monitor_inn: "Lithium citrate"
predicted_indications: ["Malan overgrowth syndrome"]
last_modified_at: 2026-11-24
description: "Lithium Citrate：予測新適応症はMalan 過成長症候群 (Malan overgrowth syndrome)（エビデンスレベル L5）。既存適応症：躁病および躁うつ病の躁状態"
---

# Lithium Citrate
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

## クエン酸リチウム：躁病・躁うつ病の躁状態から Malan 過成長症候群へ
{: .text-alpha }

## 一言要約

クエン酸リチウム（炭酸リチウムと同系統のリチウム製剤）は、元々**躁病および躁うつ病の躁状態**の治療に使われていました。
TxGNN モデルは **Malan 過成長症候群 (Malan overgrowth syndrome)** に有効である可能性を予測していますが、この疾患に関する臨床試験・文献は今回のデータにはなく、**モデル予測のみ**の段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 躁病および躁うつ病の躁状態 |
| 予測新規適応症 | Malan 過成長症候群 (Malan overgrowth syndrome) |
| TxGNN 予測スコア | 0.9907 |
| エビデンスレベル | L5 |
| 日本市販状況 | 本サイトのデータ（薬価基準収載医薬品マスター）に該当品目なし（国内の承認状況は未確認） |
| 承認番号数 | 0 件（有効 0 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Lithium Citrate の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「気分安定薬としてのリチウムの作用機序は不明である。」英語原文："The mechanism of action of lithium as a mood stabilizing agent is unknown."（[DailyMed: lithium prescribing information, REMEDYREPACK INC.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=be1346df-4a39-45e8-874b-e2a496847fd5)、版 2026-10-23、参照日 2026-11-19）。ただし、リチウムは一般に GSK-3 とイノシトールモノホスファターゼを阻害し、PI3K/AKT/mTOR シグナルにも影響することが知られています。これらの経路は過成長を伴う疾患と概念的に関連します。

Malan 症候群は NFIX 関連の疾患で、躁病とは病態が大きく異なります。両者の関連は機序面の推測にとどまり、臨床的な裏付けはありません。

その他の上位予測も同様にモデル予測のみです。

| 順位 | 予測疾患 | スコア | 備考 |
|------|---------|--------|------|

## 文献エビデンス

Malan 過成長症候群について、関連する文献は現在ありません。

参考として、予測順位 3 位（肥満）には文献が 1 編ありますが、治療効果ではなく薬物動態を扱ったものです。

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [8162665](https://pubmed.ncbi.nlm.nih.gov/8162665/) | 1994 | Cohort | Clin Pharmacol Ther | 肥満者と標準体重者でのリチウムの体内動態の比較（有効性の検討ではない） |

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 日本市販情報

<!-- licenses:begin -->

医薬品マスター（薬価基準収載品目、本レポートで使用したデータ）には本薬の成分を含む品目がありません。

<!-- licenses:end -->

本サイトのデータでは、日本でのクエン酸リチウムの承認は確認できません（炭酸リチウム製剤は別成分のため含めていません）。

## 安全性に関する考慮事項

- **知識グラフ上の禁忌関連疾患**（添付文書ではなくモデルの知識グラフ由来）：腎疾患、認知障害、甲状腺機能低下症（粘液水腫、先天性甲状腺機能低下症を含む）、乾癬、突然の心停止、心伝導障害、尿崩症（中枢性・神経下垂体性を含む）
- **薬物相互作用**：該当する情報は見つかりませんでした。

警告・禁忌の詳細は添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- 予測は TxGNN モデルのみに基づき（L5）、Malan 過成長症候群での臨床試験・文献がありません。
- 日本ではクエン酸リチウム製剤の薬価基準収載はなく（医薬品マスターに該当品目なし）、安全性の確認は不足しています。

<!-- review:begin jp-lic-20261117-lithium_citrate-1 -->

> **確認による訂正（2026-11-24）**：元の記載は「日本では販売中で、承認 4件のうち 4件が有効ですが、」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルには、クエン酸リチウムを成分とする品目はありません。以前本ページのデータに含まれていた炭酸リチウム製剤（リーマス錠２００、炭酸リチウム錠２００ｍｇ「フジナガ」「大正」など）は別成分（炭酸リチウム）のため、2026-11-24 にデータから除きました。薬価基準に収載されていないことは承認の有無を意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-lithium_citrate-1 -->

**進める場合に必要なもの：**
- 添付文書の警告・禁忌情報の入手と安全性評価
- 詳細な作用機序データ（MOA）の補充
- Malan 症候群に対する前臨床研究（GSK-3、PI3K/AKT/mTOR 経路）の調査
- 疾患モデルでの有効性確認
- 治療域が狭いため、血中濃度モニタリングを含む安全性計画の策定

<!-- review:begin jp-lic-20261106-lithium_citrate-1 -->

> **確認による訂正（2026-11-24）**：元の記載は「治療域が狭いため、血中濃度モニタリングを含む安全性計画の策定／日本での承認取消の理由の確認と、経路適合性（投与経路）の検討」でした。削除：承認が取り消されたという前提は、医薬品マスター（薬価基準収載品目）の情報からは確認できません（医薬品マスターにクエン酸リチウムを成分とする品目はなく、承認状況はこのデータでは確認できません；2026-11-24 確認）。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-lithium_citrate-1 -->

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-24 | 削除：「日本での承認取消の理由の確認と、経路適合性（投与経路）の検討」 | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-24 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: lithium prescribing information, REMEDYREPACK INC.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=be1346df-4a39-45e8-874b-e2a496847fd5) |
| 2026-11-24 | 訂正：上表の品目は炭酸リチウム製剤（「含めていません」ではない） | 確認を撤回（2026-11-24：本ページのデータから炭酸リチウム製剤（炭酸リチウムは別成分）を除いたため、元の記載「炭酸リチウム製剤は別成分のため含めていません」が正しくなりました；元の対応：訂正（2026-11-24 改訂、旧版は記録に保存）） | [医薬品マスター（全件ファイル y_ALL20261112.zip）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

