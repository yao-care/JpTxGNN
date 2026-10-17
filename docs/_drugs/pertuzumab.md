---
layout: default
title: Pertuzumab
parent: 高エビデンスレベル
nav_order: 241
evidence_level: L1
indication_count: 10
last_modified_at: 2026-10-17
description: "Pertuzumab：予測新適応症はプロゲステロン受容体陽性乳癌 (Progesterone-receptor positive breast cancer)（エビデンスレベル L1）。既存適応症：HER2 陽性乳癌"
monitor_inn: "Pertuzumab"
predicted_indications: ["ectomesenchymoma", "malignant cutaneous granular cell skin tumor", "human herpesvirus 8-related tumor", "middle ear neuroendocrine tumor", "prostatic urethra urothelial carcinoma", "kidney pelvis sarcomatoid transitional cell carcinoma"]
---

# Pertuzumab
{: .fs-9 }

エビデンスレベル: **L1** | 予測適応症: **10** 件
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

# ペルツズマブ：HER2陽性乳癌から プロゲステロン受容体陽性乳癌 へ

## 一言要約

ペルツズマブは HER2 を標的とする抗体医薬で、元々 HER2 陽性乳癌の治療に使用されていました。
TxGNN モデルは**プロゲステロン受容体陽性乳癌 (Progesterone-receptor positive breast cancer)** に有効である可能性を予測しており、現在 **1 件の臨床試験**と **20 編の文献**がこの方向性に関連しています。ただし、エビデンスは HER2 陽性サブセットに限られます。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | HER2 陽性乳癌 |
| 予測新規適応症 | プロゲステロン受容体陽性乳癌 (Progesterone-receptor positive breast cancer) |
| TxGNN 予測スコア | 99.93% |
| エビデンスレベル | L1 |
| 日本市販状況 | 販売承認は整理済み（現在は市販されていません） |
| 承認番号数 | 1 件（整理済み） |
| 推奨決定 | Proceed with Guardrails |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。既知の情報によると、ペルツズマブは HER2 の細胞外ドメイン II に結合し、HER3 や EGFR とのヘテロ二量体形成を妨げる抗体医薬です。これにより PI3K/AKT や MAPK のシグナルが抑制されると考えられています。

既存適応症の HER2 陽性乳癌と、予測された PR 陽性乳癌は、HER2 陽性かつホルモン受容体陽性（HR+/HER2+）の患者群で重なります。HER2 陽性乳癌の約半数にはホルモン受容体の共発現があるとされています。そのため、この患者群では HER2 阻害が機序的に適用できると考えられます。

ただし、この妥当性は **HER2 陽性サブセットに限られます**。HER2 陰性の PR 陽性乳癌には、機序的な根拠はありません。

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT04629846](https://clinicaltrials.gov/study/NCT04629846) | Phase 3 | 完了 | 517 | HER2 陽性・ER/PR 陰性の早期または局所進行乳癌で、ペルツズマブ後続品 QL1209 と先行品を、トラスツズマブ＋ドセタキセルとの併用で比較したランダム化二重盲検試験。後続品であり、PR 陽性例は対象外のため、間接的な根拠にとどまります。 |

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [42150145](https://pubmed.ncbi.nlm.nih.gov/42150145/) | 2026 | RCT | J Clin Oncol | WSG TP-II 試験の生存解析。HR 陽性/HER2 陽性早期乳癌で、術前のトラスツズマブ＋ペルツズマブ＋内分泌療法と化学療法を比較。 |
| [37166817](https://pubmed.ncbi.nlm.nih.gov/37166817/) | 2023 | RCT | JAMA Oncol | WSG-TP-II 試験。HR 陽性/HER2 陽性早期乳癌で、内分泌療法＋二重 HER2 阻害と減量化学療法を比較。 |
| [27179402](https://pubmed.ncbi.nlm.nih.gov/27179402/) | 2016 | RCT | Lancet Oncol | NeoSphere 試験の 5 年解析。術前ペルツズマブ＋トラスツズマブ＋ドセタキセルの無増悪生存期間、無病生存期間、安全性を報告。 |
| [28945833](https://pubmed.ncbi.nlm.nih.gov/28945833/) | 2017 | RCT | Ann Oncol | WSG-ADAPT HER2+/HR- 試験の最終解析。12 週間の二重阻害（化学療法の有無）を比較。 |
| [38906970](https://pubmed.ncbi.nlm.nih.gov/38906970/) | 2024 | RCT | Br J Cancer | ペルツズマブ後続品 QL1209 と先行品の同等性を示した第 3 相試験。 |
| [27057657](https://pubmed.ncbi.nlm.nih.gov/27057657/) | 2016 | Review | Cancer Treat Rev | HR 陽性/HER2 陽性乳癌の現状と今後の展望。 |
| [40983817](https://pubmed.ncbi.nlm.nih.gov/40983817/) | 2025 | Review | Breast Cancer | HR+/HER2+ 乳癌のシグナル経路の相互作用と臨床応用。 |
| [35640077](https://pubmed.ncbi.nlm.nih.gov/35640077/) | 2022 | Review | J Clin Oncol | 進行 HER2 陽性乳癌の全身療法に関する ASCO ガイドライン更新。 |
| [40076535](https://pubmed.ncbi.nlm.nih.gov/40076535/) | 2025 | Review | Int J Mol Sci | ペルツズマブ＋トラスツズマブ＋ドセタキセルによる術後補助療法のシステマティックレビュー。 |
| [38582875](https://pubmed.ncbi.nlm.nih.gov/38582875/) | 2024 | 後ろ向き研究 | World J Surg Oncol | 中国における術前二重 HER2 阻害＋化学療法の実臨床での有効性と安全性。 |

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 622255101 | パージェタ点滴静注420mg/14mL | 注射剤（420mg/14mL） | 記載なし（承認は整理済み） |

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 分子標的薬（抗 HER2 モノクローナル抗体） |
| 骨髄抑制リスク | 低（単剤での骨髄抑制は主要なリスクではありません。ただし併用する化学療法の影響に注意が必要です） |
| 催吐性分類 | 低 |
| モニタリング項目 | 心機能（左室駆出率）、CBC、肝腎機能。心毒性の評価は、試験文献（TRYPHAENA、BERENICE）でも重視されています。 |
| 取り扱い防護 | 添付文書の警告および注意事項を参照してください |

## 安全性に関する考慮事項

- **薬物相互作用**：イデラリシブとの相互作用が報告されています（重要度：中等度）。

その他の警告・禁忌については、添付文書を参照してください。

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
HR 陽性/HER2 陽性の乳癌では、完了した第 3 相 RCT を含む複数のランダム化試験があり、エビデンスレベルは L1 です。ただし、これらは HER2 陽性サブセットを対象としたものであり、PR 陽性乳癌全体への外挿はできません。

**進める場合に必要なもの：**
- 対象を **HER2 陽性（確定診断済み）の PR 陽性乳癌**に限定すること
- 日本の添付文書（警告・禁忌）の取得と確認（現在は欠落しており、安全性審査の前提となります）
- 詳細な作用機序データ（MOA）の補充
- 日本での販売承認が整理済みであるため、現在の供給状況と再承認の要否の確認
- 心機能モニタリング計画の策定
- PR 陽性サブセットに特化した臨床試験データの確認（現在の試験は PR 陰性例が中心）
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---





<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：パージェタ点滴静

**販売名（規格別）**：パージェタ点滴静注420mg/14mL
<!-- brand-names:end -->

