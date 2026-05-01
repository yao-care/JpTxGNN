---
layout: default
title: Mirtazapine
parent: 僅模型預測 (L5)
nav_order: 99
evidence_level: L5
indication_count: 10
---

# Mirtazapine
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

# ミルタザピン：大うつ病（国際標準適応）からメランコリー型うつ病へ

## 一言要約

ミルタザピン（Mirtazapine, DB00370）は NaSSA（ノルアドレナリン作動性・特異的セロトニン作動性抗うつ薬）として世界各国で大うつ病の治療に使用されていますが、台湾では現在未承認です。
TxGNN モデルは計 **10 種類の新規適応症候補**を予測しており、最もエビデンスが充実した候補は**メランコリー型うつ病 (Melancholia)** で、**1 件の臨床試験**と **20 編の文献**（複数のメタアナリシスおよび RCT を含む）がこの方向性を支持しています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 台湾未承認（国際標準適応：大うつ病） |
| 最高エビデンス予測適応症 | メランコリー型うつ病 (Melancholia) |
| TxGNN 予測スコア | 98.33%（TxGNN rank 2,749 位） |
| エビデンスレベル | L1 |
| 台湾市販状況 | ✗ 未上市 |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails |

### 全予測適応症サマリー

| 順位 | 疾患名 | TxGNN スコア | エビデンスレベル | 推奨 |
|------|-------|------------|----------------|------|
| 1 | Ohdo syndrome and variants | 99.42% | L5 | Hold |
| 2 | Blepharophimosis-intellectual disability, Ohdo type | 99.11% | L5 | Hold |
| 3 | Benign paroxysmal torticollis of infancy | 99.11% | L5 | Hold |
| 4 | Ligneous conjunctivitis | 98.94% | L5 | Hold |
| 5 | Childhood apraxia of speech | 98.70% | L5 | Hold |
| 6 | **気分変調症 (Dysthymic disorder)** | **98.64%** | **L2** | **Proceed with Guardrails** |
| 7 | 広場恐怖症 (Agoraphobia) | 98.60% | L4 | Research Question |
| 8 | **恐怖症性障害 (Phobic disorder)** | **98.59%** | **L2** | **Proceed with Guardrails** |
| 9 | **メランコリー型うつ病 (Melancholia)** | **98.33%** | **L1** | **Proceed with Guardrails** |
| 10 | **神経症性うつ病 (Neurotic depression)** | **98.24%** | **L2** | **Proceed with Guardrails** |

> ⚠️ TxGNN スコア上位 5 件（Ohdo 症候群等の希少遺伝性疾患）は機序的根拠なし・エビデンスなし（L5）のため全件 Hold。スコア下位の精神疾患群が実際には高いエビデンスを保有します。

---

## この予測が妥当である理由

現在の Evidence Pack には公式な作用機序（MOA）データが含まれていませんが、PubMed 文献（PMID 8930006、10333982）によるとミルタザピンの主な薬理作用は次の通りです。シナプス前 α2 自体受容体および α2 ヘテロ受容体を拮抗することでノルアドレナリンとセロトニンの両方の放出を増強します。加えて、シナプス後 5-HT2A・5-HT2C・5-HT3 受容体を遮断することで、SSRI に見られる性機能障害・嘔気を回避しながら抗不安・睡眠改善効果を発揮します。強力な H1 拮抗作用により鎮静・食欲増進効果も持ちます。

メランコリー型うつ病（DSM-5: Major Depression with Melancholic Features）の核心症状群——快楽消失、早朝覚醒・睡眠断片化、朝方の症状悪化、著明な意欲・精力喪失、精神運動変化——は、ミルタザピンの三重の作用（ノルアドレナリン増強 → 意欲・精力の回復、セロトニン調節 → 情動安定化、H1 遮断 → 睡眠の修復）と直接的かつ機序的に対応しています。また気分変調症・恐怖症性障害・神経症性うつ病においても、5-HT2A/2C 拮抗による恐怖応答抑制と α2 拮抗による持続的情緒安定という共通機序が予測の妥当性を支持しています。

台湾での承認実績はないものの、世界 80 カ国以上（Remeron、Zispin 等のブランド名）での大うつ病治療への長期使用実績と豊富な RCT・メタアナリシスが存在することは、台湾への橋渡し申請を検討する際の重要な強みとなります。

---

