---
layout: default
title: Bisoprolol
parent: 僅模型預測 (L5)
nav_order: 25
evidence_level: L5
indication_count: 10
---

# Bisoprolol
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

# ビソプロロール：心不全・高血圧 から 慢性肺性心疾患 へ

## 一言要約

ビソプロロール（Bisoprolol）は高度選択的 β1 受体遮断薬として、心不全・高血圧・狭心症の治療に広く使用されている薬物です。TxGNN モデルは上位 10 疾患への再利用可能性を予測しており、中でも**慢性肺性心疾患（Chronic Pulmonary Heart Disease）**に対しては **16 件の臨床試験**と **20 編の文献**を含む実質的なエビデンスが存在し、L2 レベルの支持が確認されています。TxGNN スコア最上位の悪性腎血管性高血圧（99.94%）はエビデンスが皆無のため保留推奨であり、慢性肺性心疾患（98.63%）が実際に進めることのできる最優先候補です。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 承認情報なし（PMDA データ未取得） |
| 主要予測新規適応症 | 慢性肺性心疾患（Chronic Pulmonary Heart Disease） |
| TxGNN 予測スコア | 98.63% |
| エビデンスレベル | L2 |
| 日本市販状況 | ✗ 未上市（承認情報なし） |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails |

---

## 全予測適応症サマリー

本エビデンスパックは複数適応症（multi）に対する予測を含みます。

| ランク | 疾患名 | TxGNN スコア | エビデンスレベル | 推奨 |
|------|------|------|------|------|
| 1 | 悪性腎血管性高血圧 | 99.94% | L5 | Hold |
| 2 | 悪性高血圧性腎疾患 | 99.94% | L5 | Hold |
| 3 | 多因子性肺高血圧（機序不明） | 99.93% | L5 | Hold |
| 4 | 肺疾患/低酸素性肺高血圧 | 99.93% | L5 | Hold |
| 5 | Braddock 症候群 | 99.91% | L5 | Hold |
| **6** | **慢性肺性心疾患** ← 最優先 | **98.63%** | **L2** | **Proceed with Guardrails** |
| 7 | Prinzmetal 狭心症 ⚠️ | 94.42% | L4 | Hold |
| 8 | 虚血性脳卒中感受性（廃止術語） | 75.23% | L5 | Hold |
| 9 | 脳幹梗塞 | 68.17% | L5 | Hold |
| 10 | 脳血管障害 | 68.13% | L4 | Research Question |

> ⚠️ **Prinzmetal 狭心症**：Beta-blockers は従来この病態への相対禁忌。α 受体相対優位化による冠動脈攣縮増悪リスクがあるため、状態不明の試験 1 件（NCT05294887）のみでは進捗不可。

---

## この予測が妥当である理由

ビソプロロールは現在知られている中で最も高い β1 選択性を持つ beta-blocker の一つであり、β1/β2 親和性比は約 75:1 と報告されています。この高度選択性が、気道の β2 受体に悪影響を与えずに心臓保護効果を発揮する根拠となっています（PMID 38597063）。詳細な MOA データは本エビデンスパックでは未取得のため、既知の薬理学的知見に基づいて評価を行っています。

慢性肺性心疾患（肺疾患を基盤とする右心室過負荷・不全、代表的には COPD に伴う肺性心）の病態では、交感神経系の持続的亢進が心室リモデリングと不整脈リスクを増大させます。ビソプロロールによる β1 遮断は心拍数低下・右心室機能改善・交感神経過活動の抑制を通じた心臓保護効果という合理的な機序的根拠があります。実験的肺高血圧モデルでは、低用量の bisoprolol 慢性投与が右心室不全への進行を有意に遅延させることが動物実験で直接示されています（PMID 22157723）。

