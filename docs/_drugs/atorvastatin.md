---
layout: default
title: Atorvastatin
parent: 僅模型預測 (L5)
nav_order: 21
evidence_level: L5
indication_count: 10
---

# Atorvastatin
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

# アトルバスタチン：高脂血症 から 家族性高コレステロール血症 へ

## 一言要約

アトルバスタチンは HMG-CoA 還元酵素阻害薬（スタチン系）として、高脂血症・脂質異常症の治療に広く使用されてきた薬剤です。TxGNN モデルは**家族性高コレステロール血症（Familial Hypercholesterolemia）**に有効である可能性を予測しており、現在 **34 件の臨床試験**と **19 編の文献**がこの方向性を支持しています。ただし今回の PMDA 照会では日本国内の承認記録が確認されていません。

---

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 承認記録なし（高脂血症・脂質異常症治療薬として広く使用） |
| 予測新規適応症 | 家族性高コレステロール血症（Familial Hypercholesterolemia） |
| TxGNN 予測スコア | 99.42% |
| エビデンスレベル | L1 |
| 日本市販状況 | 未上市（PMDA 照会で承認記録なし） |
| 承認番号数 | 0 件 |
| 推奨決定 | Proceed with Guardrails |

---

## この予測が妥当である理由

アトルバスタチンは HMG-CoA（3-ヒドロキシ-3-メチルグルタリル補酵素 A）還元酵素を競合的に阻害し、肝細胞内の内因性コレステロール合成を抑制します。これに伴い肝細胞表面の LDL 受容体が代償性に上方制御され、血中 LDL-C が用量依存的に著明に低下します。また中性脂肪（TG）低下効果も有し、脂質プロファイル全般の改善に寄与します。

家族性高コレステロール血症（FH）は LDL 受容体遺伝子（LDLR）・アポリポ蛋白 B（APOB）・PCSK9 のいずれかに変異を持つ遺伝性疾患で、LDL 受容体機能の低下または欠失により血中 LDL-C が著しく上昇し、早期動脈硬化・心血管イベントリスクが大幅に高まります。アトルバスタチンは残存する LDL 受容体を最大限に活性化することで、とくにヘテロ接合体型（HeFH）患者において顕著な LDL-C 低下効果を発揮します。ホモ接合体型（HoFH）では受容体機能が著しく低下しているため単剤では不十分なケースもありますが、LDL アフェレーシスや ezetimibe・PCSK9 阻害薬との組み合わせで治療強度を高めることができます。

国際的には ACC/AHA・ESC/EAS などの主要ガイドラインで FH の一線治療として推奨されており、小児・青年期から成人まで幅広い年齢層で複数の Phase 3 RCT により長期有効性と安全性が確立されています。TxGNN モデルのスコア（99.42%）はこの確立された医学的コンセンサスと完全に一致しており、予測の妥当性を強く裏付けています。

