---
layout: default
title: 薬物レポート
nav_order: 3
has_children: true
description: "124件のドラッグリポジショニング検証レポートを閲覧。L1-L5 エビデンスレベル別に分類。"
---

# 薬物レポート

<p style="font-size: 1.1rem; color: #666; margin-bottom: 1.5rem;">
エビデンスレベル別に <strong>124</strong> 件のドラッグリポジショニング検証レポートを閲覧
</p>

<style>
.drug-dist-container {
  margin: 2rem 0;
}
.drug-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
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

.drug-card-info {
  flex: 1;
}
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

<div class="drug-dist-container">
  <div class="drug-cards">
    <a href="{{ '/evidence-high' | relative_url }}" class="drug-card high">
      <div class="drug-card-icon">
        <span class="drug-card-count">-</span>
      </div>
      <div class="drug-card-info">
        <div class="drug-card-title">高エビデンスレベル</div>
        <div class="drug-card-desc">臨床試験による支持あり、優先評価可能</div>
      </div>
      <span class="drug-card-badge">L1-L2</span>
    </a>

    <a href="{{ '/evidence-medium' | relative_url }}" class="drug-card medium">
      <div class="drug-card-icon">
        <span class="drug-card-count">-</span>
      </div>
      <div class="drug-card-info">
        <div class="drug-card-title">中エビデンスレベル</div>
        <div class="drug-card-desc">文献エビデンスあり、追加研究が必要</div>
      </div>
      <span class="drug-card-badge">L3-L4</span>
    </a>

    <a href="{{ '/evidence-low' | relative_url }}" class="drug-card low">
      <div class="drug-card-icon">
        <span class="drug-card-count">124</span>
      </div>
      <div class="drug-card-info">
        <div class="drug-card-title">モデル予測のみ</div>
        <div class="drug-card-desc">AI 予測結果、研究方向の参考</div>
      </div>
      <span class="drug-card-badge">L5</span>
    </a>
  </div>
</div>

<p style="text-align: center; margin-top: 2rem;">
  <a href="{{ '/drugs/' | relative_url }}" style="display: inline-block; padding: 0.75rem 2rem; background: #2E7D32; color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">完全な薬物リストを表示</a>
</p>
