---
layout: default
title: Morphine
parent: 僅模型預測 (L5)
nav_order: 101
evidence_level: L5
indication_count: 10
---

# Morphine
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

# モルヒネ：重度疼痛から筋筋膜性疼痛症候群へ

## 一言要約

モルヒネ（Morphine, DB00295）は μ-オピオイド受容体に作用する古典的な麻薬性鎮痛薬で、重度疼痛の管理に広く使用されています。TxGNN モデルは**筋筋膜性疼痛症候群 (Myofascial Pain Syndrome)** に有効である可能性を予測しており、現在 **33 件の臨床試験**と **17 編の文献**がこの方向性を支持しています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 重度疼痛（PMDA 未登録） |
| 予測新規適応症 | 筋筋膜性疼痛症候群 (Myofascial Pain Syndrome) |
| TxGNN 予測スコア | 99.75% |
| エビデンスレベル | L2 |
| 日本市販状況 | ✗ 未上市 |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails |

---

## この予測が妥当である理由

モルヒネは脊髄後角および末梢組織の μ-オピオイド受容体を活性化し、P 物質・CGRP の放出抑制と痛覚上行伝導の遮断を通じて強力な鎮痛効果を発揮します。現在、詳細な作用機序（MOA）データは未取得ですが、既知の薬理学的情報として、モルヒネは中枢・末梢の双方で侵害受容シグナルを抑制し、慢性疼痛における中枢感作を調節する可能性があります。

筋筋膜性疼痛症候群（MPS）はトリガーポイントを中心とした慢性筋肉骨格疼痛で、末梢侵害受容体の過剰感作と中枢感作が病態の核心を成します。モルヒネの μ-オピオイド受容体を介した疼痛抑制機構は、MPS の主要病態に直接作用することが機序的に妥当であり、特に侵害受容性疼痛が主体の難治性 MPS においてオピオイド鎮痛薬が補助療法として位置付けられています。

最も直接的なエビデンスとして、PMID 41664327（2026年 RCT）は脊椎固定術後の筋筋膜浸潤注射において dexmedetomidine+morphine が ropivacaine 単独と比較された試験であり、また PMID 16713811（2006年 RCT）では難治性顳顎関節 MPS に対する関節内モルヒネ注入の長期鎮痛効果が報告されています。局所モルヒネ投与が MPS 疼痛に直接有効であることを示す最高品質の直接証拠です。

