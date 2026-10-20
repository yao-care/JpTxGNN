---
layout: default
title: Sodium Citrate
parent: 中エビデンス (L3-L4)
nav_order: 158
evidence_level: L3
indication_count: 1
last_modified_at: 2026-04-19
description: "Sodium Citrate：予測新適応症は胃疾患（stomach disease）、胃十二指腸炎（gastroduodenitis）（エビデンスレベル L3）。既存適応症：日本の承認適応症は本サイトのデータに未収載、peptic esophagitis、dyspepsia、pharyngitis）"
---

# Sodium Citrate
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

# クエン酸ナトリウム（Sodium Citrate）：抗凝固薬から胃疾患の補助療法への探索

## 一言まとめ

Sodium Citrate は主に抗凝固薬および去痰薬として使用されており、TxGNN は胃疾患に対する補助療法としての可能性を予測している。胃癌の抑制および胃粘膜保護に関する作用を支持する文献が複数ある。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：peptic ulcer disease、gastroesophageal reflux disease、esophagitis (disease)、peptic esophagitis、dyspepsia、pharyngitis） |
| 予測新適応症 | 胃疾患（stomach disease）、胃十二指腸炎（gastroduodenitis） |
| TxGNN 予測スコア | 0.999（stomach disease） |
| エビデンスレベル | L3（PubMed 文献および臨床試験が複数あり） |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Watch |

## この予測が妥当な理由

### 胃疾患（Stomach Disease）- TxGNN スコア 0.999

**作用機序の仮説：**
Sodium Citrate は解糖系（glycolysis）を抑制することで腫瘍細胞の増殖を抑える。ホスホフルクトキナーゼ（phosphofructokinase, PFK）の活性を抑制し、ATP および乳酸の産生を減少させ、ミトコンドリア介在性のアポトーシス経路を誘導することが研究で示されている。

**文献による裏付け：**
1. **2016 年 Biochemical and Biophysical Research Communications（PMID: 27163639）**：Sodium Citrate が、解糖系の阻害とミトコンドリアアポトーシス経路の促進を介して、ヒト胃癌細胞株 MGC-803 の増殖を抑制することを確認した。

2. **2016 年 Oncology Reports（PMID: 26708213）**：胃癌の同所移植腫瘍モデルにおいて、Sodium Citrate は腫瘍の増殖を抑制し、アポトーシスを誘導するとともに、抗アポトーシスタンパク質 Survivin を下方制御した。

3. **2018 年 Oncology Reports（PMID: 29115645）**：18F-FDG PET/CT 画像を用いて、Sodium Citrate が生体内で胃癌の解糖系代謝と腫瘍の増殖を抑制することを確認した。

### 胃十二指腸炎（Gastroduodenitis）- TxGNN スコア 0.996

**作用機序の仮説：**
Sodium Citrate は胃内 pH を調節し、胃粘膜に対する保護作用を示す。

**文献による裏付け：**
- 1991 年の研究（PMID: 1777551）では、Sodium Citrate と glucose の配合により、非ステロイド性抗炎症薬による消化管障害を軽減できることが示された。
- 1999 年の研究（PMID: 10499455）では、monosodium citrate を含む発泡錠に制酸能があり、胃酸逆流症状を速やかに緩和すると指摘されている。

## 臨床試験

Sodium Citrate と胃疾患に関連する臨床試験は多数あり、主に以下に集中している：

| 試験番号 | タイトル | 相 | 状態 |
|---------|------|------|------|
| NCT03050359 | 十二指腸潰瘍に対する TAK-438 vs Lansoprazole | Phase 3 | 完了 |
| NCT03050307 | 胃潰瘍に対する TAK-438 vs Lansoprazole | Phase 3 | 完了 |
| NCT02891447 | 胃癌に対する腫瘍減量手術と HIPEC | Phase 2 | 完了 |
| NCT05753306 | ロボット支援下胃癌 HIPEC 手術 | Phase 2 | 募集中 |

## 関連文献

| PMID | タイトル | 発表年 | 関連性 |
|------|------|------|--------|
| 27163639 | 3-Bromopyruvate and sodium citrate induce apoptosis in gastric cancer | 2016 | 高 |
| 26708213 | Sodium citrate target glycolysis in gastric cancer cells | 2016 | 高 |
| 29115645 | 18F-FDG PET/CT evaluation of glycolysis-targeted therapy | 2018 | 高 |
| 35934181 | 5-ALA and sodium ferrous citrate in gastric cancer | 2022 | 中 |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **警告・禁忌**：詳細な添付文書情報はなし
- **薬物相互作用**：既知の重大な薬物相互作用に関するデータは見つかっていない
- **特殊集団**：
  - 高用量では代謝性アルカローシスを来すおそれがある
  - 他の電解質との相互作用に注意が必要

**備考**：Sodium Citrate は抗凝固薬および補助剤としての安全性は良好であるが、抗腫瘍への応用では用量および投与経路についてさらなる評価が必要である。

## 結論と次のステップ

**判断：Watch**

**理由：**
TxGNN の予測スコアは極めて高く（0.999）、Sodium Citrate が胃癌細胞を抑制する機序を支持する質の高い in vitro 試験および動物実験の文献が複数ある。しかし、現時点のエビデンスは基礎研究段階にとどまり、この適応症を対象としたヒト臨床試験はまだない。

**推進に必要な事項：**
- ヒトにおける安全な抗腫瘍用量の確立
- 経口投与または静脈内投与の実現可能性の評価
- Phase I 安全性試験の設計
- 既存の胃癌化学療法薬との相乗作用の探索
- 単独療法ではなく、化学療法の増感剤としての位置づけの検討


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
