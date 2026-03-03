---
layout: default
title: 健康ニュース
nav_order: 3
description: "ドラッグリポジショニングに関連する最新の健康・医療ニュース"
permalink: /news/
---

# 健康ニュース

<p class="key-answer" data-question="JpTxGNN の健康ニュースとは？">
JpTxGNN データベースの医薬品と疾患に関連する最新の健康・医療ニュースを監視しています。ドラッグリポジショニング研究に関連する新しい発見や臨床試験の結果をお届けします。
</p>

---

## ニュースソース

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0;">
  <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px; text-align: center;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📰</div>
    <strong>医療ニュース</strong>
    <p style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">国内外の医療・健康ニュース</p>
  </div>
  <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px; text-align: center;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔬</div>
    <strong>研究成果</strong>
    <p style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">最新の研究論文と発見</p>
  </div>
  <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px; text-align: center;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">💊</div>
    <strong>臨床試験</strong>
    <p style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">進行中の臨床試験情報</p>
  </div>
  <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px; text-align: center;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏥</div>
    <strong>規制情報</strong>
    <p style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">PMDA・厚労省の発表</p>
  </div>
</div>

---

## 最新ニュース

<div id="news-container">
  <div id="news-stats">
    <p>読み込み中...</p>
  </div>
  <div id="news-list"></div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const statsDiv = document.getElementById('news-stats');
  const listDiv = document.getElementById('news-list');

  fetch('/data/news-index.json')
    .then(response => response.json())
    .then(data => {
      statsDiv.innerHTML = `
        <p><strong>最終更新:</strong> ${new Date(data.generated).toLocaleString('ja-JP')}</p>
        <p><strong>マッチしたニュース:</strong> ${data.count} 件</p>
      `;

      if (data.news && data.news.length > 0) {
        let html = '<ul class="news-list">';
        data.news.slice(0, 20).forEach(item => {
          const date = new Date(item.published).toLocaleDateString('ja-JP');
          const source = item.sources[0] || {};
          const keywords = item.keywords.map(k =>
            `<span class="keyword-tag ${k.type}">${k.keyword}</span>`
          ).join(' ');

          html += `
            <li class="news-item">
              <a href="${source.link}" target="_blank" rel="noopener">${item.title}</a>
              <div class="news-meta">
                <span class="news-date">${date}</span>
                <span class="news-source">${source.name || 'Unknown'}</span>
                ${keywords}
              </div>
            </li>
          `;
        });
        html += '</ul>';

        if (data.news.length > 20) {
          html += `<p><em>他 ${data.news.length - 20} 件のニュースがあります</em></p>`;
        }

        listDiv.innerHTML = html;
      } else {
        listDiv.innerHTML = '<div style="background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 16px;"><strong>準備中</strong><br>健康ニュースの自動収集システムは現在開発中です。</div>';
      }
    })
    .catch(err => {
      statsDiv.innerHTML = '';
      listDiv.innerHTML = '<div style="background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 16px;"><strong>準備中</strong><br>健康ニュースの自動収集システムは現在開発中です。</div>';
    });
});
</script>

<style>
.news-list {
  list-style: none;
  padding: 0;
}
.news-item {
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}
.news-item a {
  font-size: 1.1em;
  text-decoration: none;
}
.news-item a:hover {
  text-decoration: underline;
}
.news-meta {
  margin-top: 4px;
  font-size: 0.9em;
  color: #666;
}
.news-date {
  margin-right: 8px;
}
.news-source {
  margin-right: 8px;
  color: #888;
}
.keyword-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  margin-left: 4px;
}
.keyword-tag.drug {
  background: #e3f2fd;
  color: #1565c0;
}
.keyword-tag.indication {
  background: #fff3e0;
  color: #e65100;
}
</style>

---

## 関連キーワード

本サイトでは以下のキーワードに関連するニュースを監視予定です：

### 医薬品カテゴリ

- 抗がん剤
- 免疫抑制剤
- 循環器用薬
- 消化器用薬
- 神経系用薬

### 疾患カテゴリ

- 希少疾患
- 自己免疫疾患
- 感染症
- 代謝疾患
- 神経変性疾患

---

## ニュース通知

最新のニュースを受け取るには：

<div style="display: flex; gap: 1rem; flex-wrap: wrap; margin: 1rem 0;">
  <a href="{{ '/feed.xml' | relative_url }}" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 10px 20px; background: #FF6600; color: white; text-decoration: none; border-radius: 8px;">
    RSS フィード
  </a>
  <a href="https://github.com/yao-care/JpTxGNN" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 10px 20px; background: #333; color: white; text-decoration: none; border-radius: 8px;">
    GitHub で Watch
  </a>
</div>

---

## 免責事項

<div class="disclaimer">
<strong>重要なお知らせ</strong><br>
本ページのニュース情報は参考目的のみで提供されており、医療アドバイスを構成するものではありません。健康上の問題については、必ず医療専門家にご相談ください。
</div>
