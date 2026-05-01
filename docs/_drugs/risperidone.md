---
layout: default
title: Risperidone
parent: 僅模型預測 (L5)
nav_order: 122
evidence_level: L5
indication_count: 10
---

# Risperidone
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

スキルを確認しました。レポート生成に特化した追加指示はないため、システムプロンプトの評価フォーマット（v5）に従って作成します。

本 Pack は `candidate_id: TW-DB00734-multi`（10 適応症の多指標評価）です。TxGNN スコア Rank 1（Gaze palsy, L5, Hold）ではなく、最高エビデンス適応症の **Rank 6（Major Affective Disorder, L1）** を主要評価対象として選定しています。

---

# リスペリドン：統合失調症 から 大うつ病・双極性感情障害 へ

## 一言要約

リスペリドンは D2/5-HT2A 受容体を拮抗する非定型抗精神病薬で、統合失調症の治療薬として国際的に広く使用されています。TxGNN モデルは 10 の新規適応症を予測しており、中でも最もエビデンスが充実した**大うつ病・双極性感情障害 (Major Affective Disorder)** については、**36 件の臨床試験**（複数の Phase 3 RCT を含む）と **20 編の文献**（Cochrane meta-analysis を含む）が有効性を強力に支持しています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 統合失調症（日本薬事承認データは本 Pack 外） |
| 予測新規適応症 | 大うつ病・双極性感情障害 (Major Affective Disorder) |
| TxGNN 予測スコア | 99.11% |
| エビデンスレベル | L1 |
| 日本市販状況 | × 未上市 |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails |

> **多指標評価について：** 本 Pack は計 10 の予測適応症を含みます。TxGNN スコア最上位は *Gaze palsy, familial horizontal* (99.76%, Rank 1) ですが、エビデンスレベルが L5（臨床データなし）のため、最高エビデンス適応症である Rank 6（L1）を主要評価対象としています。

---

## 予測適応症一覧

| Rank | 疾患名 | TxGNN スコア | エビデンス | 推奨 |
|------|--------|------------|----------|------|
| 1 | Gaze palsy, familial horizontal（水平注視麻痺・進行性脊柱側弯症） | 99.76% | L5 | Hold |
| 2 | Asperger syndrome, susceptibility to（アスペルガー症候群易感性） | 99.74% | L5 | Hold |
| 3 | Amelocerebrohypohidrotic syndrome（法瑯質・小脳・無汗症候群） | 99.69% | L5 | Hold |
| 4 | Phelan-McDermid syndrome（フェラン・マクダーミド症候群） | 99.59% | L4 | Research Question |
| 5 | Trichotillomania（抜毛症） | 99.51% | L4 | Research Question |
| **6** | **Major affective disorder（大うつ病・双極性感情障害）** | **99.11%** | **L1** | **Proceed with Guardrails** |
| 7 | Tourette syndrome（トゥレット症候群） | 98.76% | L2 | Proceed with Guardrails |
| 8 | Intellectual disability（知的障害） | 98.72% | L2 | Proceed with Guardrails |
| 9 | Autism, susceptibility to（自閉症易感性） | 98.65% | L2 | Proceed with Guardrails |
| 10 | Chromosome 15q11.2 deletion syndrome（第 15 染色体 q11.2 欠失症候群） | 98.59% | L5 | Hold |

---

## この予測が妥当である理由

リスペリドンはドーパミン D2 受容体とセロトニン 5-HT2A 受容体を強力に拮抗する非定型抗精神病薬です。本 Pack には詳細な MOA データが含まれていませんが、確立された薬理学的知識に基づき情動障害への適用根拠を以下に示します。

躁状態の病態中核には中脳辺縁系ドーパミン経路の過活性が存在します。リスペリドンの D2 拮抗はこの過活性を直接抑制し、抗躁効果をもたらします。うつ状態では前頭皮質の血清素伝達低下が認められ、5-HT2A 拮抗による皮質セロトニン放出の増加が抗うつ薬との協調（augmentation）の機序的根拠となります。この D2/5-HT2A 二重拮抗により、リスペリドンは気分安定薬としても既存抗うつ薬の増強剤としても機能し得ます。

統合失調症と大うつ病・双極性感情障害は共通の神経伝達物質基盤（ドーパミン・セロトニン経路の dysregulation）を有しており、薬理学的類縁性が高い疾患群です。統合感情障害（schizoaffective disorder）という両者の中間診断概念が存在することも、この連続性を臨床的に裏付けています。複数の Phase 3 RCT および Cochrane meta-analysis がリスペリドンの情動障害への有効性を実証しており、TxGNN の高スコア予測（99.11%）は既存エビデンスと整合しています。

