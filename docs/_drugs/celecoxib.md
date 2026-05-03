---
layout: default
title: Celecoxib
parent: 僅模型預測 (L5)
nav_order: 32
evidence_level: L5
indication_count: 10
---

# Celecoxib
{: .fs-9 }

證據等級: **L5** | 預測適應症: **10** 個
{: .fs-6 .fw-300 }

---

## 目錄
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist">

## 藥師評估報告

</div>

# Celecoxib：関節リウマチ から 炎症性脊椎症 へ

## 一言要約

Celecoxib（セレコキシブ）は選択的 COX-2 阻害薬として、世界各国で骨関節炎・関節リウマチ・強直性脊椎炎の治療に承認されていますが、日本国内では現時点で承認実績が確認されていません。TxGNN モデルは**炎症性脊椎症 (Inflammatory Spondylopathy)** への有効性を予測しており、現在 **19 件の臨床試験**と **20 編の文献**がこの方向性を強力に支持しています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 骨関節炎・関節リウマチ（グローバル承認、日本未承認） |
| 予測新規適応症 | 炎症性脊椎症 (Inflammatory Spondylopathy) |
| TxGNN 予測スコア | 99.80% |
| エビデンスレベル | L1 |
| 日本市販状況 | ✗ 未上市 |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails |

---

## この予測が妥当である理由

Celecoxib はシクロオキシゲナーゼ-2（COX-2）を選択的に阻害することで、プロスタグランジン E2（PGE2）の産生を抑制し、炎症・疼痛・腫脹を緩和します。COX-1 を温存するため、非選択的 NSAIDs と比較して胃腸毒性リスクが低く、長期投与に適した安全性プロファイルを持ちます。

炎症性脊椎症（強直性脊椎炎を含む脊椎関節炎）の病態は、TNF-α・IL-17 主導の滑膜・付着部炎症と骨形成亢進（アンキローシス）を特徴とします。Celecoxib は COX-2 阻害を通じて PGE2 を減少させ、炎症性腰背部痛と朝のこわばりを改善します。さらに機序研究では、Wnt/Dkk-1 経路を調節することで骨芽細胞活性化と脊椎骨化進行を抑制する可能性が示されており、他の NSAIDs にはない疾患修飾作用として注目されています。

Celecoxib が既に骨関節炎・関節リウマチに使用されることから、同じ滑膜・骨格系炎症を基盤とする炎症性脊椎症への適用は機序的に自然な延長です。実際、複数の Phase 3/4 RCT が強直性脊椎炎における症状改善と構造進行抑制を直接実証しており、エビデンスの質・量ともに最高水準 (L1) に達しています。

