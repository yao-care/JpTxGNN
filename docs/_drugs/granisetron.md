---
layout: default
title: Granisetron
parent: モデル予測のみ
nav_order: 153
evidence_level: L5
indication_count: 10
monitor_inn: "Granisetron"
predicted_indications: ["manic bipolar affective disorder", "Tourette syndrome", "acute contagious conjunctivitis", "angioedema", "allergic urticaria", "nephrogenic syndrome of inappropriate antidiuresis", "trichotillomania", "bronchitis", "cold urticaria", "conjunctivitis"]
last_modified_at: 2026-11-24
description: "Granisetron：予測新適応症は躁病性双極性感情障害 (manic bipolar affective disorder)（エビデンスレベル L5）。既存適応症：承認書のデータに記載なし"
---

# Granisetron
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

## グラニセトロン：既存適応症（記載なし）から躁病性双極性感情障害へ
{: .text-alpha }

## 一言要約

TxGNN モデルは**躁病性双極性感情障害 (manic bipolar affective disorder)** に有効である可能性を予測していますが、臨床試験・文献はいずれも **0 件**で、モデル予測のみの段階です。

<!-- review:begin jp-lic-20261106-granisetron-1 -->

> **確認による訂正（2026-11-06）**：元の記載は「グラニセトロンは選択的 5-HT3 受容体拮抗薬で、日本では注射剤・錠剤・内服ゼリーとして承認されていましたが、現在は 20 件すべての承認が整理（取消）済みです。／TxGNN モデルは**躁病性双極性感情障害 (manic bipolar affective disorder)** に有効である可能性を予測していますが、臨床試験・文献はいずれも **0 件**で、モデル予測のみの段階です。」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-granisetron-1 -->

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 承認書のデータに記載なし |
| 予測新規適応症 | 躁病性双極性感情障害 (manic bipolar affective disorder) |
| TxGNN 予測スコア | 0.9962 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 17 件以上） |
| 承認番号数 | 20 件以上 |
| 推奨決定 | Hold |

## この予測が妥当である理由

米国 FDA が承認した Granisetron の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「グラニセトロンは選択的5-ヒドロキシトリプタミン3（5-HT 3 ）受容体拮抗薬であり、5-HT 1、5-HT 1A、5-HT 1B/C、5-HT 2を含む他のセロトニン受容体、α 1-、α 2-又はβ-アドレナリン受容体、ドパミンD 2受容体、あるいはヒスタミンH 1受容体、ベンゾジアゼピン受容体、ピクロトキシン受容体又はオピオイド受容体に対してはほとんど又は全く親和性を示さない。5-HT 3型のセロトニン受容体は、末梢では迷走神経終末に、中枢では最後野の化学受容器引き金帯に存在する。」英語原文："Granisetron is a selective 5-hydroxytryptamine 3 (5-HT 3 ) receptor antagonist with little or no affinity for other serotonin receptors, including 5-HT 1, 5-HT 1A, 5-HT 1B/C, 5-HT 2; for alpha 1-, alpha 2-, or beta-adrenoreceptors; for dopamine-D 2; or for histamine-H 1; benzodiazepine; picrotoxin or opioid receptors. Serotonin receptors of the 5-HT 3 type are located peripherally on vagal nerve terminals and centrally in the chemoreceptor trigger zone of the area postrema."（[DailyMed: Sustol (granisetron) prescribing information, Heron Therapeutics, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=f7c7ffdd-8270-4030-bc1e-a1cb28a6de56)、版 2026-04-30、参照日 2026-11-19）。既知の情報によると、グラニセトロンは選択的 5-HT3 受容体拮抗薬です。

5-HT3 の調節がセロトニン系・ドパミン系のシグナルを介して気分調節に影響する、という仮説はあります。ただし、これは推測の域を出ません。臨床試験も文献もなく、根拠は TxGNN の予測だけです。既存適応症との類似性の評価も未実施です。

### 他の予測候補（参考）

上位 10 件の予測はいずれもエビデンスレベル L5、推奨は Hold です。