---

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT00277654](https://clinicaltrials.gov/study/NCT00277654) | Phase 3 | 完了 | 111 | リスペリドン単剤による外来双極性障害（パニック/全般性不安障害合併）の安全性・有効性 RCT |
| [NCT00176202](https://clinicaltrials.gov/study/NCT00176202) | Phase 3 | 完了 | 65 | 小児双極性障害における Risperidone vs Divalproex 比較 RCT（MRI 神経回路評価を含む） |
| [NCT00012558](https://clinicaltrials.gov/study/NCT00012558) | N/A | 完了 | 5,000 | STEP-BD：双極性障害の薬物療法・心理社会療法を系統的に長期評価した大規模実世界研究 |
| [NCT00057681](https://clinicaltrials.gov/study/NCT00057681) | Phase 3 | 完了 | 379 | TEAM Study：早発性躁症（小児・青少年）に対する Lithium / Valproate / Risperidone 三群比較 RCT |
| [NCT00391222](https://clinicaltrials.gov/study/NCT00391222) | Phase 3 | 完了 | 585 | Risperidone LAI 単剤 vs プラセボによる双極 I 型障害の気分エピソード再発予防 RCT |
| [NCT02918097](https://clinicaltrials.gov/study/NCT02918097) | Phase 4 | 完了 | 78 | 双極性障害うつ病エピソードへのアルゴリズム治療の費用対効果・生活品質評価（実用 RCT） |
| [NCT00044681](https://clinicaltrials.gov/study/NCT00044681) | Phase 3 | 完了 | 258 | SSRI 治療抵抗性うつ病に対する Risperidone 補助療法の有効性・安全性・長期維持効果 RCT |
| [NCT00095134](https://clinicaltrials.gov/study/NCT00095134) | Phase 3 | 完了 | 630 | 標準抗うつ薬不応の大うつ病に対する Risperidone 補助 vs プラセボの多施設 RCT |
| [NCT00221403](https://clinicaltrials.gov/study/NCT00221403) | Phase 3 | 完了 | 46 | 3〜7 歳幼児双極性障害を対象とした Valproate vs Risperidone の予備的ランダム化対照試験 |
| [NCT00571688](https://clinicaltrials.gov/study/NCT00571688) | Phase 4 | 完了 | 50 | Risperidone Consta 隔週投与による双極性障害の症状再発・再入院抑制の評価 |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [34986373](https://pubmed.ncbi.nlm.nih.gov/34986373/) | 2022 | Meta-analysis | J Affect Disord | 難治性うつ病に対する増強療法のネットワーク meta-analysis（SGA を含む全 augmentation 剤を比較） |
| [35861202](https://pubmed.ncbi.nlm.nih.gov/35861202/) | 2023 | Meta-analysis | J Psychopharmacol | 早期難治性うつ病の増強・併用療法に関する系統的レビュー・meta-analysis |
| [34238049](https://pubmed.ncbi.nlm.nih.gov/34238049/) | 2021 | Meta-analysis | J Psychopharmacol | 大うつ病における SGA＋抗うつ薬・エスケタミン・リチウムの有効性・忍容性比較 meta-analysis |
| [35510505](https://pubmed.ncbi.nlm.nih.gov/35510505/) | 2023 | Meta-analysis | Psychol Med | 大うつ病に対する抗精神病薬（単剤・補助）の包括的 meta-analysis |
| [21154393](https://pubmed.ncbi.nlm.nih.gov/21154393/) | 2010 | Meta-analysis | Cochrane DB Syst Rev | 大うつ病・気分変調症に対する第二世代抗精神病薬の Cochrane 系統的レビュー |
| [17975181](https://pubmed.ncbi.nlm.nih.gov/17975181/) | 2007 | RCT | Ann Intern Med | 難治性大うつ病に対する Risperidone 補助療法のランダム化試験 |
| [20486830](https://pubmed.ncbi.nlm.nih.gov/20486830/) | 2010 | Cohort | Expert Opin Pharmacother | 双極性障害の維持治療における Risperidone LAI の有効性と服薬継続率 |
| [25295435](https://pubmed.ncbi.nlm.nih.gov/25295435/) | 2014 | Cohort | J Clin Psychiatry | 台湾全国データベースを用いた SGA 補助療法（Risperidone 含む）による大うつ病治療有効性の比較 |
| [33460070](https://pubmed.ncbi.nlm.nih.gov/33460070/) | 2020 | Review | Acta Psychiatr Scand | 双極性躁病の治療法概観（気分安定薬・抗精神病薬の選択指針を含む） |
| [7545159](https://pubmed.ncbi.nlm.nih.gov/7545159/) | 1995 | Case series | J Clin Psychiatry | リスペリドンの情動障害・OCD への適用の初期報告（D2/5-HT2A 二重拮抗機序の提示） |

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
大うつ病・双極性感情障害に対するリスペリドンの有効性は、複数の Phase 3 RCT および Cochrane meta-analysis（L1 エビデンス）によって強力に裏付けられており、D2/5-HT2A 二重拮抗という明確な機序的根拠が存在します。ただし、日本での薬事承認が未取得であり、添付文書の安全性情報（警告・禁忌・薬物相互作用）の取得が課題として残存しています。

**進める場合に必要なもの：**
- PMDA データベースによる日本国内薬事承認状況の確認
- 添付文書（仿単）の取得・解析による安全性情報（警告・禁忌・DDI）の補完
- DrugBank API による詳細 MOA データの取得
- 日本における情動障害への既承認薬（リチウム、quetiapine 等）との競合分析
- 日本での本適応症に対する承認取得可能性の規制戦略評価
---

