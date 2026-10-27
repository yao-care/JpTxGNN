---
layout: default
title: Human Immunoglobulin G
parent: 中エビデンス (L3-L4)
nav_order: 79
evidence_level: L3
indication_count: 1
last_modified_at: 2026-04-19
description: "Human Immunoglobulin G：予測新適応症は糖尿病網膜症 (diabetic retinopathy)（エビデンスレベル L3）。既存適応症：日本の承認適応症は本サイトのデータに未収載"
---

# Human Immunoglobulin G
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

## Human Immunoglobulin G：免疫調節から糖尿病網膜症へ
{: .text-alpha }

## 一言まとめ

Human immunoglobulin G（ヒト免疫グロブリンG）（IVIG）は、もともと免疫不全症、ITP、川崎病などの免疫調節治療に用いられています。
TxGNN モデルは、本剤が**糖尿病網膜症 (diabetic retinopathy)** に有効である可能性を予測しており、
現在、関連する研究として **3 件の臨床試験**と **20 件の文献**があります。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載 |
| 予測新適応症 | 糖尿病網膜症 (diabetic retinopathy) |
| TxGNN 予測スコア | 99.63% |
| エビデンスレベル | L3 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Explore |

## この予測が妥当な理由

Human immunoglobulin G は免疫調節作用を有する生物学的製剤であり、
自己抗体の中和、補体系の調節、Fc 受容体機能への影響など、複数の機序で作用します。

**予測の妥当性の分析：**
- 糖尿病網膜症には、慢性炎症と免疫調節の破綻が関与する
- 研究により、DR 患者の血清中で IgG の糖鎖修飾パターンに異常があることが示されており、疾患における IgG の役割が示唆される
- 自己抗体が網膜周皮細胞（pericyte）の損傷機序に関与している可能性がある
- 補体活性化産物（C3a、C5a）が DR 患者で上昇している

**機序との関連：**
- IgG の糖鎖修飾の変化は DR の重症度と関連する（PMID: 33491329, 40204274）
- 網膜周皮細胞反応性の自己抗体が、補体を介して損傷を引き起こす（PMID: 26839120）
- 増殖性 DR では、硝子体液中の IgG 濃度が上昇する（PMID: 32714992）

## 臨床試験エビデンス

| 試験番号 | 相 | 状態 | 人数 | 主な所見 |
|---------|------|------|------|---------|
| [NCT01148225](https://clinicaltrials.gov/study/NCT01148225) | Phase 3 | COMPLETED | 424 | Adalimumab の非感染性ぶどう膜炎（DR 関連合併症を含む）への使用 |
| [NCT02924987](https://clinicaltrials.gov/study/NCT02924987) | Phase 4 | UNKNOWN | 40 | 糖尿病黄斑浮腫に対する抗 VEGF 治療 |
| [NCT02443155](https://clinicaltrials.gov/study/NCT02443155) | Phase 2 | COMPLETED | 308 | beta 細胞機能を保護する免疫調節治療の研究 |

*注：上記の試験は IVIG の DR への使用を直接検証したものではなく、免疫グロブリン関連薬または糖尿病の合併症に関するものです*

## 文献エビデンス

| PMID | 年 | 種類 | 雑誌 | 主な所見 |
|------|-----|------|------|---------|
| [40204274](https://pubmed.ncbi.nlm.nih.gov/40204274/) | 2025 | 研究 | Mol Cell Proteomics | 血清 IgG Fc の糖鎖修飾は DR の診断バイオマーカーとなり得る |
| [33491329](https://pubmed.ncbi.nlm.nih.gov/33491329/) | 2021 | 研究 | J Diabetes | IgG の N-糖鎖修飾パターンが DR と関連する |
| [26839120](https://pubmed.ncbi.nlm.nih.gov/26839120/) | 2016 | 研究 | Sci Rep | DR 患者に網膜周皮細胞反応性の自己抗体が存在する |
| [32714992](https://pubmed.ncbi.nlm.nih.gov/32714992/) | 2020 | 研究 | J Diabetes Res | 2型糖尿病患者の硝子体液中の B 細胞抗体の解析 |
| [33625683](https://pubmed.ncbi.nlm.nih.gov/33625683/) | 2021 | 研究 | Immunol Res | PDR 患者で濾胞性ヘルパー T 細胞の調節異常がみられ、IgG 濃度が上昇している |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **薬物相互作用**：DDI データベースに重大な相互作用は見つかっていない
- **注意事項**：
  - 輸注反応（発熱、悪寒、頭痛）を起こす可能性がある
  - 高用量の IVIG では血栓塞栓症のリスクがある
  - 腎機能障害のある患者には慎重に使用する必要がある
- **特殊集団**：糖尿病患者は腎症を合併していることが多く、使用時には腎機能のモニタリングが必要

安全性情報は添付文書をご参照ください。

## 結論と次のステップ

**判断：Explore**

**理由：**
- 多数の文献が、糖尿病網膜症の病態機序における IgG の役割を支持している
- 免疫調節は、DR 治療においてまだ十分に検討されていない方向性である
- ただし、IVIG の DR に対する有効性を評価した直接的な臨床試験は現時点でない
- IVIG は高額であり、費用対効果の評価が必要

**推進に必要な事項：**
- IVIG の網膜周皮細胞保護作用の機序を確認する基礎研究
- IVIG の DR 患者における安全性と初期有効性を評価する小規模臨床試験
- 既存の抗 VEGF 治療との比較または併用療法の研究
- 費用対効果分析


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
