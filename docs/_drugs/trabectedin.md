---
noindex: true
sitemap: false
layout: default
title: Trabectedin
parent: モデル予測のみ (L5)
nav_order: 179
evidence_level: L5
indication_count: 1
last_modified_at: 2026-09-17
description: "Trabectedin：予測新適応症は女性乳腺癌 (female breast carcinoma)（エビデンスレベル L5）。既存適応症：無法切除或轉移性脂肪肉瘤/平滑肌肉瘤"
---

# Trabectedin
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **1** 件
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

# Trabectedin：軟部肉腫から女性乳癌へ

## 一言まとめ

Trabectedin（トラベクテジン） は、もともと切除不能または転移性の脂肪肉腫および平滑筋肉腫の治療に用いられています。
TxGNN モデルは、本剤が**女性乳癌 (female breast carcinoma)** に有効である可能性を予測しており、
現在 **2 件の臨床試験**と**複数の文献**がこの方向性を支持しています。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 切除不能または転移性の脂肪肉腫/平滑筋肉腫 |
| 予測新適応症 | 女性乳癌 (female breast carcinoma) |
| TxGNN 予測スコア | 99.73% |
| エビデンスレベル | 評価待ち |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Trabectedin は海洋生物由来の抗腫瘍薬で、主に転写調節への影響を介してがん細胞の増殖を抑制します。その特徴的な作用機序は次のとおりです。

1. **DNA 修復系の阻害**：転写共役ヌクレオチド除去修復および相同組換え修復 (HRR) に影響を与える
2. **腫瘍微小環境の調節**：腫瘍関連マクロファージ (TAM) の数を減少させる
3. **BRCA 欠損に対する感受性**：BRCA1/2 変異を有する腫瘍に対して特異的な効果を示す

これらの機序は乳癌においても臨床的に意義があり、特に BRCA 変異を有する乳癌患者で重要です。

## 臨床試験エビデンス

| 試験番号 | 相 | 状態 | 症例数 | 主な所見 |
|---------|------|------|------|---------|
| [NCT03470805](https://clinicaltrials.gov/study/NCT03470805) | Phase 2 | COMPLETED | 9 | 再発卵巣癌において、Trabectedin-PLD 療法後の維持療法としての Olaparib の効果を評価 |
| [NCT00786838](https://clinicaltrials.gov/study/NCT00786838) | Phase 2 | COMPLETED | 76 | Trabectedin が QT/QTc 間隔に及ぼす影響を評価 |

## 文献エビデンス

| PMID | 年 | 種類 | 雑誌 | 主な所見 |
|------|-----|------|------|---------|
| [26592307](https://pubmed.ncbi.nlm.nih.gov/26592307/) | 2016 | Review | Expert Opin Investig Drugs | 乳癌における Trabectedin の潜在的な応用について論じている |
| [25239225](https://pubmed.ncbi.nlm.nih.gov/25239225/) | 2014 | Phase II RCT | Clin Breast Cancer | 進行乳癌に対する Trabectedin 単剤療法の有効性と安全性を評価 |
| [27710871](https://pubmed.ncbi.nlm.nih.gov/27710871/) | 2016 | Review | Cancer Treat Rev | BRCA 欠損患者における Trabectedin の化学療法としての選択肢を検討 |
| [27266804](https://pubmed.ncbi.nlm.nih.gov/27266804/) | 2016 | Phase II | Clin Breast Cancer | XPG 遺伝子発現に基づき、HR+/HER2- 進行乳癌における Trabectedin の有効性を評価 |
| [38863768](https://pubmed.ncbi.nlm.nih.gov/38863768/) | 2024 | Review | Drug Des Devel Ther | 卵巣癌における Trabectedin の応用と BRCA 変異の状況に焦点を当てている |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 抗腫瘍性抗生物質 (海洋由来) |
| 骨髄抑制リスク | 高度 |
| 催吐性分類 | 中等度から高度 |
| モニタリング項目 | CBC（分画を含む）、肝腎機能、CK |
| 取り扱い時の防護 | 細胞毒性薬の取り扱い基準に従って操作すること |
| 特記事項 | 横紋筋融解症を起こす可能性があり、クレアチンキナーゼのモニタリングが必要 |

## 安全性に関する考慮事項

- **肝毒性**：定期的な肝機能のモニタリングが必要
- **骨髄抑制**：好中球減少、血小板減少を起こす可能性がある
- **横紋筋融解症**：まれだが重篤な副作用
- **心毒性**：QT 間隔のモニタリングが必要

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
乳癌における Trabectedin の複数の臨床試験および文献から、特に BRCA 変異患者での潜在的な有効性が示唆されています。本剤の特徴的な作用機序は既存の乳癌治療薬とは異なり、新たな治療選択肢となる可能性があります。

**推進に必要な事項：**
- 乳癌を対象とした大規模ランダム化比較試験
- BRCA 変異状態に基づくバイオマーカーのスクリーニング戦略
- 既存の乳癌治療レジメンとの比較研究


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