---

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT00134485](https://clinicaltrials.gov/study/NCT00134485) | Phase 3 | 完了 | 400 | HeFH 患者に対する torcetrapib/atorvastatin vs. atorvastatin 単剤の多施設二重盲検 RCT。atorvastatin 単剤群の FH に対する有効性・安全性を直接確立 |
| [NCT00136981](https://clinicaltrials.gov/study/NCT00136981) | Phase 3 | 完了 | 800 | HeFH 患者における 24 ヵ月間頸動脈 B モード超音波によるアトルバスタチンの抗動脈硬化効果を評価した最大規模の長期試験 |
| [NCT03867318](https://clinicaltrials.gov/study/NCT03867318) | Phase 3 | 完了 | 621 | HeFH 患者においてアトルバスタチン 10 mg 単剤で LDL-C コントロール不十分な患者に ezetimibe 10 mg を追加した大規模二重盲検試験 |
| [NCT03882996](https://clinicaltrials.gov/study/NCT03882996) | Phase 3 | 完了 | 432 | HeFH または多重 CV リスク因子患者における ezetimibe + atorvastatin 10〜80 mg の 12 ヵ月長期安全性・耐容性を評価 |
| [NCT00827606](https://clinicaltrials.gov/study/NCT00827606) | Phase 3 | 完了 | 272 | HeFH 小児・青年期患者（3 年間前向き開放標識試験）でのコレステロール低下効果・成長発達指標（身長・体重・BMI・Tanner 分類）への影響を評価 |
| [NCT03884452](https://clinicaltrials.gov/study/NCT03884452) | Phase 3 | 完了 | 50 | HoFH 患者における ezetimibe 10 mg + atorvastatin（または simvastatin）併用療法の有効性・安全性を評価した第一優先試験 |
| [NCT03510884](https://clinicaltrials.gov/study/NCT03510884) | Phase 3 | 完了 | 153 | 8〜17 歳 HeFH 小児・青年期患者に対して alirocumab の有効性をアトルバスタチン背景治療下で評価した二重盲検プラセボ対照 RCT |
| [NCT01507831](https://clinicaltrials.gov/study/NCT01507831) | Phase 3 | 完了 | 2341 | 高 CV リスク高コレステロール血症患者（FH 含む）を対象とした alirocumab 長期安全性試験。アトルバスタチンが主要背景治療として使用 |
| [NCT00134511](https://clinicaltrials.gov/study/NCT00134511) | Phase 3 | 完了 | 30 | HoFH 患者に対する torcetrapib/atorvastatin の強制漸増（強度強化）試験でアトルバスタチンの HoFH における限界と可能性を評価 |
| [NCT00739999](https://clinicaltrials.gov/study/NCT00739999) | Phase 1 | 完了 | 39 | HeFH 小児・青年期患者（8 週間）におけるアトルバスタチンの薬物動態・薬力学・安全性・耐容性の基礎データを確立 |

---

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [9793596](https://pubmed.ncbi.nlm.nih.gov/9793596/) | 1998 | RCT | Ann Pharmacother | 原発性高コレステロール血症・混合型脂質異常症（FH 含む）に対するアトルバスタチンの有効性・安全性を総括した初期臨床レビュー |
| [11058703](https://pubmed.ncbi.nlm.nih.gov/11058703/) | 2000 | Cohort | Atherosclerosis | LDL アフェレーシス施行中の HoFH 患者 9 例にアトルバスタチン 10〜40 mg を漸増投与した結果、5 例で血清脂質の有意な改善を確認 |
| [27417002](https://pubmed.ncbi.nlm.nih.gov/27417002/) | 2016 | Cohort | JACC | HeFH 患者におけるスタチン治療が冠動脈疾患イベントおよび全死亡を有意に低下させることを大規模コホートで実証 |
| [27678432](https://pubmed.ncbi.nlm.nih.gov/27678432/) | 2016 | Cohort | J Clin Lipidology | 6〜17 歳 HeFH 小児・青年期患者において 3 年間のアトルバスタチン投与が持続的な LDL-C 低下効果を示し、長期安全性を確認 |
| [39751968](https://pubmed.ncbi.nlm.nih.gov/39751968/) | 2025 | Review | Curr Atheroscler Rep | HoFH 治療の最新動向をレビュー。スタチン系薬剤を基盤に PCSK9 阻害薬・inclisiran・evinacumab 等の新規薬剤との組み合わせ戦略を概説 |
| [9129869](https://pubmed.ncbi.nlm.nih.gov/9129869/) | 1997 | Review | Drugs | アトルバスタチンの薬理学・代謝・高脂血症治療における臨床効果と安全性の包括的レビュー |
| [26988948](https://pubmed.ncbi.nlm.nih.gov/26988948/) | 2016 | Review | JACC | FH 患者のモニタリングと管理改善に関する提言。スタチンを中心とした LDL-C 目標達成と長期フォローアップ体制の重要性を強調 |
| [35361995](https://pubmed.ncbi.nlm.nih.gov/35361995/) | 2022 | Cohort | Pharmacogenomics J | FH 遺伝子診断パネルとスタチン薬理ゲノミクス遺伝子（SLCO1B1 等）を統合した NGS 戦略の実装研究。個別化スタチン処方の実現可能性を提示 |
| [32800790](https://pubmed.ncbi.nlm.nih.gov/32800790/) | 2020 | Case series | J Clin Lipidology | 複合ヘテロ接合体型 FH 小児（LDL-C 17.4 mmol/L）における 10 年間の治療経過を報告。アトルバスタチンを含む積極的多剤療法で管理に成功 |
| [28437620](https://pubmed.ncbi.nlm.nih.gov/28437620/) | 2017 | Review | Endocr Pract | AACE/ACE 脂質異常症・CV 疾患予防ガイドライン。FH 患者に対する高強度スタチン療法（アトルバスタチン含む）を明確に推奨 |

---

## 安全性に関する考慮事項

安全性情報については添付文書を参照してください。

---

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
家族性高コレステロール血症に対するアトルバスタチンの有効性は、複数の大規模 Phase 3 RCT（HeFH・HoFH・成人・小児を含む）によりエビデンスレベル L1 として確立されており、国際ガイドラインでも一線治療として推奨されている。ただし今回の PMDA 照会では日本国内の承認記録が取得できておらず、規制上の根拠を改めて確認する必要がある。

**進める場合に必要なもの：**
- PMDA での正確な承認状況の再確認（日本市場での実際の承認・販売状況を把握）
- 仿単 PDF の取得・解析による警告・禁忌・薬物相互作用情報の補完（データギャップ DG001 の解消）
- DrugBank API 照会による正式な作用機序（MOA）データの取得（DG002 の解消）
- 日本人 FH 患者における薬理ゲノミクス（SLCO1B1・CYP3A4 多型等）を考慮した用量調整指針の確認
- HoFH（重症型）患者に対する PCSK9 阻害薬・ezetimibe との併用レジメンの日本国内適用可否の検討
---

