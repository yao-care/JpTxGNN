---
layout: default
title: Haloperidol
parent: 僅模型預測 (L5)
nav_order: 69
evidence_level: L5
indication_count: 10
---

# Haloperidol
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

TxGNN パイプラインスキルを確認しました。これはレポート生成タスクです。Evidence Pack を分析してレポートを作成します。

---

**分析メモ：**
- `predicted_indications` は 10 件あり、TxGNN スコア最上位（rank 1）は「先天性糖基化障害」で **L5・Hold**（証拠ゼロ）
- **rank 10「双極性障害・躁状態」** が唯一 **L1・Proceed with Guardrails** であり、9 件の臨床試験（うち 3 件で Haloperidol が積極的対照として直接参加）と 20 編の文献を有する
- 本レポートは最もエビデンスが充実した適応症（rank 10）を主眼として作成する

---

# ハロペリドール：統合失調症 から 双極性障害（躁状態） へ

## 一言要約

ハロペリドール（Haloperidol）は代表的な定型抗精神病薬として、主に統合失調症の治療に国際的に広く使用されてきました。TxGNN モデルは 10 疾患への適応可能性を予測しており、そのうち **双極性障害の躁状態 (Manic Bipolar Affective Disorder)** が最もエビデンスの充実した候補です。現在 **9 件の臨床試験**（複数の Phase 3 RCT にてハロペリドールが積極的対照として直接参加）と **20 編の文献**（ネットワークメタ分析 2 編を含む）がこの方向性を支持しています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 統合失調症（国際的承認適応症；日本 PMDA データなし） |
| 予測新規適応症 | 双極性障害・躁状態 (Manic Bipolar Affective Disorder) |
| TxGNN 予測スコア | 99.83% |
| エビデンスレベル | L1 |
| 日本市販状況 | ✗ 未上市 |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails |

---

## この予測が妥当である理由

ハロペリドールは高力価の定型抗精神病薬であり、その主要な作用機序はドパミン D2 受容体への高親和性拮抗（Ki ≈ 1 nM）です。急性躁症発作では中脳辺縁系のドパミン伝達が過亢進しており、ハロペリドールはこの病態に直接介入することで気分の安定化と激越行動の制御を促します。なお、本 Evidence Pack における MOA の詳細データは現時点では未取得であるため（Data Gap）、上記は国際的に確立された薬理学的知見に基づいています。

統合失調症の陽性症状（幻覚・妄想）と双極性障害の躁症状（易刺激性・誇大性・思考奔逸）は、いずれもドパミン過剰活動という共通の神経生物学的基盤を持ちます。このため、D2 受容体拮抗作用を持つハロペリドールは機序的に両疾患に作用しうると考えられており、適応症間の薬理学的類似性は非常に高いといえます。

実際、本 Evidence Pack 内の複数の Phase 3 RCT（NCT00253162・NCT00129220・NCT00253149）ではハロペリドールが躁症治療試験の積極的対照薬として直接組み込まれています。また 2022 年発表のネットワークメタ分析（PMID: 34642461）は急性躁症に対する複数薬剤を系統的に比較しており、ハロペリドールを確立した治療選択肢として評価しています。日本人患者を対象とした Phase 3 RCT（PMID: 22134043）でも同様の位置づけが確認されています。

