---
layout: default
title: Acitretin（アシトレチン）
parent: 中エビデンス (L3-L4)
nav_order: 12
evidence_level: L3
indication_count: 1
last_modified_at: 2026-09-17
description: "Acitretin：予測新適応症は尋常性ざ瘡 (acne)（エビデンスレベル L3）。既存適応症：日本の承認適応症は本サイトのデータに未収載"
---

# Acitretin:乾癬からざ瘡への新規適応症探索

## 一言まとめ

Acitretin は本来、重症の乾癬および皮膚角化症に用いられます。
TxGNN モデルは、**ざ瘡 (acne)** にも有効な可能性があると予測しており、
現在この方向を支持する **臨床試験1件**と**文献18件**があります。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載 |
| 予測新適応症 | 尋常性ざ瘡 (acne) |
| TxGNN 予測スコア | 99.94% |
| エビデンスレベル | L3 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Acitretin は第二世代の芳香族レチノイド（retinoid）に属し、主な作用機序は次のとおりです。
1. 角化細胞の分化と増殖の調節
2. 皮脂腺活性の抑制
3. 抗炎症作用
4. 免疫調節機能

ざ瘡の病態には、皮脂腺からの過剰分泌、毛包の角化異常、アクネ菌の増殖、炎症反応が関与します。Retinoids 系薬剤（isotretinoin など）は、すでに重症ざ瘡の標準治療となっています。

Acitretin は isotretinoin と同じく retinoids に属しますが、皮脂腺の抑制効果が isotretinoin より弱いため、従来ざ瘡にはあまり用いられてきませんでした。しかし文献では、acitretin が次のような場面で代替の選択肢となり得ることが示されています。
- Isotretinoin 治療が奏効しなかった後の維持療法
- 結節嚢腫性ざ瘡を合併した化膿性汗腺炎（hidradenitis suppurativa / acne inversa）

2002 年の症例報告 (PMID: 12080949) では、isotretinoin 治療が無効であった結節嚢腫性ざ瘡の患者が、acitretin の使用により著明に改善したことが示されています。

## 臨床試験エビデンス

| 試験番号 | 相 | 状態 | 症例数 | 主な知見 |
|---------|------|------|------|---------|
| [NCT04663906](https://clinicaltrials.gov/study/NCT04663906) | N/A | UNKNOWN | 300 | 経口 isotretinoin（同じ retinoid）が COVID-19 感染リスクに及ぼす影響を検討 |

*注:acitretin のざ瘡治療を専門に対象とした登録済み臨床試験は、現時点ではありません*

## 文献エビデンス

| PMID | 発行年 | 種類 | 雑誌 | 主な知見 |
|------|-----|------|------|---------|
| [12080949](https://pubmed.ncbi.nlm.nih.gov/12080949/) | 2002 | Case Report | Cutis | Isotretinoin が無効であった結節嚢腫性ざ瘡合併の化膿性汗腺炎で、acitretin による維持療法が成功 |
| [25640693](https://pubmed.ncbi.nlm.nih.gov/25640693/) | 2015 | Guideline | JEADV | 欧州の化膿性汗腺炎治療ガイドライン。acitretin を治療選択肢として言及 |
| [29234829](https://pubmed.ncbi.nlm.nih.gov/29234829/) | 2018 | Review | Der Hautarzt | 化膿性汗腺炎の薬物治療:isotretinoin の効果は限定的で、acitretin の方が良好な効果 |
| [20874789](https://pubmed.ncbi.nlm.nih.gov/20874789/) | 2011 | Journal Article | Br J Dermatol | 25 年間にわたる acitretin による化膿性汗腺炎治療の長期追跡で、良好な効果 |
| [8573927](https://pubmed.ncbi.nlm.nih.gov/8573927/) | 1995 | Review | Dermatology | Retinoids と皮脂腺活性:各 retinoids の抗ざ瘡効果を比較 |
| [9074840](https://pubmed.ncbi.nlm.nih.gov/9074840/) | 1997 | Review | Drugs | 皮膚科における retinoids の現状と将来:ざ瘡関連の応用を含む |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

### 重要な薬物相互作用

**Major 相互作用:**
- Tetracyclines（Doxycycline、Minocycline、Tetracycline）:偽脳腫瘍のリスクを増加
- Vitamin A:ビタミンA過剰症のリスクを増加
- Ethanol（アルコール）:acitretin が etretinate に変換される可能性があり、半減期が数か月まで延長
- Isotretinoin:併用禁忌。ビタミンA毒性が増加
- Methotrexate:肝毒性のリスクを増加
- 経口避妊薬（Levonorgestrel、Norethisterone など）:避妊効果が低下する可能性

**Moderate 相互作用:**
- スルホニル尿素系血糖降下薬（Glimepiride、Glipizide など）:血糖コントロールに影響する可能性
- 光感受性薬剤（Aminolevulinic acid、Methoxsalen など）:光感受性反応が増加

### 重要な警告
- **妊娠は絶対禁忌**:acitretin は強い催奇形性を有するため、妊娠可能な女性は治療前・治療中・治療後に有効な避妊措置を講じる必要があります
- etretinate に変換される可能性があるため、**投与中止後も少なくとも 3 年間は避妊が必要**
- **飲酒禁止**:アルコールは acitretin の長時間作用型 etretinate への変換を促進します
- 肝機能と血中脂質を定期的にモニタリング

安全性情報は添付文書をご参照ください。

## 結論と次のステップ

**判断:Proceed with Guardrails**

**理由:**
Acitretin は isotretinoin と同じく retinoids に属し、類似した抗角化作用および抗炎症作用の機序を有します。文献では、isotretinoin による治療が奏効しなかった、または長期の維持療法が必要なざ瘡患者において、応用価値があることが示されています。特に化膿性汗腺炎にざ瘡を合併する場合には、acitretin が isotretinoin より有効である可能性があります。

**推進に必要な事項:**
- 妊娠の可能性を除外し、妊娠可能な女性は二種類の有効な避妊方法を用いること
- 飲酒を完全に禁止すること
- 肝機能（ALT、AST）および血中脂質（TG、Cholesterol）を定期的にモニタリングすること
- ビタミンA補充剤との併用を避けること
- テトラサイクリン系抗菌薬との併用を避けること
- 各タイプのざ瘡における acitretin と isotretinoin の効果を比較する RCT を設計すること


---




# Acitretin
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

<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
