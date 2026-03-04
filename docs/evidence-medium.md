---
layout: default
title: 中エビデンスレベル
parent: 医薬品レポート
nav_order: 2
description: "L3-L4 レベルのドラッグリポジショニング候補薬。観察研究または前臨床エビデンスによる支持があり、さらなる研究探索の価値があります。"
permalink: /evidence-medium/
---

# 中エビデンスレベル薬物

<p style="font-size: 1.25rem; color: #666; margin-bottom: 1.5rem;">
追加エビデンス収集後にさらなる評価が可能な候補薬
</p>

---

## エビデンス基準

| レベル | 定義 | 臨床的意義 |
|--------|------|-----------|
| **L3** | 観察研究 / 大規模ケースシリーズ | 初期エビデンスあり、補完後に評価 |
| **L4** | 前臨床 / メカニズム研究 / 症例報告 | メカニズムは合理的、臨床検証が不足 |

---

## 薬物リスト

<div id="drug-stats">
  <p>読み込み中...</p>
</div>

<div id="drug-list"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const statsDiv = document.getElementById('drug-stats');
  const listDiv = document.getElementById('drug-list');

  fetch('/data/drugs.json')
    .then(response => response.json())
    .then(data => {
      // L3-L4 薬物をフィルタ
      const l3Drugs = data.drugs.filter(d => d.evidence_level === 'L3');
      const l4Drugs = data.drugs.filter(d => d.evidence_level === 'L4');

      statsDiv.innerHTML = `
        <p><strong>L3 レベル:</strong> ${l3Drugs.length} 件 | <strong>L4 レベル:</strong> ${l4Drugs.length} 件</p>
      `;

      let html = '';

      if (l3Drugs.length > 0) {
        html += '<h3>L3 レベル（' + l3Drugs.length + ' 件）</h3>';
        html += '<table><thead><tr><th>薬物名</th><th>予測適応症数</th><th>リンク</th></tr></thead><tbody>';
        l3Drugs.forEach(drug => {
          html += `<tr>
            <td><strong>${drug.name}</strong></td>
            <td>${drug.indication_count}</td>
            <td><a href="${drug.url}">レポートを見る</a></td>
          </tr>`;
        });
        html += '</tbody></table>';
      }

      if (l4Drugs.length > 0) {
        html += '<h3>L4 レベル（' + l4Drugs.length + ' 件）</h3>';
        html += '<table><thead><tr><th>薬物名</th><th>予測適応症数</th><th>リンク</th></tr></thead><tbody>';
        l4Drugs.forEach(drug => {
          html += `<tr>
            <td><strong>${drug.name}</strong></td>
            <td>${drug.indication_count}</td>
            <td><a href="${drug.url}">レポートを見る</a></td>
          </tr>`;
        });
        html += '</tbody></table>';
      }

      if (l3Drugs.length === 0 && l4Drugs.length === 0) {
        html = `<div style="background: #fff3cd; padding: 1rem; border-left: 4px solid #ffc107; border-radius: 4px;">
          <strong>データ準備中</strong><br>
          現在、中エビデンスレベル（L3-L4）の薬物はありません。エビデンス収集プロセスが完了次第、こちらに表示されます。<br><br>
          すべての薬物は現在 <a href="/evidence-low/">L5（モデル予測のみ）</a> として分類されています。
        </div>`;
      }

      listDiv.innerHTML = html;
    })
    .catch(err => {
      statsDiv.innerHTML = '';
      listDiv.innerHTML = '<p>データの読み込みに失敗しました。</p>';
    });
});
</script>

---

<div style="background: #d1ecf1; padding: 1rem; border-left: 4px solid #17a2b8; border-radius: 4px; margin: 1rem 0;">
<strong>注意：</strong>本サイトの情報は研究参考用であり、医療アドバイスを構成するものではありません。臨床決定については、必ず医療専門家にご相談ください。
</div>
