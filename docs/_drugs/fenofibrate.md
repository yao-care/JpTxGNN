---
layout: default
title: Fenofibrate
parent: 僅模型預測 (L5)
nav_order: 58
evidence_level: L5
indication_count: 10
---

# Fenofibrate
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

以下、Evidence Pack に基づいて薬物再利用評価レポートを生成します。

---

# フェノフィブラート：高トリグリセリド血症・混合型脂質異常症からホモ接合体型家族性高コレステロール血症へ

## 一言要約

フェノフィブラート（Fenofibrate）は PPARα（ペルオキシソーム増殖因子活性化受容体α）を活性化し、VLDL・三酸甘油酯（TG）の低下と HDL コレステロールの上昇をもたらす脂質異常症治療薬として国際的に広く使用されています。TxGNN モデルは**ホモ接合体型家族性高コレステロール血症（Homozygous Familial Hypercholesterolemia, HoFH）**への有効性を予測しており、現在 **1 件の臨床試験**と **11 編の文献**がこの疾患領域に関連する情報を提供しています。ただし、HoFH の中核病態（LDL 受容体機能の完全欠損）に対するフェノフィブラートの直接的な臨床エビデンスは限定的であり、現時点では研究課題として位置づけられます。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 高トリグリセリド血症・混合型脂質異常症（国際承認；日本未承認） |
| 予測新規適応症 | ホモ接合体型家族性高コレステロール血症（Homozygous Familial Hypercholesterolemia） |
| TxGNN 予測スコア | 99.91% |
| エビデンスレベル | L4 |
| 日本市販状況 | 未上市 |
| 承認番号数 | 0 件 |
| 推奨決定 | Hold |

---

## この予測が妥当である理由

フェノフィブラートは核内受容体 PPARα の強力な促進剤であり、肝臓での脂肪酸 β 酸化を亢進させ、リポ蛋白脂肪酶（LPL）活性を上昇させるとともに apoC-III の発現を抑制することで VLDL の産生・クリアランスを改善します。さらに、apoA-I および apoA-II 遺伝子の転写を上方調節し HDL コレステロールを増加させます。詳細な作用機序データ（MOA）については現在 DrugBank から取得中であり、本報告書の完成後に補完される予定です。

HoFH は LDL 受容体遺伝子の両アレルに機能喪失変異を持つ最重症型の遺伝性高コレステロール血症であり、LDL-C が正常値の 4〜8 倍以上に上昇します。フェノフィブラートの主要経路（LPL 活性化・VLDL 低下）は LDL 受容体非依存的であり、VLDL からの LDL 産生を上流で抑制する経路を通じた補助的効果が理論的に考えられます。1984 年の Type II 高脂蛋白血症患者を対象としたコホート研究（PMID 6593751）では HoFH 患者 1 名において最大幅の総コレステロールおよび LDL-C 低下が観察されており、限定的ながら直接的な臨床観察が存在します。

フェノフィブラートは高脂蛋白血症スペクトラム全体（Type IIa, IIb, III, IV, V）に幅広い脂質改善作用を持つことから、TxGNN モデルが脂質関連疾患群との機序的重複を認識し本予測を生成したと推測されます。ただし、HoFH に対する現行標準治療（PCSK9 阻害剤、ロミタピド、LDL アフェレーシス）との位置づけ比較、および直接的な臨床試験エビデンスの欠如が課題として残ります。

