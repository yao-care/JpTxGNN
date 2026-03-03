---
layout: default
title: CQL 構文学習ノート
parent: SMART on FHIR
nav_order: 9
description: Clinical Quality Language (CQL) の構文と使用方法の学習ノート
permalink: /smart/cql-notes/
---

# CQL 構文学習ノート

Clinical Quality Language (CQL) は、臨床品質測定や臨床決定支援のための表現言語です。

---

## CQL とは

CQL は HL7 が策定した言語で、以下の目的で使用されます：

- **品質測定**: 医療品質指標の定義
- **臨床決定支援**: CDS ルールの記述
- **FHIR 統合**: FHIR リソースのクエリ

---

## 基本構文

### ライブラリ定義

```cql
library DrugRepurposingCheck version '1.0.0'

using FHIR version '4.0.1'

include FHIRHelpers version '4.0.1'

context Patient
```

### データ取得

```cql
// 患者の用薬を取得
define "Active Medications":
  [MedicationRequest: status in {'active', 'completed'}]

// 特定の医薬品を検索
define "Famotidine Prescriptions":
  "Active Medications" M
    where M.medication.coding.display contains 'famotidine'
```

### 条件評価

```cql
define "Has Gastric Ulcer":
  exists([Condition: code in "Gastric Ulcer Codes"])

define "Famotidine for New Indication":
  "Famotidine Prescriptions" M
    where not "Has Gastric Ulcer"
```

---

## ドラッグリポジショニングでの活用

### 適応症外使用の検出

```cql
library OffLabelDetection version '1.0.0'

using FHIR version '4.0.1'

// 医薬品の承認適応症
valueset "Famotidine Approved Indications": 'https://jptxgnn.yao.care/valueset/famotidine-approved'

// 患者の診断
define "Patient Conditions":
  [Condition: clinicalStatus ~ 'active']

// 適応症外使用の検出
define "Potential Off-Label Use":
  [MedicationRequest] M
    where M.medication.coding.display contains 'famotidine'
      and not exists(
        "Patient Conditions" C
          where C.code in "Famotidine Approved Indications"
      )
```

### TxGNN 予測の統合

```cql
// TxGNN 予測適応症
valueset "TxGNN Predicted Indications": 'https://jptxgnn.yao.care/valueset/famotidine-predicted'

// 予測適応症に該当する診断
define "Matches Predicted Indication":
  exists(
    "Patient Conditions" C
      where C.code in "TxGNN Predicted Indications"
  )

// アラート条件
define "Show Repurposing Alert":
  "Potential Off-Label Use" is not null
    and "Matches Predicted Indication"
```

---

## CQL 実行環境

### cqf-ruler

FHIR サーバー上で CQL を実行するための拡張機能。

```
POST /Library/$evaluate
```

### CQL Testing Framework

テスト用のオープンソースツール。

```bash
# CQL テスト実行
cql-testing run --library DrugRepurposingCheck
```

---

## ベストプラクティス

### 1. ValueSet の活用

```cql
// ハードコードを避ける
valueset "H2 Blockers": 'https://example.org/valueset/h2-blockers'

define "H2 Blocker Medications":
  [MedicationRequest: medication in "H2 Blockers"]
```

### 2. 再利用可能な定義

```cql
// 共通パターンを定義
define function MedicationsByClass(class System.Code):
  [MedicationRequest] M
    where M.medication.coding contains class
```

### 3. パフォーマンス考慮

```cql
// 必要なデータのみ取得
define "Recent Medications":
  "Active Medications" M
    where M.authoredOn after Now() - 90 days
```

---

## 関連リンク

- [CQL 仕様](https://cql.hl7.org/)
- [CQL Reference](https://cql.hl7.org/09-b-cqlreference.html)
- [cqf-ruler GitHub](https://github.com/DBCG/cqf-ruler)
