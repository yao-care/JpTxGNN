---
layout: default
title: Montelukast
parent: 僅模型預測 (L5)
nav_order: 100
evidence_level: L5
indication_count: 10
---

# Montelukast
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

# モンテルカスト：喘息から気管支炎へ

## 一言要約

モンテルカストはシステイニルロイコトリエン（CysLT1）受容体拮抗薬であり、世界的には喘息およびアレルギー性鼻炎の治療薬として広く使用されています。
TxGNN モデルは**気管支炎 (Bronchitis)** に有効である可能性を予測しており、特に細支気管支炎（Bronchiolitis）および移植後閉塞性細支気管支炎症候群（BOS）の領域において現在 **23 件の臨床試験**と **20 編の文献**がこの方向性を支持しています。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 喘息・アレルギー性鼻炎（世界承認；日本 PMDA データ未収載） |
| 予測新規適応症 | 気管支炎 (Bronchitis) |
| TxGNN 予測スコア | 99.95% |
| エビデンスレベル | L2 |
| 日本市販状況 | 未上市（PMDA 照会結果：0 件） |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails（研究段階） |

---

## この予測が妥当である理由

モンテルカストは選択的・経口活性の CysLT1 受容体拮抗薬であり、システイニルロイコトリエン（LTC4・LTD4・LTE4）が誘導する気道炎症、気管支痙攣、粘液過剰分泌、好酸球浸潤を選択的にブロックします。この作用機序は気管支の炎症性・閉塞性疾患全般に理論的に適用可能であり、喘息での豊富な臨床エビデンスがその機序的基盤を強固に支えています。

気管支炎と喘息はいずれも下気道の炎症を核心的病態として共有する疾患群です。特に急性ウイルス性細支気管支炎（RSV 感染など）では白三烯経路の活性化と尿中 LTE4 の上昇が確認されており、CysLT1 阻害により気道炎症の緩和と病後ウイルス誘発性喘鳴の抑制が期待されます。また、造血幹細胞移植（HSCT）後または肺移植後に発症する閉塞性細支気管支炎症候群（BOS）では、GVHD に伴う免疫炎症カスケードにロイコトリエンが直接関与することから、FAM 三聯療法（フルチカゾン＋アジスロマイシン＋モンテルカスト）が複数の Phase 2 試験で評価されています。

現時点では詳細な MOA データが本 Evidence Pack に収録されていませんが、白三烯シグナル阻害という機序は、急性ウイルス性気管支炎・反復閉塞性気管支炎・非喘息性好酸球性気管支炎・移植後慢性閉塞性気管支炎まで幅広い「気管支炎」スペクトラムへの適用可能性を機序的に裏付けています。