---

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT03510715](https://clinicaltrials.gov/study/NCT03510715) | Phase 3 | 完了 | 18 | HoFH の小児・青少年（8〜17 歳）を対象に Alirocumab（体重別 75 または 150 mg、Q2W 投与）の有効性・安全性を評価。Week 12 での LDL-C 低下が主要エンドポイント。疾患コホートとしての参照価値はあるが、研究主薬は PCSK9 阻害剤（Alirocumab）であり、Fenofibrate は対象外。 |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [6593751](https://pubmed.ncbi.nlm.nih.gov/6593751/) | 1984 | Cohort | Pharmacological Research Communications | Type II 高脂蛋白血症 22 名に Fenofibrate 300 mg/日を 4〜12 ヶ月投与。HoFH 患者 1 名で総コレステロール・LDL-C の最大幅低下を確認。唯一の HoFH 直接観察データ |
| [24734312](https://pubmed.ncbi.nlm.nih.gov/24734312/) | 2014 | — | Pharmacotherapy | HoFH 管理薬（Atorvastatin, Simvastatin, Rosuvastatin, **Fenofibrate**, Ezetimibe, Niacin）に対する Lomitapide の薬物動態的相互作用を検討。HoFH 治療文脈における Fenofibrate の位置を確認 |
| [2042836](https://pubmed.ncbi.nlm.nih.gov/2042836/) | 1991 | Review | Annals of the New York Academy of Sciences | 小児・青少年の脂質異常症に対する薬物・外科的治療のレビュー。FH 患者での Fenofibrate を含む各種薬剤の使用実績と成功例を収載 |
| [24946816](https://pubmed.ncbi.nlm.nih.gov/24946816/) | 2014 | Review | Internal Medicine Journal | HoFH に対する肝移植の治療的役割と新興脂質降下療法（LDL アフェレーシス代替）との比較を考察。標準治療の限界と補助療法の必要性を提示 |
| [28437620](https://pubmed.ncbi.nlm.nih.gov/28437620/) | 2017 | Review | Endocrine Practice | AACE/ACE 脂質異常症管理・心血管疾患予防の包括的臨床実践ガイドライン。非スタチン薬（フィブラート系を含む）の適応と位置づけを規定 |
| [37979722](https://pubmed.ncbi.nlm.nih.gov/37979722/) | 2024 | Review | Indian Heart Journal | 非スタチン脂質降下薬の最新包括レビュー。Fenofibrate の最も明確な単独適応は TG > 500 mg/dL による急性膵炎リスク低減と明記。混合脂質異常症での補助的役割も解説 |
| [26432726](https://pubmed.ncbi.nlm.nih.gov/26432726/) | 2015 | Review | Indian Heart Journal | LDL-C・スタチン・PCSK9 阻害剤のレビュー。重症高コレステロール血症（HoFH 含む）に対する補助療法としての非スタチン薬の役割を考察 |
| [14620392](https://pubmed.ncbi.nlm.nih.gov/14620392/) | 2003 | Review | Pharmacotherapy | エゼチミブの選択的コレステロール吸収阻害作用のレビュー。HoFH を含む高コレステロール血症に対する多剤併用治療の文脈で参照 |
| [35499807](https://pubmed.ncbi.nlm.nih.gov/35499807/) | 2022 | Review | Current Atherosclerosis Reports | 妊娠中の脂質異常症管理レビュー。フィブラート系薬剤を含む脂質降下療法の適応・禁忌・エビデンスギャップを包括的に考察 |
| [9129869](https://pubmed.ncbi.nlm.nih.gov/9129869/) | 1997 | Review | Drugs | アトルバスタチンの薬理と高脂血症（高コレステロール血症・高トリグリセリド血症）における治療可能性のレビュー。スタチン治療の標準的背景情報として参照 |

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Hold**

**理由：**
HoFH の中核病態は LDL 受容体機能の両アレル完全欠損であり、フェノフィブラートの PPARα 経路は VLDL・TG 代謝を主標的とするため LDL-C への直接効果は限定的です。フェノフィブラートを HoFH に直接適用した臨床試験は存在せず、1984 年の単症例観察を除く直接的エビデンスがなく、現段階ではエビデンスレベル L4（機序研究・間接的文献）にとどまります。

**進める場合に必要なもの：**
- HoFH 患者を対象とした Fenofibrate の探索的前向き臨床試験または症例シリーズの設計
- PPARα 活性化が LDL 受容体非依存的経路（apoB 合成抑制・残存 VLDL 低下→ LDL 産生減少）で LDL-C を低下させるかを検証する前臨床・メカニズム研究
- 現行 HoFH 標準治療（PCSK9 阻害剤・ロミタピド・LDL アフェレーシス）との補助療法としての位置づけ評価
- 日本（PMDA）における Fenofibrate の承認申請のための安全性・有効性基礎データ整備
- TFDA 仿單相当の安全性資料（警語・禁忌）の収集と初期安全性評価（S1 ステージ）への移行
---

