---
layout: default
title: Clomipramine
parent: 高エビデンスレベル
nav_order: 74
evidence_level: L2
indication_count: 10
last_modified_at: 2026-10-15
description: "Clomipramine：予測新適応症は不安障害 (Anxiety Disorder)（エビデンスレベル L2）。既存適応症：強迫性障害 (OCD)"
monitor_inn: "Clomipramine"
predicted_indications: ["anxiety disorder", "benign paroxysmal torticollis of infancy", "schizoid personality disorder", "histrionic personality disorder (disease)", "schizotypal personality disorder", "paranoid personality disorder", "agoraphobia", "major depressive disorder", "endogenous depression", "attention deficit-hyperactivity disorder"]
---

# Clomipramine
{: .fs-9 }

エビデンスレベル: **L2** | 予測適応症: **10** 件
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

# クロミプラミン：強迫性障害から不安障害へ

## 一言要約

クロミプラミンは三環系抗うつ薬で、元々強迫性障害 (OCD) の治療に使われていました。
TxGNN モデルは**不安障害 (Anxiety Disorder)** に有効である可能性を予測しており、現在 **8 件の臨床試験**と **20 編の文献**がこの方向性に関連しています。ただし、臨床試験の多くは OCD を対象とした間接的な根拠です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 強迫性障害 (OCD) |
| 予測新規適応症 | 不安障害 (Anxiety Disorder) |
| TxGNN 予測スコア | 99.93% |
| エビデンスレベル | L2 |
| 日本市販状況 | 承認は全て取消済み（現在市販なし） |
| 承認番号数 | 3 件（すべて取消） |
| 推奨決定 | Proceed with Guardrails |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。一般的な薬理学的知見によると、クロミプラミンは強力なセロトニン再取り込み阻害薬です。活性代謝物のデスメチルクロミプラミンはノルアドレナリン再取り込みも阻害します。

OCD は不安スペクトラムの疾患と位置づけられることが多く、セロトニン系の調節はパニックや不安症状にも関連します。

文献では、パニック障害や広場恐怖でクロミプラミンの有効性を示す比較試験や、ネットワークメタアナリシスが報告されています。そのため、不安障害への機序的な適用可能性は高いと考えられます。

## 臨床試験エビデンス

