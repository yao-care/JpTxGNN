---
layout: default
title: Methotrexate
parent: 僅模型預測 (L5)
nav_order: 95
evidence_level: L5
indication_count: 10
---

# Methotrexate
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

# メトトレキサート：悪性リンパ腫から 原発性肺リンパ腫 へ

## 一言要約

メトトレキサート（MTX）は葉酸拮抗薬として、悪性リンパ腫・急性白血病・関節リウマチなど多様な疾患の治療に長年使用されてきた薬剤です。TxGNN モデルは 10 の新規適応症を予測しており、最高スコアを得た肺母細胞腫（pulmonary blastoma）はエビデンスが皆無（L5、Hold）のため、有証拠の筆頭予測として**原発性肺リンパ腫（Primary Pulmonary Lymphoma）**を本レポートの主要焦点として評価しました。現在 **12 件の臨床試験**と **20 編の文献**が高用量 MTX の結外リンパ腫への適用可能性を支持しており、ホジキンリンパ腫（L2）・小細胞肺癌（L2）についても歴史的 RCT を含む有意なエビデンスが確認されています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 悪性リンパ腫・急性白血病（CNS リンパ腫標準療法など）※PMDA データ未取得 |
| 予測新規適応症 | 原発性肺リンパ腫（Primary Pulmonary Lymphoma） |
| TxGNN 予測スコア | 99.45% |
| エビデンスレベル | L3 |
| 日本市販状況 | PMDA 照会 0 件（データ未取得） |
| 承認番号数 | 0 件（データ未取得） |
| 推奨決定 | Proceed with Guardrails |

---

## この予測が妥当である理由

メトトレキサートはジヒドロ葉酸還元酵素（DHFR）を競合阻害し、プリン合成および thymidylate 合成を阻断することで、急速増殖するリンパ球・腫瘍細胞に強力な細胞毒性を示します。加えて T 細胞活性化抑制・炎症性サイトカイン産生低下を介した免疫調節作用も有しており、リンパ増殖性疾患全般への薬理学的妥当性が高い薬剤です。本エビデンスパックでは詳細な MOA データが未取得ですが、DrugBank（DB00563）における DHFR 阻害機序は国際的に確立されています。

原発性肺リンパ腫（PPL）は全悪性リンパ腫の約 0.4〜1.0% を占める希少な結外リンパ腫で、主に DLBCL（びまん性大細胞型 B 細胞リンパ腫）または MALT 型リンパ腫として発症します。高用量 MTX（HD-MTX）はすでに原発性 CNS リンパ腫（PCNSL）の確立された標準療法であり（複数の Phase 2 コホート研究で有効性実証済み）、PPL が CNS リンパ腫と類似した免疫特権的な腫瘍微小環境を一部共有することから、機序的な外推が成立します。

特に重要な直接的関連性として、MTX 関連リンパ増殖性疾患（MTX-LPD）に起因する原発性肺 DLBCL の症例報告（PMID 38720609、2024 年）があり、MTX と肺リンパ腫の病態間に直接的なリンクが示されています。ただし PPL を対象とした前向き介入試験は現時点で存在せず、PCNSL エビデンスからの外推に依存している点は留意が必要です。

---

## 臨床試験エビデンス

