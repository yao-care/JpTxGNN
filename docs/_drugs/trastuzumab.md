---
layout: default
title: Trastuzumab
parent: モデル予測のみ
nav_order: 321
evidence_level: L5
indication_count: 10
monitor_inn: "Trastuzumab"
predicted_indications: ["normal breast-like subtype of breast carcinoma", "progesterone-receptor positive breast cancer", "progesterone-receptor negative breast cancer", "breast tumor luminal A or B", "malignant cutaneous granular cell skin tumor", "ectomesenchymoma", "human herpesvirus 8-related tumor", "middle ear neuroendocrine tumor", "kidney pelvis sarcomatoid transitional cell carcinoma", "prostatic urethra urothelial carcinoma"]
last_modified_at: 2026-10-17
description: "Trastuzumab：予測新適応症はプロゲステロン受容体陽性乳癌 (progesterone-receptor positive breast cancer)（エビデンスレベル L5）。既存適応症：HER2 陽性乳癌"
---

# Trastuzumab
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **10** 件
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

# トラスツズマブ：HER2 陽性乳癌から プロゲステロン受容体陽性乳癌 へ

## 一言要約

トラスツズマブは抗 HER2 モノクローナル抗体で、元々 HER2 陽性乳癌の治療に使用されていました。
TxGNN モデルは**プロゲステロン受容体陽性乳癌 (progesterone-receptor positive breast cancer)** に有効である可能性を予測しており、現在 **13 件の臨床試験**と **20 編の文献**がこの方向性に関連しています。
ただし、これは HER2 陽性かつ PR 陽性のサブグループに限られると考えられ、HER2 陰性の腫瘍には効果が期待できません。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | HER2 陽性乳癌 |
| 予測新規適応症 | プロゲステロン受容体陽性乳癌 (progesterone-receptor positive breast cancer) |
| TxGNN 予測スコア | 99.90% |
| エビデンスレベル | L1（完了した Phase 3 RCT が 2 件以上：NCT01275677、NCT04629846） |
| 日本市販状況 | 承認は取り消し済み（現在市販中の承認なし） |
| 承認番号数 | 2 件（いずれも取消） |
| 推奨決定 | Proceed with Guardrails |

> 補足：データ上のエビデンスレベル判定は L2 ですが、完了した Phase 3 試験が 2 件あるため、本レポートの判定ルールでは L1 に該当します。ただし NCT04629846 は主にペルツズマブのバイオシミラー比較試験であり、NCT01275677 は HER2 低発現乳癌が対象です。トラスツズマブそのものの PR 陽性乳癌への効果を直接示す試験とは言い切れないため、解釈には注意が必要です。

## この予測が妥当である理由

現在、詳細な作用機序データはありません。既知の情報によると、トラスツズマブは HER2 の細胞外ドメインに結合するヒト化抗体です。HER2 を介した PI3K/AKT や MAPK のシグナルを阻害し、抗体依存性細胞傷害 (ADCC) も誘導します。

乳癌の約 5〜10% は ER 陽性・PR 陽性・HER2 陽性のトリプルポジティブです。このサブグループでは、HER2 経路とホルモン受容体経路の相互作用があるため、トラスツズマブに内分泌療法や CDK4/6 阻害薬を併用する治療が研究されています。そのため、機序的には PR 陽性乳癌のうち **HER2 陽性の症例**に適用できる可能性があります。

