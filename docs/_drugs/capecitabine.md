---
layout: default
title: Capecitabine
parent: 僅模型預測 (L5)
nav_order: 29
evidence_level: L5
indication_count: 10
---

# Capecitabine
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

# カペシタビン：大腸癌・乳癌 から 胃管状腺癌 へ

## 一言要約

カペシタビン（Capecitabine）は経口フルオロピリミジン系前駆薬で、腫瘍組織内のチミジンホスホリラーゼ（TP）により選択的に 5-FU へ変換され、大腸癌・乳癌の治療に広く使用されています。TxGNN モデルは胃癌の複数の組織学的亜型への転用可能性を予測しており、その中でも**胃管状腺癌 (Gastric Tubular Adenocarcinoma)** に対しては証拠レベル **L1** が確認されており、CLASSIC Phase 3 RCT を筆頭に **9 件の RCT** がこの方向性を強力に支持しています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 大腸癌・乳癌（グローバル承認）※日本 PMDA 登録データ取得不可 |
| 予測新規適応症 | 胃管状腺癌 (Gastric Tubular Adenocarcinoma) |
| TxGNN 予測スコア | 99.94% |
| エビデンスレベル | L1 |
| 日本市販状況 | データ取得不可（PMDA クエリ結果 0 件） |
| 承認番号数 | 0 件（要 PMDA 直接確認） |
| 推奨決定 | Proceed with Guardrails |

---

## この予測が妥当である理由

カペシタビンは腸管・肝臓・腫瘍組織の 3 段階の酵素変換を経て活性化される設計の経口前駆薬です。最終変換に関わるチミジンホスホリラーゼ（TP）は正常組織と比較して多くの固形腫瘍で高発現しており、正常組織への毒性を抑制しながら腫瘍選択的に 5-FU を産生するという優れた選択性をもたらします。活性型 5-FU はチミジル酸合成酵素（TYMS）を阻害し、DNA 複製に必須のデオキシチミジン一リン酸（dTMP）の合成を遮断することで腫瘍細胞の増殖を抑制します。

胃管状腺癌（tubular adenocarcinoma）は胃腺癌の中で最も頻度が高い組織学的亜型であり、アジア地域で特に多く発症します。胃腺癌腫瘍組織は TP を高発現する傾向があり、カペシタビンの選択的活性化機序が機能する生物学的環境を提供しています。TYMS は胃腺癌における重要な増殖依存因子であり、その阻害はこの亜型に対して機序的合理性を持ちます。

CLASSIC Phase 3 RCT（PMID 22226517）では D2 胃切除後の胃癌患者を対象に CAPOX（カペシタビン + オキサリプラチン）補助化学療法の有意な無病生存率改善が示され、L1 エビデンスの主要根拠となっています。RESOLVE trial（PMID 34252374）は局所進行胃癌における CAPOX 補助化療の有効性を再確認し、最終報告（PMID 39952264）でも長期生存データが更新されました。さらに GLOW・CheckMate 649・KEYNOTE-859・ORIENT-16・RATIONALE-305・GEMSTONE-303 等の主要 Phase 3 試験でも CAPOX が標準化学療法骨格として採用されており、カペシタビンの胃腺癌における中心的役割が確立されています。

---

## 臨床試験エビデンス

