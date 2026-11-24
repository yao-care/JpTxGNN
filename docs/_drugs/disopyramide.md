---
layout: default
title: Disopyramide
parent: モデル予測のみ
nav_order: 96
evidence_level: L5
indication_count: 10
monitor_inn: "Disopyramide"
predicted_indications: ["Tourette syndrome", "attention deficit-hyperactivity disorder", "trichotillomania", "attention deficit hyperactivity disorder, inattentive type", "faciodigitogenital syndrome", "specific developmental disorder", "idiopathic neonatal atrial flutter", "chondromyxoid fibroma", "multifocal atrial tachycardia (disease)", "trigeminal nerve neoplasm"]
last_modified_at: 2026-11-24
description: "Disopyramide：予測新適応症はトゥレット症候群 (Tourette syndrome)（エビデンスレベル L5）。既存適応症：記載なし（日本の承認情報に適応症テキストが含まれていません）"
---

# Disopyramide
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

## ジソピラミド：既存適応症（登録データなし）からトゥレット症候群へ
{: .text-alpha }

## 一言要約

ジソピラミドはクラスIA群の抗不整脈薬（ナトリウムチャネル遮断薬で、抗コリン作用も持つ）です。日本では、今回まとめたデータ上で承認適応症の記載を確認できませんでした。
TxGNN モデルは**トゥレット症候群 (Tourette syndrome)** に有効である可能性を予測していますが、関連する臨床試験・文献は **0 件**で、モデル予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 記載なし（日本の承認情報に適応症テキストが含まれていません） |
| 予測新規適応症 | トゥレット症候群 (Tourette syndrome) |
| TxGNN 予測スコア | 0.9986 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 8 件／全 9 件） |
| 承認番号数 | 9 件（有効 8 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Disopyramide の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「Norpace（リン酸ジソピラミド）は1群抗不整脈薬（すなわち、プロカインアミド及びキニジンと類似）である。動物試験において、Norpaceは自動能が亢進した細胞における拡張期脱分極（第4相）の速度を低下させ、正常心筋細胞の立ち上がり速度（第0相）を低下させるとともに活動電位持続時間を延長させ、梗塞心筋と隣接する正常灌流心筋との間の不応期の不均一性を減少させ、α及びβアドレナリン受容体には影響を及ぼさない。」英語原文："Norpace (disopyramide phosphate) is a Type 1 antiarrhythmic drug (i.e., similar to procainamide and quinidine). In animal studies Norpace decreases the rate of diastolic depolarization (phase 4) in cells with augmented automaticity, decreases the upstroke velocity (phase 0) and increases the action potential duration of normal cardiac cells, decreases the disparity in refractoriness between infarcted and adjacent normally perfused myocardium, and has no effect on alpha- or beta-adrenergic receptors."（[DailyMed: Norpace (disopyramide phosphate) prescribing information, Pfizer Laboratories Div Pfizer Inc](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=e2aa1642-d262-4520-bc6a-9fd3ad795677)、版 2026-08-24、参照日 2026-11-19）。既知の情報によると、ジソピラミドはクラスIA群の抗不整脈薬で、ナトリウムチャネル遮断作用と抗コリン作用を持ちます。

一方、トゥレット症候群は線条体のドパミン系を中心とした神経回路の異常が関わる疾患です。ジソピラミドの薬理作用とこの回路との間に、確立した機序上の関連は見つかっていません。したがって、この予測スコアはTxGNNモデル(ディープラーニング)が出力したもので、関連する疾患間でモデルが学習した類似性を反映している可能性があり、生物学的な根拠ではありません。妥当性を裏付ける根拠は現時点でありません。

参考として、他の上位予測にも同様の傾向があります。注意欠如・多動症（ADHD）、抜毛症、顔面指趾性器症候群などは、いずれも機序上の関連が乏しい予測です。一方、**多源性心房頻拍**と**特発性新生児心房粗動**は抗不整脈薬の領域に属するため、機序的にはより自然です。ただし後者は、新生児への使用で安全性上の大きな懸念があります（陰性変力作用、催不整脈作用、抗コリン作用）。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