不安障害そのものを直接検証した試験はなく、多くは OCD を対象とした試験です。

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT00466609](https://clinicaltrials.gov/study/NCT00466609) | Phase 4 | 完了 | 54 | 一次治療無効の OCD で、フルオキセチンへのクエチアピンまたはクロミプラミン併用を比較 |
| [NCT00564564](https://clinicaltrials.gov/study/NCT00564564) | Phase 4 | 完了 | 21 | SSRI 無効の OCD で、クエチアピン併用とクロミプラミン併用を比較 |
| [NCT00004310](https://clinicaltrials.gov/study/NCT00004310) | Phase 2 | 不明 | 76 | OCD における静注と経口のクロミプラミン負荷投与を比較 |
| [NCT00074815](https://clinicaltrials.gov/study/NCT00074815) | Phase 3 | 完了 | 124 | SRI 部分反応の小児 OCD に対する認知行動療法の上乗せ効果 |
| [NCT05737511](https://clinicaltrials.gov/study/NCT05737511) | Phase 4 | 募集前 | 80 | パニック障害でヒドロキシジンを通常治療と比較（クロミプラミンは通常治療の一部の可能性） |
| [NCT01404871](https://clinicaltrials.gov/study/NCT01404871) | 該当なし | 完了 | 26 | OCD でクロミプラミンまたはエスシタロプラムへの反応予測因子を検討 |
| [NCT00254735](https://clinicaltrials.gov/study/NCT00254735) | Phase 3 | 完了 | 44 | 重症 OCD でクエチアピン上乗せを検討（SSRI/クロミプラミンのベース治療） |
| [NCT02374567](https://clinicaltrials.gov/study/NCT02374567) | Phase 3 | 中止 | 407 | 高齢精神科入院患者における薬物療法の安全性・副作用調査 |

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [38014714](https://pubmed.ncbi.nlm.nih.gov/38014714/) | 2023 | メタアナリシス | Cochrane Database Syst Rev | 成人パニック障害の薬物療法のネットワークメタアナリシス |
| [40788541](https://pubmed.ncbi.nlm.nih.gov/40788541/) | 2026 | メタアナリシス | Eur Arch Psychiatry Clin Neurosci | 不安障害に対する抗不安薬の有効性と受容性の比較 |
| [40946318](https://pubmed.ncbi.nlm.nih.gov/40946318/) | 2026 | システマティックレビュー | Psychother Psychosom | 治療抵抗性不安障害の薬物・心理・神経刺激治療 |
| [6373161](https://pubmed.ncbi.nlm.nih.gov/6373161/) | 1984 | RCT | Curr Med Res Opin | 広場恐怖・社交恐怖でクロミプラミンとジアゼパムを比較 |
| [22290995](https://pubmed.ncbi.nlm.nih.gov/22290995/) | 1993 | RCT | J Psychopharmacol | パニック障害・広場恐怖でイミプラミン、クロミプラミン、実薬プラセボを比較し、精神運動・認知への影響を評価 |
| [35900217](https://pubmed.ncbi.nlm.nih.gov/35900217/) | 2023 | ガイドライン/レビュー | World J Biol Psychiatry | 不安障害・OCD・PTSD の薬物治療ガイドライン (WFSBP) |
| [2178909](https://pubmed.ncbi.nlm.nih.gov/2178909/) | 1990 | レビュー | Drugs | OCD とパニック障害でのクロミプラミンの薬理と治療的使用 |
| [9707160](https://pubmed.ncbi.nlm.nih.gov/9707160/) | 1998 | レビュー | J Clin Psychiatry | パニック障害の薬物療法における有効性の違い（クロミプラミンを含む） |
| [18849910](https://pubmed.ncbi.nlm.nih.gov/18849910/) | 2008 | レビュー | CNS Spectrums | OCD と不安の薬物治療。クロミプラミンは有効だが有害事象が多い |
| [11801290](https://pubmed.ncbi.nlm.nih.gov/11801290/) | 2001 | レビュー | Neurosci Biobehav Rev | パニック発作の動物モデルで、クロミプラミン慢性投与の効果を検討 |

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 611170027 | アナフラニール錠10mg | 錠 10mg | （取消済み） |
| 611170028 | アナフラニール錠25mg | 錠 25mg | （取消済み） |
| 620007173 | アナフラニール点滴静注液25mg | 注液 25mg | （取消済み） |

3 件はいずれも承認取消の状態で、現在有効な承認はありません。

## 安全性に関する考慮事項

- **禁忌に関連する疾患（知識グラフ上の情報、添付文書の記載ではありません）**：てんかん、躁病性双極性障害、肝疾患、胆嚢疾患、物質乱用・依存、悪性高熱症、褐色細胞腫、緑内障、甲状腺機能亢進症（バセドウ病を含む）、神経芽腫など。
- **薬物相互作用**：計 100 件が確認されています。主なものは次のとおりです。
  - 重大 (Major)：エピネフリン、ブプロピオン、ロルカセリン、クエン酸カリウム、シサプリド
  - 中等度 (Moderate)：ファモチジン、シメチジン、クラリスロマイシン、モルヒネ、アセチルサリチル酸、抗コリン薬（アトロピン、ヒヨスチアミンなど）

そのほかの警告・禁忌については添付文書を参照してください。

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
パニック障害・広場恐怖でクロミプラミンを検証した RCT とメタアナリシスがあり、不安障害への有効性を支持するエビデンスは比較的充実しています。一方、日本では承認が取消されており、安全性の公式情報も未整備です。そのため、条件を付けて慎重に進めるべきです。

**進める場合に必要なもの：**
- 添付文書の警告・禁忌の取得と確認（現時点で最優先の不足データ）
- 詳細な作用機序データ（MOA）の補充
- 不安障害を直接対象としたクロミプラミンの臨床試験の確認
- 日本での承認取消の経緯と、再導入の可否の確認
- 相互作用（重大レベルの併用薬）、てんかん・心疾患・高齢者などのリスク集団に対する安全性モニタリング計画
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

