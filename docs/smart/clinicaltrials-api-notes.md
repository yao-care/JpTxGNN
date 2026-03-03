---
layout: default
title: ClinicalTrials.gov API v2 技術ノート
parent: SMART on FHIR
nav_order: 8
description: ClinicalTrials.gov API v2 の技術メモと実装ガイド
permalink: /smart/clinicaltrials-api-notes/
---

# ClinicalTrials.gov API v2 技術ノート

ClinicalTrials.gov は 2024 年に API v2 を公開しました。本ページでは、JpTxGNN での統合に関する技術メモを記録します。

---

## API 概要

| 項目 | 値 |
|------|------|
| ベース URL | `https://clinicaltrials.gov/api/v2` |
| 認証 | 不要 |
| レート制限 | 3 リクエスト/秒 |
| 形式 | JSON |

---

## 主要エンドポイント

### /studies

臨床試験を検索します。

```
GET https://clinicaltrials.gov/api/v2/studies
```

**パラメータ**:

| パラメータ | 説明 | 例 |
|-----------|------|-----|
| `query.term` | 検索キーワード | `famotidine gastric ulcer` |
| `query.cond` | 疾患条件 | `gastric ulcer` |
| `query.intr` | 介入（医薬品等） | `famotidine` |
| `filter.overallStatus` | 試験ステータス | `RECRUITING` |
| `countTotal` | 総数を返す | `true` |
| `pageSize` | ページサイズ | `10` |

### /studies/{nctId}

特定の臨床試験を取得します。

```
GET https://clinicaltrials.gov/api/v2/studies/NCT12345678
```

---

## 検索例

### 医薬品 + 疾患で検索

```bash
curl "https://clinicaltrials.gov/api/v2/studies?query.intr=famotidine&query.cond=gastric%20ulcer&pageSize=5"
```

### Python での実装

```python
import requests

def search_clinical_trials(drug: str, disease: str, limit: int = 10):
    """ClinicalTrials.gov で臨床試験を検索"""
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.intr": drug,
        "query.cond": disease,
        "pageSize": limit,
        "countTotal": "true"
    }

    response = requests.get(url, params=params)
    data = response.json()

    studies = []
    for study in data.get("studies", []):
        protocol = study.get("protocolSection", {})
        identification = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})

        studies.append({
            "nct_id": identification.get("nctId"),
            "title": identification.get("briefTitle"),
            "status": status.get("overallStatus"),
            "phase": design.get("phases", []),
            "enrollment": status.get("enrollmentInfo", {}).get("count")
        })

    return {
        "total": data.get("totalCount", 0),
        "studies": studies
    }

# 使用例
results = search_clinical_trials("famotidine", "gastric ulcer")
print(f"Found {results['total']} studies")
```

---

## レスポンス構造

```json
{
  "studies": [
    {
      "protocolSection": {
        "identificationModule": {
          "nctId": "NCT12345678",
          "briefTitle": "Study Title"
        },
        "statusModule": {
          "overallStatus": "COMPLETED",
          "startDateStruct": {
            "date": "2020-01-01"
          }
        },
        "designModule": {
          "phases": ["PHASE3"],
          "studyType": "INTERVENTIONAL"
        }
      }
    }
  ],
  "totalCount": 100
}
```

---

## 注意事項

### レート制限

- **3 リクエスト/秒** の制限があります
- 大量検索時は適切な待機時間を設定してください

```python
import time

for drug in drugs:
    results = search_clinical_trials(drug, disease)
    time.sleep(0.4)  # 400ms 待機
```

### 検索のベストプラクティス

1. **具体的なキーワード**: 一般的すぎる用語は避ける
2. **同義語検索**: 疾患名の異なる表記を考慮
3. **フィルタ活用**: ステータスやフェーズで絞り込み

---

## JpTxGNN での活用

ドラッグリポジショニング候補の検証において：

1. **予測適応症の確認**: 予測された疾患に対する臨床試験の有無
2. **エビデンスレベル判定**: Phase 3 RCT の存在で L1 に分類
3. **研究トレンド**: 関連研究の動向把握

---

## 関連リンク

- [ClinicalTrials.gov API 公式ドキュメント](https://clinicaltrials.gov/data-api/api)
- [API v2 リファレンス](https://clinicaltrials.gov/data-api/about-api/api-reference)
