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

{% assign l3_drugs = site.drugs | where: "evidence_level", "L3" | sort: "title" %}
{% assign l4_drugs = site.drugs | where: "evidence_level", "L4" | sort: "title" %}

### L3 レベル ({{ l3_drugs.size }} 件)

| 薬物名 | 適応症数 | リンク |
|--------|----------|--------|
{% for drug in l3_drugs %}| **{{ drug.title }}** | {{ drug.indication_count }} | [レポートを見る]({{ drug.url | relative_url }}) |
{% endfor %}

### L4 レベル ({{ l4_drugs.size }} 件)

| 薬物名 | 適応症数 | リンク |
|--------|----------|--------|
{% for drug in l4_drugs %}| **{{ drug.title }}** | {{ drug.indication_count }} | [レポートを見る]({{ drug.url | relative_url }}) |
{% endfor %}

---

<div style="background: #d1ecf1; padding: 1rem; border-left: 4px solid #17a2b8; border-radius: 4px; margin: 1rem 0;">
<strong>注意：</strong>本サイトの情報は研究参考用であり、医療アドバイスを構成するものではありません。臨床決定については、必ず医療専門家にご相談ください。
</div>
