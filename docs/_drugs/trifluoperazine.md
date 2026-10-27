---
layout: default
title: Trifluoperazine
parent: 中エビデンス (L3-L4)
nav_order: 184
evidence_level: L3
indication_count: 1
last_modified_at: 2026-09-17
description: "Trifluoperazine：予測新適応症は双極性障害の躁病相 (manic bipolar affective disorder)（エビデンスレベル L3）。既存適応症：日本の承認適応症は本サイトのデータに未収載"
---

# Trifluoperazine
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

## Trifluoperazine：精神病状態から双極性障害の躁病相へ
{: .text-alpha }

## 一言まとめ

Trifluoperazine（トリフルオペラジン） は、もともと精神病状態および行動障害の治療に用いられている。
TxGNN モデルは、本剤が**双極性障害の躁病相 (manic bipolar affective disorder)** に有効である可能性を予測しており、
現時点で **20 篇の文献**がこの方向性を支持している。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：schizophrenia、anxiety） |
| 予測新適応症 | 双極性障害の躁病相 (manic bipolar affective disorder) |
| TxGNN 予測スコア | 99.51% |
| エビデンスレベル | L3 (間接的な文献エビデンスあり) |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Trifluoperazine は定型抗精神病薬（フェノチアジン系）であり、その作用機序は躁病相での応用を支持するものである。

1. **ドパミン D2 受容体遮断**：中脳辺縁系のドパミン過剰活性化を抑制する
2. **鎮静作用**：興奮や攻撃的行動を軽減する
3. **抗精神病作用**：妄想・幻覚などの精神病性症状を改善する

躁病相にはしばしば精神病性症状が伴い、定型抗精神病薬は非定型薬が登場するまで、躁病の急性期における標準的な治療選択肢の一つであった。

## 臨床試験エビデンス

双極性障害の躁病相を対象とした専用の臨床試験は現時点でないが、躁病相での使用を支持する文献が複数ある。

## 文献エビデンス

| PMID | 年 | 種類 | 雑誌 | 主な知見 |
|------|-----|------|------|---------|
| [14309092](https://pubmed.ncbi.nlm.nih.gov/14309092/) | 1965 | Clinical Study | Int J Neuropsychiatry | 統合失調症および躁病患者における Haloperidol と Trifluoperazine の効果を比較 |
| [24943390](https://pubmed.ncbi.nlm.nih.gov/24943390/) | 2014 | Survey | J Clin Psychopharmacol | ウガンダの精神科病院における処方パターン：双極性障害に対する Trifluoperazine と Carbamazepine の併用が 45% を占めた |
| [17017818](https://pubmed.ncbi.nlm.nih.gov/17017818/) | 2006 | Review | J Clin Psychiatry | 双極性障害の不安症状に対する定型・非定型抗精神病薬の効果のレビュー |
| [970489](https://pubmed.ncbi.nlm.nih.gov/970489/) | 1976 | Case Study | Am J Psychiatry | 躁病におけるドパミン機構の役割を検討 |
| [3935307](https://pubmed.ncbi.nlm.nih.gov/3935307/) | 1985 | Case Report | Can J Psychiatry | 青年期の双極性障害症例。Trifluoperazine で治療 |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **錐体外路症状 (EPS)**：定型抗精神病薬の主な副作用
- **遅発性ジスキネジア (Tardive dyskinesia)**：長期使用に伴うリスク
- **悪性症候群 (NMS)**：まれだが重篤な有害反応
- **主要な相互作用 (Major)**：
  - Bupropion（けいれん閾値を低下させる）
  - Morphine（中枢抑制を増強する）
  - Metoclopramide（錐体外路症状のリスクを増加させる）
  - Potassium chloride、Potassium citrate（消化管潰瘍のリスクを増加させる）
  - Dolasetron（QT 延長のリスク）
- **中等度の相互作用 (Moderate)**：
  - 糖尿病治療薬（血糖コントロールに影響する可能性）
  - 抗コリン薬（抗コリン作用を増強する）
  - Levofloxacin（QT 延長のリスク）

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
Trifluoperazine は定型抗精神病薬として、躁病相での使用に歴史的な臨床経験の裏付けがある。複数の文献が双極性障害患者での応用を示しており、特に医療資源の限られた地域では今も重要な治療選択肢となっている。

**推進に必要な事項：**
- 非定型抗精神病薬との比較研究
- EPS および代謝系副作用についてのリスク・ベネフィットの評価
- 明確な用量の推奨と monitoring 計画の策定
- 長期維持療法ではなく急性期治療としての位置づけの検討

**臨床上の注意：**
現代の躁病急性期治療では、第一選択は通常、非定型抗精神病薬（Olanzapine、Quetiapine、Risperidone など）であり、Trifluoperazine は代替選択肢となり得るが、EPS のリスクに注意が必要である。


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
