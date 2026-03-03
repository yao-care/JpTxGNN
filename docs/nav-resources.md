---
layout: default
title: リソース
nav_order: 6
has_children: true
description: "データソース、ダウンロード、研究ケースなどのリソース"
permalink: /resources/
---

# リソース

<p class="key-answer" data-question="JpTxGNN のリソースとは？">
JpTxGNN プロジェクトで使用しているデータソース、ダウンロード可能なデータ、研究ケースなどのリソースを提供しています。
</p>

---

## クイックアクセス

<style>
.resource-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}
.resource-card {
  display: flex;
  align-items: center;
  padding: 1.25rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
  border-left: 5px solid;
}
.resource-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.resource-card.sources { border-color: #1565C0; }
.resource-card.downloads { border-color: #2E7D32; }
.resource-card.cases { border-color: #7B1FA2; }

.resource-card-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  flex-shrink: 0;
  font-size: 1.5rem;
}
.resource-card.sources .resource-card-icon { background: #E3F2FD; }
.resource-card.downloads .resource-card-icon { background: #E8F5E9; }
.resource-card.cases .resource-card-icon { background: #F3E5F5; }

.resource-card-info {
  flex: 1;
}
.resource-card-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #333;
}
.resource-card-desc {
  font-size: 0.8rem;
  color: #666;
}
</style>

<div class="resource-cards">
  <a href="{{ '/sources/' | relative_url }}" class="resource-card sources">
    <div class="resource-card-icon">📊</div>
    <div class="resource-card-info">
      <div class="resource-card-title">データソース</div>
      <div class="resource-card-desc">使用しているデータベースの説明</div>
    </div>
  </a>

  <a href="{{ '/downloads/' | relative_url }}" class="resource-card downloads">
    <div class="resource-card-icon">📥</div>
    <div class="resource-card-info">
      <div class="resource-card-title">データダウンロード</div>
      <div class="resource-card-desc">予測結果データのダウンロード</div>
    </div>
  </a>

  <a href="{{ '/cases/' | relative_url }}" class="resource-card cases">
    <div class="resource-card-icon">📚</div>
    <div class="resource-card-info">
      <div class="resource-card-title">研究ケース</div>
      <div class="resource-card-desc">ドラッグリポジショニングの成功例</div>
    </div>
  </a>
</div>

---

## 外部リソース

### 予測モデル

| リソース | 説明 |
|----------|------|
| [TxGNN (Harvard)](https://zitniklab.hms.harvard.edu/projects/TxGNN/) | 元の TxGNN プロジェクト |
| [TxGNN Paper](https://www.nature.com/articles/s41591-023-02233-x) | Nature Medicine 論文 |
| [TxGNN GitHub](https://github.com/mims-harvard/TxGNN) | ソースコード |

### 薬物データベース

| リソース | 説明 |
|----------|------|
| [DrugBank](https://go.drugbank.com/) | 包括的な薬物データベース |
| [KEGG DRUG](https://www.kegg.jp/kegg/drug/) | 医薬品データベース |
| [ChEMBL](https://www.ebi.ac.uk/chembl/) | 生物活性分子データベース |

### 日本の規制機関

| リソース | 説明 |
|----------|------|
| [PMDA](https://www.pmda.go.jp/) | 医薬品医療機器総合機構 |
| [厚生労働省](https://www.mhlw.go.jp/) | 医薬品行政 |
| [日本薬局方](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000066597.html) | 医薬品規格 |

### 臨床試験

| リソース | 説明 |
|----------|------|
| [jRCT](https://jrct.niph.go.jp/) | 日本臨床研究登録システム |
| [UMIN-CTR](https://www.umin.ac.jp/ctr/) | UMIN 臨床試験登録 |
| [ClinicalTrials.gov](https://clinicaltrials.gov/) | 国際臨床試験登録 |

---

## API アクセス

JpTxGNN は HL7 FHIR R4 準拠の API を提供しています：

- **ベース URL**: `https://jptxgnn.yao.care/fhir`
- **ドキュメント**: [FHIR API 仕様]({{ '/smart/api-spec/' | relative_url }})

---

## ライセンス

本プロジェクトのデータおよびコードは、学術研究目的で提供されています。詳細は [GitHub リポジトリ](https://github.com/yao-care/JpTxGNN) をご確認ください。
