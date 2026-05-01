---
layout: default
title: Metoprolol
parent: 僅模型預測 (L5)
nav_order: 97
evidence_level: L5
indication_count: 10
---

# Metoprolol
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

# メトプロロール：高血圧・心不全 から 慢性肺性心疾患 へ

## 一言要約

メトプロロールは高い β₁ 選択性を持つアドレナリン受容体遮断薬で、国際的に高血圧・慢性心不全・狭心症・不整脈などの心疾患治療に広く用いられています（日本での承認なし）。
TxGNN モデルは 10 の新規適応症を予測しており、そのうち **慢性肺性心疾患 (Chronic Pulmonary Heart Disease)** が最もエビデンスの充実した候補です。
現在 **15 件の臨床試験**（Phase 3/4 を含む）と **20 編の文献**（*NEJM*・*JAMA* 掲載 RCT を含む）がこの方向性を支持しています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本未承認（国際的：高血圧・心不全・狭心症・不整脈） |
| 予測新規適応症 | 慢性肺性心疾患 (Chronic Pulmonary Heart Disease) |
| TxGNN 予測スコア | 99.40% |
| エビデンスレベル | L2 |
| 日本市販状況 | ✗ 未上市 |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails |

---

## 全予測候補サマリー

本レポートは候補 ID `TW-DB00264-multi`（10 適応症）の評価結果です。以下に全候補の概要を示し、最もエビデンスが充実した「慢性肺性心疾患」（順位 9）を主要候補として詳述します。

| 順位 | 疾患名 | TxGNN スコア | エビデンスレベル | 推奨決定 |
|------|--------|------------|--------------|--------|
| 1 | Malignant Hypertensive Renal Disease | 99.91% | L5 | Hold |
| 2 | Malignant Renovascular Hypertension | 99.91% | L5 | Hold |
| 3 | Pulmonary Hypertension with Unclear Multifactorial Mechanism | 99.91% | L5 | Hold |
| 4 | Pulmonary Hypertension owing to Lung Disease and/or Hypoxia | 99.91% | L5 | Hold |
| 5 | Braddock Syndrome | 99.89% | L5 | Hold |
| 6 | Posterolateral Myocardial Infarction | 99.84% | L3 | Research Question |
| 7 | Posteroinferior Myocardial Infarction | 99.84% | L5 | Hold |
| 8 | Septal Myocardial Infarction | 99.80% | L3 | Research Question |
| **9** | **Chronic Pulmonary Heart Disease** | **99.40%** | **L2** | **Proceed with Guardrails** |
| 10 | Trichotillomania | 99.05% | L5 | Hold |

---

## この予測が妥当である理由

メトプロロールは高い β₁ 選択性を持つアドレナリン受容体遮断薬で、β₁ 受容体を優先的に遮断することで心拍数・心拍出量を低下させ、交感神経張力を抑制します。β₂ 受容体への影響が非選択性β遮断薬より限定的なため、気管支平滑筋への影響が相対的に少なく、肺疾患合併患者への使用適性が比較的高いとされています。なお、本 Evidence Pack では詳細な作用機序データ（MOA）は確認されていません。DrugBank API からの補完が推奨されます。

慢性肺性心疾患（肺性心）は COPD・慢性肺高血圧症を主な原因とし、慢性的な肺の過負荷によって右心室の肥大・機能不全をきたす病態です。β₁ 遮断による心拍数低下と交感神経張力の抑制は、右心室後負荷の軽減および心臓リモデリングの抑制につながる可能性があります。また COPD 患者は心不全・不整脈を高頻度に合併しており、心臓選択性β遮断薬の使用が生存率改善と関連するとの観察研究が台湾・デンマークなど複数の大規模データベース研究から報告されています。

一方で、β遮断薬を COPD 合併患者に使用する際は、気管支痙攣の誘発や急性増悪頻度の増加というリスクが懸念されます。BLOCK COPD 試験（Phase 3 RCT）ではメトプロロールが COPD 急性増悪予防に有効でなく、入院を要する増悪を増加させた可能性が示唆されており、適応患者の慎重な選択と継続的な肺機能モニタリングが不可欠です。

