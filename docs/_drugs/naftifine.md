---
layout: default
title: Naftifine
parent: 高エビデンス (L1-L2)
nav_order: 108
evidence_level: L1
indication_count: 1
---

# Naftifine
{: .fs-9 }

エビデンスレベル: **L1** | 予測適応症: **1** 件
{: .fs-6 .fw-300 }

---

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist">

## 薬剤師評価レポート

</div>

# Naftifine：從 皮膚黴菌病 到 皮膚念珠菌病

## 一言まとめ

Naftifine（萘替芬）是一種烯丙胺類局部抗黴菌藥，用於治療皮膚黴菌感染。TxGNN 模型預測它對**皮膚念珠菌病 (cutaneous candidiasis)** 和**花斑癬 (pityriasis versicolor)** 有治療效果，這些預測與其已核准適應症高度一致，有充分文獻支持。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 皮膚黴菌病、表皮念珠菌病、甲黴菌病、花斑癬 |
| 予測新適応症 | 皮膚念珠菌病、花斑癬、Majocchi 肉芽腫 |
| TxGNN 予測スコア | 99.84% (皮膚念珠菌病), 99.68% (花斑癬) |
| エビデンスレベル | L1 |
| 日本上市 | 已上市 |
| 承認数 | 多張 |
| 推奨判断 | Validate |

## この予測が妥当な理由

Naftifine 通過抑制角鯊烯環氧化酶（squalene epoxidase），阻斷麥角固醇合成，破壞真菌細胞膜完整性。

**機轉支持：**
- 對皮膚真菌病（dermatophytes）具有強效殺菌活性
- 對念珠菌屬（Candida spp.）具有抑菌活性
- 對馬拉色菌（Malassezia）有效，可治療花斑癬
- 具有輕微抗發炎作用

這些預測適應症實際上已包含在台灣核准適應症中，TxGNN 的預測與現有臨床應用一致。

## 臨床試験エビデンス

雖無專門的 RCT 登記，但多項開放性研究已證實療效。

## 文献エビデンス

**皮膚念珠菌病：**

| PMID | 年份 | 類型 | 主要發現 |
|------|-----|------|---------|
| [3048914](https://pubmed.ncbi.nlm.nih.gov/3048914/) | 1988 | RCT | 雙盲試驗：77% 的 naftifine 治療患者達成真菌學治癒，對照組僅 3% |
| [1723367](https://pubmed.ncbi.nlm.nih.gov/1723367/) | 1991 | Review | 綜述確認 naftifine 對皮膚念珠菌病有效 |
| [18346400](https://pubmed.ncbi.nlm.nih.gov/18346400/) | 2008 | Review | 確認 naftifine 對念珠菌和曲霉菌有效 |

**花斑癬：**

| PMID | 年份 | 類型 | 主要發現 |
|------|-----|------|---------|
| [3531847](https://pubmed.ncbi.nlm.nih.gov/3531847/) | 1986 | Clinical Trial | Naftifine 1% 溶液治療花斑癬的療效研究 |
| [22165042](https://pubmed.ncbi.nlm.nih.gov/22165042/) | 2011 | Open-label Study | Naftifine 1% 凝膠每日兩次治療花斑癬 2 週，8 週時 50% 達真菌學陰性 |
| [8370053](https://pubmed.ncbi.nlm.nih.gov/8370053/) | 1993 | Laboratory/Clinical | 確認 naftifine 對皮膚真菌病和花斑癬的療效 |

## 日本上市情報

| 承認番号 | 品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 多張許可證 | 鹽酸萘替芬 | 乳膏/溶液 | 皮膚真菌病、表皮念珠菌病、甲黴菌病、花斑癬 |

## 安全性に関する考慮事項

**常見副作用：**
- 局部灼熱感（6.8%）
- 局部刺激
- 皮膚乾燥
- 紅斑

**禁忌症：**
- 對 naftifine 或其他烯丙胺類藥物過敏

**使用注意：**
- 僅供外用
- 避免接觸眼睛和黏膜
- 如出現明顯刺激應停藥

## 結論と次のステップ

**判断：Validate**

**理由：**
TxGNN 預測的「皮膚念珠菌病」和「花斑癬」實際上已是 naftifine 在台灣的核准適應症（「表皮念珠菌病」和「花斑癬」）。文獻提供了充分的療效證據。此預測更多是對現有適應症的確認，而非新發現。

**推進に必要な事項：**
- 此藥物已被核准用於預測適應症
- 無需額外驗證研究
- 可直接依據仿單使用


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
