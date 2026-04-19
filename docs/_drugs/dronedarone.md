---
layout: default
title: Dronedarone
parent: 高エビデンス (L1-L2)
nav_order: 62
evidence_level: L2
indication_count: 1
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

<div id="pharmacist">

## 薬剤師評価レポート

</div>

# Dronedarone：從心房纖維顫動到中風疾病

## 一言まとめ

Dronedarone 原本用於治療陣發性或持續性心房纖維顫動/心房撲動。
TxGNN 模型預測它可能對**中風疾病 (stroke disorder)** 有效，
目前有 **多個臨床試驗**和 **多篇文獻**支持這個方向。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 心房纖維顫動、心房撲動 |
| 予測新適応症 | 中風疾病 (stroke disorder) |
| TxGNN 予測スコア | 99.97% |
| エビデンスレベル | L2 |
| 日本上市 | 已上市 |
| 承認数 | 1 張 |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Dronedarone 是 amiodarone 的衍生物，具有多通道阻斷作用，能維持竇性心律。
心房纖維顫動是中風的主要危險因素，透過維持竇性心律可減少心房血栓形成。
ATHENA 試驗的事後分析顯示 dronedarone 可降低中風和暫時性腦缺血發作風險，
且研究發現其具有獨立於抗心律不整作用之外的抗凝血和抗血小板效應。

## 臨床試験エビデンス

| 試驗編號 | 階段 | 狀態 | 人數 | 主要發現 |
|---------|------|------|------|---------|
| [NCT01151137](https://clinicaltrials.gov/study/NCT01151137) | Phase 3 | TERMINATED | 3236 | PALLAS 試驗評估 dronedarone 在永久性心房纖維顫動預防主要心血管事件 |
| [NCT01288352](https://clinicaltrials.gov/study/NCT01288352) | Phase 4 | COMPLETED | 2789 | EAST 試驗證實早期節律控制可預防心血管死亡和中風 |
| [NCT05130268](https://clinicaltrials.gov/study/NCT05130268) | Phase 4 | COMPLETED | 339 | 評估首發心房纖維顫動患者早期使用 dronedarone 的效果 |
| [NCT05293080](https://clinicaltrials.gov/study/NCT05293080) | Phase 3 | NOT_YET_RECRUITING | 1746 | 急性中風合併心房纖維顫動患者的早期節律控制 |
| [NCT00911508](https://clinicaltrials.gov/study/NCT00911508) | N/A | COMPLETED | 2204 | CABANA 試驗比較導管消融與抗心律不整藥物治療 |

## 文献エビデンス

| PMID | 年份 | 類型 | 期刊 | 主要發現 |
|------|-----|------|------|---------|
| [22166900](https://pubmed.ncbi.nlm.nih.gov/22166900/) | 2012 | Review | Lancet | 心房纖維顫動治療進展，包括 dronedarone 的角色 |
| [28992468](https://pubmed.ncbi.nlm.nih.gov/28992468/) | 2017 | In vitro | Atherosclerosis | Dronedarone 具有獨立於抗心律不整作用的抗凝血和抗血小板效應 |
| [40387892](https://pubmed.ncbi.nlm.nih.gov/40387892/) | 2025 | RCT analysis | Clin Res Cardiol | EAST-AFNET 4 試驗中 amiodarone 和 dronedarone 用於早期節律控制的安全性和療效 |
| [20730068](https://pubmed.ncbi.nlm.nih.gov/20730068/) | 2010 | Review | Vasc Health Risk Manag | Dronedarone 獲批及其在心房纖維顫動治療中的療效 |
| [35293087](https://pubmed.ncbi.nlm.nih.gov/35293087/) | 2022 | Post-hoc analysis | Eur J Heart Fail | ATHENA 試驗事後分析評估 dronedarone 在 HFpEF/HFmrEF 合併心房纖維顫動的效果 |

## 日本上市情報

| 承認番号 | 品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 1 張許可證 | 決奈達隆鹽酸鹽 | 口服劑型 | 陣發性或持續性心房纖維顫動/心房撲動，降低心房顫動住院風險 |

## 安全性に関する考慮事項

- **黑框警告**：永久性心房纖維顫動、嚴重心衰竭患者禁用
- **主要不良反應**：腹瀉、噁心、腹痛、血清肌酐升高
- **肝毒性**：罕見但嚴重，需監測肝功能
- **藥物交互作用**：與 digoxin 併用時會增加 digoxin 血中濃度

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
Dronedarone 透過維持竇性心律和潛在的抗血栓機制，可能對中風預防有效。
ATHENA 試驗已顯示其在中風/TIA 預防方面的益處，但需注意適應症限制。

**推進に必要な事項：**
- 排除永久性心房纖維顫動和嚴重心衰竭患者
- 嚴格的肝功能監測計畫
- 與抗凝血藥物併用策略的優化研究


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
