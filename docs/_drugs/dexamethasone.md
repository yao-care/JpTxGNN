---
layout: default
title: Dexamethasone
parent: 僅模型預測 (L5)
nav_order: 42
evidence_level: L5
indication_count: 10
---

# Dexamethasone
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

# デキサメタゾン：抗炎症・免疫抑制から円形脱毛症へ

## 一言要約

デキサメタゾンは強力な合成糖皮質激素であり、炎症・自己免疫疾患・アレルギーなど広範な疾患の治療に用いられています。TxGNN モデルは**円形脱毛症 (Alopecia Areata)** への有効性を予測しており、現在 **13 件の臨床試験**と **20 編の文献**がこの方向性に関連する証拠を提供しています。なかでも RCT・メタ解析・複数のコホート研究が口服 mini-pulse 療法の有効性を直接支持しており、エビデンスは L1 と判定されています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | データなし（PMDA 未収載） |
| 予測新規適応症 | 円形脱毛症 (Alopecia Areata) |
| TxGNN 予測スコア | 99.99% |
| エビデンスレベル | L1 |
| 日本市販状況 | ✗ 未上市（PMDA 照会結果 0 件） |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails |

---

## この予測が妥当である理由

現在、本 Evidence Pack には詳細な作用機序データが収録されていません。ただし、デキサメタゾンは糖皮質激素受容体（GR）を介した転写調節作用により、炎症性サイトカイン（IL-2、IFN-γ、TNF-α など）の産生を抑制し、広範な免疫抑制・抗炎症効果を発揮することが知られています。

円形脱毛症は、CD8⁺ T 細胞が毛包周囲に浸潤し、正常な「免疫特権（immune privilege）」状態を破壊することで生じる自己免疫性脱毛症です。デキサメタゾンは T 細胞の活性化・増殖を抑制することで、この自己免疫攻撃を鎮静させ、毛包の免疫特権を回復させる可能性があります。この機序は本 Evidence Pack 内の `repurposing_rationale` にも明記されています。

臨床的に確立されているのが「口服 mini-pulse 療法」です。毎週連続 2 日間に 5mg を間歇投与することで、連続投与時の副作用（HPA 軸抑制・骨粗鬆症など）を最小化しながら免疫抑制効果を維持します。RCT（PMID 36086930）、ネットワークメタ解析（PMID 39042154）、複数の多施設コホート研究がこの療法の中等症〜重症円形脱毛症に対する有効性を直接実証しており、JAK 阻害剤が入手困難・禁忌の場合の代替療法として欧州・アジア皮膚科領域で広く評価されています。

---

## 臨床試験エビデンス

