---
layout: default
title: HL7 PDDI-CDS IG 技術ノート
parent: SMART on FHIR
nav_order: 10
description: HL7 Potential Drug-Drug Interaction Clinical Decision Support Implementation Guide の技術ノート
permalink: /smart/pddi-cds-notes/
---

# HL7 PDDI-CDS IG 技術ノート

HL7 Potential Drug-Drug Interaction Clinical Decision Support (PDDI-CDS) Implementation Guide は、薬物相互作用の臨床決定支援を標準化するための実装ガイドです。

---

## 概要

PDDI-CDS IG は以下を定義します：

- **データモデル**: DDI 情報の構造化
- **CDS Hooks**: 処方時のアラート
- **FHIR リソース**: DDI 情報の表現

---

## CDS Hooks フック

### order-select

処方入力時にトリガーされます。

```json
{
  "hook": "order-select",
  "hookInstance": "123",
  "context": {
    "userId": "Practitioner/123",
    "patientId": "Patient/456",
    "selections": ["MedicationRequest/789"],
    "draftOrders": {
      "resourceType": "Bundle",
      "entry": [
        {
          "resource": {
            "resourceType": "MedicationRequest",
            "medicationCodeableConcept": {
              "coding": [{
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "855332",
                "display": "Warfarin"
              }]
            }
          }
        }
      ]
    }
  }
}
```

### order-sign

処方確定時にトリガーされます。

---

## レスポンス形式

### 警告カード

```json
{
  "cards": [
    {
      "uuid": "card-001",
      "summary": "Warfarin + Aspirin: 出血リスク増加",
      "indicator": "warning",
      "detail": "Warfarin と Aspirin の併用は出血リスクを増加させます。",
      "source": {
        "label": "DDInter 2.0",
        "url": "https://ddinter2.scbdd.com/"
      },
      "suggestions": [
        {
          "label": "代替薬を検討",
          "actions": []
        }
      ]
    }
  ]
}
```

### 重大度インジケータ

| インジケータ | 意味 | 表示色 |
|-------------|------|--------|
| `critical` | 重大な相互作用 | 赤 |
| `warning` | 注意が必要 | 黄 |
| `info` | 参考情報 | 青 |

---

## JpTxGNN での活用

### ドラッグリポジショニング × DDI

ドラッグリポジショニング候補を検討する際、既存薬との相互作用も考慮が必要です。

```json
{
  "cards": [
    {
      "summary": "Famotidine: 新適応症候補あり",
      "indicator": "info",
      "detail": "TxGNN により esophagitis への効果が予測されています（スコア: 99%）",
      "source": {
        "label": "JpTxGNN",
        "url": "https://jptxgnn.yao.care/drugs/famotidine/"
      }
    },
    {
      "summary": "Famotidine + Ketoconazole: 吸収低下",
      "indicator": "warning",
      "detail": "Famotidine は胃酸を抑制し、Ketoconazole の吸収を低下させる可能性があります。"
    }
  ]
}
```

---

## 実装パターン

### 1. プリフェッチ

事前に必要なデータを取得します。

```json
{
  "prefetch": {
    "patient": "Patient/{{context.patientId}}",
    "medications": "MedicationRequest?patient={{context.patientId}}&status=active"
  }
}
```

### 2. DDI ルックアップ

```python
def check_ddi(drug1: str, drug2: str) -> dict | None:
    """DDI データベースを検索"""
    # DDInter API やローカルデータベースを検索
    pass
```

### 3. カード生成

```python
def generate_ddi_card(ddi: dict) -> dict:
    """CDS Hooks カードを生成"""
    return {
        "summary": f"{ddi['drug1']} + {ddi['drug2']}: {ddi['effect']}",
        "indicator": map_severity(ddi['severity']),
        "detail": ddi['description'],
        "source": {
            "label": ddi['source'],
            "url": ddi['url']
        }
    }
```

---

## 関連リンク

- [PDDI-CDS IG](http://hl7.org/fhir/uv/pddi/STU1/)
- [CDS Hooks 仕様](https://cds-hooks.org/)
- [DDInter 2.0](https://ddinter2.scbdd.com/)
