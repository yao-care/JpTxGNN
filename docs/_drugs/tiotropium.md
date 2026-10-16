---
layout: default
title: Tiotropium
parent: 高エビデンスレベル
nav_order: 308
evidence_level: L1
indication_count: 10
monitor_inn: "Tiotropium"
predicted_indications: ["obstructive lung disease", "respiratory malformation", "Rienhoff syndrome", "COPD, severe early onset", "chronic obstructive pulmonary disease", "compensatory emphysema", "interstitial emphysema", "hyperlucent lung", "tracheal stenosis", "susceptibility to respiratory infections associated with CD8alpha chain mutation"]
last_modified_at: 2026-10-17
description: "Tiotropium：予測新適応症は閉塞性肺疾患 (Obstructive Lung Disease)（エビデンスレベル L1）。既存適応症：気管支炎、喘息、内因性喘息、アレルギー性喘息、肺気腫"
---

# Tiotropium
{: .fs-9 }

エビデンスレベル: **L1** | 予測適応症: **10** 件
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

# チオトロピウム：気管支炎・喘息・肺気腫から閉塞性肺疾患へ

## 一言要約

チオトロピウムは長時間作用型の抗コリン薬（吸入）で、元々気管支炎、喘息、肺気腫などの治療に使用されていました。
TxGNN モデルは**閉塞性肺疾患 (Obstructive Lung Disease)** に有効である可能性を予測しており、現在 **35 件以上の臨床試験**と **20 編の文献**がこの方向性を支持しています。
ただし、この適応症は既存の適応症と重なっており、新規の再利用というより既知の効果の確認にあたります。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 気管支炎、喘息、内因性喘息、アレルギー性喘息、肺気腫 |
| 予測新規適応症 | 閉塞性肺疾患 (Obstructive Lung Disease) |
| TxGNN 予測スコア | 99.99% |
| エビデンスレベル | L1 |
| 日本市販状況 | 販売承認は取消済み（現在市販なし） |
| 承認番号数 | 3 件（すべて取消） |
| 推奨決定 | Proceed with Guardrails |

## この予測が妥当である理由

現在、詳細な作用機序データはありません。一般的な薬理学の知見では、チオトロピウムは長時間作用型ムスカリン拮抗薬（LAMA）です。気道平滑筋の M3 受容体を遮断して持続的な気管支拡張をもたらし、コリン作動性の気管支収縮tone を弱めます。文献でも、M3 受容体からの解離が遅く、1 日 1 回の投与が可能であることが報告されています。

既存適応症（気管支炎、喘息、肺気腫）はいずれも気道閉塞を伴う疾患で、閉塞性肺疾患と病態が大きく重なります。そのため機序的には自然な適用です。

なお、今回の予測は既存適応症の範囲内にあるため、真の意味での新規再利用シグナルではありません。

## 臨床試験エビデンス

