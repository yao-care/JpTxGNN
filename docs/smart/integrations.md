---
layout: default
title: 統合リソース
parent: SMART on FHIR
nav_order: 3
description: JpTxGNN 外部リソース統合 - ClinicalTrials.gov、PubMed、DDI チェック
permalink: /smart/integrations/
---

# 統合リソース

JpTxGNN SMART App は複数の外部リソースを統合し、ドラッグリポジショニング候補の包括的な評価を支援します。

---

## 統合リソース一覧

### 1. ClinicalTrials.gov

臨床試験情報をリアルタイムで検索し、予測されたドラッグリポジショニング候補に関連する臨床研究を確認できます。

| 項目 | 説明 |
|------|------|
| API バージョン | v2 |
| 検索戦略 | 医薬品名 + 疾患名 |
| 取得情報 | NCT 番号、試験フェーズ、ステータス、被験者数 |

### 2. PubMed

学術文献を検索し、予測の科学的根拠を確認できます。

| 項目 | 説明 |
|------|------|
| API | NCBI E-utilities |
| 検索戦略 | 医薬品名 + 疾患名 |
| 取得情報 | PMID、タイトル、年、ジャーナル、要約 |

### 3. DrugBank

医薬品の詳細情報を取得し、作用機序や薬理作用を確認できます。

| 項目 | 説明 |
|------|------|
| データソース | DrugBank Open Data |
| 取得情報 | 作用機序、薬理作用、適応症 |

### 4. KEGG DRUG

日本の医薬品薬効分類情報を取得します。

| 項目 | 説明 |
|------|------|
| データソース | KEGG DRUG |
| 取得情報 | 薬効分類、効能・効果 |

---

## CDS Hooks 統合

JpTxGNN は CDS Hooks 仕様に基づく臨床決定支援統合をサポートしています。

### サポートするフック

| フック | 説明 |
|------|------|
| `patient-view` | 患者カルテを開いた時にドラッグリポジショニング候補を表示 |
| `medication-prescribe` | 処方時に関連する新適応症候補を提示 |

### レスポンス形式

```json
{
  "cards": [
    {
      "summary": "Famotidine: 潜在的新適応症",
      "indicator": "info",
      "detail": "TxGNN により予測された適応症候補があります",
      "source": {
        "label": "JpTxGNN",
        "url": "https://jptxgnn.yao.care/drugs/famotidine/"
      }
    }
  ]
}
```

---

## 関連ドキュメント

- [CDS Hooks アーキテクチャ設計]({{ '/smart/cds-hooks-architecture/' | relative_url }})
- [ClinicalTrials.gov API v2 技術ノート]({{ '/smart/clinicaltrials-api-notes/' | relative_url }})
- [FHIR API 仕様]({{ '/smart/api-spec/' | relative_url }})
