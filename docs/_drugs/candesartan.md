---
layout: default
title: Candesartan
parent: 僅模型預測 (L5)
nav_order: 28
evidence_level: L5
indication_count: 10
---

# Candesartan
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

# カンデサルタン：高血圧症から偏頭痛へ

## 一言要約

カンデサルタンはアンジオテンシン II タイプ 1（AT1）受容体拮抗薬（ARB）として世界的に高血圧症・心不全の治療に広く使用されていますが、日本（PMDA）における本 DrugBank エントリ（DB13919）への承認記録は確認されていません。TxGNN モデルは**偏頭痛 (migraine disorder)** への有効性を予測しており、現在 **4 件の臨床試験**と **20 編の文献**がこの方向性を支持しています。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 高血圧症（グローバル承認あり、日本 PMDA 未収載） |
| 予測新規適応症 | 偏頭痛 (migraine disorder) |
| TxGNN 予測スコア | 99.97% |
| エビデンスレベル | L1 |
| 日本市販状況 | 未上市 |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails |

## この予測が妥当である理由

カンデサルタンはレニン-アンジオテンシン-アルドステロン系（RAAS）の AT1 受容体を選択的に阻断する ARB です。詳細な MOA データは本 Evidence Pack には未収録ですが、AT1 受容体阻断により血管収縮・ナトリウム貯留・臓器リモデリングを促すアンジオテンシン II のシグナルを遮断することが薬理学的に確立されています。

偏頭痛の病態生理においては、三叉神経血管系の活性化と神経炎症が中心的な役割を果たします。カンデサルタンは脳血管の AT1 受容体を阻断することで、アンジオテンシン II が誘発する三叉神経血管活性化・神経炎症を抑制し、さらに皮質拡散性抑制（CSD）の発生頻度低下および CGRP 放出調節を通じて偏頭痛発作頻度を減少させると考えられます。

加えて、RAAS 系の遺伝的多態性（ACE I/D 多態性など）が偏頭痛易感性に関与することが複数の研究で示されており、ARB 介入が偏頭痛予防として生物学的に合理的である根拠を補強しています。この機序的推論は、複数の完了済み RCT・メタ解析・国際ガイドラインによって臨床的に裏付けられています。

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT04574713](https://clinicaltrials.gov/study/NCT04574713) | Phase 2 | 完了 | 450 | 多施設・三盲・安慰剤対照 RCT。カンデサルタン 8 mg および 16 mg の反復性偏頭痛予防効果を検証；結果は Lancet Neurology（PMID 40975098）に発表済み |
| [NCT00884663](https://clinicaltrials.gov/study/NCT00884663) | Phase 2/3 | 完了 | 72 | 二重盲検・安慰剤対照・二重ダミー・三重クロスオーバー試験。カンデサルタン vs プロプラノロールの偏頭痛予防効果を直接比較 |
| [NCT04138316](https://clinicaltrials.gov/study/NCT04138316) | 非該当 | 完了 | 85 | CandeSpartan 観察研究。3 剤以上の予防薬が無効だった反復性・慢性偏頭痛患者における反応予測因子と耐用性を評価 |
| [NCT04989413](https://clinicaltrials.gov/study/NCT04989413) | Phase 2/3 | 中止 | 110 | CBD + CBG + THC 補助療法の慢性偏頭痛試験（主要薬物はカンデサルタンでなく中止）；偏頭痛集団の背景情報として参照 |

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [40975098](https://pubmed.ncbi.nlm.nih.gov/40975098/) | 2025 | RCT | The Lancet Neurology | カンデサルタン vs プラセボ（Phase 2 RCT, n=450）：反復性偏頭痛予防における有効性・安全性・耐用性を評価 |
| [38057728](https://pubmed.ncbi.nlm.nih.gov/38057728/) | 2023 | Meta-analysis | Journal of Headache and Pain | 慢性偏頭痛予防薬のネットワークメタ解析；各薬剤の有効性ランキングを比較 |
| [37350141](https://pubmed.ncbi.nlm.nih.gov/37350141/) | 2023 | Meta-analysis | Cephalalgia | 降圧薬の反復性偏頭痛予防効果に関するシステマティックレビューとメタ解析；ARB クラスの有効性を検討 |
| [22529202](https://pubmed.ncbi.nlm.nih.gov/22529202/) | 2012 | Review | Neurology | AAN/AHS 偏頭痛予防薬物療法ガイドライン改訂版；エビデンスに基づく推奨薬物を体系的に評価 |
| [39899861](https://pubmed.ncbi.nlm.nih.gov/39899861/) | 2025 | Review | Annals of Internal Medicine | ACP による外来反復性偏頭痛予防の薬物療法ガイドライン（2025 年版） |
| [22683887](https://pubmed.ncbi.nlm.nih.gov/22683887/) | 2012 | Review | Canadian Journal of Neurological Sciences | カナダ頭痛学会の偏頭痛予防薬ガイドライン；カンデサルタンを含む予防薬の推奨を整理 |
| [38663908](https://pubmed.ncbi.nlm.nih.gov/38663908/) | 2024 | Cohort | Cephalalgia | CandeSpartan 研究：偏頭痛患者 85 名における有効性・耐用性・反応予測因子を評価 |
| [33589682](https://pubmed.ncbi.nlm.nih.gov/33589682/) | 2021 | Cohort | Scientific Reports | 実臨床における偏頭痛へのカンデサルタン有効性と耐用性の後ろ向きコホート研究（2008〜2019 年）；反応予測因子も探索 |
| [40571531](https://pubmed.ncbi.nlm.nih.gov/40571531/) | 2025 | Review | Clinical Therapeutics | カンデサルタンの偏頭痛管理に関するスコーピングレビュー；ARB としての有望性を総括 |
| [35190383](https://pubmed.ncbi.nlm.nih.gov/35190383/) | 2022 | Review | Archives of Disease in Childhood | 小児・若年者の偏頭痛管理最新レビュー；カンデサルタンを含むアンジオテンシン拮抗薬のエビデンスを含む |

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
偏頭痛予防に対するカンデサルタンの有効性を支持する複数の完了済み RCT（最大規模は Phase 2、n=450 の Lancet Neurology 掲載試験）、複数のメタ解析、および国際ガイドライン（AAN、ACP、カナダ頭痛学会）が存在し、エビデンスレベルは L1 に達しています。ただし日本 PMDA における承認実績がなく、安全性・禁忌の詳細データ取得が先決です。

**進める場合に必要なもの：**
- PMDA 仿単（添付文書）の取得・解析による警告・禁忌・薬物相互作用の確認（Data Gap DG001）
- DrugBank API からの詳細 MOA データ取得（Data Gap DG002）
- 日本・アジア人集団における有効性・安全性データの確認
- 最適用量（8 mg vs 16 mg）の検討：NCT04574713 の詳細結果参照
- 既存偏頭痛予防薬（プロプラノロール、トピラマート、CGRP 抗体等）との治療上の位置付け整理
- 日本での薬事承認戦略の策定（新規適応症申請 vs 既存 ARB 製品への適応追加）
---