（原発性肺リンパ腫 関連試験、関連性の高いものを最大 10 件）

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT00051311](https://clinicaltrials.gov/study/NCT00051311) | Phase 2 | 完了 | 62 | EPOCH-F/R 誘導化療（MTX 含む）後の降強度 allo-SCT。難治/再発リンパ腫を対象とし、PPL と病理的に重複する疾患族群への MTX 含有方案（Grade B） |
| [NCT02911142](https://clinicaltrials.gov/study/NCT02911142) | Phase 1/2 | 募集終了 | 17 | レナリドミド + 修正 DA-EPOCH-R による原発性滲出液リンパ腫（PEL）治療。PPL と類似した希少結外リンパ腫亜型への臨床アプローチ |
| [NCT00916630](https://clinicaltrials.gov/study/NCT00916630) | Phase 1 | 完了 | 18 | ペメトレキセド（葉酸拮抗薬）による再発/難治性 CNS リンパ腫の安全性評価。MTX と同クラスの抗葉酸薬としての間接的機序支持 |
| [NCT02345850](https://clinicaltrials.gov/study/NCT02345850) | Phase 3 | 完了 | 346 | Tac/MTX vs CNI フリー戦略の GvHD 予防 3 腕 Phase 3 RCT。血液悪性腫瘍 allo-SCT における MTX の標準免疫抑制役割を確立 |
| [NCT03959241](https://clinicaltrials.gov/study/NCT03959241) | Phase 3 | 完了 | 431 | Tac/MTX vs PT-Cy/Tac/MMF の GvHD 予防比較（降強度移植）。MTX を標準対照臂とした大規模比較試験 |
| [NCT00448357](https://clinicaltrials.gov/study/NCT00448357) | Phase 1/2 | 完了 | 54 | 最大強度 Busulfex ベース allo-HCT（広範囲血液疾患）。リンパ腫を含む移植設定での MTX 安全性データ |
| [NCT01338987](https://clinicaltrials.gov/study/NCT01338987) | Phase 2 | 完了 | 76 | Lupron による allo-BMT 後リンパ球免疫再建促進。移植後リンパ系免疫応答のメカニズム理解に寄与 |
| [NCT00245037](https://clinicaltrials.gov/study/NCT00245037) | Phase 1/2 | 完了 | 147 | 非清髄性 allo-HCT（Flu/Bu/TBI 前処理 + MTX 含む GvHD 予防）。MTX 投与時の腎機能・毒性プロファイルデータ |
| [NCT00448201](https://clinicaltrials.gov/study/NCT00448201) | Phase 2 | 完了 | 71 | 標準移植不適格血液疾患への低強度 allo-HCT。MTX を含む GvHD 予防の安全性背景 |
| [NCT02356159](https://clinicaltrials.gov/study/NCT02356159) | Phase 1/2 | 完了 | 34 | 非血縁者 allo-HCT における Palifermin の MTX 含む GvHD 予防設定での粘膜毒性軽減効果 |

---

## 文献エビデンス

（原発性肺リンパ腫 関連文献、優先順位に従い最大 10 編）

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [38720609](https://pubmed.ncbi.nlm.nih.gov/38720609/) | 2024 | Case series | Kyobu Geka | MTX-LPD 由来の原発性肺 DLBCL 症例報告（MTX と肺リンパ腫の直接的病態関連を実証する唯一の文献） |
| [30842385](https://pubmed.ncbi.nlm.nih.gov/30842385/) | 2019 | Cohort | Rinsho Ketsueki | PCNSL 6 例への HD-MTX + rituximab 療法の後ろ向き解析（日本における CNS リンパ腫標準療法の実績） |
| [11244328](https://pubmed.ncbi.nlm.nih.gov/11244328/) | 2001 | Cohort | Oncology | 免疫正常 PCNSL への HD-MTX + 放射線治療（鞘内化療なし）の実現可能性・有効性評価（Ferreri ら） |
| [15747120](https://pubmed.ncbi.nlm.nih.gov/15747120/) | 2005 | Cohort | Ann Hematol | MTX 500 mg/m² 含む修正 ProMACE-MOPP 方案による PCNSL 32 例の 2 年・5 年全生存率評価 |
| [12860951](https://pubmed.ncbi.nlm.nih.gov/12860951/) | 2003 | Cohort | J Clin Oncol | 60 歳超 PCNSL への化学療法単独（HD-MTX ベース）多施設 Phase 2（EORTC 26952）。高齢者安全性データを含む |
| [41485126](https://pubmed.ncbi.nlm.nih.gov/41485126/) | 2026 | Cohort | Cancer | BTKi + PD-1 阻害薬 + MTX 除外化療による PCNSL 一次治療の高奏効率。MTX の代替療法との位置付け比較に有用 |
| [32590768](https://pubmed.ncbi.nlm.nih.gov/32590768/) | 2020 | Case series | Medicine | 原発性肺 ENKTL-NT の 2 例報告と文献レビュー（計 20 例累積）。PPL の疾病スペクトラム背景資料 |
| [35831185](https://pubmed.ncbi.nlm.nih.gov/35831185/) | 2022 | Case series | Rinsho Ketsueki | 全身進展した原発性皮膚 ALCL に低用量 MTX が著効した症例（希少リンパ腫亜型への MTX 有効性） |
| [12241119](https://pubmed.ncbi.nlm.nih.gov/12241119/) | 2002 | Cohort | J Neuro-oncol | MTX 3500 mg/m² + シタラビン ± 脳照射による PCNSL 14 例の治療経験（HD-MTX 投与量・毒性データ） |
| [29931605](https://pubmed.ncbi.nlm.nih.gov/29931605/) | 2018 | Review | Curr Treat Options Oncol | 結外 DLBCL の分子分類・予後・CNS 再発リスクのレビュー（PPL が属する疾患スペクトラムの包括的整理） |

---

## 細胞毒性

メトトレキサートは葉酸拮抗薬・抗代謝薬として分類される抗腫瘍薬です。

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 従来型細胞毒性薬（葉酸拮抗薬・抗代謝薬） |
| 骨髄抑制リスク | 高（汎血球減少・白血球減少・血小板減少）：用量依存性。高用量（HD-MTX）では leucovorin レスキューが必須 |
| 催吐性分類 | 低〜中等度（低用量）、高（HD-MTX ≥500 mg/m²） |
| モニタリング項目 | CBC（分画含む）、血清 MTX 濃度（HD-MTX では治療後 24/48/72 時間モニタリング必須）、血清クレアチニン・BUN、肝機能（ALT/AST）、尿 pH（アルカリ化維持） |
| 取り扱い防護 | 細胞毒性薬取り扱い規程に従う必要あり |

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Proceed with Guardrails（原発性肺リンパ腫）**

**理由：**
HD-MTX は CNS リンパ腫の確立された標準療法であり、原発性肺リンパ腫（主に DLBCL・MALT 型）との結外リンパ腫としての病理学的重複、および MTX-LPD に起因する肺 DLBCL の直接症例報告（PMID 38720609）から機序的妥当性が支持されます。一方、PPL 特化の前向き介入試験は現時点で存在しないため、注意喚起付きの進行が適切です。

**その他の注目適応症：**
- **ホジキンリンパ腫（L2、Proceed with Guardrails）**：VBM 方案（ビンブラスチン/ブレオマイシン/MTX）が早期HL の複数コホート研究で CR 率 94〜100% を実証（PMID 14635074、7509382）。MIME 方案（MTX 含む）による難治/再発 HL 挽救療法のエビデンスもあり（PMID 2363941）。Phase 3 BEAM+PBSCT 試験（NCT00025636）が最高グレードの証拠として存在。
- **小細胞肺癌（L2、Research Question）**：ECMV 方案（etoposide/cyclophosphamide/MTX/vincristine）が Phase 3 RCT（PMID 7505104、SAKK 試験 PMID 7536028）で評価済み。現代標準治療（プラチナ+VP-16+免疫療法）への移行により MTX の役割は再定義が必要。

**進める場合に必要なもの：**
- 原発性肺リンパ腫（DLBCL 型・MALT 型別）に特化したパイロット研究の設計
- MOA 詳細データの補充（DrugBank API 照会により DG002 を解消）
- PMDA 添付文書 PDF の取得・解析による安全性プロファイルの確認（DG001 を解消）
- 現代リンパ腫標準療法（R-CHOP、BTKi 併用レジメン等）と HD-MTX の位置付け整理
---