> ⚠️ **注記**：ClinicalTrials.gov で取得された 13 件はすべてデキサメタゾンを癌治療の支持療法（制吐・脳浮腫管理・免疫調節）として使用した試験であり、円形脱毛症を主要対象とするものではありません（関連性グレード C）。円形脱毛症に対する直接的な臨床的エビデンスは下記「文献エビデンス」セクションを参照してください。

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見（間接参考） |
|---------|--------|------|----------|---------|
| [NCT04343560](https://clinicaltrials.gov/study/NCT04343560) | N/A | 完了 | 380 | 異常ステロイドメタボロームが骨強度・骨密度・体組成に及ぼす影響を探索（全身性糖皮質激素効果の背景情報） |
| [NCT02685826](https://clinicaltrials.gov/study/NCT02685826) | Phase 1/2 | 完了 | 56 | 新規診断多発性骨髄腫における Durvalumab + Lenalidomide ± Dexamethasone（免疫調節役割の確認） |
| [NCT02004275](https://clinicaltrials.gov/study/NCT02004275) | Phase 1/2 | 不明 | 118 | 多発性骨髄瘤の Pomalidomide + Dexamethasone ± Ixazomib 比較試験（デキサメタゾン免疫調節の核心的役割） |
| [NCT01055496](https://clinicaltrials.gov/study/NCT01055496) | Phase 1 | 完了 | 103 | CD22 陽性非ホジキンリンパ腫における R-CVP または R-GDP + Inotuzumab Ozogamicin（R-GDP アームにデキサメタゾン含む） |
| [NCT01866449](https://clinicaltrials.gov/study/NCT01866449) | Phase 2 | 完了 | 24 | テモゾロミド抵抗性膠芽腫における Cabazitaxel 試験（脳浮腫管理用途） |
| [NCT01126736](https://clinicaltrials.gov/study/NCT01126736) | Phase 1/2 | 完了 | 98 | 非扁平上皮 NSCLC における Eribulin + Pemetrexed（予防的支持療法として使用） |
| [NCT02288078](https://clinicaltrials.gov/study/NCT02288078) | Phase 2 | 不明 | 74 | Regorafenib 治療による疲労・倦怠感に対するデキサメタゾン予防投与のランダム化二重盲検試験 |
| [NCT01215916](https://clinicaltrials.gov/study/NCT01215916) | Phase 1 | 完了 | 39 | 固形腫瘍に対する LY573636-sodium + Pemetrexed 組み合わせ療法（支持療法として使用） |
| [NCT00402766](https://clinicaltrials.gov/study/NCT00402766) | Phase 1 | 完了 | 19 | 悪性中皮腫における Cisplatin + Pemetrexed + Imatinib（制吐支持療法として使用） |
| [NCT00282087](https://clinicaltrials.gov/study/NCT00282087) | Phase 2 | 完了 | 47 | 子宮平滑筋肉腫術後補助化学療法（Gemcitabine/Docetaxel → Doxorubicin）の前投薬として使用 |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [39042154](https://pubmed.ncbi.nlm.nih.gov/39042154/) | 2024 | Meta-analysis | Archives of Dermatological Research | 重症円形脱毛症に対するシステミックステロイド・経口 JAK 阻害剤・接触免疫療法の有効性・安全性をネットワークメタ解析で比較。ステロイドの優位性・限界を定量評価 |
| [36086930](https://pubmed.ncbi.nlm.nih.gov/36086930/) | 2022 | RCT | Dermatologic Therapy | 重症小児円形脱毛症（N=30）においてデキサメタゾン oral mini-pulse と DPCP 接触感作を直接比較したランダム化非盲検試験 |
| [35330017](https://pubmed.ncbi.nlm.nih.gov/35330017/) | 2022 | Cohort | Journal of Clinical Medicine | 円形脱毛症に対するデキサメタゾン mini-pulse 療法の実臨床エビデンス。治療反応の成功に関連する因子を探索した前向きコホート研究 |
| [36070222](https://pubmed.ncbi.nlm.nih.gov/36070222/) | 2022 | Cohort | Dermatologic Therapy | 中等症〜重症円形脱毛症に対する口服デキサメタゾン mini-pulse 療法の多施設研究。欧州での JAK 阻害剤代替療法としての位置づけを評価 |
| [31579982](https://pubmed.ncbi.nlm.nih.gov/31579982/) | 2019 | Cohort | Dermatologic Therapy | 重症小児円形脱毛症（N=73）における静脈内デキサメタゾンパルス 1 日法 vs 3 日法の比較。6〜12 ヶ月月次投与での毛髪再生率を評価 |
| [26179196](https://pubmed.ncbi.nlm.nih.gov/26179196/) | 2015 | Cohort | Dermatologic Therapy | 重症小児円形脱毛症（N=65）に対する口服パルス + 外用コルチコステロイド併用療法の長期追跡（中央値 96 ヶ月） |
| [41243342](https://pubmed.ncbi.nlm.nih.gov/41243342/) | 2025 | Case series | Journal of Dermatological Treatment | JAK 阻害剤が使用不可の患者におけるデキサメタゾン oral mini-pulse による重症円形脱毛症の持続的寛解と関連文献レビュー |
| [10535249](https://pubmed.ncbi.nlm.nih.gov/10535249/) | 1999 | Cohort | Journal of Dermatology | 広汎性円形脱毛症（N=30）に対するデキサメタゾン 5mg 週 2 日間口服パルス投与。最短 12 週間評価での毛髪再生効果 |
| [16707886](https://pubmed.ncbi.nlm.nih.gov/16707886/) | 2006 | Cohort | Dermatology | 広汎性円形脱毛症に対するシステミックコルチコステロイド 3 種類の有効性・再発率・副作用を直接比較 |
| [36461625](https://pubmed.ncbi.nlm.nih.gov/36461625/) | 2023 | Review | Pediatric Dermatology | 小児円形脱毛症に対するパルス用量コルチコステロイド療法の用量・投与レジメン・副作用に関する文献レビュー |

---

## 日本市販情報

PMDA データベースへの照会（2026-03-10）の結果、デキサメタゾン（DB01234）の承認記録は 0 件でした。デキサメタゾンは国際的に広く承認されている薬剤であるため、データ収集方法の再確認が推奨されます。正確な承認情報は [PMDA 医薬品情報検索](https://www.pmda.go.jp/PmdaSearch/iyakuSearch/) でご確認ください。

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
円形脱毛症に対するデキサメタゾン口服 mini-pulse 療法は、RCT・ネットワークメタ解析・複数の多施設コホート研究（L1 エビデンス）により有効性が直接支持されています。機序的な合理性も明確であり、JAK 阻害剤が使用できない患者への現実的な代替療法として一定の臨床的地位を確立しています。ただし、日本での承認情報が未収載（PMDA 照会結果 0 件）であり、本 Evidence Pack の安全性データが欠落しているため、実際の適用には以下の補完的評価が必要です。

**進める場合に必要なもの：**
- PMDA 承認情報の再確認（薬剤名・一般名・塩形を変えた再照会）
- PMDA 仿單からの警告・禁忌・特定集団（小児・高齢者・妊婦・腎機能障害）の安全性情報の抽出（DG001 解消）
- DrugBank API によるデキサメタゾン MOA データの補充（DG002 解消）
- 口服 mini-pulse 療法の具体的な投与スケジュール（5mg 週 2 日間など）と日本国内での用量適合性の確認
- 長期コルチコステロイド使用に伴う副作用（HPA 軸抑制・骨粗鬆症・血糖上昇）のモニタリング計画策定
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

