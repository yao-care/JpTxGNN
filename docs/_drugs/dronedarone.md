---
layout: default
title: Dronedarone
parent: 高エビデンス (L1-L2)
nav_order: 62
evidence_level: L2
indication_count: 1
last_modified_at: 2026-09-17
description: "Dronedarone：予測新適応症は脳卒中 (stroke disorder)（エビデンスレベル L2）。既存適応症：日本の承認適応症は本サイトのデータに未収載）"
---

# Dronedarone
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

# Dronedarone：心房細動から脳卒中へ

## 一言まとめ

Dronedarone（ドロネダロン） は本来、発作性または持続性の心房細動／心房粗動の治療に用いられます。
TxGNN モデルは、**脳卒中 (stroke disorder)** に有効な可能性があると予測しており、
現在 **複数の臨床試験**と **複数の文献**がこの方向性を支持しています。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：atrial fibrillation (disease)） |
| 予測新適応症 | 脳卒中 (stroke disorder) |
| TxGNN 予測スコア | 99.97% |
| エビデンスレベル | L2 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Dronedarone は amiodarone の誘導体で、多チャネル遮断作用を持ち、洞調律を維持することができます。
心房細動は脳卒中の主要な危険因子であり、洞調律を維持することで心房内血栓の形成を減らせる可能性があります。
ATHENA 試験の事後解析では、dronedarone が脳卒中および一過性脳虚血発作のリスクを低下させることが示されており、
さらに、抗不整脈作用とは独立した抗凝固・抗血小板作用を有することが報告されています。

## 臨床試験エビデンス

| 試験番号 | 相 | 状態 | 症例数 | 主な所見 |
|---------|------|------|------|---------|
| [NCT01151137](https://clinicaltrials.gov/study/NCT01151137) | Phase 3 | TERMINATED | 3236 | PALLAS 試験。永続性心房細動における主要心血管イベントの予防について dronedarone を評価 |
| [NCT01288352](https://clinicaltrials.gov/study/NCT01288352) | Phase 4 | COMPLETED | 2789 | EAST 試験。早期のリズムコントロールが心血管死亡と脳卒中を予防することを実証 |
| [NCT05130268](https://clinicaltrials.gov/study/NCT05130268) | Phase 4 | COMPLETED | 339 | 初発の心房細動患者における dronedarone 早期使用の効果を評価 |
| [NCT05293080](https://clinicaltrials.gov/study/NCT05293080) | Phase 3 | NOT_YET_RECRUITING | 1746 | 心房細動を合併する急性期脳卒中患者における早期リズムコントロール |
| [NCT00911508](https://clinicaltrials.gov/study/NCT00911508) | N/A | COMPLETED | 2204 | CABANA 試験。カテーテルアブレーションと抗不整脈薬治療を比較 |

## 文献エビデンス

| PMID | 発表年 | 種類 | 雑誌 | 主な所見 |
|------|-----|------|------|---------|
| [22166900](https://pubmed.ncbi.nlm.nih.gov/22166900/) | 2012 | Review | Lancet | 心房細動治療の進歩（dronedarone の役割を含む） |
| [28992468](https://pubmed.ncbi.nlm.nih.gov/28992468/) | 2017 | In vitro | Atherosclerosis | Dronedarone は抗不整脈作用とは独立した抗凝固・抗血小板作用を有する |
| [40387892](https://pubmed.ncbi.nlm.nih.gov/40387892/) | 2025 | RCT analysis | Clin Res Cardiol | EAST-AFNET 4 試験における、早期リズムコントロールでの amiodarone と dronedarone の安全性と有効性 |
| [20730068](https://pubmed.ncbi.nlm.nih.gov/20730068/) | 2010 | Review | Vasc Health Risk Manag | Dronedarone の承認と、心房細動治療における有効性 |
| [35293087](https://pubmed.ncbi.nlm.nih.gov/35293087/) | 2022 | Post-hoc analysis | Eur J Heart Fail | ATHENA 試験の事後解析。HFpEF/HFmrEF に心房細動を合併する患者での dronedarone の効果を評価 |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **黒枠警告**：永続性心房細動および重度心不全の患者には禁忌
- **主な副作用**：下痢、悪心、腹痛、血清クレアチニン上昇
- **肝毒性**：まれだが重篤であり、肝機能のモニタリングが必要
- **薬物相互作用**：digoxin との併用で digoxin の血中濃度が上昇する

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
Dronedarone は、洞調律の維持と潜在的な抗血栓作用により、脳卒中予防に有効な可能性があります。
ATHENA 試験では脳卒中／TIA の予防における有益性がすでに示されていますが、適応症の制限に注意が必要です。

**推進に必要な事項：**
- 永続性心房細動および重度心不全の患者を除外すること
- 厳格な肝機能モニタリング計画
- 抗凝固薬との併用戦略を最適化するための研究


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
