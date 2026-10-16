---
layout: default
title: Vilanterol
parent: 高エビデンスレベル
nav_order: 336
evidence_level: L1
indication_count: 10
last_modified_at: 2026-10-15
description: "Vilanterol：予測新適応症は閉塞性肺疾患 (Obstructive Lung Disease)（エビデンスレベル L1）。既存適応症：慢性閉塞性肺疾患、喘息、気管支炎、肺気腫"
monitor_inn: "Vilanterol"
predicted_indications: ["obstructive lung disease", "hyperlucent lung", "compensatory emphysema", "interstitial emphysema", "tracheal stenosis", "bronchial neoplasm (disease)", "congenital lobar emphysema", "respiratory malformation", "tracheal calcification", "laryngotracheitis"]
---

# Vilanterol
{: .fs-9 }

エビデンスレベル: **L1** | 予測適応症: **10** 件
{: .fs-6 .fw-300 }

---

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist">

## 薬剤師評価レポート

</div>

# ビランテロール：慢性閉塞性肺疾患・喘息から閉塞性肺疾患へ

## 一言要約

ビランテロールは長時間作用型β2刺激薬（LABA）で、元々慢性閉塞性肺疾患（COPD）や喘息の治療に使用されていました。
TxGNN モデルは**閉塞性肺疾患 (Obstructive Lung Disease)** に有効である可能性を予測しており、現在 **25 件の臨床試験**と **20 編の文献**がこの方向性を支持しています。
ただし、この予測は既存の適応症とほぼ重なるため、新規の再利用というより既存用途の裏付けに近い内容です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 慢性閉塞性肺疾患、喘息、気管支炎、肺気腫（知識グラフ上の適応症。日本の承認適応症のテキストはデータにありません） |
| 予測新規適応症 | 閉塞性肺疾患 (Obstructive Lung Disease) |
| TxGNN 予測スコア | 99.97% |
| エビデンスレベル | L1 |
| 日本市販状況 | 販売終了のみ（現在有効な承認なし） |
| 承認番号数 | 6 件（すべて取消済み） |
| 推奨決定 | Proceed with Guardrails |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。既知の情報によると、ビランテロールは吸入ステロイド（フルチカゾンフランカルボン酸エステル）やウメクリジニウムとの配合剤として使われる長時間作用型β2刺激薬です。気道平滑筋のβ2受容体を介して cAMP を増加させ、気管支拡張を起こすと考えられています。

COPD や喘息はいずれも気流閉塞を特徴とする疾患で、「閉塞性肺疾患」はこれらを含む上位概念です。そのため、予測は機序的に自然です。

一方で、この予測は既に知られている COPD・喘息への用途と重なっています。新しい適応症の発見というより、既存の用途をモデルが再確認したものと捉えるのが適切です。

## 臨床試験エビデンス

