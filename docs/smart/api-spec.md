---
layout: default
title: FHIR API 仕様
parent: SMART on FHIR
nav_order: 6
description: JpTxGNN FHIR R4 API の詳細仕様
permalink: /smart/api-spec/
---

# FHIR API 仕様

JpTxGNN は HL7 FHIR R4 準拠の静的 API を提供します。

---

## 概要

| 項目 | 値 |
|------|------|
| FHIR バージョン | R4 (4.0.1) |
| ベース URL | `https://jptxgnn.yao.care/fhir` |
| 形式 | application/fhir+json |
| 認証 | 不要（公開 API） |

---

## エンドポイント

### CapabilityStatement

サーバーの機能を記述します。

```
GET /fhir/metadata
```

**レスポンス例**:
```json
{
  "resourceType": "CapabilityStatement",
  "status": "active",
  "fhirVersion": "4.0.1",
  "format": ["application/fhir+json"],
  "rest": [
    {
      "mode": "server",
      "resource": [
        {
          "type": "MedicationKnowledge",
          "interaction": [{"code": "read"}]
        },
        {
          "type": "ClinicalUseDefinition",
          "interaction": [{"code": "read"}]
        }
      ]
    }
  ]
}
```

### MedicationKnowledge

医薬品情報を取得します。

```
GET /fhir/MedicationKnowledge/{id}.json
```

**パラメータ**:
- `{id}`: 医薬品スラッグ（例: `famotidine`）

**レスポンス例**:
```json
{
  "resourceType": "MedicationKnowledge",
  "id": "famotidine",
  "status": "active",
  "code": {
    "coding": [
      {
        "system": "https://jptxgnn.yao.care/drugs",
        "code": "famotidine",
        "display": "ガスター散２％"
      }
    ]
  },
  "intendedJurisdiction": [
    {
      "coding": [
        {
          "system": "urn:iso:std:iso:3166",
          "code": "JP",
          "display": "Japan"
        }
      ]
    }
  ]
}
```

### ClinicalUseDefinition

予測適応症情報を取得します。

```
GET /fhir/ClinicalUseDefinition/{id}.json
```

**パラメータ**:
- `{id}`: リソース ID（例: `famotidine-esophagitis-disease`）

**レスポンス例**:
```json
{
  "resourceType": "ClinicalUseDefinition",
  "id": "famotidine-esophagitis-disease",
  "type": "indication",
  "subject": [
    {
      "reference": "MedicationKnowledge/famotidine"
    }
  ],
  "indication": {
    "diseaseSymptomProcedure": {
      "concept": {
        "text": "esophagitis (disease)"
      }
    }
  },
  "extension": [
    {
      "url": "https://jptxgnn.yao.care/fhir/StructureDefinition/txgnn-score",
      "valueDecimal": 0.99
    }
  ]
}
```

### Bundle

全 MedicationKnowledge リソースを含む Bundle を取得します。

```
GET /fhir/Bundle/all-predictions.json
```

---

## カスタム拡張

### txgnn-score

TxGNN 予測スコア（0-1）を表します。

```json
{
  "url": "https://jptxgnn.yao.care/fhir/StructureDefinition/txgnn-score",
  "valueDecimal": 0.99
}
```

### evidence-level

エビデンスレベルを表します。

```json
{
  "url": "https://jptxgnn.yao.care/fhir/StructureDefinition/evidence-level",
  "valueCode": "L5"
}
```

### prediction-status

予測ステータスを表します。

```json
{
  "url": "https://jptxgnn.yao.care/fhir/StructureDefinition/prediction-status",
  "valueCode": "predicted"
}
```

---

## 使用例

### cURL

```bash
# CapabilityStatement を取得
curl https://jptxgnn.yao.care/fhir/metadata

# Famotidine の情報を取得
curl https://jptxgnn.yao.care/fhir/MedicationKnowledge/famotidine.json

# 全 MedicationKnowledge を取得
curl https://jptxgnn.yao.care/fhir/Bundle/all-predictions.json
```

### JavaScript

```javascript
// Famotidine の情報を取得
const response = await fetch('https://jptxgnn.yao.care/fhir/MedicationKnowledge/famotidine.json');
const medication = await response.json();
console.log(medication.code.coding[0].display);
```

### Python

```python
import requests

# Famotidine の情報を取得
response = requests.get('https://jptxgnn.yao.care/fhir/MedicationKnowledge/famotidine.json')
medication = response.json()
print(medication['code']['coding'][0]['display'])
```

---

## 制限事項

- **読み取り専用**: 書き込み操作はサポートしていません
- **静的ファイル**: データは定期的に更新される静的ファイルです
- **検索なし**: 検索パラメータはサポートしていません

---

## 関連リンク

- [HL7 FHIR R4 仕様](https://www.hl7.org/fhir/)
- [MedicationKnowledge](https://www.hl7.org/fhir/medicationknowledge.html)
- [ClinicalUseDefinition](https://www.hl7.org/fhir/clinicalusedefinition.html)
