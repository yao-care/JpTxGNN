---
layout: default
title: データダウンロード
parent: リソース
nav_order: 2
description: "JpTxGNN 予測データのダウンロード"
permalink: /downloads/
---

# データダウンロード

JpTxGNN の予測データをダウンロードできます。

## 利用可能なデータ

### リポジショニング候補データ

| ファイル | 形式 | 説明 |
|----------|------|------|
| [repurposing_candidates.csv](/data/repurposing_candidates.csv) | CSV | 知識グラフ（TxGNN KG）に記録済みの薬物–疾病関係（既知用途の照合に使用、新規予測ではありません） |
| [drugs.json](/data/drugs.json) | JSON | 薬物情報一覧 |
| [search-index.json](/data/search-index.json) | JSON | 検索インデックス |

### FHIR R4 リソース

| ファイル | 形式 | 説明 |
|----------|------|------|
| [all-predictions.json](/fhir/Bundle/all-predictions.json) | FHIR Bundle | 全予測データ |
| [metadata](/fhir/metadata) | FHIR CapabilityStatement | サーバー機能情報 |

詳細は [FHIR API ドキュメント](/fhir-api/) を参照してください。

## データ形式

### repurposing_candidates.csv

| カラム | 説明 |
|--------|------|
| approval_number | 承認番号 |
| brand_name | 日本での販売名 |
| ingredient | 有効成分（英語） |
| drugbank_id | DrugBank 識別子 |
| predicted_indication | 知識グラフ上で関係のある疾病 |
| source | データソース（TxGNN Knowledge Graph） |

### drugs.json

```json
{
  "generated": "2026-03-02",
  "total_count": 123,
  "drugs": [
    {
      "slug": "famotidine",
      "name": "FAMOTIDINE",
      "drugbank_id": "DB00927",
      "indication_count": 9,
      "original_indication": "胃潰瘍、十二指腸潰瘍...",
      "predicted_indication": "dyspepsia、peptic esophagitis..."
    }
  ]
}
```

## 利用条件

- **利用目的**: 研究目的のみ
- **再配布**: 出典を明記の上、非商用目的で許可
- **商用利用**: 禁止

## 引用方法

本データを研究で使用する場合は、以下のように引用してください：

```
JpTxGNN - 日本医薬品リポジショニング予測システム
https://jptxgnn.yao.care/
```

## 免責事項

- 予測データは研究参考のみを目的としています
- 医療判断には使用しないでください
- データの正確性については保証しません

## 関連ページ

- [FHIR API](/fhir-api/)
- [予測手法](/methodology/)
- [データソース](/sources/)
