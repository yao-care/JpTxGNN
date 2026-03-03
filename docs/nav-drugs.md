---
layout: default
title: 医薬品レポート
nav_order: 4
has_children: true
description: "3,824 種の日本医療用医薬品のドラッグリポジショニング予測レポート"
permalink: /drugs/
---

# 医薬品レポート

<p class="key-answer" data-question="JpTxGNN の医薬品レポートとは？">
JpTxGNN は <strong>3,824</strong> 種の日本医療用医薬品に対するドラッグリポジショニング予測レポートを提供しています。各レポートには TxGNN モデルによる予測適応症とそのスコアが含まれています。
</p>

---

## 医薬品検索

<div class="drug-lookup-container">
  <div class="lookup-search-box">
    <div class="lookup-input-wrapper">
      <input type="text" id="lookup-input" placeholder="医薬品名を入力して検索..." autocomplete="off">
      <button id="lookup-clear" class="lookup-clear-btn" style="display: none;">✕</button>
    </div>
    <button id="lookup-search" class="lookup-search-btn">検索</button>
  </div>
  <div id="lookup-results" class="lookup-results"></div>
</div>

<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.0.0"></script>
<script>
  window.JPTXGNN_CONFIG = {
    searchIndexUrl: '{{ "/data/search-index.json" | relative_url }}',
    drugsBaseUrl: '{{ "/drugs/" | relative_url }}'
  };
</script>
<script src="{{ '/assets/js/drug-lookup.js' | relative_url }}"></script>

---

## 統計

<style>
.drug-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}
.drug-stat {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
}
.drug-stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
}
.drug-stat-label {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
}
</style>

<div class="drug-stats">
  <div class="drug-stat">
    <div class="drug-stat-number">3,824</div>
    <div class="drug-stat-label">対象医薬品</div>
  </div>
  <div class="drug-stat">
    <div class="drug-stat-number">142</div>
    <div class="drug-stat-label">DrugBank マッピング</div>
  </div>
  <div class="drug-stat">
    <div class="drug-stat-number">155,638</div>
    <div class="drug-stat-label">予測候補</div>
  </div>
</div>

---

## エビデンスレベル別

<style>
.drug-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}
.drug-card {
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
.drug-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.drug-card.high { border-color: #2E7D32; }
.drug-card.medium { border-color: #F9A825; }
.drug-card.low { border-color: #9E9E9E; }
.drug-card-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  flex-shrink: 0;
}
.drug-card.high .drug-card-icon { background: #E8F5E9; }
.drug-card.medium .drug-card-icon { background: #FFF8E1; }
.drug-card.low .drug-card-icon { background: #F5F5F5; }
.drug-card-count {
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1;
}
.drug-card.high .drug-card-count { color: #2E7D32; }
.drug-card.medium .drug-card-count { color: #F9A825; }
.drug-card.low .drug-card-count { color: #757575; }
.drug-card-info { flex: 1; }
.drug-card-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #333;
}
.drug-card-desc {
  font-size: 0.875rem;
  color: #666;
}
.drug-card-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: auto;
}
.drug-card.high .drug-card-badge { background: #E8F5E9; color: #2E7D32; }
.drug-card.medium .drug-card-badge { background: #FFF8E1; color: #F57F17; }
.drug-card.low .drug-card-badge { background: #F5F5F5; color: #757575; }
</style>

<div class="drug-cards">
  <a href="{{ '/evidence-high' | relative_url }}" class="drug-card high">
    <div class="drug-card-icon">
      <span class="drug-card-count">-</span>
    </div>
    <div class="drug-card-info">
      <div class="drug-card-title">高エビデンスレベル</div>
      <div class="drug-card-desc">臨床試験による支持あり</div>
    </div>
    <span class="drug-card-badge">L1-L2</span>
  </a>

  <a href="{{ '/evidence-medium' | relative_url }}" class="drug-card medium">
    <div class="drug-card-icon">
      <span class="drug-card-count">-</span>
    </div>
    <div class="drug-card-info">
      <div class="drug-card-title">中エビデンスレベル</div>
      <div class="drug-card-desc">文献エビデンスあり</div>
    </div>
    <span class="drug-card-badge">L3-L4</span>
  </a>

  <a href="{{ '/evidence-low' | relative_url }}" class="drug-card low">
    <div class="drug-card-icon">
      <span class="drug-card-count">142</span>
    </div>
    <div class="drug-card-info">
      <div class="drug-card-title">モデル予測のみ</div>
      <div class="drug-card-desc">AI 予測結果、研究方向の参考</div>
    </div>
    <span class="drug-card-badge">L5</span>
  </a>
</div>

---

## 予測スコアについて

TxGNN スコアは「医薬品-疾患」ペアに対するモデルの予測信頼度を表し、範囲は 0-1（0%-100%）です。

| 閾値 | 意味 | 推奨用途 |
|------|------|----------|
| ≥ 99% | 非常に高い信頼度 | 優先的に検証 |
| ≥ 90% | 高い信頼度 | 詳細調査推奨 |
| ≥ 50% | 中程度の信頼度 | 参考情報 |
| < 50% | 低い信頼度 | 追加検証必要 |

---

## データダウンロード

医薬品データをダウンロードできます：

<div style="display: flex; gap: 1rem; flex-wrap: wrap; margin: 1rem 0;">
  <a href="{{ '/data/search-index.json' | relative_url }}" style="display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 8px;">JSON 形式</a>
  <a href="{{ '/downloads/' | relative_url }}" style="display: inline-block; padding: 10px 20px; background: #f5f5f5; color: #333; text-decoration: none; border-radius: 8px; border: 1px solid #e0e0e0;">その他の形式</a>
</div>

---

## 免責事項

<div class="disclaimer">
これらの予測は研究目的のみであり、医療アドバイスを構成するものではありません。臨床応用には必ず適切な検証が必要です。
</div>
