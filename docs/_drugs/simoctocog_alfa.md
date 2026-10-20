---
noindex: true
sitemap: false
layout: default
title: Simoctocog Alfa
parent: モデル予測のみ (L5)
nav_order: 156
evidence_level: L5
indication_count: 1
last_modified_at: 2026-09-17
---

# Simoctocog Alfa
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

# Simoctocog Alfa：A型血友病からその他の出血性疾患への探索

## 一言まとめ

Simoctocog Alfa（シモクトコグ アルファ）（Nuwiq）は、A型血友病の治療に用いられる遺伝子組換え第VIII因子製剤です。
TxGNNモデルは、本剤が**偽性フォン・ヴィレブランド病（Pseudo-von Willebrand Disease）**をはじめとする血小板・凝固機能異常の疾患に有効な可能性があると予測しています。
ただし、これらの新規適応症を裏付ける臨床試験や文献は現時点でありません。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：hemophilia、symptomatic form of hemophilia in female carriers） |
| 予測新適応症 | Pseudo-von Willebrand Disease（偽性フォン・ヴィレブランド病） |
| TxGNN 予測スコア | 99.997% |
| エビデンスレベル | L5 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Hold |

## この予測が妥当な理由

Simoctocog Alfaは遺伝子組換え第VIII因子（FVIII）製剤で、ヒト胎児腎細胞（HEK293）で産生されます。
A型血友病患者で欠乏している凝固因子を補充するために用いられます。作用機序は次のとおりです。
- 補因子として活性化第九因子（FIXa）と結合する
- 第十因子（FX）の活性化を促進する
- 最終的に凝固カスケードを完了させ、止血を促す

**TxGNNが予測した新規適応症の上位十件：**

| 順位 | 予測適応症 | 予測スコア | TxGNN 順位 | 作用機序との関連性 |
|------|-----------|---------|-----------|----------|
| 1 | Pseudo-von Willebrand Disease（偽性フォン・ヴィレブランド病） | 99.997% | 164 | 中等度 |
| 2 | Primary Release Disorder of Platelets（血小板放出機構の原発性障害） | 99.997% | 179 | 低 |
| 3 | Glanzmann Thrombasthenia（グランツマン血小板無力症） | 99.995% | 307 | 低 |
| 4 | Scott Syndrome（スコット症候群） | 99.969% | 1,244 | 中等度 |
| 5 | Acquired Coagulation Factor Deficiency（後天性凝固因子欠乏症） | 99.952% | 1,615 | 高 |
| 6 | Bleeding Diathesis due to Collagen Receptor Defect | 99.921% | 2,285 | 低 |
| 7 | Hemorrhagic Disorder due to Constitutional Thrombocytopenia | 99.917% | 2,394 | 低 |
| 8 | Fetal and Neonatal Alloimmune Thrombocytopenia | 99.845% | 3,964 | 低 |
| 9 | Hemophilia A with Vascular Abnormality | 99.779% | 5,200 | 高 |
| 10 | Thrombotic Thrombocytopenic Purpura（血栓性血小板減少性紫斑病） | 99.724% | 6,173 | 低 |

**作用機序の分析：**
- 偽性フォン・ヴィレブランド病、後天性凝固因子欠乏症、血管異常を伴うA型血友病：FVIII補充療法との関連が比較的強い
- 血小板機能障害性の疾患（グランツマン血小板無力症、スコット症候群など）：これらは主に血小板自体の欠陥による疾患であるため、FVIII補充療法の有効性は不明確

## 臨床試験エビデンス

予測適応症に関する臨床試験の登録は現時点でありません。

## 文献エビデンス

予測適応症に関するPubMed文献は現時点でありません。

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **既知の副作用**：
  - 抑制性抗体（FVIIIインヒビター）の産生
  - 過敏反応
  - 注射部位反応

- **薬物相互作用**：
  - 既知の重大な薬物相互作用はなし

- **特殊集団**：
  - 用量は体重および出血の重症度に応じて調整が必要
  - 詳細は添付文書を参照

安全性情報は添付文書をご参照ください。

## 結論と次のステップ

**判断：Hold**

**理由：**
TxGNNが予測した新規適応症のうち、後天性凝固因子欠乏症と血管異常を伴うA型血友病は、Simoctocog Alfaの作用機序と直接的な関連があります。
一方、血小板機能障害性疾患の予測はFVIII補充療法の作用機序との関連性が弱く、現時点では臨床的エビデンスによる裏付けがありません。

**推進に必要な事項：**
- 後天性FVIII欠乏症に関する臨床データの収集
- 偽性フォン・ヴィレブランド病におけるSimoctocog Alfaの応用の探索
- 抑制性抗体産生リスクが比較的低い状況での、他の出血性疾患への拡大の実現可能性の評価
- 他のFVIII製剤との比較研究


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