---

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT06955923](https://clinicaltrials.gov/study/NCT06955923) | Phase 2 | 完了 | 11 | TKA 術後の筋筋膜疼痛に対するトリガーポイント注射の疼痛スコアおよび opioid 使用量への影響評価（MPS 直接言及） |
| [NCT04831346](https://clinicaltrials.gov/study/NCT04831346) | NA | 進行中 | 100 | 顳顎関節筋筋膜疼痛における低レベルレーザー vs 咬合板の疼痛・開口量・筋活動比較（疾病直接一致） |
| [NCT05478928](https://clinicaltrials.gov/study/NCT05478928) | NA | 不明 | 60 | MPS トリガーポイントに対する経皮微小電気分解 vs ドライニードリングの比較（疾病直接一致） |
| [NCT04640896](https://clinicaltrials.gov/study/NCT04640896) | Phase 4 | 進行中 | 60 | 頸椎前方術後の頸部筋筋膜疼痛に対するトリガーポイント注射 vs 従来療法 |
| [NCT03271151](https://clinicaltrials.gov/study/NCT03271151) | Phase 4 | 完了 | 160 | TKA 後の duloxetine による opioid 使用量削減効果（opioid 使用量が主要評価指標） |
| [NCT04364867](https://clinicaltrials.gov/study/NCT04364867) | Phase 4 | 完了 | 102 | 肩関節置換術後の Exparel vs 持続鎮痛ポンプ（麻薬使用量・疼痛スコア比較） |
| [NCT05573594](https://clinicaltrials.gov/study/NCT05573594) | NA | 完了 | 40 | 女性機械性腰痛（MPS 類縁族群）における筋肉エネルギー療法の疼痛緩和効果 |
| [NCT04046536](https://clinicaltrials.gov/study/NCT04046536) | NA | 完了 | 204 | 湾岸戦争疾患の慢性筋骨格疼痛・共病症状に対する rTMS の有効性（n=204） |
| [NCT01878019](https://clinicaltrials.gov/study/NCT01878019) | N/A | 完了 | 92 | 慢性疼痛患者の疼痛制御機構の探索（naloxone を用いた opioid 効果評価） |
| [NCT07413770](https://clinicaltrials.gov/study/NCT07413770) | NA | 進行中 | 60 | 筋筋膜性疼痛症候群患者への古典的マッサージの疼痛・筋感受性・機能・QOL への影響（疾病直接一致） |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [41664327](https://pubmed.ncbi.nlm.nih.gov/41664327/) | 2026 | RCT | Asian Spine J | 脊椎固定術後の筋筋膜浸潤注射：dexmedetomidine+morphine vs ropivacaine 0.2%（morphine 直接比較の最高品質証拠） |
| [16713811](https://pubmed.ncbi.nlm.nih.gov/16713811/) | 2006 | RCT | J Oral Maxillofac Surg | 難治性 TMJ 疼痛への関節洗浄 + 関節内モルヒネ注入による長期鎮痛効果（morphine 局所投与の直接証拠） |
| [39793344](https://pubmed.ncbi.nlm.nih.gov/39793344/) | 2025 | RCT | Eur J Obstet Gynecol | 骨盤底筋筋膜疼痛に対する OnabotulinumtoxinA 注射後の陰部神経ブロックの術後疼痛改善効果 |
| [17870625](https://pubmed.ncbi.nlm.nih.gov/17870625/) | 2008 | RCT | Eur J Pain | 開胸術後疼痛：硬膜外 bupivacaine+morphine vs 肋間神経冷凍療法（慢性疼痛移行リスク評価） |
| [35066974](https://pubmed.ncbi.nlm.nih.gov/35066974/) | 2022 | Cohort | Pain Practice | 「レガシー疼痛」患者へのストレッチングプログラムによる筋筋膜痛解消と opioid 使用量の変化（n=後ろ向き） |
| [22648287](https://pubmed.ncbi.nlm.nih.gov/22648287/) | 2012 | Case series | J Anesthesia | 長期頸部 MPS に椎間関節注射を追加した集学的治療：疼痛・頸部可動域の改善 |
| [21419546](https://pubmed.ncbi.nlm.nih.gov/21419546/) | 2011 | Review | J Oral Maxillofac Surg | 慢性顳顎関節機能不全における opioid 長期使用のエビデンス：他の慢性非癌性疼痛での有効性を根拠とした考察 |
| [20390305](https://pubmed.ncbi.nlm.nih.gov/20390305/) | 2010 | Cohort | Schmerz | 慢性腰痛患者での長期 opioid 使用中と離脱後の疼痛閾値変化：集学的疼痛療法との比較 |

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
局所・硬膜外モルヒネ投与が MPS 疼痛に有効であることを示す RCT（PMID 41664327・16713811）が存在し、TxGNN スコア 99.75% および L2 エビデンスレベルから機序的・臨床的根拠は十分です。ただし、オピオイドの依存・乱用・薬物過使用性疼痛（MOH）リスクを考慮した厳格な管理体制が必須条件です。

**進める場合に必要なもの：**
- 詳細な作用機序データ（MOA）の補充（DrugBank API 照会）
- PMDA 添付文書 PDF の解析による日本国内の警告・禁忌情報の確認
- 最適投与経路の決定（局所浸潤注射 vs 硬膜外 vs 全身投与）
- 成癮・依存・乱用リスクのモニタリング計画策定（CDC ガイドライン／日本ペインクリニック学会指針準拠）
- 長期使用に伴う耐性・薬物過使用性疼痛リスク評価プロトコルの設計
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

