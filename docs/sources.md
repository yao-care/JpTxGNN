---
layout: page
title: データソース
permalink: /sources/
---

# データソース

JpTxGNN は以下のデータソースを統合しています。

## 日本国内データソース

### SSK 薬価基準マスター

| 項目 | 内容 |
|------|------|
| 提供元 | 社会保険診療報酬支払基金 |
| URL | [https://www.ssk.or.jp/](https://www.ssk.or.jp/) |
| データ件数 | 19,317 薬品 |
| 含まれる情報 | 薬価基準コード、販売名、薬価、単位 |
| 更新頻度 | 毎月 |

### KEGG DRUG

| 項目 | 内容 |
|------|------|
| 提供元 | 京都大学化学研究所 |
| URL | [https://www.kegg.jp/kegg/drug/](https://www.kegg.jp/kegg/drug/) |
| データ件数 | 12,639 薬品 |
| 含まれる情報 | 効能・効果、分子式、ATC コード |
| 利用条件 | 学術研究目的 |

### PMDA（医薬品医療機器総合機構）

| 項目 | 内容 |
|------|------|
| 提供元 | 独立行政法人 医薬品医療機器総合機構 |
| URL | [https://www.pmda.go.jp/](https://www.pmda.go.jp/) |
| 含まれる情報 | 承認情報、添付文書、安全性情報 |

## 国際データソース

### DrugBank

| 項目 | 内容 |
|------|------|
| 提供元 | DrugBank Online |
| URL | [https://go.drugbank.com/](https://go.drugbank.com/) |
| データ件数 | 約 7,958 薬物（TxGNN 収録分） |
| 含まれる情報 | 国際標準識別子、薬理情報、相互作用 |
| 利用条件 | CC BY-NC 4.0（非商用） |

### TxGNN 知識グラフ

| 項目 | 内容 |
|------|------|
| 提供元 | Harvard Dataverse |
| URL | [https://dataverse.harvard.edu/](https://dataverse.harvard.edu/) |
| ノード数 | 約 129,000 |
| エッジ数 | 約 8,000,000 |
| 含まれる情報 | 薬物-疾病関係、タンパク質相互作用 |

### ClinicalTrials.gov

| 項目 | 内容 |
|------|------|
| 提供元 | 米国国立医学図書館 (NLM) |
| URL | [https://clinicaltrials.gov/](https://clinicaltrials.gov/) |
| 含まれる情報 | 臨床試験登録情報 |

### PubMed

| 項目 | 内容 |
|------|------|
| 提供元 | 米国国立医学図書館 (NLM) |
| URL | [https://pubmed.ncbi.nlm.nih.gov/](https://pubmed.ncbi.nlm.nih.gov/) |
| 含まれる情報 | 医学文献データベース |

## 日本臨床試験登録

### JPRN（Japan Primary Registries Network）

JpTxGNN は以下の日本臨床試験登録機関のデータを参照します：

| 登録機関 | 提供元 | URL |
|----------|--------|-----|
| UMIN-CTR | 大学病院医療情報ネットワーク | [https://www.umin.ac.jp/ctr/](https://www.umin.ac.jp/ctr/) |
| JapicCTI | 日本医薬情報センター | [https://www.clinicaltrials.jp/](https://www.clinicaltrials.jp/) |
| JMACCT | 日本医師会治験促進センター | [https://dbcentre3.jmacct.med.or.jp/](https://dbcentre3.jmacct.med.or.jp/) |

## データ統合フロー

```
SSK マスター ──────┐
                   ├──→ 統合データ ──→ DrugBank マッピング
KEGG DRUG ─────────┘
                                              ↓
                                        TxGNN 予測
                                              ↓
                                      リポジショニング候補
```

## データ品質指標

| 指標 | 値 | 目標 |
|------|----|------|
| SSK 薬品数 | 19,317 | - |
| KEGG マッチング率 | 40.8% | >30% |
| DrugBank マッピング率 | 22.5% | >20% |
| 疾病マッピング率 | 66.6% | >50% |

## ライセンスと利用条件

- **SSK データ**: 公開情報
- **KEGG データ**: 学術研究目的での利用
- **DrugBank**: CC BY-NC 4.0（非商用利用）
- **TxGNN**: 研究目的での利用

## 免責事項

本システムで使用するデータは、各提供元の利用規約に従って使用しています。
データの正確性については各提供元の情報を参照してください。

## 関連ページ

- [予測手法](/methodology/)
- [プロジェクト概要](/about/)