関連性の高い試験を 10 件掲載します。

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT03162055](https://clinicaltrials.gov/study/NCT03162055) | Phase 3 | 完了 | 1119 | 中等症〜最重症 COPD で、グリコピロニウム/ホルモテロール配合剤とウメクリジニウム/ビランテロール配合剤を 24 週間比較 |
| [NCT02094937](https://clinicaltrials.gov/study/NCT02094937) | Phase 3 | 完了 | 430 | 日本人の喘息患者で、FF/VI 維持療法からのステップダウン時の FF の有効性と安全性を検討 |
| [NCT01134042](https://clinicaltrials.gov/study/NCT01134042) | Phase 3 | 完了 | 587 | 持続型喘息で、FF/VI と FF 単剤、フルチカゾンプロピオン酸エステルを 24 週間比較 |
| [NCT01686633](https://clinicaltrials.gov/study/NCT01686633) | Phase 3 | 完了 | 1040 | 中等症〜重症の持続型喘息で、FF/VI 200/25 と 100/25 を FF 単剤と比較 |
| [NCT01342913](https://clinicaltrials.gov/study/NCT01342913) | Phase 3 | 完了 | 528 | COPD で、FF/VI 1 日 1 回とサルメテロール/フルチカゾン 1 日 2 回の 24 時間肺機能を比較 |
| [NCT01323621](https://clinicaltrials.gov/study/NCT01323621) | Phase 3 | 完了 | 512 | COPD で、FF/VI 100/25 とフルチカゾン/サルメテロール 250/50 の 24 時間肺機能を比較 |
| [NCT01777334](https://clinicaltrials.gov/study/NCT01777334) | Phase 3 | 完了 | 905 | COPD で、ウメクリジニウム/ビランテロールとチオトロピウムを 24 週間比較 |
| [NCT01706198](https://clinicaltrials.gov/study/NCT01706198) | Phase 3 | 完了 | 4233 | 喘息で、FF/VI と通常の維持療法を 12 か月間比較する実臨床型試験 |
| [NCT02301975](https://clinicaltrials.gov/study/NCT02301975) | Phase 3 | 完了 | 1526 | 喘息で、FF/VI 1 日 1 回と ICS/LABA 1 日 2 回を比較する非劣性試験 |
| [NCT05062304](https://clinicaltrials.gov/study/NCT05062304) | N/A | 完了 | 17281 | COPD で、FF/ウメクリジニウム/ビランテロールの 3 剤併用と 2 剤併用を比較（IMPACT 試験の再現） |

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [29668352](https://pubmed.ncbi.nlm.nih.gov/29668352/) | 2018 | RCT | N Engl J Med | COPD で、1 日 1 回の 3 剤併用吸入療法と 2 剤併用療法を比較（IMPACT 試験） |
| [28375647](https://pubmed.ncbi.nlm.nih.gov/28375647/) | 2017 | RCT | Am J Respir Crit Care Med | COPD で、1 日 1 回の 3 剤併用療法と ICS/LABA 2 剤併用療法を比較（FULFIL 試験） |
| [32162970](https://pubmed.ncbi.nlm.nih.gov/32162970/) | 2020 | RCT | Am J Respir Crit Care Med | IMPACT 試験の追加解析で、3 剤併用療法による全死亡リスクの低下を報告 |
| [32918892](https://pubmed.ncbi.nlm.nih.gov/32918892/) | 2021 | RCT | Lancet Respir Med | コントロール不十分な喘息で、FF/UMEC/VI と FF/VI を比較（CAPTAIN 試験、Phase 3A） |
| [39797646](https://pubmed.ncbi.nlm.nih.gov/39797646/) | 2024 | Meta-analysis | BMJ | 実臨床の COPD 患者で、2 種類の単一吸入器 3 剤併用療法の有効性と安全性を比較 |
| [35849317](https://pubmed.ncbi.nlm.nih.gov/35849317/) | 2022 | Meta-analysis | Adv Ther | FF/UMEC/VI と他の 3 剤・2 剤併用療法の有効性をネットワークメタ解析で比較 |
| [39696097](https://pubmed.ncbi.nlm.nih.gov/39696097/) | 2024 | Meta-analysis | BMC Pulm Med | ウメクリジニウム/ビランテロールと他の気管支拡張薬の有効性をシステマティックレビューで比較 |
| [28956463](https://pubmed.ncbi.nlm.nih.gov/28956463/) | 2017 | Review | Expert Rev Respir Med | COPD における FF/VI 1 日 1 回併用療法の役割をレビュー |
| [24259654](https://pubmed.ncbi.nlm.nih.gov/24259654/) | 2014 | Review | Ann Pharmacother | COPD の維持療法における FF/VI の有効性と安全性を他の ICS/LABA と比較 |
| [23232038](https://pubmed.ncbi.nlm.nih.gov/23232038/) | 2013 | Cohort | Pulm Pharmacol Ther | 健康被験者で忍容性が良好で、喘息・COPD 患者で持続的な気管支拡張を確認 |

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 622279301 | レルベア２００エリプタ１４吸入用（取消） | 吸入用 | — |
| 622375501 | レルベア１００エリプタ３０吸入用（取消） | 吸入用 | — |
| 622279201 | レルベア１００エリプタ１４吸入用（取消） | 吸入用 | — |
| 622970301 | 小児用レルベア５０エリプタ１４吸入用（取消） | 吸入用 | — |
| 622375601 | レルベア２００エリプタ３０吸入用（取消） | 吸入用 | — |

6 件の承認はすべて取消済みです。上記は主要な 5 件で、残る 1 件は小児用レルベア５０エリプタ３０吸入用（622970401）です。

## 安全性に関する考慮事項

- **薬物相互作用**：100 件の相互作用が登録されています。代表的なものは以下のとおりです。
  - 中等度：
    - 糖尿病治療薬（アカルボース、アルビグルチド、アログリプチン、カナグリフロジン、クロルプロパミド、ダパグリフロジン、ドゥラグルチド、エンパグリフロジン）
    - QT 延長に関わる薬剤（シサプリド、ドラセトロン、クラリスロマイシン）
    - 交感神経刺激薬（エフェドリン、エピネフリン、ジエチルプロピオン）
  - 軽度：吸入・全身ステロイド（ベクロメタゾン、ベタメタゾン、ブデソニド、デキサメタゾン）

詳細な警告・禁忌については添付文書を参照してください。

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
- COPD や喘息に対する Phase 3 の RCT が複数完了しており、有効性のエビデンスは十分です。
- ただし、この予測は既存適応症とほぼ重なっており、新規の再利用ではありません。また、日本の承認はすべて取消済みです。

**進める場合に必要なもの：**
- 添付文書の警告・禁忌の確認（現時点では未取得で、安全性スクリーニングの前提となります）
- 詳細な作用機序データの補充
- 日本での販売状況（承認取消の経緯）と、再承認や代替製剤の可能性の確認
- 糖尿病治療薬、QT 延長薬、交感神経刺激薬との併用に関する安全性モニタリング計画
- 他の予測疾患（過度の肺透過性亢進、気管狭窄など）は、直接のエビデンスがなく機序的根拠も弱いため保留とし、新規適応症としては追わないことを推奨します。
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