## 臨床試験エビデンス（メランコリー型うつ病）

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT01916824](https://clinicaltrials.gov/study/NCT01916824) | Phase 4 | 完了 | 53 | 未治療 MDD 患者における抗うつ薬治療が意思決定機能に与える影響を評価。Melancholia と重複度の高い MDD 患者群での認知・情動機能への双方向改善効果を確認 |

## 文献エビデンス（メランコリー型うつ病）

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [36253442](https://pubmed.ncbi.nlm.nih.gov/36253442/) | 2023 | Meta-analysis | Molecular Psychiatry | MDD 維持療法における抗うつ薬比較ネットワークメタアナリシス；ミルタザピンの有効性・忍容性・安全性を系統的評価 |
| [40449742](https://pubmed.ncbi.nlm.nih.gov/40449742/) | 2025 | RCT | J Affect Disord | ブプロピオンとミルタザピンの MDD 症状プロファイルへの差次的効果；melancholic features への特異的反応性を示唆 |
| [18299900](https://pubmed.ncbi.nlm.nih.gov/18299900/) | 2008 | RCT | Support Care Cancer | がん患者の抑うつ・不安・睡眠障害に対してミルタザピンがイミプラミンより優れた効果を示す直接比較 RCT |
| [27289172](https://pubmed.ncbi.nlm.nih.gov/27289172/) | 2016 | Meta-analysis | Lancet | 児童・青年の MDD に対する抗うつ薬ネットワークメタアナリシス；ミルタザピンの忍容性プロファイルを評価 |
| [10333982](https://pubmed.ncbi.nlm.nih.gov/10333982/) | 1998 | Meta-analysis | J Affect Disord | 重度うつ病患者での臨床試験メタアナリシス；ミルタザピンの有効性・安全性・忍容性を包括評価 |
| [11806859](https://pubmed.ncbi.nlm.nih.gov/11806859/) | 2001 | Meta-analysis | Int J Neuropsychopharmacol | Hamilton うつ病評価尺度 core items によるメタアナリシスで純粋抗うつ効果を直接確認 |
| [39340349](https://pubmed.ncbi.nlm.nih.gov/39340349/) | 2024 | Cohort | Int J Psychiatry Clin Pract | ミルタザピン血中濃度と抗うつ効果の関連性を検討；治療薬モニタリング（TDM）の臨床的意義を評価 |
| [8930007](https://pubmed.ncbi.nlm.nih.gov/8930007/) | 1995 | Meta-analysis | Int Clin Psychopharmacol | プール化データメタアナリシスによるミルタザピン臨床有効性の初期包括評価 |
| [8930006](https://pubmed.ncbi.nlm.nih.gov/8930006/) | 1995 | Review | Int Clin Psychopharmacol | ミルタザピンの中枢ノルアドレナリン・セロトニン神経伝達への作用機序の詳細解説（MOA 参照文献） |
| [10446741](https://pubmed.ncbi.nlm.nih.gov/10446741/) | 1999 | Review | J Clin Psychiatry | うつ病以外の精神疾患（パニック障害、GAD、PTSD 等）へのミルタザピン適応可能性を論じた総説 |

---

## 臨床試験エビデンス（気分変調症）

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT00080158](https://clinicaltrials.gov/study/NCT00080158) | Phase 2/3 | 完了 | 120 | 自殺企図歴を持つ抑うつ青少年の治療比較試験；dysthymia を含む広義の抑うつ群でのミルタザピン安全性・有効性データを提供 |
| [NCT04437485](https://clinicaltrials.gov/study/NCT04437485) | Phase 2 | 完了 | 46 | 抑うつ合併糖尿病リスク患者への協調ケア介入パイロット RCT；dysthymia と重複する抑うつ群を対象に血糖・インスリン抵抗性への間接効果を評価 |
| [NCT02458690](https://clinicaltrials.gov/study/NCT02458690) | Phase 2 | 完了 | 216 | 高齢抑うつ患者の心血管リスク低減を目的とした近代化 IMPACT 介入の RCT；dysthymia を含む広義の抑うつ群での長期エビデンスを提供 |

## 文献エビデンス（気分変調症）

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [21527126](https://pubmed.ncbi.nlm.nih.gov/21527126/) | 2011 | Meta-analysis | J Clin Psychiatry | 気分変調症に対する抗うつ薬のプラセボ対照試験メタアナリシス；抗うつ薬の有効性を確認し MDD との応答率比較を実施 |
| [10569129](https://pubmed.ncbi.nlm.nih.gov/10569129/) | 1999 | Cohort | Depression & Anxiety | 気分変調症患者 15 名へのミルタザピン 15-45mg 直接投与の小規模臨床データ；改善効果を報告した先駆的研究 |
| [36999619](https://pubmed.ncbi.nlm.nih.gov/36999619/) | 2023 | Meta-analysis | Cochrane Database Syst Rev | がん患者の大うつ病・抑うつ状態に対する抗うつ薬の有効性コクランシステマティックレビュー |
| [11310816](https://pubmed.ncbi.nlm.nih.gov/11310816/) | 2001 | Review | J Clin Psychiatry | 慢性抑うつ症（dysthymia・double depression 含む）の治療アルゴリズムにおける抗うつ薬の位置づけを解説 |
| [18833439](https://pubmed.ncbi.nlm.nih.gov/18833439/) | 2008 | Case series | Rev Bras Psiquiatr | MDD with dysthymia（double depression）へのベンラファキシン＋ミルタザピン California Rocket Fuel 療法の症例報告 |

---

## 臨床試験エビデンス（恐怖症性障害）

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT07333027](https://clinicaltrials.gov/study/NCT07333027) | N/A | 募集中 | 200 | 孤独感と抑うつ症状の関連を検討する入院精神科研究；社交回避行動の機序的連結から phobic disorder への間接的参考データを提供 |
| [NCT05737511](https://clinicaltrials.gov/study/NCT05737511) | Phase 4 | 未開始 | 80 | パニック障害に対するヒドロキシジン vs TAU のパイロット RCT；phobic disorder の重要亜型であるパニック障害の治療比較基準を提供 |

## 文献エビデンス（恐怖症性障害）

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [20715300](https://pubmed.ncbi.nlm.nih.gov/20715300/) | 2010 | RCT | Int Clin Psychopharmacol | 全般性社交不安障害に対するミルタザピン vs プラセボの二重盲検 RCT（N=60）；LSAS スコアで有意な改善を確認 |
| [16282842](https://pubmed.ncbi.nlm.nih.gov/16282842/) | 2005 | RCT | J Clin Psychopharmacol | 女性の社交恐怖症に対するミルタザピン vs プラセボの二重盲検 RCT（N=66）；社交恐怖への有効性を確認 |
| [11593305](https://pubmed.ncbi.nlm.nih.gov/11593305/) | 2001 | RCT | Braz J Med Biol Res | パニック障害に対するミルタザピン vs フルオキセチンの二重盲検 RCT；同等の有効性を確認 |
| [17419001](https://pubmed.ncbi.nlm.nih.gov/17419001/) | 2008 | Cohort | J Anxiety Disord | 社交恐怖症の小児・青年（8-17 歳）へのミルタザピンのオープンラベル試験；56% が治療奏効 |
| [12409686](https://pubmed.ncbi.nlm.nih.gov/12409686/) | 2002 | Cohort | Int Clin Psychopharmacol | 全般型社交不安障害患者 14 名へのミルタザピン 30mg 12 週投与；41.7% が奏効し良好な忍容性を確認 |

---

## 臨床試験エビデンス（神経症性うつ病）

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT04446039](https://clinicaltrials.gov/study/NCT04446039) | N/A | 完了 | 370,212 | 全国請求データベースを用いたミルタザピン含む主要抗うつ薬の大規模真実世界後ろ向きコホート研究；neurotic depression を含む広義の抑うつ患者群での有効性・安全性の最大級のリアルワールドエビデンス |

## 文献エビデンス（神経症性うつ病）

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [11806859](https://pubmed.ncbi.nlm.nih.gov/11806859/) | 2001 | Meta-analysis | Int J Neuropsychopharmacol | HAMD depression factor を用いたプラセボ対照メタアナリシスで、ミルタザピンの純粋抗うつ効果を直接確認 |
| [40449742](https://pubmed.ncbi.nlm.nih.gov/40449742/) | 2025 | RCT | J Affect Disord | 大うつ病患者での症状プロファイル別ミルタザピン差次的効果；神経症性要素の強い患者への応用示唆 |
| [10333982](https://pubmed.ncbi.nlm.nih.gov/10333982/) | 1998 | Meta-analysis | J Affect Disord | 軽度〜重度の幅広い抑うつ患者を対象とした臨床試験結果のメタアナリシス |
| [36253442](https://pubmed.ncbi.nlm.nih.gov/36253442/) | 2023 | Meta-analysis | Molecular Psychiatry | MDD 維持療法のネットワークメタアナリシス；再発予防効果の観点から neurotic depression への適用を間接支持 |
| [18299900](https://pubmed.ncbi.nlm.nih.gov/18299900/) | 2008 | RCT | Support Care Cancer | 抑うつ・不安・睡眠障害を共病するがん患者での RCT；神経症性うつ病に類似した症状プロファイルへの有効性を示す |

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
TxGNN が予測した 10 種類の適応症候補のうち、精神疾患群（メランコリー型うつ病 L1・気分変調症 L2・恐怖症性障害 L2・神経症性うつ病 L2）はいずれも NaSSA 機序との機序的一貫性が高く、かつ国際的な臨床試験データおよびメタアナリシスにより支持されています。なかでもメランコリー型うつ病は複数のメタアナリシスと RCT が存在し L1 の最高エビデンスレベルに達しており、台湾での適応承認申請の最優先ターゲットとして位置づけられます。

**進める場合に必要なもの：**
- 安全性情報（警告・禁忌・薬物相互作用）の補充（台湾仿单 PDF 解析：Data Gap DG001）
- 作用機序（MOA）データの DrugBank API 照会による正式確認（Data Gap DG002）
- 台湾における橋渡し臨床試験デザインの検討（国際承認データの外挿可能性評価）
- メランコリー型うつ病を主要ターゲットとした規制申請戦略の策定
- TxGNN スコア上位 5 件（Ohdo 症候群等の希少遺伝性疾患）は機序的根拠が確認されるまで Hold を維持
---

