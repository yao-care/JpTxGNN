---
layout: default
title: Diphenhydramine
parent: モデル予測のみ
nav_order: 95
evidence_level: L5
indication_count: 1
last_modified_at: 2026-11-24
description: "Diphenhydramine：予測新適応症は酒さ性結膜炎 (Rosacea Conjunctivitis)（エビデンスレベル L5）。既存適応症：アレルギー性鼻炎（抗アレルギー薬、H1 受容体拮抗薬）"
monitor_inn: "Diphenhydramine"
predicted_indications: ["rosacea conjunctivitis"]
---

# Diphenhydramine
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

## ジフェンヒドラミン：アレルギー性鼻炎から酒さ性結膜炎へ
{: .text-alpha }

## 一言要約

ジフェンヒドラミンは第一世代の H1 受容体拮抗薬で、元々アレルギー性鼻炎などの抗アレルギー目的で使用されていました。
TxGNN モデルは**酒さ性結膜炎 (Rosacea Conjunctivitis)** に有効である可能性を予測していますが、
現在、関連する臨床試験や文献は見つかっておらず、モデル予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | アレルギー性鼻炎（抗アレルギー薬、H1 受容体拮抗薬） |
| 予測新規適応症 | 酒さ性結膜炎 (Rosacea Conjunctivitis) |
| TxGNN 予測スコア | 0.9920 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 7 件／全 8 件） |
| 承認番号数 | 8 件（有効 7 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Diphenhydramine の添付文書（Prescribing Information）の「Clinical Pharmacology」の項によると（非公式訳）、「ジフェンヒドラミン塩酸塩は、抗コリン作用（乾燥作用）及び鎮静作用の副作用を有する抗ヒスタミン薬である。抗ヒスタミン薬は、効果器細胞上の細胞受容体部位においてヒスタミンと競合すると考えられる。注射剤のジフェンヒドラミン塩酸塩は作用発現が速い。」英語原文："Diphenhydramine hydrochloride is an antihistamine with anticholinergic (drying) and sedative side effects. Antihistamines appear to compete with histamine for cell receptor sites on effector cells. Diphenhydramine hydrochloride in the injectable form has a rapid onset of action."（[DailyMed: diphenhydramine hydrochloride prescribing information, Henry Schein, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=af972e71-62ab-40c6-925a-cbcb4d6720a4)、版 2026-10-28、参照日 2026-11-19）。既知の情報によると、ジフェンヒドラミンは第一世代の H1 受容体拮抗薬で、アレルギー性鼻炎での使用実績があります。ヒスタミンが関与する目のかゆみや充血を和らげる可能性があるため、眼の症状には一定の適用可能性があります。

ただし、酒さ性結膜炎（眼型酒さ）の主な原因は、マイボーム腺機能不全、自然免疫の活性化、炎症です。ヒスタミン経路との関連は間接的にとどまります。今回の予測は TxGNN のスコア（0.992）に基づくもので、臨床的・文献的な裏付けはありません。

## 日本市販情報

現在、有効な承認と薬価基準から削除済みの承認があり（件数はクイック概要を参照）、国内で販売されています。

<!-- review:begin jp-lic-20261117-diphenhydramine-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「現在、8件の承認のうち8件が有効で、国内で販売されています。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（620008671（廃止年月日 2026-09-30、後継コード 611410185））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-diphenhydramine-1 -->

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 620931001 | ジフェンヒドラミン塩酸塩注３０ｍｇ「日新」 １．５％２ｍＬ | 有効 |
| 620930901 | ジフェンヒドラミン塩酸塩注１０ｍｇ「日新」 １％１ｍＬ | 有効 |
| 662640138 | ジフェンヒドラミン ５ｇ | 有効 |
| 620008772 | レスタミンコーワ錠１０ｍｇ | 有効 |
| 620008671 | ネオレスタミンコーワ散１％ | 薬価削除（2026-09-30、後継コード 611410185） |

上表はデータ上の 8 件のうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用は合計 100 件が確認されています。主なものは次のとおりです。
  - 重大（Major）：カリウムクエン酸塩、エリグルスタット
  - 中等度（Moderate）：抗コリン作用を持つ薬剤（ヒヨスチアミン、アトロピン、グリコピロニウム、ジシクロミン など）、オピオイド（モルヒネ）、ロペラミド、ブプロピオン、メトクロプラミド、ドロナビノール など

  抗コリン作用や中枢抑制作用の重複に注意が必要です。

警告・禁忌については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測は TxGNN のモデルスコアのみに基づき、臨床試験も文献もありません（L5）。酒さ性結膜炎の病態と H1 拮抗作用の関連も間接的です。

<!-- review:begin jp-lic-20261106-diphenhydramine-1 -->

> **確認による訂正（2026-11-06）**：元の記載は「酒さ性結膜炎の病態と H1 拮抗作用の関連も間接的です。さらに、日本では現在有効な承認がありません。」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。最新の件数はクイック概要と日本市販情報にあります。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-diphenhydramine-1 -->

**進める場合に必要なもの：**
- 添付文書の警告・禁忌情報の取得（PMDA の添付文書の確認）
- 詳細な作用機序データ（MOA）の補充（DrugBank など）
- 酒さ性結膜炎に対する前臨床研究や臨床研究の文献調査
- 眼科用剤形の実現可能性の検討（投与経路の適合性）

<!-- review:begin jp-lic-20261106-diphenhydramine-2 -->

> **確認による訂正（2026-11-06）**：元の記載は「眼科用剤形の実現可能性の検討（投与経路の適合性）／現在有効な承認がないことを踏まえた、開発・導入方針の整理」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。最新の件数はクイック概要と日本市販情報にあります。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-diphenhydramine-2 -->

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-06 | 削除：「さらに、日本では現在有効な承認がありません」 | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-06 | 削除：「現在有効な承認がないことを踏まえた、開発・導入方針の整理」 | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: diphenhydramine hydrochloride prescribing information, Henry Schein, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=af972e71-62ab-40c6-925a-cbcb4d6720a4) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：レスタミン、レスタミンコーワ

**販売名（規格別）**：ジフェンヒドラミン 5g、ジフェンヒドラミン塩酸塩注10mg 1%1mL、ジフェンヒドラミン塩酸塩注30mg 1.5%2mL、レスタミンコーワクリーム1%、レスタミンコーワ錠10mg

**配合剤（この成分を含む）**：強力レスタミンコーチゾンコーワ軟膏
<!-- brand-names:end -->

