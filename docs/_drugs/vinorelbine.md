---
layout: default
title: Vinorelbine
parent: 中エビデンス (L3-L4)
nav_order: 190
evidence_level: L3
indication_count: 1
last_modified_at: 2026-09-17
description: "Vinorelbine：予測新適応症はEwing 肉腫 (Ewing sarcoma)（エビデンスレベル L3）。既存適応症：日本の承認適応症は本サイトのデータに未収載、lung cancer）"
---

# Vinorelbine
{: .fs-9 }

エビデンスレベル: **L3** | 予測適応症: **1** 件
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

# Vinorelbine：非小細胞肺癌から Ewing 肉腫へ

## 一言まとめ

Vinorelbine（ビノレルビン）は本来、非小細胞肺癌および転移性乳癌の治療に用いられます。
TxGNN モデルは、本剤が **Ewing 肉腫 (Ewing sarcoma)** に有効な可能性があると予測しており、
現在 **4 件の臨床試験**がこの方向性を支持しています。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：non-small cell lung carcinoma (disease)、lung cancer） |
| 予測新適応症 | Ewing 肉腫 (Ewing sarcoma) |
| TxGNN 予測スコア | 99.999% |
| エビデンスレベル | L3 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

ビノレルビンは半合成のビンカアルカロイド（Vinca alkaloid）で、チューブリン重合を阻害することにより有糸分裂を抑制します。Ewing 肉腫は高度に増殖する悪性腫瘍であり、微小管阻害薬に感受性を示します。ビノレルビンは、Ewing 肉腫を含む小児の難治性腫瘍を対象とした複数の臨床試験で活性を示しています。

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 人数 | 主な所見 |
|---------|------|------|------|---------|
| [NCT06451302](https://clinicaltrials.gov/study/NCT06451302) | N/A | ACTIVE_NOT_RECRUITING | 100 | 中国の小児 Ewing 肉腫に対するリスク層別化に基づく治療の有効性と安全性を評価 |
| [NCT00003234](https://clinicaltrials.gov/study/NCT00003234) | Phase 2 | COMPLETED | 50 | Ewing 肉腫を含む再発/難治性の小児悪性腫瘍に対するビノレルビンの効果を検討 |
| [NCT00180947](https://clinicaltrials.gov/study/NCT00180947) | Phase 2 | UNKNOWN | 210 | 難治性腫瘍におけるビノレルビンとシクロホスファミドの併用による抗腫瘍活性を評価 |
| [NCT05999994](https://clinicaltrials.gov/study/NCT05999994) | Phase 2 | RECRUITING | 105 | CAMPFIRE 小児・青少年イノベーション試験のマスタープロトコル |

## 文献エビデンス

現時点では、ビノレルビンの Ewing 肉腫への使用に特化した PubMed 収載文献はありませんが、難治性肉腫での使用を支持する関連の小児腫瘍研究文献があります。

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 従来型の細胞毒性薬（Vinca alkaloid） |
| 骨髄抑制リスク | 高度（好中球減少が用量制限毒性） |
| 催吐性リスク分類 | 低度 |
| モニタリング項目 | CBC（分画を含む）、肝機能、神経毒性の評価 |
| 取り扱い時の防護 | 細胞毒性薬の取り扱い基準に従って操作する必要あり。静脈内投与では血管外漏出に注意 |

## 安全性に関する考慮事項

### 重大な薬物相互作用（Major）

| 相互作用薬 | 機序の説明 |
|-------------|---------|
| Clarithromycin | CYP3A4 阻害薬。ビノレルビンの血中濃度と毒性を増加させる |

### 中等度の薬物相互作用（Moderate）

| 相互作用薬 | 機序の説明 |
|-------------|---------|
| Aprepitant | CYP3A4 阻害 |
| Dexamethasone | 代謝に影響する可能性 |
| Simvastatin | CYP3A4 の競合 |
| Rosuvastatin | 薬物トランスポーターによる相互作用 |

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
ビノレルビンは小児腫瘍の複数の臨床試験で Ewing 肉腫に対する潜在的な有効性を示しており、作用機序（微小管阻害）にも高増殖性腫瘍に対する合理的な生物学的根拠があります。

**推進に必要な事項：**
- Ewing 肉腫に特化した有効性データの収集
- 適切な小児用量および投与レジメンの確定
- 既存の Ewing 肉腫標準治療レジメンとの比較評価
- 骨髄抑制および神経毒性の綿密なモニタリング計画


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
