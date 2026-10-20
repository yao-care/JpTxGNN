---
layout: default
title: Zanubrutinib
parent: 高エビデンス (L1-L2)
nav_order: 200
evidence_level: L2
indication_count: 1
last_modified_at: 2026-09-17
description: "Zanubrutinib：予測新適応症は骨髄性白血病 (myeloid leukemia)（エビデンスレベル L2）。既存適応症：日本の承認適応症は本サイトのデータに未収載"
---

# Zanubrutinib
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

# Zanubrutinib：B細胞リンパ腫から骨髄性白血病へ

## 一言まとめ

Zanubrutinib はもともと、マントル細胞リンパ腫、ワルデンストレームマクログロブリン血症などの B 細胞性悪性腫瘍の治療に用いられている。
TxGNN モデルは、本剤が**骨髄性白血病 (myeloid leukemia)** に有効である可能性を予測しており、
この方向性を **2 件の臨床試験**と **9 件の文献**が支持している。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：mantle cell lymphoma、B-cell neoplasm、lymphosarcoma） |
| 予測新適応症 | 骨髄性白血病 (myeloid leukemia) |
| TxGNN 予測スコア | 99.65% |
| エビデンスレベル | L2 (臨床試験の支持あり) |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Zanubrutinib は高選択性のブルトン型チロシンキナーゼ (BTK) 阻害薬である。
BTK は B 細胞受容体 (BCR) のシグナル伝達で重要な役割を担っており、BTK を阻害することで悪性 B 細胞の増殖と生存を遮断できる。

**作用機序：**
- BTK (Bruton tyrosine kinase) を阻害する。IC50 は約 20 nM
- ibrutinib と比べ、BTK 選択性が高い
- オフターゲット効果が少なく、心房細動などの副作用が少ない

BTK は主に B 細胞に発現しているが、近年の研究により、一部の骨髄性悪性腫瘍でも BTK が発現していることが報告されている。
これが、zanubrutinib が骨髄性白血病に有効であるとの予測の機序的な基盤になっている可能性がある。

## 臨床試験エビデンス

| 試験番号 | 相 | 状態 | 症例数 | 主な知見 |
|---------|------|------|------|---------|
| [NCT05665530](https://clinicaltrials.gov/study/NCT05665530) | Phase 1 | COMPLETED | 86 | PRT2527 (CDK9 阻害薬) と zanubrutinib の併用による再発・難治性血液悪性腫瘍の治療 |
| [NCT04477291](https://clinicaltrials.gov/study/NCT04477291) | Phase 1a/b | TERMINATED | 45 | CG-806 (luxeptinib) による再発・難治性急性骨髄性白血病または高リスク MDS の治療 |

## 文献エビデンス

| PMID | 発表年 | 種類 | 雑誌 | 主な知見 |
|------|-----|------|------|---------|
| [39647999](https://pubmed.ncbi.nlm.nih.gov/39647999/) | 2025 | RCT Phase 3 | J Clin Oncol | SEQUOIA 試験の 5 年追跡：未治療 CLL/SLL における zanubrutinib と BR の比較 |
| [40334067](https://pubmed.ncbi.nlm.nih.gov/40334067/) | 2025 | Phase 2 | Blood Advances | ibrutinib/acalabrutinib に不耐容の患者において zanubrutinib の忍容性は良好 |
| [40829104](https://pubmed.ncbi.nlm.nih.gov/40829104/) | 2026 | 試験横断解析 | Blood Advances | del(17p)/TP53 変異を有する CLL/SLL 患者における zanubrutinib の有効性解析 |
| [34959482](https://pubmed.ncbi.nlm.nih.gov/34959482/) | 2021 | レビュー | Pharmaceutics | TKI 時代の慢性白血病：CLL における BTK 阻害薬の役割 |
| [36402930](https://pubmed.ncbi.nlm.nih.gov/36402930/) | 2023 | レビュー | Leukemia | ワルデンストレームマクログロブリン血症における BTK 阻害薬の応用 |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 分子標的治療薬 (従来型の細胞毒性薬ではない) |
| 骨髄抑制リスク | 中等度 (好中球減少、血小板減少) |
| 出血リスク | 注意が必要。特に抗凝固薬との併用時 |
| モニタリング項目 | CBC (分画を含む)、肝機能、出血徴候 |
| 取り扱い上の防護 | 経口薬のため、一般的な薬剤の取り扱い基準に従って扱う |

## 安全性に関する考慮事項

**主要な薬物相互作用 (Major)：**

| 薬剤分類 | 代表的な薬剤 | 相互作用の機序 |
|---------|---------|-------------|
| 抗凝固薬/抗血小板薬 | Warfarin, Apixaban, Clopidogrel, Aspirin | 出血リスクの増加 |
| CYP3A 強力阻害薬 | Ketoconazole, Clarithromycin, Cobicistat | zanubrutinib の血中濃度を上昇させる |
| CYP3A 強力誘導薬 | Enzalutamide, Apalutamide, Mitotane | zanubrutinib の血中濃度を低下させる |
| 他の BTK 阻害薬 | Ibrutinib, Acalabrutinib | 薬理作用の重複 |
| 免疫抑制薬 | Adalimumab, Etanercept, Infliximab | 感染リスクの増加 |

**注意事項：**
- 手術前は休薬が必要（術前に少なくとも 3-7 日）
- B 型肝炎の再活性化リスクがあり、HBsAg/anti-HBc のモニタリングが必要
- 心房細動のリスクは ibrutinib より低いが、引き続きモニタリングが必要

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
Zanubrutinib の主な作用は B 細胞に対するものであるが、血液悪性腫瘍における幅広い有効性はすでに確認されている。
骨髄性白血病に対する予測には予備的な臨床試験の支持があるが、これらの試験は単剤使用ではなく併用療法を主に検討したものである。

**推進に必要な事項：**
- 骨髄性白血病における BTK の発現と機能の確認
- 骨髄性白血病を対象とした Phase 1/2 臨床試験の設計
- 骨髄性白血病の既存治療薬との併用効果の評価
- 有益性が見込まれる患者サブグループを予測するバイオマーカーの確立


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
