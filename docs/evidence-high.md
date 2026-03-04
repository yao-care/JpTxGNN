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

{% assign l1_drugs = site.drugs | where: "evidence_level", "L1" | sort: "title" %}
{% assign l2_drugs = site.drugs | where: "evidence_level", "L2" | sort: "title" %}

### L1 レベル ({{ l1_drugs.size }} 件)

| 薬物名 | 適応症数 | リンク |
|--------|----------|--------|
{% for drug in l1_drugs %}| **{{ drug.title }}** | {{ drug.indication_count }} | [レポートを見る]({{ drug.url | relative_url }}) |
{% endfor %}

### L2 レベル ({{ l2_drugs.size }} 件)

| 薬物名 | 適応症数 | リンク |
|--------|----------|--------|
{% for drug in l2_drugs %}| **{{ drug.title }}** | {{ drug.indication_count }} | [レポートを見る]({{ drug.url | relative_url }}) |
{% endfor %}

---

<div style="background: #d1ecf1; padding: 1rem; border-left: 4px solid #17a2b8; border-radius: 4px; margin: 1rem 0;">
<strong>注意：</strong>本サイトの情報は研究参考用であり、医療アドバイスを構成するものではありません。臨床決定については、必ず医療専門家にご相談ください。
</div>
