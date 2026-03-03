---
layout: page
title: 健康ニュース
permalink: /news/
---

# 健康ニュースモニタリング

JpTxGNN は日本の健康関連ニュースを自動収集し、リポジショニング候補薬との関連を分析します。

<div id="news-container">
  <div id="news-stats">
    <p>読み込み中...</p>
  </div>
  <div id="news-list"></div>
</div>

## ニュースソース

| ソース | 説明 |
|--------|------|
| Google News Japan | 健康カテゴリ |
| Yahoo! Japan ニュース | 科学・ライフカテゴリ |

## キーワードマッチング

収集したニュースは以下のキーワードとマッチングされます：

- **薬物名**: 3,952 種類（英語・日本語）
- **適応症**: 544 種類（英語・日本語）

## 更新頻度

- ニュース収集: 毎日
- キーワードマッチング: 毎日

## 免責事項

- ニュースは自動収集されたものであり、内容の正確性を保証しません
- 医療判断の参考にしないでください
- 詳細は各ニュースソースの原文を参照してください

<script>
document.addEventListener('DOMContentLoaded', function() {
  const statsDiv = document.getElementById('news-stats');
  const listDiv = document.getElementById('news-list');

  fetch('/data/news-index.json')
    .then(response => response.json())
    .then(data => {
      // 統計表示
      statsDiv.innerHTML = `
        <p><strong>最終更新:</strong> ${new Date(data.generated).toLocaleString('ja-JP')}</p>
        <p><strong>マッチしたニュース:</strong> ${data.count} 件</p>
      `;

      // ニュース一覧
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
        listDiv.innerHTML = '<p>マッチしたニュースはありません。</p>';
      }
    })
    .catch(err => {
      statsDiv.innerHTML = '<p>ニュースデータの読み込みに失敗しました。</p>';
      console.error('Failed to load news index:', err);
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
