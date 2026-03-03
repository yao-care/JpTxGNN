---
layout: default
title: CDS Hooks アーキテクチャ設計
parent: SMART on FHIR
nav_order: 11
description: JpTxGNN CDS Hooks アーキテクチャ設計と実装パターン
permalink: /smart/cds-hooks-architecture/
---

# CDS Hooks アーキテクチャ設計

本ページでは、JpTxGNN の CDS Hooks 統合アーキテクチャを解説します。

---

## アーキテクチャ概要

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    EHR      │────▶│  CDS Hooks  │────▶│  JpTxGNN    │
│  システム   │◀────│   Service   │◀────│   API       │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   臨床医    │
                    │  (カード)   │
                    └─────────────┘
```

---

## コンポーネント

### 1. CDS Service Discovery

サービスの機能を公開します。

```json
{
  "services": [
    {
      "hook": "patient-view",
      "title": "JpTxGNN Drug Repurposing",
      "description": "患者の用薬に対するドラッグリポジショニング候補を表示",
      "id": "jptxgnn-repurposing",
      "prefetch": {
        "medications": "MedicationRequest?patient={{context.patientId}}&status=active"
      }
    },
    {
      "hook": "order-select",
      "title": "JpTxGNN Order Check",
      "description": "処方時にドラッグリポジショニング情報を提供",
      "id": "jptxgnn-order-check",
      "prefetch": {
        "patient": "Patient/{{context.patientId}}",
        "conditions": "Condition?patient={{context.patientId}}&clinical-status=active"
      }
    }
  ]
}
```

### 2. Hook Handler

リクエストを処理しカードを生成します。

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CDSRequest(BaseModel):
    hook: str
    hookInstance: str
    context: dict
    prefetch: dict = None

@app.post("/cds-services/jptxgnn-repurposing")
async def handle_repurposing(request: CDSRequest):
    # 用薬を抽出
    medications = extract_medications(request.prefetch.get("medications"))

    # JpTxGNN データベースを検索
    cards = []
    for med in medications:
        predictions = lookup_predictions(med)
        if predictions:
            cards.append(create_card(med, predictions))

    return {"cards": cards}
```

### 3. Card Generator

カードを生成します。

```python
def create_card(medication: dict, predictions: list) -> dict:
    """ドラッグリポジショニングカードを生成"""

    top_prediction = predictions[0]

    return {
        "uuid": str(uuid.uuid4()),
        "summary": f"{medication['name']}: 潜在的新適応症",
        "indicator": "info",
        "detail": f"TxGNN により {top_prediction['disease']} への効果が予測されています（スコア: {top_prediction['score']}%）",
        "source": {
            "label": "JpTxGNN",
            "url": f"https://jptxgnn.yao.care/drugs/{medication['slug']}/"
        },
        "links": [
            {
                "label": "詳細を見る",
                "url": f"https://jptxgnn.yao.care/drugs/{medication['slug']}/",
                "type": "absolute"
            }
        ]
    }
```

---

## フロー詳細

### patient-view フック

```
1. 臨床医がカルテを開く
2. EHR が patient-view フックをトリガー
3. CDS Service が用薬リストを取得（prefetch）
4. 各用薬について JpTxGNN を検索
5. 予測がある場合はカードを生成
6. EHR にカードを返却
7. 臨床医にカードを表示
```

### order-select フック

```
1. 臨床医が処方を入力
2. EHR が order-select フックをトリガー
3. CDS Service が処方内容と診断を取得
4. JpTxGNN でマッチングを確認
5. 関連する予測がある場合はカードを生成
6. EHR にカードを返却
```

---

## 設計パターン

### 1. Prefetch の活用

ネットワークラウンドトリップを削減します。

```json
{
  "prefetch": {
    "medications": "MedicationRequest?patient={{context.patientId}}&status=active",
    "conditions": "Condition?patient={{context.patientId}}&clinical-status=active"
  }
}
```

### 2. キャッシング

JpTxGNN データをキャッシュしてレスポンスを高速化します。

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def lookup_predictions(drug_slug: str) -> list:
    """予測を検索（キャッシュ付き）"""
    # search-index.json から検索
    pass
```

### 3. 非同期処理

複数の検索を並行実行します。

```python
import asyncio

async def handle_request(medications: list) -> list:
    tasks = [lookup_predictions_async(med) for med in medications]
    results = await asyncio.gather(*tasks)
    return results
```

---

## デプロイメント

### オプション 1: サーバーレス

```yaml
# AWS Lambda / Google Cloud Functions
functions:
  cds-service:
    handler: handler.main
    events:
      - http:
          path: /cds-services/{proxy+}
          method: any
```

### オプション 2: コンテナ

```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### オプション 3: 静的（現在の実装）

JpTxGNN は現在、静的サイトとして実装されています。完全な CDS Hooks サポートには動的サービスが必要です。

---

## 今後の展開

1. **動的 CDS Service の実装**
2. **EHR ベンダーとの連携テスト**
3. **CQL ルールとの統合**

---

## 関連リンク

- [CDS Hooks 仕様](https://cds-hooks.org/)
- [CDS Hooks Sandbox](https://sandbox.cds-hooks.org/)
- [HL7 CDS Hooks IG](http://hl7.org/fhir/uv/cds-hooks/)
