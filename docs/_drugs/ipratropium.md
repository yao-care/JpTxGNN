---
layout: default
title: Ipratropium
parent: 高エビデンス (L1-L2)
nav_order: 91
evidence_level: L1
indication_count: 1
last_modified_at: 2026-09-17
description: "Ipratropium：予測新適応症は閉塞性肺疾患 (obstructive lung disease)（エビデンスレベル L1）。既存適応症：日本の承認適応症は本サイトのデータに未収載"
---

# Ipratropium
{: .fs-9 }

エビデンスレベル: **L1** | 予測適応症: **1** 件
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

## Ipratropium：閉塞性気道疾患から閉塞性肺疾患へ
{: .text-alpha }

## 一言まとめ

Ipratropium（イプラトロピウム臭化物）は抗コリン性の気管支拡張薬で、慢性閉塞性肺疾患および気管支喘息の治療に用いられます。TxGNN モデルは、本剤が**閉塞性肺疾患 (obstructive lung disease)** に対して治療効果を持つ可能性があると予測しており、現在、この予測を裏付ける **40 件超の臨床試験**があります。エビデンスレベルは極めて高い水準です。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：chronic obstructive pulmonary disease、COPD, severe early onset、allergic rhinitis、vasomotor rhinitis、bronchitis、common cold） |
| 予測新適応症 | 閉塞性肺疾患 (obstructive lung disease) |
| TxGNN 予測スコア | 99.97% |
| エビデンスレベル | L1 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Validate |

## この予測が妥当な理由

Ipratropium は短時間作用型の抗コリン薬で、気管支平滑筋の M3 受容体に対するアセチルコリンの作用を遮断することで、気管支拡張効果を発揮します。本来の適応症にはすでに COPD と喘息が含まれており、予測された「閉塞性肺疾患」は本質的に本来の適応症と大きく重なっています。

**作用機序による裏付け：**
- 抗コリン作用により気道平滑筋が直接弛緩する
- 気道分泌物が減少する
- β2 刺激薬との併用により相乗効果が得られる

この予測は、薬剤と疾患カテゴリーの自然な関連性を反映したものであり、適応症の拡張または細分化にあたります。

## 臨床試験エビデンス

現在、関連する臨床試験は 40 件を超えており、以下のようなものがあります：

| 試験番号 | 相 | 状態 | 主な知見 |
|---------|------|------|---------|
| NCT00371527 | N/A | 完了 | 急性気管支炎の症状コントロール効果を評価 |
| NCT00583778 | N/A | 完了 | Levalbuterol + Ipratropium と Levalbuterol 単独使用の比較 |
| NCT02260011 | Phase 2 | 完了 | Ipratropium bromide HFA と Atrovent CFC の比較 |
| NCT00239434 | Phase 3 | 完了 | COPD における Tiotropium と Ipratropium の比較 |
| NCT00794157 | Phase 3 | 完了 | 中等症〜重症 COPD における Indacaterol の効果 |
| NCT02542254 | Phase 2 | 完了 | Ipratropium に RPL554 を追加した場合の気管支拡張効果 |

複数の試験で、COPD および閉塞性肺疾患における ipratropium の有効性が示されています。

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

**主な副作用：**
- 口渇
- 頭痛
- 咳嗽
- 悪心

**禁忌：**
- アトロピンまたはその誘導体に対する過敏症
- 閉塞隅角緑内障
- 尿閉を伴う前立腺肥大

**薬物相互作用：**
- 他の抗コリン薬との併用により副作用が増強するおそれがある
- β2 刺激薬：気管支拡張効果の相乗作用

## 結論と次のステップ

**判断：Validate**

**理由：**
TxGNN が予測した「閉塞性肺疾患」は、ipratropium の中核的な適応症とほぼ一致しています。40 件を超える臨床試験により、有効性と安全性について十分なエビデンスが得られています。この予測は、既存適応症の確認と細分化という性格が強く、真の意味でのドラッグ・リポジショニングによる新発見ではありません。

**推進に必要な事項：**
- 本剤は閉塞性肺疾患に対してすでに十分に検証されている
- 既存の臨床ガイドラインを直接参照して使用できる
- 追加の検証研究は不要


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