---

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT01307462](https://clinicaltrials.gov/study/NCT01307462) | Phase 2 | 完了 | 36 | HSCT 後 BOS 患者への FAM 三聯療法（Montelukast 含む）の有効性を評価；治療失敗基準 FEV1 ≥10% 低下を主要エンドポイントとした多施設共同試験 |
| [NCT01370187](https://clinicaltrials.gov/study/NCT01370187) | NA | 完了 | 146 | 乳幼児（3〜12 か月）の急性細支気管支炎および病後ウイルス誘発喘鳴に対する Montelukast の効果を直接評価 |
| [NCT00656058](https://clinicaltrials.gov/study/NCT00656058) | Phase 2 | 完了 | 25 | 同種・自家 HSCT 後閉塞性細支気管支炎への Montelukast 単独療法の多機関前向き Phase 2 試験 |
| [NCT04613180](https://clinicaltrials.gov/study/NCT04613180) | Phase 4 | 不明 | 100 | 反復閉塞性気管支炎（1〜7 歳児）における Montelukast の治療・予防効果を無作為割付で評価 |
| [NCT00863317](https://clinicaltrials.gov/study/NCT00863317) | NA | 完了 | 141 | 初発ウイルス性細支気管支炎乳児への毎日 Montelukast 投与の RCT；急性疾患期間の短縮を主要評価項目とする二重盲検プラセボ対照試験 |
| [NCT00524693](https://clinicaltrials.gov/study/NCT00524693) | NA | 完了 | 51 | 急性 RSV 細支気管支炎への Montelukast 二重盲検 RCT；白三烯上昇（CysLT）と炎症性サイトカインプロファイルへの影響を評価 |
| [NCT01211509](https://clinicaltrials.gov/study/NCT01211509) | Phase 4 | 完了 | 30 | 肺移植後 BOS（慢性拒絶）に対する Montelukast の二重盲検 RCT；同様の病態を持つ骨髄移植後 BOS での知見を基に設計 |
| [NCT03072849](https://clinicaltrials.gov/study/NCT03072849) | N/A | 完了 | 23 | HSCT 後早期スパイロメトリー検出と FAM 療法（Montelukast 含む）による閉塞性細支気管支炎の進行抑制・予防研究 |
| [NCT01121016](https://clinicaltrials.gov/study/NCT01121016) | Phase 4 | 不明 | 63 | 非喘息性好酸球性気管支炎（NAEB）に対する吸入ブデソニドへの Montelukast 追加療法；咳嗽 VAS スコアと気道好酸球減少を主要エンドポイントとする RCT |
| [NCT00394069](https://clinicaltrials.gov/study/NCT00394069) | Phase 2 | 完了 | 14 | 細支気管支炎乳児（3〜6 か月）を対象とした Montelukast 経口顆粒の安全性・忍容性・血漿濃度プロファイルの多施設評価 |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [25563311](https://pubmed.ncbi.nlm.nih.gov/25563311/) | 2015 | RCT | Chinese Medical Journal | 非喘息性好酸球性気管支炎（NAEB）において吸入ブデソニドへの Montelukast 追加療法は気道好酸球炎症を有意に抑制し、咳嗽重症度と QOL を改善 |
| [20976161](https://pubmed.ncbi.nlm.nih.gov/20976161/) | 2010 | RCT | PLoS One | 喘息患者において Montelukast は過換気誘発性気管支収縮（EVH）と気道炎症を有意に抑制；フィッシュオイルとの併用効果も評価 |
| [38485149](https://pubmed.ncbi.nlm.nih.gov/38485149/) | 2024 | Review | European Respiratory Journal | ERS/EBMT 共同診療ガイドライン：肺 cGVHD の複雑な管理において FAM 療法（Montelukast を含む）を標準的治療選択肢として位置付け |
| [38504551](https://pubmed.ncbi.nlm.nih.gov/38504551/) | 2024 | Review | Ther Adv Respir Dis | 肺・HSCT 後 BOS に対する Montelukast の治療可能性を包括的に概説；CysLT 阻害、NF-κB、TGF-β 関与の機序を考察 |
| [26475726](https://pubmed.ncbi.nlm.nih.gov/26475726/) | 2016 | Cohort | Biol Blood Marrow Transplant | HCT 後新発 BOS 36 例への FAM＋短期ステロイド療法の Phase 2 多施設試験；12 か月時点の FEV1 安定化に一定の有効性を確認 |
| [27229850](https://pubmed.ncbi.nlm.nih.gov/27229850/) | 2016 | Cohort | Respiratory Research | HSCT 後 BOS にブデソニド/ホルモテロール＋Montelukast＋N-アセチルシステイン投与で、ステロイド単独と比較して FEV1 低下が有意に抑制 |
| [35114411](https://pubmed.ncbi.nlm.nih.gov/35114411/) | 2022 | 前向き Phase II | Transplant Cell Ther | HCT 後 BOS への Montelukast 前向き Phase 2 多機関試験；CysLT 介在経路の阻害により肺機能低下に対する一定の抑制効果を示唆、病態機序の探索も実施 |
| [28545478](https://pubmed.ncbi.nlm.nih.gov/28545478/) | 2017 | Animal | J Cardiothoracic Surg | ラット肺移植後閉塞性細支気管支炎モデルで LTB4 が慢性拒絶の病態に関与することを確認；Montelukast が炎症・線維化を有意に抑制 |
| [20442434](https://pubmed.ncbi.nlm.nih.gov/20442434/) | 2010 | 動物実験 | Am J Respir Crit Care Med | 新生児期 RSV 初感染マウスへの Montelukast 投与により、再感染後の気道過敏性亢進・好酸球炎症・粘液過産生が予防；乳幼児期の使用根拠を支持 |
| [21486501](https://pubmed.ncbi.nlm.nih.gov/21486501/) | 2011 | Review | BMJ Clinical Evidence | 細支気管支炎（乳幼児下気道感染）の疫学・治療の系統的概説；ロイコトリエン拮抗薬を含む介入の現時点のエビデンスを整理 |

---

## 日本市販情報

PMDA データベース照会（2026-03-10）の結果、モンテルカストを有効成分とする日本承認取得薬剤の記録は確認されませんでした（照会件数 0 件）。

なお、モンテルカストは国際的にはシングレア®（Merck）等の商品名で喘息・アレルギー性鼻炎治療薬として欧米・アジア諸国で広く承認されています。PMDA 仿単データベースでの直接検索および最新版添付文書の確認を別途推奨します。

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

なお、文献エビデンスより以下の重要な安全性シグナルが確認されています：

- **神経精神系副作用**：FDA は 2020 年にモンテルカストの悪夢・睡眠障害・行動変化・自傷念慮等の神経精神系副作用に関するブラックボックス警告を追加しています。小児・青少年への使用時は特に注意が必要です（PMID [37758273](https://pubmed.ncbi.nlm.nih.gov/37758273/)、PMID [30905424](https://pubmed.ncbi.nlm.nih.gov/30905424/) 参照）。
- **好酸球性肉芽腫性多発血管炎（EGPA）**：ロイコトリエン受容体拮抗薬使用中にチャーグ・ストラウス症候群（EGPA）の発症報告があります（PMID [39959324](https://pubmed.ncbi.nlm.nih.gov/39959324/)）。

---

## 結論と次のステップ

**決定：Proceed with Guardrails（研究段階での進行）**

**理由：**
細支気管支炎（急性 RSV 型）および移植後閉塞性細支気管支炎症候群（BOS）に対するモンテルカストの有効性を支持する複数の Phase 2/4 完了試験が存在し、CysLT1 拮抗による気道炎症抑制という機序的妥当性も確立されています。ただし、一般的な急性気管支炎に対する直接の大規模 RCT は不足しており、現時点では「研究課題（Research Question）」段階に位置付けられます。

**進める場合に必要なもの：**
- 日本 PMDA 仿単の直接確認（MOA・警告・禁忌・相互作用データの取得）
- 適応症を疾患亜型別（急性ウイルス性細支気管支炎 / 反復閉塞性気管支炎 / 移植後 BOS）に分層した有効性評価
- 急性気管支炎に対する直接的な大規模 RCT データの収集
- FDA ブラックボックス警告（神経精神系副作用）を踏まえた安全性モニタリング計画の策定
- 日本国内での開発・承認申請に向けた規制戦略の検討
---

