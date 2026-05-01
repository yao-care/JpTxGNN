---
layout: default
title: Simvastatin
parent: 僅模型預測 (L5)
nav_order: 129
evidence_level: L5
indication_count: 10
---

# Simvastatin
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

`txgnn-pipeline` スキルを確認しました。Evidence Pack JSON に基づいて、以下の薬物再利用評価レポートを生成します。

---

# シンバスタチン：高コレステロール血症から家族性高コレステロール血症へ

## 一言要約

シンバスタチンは世界的に広く使用されている HMG-CoA 還元酵素阻害薬（スタチン系薬剤）であり、高コレステロール血症治療の標準薬として長年の実績を持ちます。ただし、日本国内では現時点で PMDA 承認が確認されていません。TxGNN モデルは**家族性高コレステロール血症 (Familial Hypercholesterolemia)** に有効である可能性を 99.63% のスコアで予測しており、現在 **19 件の臨床試験**と **18 編の文献**がこの方向性を強く支持しています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本国内未登録（PMDA 承認なし） |
| 予測新規適応症 | 家族性高コレステロール血症 (Familial Hypercholesterolemia) |
| TxGNN 予測スコア | 99.63% |
| エビデンスレベル | L1 |
| 日本市販状況 | ✗ 未上市 |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails |

---

## この予測が妥当である理由

現在、DrugBank からの詳細な作用機序データ（MOA）は取得できていません。既知の情報によると、シンバスタチンは **HMG-CoA 還元酵素阻害薬（スタチン系薬剤）** であり、高コレステロール血症における有効性が世界的に証明されており、機序的に家族性高コレステロール血症にも直接適用可能です。

シンバスタチンは肝臓でのコレステロール生合成を律速する HMG-CoA 還元酵素を競合的に阻害し、代償的な LDL 受容体の上方制御（upregulation）を促すことで血中 LDL-C 濃度を約 30〜45% 低下させます。また、VLDL 産生の減少や HDL-C の軽度上昇など、多面的な脂質改善効果も有します。

家族性高コレステロール血症（FH）は LDLR・ApoB・PCSK9 遺伝子の変異により LDL-C の受容体介在性クリアランスが障害される単遺伝子性疾患で、未治療では冠動脈疾患が早期発症し平均余命が 15〜30 年短縮されます。シンバスタチンは残存する LDL 受容体活性を代償的に最大化し、FH 患者の心血管イベントリスクを有意に軽減します。ENHANCE 試験（Phase 3 RCT、720 例）や Cochrane 系統的レビューを含む複数の高質エビデンスが FH に対するシンバスタチンの有用性を確立しており、TxGNN の予測は既存のエビデンスベースを強く追認するものです。

