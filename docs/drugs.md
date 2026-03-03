---
layout: page
title: 医薬品検索
permalink: /drugs/
---

# 医薬品リポジショニング候補検索

<div id="search-container">
  <input type="text" id="drug-search" placeholder="医薬品名または成分名を入力..." class="search-input">
  <div id="search-results"></div>
</div>

## 統計サマリー

| 指標 | 数値 |
|------|------|
| リポジショニング候補総数 | 37,686 |
| 対象医薬品数 | 3,952 |
| 潜在的新適応症数 | 482 |

## 予測について

予測は TxGNN 知識グラフに基づいています。各候補には以下の情報が含まれます：

- **医薬品名**: 日本での販売名
- **DrugBank ID**: 国際標準識別子
- **潜在的新適応症**: TxGNN で予測された疾病

## エビデンスレベル

| レベル | 説明 |
|--------|------|
| L1 | 承認済み適応症 |
| L2 | 臨床試験で検証済み |
| L3 | 症例報告あり |
| L4 | In vitro/動物実験 |
| L5 | 計算予測のみ |

**注意**: 本システムの予測はすべて L5（計算予測のみ）です。

## 免責事項

これらの予測は研究目的のみであり、医療アドバイスを構成するものではありません。臨床応用には必ず適切な検証が必要です。

<script>
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('drug-search');
  const resultsDiv = document.getElementById('search-results');
  let searchIndex = null;

  // Load search index
  fetch('/data/search-index.json')
    .then(response => response.json())
    .then(data => {
      searchIndex = data;
      console.log('Loaded', data.drugs.length, 'drugs');
    })
    .catch(err => console.error('Failed to load search index:', err));

  searchInput.addEventListener('input', function() {
    const query = this.value.toLowerCase().trim();
    if (!searchIndex || query.length < 2) {
      resultsDiv.innerHTML = '';
      return;
    }

    const results = searchIndex.drugs.filter(drug =>
      drug.name.toLowerCase().includes(query) ||
      drug.slug.includes(query)
    ).slice(0, 20);

    if (results.length === 0) {
      resultsDiv.innerHTML = '<p>該当する医薬品が見つかりません</p>';
      return;
    }

    let html = '<ul class="drug-list">';
    results.forEach(drug => {
      html += `<li>
        <strong>${drug.name}</strong>
        ${drug.drugbank_id ? `<span class="drugbank-id">${drug.drugbank_id}</span>` : ''}
        <br>
        <small>潜在的新適応症: ${drug.indications.length}件</small>
      </li>`;
    });
    html += '</ul>';
    resultsDiv.innerHTML = html;
  });
});
</script>

<style>
.search-input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 20px;
}
.drug-list {
  list-style: none;
  padding: 0;
}
.drug-list li {
  padding: 10px;
  border-bottom: 1px solid #eee;
}
.drug-list li:hover {
  background: #f9f9f9;
}
.drugbank-id {
  background: #e3f2fd;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
  margin-left: 8px;
}
</style>
