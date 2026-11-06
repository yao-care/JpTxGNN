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
| predicted_indication | 知識グラフ上で関係のある疾病（既知の関係。新規予測ではありません） |
| source | データソース（TxGNN Knowledge Graph） |

### drugs.json

公開している薬物ページの一覧です（1 薬物 1 件、件数は `total_count`）。

| フィールド | 説明 |
|------------|------|
| slug | 薬物ページの URL 名（`/drugs/<slug>/`） |
| name | 薬物名 |
| evidence_level | エビデンスレベル（薬物ページの見出しと同じ L1–L5） |
| indication_count | 予測適応症の件数（薬物ページの「予測適応症」の件数） |
| original_indication | 既存適応症。薬物ページのフロントマターに記載がある場合のみ入り、現在はすべて空欄（`""`）です |
| predicted_indication | 現在はすべて空欄（`""`）です。以前は薬物ページ本文から自動抽出していましたが、多くが表の見出し語を拾っていたため、2026-11-06 から値を入れていません。フィールドは互換性のために残しています |
| txgnn_score | 現在はすべて空欄（`""`）です（理由は predicted_indication と同じ） |
| url | 薬物ページの URL |

予測適応症とスコアは各薬物ページ、または [search-index.json](/data/search-index.json) を参照してください。知識グラフ上の既知の関係は repurposing_candidates.csv にあります。

出力例（生成ファイルからの抜粋）：

```json
{
  "generated": "2026-11-06",
  "total_count": {{ site.data.drug_stats.total_drugs }},
  "source": "JpTxGNN",
  "drugs": [
    {
      "slug": "famotidine",
      "name": "Famotidine",
      "evidence_level": "L5",
      "indication_count": 4,
      "original_indication": "",
      "predicted_indication": "",
      "txgnn_score": "",
      "url": "/drugs/famotidine/"
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