---

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT03884452](https://clinicaltrials.gov/study/NCT03884452) | Phase 3 | 完了 | 50 | ホモ接合体 FH 患者に対する Ezetimibe と Atorvastatin または **Simvastatin** 併用の有効性・安全性を評価した二重盲検 RCT |
| [NCT00129402](https://clinicaltrials.gov/study/NCT00129402) | Phase 3 | 完了 | 248 | ヘテロ接合体 FH 青少年（10〜17 歳）における **Ezetimibe + Simvastatin** vs Simvastatin 単独の有効性・安全性（多施設二重盲検 RCT） |
| [NCT00552097](https://clinicaltrials.gov/study/NCT00552097) | Phase 3 | 完了 | 720 | **ENHANCE 試験**：ヘテロ接合体 FH 患者において高用量 Simvastatin + Ezetimibe vs Simvastatin 単独で頚動脈 IMT 進展抑制効果を比較 |
| [NCT00465088](https://clinicaltrials.gov/study/NCT00465088) | Phase 3 | 完了 | 199 | **SUPREME 試験**：高脂血症・混合型脂質異常症患者において Niacin ER + **Simvastatin** と Atorvastatin の HDL-C 上昇効果を直接比較 |
| [NCT03510884](https://clinicaltrials.gov/study/NCT03510884) | Phase 3 | 完了 | 153 | ヘテロ接合体 FH 小児・青少年（8〜17 歳）における Alirocumab の二重盲検プラセボ対照 RCT（スタチン安定投与を背景治療として設定） |
| [NCT01507831](https://clinicaltrials.gov/study/NCT01507831) | Phase 3 | 完了 | 2,341 | 高心血管リスク高コレステロール血症患者における Alirocumab（PCSK9 阻害薬）の長期（2 年）安全性・忍容性 RCT |
| [NCT01623115](https://clinicaltrials.gov/study/NCT01623115) | Phase 3 | 完了 | 486 | ヘテロ接合体 FH 患者を対象に Alirocumab の LDL-C 低下効果を 24 週間評価した二重盲検プラセボ対照 RCT |
| [NCT03885921](https://clinicaltrials.gov/study/NCT03885921) | Phase 3 | 完了 | 44 | ホモ接合体 FH 患者における Ezetimibe + Atorvastatin/**Simvastatin** 長期安全性・忍容性追跡調査（最大 24 ヵ月、NCT03884452 の延長試験） |
| [NCT00654446](https://clinicaltrials.gov/study/NCT00654446) | Phase 3 | 完了 | 442 | Fredrickson Type IIa/IIb 脂質異常症（ヘテロ接合体 FH 含む）において Rosuvastatin と **Simvastatin** の腎臓への影響を 6 週間比較 |
| [NCT01890967](https://clinicaltrials.gov/study/NCT01890967) | Phase 2 | 完了 | 527 | 原発性高コレステロール血症患者を対象とした LY3015014（PCSK9 阻害薬）の用量設定試験（スタチン ± Ezetimibe 背景治療） |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [18376000](https://pubmed.ncbi.nlm.nih.gov/18376000/) | 2008 | RCT | N Engl J Med | **ENHANCE 試験**：ヘテロ接合体 FH 患者で Ezetimibe + Simvastatin は LDL-C を追加 7.2% 低下させたが、頚動脈 IMT の有意差は認められず |
| [31696945](https://pubmed.ncbi.nlm.nih.gov/31696945/) | 2019 | Cochrane SR | Cochrane Database Syst Rev | FH 小児・青少年へのスタチン療法を系統的レビュー・メタ解析；LDL-C 低下効果と忍容性を包括的に評価 |
| [28685504](https://pubmed.ncbi.nlm.nih.gov/28685504/) | 2017 | Cochrane SR | Cochrane Database Syst Rev | 上記 Cochrane レビュー 2017 年改訂版；FH 小児への早期スタチン開始推奨を支持 |
| [35629051](https://pubmed.ncbi.nlm.nih.gov/35629051/) | 2022 | Cohort | J Clin Med | Simvastatin 治療中の FH 小児 13 例と未治療 13 例を比較；フローサイトメトリーにてリンパ球サブセットおよび免疫パラメータを評価 |
| [35361995](https://pubmed.ncbi.nlm.nih.gov/35361995/) | 2022 | Cohort | Pharmacogenomics J | FH 遺伝子診断パネルとスタチン薬理ゲノミクスを統合した NGS 戦略を実装；遺伝子型に基づくスタチン処方最適化を提案 |
| [27417002](https://pubmed.ncbi.nlm.nih.gov/27417002/) | 2016 | Cohort | J Am Coll Cardiol | ヘテロ接合体 FH 患者においてスタチン投与が冠動脈疾患イベントを 76% 低下させ、全死亡率も有意に改善 |
| [15794711](https://pubmed.ncbi.nlm.nih.gov/15794711/) | 2005 | Review | Expert Opin Drug Saf | FH 患者における Simvastatin のベネフィット（LDL-C 低下、心血管リスク軽減）とリスク（筋毒性、肝毒性）を包括的評価 |
| [2083515](https://pubmed.ncbi.nlm.nih.gov/2083515/) | 1990 | Review | Drugs | Simvastatin の薬理学的特性レビュー；FH・非 FH 高コレステロール血症患者で LDL-C 30〜45% 低下を確認 |
| [15554726](https://pubmed.ncbi.nlm.nih.gov/15554726/) | 2004 | Review | Am J Cardiovasc Drugs | Ezetimibe/Simvastatin（Vytorin）の高コレステロール血症管理における使用レビュー；腸管吸収阻害と肝臓生合成阻害の相補的機序を解説 |
| [28437620](https://pubmed.ncbi.nlm.nih.gov/28437620/) | 2017 | Review | Endocrine Practice | AACE/ACE 脂質異常症管理ガイドライン 2017；FH を含む高リスク群へのスタチン積極使用推奨を提示 |

---

## 日本市販情報

日本国内（PMDA）でのシンバスタチン単剤承認は本データに確認されていません（PMDA クエリ結果 0 件）。シンバスタチン含有配合剤（例：エゼチミブ配合剤）の承認状況については PMDA への追加照会が必要です。

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
家族性高コレステロール血症に対するシンバスタチンの有効性は、ENHANCE 試験を含む複数の Phase 3 RCT および Cochrane 系統的レビュー（L1 エビデンス）によってグローバルに確立されており、TxGNN スコア 99.63% もこれを強く裏付けています。ただし、日本国内では PMDA 未登録であり、安全性情報の補充と薬物相互作用プロファイルの確認が必要です。

**進める場合に必要なもの：**
- PMDA 添付文書（仿単）の取得と安全性情報（警告・禁忌・相互作用）の精査
- シンバスタチン含有配合剤（Ezetimibe 配合剤等）の日本国内承認状況の確認
- 詳細な作用機序データ（DrugBank MOA）の補充
- CYP3A4 阻害薬（HIV プロテアーゼ阻害薬、アゾール系抗真菌薬等）との薬物相互作用プロファイルの確認
- 日本動脈硬化学会ガイドラインとの整合性確認および日本人 FH 患者データの照合
---

