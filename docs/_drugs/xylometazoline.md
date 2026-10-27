---
layout: default
title: Xylometazoline
parent: 中エビデンス (L3-L4)
nav_order: 199
evidence_level: L3
indication_count: 1
last_modified_at: 2026-09-17
description: "Xylometazoline：予測新適応症は鼻腔疾患、急性咽喉頭炎（エビデンスレベル L3）。既存適応症：日本の承認適応症は本サイトのデータに未収載"
---

# Xylometazoline：アレルギー性鼻炎から鼻腔疾患までの幅広い応用
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

## Xylometazoline：アレルギー性鼻炎から鼻腔疾患までの幅広い応用
{: .text-alpha }

## 一言まとめ

Xylometazoline（キシロメタゾリン） はもともと、鼻閉やアレルギー性鼻炎などの症状の緩和に用いられています。
TxGNN モデルは、本剤が**鼻腔疾患 (nasal cavity disease)** と**急性咽喉頭炎 (acute laryngopharyngitis)** に有効である可能性を予測しています。
鼻腔疾患の方向性については、**2 件の臨床試験**と **7 件の文献**が裏付けています。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：pharyngitis、common cold） |
| 予測新適応症 | 鼻腔疾患、急性咽喉頭炎 |
| TxGNN 予測スコア | 99.91% (鼻腔疾患)、99.89% (急性咽喉頭炎) |
| エビデンスレベル | L3 (文献による裏付けあり) |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Xylometazoline は alpha アドレナリン受容体作動薬で、鼻粘膜の血管に作用し、
血管を収縮させることで鼻腔の充血を軽減します。作用標的は次のとおりです。

- **alpha-1D アドレナリン受容体** (ADRA1D)
- **alpha-2A アドレナリン受容体** (ADRA2A)
- **alpha-2B アドレナリン受容体** (ADRA2B)
- **alpha-2C アドレナリン受容体** (ADRA2C)

本剤は鼻腔に作用する血管収縮薬であるため、鼻腔疾患に有効と予測されることは作用機序の上で十分に妥当です。
この予測は、真の意味での「ドラッグ・リポジショニング」というよりも、既存適応症の延長を確認するものに近いといえます。

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 人数 | 主な知見 |
|---------|------|------|------|---------|
| [NCT05072392](https://clinicaltrials.gov/study/NCT05072392) | N/A | UNKNOWN | 80 | 成人患者の鼻出血に対する、Foley カテーテルを用いた経鼻挿管補助の影響を検討 |
| [NCT06443255](https://clinicaltrials.gov/study/NCT06443255) | Phase 3 | COMPLETED | 16 | 鼻腔の鎮痛効果について、cocaine、lidocaine/xylometazoline、生理食塩水を比較 |

## 文献エビデンス

| PMID | 年 | 種類 | 雑誌 | 主な知見 |
|------|-----|------|------|---------|
| [24023995](https://pubmed.ncbi.nlm.nih.gov/24023995/) | 2013 | 臨床研究 | Korean J Anesthesiol | Xylometazoline の噴霧は鼻腔を効果的に拡張する |
| [8740084](https://pubmed.ncbi.nlm.nih.gov/8740084/) | 1996 | RCT | Arzneimittel-Forschung | 鼻腔抵抗の低減効果について、tuaminoheptane/NAC と xylometazoline を比較 |
| [34783482](https://pubmed.ncbi.nlm.nih.gov/34783482/) | 2021 | レビュー | Vestn Otorinolaringol | 0.1% xylometazoline と 5% dexpanthenol の併用により、高齢者の鼻粘膜の再生が改善しうる |
| [22427029](https://pubmed.ncbi.nlm.nih.gov/22427029/) | 2013 | RCT | Eur Arch Otorhinolaryngol | 鼻内視鏡検査前の準備として、綿塞栓による充填と局所噴霧の効果を比較 |
| [1281924](https://pubmed.ncbi.nlm.nih.gov/1281924/) | 1992 | 臨床研究 | Rhinology | Xylometazoline は鼻気道抵抗を有意に低下させ、左右差を解消しうる |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **薬物相互作用**：alpha アドレナリン受容体に作用するため、他の交感神経作動薬との併用には注意が必要です。
- **使用上の制限**：薬剤性鼻炎 (rhinitis medicamentosa) を避けるため、連続使用は 7 日を超えないようにします。
- **禁忌**：閉塞隅角緑内障や重度の高血圧の患者には、慎重に使用する必要があります。

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
Xylometazoline の鼻腔疾患への応用は、本来の適応症と高い関連性があり、作用機序が明確で、十分な臨床的エビデンスの裏付けがあります。
予測された「鼻腔疾患」は、実際には本来の適応症を一般化した表現であり、臨床ではすでに広く使用されています。

**推進に必要な事項：**
- 急性咽喉頭炎の適応症については、追加の臨床的エビデンスが必要
- 特定の鼻腔疾患サブタイプに対する有効性の評価
- 長期使用時の安全性モニタリング


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
