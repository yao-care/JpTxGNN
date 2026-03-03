---
layout: default
title: 安全性データ
nav_order: 5
has_children: true
description: "薬物相互作用データベース：DDI、DDSI、DFI、DHI"
permalink: /safety/
---

# 安全性データ

<p style="font-size: 1.1rem; color: #666; margin-bottom: 1.5rem;">
ドラッグリポジショニング候補の安全性評価に必要な <strong>4 種類の相互作用データ</strong> を提供予定
</p>

---

## 概要

ドラッグリポジショニングを検討する際、既存の安全性情報は重要な考慮事項です。JpTxGNN では以下の相互作用データを統合予定です：

<style>
.safety-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}
.safety-card {
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
.safety-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.safety-card.ddi { border-color: #1565C0; }
.safety-card.ddsi { border-color: #7B1FA2; }
.safety-card.dfi { border-color: #388E3C; }
.safety-card.dhi { border-color: #E65100; }

.safety-card-icon {
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
.safety-card.ddi .safety-card-icon { background: #E3F2FD; }
.safety-card.ddsi .safety-card-icon { background: #F3E5F5; }
.safety-card.dfi .safety-card-icon { background: #E8F5E9; }
.safety-card.dhi .safety-card-icon { background: #FFF3E0; }

.safety-card-info {
  flex: 1;
}
.safety-card-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #333;
}
.safety-card-desc {
  font-size: 0.8rem;
  color: #666;
}
.safety-card-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
  margin-left: auto;
  white-space: nowrap;
}
.safety-card.ddi .safety-card-badge { background: #E3F2FD; color: #1565C0; }
.safety-card.ddsi .safety-card-badge { background: #F3E5F5; color: #7B1FA2; }
.safety-card.dfi .safety-card-badge { background: #E8F5E9; color: #388E3C; }
.safety-card.dhi .safety-card-badge { background: #FFF3E0; color: #E65100; }
</style>

<div class="safety-cards">
  <a href="{{ '/ddi/' | relative_url }}" class="safety-card ddi">
    <div class="safety-card-icon">💊</div>
    <div class="safety-card-info">
      <div class="safety-card-title">薬物-薬物相互作用</div>
      <div class="safety-card-desc">併用薬のリスク評価</div>
    </div>
    <span class="safety-card-badge">DDI</span>
  </a>

  <a href="{{ '/ddsi/' | relative_url }}" class="safety-card ddsi">
    <div class="safety-card-icon">🏥</div>
    <div class="safety-card-info">
      <div class="safety-card-title">薬物-疾患注意事項</div>
      <div class="safety-card-desc">禁忌症情報</div>
    </div>
    <span class="safety-card-badge">DDSI</span>
  </a>

  <a href="{{ '/dfi/' | relative_url }}" class="safety-card dfi">
    <div class="safety-card-icon">🍎</div>
    <div class="safety-card-info">
      <div class="safety-card-title">薬物-食物相互作用</div>
      <div class="safety-card-desc">食事との相互作用</div>
    </div>
    <span class="safety-card-badge">DFI</span>
  </a>

  <a href="{{ '/dhi/' | relative_url }}" class="safety-card dhi">
    <div class="safety-card-icon">🌿</div>
    <div class="safety-card-info">
      <div class="safety-card-title">薬物-ハーブ相互作用</div>
      <div class="safety-card-desc">漢方・サプリとの相互作用</div>
    </div>
    <span class="safety-card-badge">DHI</span>
  </a>
</div>

---

## 現在のステータス

<div style="background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 16px; margin: 20px 0;">
<strong>開発中</strong><br>
安全性データの統合は現在開発中です。今後、DDInter 2.0 などのデータソースから相互作用情報を統合予定です。
</div>

---

## データソース（予定）

| 種類 | データソース | 説明 |
|------|-------------|------|
| DDI | DDInter 2.0 | 薬物-薬物相互作用 |
| DDSI | DDInter 2.0 | 薬物-疾患禁忌 |
| DFI | DDInter 2.0 | 薬物-食物相互作用 |
| DHI | 文献調査 | 薬物-ハーブ相互作用 |

---

## 注意事項

<div style="background: #ffebee; padding: 1rem; border-left: 4px solid #f44336; border-radius: 4px; margin: 1rem 0;">
<strong>重要：</strong>ドラッグリポジショニング候補を評価する際は、必ず既存の適応症における安全性プロファイルを確認してください。新しい適応症での使用には、追加の安全性評価が必要となる場合があります。
</div>

---

## 関連リンク

- [PMDA 医薬品安全性情報](https://www.pmda.go.jp/safety/info-services/drugs/0001.html)
- [DDInter 2.0](https://ddinter2.scbdd.com/)
- [DrugBank](https://go.drugbank.com/)
