---
noindex: true
sitemap: false
layout: default
title: Sacituzumab Govitecan
parent: モデル予測のみ (L5)
nav_order: 151
evidence_level: L5
indication_count: 1
last_modified_at: 2026-09-17
---

# Sacituzumab Govitecan
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

## Sacituzumab Govitecan:トリプルネガティブ乳癌から新規適応症の探索へ
{: .text-alpha }

## 一言まとめ

Sacituzumab govitecan（サシツズマブ ゴビテカン） はもともと進行トリプルネガティブ乳癌およびHR+/HER2- 乳癌の治療に用いられる薬剤です。TxGNN モデルは、本剤が**薬剤性骨粗鬆症 (drug-induced osteoporosis)** に有効である可能性を予測しましたが、現時点ではモデル予測のみが根拠で、臨床エビデンスはありません。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 進行トリプルネガティブ乳癌、HR+/HER2- 乳癌 |
| 予測新適応症 | 薬剤性骨粗鬆症 (drug-induced osteoporosis) |
| TxGNN 予測スコア | 99.78% |
| エビデンスレベル | L5 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Hold |

## この予測が妥当な理由

Sacituzumab govitecan は抗体薬物複合体（ADC）で、抗 Trop-2 抗体と SN-38（irinotecan の活性代謝物）が結合しています。

1. **Trop-2 標的**:Trop-2（tumor-associated calcium signal transducer 2）は主に上皮細胞に発現し、多くの固形腫瘍で過剰発現しています。

2. **細胞毒性の作用機序**:SN-38 はトポイソメラーゼI阻害薬で、主に抗腫瘍治療に用いられます。

3. **予測適応症の妥当性に疑問あり**:薬剤性骨粗鬆症と、Trop-2 またはトポイソメラーゼI阻害薬の作用機序との間には明確な関連が認められず、この予測の生物学的妥当性は低いと考えられます。

## 臨床試験エビデンス

現時点で、Sacituzumab govitecan の薬剤性骨粗鬆症に対する臨床試験の登録はありません。

## 文献エビデンス

現時点で、これを裏付ける関連文献はありません。

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 抗体薬物複合体 (ADC) |
| 骨髄抑制リスク | 高 - 好中球減少症は頻度の高い重篤な副作用 |
| 催吐性分類 | 中等度 |
| モニタリング項目 | 全血球計算、肝腎機能、下痢症状 |
| 取り扱い・曝露対策 | 細胞毒性薬の取り扱い基準に従う必要あり |

## 安全性に関する考慮事項

### 重大な薬物相互作用

| 相互作用薬 | 重症度 | 情報源 |
|-------------|---------|------|
| Deferiprone | 重大 | DDInter |
| Irinotecan | 重大 | DDInter |
| Leflunomide | 重大 | DDInter |
| Natalizumab | 重大 | DDInter |
| Adalimumab | 重大 | DDInter |
| Infliximab | 重大 | DDInter |
| Etanercept | 重大 | DDInter |
| Fingolimod | 重大 | DDInter |
| Apalutamide | 重大 | DDInter |

### 薬理学的標的

| 標的 | 遺伝子名 | 説明 |
|-----|---------|------|
| TROP-2 (tumor associated calcium signal transducer 2) | TACSTD2 | Sacituzumab govitecan の抗体部分が TROP-2 に結合する |

### 重要な警告

- **重度の好中球減少症**:発熱性好中球減少症を引き起こす可能性があります
- **重度の下痢**:SN-38 により重度の下痢が起こることがあります
- **過敏反応**:インフュージョンリアクション
- **UGT1A1 多型**:UGT1A1*28 ホモ接合体の患者では、毒性リスクがより高い可能性があります

## 結論と次のステップ

**判断:Hold**

**理由:**
1. 予測適応症（薬剤性骨粗鬆症）と本剤の作用機序との間に生物学的妥当性が認められない
2. 臨床試験または文献によるエビデンスがない
3. 細胞毒性薬として、悪性疾患以外に用いる場合の安全性が懸念される
4. 費用対効果の観点から、骨粗鬆症の適応には適さない

**推進に必要な事項:**
- Trop-2 の骨代謝における関連する作用が見出されること
- 基礎研究により作用機序の妥当性が示されること
- 毒性を考慮すると、この適応症のさらなる探索は推奨されない


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
