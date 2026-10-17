---
layout: default
title: Atorvastatin
parent: 高エビデンスレベル
nav_order: 33
evidence_level: L1
indication_count: 10
last_modified_at: 2026-10-17
description: "Atorvastatin：予測新適応症は家族性高コレステロール血症 (Familial Hypercholesterolemia)（エビデンスレベル L1）。既存適応症：脂質異常症治療薬、HMG-CoA 還元酵素阻害薬"
monitor_inn: "Atorvastatin"
predicted_indications: ["HIV infectious disease", "brain stem infarction", "cholesterol-ester transfer protein deficiency", "hypercholesterolemia due to cholesterol 7alpha-hydroxylase deficiency", "neurodevelopmental disorder with ataxic gait, absent speech, and decreased cortical white matter", "hypoalphalipoproteinemia", "hypercholesterolemia, autosomal dominant", "feline acquired immunodeficiency syndrome", "simian immunodeficiency virus infection"]
---

# Atorvastatin
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

# アトルバスタチン：脂質異常症から家族性高コレステロール血症へ

## 一言要約

アトルバスタチンは HMG-CoA 還元酵素阻害薬（スタチン）で、元々脂質異常症の治療に使用されていました。
TxGNN モデルは**家族性高コレステロール血症 (Familial Hypercholesterolemia)** に有効である可能性を予測しており、予測スコアは 99.42% です。
このデータでは **13 件の臨床試験**と **20 編の文献**が確認されています。ただし、この適応症は薬の本来の作用機序とほぼ重なるため、「新規」というより適応症の近縁拡張と見るのが妥当です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 脂質異常症治療薬、HMG-CoA 還元酵素阻害薬 |
| 予測新規適応症 | 家族性高コレステロール血症 (Familial Hypercholesterolemia) |
| TxGNN 予測スコア | 99.42% |
| エビデンスレベル | L1 |
| 日本市販状況 | 承認は全て整理済み（現在有効な承認なし） |
| 承認番号数 | 20 件（全て整理済み） |
| 推奨決定 | Proceed with Guardrails |

## この予測が妥当である理由

現在、詳細な作用機序データは、このレポートの元データには含まれていません。既知の情報によると、アトルバスタチンは HMG-CoA 還元酵素を阻害して肝臓の LDL 受容体を増やし、LDL コレステロール（LDL-C）を下げる薬です。これは脂質異常症治療の中核となる機序です。

家族性高コレステロール血症（FH）は LDL 受容体の機能低下による LDL-C 上昇を特徴とします。アトルバスタチンはこの経路を介して LDL-C を下げるため、機序的に適用可能であり、実質的には既存適応症に近い位置づけです。

なお、予測上位には HIV 感染症（スコア 99.31%）もあります。こちらは抗ウイルス作用が確立しておらず、炎症や ART 関連脂質異常への効果を探る段階で、証拠レベルは L2、推奨は「Research Question」です。

## 臨床試験エビデンス

