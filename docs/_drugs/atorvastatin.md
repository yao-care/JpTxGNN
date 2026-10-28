---
layout: default
title: Atorvastatin
parent: 高エビデンスレベル
nav_order: 41
evidence_level: L2
indication_count: 4
monitor_inn: "Atorvastatin"
predicted_indications: ["HIV infectious disease", "brain stem infarction", "cholesterol-ester transfer protein deficiency", "neurodevelopmental disorder with ataxic gait, absent speech, and decreased cortical white matter"]
last_modified_at: 2026-10-27
description: "Atorvastatin：予測新適応症はHIV感染症 (HIV infectious disease)（エビデンスレベル L2）。既存適応症：日本の承認情報に適応症の記載なし"
---

# Atorvastatin
{: .fs-9 }

エビデンスレベル: **L2** | 予測適応症: **4** 件
{: .fs-6 .fw-300 }

---

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist" markdown="1">

## 薬剤師評価レポート

</div>

## アトルバスタチン：HMG-CoA還元酵素阻害薬 → HIV感染症 (HIV infectious disease)
{: .text-alpha }

## 一言要約

アトルバスタチンは、HMG-CoA還元酵素阻害薬（スタチン）として日本で使われてきた薬です。
TxGNN モデルは **HIV感染症 (HIV infectious disease)** に有効である可能性を予測しています。
今回まとめたデータでは、**14 件の臨床試験**と **20 編の文献**が関連しています。ただし、いずれも小規模な試験が中心です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | HIV感染症 (HIV infectious disease) |
| TxGNN 予測スコア | 0.9931 |
| エビデンスレベル | L2 |
| 日本市販状況 | 販売中（有効な承認 20 件以上） |
| 承認番号数 | 20 件以上 |
| 推奨決定 | Proceed with Guardrails |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。既知の情報によると、スタチンは LDL コレステロールを下げるだけでなく、単球・マクロファージの活性化を抑えるなど、抗炎症的な作用を持つことが知られています。

HIV 感染症では、抗レトロウイルス療法（特にプロテアーゼ阻害薬）による脂質異常と、治療後も続く慢性的な免疫活性化・炎症が問題になります。スタチンは、この二つに働きかける可能性があります。実際に、脂質管理と免疫活性化の抑制を目的とした試験が複数行われています。

