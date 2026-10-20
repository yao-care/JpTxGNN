---
layout: default
title: Ritonavir
parent: 中エビデンス (L3-L4)
nav_order: 148
evidence_level: L4
indication_count: 1
last_modified_at: 2026-09-17
description: "Ritonavir：予測新適応症はサル免疫不全ウイルス感染症 (SIV Infection)、ネコ後天性免疫不全症候群（エビデンスレベル L4）。既存適応症：日本の承認適応症は本サイトのデータに未収載"
---

# Ritonavir
{: .fs-9 }

エビデンスレベル: **L4** | 予測適応症: **1** 件
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

# Ritonavir：HIVからサル免疫不全ウイルス感染症へ

## 一言まとめ

Ritonavir（リトナビル） はHIVプロテアーゼ阻害薬で、もともとヒト免疫不全ウイルス（HIV）感染症の治療に用いられています。TxGNN モデルは、本剤が**サル免疫不全ウイルス感染症 (Simian Immunodeficiency Virus Infection)** に有効である可能性を予測しており、現在、この方向性を支持する**複数の文献**があります。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：chronic hepatitis C virus infection、hepatitis C virus infection、HIV infectious disease、AIDS） |
| 予測新適応症 | サル免疫不全ウイルス感染症 (SIV Infection)、ネコ後天性免疫不全症候群 |
| TxGNN 予測スコア | 99.92% |
| エビデンスレベル | L4 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Ritonavir はHIVプロテアーゼ阻害薬で、主にHIV治療に用いられます。現在は通常、薬物動態増強薬（ブースター）として、他のプロテアーゼ阻害薬（darunavir、lopinavir など）と併用され、併用薬の血中濃度を高める目的で使われています。

サル免疫不全ウイルス（SIV）はHIVの近縁ウイルスで、非ヒト霊長類においてAIDS様疾患を引き起こします。SIV は、HIV感染や抗ウイルス薬を研究するうえで重要な動物モデルです。SIV と HIV のプロテアーゼは構造が類似しているため、HIVプロテアーゼに対する阻害薬は SIV に対しても活性を示す可能性があります。

文献研究により、以下が確認されています：
1. Ritonavir は in vitro で SIVmac239 に対して阻害活性を示す
2. ritonavir ブースト lopinavir を含む多剤併用療法は、SIV 感染アカゲザルの体内ウイルス量を効果的に抑制できる
3. SIV/SHIV 動物モデルは、抗レトロウイルス薬を評価するための重要なツールである

## 臨床試験エビデンス

SIV 感染を対象としたヒトでの臨床試験は現時点ではありません（SIV はヒトに感染しないため）。

## 文献エビデンス

| PMID | 年 | 種類 | 雑誌 | 主な所見 |
|------|-----|------|------|---------|
| [12709355](https://pubmed.ncbi.nlm.nih.gov/12709355/) | 2003 | Journal Article | Antimicrob Agents Chemother | SIVmac239 の ritonavir に対する感受性（EC50: 13 nM） |
| [16973590](https://pubmed.ncbi.nlm.nih.gov/16973590/) | 2006 | Journal Article | J Virol | SIV 感染マカクにおける四剤抗レトロウイルス療法による急速なウイルス減少 |
| [22737073](https://pubmed.ncbi.nlm.nih.gov/22737073/) | 2012 | Journal Article | PLoS Pathog | 高強度 ART により SIV ウイルス量を長期に抑制し、ウイルスリザーバーを制限 |
| [34903055](https://pubmed.ncbi.nlm.nih.gov/34903055/) | 2021 | Journal Article | mBio | 有効な ART にもかかわらず、レンチウイルス感染が脳内に持続 |
| [17350308](https://pubmed.ncbi.nlm.nih.gov/17350308/) | 2007 | Journal Article | Microbes Infect | SHIV-pr の構築とプロテアーゼ阻害薬感受性の生体内評価 |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

**主要な警告：**
- 薬物相互作用：Ritonavir は CYP3A4 の強力な阻害薬であり、多くの薬剤と顕著な相互作用を示す
- 肝毒性
- 脂質代謝異常

**禁忌：**
製造販売元の添付文書を参照してください

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
SIV は HIV の近縁ウイルスであり、ritonavir による SIV プロテアーゼの阻害活性が in vitro および動物モデルで確認されていることから、この予測は科学的に妥当です。ただし、SIV はヒトに感染しないため、この予測の主な応用先は獣医学領域（霊長類）、またはHIV研究における動物モデルのツールです。

**推進に必要な事項：**
- 主に獣医学・動物研究への応用である
- SIV 感染の非ヒト霊長類における有効性と安全性を評価する
- HIV研究のツールとしては、すでに十分な応用基盤がある
- ネコ免疫不全ウイルス（FIV）による猫エイズについては、追加の種間交差反応性の研究が必要


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
