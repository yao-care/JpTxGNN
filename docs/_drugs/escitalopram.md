---
layout: default
title: Escitalopram
parent: 僅模型預測 (L5)
nav_order: 52
evidence_level: L5
indication_count: 10
---

# Escitalopram
{: .fs-9 }

證據等級: **L5** | 預測適應症: **10** 個
{: .fs-6 .fw-300 }

---

## 目錄
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist">

## 藥師評估報告

</div>

Using `txgnn-pipeline` skill noted — this is a report generation task. The skill confirms TxGNN evidence pack processing workflow. Proceeding to generate the full report.

---

> **レポート生成メモ**: `predicted_indications[0]`（Ohdo 症候群、TxGNN スコア 98.56%）と `predicted_indications[1]`（気分変調症、98.55%）のスコアは統計的に同等です。Ohdo 症候群はエビデンスレベル L5・Hold であり臨床報告皆無のため、最も直接的エビデンスを持つ**気分変調症（L1・Proceed with Guardrails）**を本レポートの主対象に選択します。

---

# エスシタロプラム：大うつ病性障害 から 気分変調症（Dysthymic Disorder）へ

## 一言要約

エスシタロプラムは選択的セロトニン再取り込み阻害薬（SSRI）であり、米国 FDA・欧州 EMA において大うつ病性障害および各種不安障害の治療薬として広く承認されています。
TxGNN モデルは**気分変調症（Dysthymic Disorder / 持続性抑うつ障害）** への有効性を予測しており、現在 **11 件の臨床試験**と **8 編の文献**がこの方向性を支持しています。
なお、日本（PMDA）における承認記録は現時点では確認されていません。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本未承認（海外適応：大うつ病性障害・全般性不安障害） |
| 予測新規適応症 | 気分変調症（Dysthymic Disorder） |
| TxGNN 予測スコア | 98.55% |
| エビデンスレベル | L1 |
| 日本市販状況 | ✗ 未上市 |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails |

---

## この予測が妥当である理由

現在、Evidence Pack に詳細な作用機序（MOA）データは収録されていません。既知の薬理学的情報によれば、エスシタロプラムはシタロプラムの活性 S 体エナンチオマーであり、セロトニン再取り込み輸送体（SERT）を高選択的に阻害します。この阻害によりシナプス間隙のセロトニン濃度が持続的に上昇し、前頭前皮質・扁桃体・辺縁系における感情・気分調節回路の機能正常化が図られます。

気分変調症（持続性抑うつ障害）は 2 年以上継続する慢性低強度抑うつ状態であり、大うつ病性障害と共通する神経生物学的基盤（セロトニン機能不全、前頭葉-辺縁系結合の異常）を有しています。エスシタロプラムが大うつ病性障害で発揮する SERT 阻害という薬理作用は、気分変調症の中核的な神経生物学的病態に直接対処できるため、機序的適用可能性は高いと判断されます。

注目すべきは、エスシタロプラムを対象とした気分変調症の直接的二重盲検プラセボ対照試験（NCT00220701）が完了しており、さらに sertraline との直接比較試験（NCT00234312）も実施済みである点です。複数の Meta-analysis（PMID 21527126）もこの方向性を支持しており、TxGNN モデルの予測妥当性を多角的に裏付けています。