トゥレット症候群に関連する文献は現在ありません。

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 610463213 | リスモダンＲ錠１５０ｍｇ | 有効 |
| 610463214 | リスモダンカプセル５０ｍｇ | 有効 |
| 610463215 | リスモダンカプセル１００ｍｇ | 有効 |
| 620004782 | リスモダンＰ静注５０ｍｇ ５ｍＬ | 薬価削除（2026-03-31） |
| 620259505 | ジソピラミド徐放錠１５０ｍｇ「ＶＴＲＳ」 | 有効 |

上表はデータ上の 9 件のうち 5 件です。

<!-- licenses:end -->

承認には有効なものと薬価基準から削除済みのものがあります（件数はクイック概要を参照）。上記は主要な 5 件です。

<!-- review:begin jp-lic-20261117-disopyramide-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「9 件すべてが有効な承認です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（620004782（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-disopyramide-1 -->

## 安全性に関する考慮事項

- **知識グラフ上の禁忌関連疾患**（添付文書の記載ではなく、TxGNN の知識グラフに基づく）：
  - 心血管系：QT延長症候群（家族性を含む）、房室ブロック、心筋症（肥大型を含む）、心筋炎、心内膜心筋線維症、心房細動、心房粗動、低血圧
  - 抗コリン作用に関連：閉塞隅角緑内障、前立腺肥大症、重症筋無力症（神経筋接合部疾患を含む）
  - 代謝・臓器障害：低血糖、低カリウム血症、腎疾患、肝疾患、胆嚢疾患、尿管膿瘍
- **薬物相互作用**：100 件の相互作用が登録されています。主な重大（Major）なものは以下のとおりです。
  - クラリスロマイシン
  - クエン酸カリウム
  - ピコスルファート
- 中等度（Moderate）の相互作用には、以下が含まれます。
  - 抗コリン薬（アトロピン、ヒヨスチアミン、グリコピロニウム、クリジニウム）
  - 副腎皮質ステロイド（ヒドロコルチゾン、デキサメタゾン、ベタメタゾン、トリアムシノロン、ブデソニド）
  - アムホテリシンB
  - ロペラミド
  - アプレピタント
  - ファモチジン
  - クロルプロパミド
- シメチジンとの相互作用は軽度（Minor）です。

添付文書の警告・禁忌の情報は今回のデータに含まれていないため、実際の使用判断では添付文書を必ず参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
- トゥレット症候群に対する臨床試験・文献がなく、機序的な関連も確認できないため、予測はモデル出力のみ（L5）です。
- 日本では有効な承認がありますが（件数はクイック概要を参照）、添付文書上の安全性情報は未取得のため、安全性評価に進めません。

<!-- review:begin jp-lic-20261117-disopyramide-2 -->

> **確認による訂正（2026-11-17）**：元の記載は「日本では 9 件の承認がすべて有効ですが、」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（620004782（廃止年月日 2026-03-31））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-disopyramide-2 -->

**進める場合に必要なもの：**
- PMDA の添付文書（警告・禁忌・適応症）の取得と解析
- DrugBank からの作用機序（MOA）データの取得
- トゥレット症候群との機序的関連を示す前臨床または臨床の根拠
- 予測上位のうち、抗不整脈薬の領域に近い多源性心房頻拍については、直接的な文献の追加調査（現在の文献は他の抗不整脈薬の間接的な症例報告のみ）

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-17 | 表：620004782 は有効ではなく薬価基準から削除済み | プログラム生成の承認情報表に置き換え（元の対応：訂正） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Norpace (disopyramide phosphate) prescribing information, Pfizer Laboratories Div Pfizer Inc](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=e2aa1642-d262-4520-bc6a-9fd3ad795677) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：リスモダン、リスモダンR

**販売名（規格別）**：ジソピラミドリン酸塩徐放錠150mg、ジソピラミド徐放錠150mg、リスモダンP静注50mg 5mL、リスモダンR錠150mg、リスモダンカプセル100mg、リスモダンカプセル50mg、リン酸ジソピラミド150mg徐放錠
<!-- brand-names:end -->