---

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT02587351](https://clinicaltrials.gov/study/NCT02587351) | Phase 3 | 早期終了 | 532 | BLOCK COPD：中等度〜重症 COPD 患者へのメトプロロールは急性増悪予防効果を示さず、入院を要する増悪リスク増加の可能性を報告；本適応症における最高水準の直接的 RCT |
| [NCT03566667](https://clinicaltrials.gov/study/NCT03566667) | Phase 4 | 登録終了・進行中 | 1,713 | BRONCHO：明らかな心疾患のない高増悪リスク COPD 患者へのβ遮断薬投与が死亡・増悪を抑制するかを検討中（完了予定 2026-04-30） |
| [NCT06825728](https://clinicaltrials.gov/study/NCT06825728) | Phase 4 | 登録未開始 | 311 | HFrEF 合併 COPD 患者に対するメトプロロールの有効性・安全性・最適用量を評価予定（開始予定 2025-02、完了予定 2028-02）；本レポートで最も直接的な試験 |
| [NCT00288548](https://clinicaltrials.gov/study/NCT00288548) | Phase 4 | 不明 | 45 | COPD 患者におけるメトプロロール＋フォルモテロール（β刺激薬）併用の肺機能への影響を検討 |
| [NCT03370835](https://clinicaltrials.gov/study/NCT03370835) | Phase 4 | 完了 | 21 | COPD 患者における Metoprolol-Succinate-ER vs Carvedilol の忍容性をランダム化クロスオーバー試験で比較 |
| [NCT00384566](https://clinicaltrials.gov/study/NCT00384566) | Phase 4 | 撤回 | 0 | CAMERA：CHF 合併呼吸器疾患患者での Carvedilol vs Metoprolol の肺機能影響比較（登録前撤回、設計自体は高関連性） |
| [NCT00292162](https://clinicaltrials.gov/study/NCT00292162) | NA | 完了 | 41 | 進行性 CHF 合併 AF 患者への高周波アブレーション治療；心肺合併疾患コホートでの安全性・有効性データを提供 |
| [NCT00745043](https://clinicaltrials.gov/study/NCT00745043) | NA | 完了 | 11 | COPD 患者においてβ遮断薬がβ刺激薬吸入器の使用量に与える影響を評価；合併用薬管理の安全性データ |
| [NCT03278509](https://clinicaltrials.gov/study/NCT03278509) | Phase 4 | 登録終了・進行中 | 5,000 | REDUCE-SWEDEHEART：射血分数保持 MI 後患者での長期β遮断薬療法の死亡・再梗塞抑制効果（COPD 合併例を含む可能性） |
| [NCT03778554](https://clinicaltrials.gov/study/NCT03778554) | Phase 4 | 登録終了・進行中 | 2,760 | DANBLOCK：心不全のない MI 後患者へのβ遮断薬長期投与の複合アウトカム（再梗塞・死亡・脳卒中・新規心不全など）への影響 |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [38587241](https://pubmed.ncbi.nlm.nih.gov/38587241/) | 2024 | RCT | N Engl J Med | REDUCE-MI 試験：射血分数保持 MI 後患者においてβ遮断薬は死亡・再梗塞を有意に減少させず；現代的治療背景でのβ遮断薬の位置付けを再考させる知見 |
| [38762800](https://pubmed.ncbi.nlm.nih.gov/38762800/) | 2024 | RCT | JAMA | BICS 試験：高増悪リスク COPD 患者へのビソプロロールは増悪頻度を減少させず入院増悪が増加傾向；BLOCK COPD（メトプロロール）の知見と整合し、β遮断薬全体のリスク再評価を促す |
| [32000982](https://pubmed.ncbi.nlm.nih.gov/32000982/) | 2020 | Cohort | Am J Cardiol | デンマーク行政登録：HF+COPD+DM 合併高齢患者でメトプロロール vs カルベジロールの生存率と再入院リスクを 1:1 傾向スコアマッチングで比較 |
| [29159953](https://pubmed.ncbi.nlm.nih.gov/29159953/) | 2018 | Cohort | Eur J Heart Fail | デンマーク全国コホート：HF 合併 COPD 患者でカルベジロール vs 心臓選択性β遮断薬（メトプロロール含む）の COPD 関連入院リスクを評価 |
| [26844454](https://pubmed.ncbi.nlm.nih.gov/26844454/) | 2016 | Cohort | Medicine | 台湾 NHI ビッグデータ：HF+COPD 合併患者においてメトプロロール含むβ遮断薬が全死亡を有意に減少させることを示す |
| [31391690](https://pubmed.ncbi.nlm.nih.gov/31391690/) | 2019 | Cohort | Med Arch | 中等度〜重症 COPD 患者における選択的β遮断薬の安全性と有効性を評価；臨床ガイドラインとの齟齬を議論 |
| [33784233](https://pubmed.ncbi.nlm.nih.gov/33784233/) | 2021 | Cohort | Ann Am Thorac Soc | BLOCK COPD 副次解析：時系列心拍指数が COPD 急性増悪リスクと関連し、メトプロロール有害効果の予測マーカーとなる可能性を示唆 |
| [15358010](https://pubmed.ncbi.nlm.nih.gov/15358010/) | 2004 | Review | JACC | CHF+COPD 合併患者における非選択的・選択的β遮断薬療法の包括的レビュー；換気制限と心拍出量低下の相互作用を解析 |
| [32250198](https://pubmed.ncbi.nlm.nih.gov/32250198/) | 2020 | Review | Expert Rev Respir Med | COPD 患者へのβ遮断薬使用に関する実践的推奨；安全性エビデンスと潜在的有益性を包括的にまとめた臨床指針 |
| [31391573](https://pubmed.ncbi.nlm.nih.gov/31391573/) | 2019 | Review | Sci Reports | イタリア登録コホート：HF+COPD 患者におけるβ遮断薬選択の予測因子とメトプロロール vs カルベジロールの交換可能性を検討 |

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
慢性肺性心疾患（COPD 合併心不全を含む）に対するメトプロロールは L2 レベルのエビデンスを有し、大規模 Phase 3/4 試験が複数存在します。しかしながら BLOCK COPD（Phase 3 RCT）は入院を要する COPD 急性増悪リスクの増加を示しており、2024 年の BICS 試験（JAMA）も類似の懸念を提示していることから、適応患者の層別化と継続的な肺機能モニタリング体制の構築を前提とした条件付き前進が適切です。

**進める場合に必要なもの：**
- 詳細な作用機序データ（MOA）の補完（DrugBank API から取得可能、DG002 対応）
- 日本国内安全性情報の収集（PMDA 添付文書相当資料の解析、DG001 対応）
- 適応患者層別化基準の策定（COPD 重症度・右心機能・合併心疾患の種類による選択基準）
- 有効性エンドポイントの明確化（右心不全入院・肺機能低下・全死亡・急性増悪頻度）
- 進行中試験の結果を待って再評価：BRONCHO（NCT03566667、n=1,713、完了予定 2026-04-30）および Metoprolol in HFrEF+COPD（NCT06825728、n=311、完了予定 2028-02）
- Rank 6（後外側 MI、L3）および Rank 8（中隔 MI、L3）については追加文献収集と Research Question 段階の評価継続を推奨
---

