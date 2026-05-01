---
layout: default
title: Riboflavin
parent: 僅模型預測 (L5)
nav_order: 121
evidence_level: L5
indication_count: 10
---

# Riboflavin
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

Using `txgnn-pipeline` to confirm workflow context. The skill confirms this is a JpTxGNN report generation task — proceeding to produce the evaluation report from the Evidence Pack.

---

# リボフラビン（ビタミン B2）：栄養補助から Biotin 代謝疾患へ

## 一言要約

リボフラビン（ビタミン B2）は、FMN・FAD という補酵素に変換されてエネルギー代謝を支える水溶性ビタミンであり、ビタミン B2 欠乏症の補充を主な用途として世界的に広く使用されています。
TxGNN モデルは **Biotin 代謝疾患（biotin metabolic disease）** に対する有効性を予測しており、予測スコアは **94.88%** に達しています。
現在 **9 件の臨床試験**と **20 編の文献**が関連エビデンスとして収集されていますが、いずれも直接的な介入試験ではなく、機序的関連性を示す間接エビデンスにとどまります。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | ビタミン B2 欠乏症補充（栄養補助）|
| 予測新規適応症 | Biotin 代謝疾患（biotin metabolic disease）|
| TxGNN 予測スコア | 94.88% |
| エビデンスレベル | L4 |
| 日本市販状況 | 未上市（医薬品承認なし）|
| 承認番号数 | 0 件 |
| 推奨決定 | Hold |

---

## この予測が妥当である理由

現在、DrugBank からの詳細な作用機序データは取得できていません。既知の情報によると、リボフラビン（ビタミン B2）は体内でフラビンモノヌクレオチド（FMN）およびフラビンアデニンジヌクレオチド（FAD）に変換され、数百種の酵素の補酵素として機能します。エネルギー産生、酸化還元反応、脂肪酸 β 酸化、アミノ酸代謝など、広範な細胞代謝に不可欠な役割を担っています。

リボフラビンと biotin（ビタミン B7）は、SLC（溶質輸送体）トランスポーター経路を共有しており、ともに粒線体エネルギー代謝の必須補酵素です。PMID 37085971 は、在胎 25 週の双生児早産児が長期的な完全静脈栄養中にリボフラビンと biotin を同時に欠乏し、乳酸アシドーシス・多臓器不全を発症した症例を報告しており、両者の代謝的連鎖関係を直接示しています。また PMID 40258084 は、小児代謝疾患の治療に thiamine・リボフラビン・pyridoxine・biotin の複合カプセル製剤が処方される実臨床慣行を記録しており、リボフラビンが biotin 代謝関連疾患の補助治療として実際に使用されている背景を裏付けています。

ただし、リボフラビン単独で biotin 代謝疾患を直接治療した介入研究は現時点では存在せず、TxGNN の予測は機序的関連性の示唆にとどまります。SLC 輸送体を介した相互補完仮説を検証するための前臨床研究が次のステップとして必要です。

---

## 臨床試験エビデンス