臨床的には、2024 年の BICS 試験（JAMA 掲載、PMID 38762800）がビソプロロールを高リスク COPD 患者に投与した大規模 RCT として安全性を確認し、メタ解析（PMID 38152590）も COPD 患者群における bisoprolol の全体的な安全性・有効性を支持しています。COPD 合併心不全患者を対象としたコホート研究（PMID 29159953）でも bisoprolol/metoprolol/nebivolol が carvedilol と比較して推奨されており、ガイドライン的支持も確立しています。

---

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT00702156](https://clinicaltrials.gov/study/NCT00702156) | Phase 2 | 終了 | 27 | 慢性心不全合併中等度〜重症 COPD 患者への bisoprolol 心臓選択的 beta-blockade の肺機能・QOL への影響評価（直接最高関連、早期終了） |
| [NCT01656005](https://clinicaltrials.gov/study/NCT01656005) | Phase 4 | 完了 | 18 | 中等度〜重症 COPD における心臓選択性・非選択性 beta-blockers の慢性暴露が心肺機能指標に与える効果を比較評価 |
| [NCT02106286](https://clinicaltrials.gov/study/NCT02106286) | Early Phase 1 | 完了 | 55 | 心肺運動試験による beta-blockade の心肺機能への直接影響を評価（周術期心機能リスク指標との関連） |
| [NCT02380053](https://clinicaltrials.gov/study/NCT02380053) | Phase 4 | 完了 | 10 | COPD 患者における慢性 beta-blockade の心肺アウトカム：celiprolol vs bisoprolol の差異的効果 |
| [NCT00517725](https://clinicaltrials.gov/study/NCT00517725) | Phase 4 | 完了 | 60 | 心不全における nebivolol vs bisoprolol vs carvedilol の運動耐容能・低酸素・化学受容体反応・肺機能への影響比較 |
| [NCT03917914](https://clinicaltrials.gov/study/NCT03917914) | Phase 3 | 完了 | 280 | COPD 患者の既知・未診断心血管リスクを積極的治療することで心臓・呼吸器アウトカムが改善するかを二重盲検 RCT で検討 |
| [NCT03278509](https://clinicaltrials.gov/study/NCT03278509) | Phase 4 | 募集完了 | 5,000 | REDUCE-SWEDEHEART：心筋梗塞後・保存型駆出分率患者における beta-blocker 長期効果の大規模レジストリ試験 |
| [NCT03778554](https://clinicaltrials.gov/study/NCT03778554) | Phase 4 | 募集完了 | 2,760 | DANBLOCK：射出分率保存型心筋梗塞後 beta-blocker 投与の複合心血管アウトカム（再梗塞・死亡・血行再建・心不全）評価 |
| [NCT01829880](https://clinicaltrials.gov/study/NCT01829880) | N/A | 不明 | 60 | 心不全患者の悪液質・体組成変化が bisoprolol および ramipril の薬物動力学と腎機能推算精度に与える影響 |
| [NCT04542785](https://clinicaltrials.gov/study/NCT04542785) | N/A | 不明 | 350 | DanAF 試験：心房細動における寛容的心拍数管理 vs. 厳格心拍数管理の無作為化比較（心機能・QOL 指標） |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [38762800](https://pubmed.ncbi.nlm.nih.gov/38762800/) | 2024 | RCT | JAMA | BICS 試験：高リスク COPD 患者への bisoprolol 投与、安全性確認・急性増悪予防効果を大規模 RCT で検討 |
| [40386836](https://pubmed.ncbi.nlm.nih.gov/40386836/) | 2025 | RCT | Health Technol Assess | BICS 試験完全報告：COPD 患者への bisoprolol 有効性・安全性に関する詳細データおよびコスト評価 |
| [38587241](https://pubmed.ncbi.nlm.nih.gov/38587241/) | 2024 | RCT | N Engl J Med | 心筋梗塞後・射出分率保存型患者における beta-blocker 治療の現代的評価（非劣性試験） |
| [19460848](https://pubmed.ncbi.nlm.nih.gov/19460848/) | 2009 | RCT | Eur J Heart Fail | 心不全合併中等度〜重症 COPD 患者における bisoprolol の前向き無作為化対照試験（慢性肺性心疾患の中核エビデンス） |
| [33847660](https://pubmed.ncbi.nlm.nih.gov/33847660/) | 2021 | RCT | Medicine | 慢性心不全+COPD 患者への trimetazidine + bisoprolol 併用療法の有効性・安全性系統的レビュー・メタ解析 |
| [38152590](https://pubmed.ncbi.nlm.nih.gov/38152590/) | 2023 | Meta-analysis | Int J COPD | COPD 患者における bisoprolol の有効性・安全性：システマティックレビューとメタ解析 |
| [29159953](https://pubmed.ncbi.nlm.nih.gov/29159953/) | 2018 | Cohort | Eur J Heart Fail | 心不全+COPD 患者の carvedilol vs bisoprolol/metoprolol/nebivolol：全原因・COPD・HF 入院リスク比較（デンマーク全国コホート） |
| [31391573](https://pubmed.ncbi.nlm.nih.gov/31391573/) | 2019 | Cohort | Scientific Reports | 心不全+COPD 患者における bisoprolol 選択を規定する予測因子（イタリア地域登録研究） |
| [27792991](https://pubmed.ncbi.nlm.nih.gov/27792991/) | 2017 | Cohort | Int J Cardiology | 慢性心不全患者における bisoprolol vs carvedilol の心筋保護・肺機能保護効果の差異比較 |
| [22157723](https://pubmed.ncbi.nlm.nih.gov/22157723/) | 2012 | Animal | Circ Heart Fail | 実験的肺高血圧モデル：bisoprolol 低用量慢性投与による右心室不全進行遅延効果の機序解析 |

---

## 日本市販情報

本エビデンスパックの PMDA 照会（2026-03-10）では承認情報が取得できませんでした（承認件数 0 件、市販状況：未上市）。

> **注意**：ビソプロロールは海外では心不全・高血圧・狭心症の適応症で広く承認されており（CIBIS-II 試験など）、日本国内でも「メインテート®」等の商品名で汎用されていることが本エビデンスパック内の複数文献から確認されます（例：PMID 34083113 に日本発のビソプロロール経皮パッチ研究）。PMDA データ取得 0 件はデータ収集の技術的問題である可能性が高く、再確認を強く推奨します。

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

> 本エビデンスパックでは警告・禁忌・薬物相互作用のすべてがデータギャップです。慢性肺性心疾患患者への適用にあたっては特に以下の点に留意が必要です：
> - 喘息・重症気管支攣縮のある患者への適用（β1 高度選択性にもかかわらず重症例では注意）
> - 著明な肺高血圧を合併する症例での右心室機能悪化リスク
> - 高度徐脈・房室ブロックを有する患者への禁忌の確認

---

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
慢性肺性心疾患（主に COPD を基盤とする心疾患）に対し、BICS 試験（JAMA 2024）を含む複数の RCT・メタ解析・コホート研究がビソプロロールの安全性と一定の有効性を支持しています。β1 高度選択性による気管支収縮リスクの最小化という機序的合理性も確立されており、L2 レベルのエビデンスが揃っています。

**進める場合に必要なもの：**
- PMDA 承認情報の再確認（データギャップ解消、既存適応症・添付文書警告の確認）
- 作用機序データ（MOA）の取得（DrugBank API 照会、DG002 対応）
- 安全性情報（警告・禁忌・DDI）の取得（添付文書 PDF 解析、DG001 対応）
- Prinzmetal 狭心症（ランク 7）への適用は beta-blocker 相対禁忌のため現時点では不推奨
- 慢性肺性心疾患の疾患範囲明確化（ICD-10 I26-I28 相当の定義特定）
- 肺高血圧合併例での bisoprolol 用量設定プロトコルおよびモニタリング計画の策定
---

