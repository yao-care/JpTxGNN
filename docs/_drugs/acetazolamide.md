---
layout: default
title: Acetazolamide
parent: 高エビデンス (L1-L2)
nav_order: 11
evidence_level: L2
indication_count: 1
last_modified_at: 2026-09-17
description: "Acetazolamide：予測新適応症は心筋症 (cardiomyopathy)（エビデンスレベル L2）。既存適応症：日本の承認適応症は本サイトのデータに未収載"
---

# Acetazolamide
{: .fs-9 }

エビデンスレベル: **L2** | 予測適応症: **1** 件
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

# Acetazolamide：緑内障・利尿から心筋症への探索

## 一言まとめ

Acetazolamide は本来、緑内障および利尿に用いられてきた薬剤である。
TxGNN モデルは、本剤が**心筋症 (cardiomyopathy)** および**肥大型心筋症 (hypertrophic cardiomyopathy)** に有効である可能性を予測しており、
現在 **3 件の臨床試験**と **10 件の文献**がこの方向性を支持している。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：absence epilepsy、congestive heart failure、open-angle glaucoma、angle-closure glaucoma、closed-angle glaucoma、altitude sickness） |
| 予測新適応症 | 心筋症 (cardiomyopathy) |
| TxGNN 予測スコア | 99.83% |
| エビデンスレベル | L2 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Acetazolamide は炭酸脱水酵素阻害薬であり、従来は緑内障および利尿に用いられてきた。近年の研究により、急性非代償性心不全における本剤の有用性が顕著に高まっていることが明らかになった。

ADVOR 試験 (2022) では、acetazolamide をループ利尿薬に追加することで、急性心不全患者のうっ血解除効果が有意に改善することが示された。その作用機序には以下が含まれる。
1. 近位尿細管の炭酸脱水酵素を阻害し、ナトリウム排泄を増加させる
2. 利尿薬抵抗性を克服する
3. 電解質バランス（特に塩化物イオン）を調節する

心筋症患者では心不全症状を伴うことが多く、acetazolamide の補助的利尿薬としての役割は臨床的に検証済みである。また、2018 年の日本の症例報告では、acetazolamide を肥大型心筋症に低クロール血症を合併した患者の治療に用いることができると示されている。

## 臨床試験エビデンス

| 試験番号 | 段階 | 状態 | 人数 | 主な所見 |
|---------|------|------|------|---------|
| [NCT05802849](https://clinicaltrials.gov/study/NCT05802849) | Phase 4 | RECRUITING | 400 | 心筋症を含む非代償性心不全における acetazolamide 経口投与の有効性を評価 |
| [NCT06166654](https://clinicaltrials.gov/study/NCT06166654) | Phase 4 | RECRUITING | 939 | 急性心不全の体液過剰に対する、ループ利尿薬への Metolazone または Acetazolamide 併用の効果を比較 |
| [NCT06092437](https://clinicaltrials.gov/study/NCT06092437) | N/A | RECRUITING | 466 | TAILOR-AHF：尿中ナトリウム指標に基づく利尿薬アルゴリズムの研究 |

## 文献エビデンス

| PMID | 年 | 種類 | 雑誌 | 主な所見 |
|------|-----|------|------|---------|
| [38806171](https://pubmed.ncbi.nlm.nih.gov/38806171/) | 2025 | Review | ESC heart failure | 2024 年心不全アップデート：acetazolamide とループ利尿薬の併用療法を支持 |
| [37169875](https://pubmed.ncbi.nlm.nih.gov/37169875/) | 2023 | Journal Article | Eur Heart J Cardiovasc Pharmacother | 2022 年の心血管薬理学の進展レビュー。acetazolamide とループ利尿薬の併用が標準治療に組み入れられた |
| [30279861](https://pubmed.ncbi.nlm.nih.gov/30279861/) | 2018 | Case Report | J Cardiol Cases | 低クロール血症を合併した肥大型心筋症で、acetazolamide の使用により電解質の補正に成功 |
| [742352](https://pubmed.ncbi.nlm.nih.gov/742352/) | 1978 | Journal Article | Acta Neurol Scand | 低カリウム性周期性麻痺と心筋症との関連に関する研究 |
| [7324871](https://pubmed.ncbi.nlm.nih.gov/7324871/) | 1981 | Case Report | Acta Neurol Scand | 家族性低カリウム性周期性麻痺における心筋疾患の所見 |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

### 重要な薬物相互作用

**Major 相互作用：**
- Aspirin（高用量）：acetazolamide の毒性リスクを増加させ、代謝性アシドーシスを引き起こす可能性がある

**Moderate 相互作用：**
- 血糖降下薬（各種経口血糖降下薬、インスリン）：血糖コントロールに影響する可能性がある
- Amphotericin B：低カリウム血症のリスクを増加させる
- ステロイド（Betamethasone、Budesonide など）：低カリウム血症のリスクを増加させる
- Bisacodyl：電解質異常のリスク
- Digoxin：低カリウム血症によりジギタリス中毒のリスクが増加する可能性がある
- Lithium：リチウム中毒のリスクが増加する可能性がある
- Metformin：乳酸アシドーシスのリスクが増加する可能性がある
- Carbamazepine、Phenytoin：抗てんかん薬の血中濃度に影響する可能性がある
- Topiramate：代謝性アシドーシスおよび腎結石のリスクを増加させる

### 禁忌
- スルホンアミド系薬剤に対する過敏症
- 重度の肝機能障害
- 低ナトリウム血症または低カリウム血症
- 代謝性アシドーシス
- アジソン病

安全性情報は添付文書をご参照ください。

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
Acetazolamide の急性非代償性心不全における補助的利尿薬としての役割は、質の高い RCT のエビデンス（ADVOR 試験）に支持されており、現在複数の第四相臨床試験が進行中である。心筋症に心不全を合併した患者において、acetazolamide は利尿薬抵抗性を克服する有効な選択肢となり得る。

**推進に必要な事項：**
- 電解質（特にカリウム、ナトリウム、塩化物、重炭酸）を綿密にモニタリングする
- 高用量 aspirin との併用を避ける
- 腎機能および酸塩基平衡をモニタリングする
- スルホンアミド系薬剤に対するアレルギー歴の有無を評価する


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
