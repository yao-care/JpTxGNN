---
noindex: true
sitemap: false
layout: default
title: Tiaprofenic Acid
parent: モデル予測のみ (L5)
nav_order: 171
evidence_level: L5
indication_count: 1
last_modified_at: 2026-09-17
---

# Tiaprofenic Acid
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

## Tiaprofenic Acid：消炎鎮痛薬から希少骨系統疾患への探索
{: .text-alpha }

## 一言まとめ

Tiaprofenic Acid（チアプロフェン酸）は、もともと消炎鎮痛に用いられる薬です。
TxGNN モデルは、本剤が複数の希少な骨発育不全疾患に有効である可能性を予測しましたが、
現時点では、これらの予測を裏付ける **臨床試験や文献のエビデンスは一切ありません**。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 消炎鎮痛 |
| 予測新適応症 | Brachydactyly-Syndactyly Syndrome（第1位） |
| TxGNN 予測スコア | 99.99%（最高スコア） |
| エビデンスレベル | L5（予測のみ） |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Hold |

## TxGNN 予測適応症一覧

| 順位 | 予測疾患 | TxGNN スコア | 疾患タイプ |
|-----|---------|-----------|---------|
| 1 | Brachydactyly-Syndactyly Syndrome | 99.99% | 骨発育異常 |
| 2 | Colobomatous Microphthalmia-Rhizomelic Dysplasia Syndrome | 99.99% | 骨発育異常 |
| 3 | Brachyolmia-Amelogenesis Imperfecta Syndrome | 99.99% | 骨発育異常 |
| 4 | Acromesomelic Dysplasia, Hunter-Thompson Type | 99.99% | 骨発育異常 |
| 5 | Myosclerosis | 99.99% | 筋疾患 |
| 6 | Spondyloarthropathy, Susceptibility to | 99.99% | 脊椎関節症 |
| 7 | Brachyolmia | 99.99% | 骨発育異常 |
| 8 | Factor 5 Excess with Spontaneous Thrombosis | 99.98% | 凝固異常 |
| 9 | Heparin Cofactor 2 Deficiency | 99.98% | 凝固異常 |
| 10 | Pseudoachondroplasia | 99.98% | 骨発育異常 |

**パターンの観察：** 予測結果は、骨発育不全および関連する遺伝性疾患に高度に集中しています。

## この予測が妥当な理由

Tiaprofenic Acid は **非ステロイド性抗炎症薬（NSAID）** で、プロピオン酸誘導体に属します。

**想定される作用機序の推測：**
1. **COX 阻害作用**：シクロオキシゲナーゼを阻害してプロスタグランジンの合成を減らし、骨リモデリングの過程に影響する可能性があります
2. **軟骨保護仮説**：NSAID が軟骨代謝に影響を与える可能性を示す研究もあります
3. **抗炎症作用**：骨発育異常に関連する炎症反応を緩和する可能性があります

**重要な注意：**
- 予測された疾患の多くは希少な遺伝性疾患で、主に骨・軟骨の発育に関わる遺伝子変異が関与しています
- NSAID は遺伝子の欠陥を是正できず、症状緩和にとどまる可能性があります
- 現時点では、この予測を裏付ける文献や臨床エビデンスはありません

## 臨床試験エビデンス

予測された 10 件の適応症すべてについて、関連する臨床試験の登録はありません。

## 文献エビデンス

| 疾患 | PubMed 文献数 | ClinicalTrials.gov | ICTRP |
|-----|--------------|-------------------|-------|
| 予測新適応症 10 件すべて | 0 件 | 0 件 | 0 件 |

**結論：** 裏付けとなるエビデンスは全くありません。

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

**NSAID 類に共通するリスク：**
- 消化管出血および潰瘍
- 心血管リスク（長期使用時）
- 腎機能への影響
- 過敏反応

**Tiaprofenic Acid に特有の注意：**
- 膀胱刺激症状（cystitis-like symptoms）：海外で報告例があります
- 泌尿器症状に注意が必要です

**薬物相互作用：**
- 今回のデータ収集では、特定の相互作用の記録は確認されませんでした
- NSAID 類の標準的な相互作用（抗凝固薬、他の NSAID、ACE 阻害薬など）を参照すべきです

## 結論と次のステップ

**判断：Hold**

**理由：**
1. いずれの予測適応症についても、それを裏付ける臨床試験や文献のエビデンスが全くありません
2. 予測された疾患の多くは希少な遺伝性疾患であり、NSAID の作用機序では有効性を説明しにくいです
3. 対象疾患の患者集団が極めて小さく、臨床開発の難度が高いです
4. この予測は、希少疾患の予測における TxGNN の限界を反映している可能性があります

**推進に必要な事項：**
- Tiaprofenic Acid が骨・軟骨細胞に与える影響を検証する前臨床研究
- 希少疾患の動物モデルでの有効性評価
- 遺伝学の専門家と連携した、作用機序の妥当性の評価
- オーファンドラッグとしての開発経路の実現可能性の検討

**薬剤師からの提言：**
この予測の臨床応用上の価値は低く、よりエビデンスの基盤がある他の候補薬を優先して注目することを推奨します。


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