アトルバスタチン自体を試験薬とする試験を優先し、最大 10 件を記載します。

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT00827606](https://clinicaltrials.gov/study/NCT00827606) | Phase 3 | 完了 | 272 | 小児・若年の heFH におけるアトルバスタチンの 3 年間の成長・発達とコレステロール低下効果 |
| [NCT00134485](https://clinicaltrials.gov/study/NCT00134485) | Phase 3 | 完了 | 400 | heFH でトルセトラピブ/アトルバスタチン配合 vs アトルバスタチン単独（トルセトラピブは安全性の問題で開発中止） |
| [NCT00136981](https://clinicaltrials.gov/study/NCT00136981) | Phase 3 | 完了 | 800 | heFH で頸動脈超音波による動脈硬化評価（トルセトラピブ/アトルバスタチン配合 vs アトルバスタチン単独、24 か月） |
| [NCT00134511](https://clinicaltrials.gov/study/NCT00134511) | Phase 3 | 完了 | 30 | ホモ接合体 FH でトルセトラピブ/アトルバスタチンの有効性・安全性（強制増量、非盲検） |
| [NCT00739999](https://clinicaltrials.gov/study/NCT00739999) | Phase 1 | 完了 | 39 | 小児・若年の heFH におけるアトルバスタチンの薬物動態・薬力学・安全性（有効性は評価せず） |
| [NCT03884452](https://clinicaltrials.gov/study/NCT03884452) | Phase 3 | 完了 | 50 | ホモ接合体 FH でエゼチミブをアトルバスタチンまたはシンバスタチンに追加（アトルバスタチンは背景治療） |
| [NCT03885921](https://clinicaltrials.gov/study/NCT03885921) | Phase 3 | 完了 | 44 | 上記試験の長期延長（最長 24 か月）で、エゼチミブ併用の安全性と忍容性を評価 |
| [NCT01709500](https://clinicaltrials.gov/study/NCT01709500) | Phase 3 | 完了 | 249 | heFH でアリロクマブ vs プラセボ（アトルバスタチンは背景治療の可能性） |
| [NCT03510884](https://clinicaltrials.gov/study/NCT03510884) | Phase 3 | 完了 | 153 | 小児・若年の heFH でアリロクマブ vs プラセボ（スタチンは背景治療） |
| [NCT01279590](https://clinicaltrials.gov/study/NCT01279590) | Phase 2 | 完了 | 282 | スタチン関連筋痛の既往がある高コレステロール血症で PPD10558 vs アトルバスタチン |

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [25760954](https://pubmed.ncbi.nlm.nih.gov/25760954/) | 2015 | Review (Cochrane) | Cochrane Database Syst Rev | アトルバスタチンの用量依存的な脂質低下効果を整理 |
| [27678432](https://pubmed.ncbi.nlm.nih.gov/27678432/) | 2016 | 臨床試験 | J Clin Lipidol | 小児・若年 heFH におけるアトルバスタチン 3 年間の有効性と安全性 |
| [27417002](https://pubmed.ncbi.nlm.nih.gov/27417002/) | 2016 | コホート | J Am Coll Cardiol | heFH でのスタチン治療による冠動脈疾患・全死亡の低減 |
| [9666952](https://pubmed.ncbi.nlm.nih.gov/9666952/) | 1998 | コホート | QJM | 重症 heFH 54 例で、アトルバスタチンにより LDL が約 46% 低下 |
| [9301631](https://pubmed.ncbi.nlm.nih.gov/9301631/) | 1997 | 非盲検試験 | Arterioscler Thromb Vasc Biol | FH でアトルバスタチン 80 mg の有効性と安全性（22 例） |
| [11383320](https://pubmed.ncbi.nlm.nih.gov/11383320/) | 2001 | 比較試験 | Nutr Metab Cardiovasc Dis | heFH でアトルバスタチンとシンバスタチンの LDL-C 目標達成を比較 |
| [12883464](https://pubmed.ncbi.nlm.nih.gov/12883464/) | 2003 | 臨床研究 | Med Sci Monit | FH でアトルバスタチンが微量アルブミン尿を減少 |
| [36928267](https://pubmed.ncbi.nlm.nih.gov/36928267/) | 2023 | コホート | J Atheroscler Thromb | 日本の実臨床における高リスク患者の LDL-C 目標達成率 |
| [40254247](https://pubmed.ncbi.nlm.nih.gov/40254247/) | 2025 | 前臨床 | Toxicology | FH 患者由来 iPSC 筋細胞での脂溶性・水溶性スタチンの筋毒性の違い |
| [28437620](https://pubmed.ncbi.nlm.nih.gov/28437620/) | 2017 | ガイドライン | Endocr Pract | AACE/ACE の脂質異常症管理ガイドライン |

## 日本市販情報

現在有効な承認はなく、下記は全て整理済みの承認です。

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 622152101 | アトルバスタチン錠１０ｍｇ「ＺＥ」 | 錠 | 脂質異常症治療薬, HMG-CoA還元酵素阻害薬 |
| 622110501 | アトルバスタチン錠１０ｍｇ「トーワ」 | 錠 | 脂質異常症治療薬, HMG-CoA還元酵素阻害薬 |
| 622167701 | アトルバスタチン錠１０ｍｇ「日医工」 | 錠 | 脂質異常症治療薬, HMG-CoA還元酵素阻害薬 |
| 622921301 | アトルバスタチン錠５ｍｇ「ＶＴＲＳ」 | 錠 | 脂質異常症治療薬, HMG-CoA還元酵素阻害薬 |
| 622465301 | アマルエット配合錠１番「日医工」 | 錠（配合剤） | 記載なし |

## 安全性に関する考慮事項

- **知識グラフ上の禁忌関連疾患**（添付文書の記載ではありません）：肝不全、肝疾患、腎疾患、胆嚢疾患、甲状腺機能低下症、粘液水腫、ミオパチー、筋疾患、横紋筋融解症、低血圧性障害、物質乱用・依存など。
- **薬物相互作用**（計 100 件、主なもの）：
  - 重大（Major）：クラリスロマイシン
  - 中等度（Moderate）：アプレピタント、オメプラゾール、シメチジン、クロトリマゾール、デキサメタゾン、ミコナゾール、メトロニダゾール、ロスバスタチン、シンバスタチンなど
  - 軽微（Minor）：水酸化アルミニウム、水酸化マグネシウム、リラグルチド
- HIV 治療で用いるプロテアーゼ阻害薬は CYP3A4 を強く阻害するため、併用時は用量に注意が必要です。

警告および禁忌の詳細は添付文書で確認してください。

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
- FH に対するアトルバスタチンの有効性は、複数の Phase 3 試験と多数の文献で支持されており、機序的にも本来の作用そのものです。
- ただし日本では現在、有効な承認が全て整理済みで、添付文書の警告・禁忌データも未取得です。

**進める場合に必要なもの：**
- 添付文書（PMDA）の警告・禁忌情報の取得（ブロッキング課題）
- 詳細な作用機序データ（DrugBank）の補完
- 日本での現行の販売・承認状況の再確認（整理済みの承認が多いため）
- 小児や CYP3A4 阻害薬併用患者など、特定集団の安全性モニタリング計画
- HIV など他の予測適応症は L2 以下のため、別途検証が必要
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