一方、PR 陽性であっても HER2 陰性の腫瘍（ルミナル A 型など）には効果が期待できません。HER2 の状態が使用の前提条件になります。

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT01275677](https://clinicaltrials.gov/study/NCT01275677) | Phase 3 | 完了 | 3270 | HER2 低発現の浸潤性乳癌における術後化学療法へのトラスツズマブ上乗せの比較 |
| [NCT04629846](https://clinicaltrials.gov/study/NCT04629846) | Phase 3 | 完了 | 517 | HER2 陽性・ER/PR 陰性乳癌で QL1209（ペルツズマブ）とトラスツズマブ＋ドセタキセルを併用した比較 |
| [NCT00053339](https://clinicaltrials.gov/study/NCT00053339) | Phase 3 | 中止（取下げ） | 0 | ER/PR 陽性・HER2 陽性の進行乳癌でトラスツズマブ±タモキシフェンを比較する計画。登録なしのためデータなし |
| [NCT02260531](https://clinicaltrials.gov/study/NCT02260531) | Phase 2 | 完了 | 36 | 脳転移を有する乳癌でカボザンチニブ単独またはトラスツズマブ併用 |
| [NCT01750073](https://clinicaltrials.gov/study/NCT01750073) | Phase 2 | 完了 | 92 | 乳癌における術前化学療法へのトラスツズマブ上乗せの検討 |
| [NCT00134680](https://clinicaltrials.gov/study/NCT00134680) | Phase 2 | 完了 | 33 | ER/PR 陽性・HER2 陽性の転移性乳癌でレトロゾール＋トラスツズマブ |
| [NCT04334330](https://clinicaltrials.gov/study/NCT04334330) | Phase 2 | 不明 | 34 | ER/PR 陽性・HER2 陽性で脳転移を有する乳癌におけるパルボシクリブ・トラスツズマブ・ピロチニブ・フルベストラント併用 |
| [NCT04886531](https://clinicaltrials.gov/study/NCT04886531) | Phase 2 | 募集中 | 30 | ER 陽性・HER2 陽性乳癌における術前ネラチニブ＋内分泌療法＋トラスツズマブ |
| [NCT02152943](https://clinicaltrials.gov/study/NCT02152943) | Phase 1 | 完了 | 37 | ホルモン受容体陽性・HER2 陽性の進行乳癌でエベロリムス・レトロゾール・トラスツズマブ併用 |
| [NCT00194779](https://clinicaltrials.gov/study/NCT00194779) | Phase 2 | 完了 | 50 | HER2 陽性乳癌における術前化学療法（ドキソルビシン、シクロホスファミド、パクリタキセル）。トラスツズマブの関与は確認できない |

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [16236738](https://pubmed.ncbi.nlm.nih.gov/16236738/) | 2005 | RCT | N Engl J Med | 手術可能な HER2 陽性乳癌で、術後化学療法にトラスツズマブを併用した 2 試験の統合解析 |
| [32353342](https://pubmed.ncbi.nlm.nih.gov/32353342/) | 2020 | RCT | Lancet Oncol | ホルモン受容体陽性・HER2 陽性の進行乳癌で、アベマシクリブ＋トラスツズマブ（±フルベストラント）と標準化学療法＋トラスツズマブを比較（monarcHER） |
| [27179402](https://pubmed.ncbi.nlm.nih.gov/27179402/) | 2016 | RCT | Lancet Oncol | HER2 陽性乳癌の術前療法におけるペルツズマブ＋トラスツズマブの 5 年成績（NeoSphere） |
| [28945833](https://pubmed.ncbi.nlm.nih.gov/28945833/) | 2017 | RCT | Ann Oncol | HER2 陽性・HR 陰性早期乳癌で、トラスツズマブ＋ペルツズマブの 12 週間の術前療法を評価（WSG-ADAPT） |
| [41780642](https://pubmed.ncbi.nlm.nih.gov/41780642/) | 2026 | RCT | Ann Oncol | HR 陽性・HER2 低発現/超低発現の転移性乳癌におけるトラスツズマブ デルクステカンの追加解析（DESTINY-Breast06） |
| [31410192](https://pubmed.ncbi.nlm.nih.gov/31410192/) | 2019 | 解析研究 | Theranostics | ER 陽性・PR 陽性・HER2 陽性乳癌の分子特性とトラスツズマブへの反応性 |
| [21151204](https://pubmed.ncbi.nlm.nih.gov/21151204/) | 2011 | Review | Nat Rev Clin Oncol | HER2 陽性かつホルモン受容体陽性乳癌に対する、芳香族化酵素阻害薬と抗 HER2 療法の併用戦略 |
| [39631485](https://pubmed.ncbi.nlm.nih.gov/39631485/) | 2024 | Review | Pharmacol Res | 乳癌に用いる分子標的薬と細胞傷害性薬剤の総説 |
| [35640077](https://pubmed.ncbi.nlm.nih.gov/35640077/) | 2022 | ガイドライン | J Clin Oncol | 進行 HER2 陽性乳癌の全身療法に関する ASCO ガイドライン更新 |
| [17687157](https://pubmed.ncbi.nlm.nih.gov/17687157/) | 2007 | 解析研究 | J Clin Oncol | 術後トラスツズマブ試験における心毒性の経過と可逆性の検討 |

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 | 状態 |
|---------|------|------|-----------|------|
| 629921901 | ハーセプチン注射用60 60mg | 注射剤 | 記載なし | 取消 |
| 629922001 | ハーセプチン注射用150 150mg | 注射剤 | 記載なし | 取消 |

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 分子標的薬（抗 HER2 モノクローナル抗体） |
| 骨髄抑制リスク | 低（単剤では少ない。化学療法との併用時は併用薬の影響を受ける） |
| 催吐性分類 | 低 |
| モニタリング項目 | 心機能（左室駆出率）、CBC、肝腎機能。心毒性は文献でも報告されている |
| 取り扱い防護 | 添付文書の警告および注意事項を参照してください |

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用データが 94 件あります。主なものは次のとおりです。
  - 重大（Major）：デフェリプロン、サマリウム（153Sm）レキシドロナム、アダリムマブ、バリシチニブ
  - 中等度（Moderate）：パクリタキセル、ワルファリン、ジクマロール、ゾルブジン、アレムツズマブ、アナキンラ、アザチオプリンなど
- **心毒性**：文献で、術後トラスツズマブ療法に伴う心毒性が報告されています。

その他の警告・禁忌については、添付文書を参照してください。

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
- HER2 陽性かつ PR 陽性の乳癌では、トラスツズマブ併用の臨床試験と RCT 文献が複数あり、機序的にも妥当です。
- ただし、PR 陽性乳癌全体への一律の適応拡大ではなく、**HER2 陽性症例に限定する**必要があります。日本の承認も現在は取り消されています。

**進める場合に必要なもの：**
- 添付文書の警告・禁忌の確認（現時点では未取得で、安全性評価の前提となる）
- 作用機序データの補完
- 対象を HER2 陽性（IHC 3+ または ISH 陽性）に限定する患者選択基準の設定
- 心機能モニタリング計画の策定
- 日本での承認取消の経緯と、現在入手可能な製剤の確認
- 一部の試験（NCT04629846 など）は他剤が主眼であるため、トラスツズマブ自体の寄与を示すデータの精査

なお、予測順位 2 位以降のうち、乳癌以外の 5〜10 位（皮膚顆粒細胞腫、外胚葉間葉腫、ヒトヘルペスウイルス 8 関連腫瘍、中耳神経内分泌腫瘍、腎盂・前立腺部尿道の尿路上皮癌など）は臨床試験も文献もなく、モデル予測のみ（L5）のため **Hold** が妥当です。
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---


<!-- brand-names:start -->
## 日本の主な販売名

以下の販売名・製品名でも検索できます（成分は同じです）。

ハーセプチン、ハーセプチン注射用150 150mg、ハーセプチン注射用60 60mg
<!-- brand-names:end -->