ただし、スタチン自体に確立した抗ウイルス作用はありません。また、プロテアーゼ阻害薬との間に強い CYP3A4 相互作用があるため、用量には注意が必要です。

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT01766076](https://clinicaltrials.gov/study/NCT01766076) | Phase 3 | 完了 | 30 | ART 反応が不十分な成人へのアトルバスタチン補助療法の RCT。免疫活性化の変化を評価 |
| [NCT00367458](https://clinicaltrials.gov/study/NCT00367458) | Phase 2 | 完了 | 24 | 抗レトロウイルス薬未使用の HIV 陽性者での、プラセボ対照 RCT。ウイルス量と免疫活性化マーカーへの影響を検討 |
| [NCT00663234](https://clinicaltrials.gov/study/NCT00663234) | Phase 1/2 | 中止 | 28 | HIV 感染小児・青年のプロテアーゼ阻害薬関連高 LDL コレステロールに対する安全性と有効性の検討 |
| [NCT03037372](https://clinicaltrials.gov/study/NCT03037372) | Phase 3 | 不明 | 320 | サブサハラアフリカの ART 治療中成人で、アトルバスタチンとロスバスタチンの免疫活性化・炎症抑制効果の同等性を検証 |
| [NCT02081638](https://clinicaltrials.gov/study/NCT02081638) | Phase 2 | 完了 | 53 | エリートコントローラーおよび ART 治療中の HIV 陽性者で、スタチンとアスピリンの炎症・凝固への影響を比較 |
| [NCT01600170](https://clinicaltrials.gov/study/NCT01600170) | Phase 4 | 完了 | 11 | HIV 関連神経認知障害に対し、スタチンによる単球・マクロファージ活性化の抑制を検討 |
| [NCT01263938](https://clinicaltrials.gov/study/NCT01263938) | Phase 4 | 完了 | 5 | ART 治療中の HIV 感染者における単球活性化へのアトルバスタチンの影響を調べたパイロット試験 |
| [NCT00355251](https://clinicaltrials.gov/study/NCT00355251) | Phase 4 | 中止 | 5 | ART 中断前のアトルバスタチンがウイルス複製に与える影響を検討。早期終了のため情報は乏しい |
| [NCT00965185](https://clinicaltrials.gov/study/NCT00965185) | 該当なし | 完了 | 40 | HIV 患者でのスタチン療法による、プラーク炎症と動脈硬化の改善を検討 |
| [NCT00017758](https://clinicaltrials.gov/study/NCT00017758) | Phase 1 | 完了 | 56 | エファビレンツ・ネルフィナビルがスタチンの血中濃度に与える影響を調べた薬物動態試験（安全性情報） |

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [37450602](https://pubmed.ncbi.nlm.nih.gov/37450602/) | 2023 | RCT | AIDS | エリートコントローラーと ART 治療中の HIV 陽性者で、アトルバスタチンとアスピリンを比較した非盲検 RCT。残存炎症の抑制を狙う |
| [18991624](https://pubmed.ncbi.nlm.nih.gov/18991624/) | 2008 | RCT | Current HIV Research | プロテアーゼ阻害薬使用中の HIV 感染者の高コレステロール血症に対し、ロスバスタチン、プラバスタチン、アトルバスタチンを比較した非盲検ランダム化試験 |
| [26851703](https://pubmed.ncbi.nlm.nih.gov/26851703/) | 2016 | メタ解析 | European Heart Journal | HIV 陽性者 736 例（18 研究）で、一次予防におけるスタチンの有効性と安全性を比較 |
| [25907504](https://pubmed.ncbi.nlm.nih.gov/25907504/) | 2015 | システマティックレビュー | American Journal of Cardiology | HIV 感染者に対するスタチン療法の有用性を整理 |
| [29804227](https://pubmed.ncbi.nlm.nih.gov/29804227/) | 2018 | Review | Current Infectious Disease Reports | ART 中の HIV 感染者におけるスタチンの心血管リスク低減効果と安全性 |
| [26658651](https://pubmed.ncbi.nlm.nih.gov/26658651/) | 2016 | Review | Current Opinion in Infectious Diseases | 治療中の HIV 感染でスタチンが心血管アウトカムを改善するかを検証 |
| [31126301](https://pubmed.ncbi.nlm.nih.gov/31126301/) | 2019 | コホート／レビュー | AIDS Research and Therapy | HIV 陽性者の心血管疾患予防におけるスタチンとアスピリンの役割と課題 |
| [29770749](https://pubmed.ncbi.nlm.nih.gov/29770749/) | 2018 | コホート | HIV Clinical Trials | 慢性腎臓病と脂質異常症を併発した HIV-1 感染者で、ロスバスタチンとアトルバスタチンが腎機能を維持するか検討 |
| [22770622](https://pubmed.ncbi.nlm.nih.gov/22770622/) | 2012 | Review | Expert Opinion on Pharmacotherapy | HIV に伴う脂質異常症に対するスタチンの安全性と有効性 |
| [41774493](https://pubmed.ncbi.nlm.nih.gov/41774493/) | 2026 | 動物実験 | JCI Insight | HIV／抗レトロウイルス薬で誘発されるマウスの心臓線維化・機能障害を、アトルバスタチンが血小板 TGF-β1 シグナルの遮断により抑制 |

## 日本市販情報

日本では複数のアトルバスタチン製剤が市販されており、経口の錠剤が中心です。

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用は合計 100 件が記録されています。主なものは次のとおりです。
  - **重大（Major）**：クラリスロマイシン
  - **中等度（Moderate）**：オメプラゾール、シメチジン、デキサメタゾン、メトロニダゾール、ロスバスタチン、シンバスタチンなど
- **抗 HIV 薬との併用**：プロテアーゼ阻害薬は CYP3A4 を強く阻害します。アトルバスタチンの血中濃度が上がるおそれがあるため、併用時は用量に注意が必要です。筋障害（横紋筋融解症など）のリスクも考慮してください。

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
HIV 陽性者を対象に、完了した Phase 3 RCT と Phase 2 のプラセボ対照 RCT が各 1 件あり、免疫活性化や脂質管理への関与が検討されています。ただし、いずれも被験者数が少なく、抗ウイルス効果は確立していません。そのため、研究段階として慎重に進めるのが妥当です。

**進める場合に必要なもの：**
- 免疫活性化・炎症マーカーに対する効果を、より大規模な試験（例：NCT03037372 の結果）で確認すること
- プロテアーゼ阻害薬など抗 HIV 薬との併用に関する、用量設定と安全性モニタリング計画
- 添付文書の警告・禁忌の確認（今回のデータでは取得できていません）
- 詳細な作用機序データの補充
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：リピトール

**販売名（規格別）**：アトルバスタチンOD錠10mg、アトルバスタチンOD錠5mg、アトルバスタチンカルシウム10mg錠、アトルバスタチンカルシウム5mg口腔内崩壊錠、アトルバスタチンカルシウム5mg錠、アトルバスタチン錠10mg、アトルバスタチン錠5mg、リピトール錠10mg、リピトール錠5mg

**配合剤（この成分を含む）**：アトーゼット配合錠HD、アトーゼット配合錠LD、アマルエット配合錠1番、アマルエット配合錠2番、アマルエット配合錠3番、アマルエット配合錠4番、アムロジピンベシル酸塩・アトルバスタチンカルシウム2番錠、アムロジピンベシル酸塩・アトルバスタチンカルシウム3番錠、アムロジピンベシル酸塩・アトルバスタチンカルシウム4番錠、エゼアト配合錠HD、エゼアト配合錠LD、カデュエット配合錠1番、カデュエット配合錠2番、カデュエット配合錠3番、カデュエット配合錠4番
<!-- brand-names:end -->

