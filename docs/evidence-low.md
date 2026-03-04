---
layout: default
title: モデル予測のみ
parent: 医薬品レポート
nav_order: 3
description: "L5 レベルのドラッグリポジショニング候補薬。現在 AI モデル予測のみで臨床エビデンスがなく、研究方向の参考として使用できます。"
permalink: /evidence-low/
---

# モデル予測のみの薬物

<p style="font-size: 1.25rem; color: #666; margin-bottom: 1.5rem;">
TxGNN モデルによる予測はあるが、臨床エビデンスの支持がない候補薬
</p>

---

## エビデンス基準

| レベル | 定義 | 臨床的意義 |
|--------|------|-----------|
| **L5** | モデル予測のみ、臨床エビデンスなし | 研究仮説として使用可能、さらなる検証が必要 |

<div style="background: #fff3cd; padding: 1rem; border-left: 4px solid #ffc107; border-radius: 4px; margin: 1rem 0;">
<strong>注意：</strong>L5 レベルの薬物は知識グラフ予測のみに基づいており、直接的な臨床エビデンスの支持がありません。臨床決定に直接使用することは推奨されず、研究方向の参考としてご利用ください。
</div>

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
      // L5 薬物をフィルタ
      const l5Drugs = data.drugs.filter(d => d.evidence_level === 'L5');

      statsDiv.innerHTML = `
        <p><strong>L5 レベル薬物数:</strong> ${l5Drugs.length} 件</p>
      `;

      if (l5Drugs.length > 0) {
        let html = '<table><thead><tr><th>薬物名</th><th>予測適応症数</th><th>リンク</th></tr></thead><tbody>';
        l5Drugs.forEach(drug => {
          html += `<tr>
            <td><strong>${drug.name}</strong></td>
            <td>${drug.indication_count}</td>
            <td><a href="${drug.url}">レポートを見る</a></td>
          </tr>`;
        });
        html += '</tbody></table>';
        listDiv.innerHTML = html;
      } else {
        listDiv.innerHTML = '<p>L5 レベルの薬物データはありません。</p>';
      }
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