---

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT00648141](https://clinicaltrials.gov/study/NCT00648141) | Phase 3 | 完了 | 458 | AS 患者を対象に Celecoxib 200mg QD・200mg BID vs ジクロフェナク 3 回/日の 12 週間症状効果・安全性比較 |
| [NCT00762463](https://clinicaltrials.gov/study/NCT00762463) | Phase 3 | 完了 | 240 | 中国人 AS 患者における Celecoxib vs ジクロフェナク 6 週間二重盲検試験、400mg QD への延長期含む |
| [NCT02528201](https://clinicaltrials.gov/study/NCT02528201) | Phase 4 | 完了 | 330 | Celecoxib 200mg・400mg QD vs ジクロフェナク 3 回/日の AS 12 週間試験（6 週先行試験の確認研究） |
| [NCT02758782](https://clinicaltrials.gov/study/NCT02758782) | Phase 4 | 完了 | 156 | AS 患者における Celecoxib＋ゴリムマブ vs ゴリムマブ単独の 2 年間脊椎構造進行比較（CONSUL 試験） |
| [NCT01934933](https://clinicaltrials.gov/study/NCT01934933) | Phase 4 | 完了 | 150 | 活動性 AS における Celecoxib 単独・エタネルセプト単独・併用療法の有効性・安全性 54 週間無作為比較 |
| [NCT02355236](https://clinicaltrials.gov/study/NCT02355236) | Phase 4 | 不明 | 106 | 骨関節炎（AS 含む）患者における Naxozol vs Celecoxib の胃腸保護効果・疼痛緩和前向き無作為二重盲検試験 |
| [NCT05164198](https://clinicaltrials.gov/study/NCT05164198) | Phase 4 | 不明 | 448 | 安定期 AS 患者における TNF 阻害薬標準用量維持 vs 減量の再燃率比較（Celecoxib は背景 NSAID） |
| [NCT04115098](https://clinicaltrials.gov/study/NCT04115098) | Phase 2 | 終了 | 42 | 軸性脊椎関節炎患者における選択的 COX-2 阻害薬 vs 非選択的 NSAIDs の個別化 N-of-1 試験（疾患活動性・QOL 比較） |
| [NCT03190603](https://clinicaltrials.gov/study/NCT03190603) | Phase 4 | 完了 | 12 | 軸性脊椎関節炎の MRI 炎症病変に対する NSAID 治療効果の評価（アンキローシス予防への含意） |
| [NCT01572675](https://clinicaltrials.gov/study/NCT01572675) | N/A | 完了 | 547 | フランスにおける Etoricoxib と Celecoxib の実臨床使用状況・安全性薬物疫学調査 |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [36800138](https://pubmed.ncbi.nlm.nih.gov/36800138/) | 2023 | RCT | Clinical Rheumatology | 軸性脊椎関節炎において Celecoxib とイメレコキシブは骨代謝マーカー・血管新生を調節し仙腸関節炎症を有意に改善 |
| [28626213](https://pubmed.ncbi.nlm.nih.gov/28626213/) | 2017 | RCT | Medical Science Monitor | 軸性脊椎関節炎患者（n=51）で Celecoxib 200mg BID の治療効果と血清 DKK-1 低下による骨化抑制機序を確認 |
| [38832489](https://pubmed.ncbi.nlm.nih.gov/38832489/) | 2024 | RCT | Scand J Rheumatology | 活動性軸性脊椎関節炎においてイグラチモドと Celecoxib の併用は有効かつ安全（無作為化二重盲検プラセボ対照試験） |
| [38228361](https://pubmed.ncbi.nlm.nih.gov/38228361/) | 2024 | RCT | Ann Rheum Dis | CONSUL 試験：放射線学的軸性脊椎関節炎で Celecoxib＋TNFi 群は TNFi 単独群と比較し 2 年間の脊椎骨化進行を抑制 |
| [40028763](https://pubmed.ncbi.nlm.nih.gov/40028763/) | 2025 | Cohort | Scand J Rheumatology | AS 患者において Celecoxib と非選択的 NSAIDs の心血管疾患・消化管出血リスクは同等（全国コホート研究） |
| [39315555](https://pubmed.ncbi.nlm.nih.gov/39315555/) | 2024 | Cohort | Reumatismo | AS 患者における長期 NSAID 単独療法での肝（AST・ALT）および腎（クレアチニン）機能への影響を評価 |
| [40911151](https://pubmed.ncbi.nlm.nih.gov/40911151/) | 2025 | Umbrella Review | Drugs | 慢性筋骨格疾患における Celecoxib 安全性を体系的に合成したアンブレラレビュー（複数メタ解析を統合） |
| [39757202](https://pubmed.ncbi.nlm.nih.gov/39757202/) | 2025 | Review | BMB Reports | Celecoxib は脊椎関節炎の骨化進行を抑制する唯一の NSAID であり、COX-2 非依存的な骨形成抑制機序が示唆される |
| [22141388](https://pubmed.ncbi.nlm.nih.gov/22141388/) | 2011 | Review | Drugs | Celecoxib の骨関節炎・RA・AS における有効性・安全性の包括的レビュー（EU 承認適応症の全エビデンス整理） |
| [27603385](https://pubmed.ncbi.nlm.nih.gov/27603385/) | 2016 | — | Medicine | 台湾 NHI コホート（AS 患者 4,829 名）：Celecoxib とサラゾスルファピリジンは冠動脈疾患リスクと負の関連 |

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
炎症性脊椎症（強直性脊椎炎含む）に対する Celecoxib の有効性は複数の Phase 3/4 完了 RCT によってエビデンスレベル L1 が確立されており、Wnt/Dkk-1 経路を介した骨化抑制という疾患修飾効果も機序研究で裏付けられています。日本では未承認であるものの、グローバルな科学的根拠は申請検討を支持する水準に達しています。

**進める場合に必要なもの：**
- PMDA への承認申請に向けた日本人患者を対象とする試験データの収集・評価
- TFDA/PMDA 添付文書の安全性情報（警告・禁忌・重大副作用）の取得と日本語化
- 長期 COX-2 阻害に伴う心血管・腎機能リスクの継続モニタリング計画策定
- 高齢者・腎機能低下患者・心血管リスク保有者への用量調整基準の明文化
- 詳細な作用機序データ（MOA）の文書化（DrugBank API 照会）
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

