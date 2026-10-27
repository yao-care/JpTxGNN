---
noindex: true
sitemap: false
layout: default
title: Salicylic Acid
parent: モデル予測のみ (L5)
nav_order: 153
evidence_level: L5
indication_count: 1
last_modified_at: 2026-09-17
---

# Salicylic Acid
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

## Salicylic Acid：皮膚科用薬から眼科および骨格疾患への探索
{: .text-alpha }

## 一言まとめ

Salicylic Acid（サリチル酸） は主に角質溶解剤、抗真菌外用薬および鎮痛解熱薬として用いられる。
TxGNN モデルは、本剤が**乳頭状結膜炎 (Papillary Conjunctivitis)** などの眼科疾患および骨格疾患に有効である可能性を予測しているが、
現時点ではこれらの新適応症を裏付ける臨床試験および文献は存在しない。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：tinea pedis、synovitis (disease)、tenosynovitis、rheumatoid arthritis、allergic rhinitis、vasomotor rhinitis） |
| 予測新適応症 | Papillary Conjunctivitis |
| TxGNN 予測スコア | 99.88% |
| エビデンスレベル | L5 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Hold |

## この予測が妥当な理由

現時点では、詳細な作用機序に関するデータは乏しい。既知の情報によれば、Salicylic Acid は広く使用されている皮膚科用薬であり、
その角質軟化作用および抗炎症作用の機序は確認されている。Salicylic Acid は COX 酵素を阻害することで抗炎症効果を示す可能性があり、
同時に ASIC3 イオンチャネルとも相互作用すると考えられている。

**TxGNN が予測した新適応症の上位五位：**

| 排名 | 予測適応症 | 予測分数 | TxGNN 排名 |
|------|-----------|---------|-----------|
| 1 | Papillary Conjunctivitis（乳頭状結膜炎） | 99.88% | 3,238 |
| 2 | Colobomatous Microphthalmia-Rhizomelic Dysplasia Syndrome | 99.78% | 5,166 |
| 3 | Brachydactyly-Syndactyly Syndrome | 99.73% | 6,122 |
| 4 | Brachyolmia-Amelogenesis Imperfecta Syndrome | 99.55% | 9,127 |
| 5 | Rosacea Conjunctivitis（酒さ性結膜炎） | 99.53% | 9,298 |

しかし、これらの予測は主に希少遺伝性疾患または眼科疾患であり、Salicylic Acid の既知の皮膚科領域における作用機序との関連性は明確ではなく、
検証には更なる機序研究が必要である。

## 臨床試験エビデンス

予測新適応症に関する臨床試験の登録は現時点で確認されていない。

## 文献エビデンス

予測新適応症に関する PubMed 文献は現時点で確認されていない。

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **薬物相互作用**：
  - ASIC3（酸感受性イオンチャネル3）と相互作用する（出典：Guide to PHARMACOLOGY）

- **臨床使用上の注意**：
  - 尋常性痤瘡、乾癬、鶏眼、疣贅などの皮膚疾患に対する外用療法に広く用いられる
  - CAS 番号：69-72-7

安全性情報は添付文書をご参照ください。

## 結論と次のステップ

**判断：Hold**

**理由：**
TxGNN が予測した新適応症（乳頭状結膜炎、希少な骨格発育疾患）は、Salicylic Acid の既知の皮膚科領域における作用機序との明確な関連が乏しい。
現時点では、これらの予測を裏付ける臨床試験および文献は存在しない。

**推進に必要な事項：**
- Salicylic Acid の眼科疾患に対する作用機序の可能性を明らかにする
- 結膜炎適応症に対する前臨床研究
- 抗炎症機序の眼科領域への応用可能性の検討


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