以下の 9 件はすべて間接的エビデンスであり、リボフラビンを biotin 代謝疾患に直接投与した試験は含まれません。

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT05687474](https://clinicaltrials.gov/study/NCT05687474) | N/A | 完了 | 6,824 | 新生児全ゲノム篩検プログラム（Baby Detect）；biotin 関連代謝疾患を含む 126 疾患を対象とした早期発見研究 |
| [NCT03655223](https://clinicaltrials.gov/study/NCT03655223) | N/A | 招待登録中 | 30,000 | Early Check 新生児症状前臨床試験協作；代謝性疾患を含む希少疾患の早期介入基盤構築 |
| [NCT02302729](https://clinicaltrials.gov/study/NCT02302729) | N/A | 完了 | 1,730 | グアテマラの発育不全幼児に対する微量栄養素パウダー（riboflavin 含有）vs プラセボ + 早期学習プログラム比較試験 |
| [NCT01643187](https://clinicaltrials.gov/study/NCT01643187) | Phase 2 | 不明 | 1,000 | 栄養不良幼児における強化食品 vs 牛乳の栄養・微量栄養素状態への影響（riboflavin 含む） |
| [NCT01173315](https://clinicaltrials.gov/study/NCT01173315) | Phase 2 | 完了 | 75 | 2 型糖尿病患者へのビタミン・ミネラル複合補充が神経・腎病変に与える影響；血糖・脂質・酸化ストレスを評価 |
| [NCT04586348](https://clinicaltrials.gov/study/NCT04586348) | Phase 4 | 募集終了・進行中 | 794 | 産前ヨウ素補充と乳幼児神経発育 RCT；目標微量栄養素はヨウ素で riboflavin との直接関連は低い |
| [NCT03444155](https://clinicaltrials.gov/study/NCT03444155) | N/A | 完了 | 30 | 天然 vs 合成ビタミン B 複合物の生物学的利用率クロスオーバー比較；riboflavin の吸収動態データを提供 |
| [NCT03360435](https://clinicaltrials.gov/study/NCT03360435) | N/A | 完了 | 99 | 胃バイパス術後患者への経皮ビタミンパッチによる微量栄養素（riboflavin 含む）の吸収評価 |
| [NCT01474486](https://clinicaltrials.gov/study/NCT01474486) | N/A | 完了 | 40 | うっ血性心不全患者への多微量栄養素（riboflavin 含む）介入による心機能・QOL 改善の実現可能性試験 |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [37085971](https://pubmed.ncbi.nlm.nih.gov/37085971/) | 2023 | Case series | J Investig Med High Impact Case Rep | 双生児早産児（在胎 25.6 週）が長期 TPN 中にリボフラビンと biotin を同時欠乏；乳酸アシドーシス・多臓器不全を発症し、両ビタミン補充で改善 |
| [40258084](https://pubmed.ncbi.nlm.nih.gov/40258084/) | 2025 | In vitro | PLoS One | 小児代謝疾患の治療に thiamine・riboflavin・pyridoxine・biotin 複合カプセルを事前調製・保存する安全な代替法を検証；安定性確認済み |
| [39234898](https://pubmed.ncbi.nlm.nih.gov/39234898/) | 2024 | Review | Clin Pharmacol Ther | 血液脳関門の膜輸送体変異と希少疾患；riboflavin・biotin 等のビタミン輸送体（SLC 遺伝子）変異が代謝疾患を引き起こすことを系統的に解説 |
| [34797406](https://pubmed.ncbi.nlm.nih.gov/34797406/) | 2022 | Case series | Human Genetics | サウジアラビア小児の SLC 遺伝子変異と神経学的疾患；riboflavin・biotin 輸送に関わる SLC52A2、SLC5A6 等の変異例を報告 |
| [15231238](https://pubmed.ncbi.nlm.nih.gov/15231238/) | 2004 | Review | Ageing Res Rev | ヘム生合成には riboflavin・biotin・パントテン酸・リポ酸が必要であることを解説；両者の粒線体機能における補完的役割を強調 |
| [33158037](https://pubmed.ncbi.nlm.nih.gov/33158037/) | 2020 | Review | Nutrients | B 群ビタミンが免疫調節・癌に果たす役割のレビュー；riboflavin の補酵素機能（FMN/FAD）と代謝経路への関与を解説 |
| [40076592](https://pubmed.ncbi.nlm.nih.gov/40076592/) | 2025 | Review | Int J Mol Sci | B 群ビタミン（B1〜B12、biotin 含む）の癌予防・進展における最新知見；riboflavin と biotin の相互依存的な代謝経路を論じる |
| [37189771](https://pubmed.ncbi.nlm.nih.gov/37189771/) | 2023 | Review | Biomedicines | ビタミン B 欠乏と糖尿病性腎症の生理学的関連；riboflavin を含む B 群欠乏が腎機能に与える影響を系統的に解説 |
| [7015958](https://pubmed.ncbi.nlm.nih.gov/7015958/) | 1980 | Review | Ann NY Acad Sci | B 群ビタミン間の相互作用；riboflavin 欠乏が他の B ビタミン（biotin を含む）の代謝と利用率に連鎖的影響を与えることを示す古典的論文 |
| [40563372](https://pubmed.ncbi.nlm.nih.gov/40563372/) | 2025 | In vitro | Antioxidants (Basel) | エチルマロン酸脳症（ETHE1 変異）の細胞モデルで粒線体 UPR 活性化が病態改善；biotin 関連代謝疾患に類似する粒線体機能不全モデルとして参照価値あり |

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

> **注記**：本 Evidence Pack では薬物相互作用・主要警告・禁忌のいずれも取得できていません（データギャップ DG001）。リボフラビンは水溶性ビタミンであり過剰分は尿中に排泄されるため毒性リスクは一般的に低いとされていますが、正式な評価には PMDA 仿単の確認が必要です。

---

## 結論と次のステップ

**決定：Hold**

**理由：**
TxGNN 予測スコアは 94.88% と高いものの、リボフラビンを biotin 代謝疾患に直接投与した介入研究は現時点で存在せず、エビデンスは機序的関連性（SLC 共有輸送体・粒線体補酵素補完）を示す間接的・背景的知見にとどまります（L4）。仮説は生物学的に筋が通っており価値ある研究方向ですが、前臨床検証が先行して必要です。

**進める場合に必要なもの：**
- **前臨床研究**：biotin 代謝酵素欠損モデル（ビオチニダーゼ欠損症、ホロカルボキシラーゼ合成酵素欠損症）における riboflavin 補充の有効性・機序検証
- **MOA データ補完**：DrugBank API クエリによる riboflavin の完全な作用機序情報の取得（DG002 解消）
- **安全性情報**：PMDA 仿単 PDF の取得・解析（DG001 解消）
- **SLC 輸送体相互作用解析**：SLC52A2（RFVT2）および SLC5A6（SMVT）における riboflavin・biotin 競合輸送の in vitro 検証
- **患者レジストリ検索**：biotin 代謝疾患（ビオチニダーゼ欠損症）の患者コホートにおける riboflavin 状態の後方視的調査
---

