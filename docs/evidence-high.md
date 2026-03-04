---
layout: default
title: 高エビデンスレベル
parent: 医薬品レポート
nav_order: 1
description: "L1-L2 レベルのドラッグリポジショニング候補薬。複数の臨床試験またはシステマティックレビューによる支持があり、臨床評価への優先的移行が可能です。"
permalink: /evidence-high/
---

# 高エビデンスレベル薬物

<p style="font-size: 1.25rem; color: #666; margin-bottom: 1.5rem;">
臨床評価段階への優先的移行が可能な候補薬
</p>

---

## エビデンス基準

| レベル | 定義 | 臨床的意義 |
|--------|------|-----------|
| **L1** | 複数の Phase 3 RCT / システマティックレビュー | 強力な支持、臨床使用を検討可能 |
| **L2** | 単一の RCT または複数の Phase 2 試験 | 中等度の支持、検証試験の設計が可能 |

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
      // L1-L2 薬物をフィルタ
      const l1Drugs = data.drugs.filter(d => d.evidence_level === 'L1');
      const l2Drugs = data.drugs.filter(d => d.evidence_level === 'L2');

      statsDiv.innerHTML = `
        <p><strong>L1 レベル:</strong> ${l1Drugs.length} 件 | <strong>L2 レベル:</strong> ${l2Drugs.length} 件</p>
      `;

      let html = '';

      if (l1Drugs.length > 0) {
        html += '<h3>L1 レベル（' + l1Drugs.length + ' 件）</h3>';
        html += '<table><thead><tr><th>薬物名</th><th>予測適応症数</th><th>リンク</th></tr></thead><tbody>';
        l1Drugs.forEach(drug => {
          html += `<tr>
            <td><strong>${drug.name}</strong></td>
            <td>${drug.indication_count}</td>
            <td><a href="${drug.url}">レポートを見る</a></td>
          </tr>`;
        });
        html += '</tbody></table>';
      }

      if (l2Drugs.length > 0) {
        html += '<h3>L2 レベル（' + l2Drugs.length + ' 件）</h3>';
        html += '<table><thead><tr><th>薬物名</th><th>予測適応症数</th><th>リンク</th></tr></thead><tbody>';
        l2Drugs.forEach(drug => {
          html += `<tr>
            <td><strong>${drug.name}</strong></td>
            <td>${drug.indication_count}</td>
            <td><a href="${drug.url}">レポートを見る</a></td>
          </tr>`;
        });
        html += '</tbody></table>';
      }

      if (l1Drugs.length === 0 && l2Drugs.length === 0) {
        html = `<div style="background: #fff3cd; padding: 1rem; border-left: 4px solid #ffc107; border-radius: 4px;">
          <strong>データ準備中</strong><br>
          現在、高エビデンスレベル（L1-L2）の薬物はありません。エビデンス収集プロセスが完了次第、こちらに表示されます。<br><br>
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