| 順位 | 予測疾患 | スコア | 機序的な見立て |
|------|---------|--------|----------------|
| 2 | トゥレット症候群 | 0.9952 | 基底核のドパミン調節への間接的影響という仮説はあるが、裏付けなし |
| 3 | 急性伝染性結膜炎 | 0.9949 | 病原体感染が原因で、機序的根拠は見当たらない |
| 4 | 血管性浮腫 | 0.9936 | セロトニンによる血管透過性への関与は理論上あるが間接的 |
| 5 | アレルギー性蕁麻疹 | 0.9932 | かゆみ伝達・肥満細胞との関連は弱い理論的link |
| 6 | 腎性抗利尿ホルモン不適合分泌症候群 | 0.9932 | AVPR2 機能獲得変異が原因で、機序的根拠は見当たらない |
| 7 | 抜毛症 | 0.9923 | 強迫スペクトラム障害との関連は推測的 |
| 8 | 気管支炎 | 0.9918 | 迷走神経求心路を介した咳反射への影響は理論上あるが間接的 |
| 9 | 寒冷蕁麻疹 | 0.9910 | 肥満細胞の脱顆粒との関連は弱い理論的link |
| 10 | 結膜炎 | 0.9909 | 機序的根拠は見当たらない |

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 610421323 | カイトリル錠２ｍｇ | 有効 |
| 620002573 | カイトリル注１ｍｇ １ｍＬ | 有効 |
| 620005666 | グラニセトロン静注液３ｍｇ「Ｆ」 ３ｍＬ | 有効 |
| 620005670 | グラニセトロン静注液３ｍｇ「トーワ」 ３ｍＬ | 有効 |
| 620008012 | グラニセトロン内服ゼリー２ｍｇ「ケミファ」 | 有効 |

データには承認の一部のみが含まれています。上表はそのうち 5 件です。

<!-- licenses:end -->

## 安全性に関する考慮事項

- **TxGNN モデル（ディープラーニング）が学習した関連疾患（添付文書ではなく、モデル上の関連情報）**：QT 延長症候群、家族性 QT 延長症候群、カリウム欠乏症、心突然死、心伝導障害
- **薬物相互作用**（100 件を検出、主なものを抜粋）：
  - **Major**：フェンタニル、デキストロメトルファン、トラマドール、アルフェンタニル、アルモトリプタン、スマトリプタン、アミオダロン、アミスルプリド、アミトリプチリン、アナグレリド
  - **Moderate**：アバメタピル（外用）、アビラテロン、ジヒドロコデイン、コデイン、ファモチジン、ホルモテロール、アデノシン、サルブタモール、アルフゾシン、プロポフォール

QT 延長リスクに関わる薬剤（アミオダロン、アミスルプリド、アミトリプチリンなど）や、セロトニン作用のある薬剤（トラマドール、トリプタン類など）との併用には特に注意が必要です。警告・禁忌の詳細については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
予測はモデルのスコアのみに基づき、臨床試験・文献・機序データがすべてありません。現時点で次の段階に進める根拠はありません。

<!-- review:begin jp-lic-20261106-granisetron-2 -->

> **確認による訂正（2026-11-06）**：元の記載は「また、日本の承認は全件が取消済みで、添付文書の警告・禁忌も確認できていません。現時点で次の段階に進める根拠はありません。」でした。削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（2026-11-06）。出典：[医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/)。

<!-- review:end jp-lic-20261106-granisetron-2 -->

**進める場合に必要なもの：**
- 添付文書の警告・禁忌情報の取得（PMDA）
- 詳細な作用機序データ（DrugBank）
- 躁病性双極性感情障害に関する前臨床・臨床の文献調査と臨床試験の検索
- QT 延長リスクを含む安全性評価と、精神科領域の併用薬との相互作用の確認
- 既存適応症と予測適応症の類似性評価、および投与経路の適合性評価

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-06 | 削除：「グラニセトロンは選択的 5-HT3 受容体拮抗薬で、日本では注射剤・錠剤・内服ゼリーとして承認されていましたが、現在は 20 件すべての承認が整理（取消）済みです」 | 訂正 | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-06 | 削除：「また、日本の承認は全件が取消済みで、添付文書の警告・禁忌も確認できていません」 | 訂正 | [医薬品マスター ダウンロードページ](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[医薬品医療機器総合機構（PMDA）](https://www.pmda.go.jp/) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Sustol (granisetron) prescribing information, Heron Therapeutics, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=f7c7ffdd-8270-4030-bc1e-a1cb28a6de56) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：カイトリル

**販売名（規格別）**：カイトリル注1mg 1mL、カイトリル注3mg 3mL、カイトリル点滴静注バッグ3mg/100mL、カイトリル細粒0.4% 2mg、カイトリル錠1mg、カイトリル錠2mg、グラニセトロン内服ゼリー1mg、グラニセトロン内服ゼリー2mg、グラニセトロン塩酸塩1mg1mL注射液、グラニセトロン塩酸塩3mg100mLキット、グラニセトロン塩酸塩3mg3mL注射液、グラニセトロン点滴静注バッグ1mg/50mL、グラニセトロン点滴静注バッグ1mg 50mL、グラニセトロン点滴静注バッグ3mg/100mL、グラニセトロン点滴静注バッグ3mg/50mL、グラニセトロン点滴静注液3mgバッグ 100mL、グラニセトロン静注液1mg 1mL、グラニセトロン静注液1mgシリンジ 1mL、グラニセトロン静注液3mg 3mL、グラニセトロン静注液3mgシリンジ 3mL
<!-- brand-names:end -->