---

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT00253162](https://clinicaltrials.gov/study/NCT00253162) | Phase 3 | 完了 | 439 | Risperidone vs プラセボ vs **Haloperidol** の躁症治療比較（3 週・12 週）；Haloperidol が積極的対照として直接参加した大規模 RCT |
| [NCT00129220](https://clinicaltrials.gov/study/NCT00129220) | Phase 3 | 完了 | 224 | Olanzapine vs プラセボ vs **Haloperidol** の二重盲検 RCT；双極性 I 型の躁・混合発作への有効性確認 |
| [NCT00253149](https://clinicaltrials.gov/study/NCT00253149) | Phase 3 | 完了 | 158 | Risperidone vs プラセボ vs **Haloperidol** の add-on 療法比較；気分安定薬との併用における躁症治療データ |
| [NCT00097266](https://clinicaltrials.gov/study/NCT00097266) | Phase 3 | 完了 | 615 | Aripiprazole 単薬療法の急性躁症 12 週試験；同一疾患集団の最大規模背景データとして参照 |
| [NCT00126009](https://clinicaltrials.gov/study/NCT00126009) | Phase 2 | 完了 | 120 | Valproate + Amisulpride vs Valproate + **Haloperidol**（5〜15 mg/日）の 3 ヶ月比較；Haloperidol 用量・安全性データを提供 |
| [NCT04327843](https://clinicaltrials.gov/study/NCT04327843) | Phase 3 | 完了 | 22 | 慢性精神病（双極性含む）における LAI アドヒアランス改善プログラム（タンザニア）；低資源環境での実用データ |
| [NCT00767715](https://clinicaltrials.gov/study/NCT00767715) | Phase 4 | 早期終了 | 11 | Olanzapine vs 従来型抗精神病薬の急性躁症コスト効果比較（スウェーデン）；早期中断・小規模のため証拠品質は低 |
| [NCT06049953](https://clinicaltrials.gov/study/NCT06049953) | N/A | 募集中 | 200 | 産前抗精神病薬（Haloperidol 含む）暴露と乳幼児発育の観察研究；主に安全性情報を提供 |
| [NCT03541031](https://clinicaltrials.gov/study/NCT03541031) | N/A | 状態不明 | 120 | 微量栄養素補助療法の双極性障害に対する効果検討；Haloperidol との直接関連は低く疾病背景として参照 |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [34642461](https://pubmed.ncbi.nlm.nih.gov/34642461/) | 2022 | Meta-analysis | Molecular Psychiatry | 双極性躁症の薬理治療に関するネットワークメタ分析（RCT 系統的レビュー）；Haloperidol を急性躁症の確立的治療薬として評価 |
| [22161387](https://pubmed.ncbi.nlm.nih.gov/22161387/) | 2011 | Meta-analysis | Cochrane Database | Oxcarbazepine の双極性情動エピソードへの有効性 Cochrane レビュー；比較対象に Haloperidol データを含む |
| [22134043](https://pubmed.ncbi.nlm.nih.gov/22134043/) | 2012 | RCT | J Affective Disorders | **日本人**双極性 I 型患者への Olanzapine vs プラセボ vs **Haloperidol** 二重盲検 RCT；日本人集団での直接有効性・安全性データ |
| [3312180](https://pubmed.ncbi.nlm.nih.gov/3312180/) | 1987 | RCT | J Clinical Psychiatry | Clonazepam vs **Haloperidol** の急性躁症二重盲検比較；Haloperidol 群の直接効果・忍容性データ |
| [369472](https://pubmed.ncbi.nlm.nih.gov/369472/) | 1979 | RCT | Archives General Psychiatry | Lithium + **Haloperidol** vs プラセボ + **Haloperidol** の興奮性統合情動障害における二重盲検 5 週試験 |
| [22070611](https://pubmed.ncbi.nlm.nih.gov/22070611/) | 2012 | Review | CNS Neuroscience & Therapeutics | 難治性双極性障害の定義と治療；部分奏効患者への **Haloperidol** 追加戦略を明示的に推奨 |
| [33460070](https://pubmed.ncbi.nlm.nih.gov/33460070/) | 2020 | Review | Acta Psychiatrica Scandinavica | 躁症治療の根拠に基づく薬物選択の臨床指針；気分安定薬と抗精神病薬の組み合わせを網羅 |
| [36789916](https://pubmed.ncbi.nlm.nih.gov/36789916/) | 2023 | Review | BMJ Mental Health | 急性躁症と統合失調症における抗精神病薬用量換算の系統的比較；Haloperidol 用量等価データを含む |
| [10343182](https://pubmed.ncbi.nlm.nih.gov/10343182/) | 1999 | その他 | Neuropsychobiology | 双極性感情障害患者における Lithium と **Haloperidol** 治療の Gαs タンパク質レベルへの異なる作用（機序研究） |
| [39756485](https://pubmed.ncbi.nlm.nih.gov/39756485/) | 2025 | その他 | J Affective Disorders | 双極性躁症入院中における LAI 追加投与が再入院率に与える影響（後向き解析）；最新の実臨床データ |

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
ハロペリドールは複数の完了した Phase 3 RCT において双極性障害の躁状態に対して積極的対照薬として直接使用されており、2022 年のネットワークメタ分析でも急性躁症における確立的治療薬として位置づけられています。エビデンスレベルは L1 に相当し、薬理学的根拠も明確です。ただし日本 PMDA での承認記録がクエリで確認されておらず（0 件）、安全性情報も未取得であるため、これらのデータ補完を先行させる必要があります。

**進める場合に必要なもの：**
- **日本 PMDA 承認状況の再確認**（ハロペリドールは国際的に広く承認されており、0 件は収集エラーの可能性が高い）
- **添付文書からの安全性情報の取得**：警告・禁忌・重大な副作用（錐体外路症状、QTc 延長、悪性症候群）
- **DrugBank からの詳細 MOA データの補完**（現在 Data Gap）
- **躁症特異的な投与量・投与経路の検討**（急性期 vs 維持期で用量が異なる）
- **特定集団の安全性評価**：高齢者（認知症関連精神症状への使用制限）・妊婦（NCT06049953 の進行中データを参照）
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

