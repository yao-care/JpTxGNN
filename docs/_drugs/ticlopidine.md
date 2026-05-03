---
layout: default
title: Ticlopidine
parent: 僅模型預測 (L5)
nav_order: 140
evidence_level: L5
indication_count: 10
---

# Ticlopidine
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

# チクロピジン：抗血小板療法（脳梗塞予防）から 関節リウマチへ

## 一言要約

チクロピジン（Ticlopidine）は P2Y12 受容体を不可逆的に阻害する thienopyridine 系抗血小板薬で、脳梗塞・血栓症の予防に広く使用されてきました。TxGNN モデルは**関節リウマチ（Rheumatoid Arthritis）**への有効性を予測スコア 98.91% で提示しており、現在 **0 件の登録臨床試験**と **9 編の文献**（1980〜90 年代の二重盲検試験・コホート研究を含む）がこの方向性を支持しています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 抗血小板薬（脳梗塞・脳血栓症予防） |
| 予測新規適応症 | 関節リウマチ (Rheumatoid Arthritis) |
| TxGNN 予測スコア | 98.91% |
| エビデンスレベル | L3 |
| 日本市販状況 | 未上市 |
| 承認番号数 | 0 件 |
| 推奨決定 | Hold |

---

## この予測が妥当である理由

現在の Evidence Pack には詳細な作用機序（MOA）データが含まれていません。既知の薬理情報によると、チクロピジンは thienopyridine 系薬物として血小板上の P2Y12 受容体を不可逆的に阻害し、ADP 誘導性の血小板凝集を遮断します。この作用は単なる抗凝集にとどまらず、血小板が担う炎症増幅シグナルの抑制にも及ぶと考えられています。

関節リウマチ（RA）の病態において、活性化血小板は滑膜組織における炎症性サイトカイン（IL-1β、TGF-β など）の放出、および P-selectin 介在性の白血球浸潤を促進することが知られています。チクロピジンによる P2Y12 阻害は、この血小板依存性の炎症カスケードを遮断し、滑膜炎および微小血管障害を緩和する機序的根拠があります。

さらに、1985 年の臨床コホート研究（PMID 3000794）では、RA 患者 22 名に低用量チクロピジンを 18 ヶ月投与した結果、関節侵襲数の有意な減少とともに血清 sulphydryl（SH）値の有意な上昇が観察されており、抗酸化・免疫調節機転の存在が示唆されています。1989 年の二重盲検試験（PMID 2790405）では ESR が −28% 改善し、全血流動性の改善も確認されており、RA に対するチクロピジンの疾患修飾活性の可能性を示す直接的なヒト臨床データが存在します。

---

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [2790405](https://pubmed.ncbi.nlm.nih.gov/2790405/) | 1989 | Cohort（二重盲検） | British Journal of Rheumatology | RA 患者 40 名のプラセボ対照二重盲検試験。チクロピジン群で ESR が −28%（p<0.01）改善、全血流動性も有意に改善 |
| [3000794](https://pubmed.ncbi.nlm.nih.gov/3000794/) | 1985 | Cohort | European Journal of Clinical Pharmacology | RA 患者 22 名に 250 mg/日 × 18 ヶ月投与で関節数有意減少、テクネシウム指数・ESR 改善、血清 SH 値上昇（抗酸化活性を示唆） |
| [16729012](https://pubmed.ncbi.nlm.nih.gov/16729012/) | 2006 | Case series | Nature Clin Pract Cardiovasc Med | RA に合併したループス抗凝固因子・虚血性心筋微小血管障害の症例。RA における血小板関連血管病態の関与を示唆 |
| [27188755](https://pubmed.ncbi.nlm.nih.gov/27188755/) | 2016 | Cohort | BMC Musculoskeletal Disorders | 全身性硬化症 vs RA 対照群における血小板 ADP 依存性活性化の比較研究。thienopyridine 系（clopidogrel）の繊維化抑制効果を評価 |
| [25446727](https://pubmed.ncbi.nlm.nih.gov/25446727/) | 2015 | Review | Nature Rev Gastroenterol Hepatol | IBD 患者の心血管リスクが RA と同水準であることを示すレビュー。慢性炎症性疾患に対する抗血小板療法の意義を考察 |
| [19765672](https://pubmed.ncbi.nlm.nih.gov/19765672/) | 2010 | Review | Clinical Gastroenterology & Hepatology | 急性大腸虚血のリスク因子調査。RA 関連疾患・薬物との関係性を解析 |
| [26939212](https://pubmed.ncbi.nlm.nih.gov/26939212/) | 2015 | Case series | Romanian J Internal Medicine | RA 合併の不安定動脈硬化性疾患に対する抗血栓療法管理の困難症例。thienopyridine 系の使用実態を記録 |
| [7893538](https://pubmed.ncbi.nlm.nih.gov/7893538/) | 1994 | Case series | 脳と神経 | 30 年来の RA 患者に合併した右片麻痺・腎不全症例。抗血小板療法の役割を検討 |
| [41689871](https://pubmed.ncbi.nlm.nih.gov/41689871/) | 2026 | In vitro | Drug Metabolism and Disposition | CYP2C19 の不可逆的阻害による clopidogrel PK への影響を解析。thienopyridine 系と RA 治療薬の代謝相互作用機序の参考情報 |

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Hold**

**理由：**
1980〜90 年代の小規模コホート研究および二重盲検試験（合計約 42 名）において生物学的に興味深い臨床所見が存在するものの、現代の基準を満たす無作為化比較試験（RCT）・大規模観察研究は皆無であり、日本においても承認実績がありません。また、thienopyridine 系薬物に特有の血栓性血小板減少性紫斑病（TTP）リスクが RA 患者集団における安全性評価を複雑にしています。

**進める場合に必要なもの：**
- 詳細な作用機序（MOA）の文書化（DrugBank API を通じた情報取得）
- 日本国内での安全性情報収集（PMDA 仿単・有害事象データベース照会）
- 現代設計基準に基づく RA を対象とした Phase 2 前向き試験の計画立案
- thienopyridine 系薬物の RA 患者における TTP・好中球減少リスクの系統的評価
- 既存 RA 治療薬（MTX、生物学的製剤）との DDI プロファイルの確認
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

