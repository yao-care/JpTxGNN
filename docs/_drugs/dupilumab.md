---
layout: default
title: Dupilumab
parent: 中エビデンス (L3-L4)
nav_order: 63
evidence_level: L3
indication_count: 1
last_modified_at: 2026-09-17
description: "Dupilumab：予測新適応症は気管支炎 (bronchitis)（エビデンスレベル L3）。既存適応症：日本の承認適応症は本サイトのデータに未収載"
---

# Dupilumab
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

## Dupilumab：アトピー性皮膚炎から気管支炎へ
{: .text-alpha }

## 一言まとめ

Dupilumab（デュピルマブ） は本来、中等症から重症のアトピー性皮膚炎、喘息、および鼻茸を伴う慢性副鼻腔炎の治療に用いられます。
TxGNN モデルは、本剤が**気管支炎 (bronchitis)** に有効である可能性を予測しており、
現時点で **1 件の臨床試験**と **複数の文献**がこの方向性を支持しています。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：atopic eczema、dermatitis, atopic） |
| 予測新適応症 | 気管支炎 (bronchitis) |
| TxGNN 予測スコア | 99.92% |
| エビデンスレベル | L3 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Dupilumab はヒト化モノクローナル抗体で、IL-4 および IL-13 のシグナル伝達を阻害します。
この二つのサイトカインは、2 型炎症反応の重要な mediator です。気管支炎、特に好酸球性気管支炎には、
類似した炎症機序が関与しています。Dupilumab は好酸球性フェノタイプの喘息に対して承認されており、
その下気道の炎症抑制作用は、気管支炎の治療にも及ぶ可能性があります。

## 臨床試験エビデンス

| 試験番号 | 相 | 状態 | 人数 | 主な所見 |
|---------|------|------|------|---------|
| [NCT04362501](https://clinicaltrials.gov/study/NCT04362501) | Phase 2 | COMPLETED | 33 | 鼻茸を伴わない慢性副鼻腔炎患者における dupilumab の有効性を評価 |
| [NCT03346434](https://clinicaltrials.gov/study/NCT03346434) | Phase 2/3 | COMPLETED | 202 | 6 か月から 6 歳未満のアトピー性皮膚炎の小児における dupilumab の薬物動態と有効性を評価 |
| [NCT01949311](https://clinicaltrials.gov/study/NCT01949311) | Phase 3 | COMPLETED | 2733 | アトピー性皮膚炎の成人患者における dupilumab の長期安全性試験 |
| [NCT04287621](https://clinicaltrials.gov/study/NCT04287621) | N/A | ACTIVE_NOT_RECRUITING | 718 | RAPID 登録研究：喘息患者における dupilumab 使用の実臨床データ |
| [NCT02277769](https://clinicaltrials.gov/study/NCT02277769) | Phase 3 | COMPLETED | 708 | 中等症から重症のアトピー性皮膚炎に対する dupilumab 単剤療法の有効性を確認 |

## 文献エビデンス

| PMID | 年 | 種別 | 雑誌 | 主な所見 |
|------|-----|------|------|---------|
| [34597534](https://pubmed.ncbi.nlm.nih.gov/34597534/) | 2022 | RCT extension | Lancet Respir Med | TRAVERSE 試験：中等症から重症の喘息における dupilumab の長期安全性と有効性 |
| [30273510](https://pubmed.ncbi.nlm.nih.gov/30273510/) | 2019 | Meta-analysis | J Asthma | コントロール不良の喘息における dupilumab の有効性と安全性に関するシステマティックレビュー |
| [38488768](https://pubmed.ncbi.nlm.nih.gov/38488768/) | 2024 | Case report | Pediatr Pulmonol | 小児の好酸球性プラスチック気管支炎に対する dupilumab の新たな治療法 |
| [30196731](https://pubmed.ncbi.nlm.nih.gov/30196731/) | 2018 | Review | Expert Opin Pharmacother | 喫煙関連気道疾患を合併した喘息の治療上の課題 |
| [32428511](https://pubmed.ncbi.nlm.nih.gov/32428511/) | 2020 | Clinical study | Chest | 抗 T2 生物学的製剤治療がステロイド依存性喘息の肺換気に及ぼす影響 |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **よくみられる副作用**：注射部位反応、結膜炎、口唇ヘルペス
- **重要な注意事項**：治療開始前に寄生虫感染の評価を行うこと。生ウイルスワクチンとの併用は推奨されません
- **特殊な集団**：小児では体重に応じた用量調整が必要

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
Dupilumab の IL-4/IL-13 抑制機序は、好酸球性炎症に関連する気管支炎に適しており、
好酸球性プラスチック気管支炎に対する有効性を支持する症例報告があります。気管支炎のサブタイプを区別する必要があります。

**推進に必要な事項：**
- 好酸球性と非好酸球性の気管支炎を区別するバイオマーカー
- 慢性気管支炎患者を対象とした前向き臨床試験
- 好酸球増多を伴う COPD 患者における治療効果の評価


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