胃管状腺癌を対象とした専用の登録試験はありません。下記は、賁門・胃体部等の胃腺癌亜型を対象としカペシタビンを直接含む高関連度試験です。

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT00374036](https://clinicaltrials.gov/study/NCT00374036) | Phase 3 | 完了 | 416 | 転移性・局所進行胃および賁門腺癌を対象とした多剤化学療法戦略の比較；賁門癌を明示的に研究集団として包含した最大規模の試験 |
| [NCT00040859](https://clinicaltrials.gov/study/NCT00040859) | Phase 2 | 完了 | 48 | 可測量転移性食道・GEJ・胃賁門腺癌への Oxaliplatin + Capecitabine（CAPOX）；Capecitabine を研究薬として直接使用 |
| [NCT00938470](https://clinicaltrials.gov/study/NCT00938470) | Phase 2 | 完了 | 73 | 局所進行食道・GEJ・胃賁門腺癌への延長新輔助療法（Docetaxel + Oxaliplatin + Capecitabine + 放射線療法）；GEJ・賁門の解剖学的直接吻合 |
| [NCT01295086](https://clinicaltrials.gov/study/NCT01295086) | N/A | 完了 | 27 | HER2 陽性非切除可能食道・賁門・胃癌への TEX（Taxotere + Eloxatin + Xeloda/Capecitabine）+ Herceptin；Capecitabine を化療の構成要素として直接使用 |
| [NCT02595424](https://clinicaltrials.gov/study/NCT02595424) | Phase 2 | 進行中（招募停止） | 67 | 転移性・切除不能 G3 非小細胞消化管神経内分泌癌：Temozolomide + Capecitabine vs Cisplatin + Etoposide の無作為比較；胃体部腫瘍亜型において Capecitabine を直接評価 |
| [NCT00414271](https://clinicaltrials.gov/study/NCT00414271) | Phase 2 | 完了 | 18 | 局所進行胃癌の新輔助化学療法；チミジル酸合成酵素（TS）の免疫組織化学的発現と治療応答の相関を探索 |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [22226517](https://pubmed.ncbi.nlm.nih.gov/22226517/) | 2012 | RCT | Lancet | CLASSIC trial: D2 胃切除後 CAPOX 補助化療が対照群比で無病生存率を有意に改善（L1 エビデンスの主根拠） |
| [34252374](https://pubmed.ncbi.nlm.nih.gov/34252374/) | 2021 | RCT | Lancet Oncol | RESOLVE trial: 局所進行胃・GEJ 腺癌における周術期 SOX vs 補助 CAPOX — CAPOX の有効性を対照アームとして確認 |
| [39952264](https://pubmed.ncbi.nlm.nih.gov/39952264/) | 2025 | RCT | Lancet Oncol | RESOLVE trial 最終報告: CAPOX 補助化療の長期全生存率データを更新、有効性持続を確認 |
| [37524953](https://pubmed.ncbi.nlm.nih.gov/37524953/) | 2023 | RCT | Nature Medicine | GLOW Phase 3: CLDN18.2 陽性・HER2 陰性局所進行または転移性胃・GEJ 腺癌への Zolbetuximab + CAPOX |
| [34102137](https://pubmed.ncbi.nlm.nih.gov/34102137/) | 2021 | RCT | Lancet | CheckMate 649: HER2 陰性進行胃・GEJ 腺癌への Nivolumab + CAPOX または FOLFOX 一次治療；OS 有意改善 |
| [38806195](https://pubmed.ncbi.nlm.nih.gov/38806195/) | 2024 | RCT | BMJ | RATIONALE-305 Phase 3: 進行胃・GEJ 腺癌への Tislelizumab + 化学療法（CAPOX 含む）；OS 改善 |
| [37875143](https://pubmed.ncbi.nlm.nih.gov/37875143/) | 2023 | RCT | Lancet Oncol | KEYNOTE-859 Phase 3: HER2 陰性進行胃・GEJ 腺癌への Pembrolizumab + 化学療法（CAPOX 骨格）；OS 有意改善 |
| [38051328](https://pubmed.ncbi.nlm.nih.gov/38051328/) | 2023 | RCT | JAMA | ORIENT-16: 切除不能胃・GEJ 腺癌への Sintilimab + 化学療法（CAPOX 含む）；全集団および PD-L1 陽性集団での OS 改善 |
| [30982686](https://pubmed.ncbi.nlm.nih.gov/30982686/) | 2019 | RCT | Lancet | FLOT4 Phase 2/3: 切除可能胃・GEJ 腺癌周術期化療 FLOT vs ECF/ECX（Capecitabine 含む）；FLOT の優越性を示しつつ CAPOX 骨格の有効性を対照として確認 |
| [20728210](https://pubmed.ncbi.nlm.nih.gov/20728210/) | 2010 | RCT | Lancet | ToGA Phase 3: HER2 陽性進行胃・GEJ 癌への Trastuzumab + 化学療法（5-FU/Capecitabine + Cisplatin）；Capecitabine 含有レジメンの標準的位置づけを確立 |

---

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 従来型細胞毒性薬（フルオロピリミジン系前駆薬） |
| 骨髄抑制リスク | 中等度（好中球減少・血小板減少が主要な血液毒性；5-FU 静注と比較して重篤な骨髄抑制は相対的に少ない） |
| 催吐性分類 | 低〜中等度 |
| モニタリング項目 | CBC（白血球分画含む）、肝機能（AST・ALT・ビリルビン）、腎機能（血清クレアチニン・CCr）、手足症候群の皮膚症状評価、DPD 欠損リスク評価 |
| 取り扱い防護 | 細胞毒性薬取り扱い規程に従う（経口薬であるが調製・ピッキング・患者への説明時に適切な防護措置が必要） |

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
胃管状腺癌（胃腺癌で最も頻度が高い組織学的亜型）に対し、カペシタビンを含む CAPOX 療法の有効性を直接検証した複数の完了済み Phase 3 RCT（CLASSIC・RESOLVE・GLOW 等）が存在し、L1 エビデンスが確立されています。腫瘍選択的 TP 活性化と TYMS 阻害による DNA 合成抑制という機序的根拠も明確であり、機序・臨床エビデンスの両面から転用適格性が認められます。

**進める場合に必要なもの：**
- 日本 PMDA への直接照会によるカペシタビン（Xeloda®）承認状況の確認（PMDA クエリ 0 件の原因究明）
- DrugBank API 照会による詳細 MOA データの補完
- DPD（ジヒドロピリミジンデヒドロゲナーゼ）欠損スクリーニングを含む安全性モニタリング計画の策定
- 胃管状腺癌の具体的な病期・HER2/PD-L1 発現ステータスに基づく適応患者選択基準の明確化
- 用量・投与計画（標準: 1,250 mg/m² 1 日 2 回、14 日間投与 → 7 日休薬）と日本市場での実臨床使用状況の確認
---