---

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT00220701](https://clinicaltrials.gov/study/NCT00220701) | Phase 4 | 完了 | 36 | エスシタロプラム（最大 20 mg/日）vs プラセボの 12 週間二重盲検試験。気分変調症患者のうつ症状・心理社会機能・認知機能の改善を検討。目標疾病・薬物完全一致（Grade A）。 |
| [NCT00234312](https://clinicaltrials.gov/study/NCT00234312) | Phase 4 | 完了 | 40 | 気分変調症および二重抑うつ（double depression）に対するエスシタロプラム vs セルトラリンの有効性・安全性比較。目標疾病・薬物完全一致。 |
| [NCT00296712](https://clinicaltrials.gov/study/NCT00296712) | Phase 4 | 完了 | 55 | 初回治療としてのエスシタロプラム＋ブプロピオン二剤併用療法の検討。抑うつ症状の寛解率改善を評価。 |
| [NCT01189812](https://clinicaltrials.gov/study/NCT01189812) | Phase 2 | 完了 | 80 | シタロプラム＋リチウム vs シタロプラム＋プラセボの二重盲検 RCT。気分障害患者のうつ症状軽減を評価。薬物クラス一致。 |
| [NCT01973283](https://clinicaltrials.gov/study/NCT01973283) | Phase 4 | 完了 | 100 | 抑うつ症状を伴う高齢患者へのシタロプラム/デュロキセチン投与と「虚弱（frailty）」症候群の改善評価。族群・疾患カテゴリ相近。 |
| [NCT04437485](https://clinicaltrials.gov/study/NCT04437485) | Phase 2 | 完了 | 46 | 抑うつ＋糖尿病前症患者を対象とした eIMPACT-DM パイロット RCT。抑うつ治療と HbA1c・インスリン抵抗性への効果を評価。 |
| [NCT02458690](https://clinicaltrials.gov/study/NCT02458690) | Phase 2 | 完了 | 216 | 高齢抑うつ患者（CVD 既往なし）の心血管リスク低減を目指した eIMPACT 協働ケア RCT。薬物・疾患カテゴリ相近。 |
| [NCT01658228](https://clinicaltrials.gov/study/NCT01658228) | Phase 4 | 完了 | 86 | 軽度認知障害合併抑うつ症患者への抗うつ薬・認知機能改善薬の併用パイロット試験。エスシタロプラム使用を含む。 |
| [NCT00080158](https://clinicaltrials.gov/study/NCT00080158) | Phase 2/3 | 完了 | 120 | 自殺企図歴を持つ抑うつ青少年を対象とした 3 種治療比較試験。抑うつ疾患スペクトラム内の多面的介入検討。 |
| [NCT00404755](https://clinicaltrials.gov/study/NCT00404755) | Phase 4 | 完了 | 17 | 二分聴覚テスト（dichotic listening）を用いた抑うつ薬物治療反応予測バイオマーカー研究。薬物機序支持。 |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [21811192](https://pubmed.ncbi.nlm.nih.gov/21811192/) | 2010 | RCT | Int Clin Psychopharmacol | エスシタロプラム（最大 20 mg/日）vs プラセボの 12 週間 RCT（n=36）。気分変調症を直接対象とし、抑うつ・心理社会機能・認知機能の改善を検討。目標疾病・薬物完全一致。 |
| [21527126](https://pubmed.ncbi.nlm.nih.gov/21527126/) | 2011 | Meta-analysis | J Clin Psychiatry | 気分変調症に対する抗うつ薬のプラセボ対照 RCT のメタ解析。MDD との奏効率比較を実施。SSRI 含む抗うつ薬の気分変調症への有効性を体系的に評価。 |
| [29683474](https://pubmed.ncbi.nlm.nih.gov/29683474/) | 2018 | Meta-analysis | Cochrane Database Syst Rev | がん患者の抑うつ症状に対する抗うつ薬（SSRI 含む）の有効性・安全性を評価した Cochrane 系統的レビュー（2018 年版）。 |
| [26029972](https://pubmed.ncbi.nlm.nih.gov/26029972/) | 2015 | Meta-analysis | Cochrane Database Syst Rev | 上記 Cochrane レビューの 2015 年版。SSRI の抑うつ全般への有効性に関する体系的エビデンス。 |
| [25647343](https://pubmed.ncbi.nlm.nih.gov/25647343/) | 2015 | Cohort | Psychoneuroendocrinology | エスシタロプラム治療中の抑うつ患者における Th2 応答亢進・自然免疫調節因子の変化を探索。抗うつ薬の免疫-神経調節機序に関するデータを提供。 |
| [21448115](https://pubmed.ncbi.nlm.nih.gov/21448115/) | 2011 | Case series | Psychiatria Danubina | 気分変調症患者のエスシタロプラム・セルトラリン治療中に生じたアレルギー反応の症例報告。SSRI 長期使用時の安全性関連情報。 |
| [19820552](https://pubmed.ncbi.nlm.nih.gov/19820552/) | 2009 | Review | J Psychiatr Pract | 初期抗うつ薬二剤併用療法による寛解率改善の可能性を検討したレビュー。エスシタロプラムを含む治療戦略の比較考察。 |
| [23260337](https://pubmed.ncbi.nlm.nih.gov/23260337/) | 2013 | Case series | Gen Hosp Psychiatry | SSRI（主にエスシタロプラム・パロキセチン）による乳汁分泌不全（galactorrhea）の症例報告と 23 例のレビュー。副作用プロファイルの補足情報。 |

---

## 日本市販情報

PMDA（医薬品医療機器総合機構）データベースへの照会（2026-04-25）の結果、エスシタロプラムの国内承認記録は 0 件でした。本剤は米国（商品名：Lexapro）および欧州（商品名：Cipralex）では承認済みですが、現時点では日本において未承認薬です。

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
エスシタロプラムの気分変調症に対する有効性は、直接の二重盲検プラセボ対照 RCT（NCT00220701）と sertraline との直接比較試験（NCT00234312）、さらに複数の Meta-analysis（PMID 21527126）によって L1 レベルで支持されており、SERT 阻害という薬理学的機序的根拠も明確です。ただし日本国内（PMDA）での承認実績が皆無であり、安全性詳細情報の確認が不可欠です。

**進める場合に必要なもの：**
- PMDA 承認申請に向けた国内臨床試験データの設計・収集
- DrugBank API を通じた詳細 MOA データの取得（現在 Data Gap）
- 警告・禁忌・薬物相互作用を含む完全な安全性プロファイルの確認（TFDA 仿単/海外添付文書の解析）
- 日本人集団における薬物動態（CYP2C19 多型の影響含む）と有効性データの評価
- 既承認国（米国・欧州）の気分変調症関連規制上の前例調査
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