閉塞性肺疾患について、関連性の高い試験を示します（最大 10 件）。

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT01431274](https://clinicaltrials.gov/study/NCT01431274) | Phase 3 | 完了 | 2624 | COPD に対する、チオトロピウム＋オロダテロール配合剤の 52 週間の有効性・安全性を単剤と比較 |
| [NCT00240435](https://clinicaltrials.gov/study/NCT00240435) | Phase 3 | 完了 | 491 | COPD でレスピマット 2 用量をプラセボおよびイプラトロピウムと比較（気管支拡張効果と安全性） |
| [NCT00877383](https://clinicaltrials.gov/study/NCT00877383) | Phase 3 | 完了 | 1142 | 中等症〜重症 COPD でインダカテロール併用とチオトロピウム単独を 12 週間比較 |
| [NCT00157235](https://clinicaltrials.gov/study/NCT00157235) | Phase 3 | 完了 | 234 | 呼吸リハビリ中の COPD 患者で運動耐容能への影響をプラセボと比較 |
| [NCT00144326](https://clinicaltrials.gov/study/NCT00144326) | Phase 3 | 完了 | 250 | COPD で 12 週間、日常の身体活動量への影響をプラセボと比較 |
| [NCT02172443](https://clinicaltrials.gov/study/NCT02172443) | Phase 3 | 完了 | 50 | COPD でチオトロピウムカプセルとイプラトロピウム MDI を比較（小規模） |
| [NCT01316380](https://clinicaltrials.gov/study/NCT01316380) | Phase 3 | 完了 | 465 | 軽症持続型喘息で 12 週間、プラセボと比較 |
| [NCT00772538](https://clinicaltrials.gov/study/NCT00772538) | Phase 3 | 完了 | 459 | 重症持続型喘息で、通常治療への上乗せとして 48 週間プラセボと比較 |
| [NCT04780984](https://clinicaltrials.gov/study/NCT04780984) | Phase 2 | 完了 | 116 | COPD での吸入液の用量設定、薬力学・相対バイオアベイラビリティ・安全性の検討 |
| [NCT04999930](https://clinicaltrials.gov/study/NCT04999930) | 該当なし | 完了 | 100 | COPD でレスピマットのスペーサー（エアロチャンバー）使用の有無による有効性・満足度の比較 |

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [28877027](https://pubmed.ncbi.nlm.nih.gov/28877027/) | 2017 | RCT | N Engl J Med | 軽症〜中等症 COPD でのチオトロピウム長期使用による肺機能改善と低下抑制を検証 |
| [29779416](https://pubmed.ncbi.nlm.nih.gov/29779416/) | 2018 | RCT | Am J Respir Crit Care Med | 長期トリプル療法からインダカテロール/グリコピロニウムへの de-escalation を検討（SUNSET 試験） |
| [16844726](https://pubmed.ncbi.nlm.nih.gov/16844726/) | 2006 | Meta-analysis | Thorax | 安定期 COPD に対するチオトロピウムの有効性を臨床イベント、症状、肺機能、有害事象から評価 |
| [25046211](https://pubmed.ncbi.nlm.nih.gov/25046211/) | 2014 | Systematic review | Cochrane Database Syst Rev | COPD でチオトロピウムとプラセボを比較（ソフトミスト吸入器の新規試験を含む更新） |
| [32727455](https://pubmed.ncbi.nlm.nih.gov/32727455/) | 2020 | Review | Respir Res | COPD におけるチオトロピウムの臨床開発のレビュー。LAMA 単剤が GOLD B・C・D 群の初期治療として推奨 |
| [12010082](https://pubmed.ncbi.nlm.nih.gov/12010082/) | 2002 | Review | Drugs | M1/M2/M3 受容体拮抗薬で、M3 からの解離が遅く 1 日 1 回投与が可能。COPD で肺機能を改善 |
| [31119643](https://pubmed.ncbi.nlm.nih.gov/31119643/) | 2019 | Review | Drugs | チオトロピウム/オロダテロール配合剤の COPD 維持療法に関するレビュー |
| [23728670](https://pubmed.ncbi.nlm.nih.gov/23728670/) | 2013 | Systematic review | Cochrane Database Syst Rev | COPD で吸入ステロイド/LABA 配合剤とチオトロピウムの相対的な効果と害を比較 |
| [21672999](https://pubmed.ncbi.nlm.nih.gov/21672999/) | 2011 | Meta-analysis | BMJ | COPD でチオトロピウムのミスト吸入器長期使用と死亡リスクの関連を検討 |
| [32274526](https://pubmed.ncbi.nlm.nih.gov/32274526/) | 2020 | Meta-analysis | Eur J Clin Pharmacol | COPD でチオトロピウム使用と心血管系有害事象リスクの関連を RCT のメタ解析で検討 |

## 日本市販情報

| 承認番号 | 商品名 | 剤形 | 承認適応症 |
|---------|------|------|-----------|
| 622507801 | スピリーバ1.25μgレスピマット60吸入 | 吸入 75μg | 取消済み |
| 621984201 | スピリーバ2.5μgレスピマット60吸入 | 吸入 150μg | 取消済み |
| 620002421 | スピリーバ吸入用カプセル18μg | カプセル 18μg | 取消済み |

3 件の承認はすべて取消済みで、現在、日本で有効な承認はありません。

## 安全性に関する考慮事項

- **禁忌（知識グラフ上の関連疾患。添付文書の記載ではありません）**：前立腺肥大症、腎機能障害、閉塞隅角緑内障、膀胱頸部閉塞
- **薬物相互作用**：100 件の相互作用が検出されています。主なものは次のとおりです。
  - 他の抗コリン薬（Moderate）：ヒヨスチアミン、アトロピン、グリコピロニウム、クリジニウム、ジサイクロミン、トロスピウム、メペンゾラート、メスコポラミン、プロパンテリン、スコポラミンなど。抗コリン作用が重なる可能性があります。
  - その他（Moderate）：エルクサドリン、プルカロプリド、吸入ヒトインスリン（速効型）
  - シメチジン（Minor）

添付文書の警告・禁忌の詳細は、今回のデータには含まれていません。添付文書を参照してください。

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
- COPD を含む閉塞性肺疾患について、完了した複数の Phase 3 RCT と、RCT・メタ解析・Cochrane レビューがあり、エビデンスは L1 に相当します。
- ただし、この適応症は既存適応症と重なる確認的な内容で、新規再利用ではありません。日本での承認も取消済みで、作用機序と添付文書の安全性データも不足しています。

**進める場合に必要なもの：**
- 詳細な作用機序データ（MOA）の補完
- 日本の添付文書（警告・禁忌）の取得と確認
- 販売承認の取消理由の確認と、現在の供給状況の確認
- 前立腺肥大症、緑内障、腎機能障害を持つ患者に対する安全性モニタリング計画

### 参考：その他の予測適応症

TxGNN のスコアはいずれも 99.8% 以上ですが、以下は実質的な根拠が乏しい状況です。

| 予測適応症 | エビデンスレベル | 推奨 | 備考 |
|-----------|----------------|------|------|
| 慢性閉塞性肺疾患 | L1 | Proceed with Guardrails | 既存適応症の範囲内で確認的な内容 |
| 重症早期発症 COPD | L4 | Research Question | COPD のサブタイプで間接的な根拠のみ。試験なし |
| 呼吸器奇形 | L5 | Hold | 嚢胞性線維症の試験は関連が低く、機序の根拠なし |
| Rienhoff 症候群、代償性肺気腫、間質性肺気腫、過透過性肺、気管狭窄、CD8α鎖変異関連の呼吸器感染感受性 | L5 | Hold | TxGNN の予測のみで、試験・文献なし |
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---



<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**販売名（規格別）**：スピリーバ1.25μgレスピマット60吸入 75μg、スピリーバ2.5μgレスピマット60吸入 150μg、スピリーバ吸入用カプセル18μg
<!-- brand-names:end -->

