---
layout: page
title: FHIR API
permalink: /fhir-api/
---

# FHIR R4 API ドキュメント

JpTxGNN は医薬品リポジショニング予測データを FHIR R4 形式で提供しています。

## エンドポイント

ベース URL: `https://jptxgnn.yao.care/fhir`

### CapabilityStatement (Metadata)

```
GET /fhir/metadata
```

サーバーの機能と対応リソースタイプを取得します。

### MedicationKnowledge

医薬品の情報を取得します。

```
GET /fhir/MedicationKnowledge/{drug-slug}.json
```

例:
```bash
curl https://jptxgnn.yao.care/fhir/MedicationKnowledge/famotidine.json
```

レスポンス例:
```json
{
  "resourceType": "MedicationKnowledge",
  "id": "famotidine",
  "status": "active",
  "code": {
    "coding": [{
      "system": "https://jptxgnn.yao.care/drugs",
      "code": "famotidine",
      "display": "ファモチジン"
    }]
  },
  "intendedJurisdiction": [{
    "coding": [{
      "system": "urn:iso:std:iso:3166",
      "code": "JP",
      "display": "Japan"
    }]
  }]
}
```

### ClinicalUseDefinition

予測された適応症の情報を取得します。

```
GET /fhir/ClinicalUseDefinition/{drug-slug}-{disease-slug}.json
```

例:
```bash
curl https://jptxgnn.yao.care/fhir/ClinicalUseDefinition/famotidine-dyspepsia.json
```

### Bundle

全リソースを含む Bundle を取得します。

```
GET /fhir/Bundle/all-predictions.json
```

## リソースタイプ

| タイプ | 説明 | 数量 |
|--------|------|------|
| MedicationKnowledge | 医薬品情報 | 3,952 |
| ClinicalUseDefinition | 予測適応症 | 37,686 |
| Bundle | 全リソース集約 | 1 |

## Extension

### evidence-level

予測のエビデンスレベルを示します。

```json
{
  "url": "https://jptxgnn.yao.care/fhir/StructureDefinition/evidence-level",
  "valueCode": "L5"
}
```

### prediction-status

予測のステータスを示します。

```json
{
  "url": "https://jptxgnn.yao.care/fhir/StructureDefinition/prediction-status",
  "valueCode": "predicted"
}
```

## SMART on FHIR

SMART App Launch をサポートしています。

Launch URL: `https://jptxgnn.yao.care/smart/launch.html`

## 制限事項

- 静的 API のため、検索機能は限定的です
- 全データの取得には Bundle を使用してください
- レート制限はありません（GitHub Pages による制限を除く）

## 免責事項

このAPIを通じて提供されるデータは研究目的のみです。医療判断には使用しないでください。
