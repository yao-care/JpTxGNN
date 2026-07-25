---
layout: default
title: 全医薬品一覧
nav_order: 20
permalink: /drugs/
description: "JpTxGNN における全医薬品の検証レポートとエビデンスレベル統計。"
---
{% assign l1_count = site.drugs | where: "evidence_level", "L1" | size %}
{% assign l2_count = site.drugs | where: "evidence_level", "L2" | size %}
{% assign l3_count = site.drugs | where: "evidence_level", "L3" | size %}
{% assign l4_count = site.drugs | where: "evidence_level", "L4" | size %}
{% assign l5_count = site.drugs | where: "evidence_level", "L5" | size %}

# 全医薬品一覧

{{ site.drugs.size }} 件の医薬品検証レポート

---

## エビデンスレベル別内訳

| エビデンスレベル | 医薬品数 | 説明 |
|---------|--------|------|
| **L1** | {{ l1_count }} | 複数の RCT／システマティックレビュー |
| **L2** | {{ l2_count }} | 単一の RCT／第 2 相試験 |
| **L3** | {{ l3_count }} | 観察研究／大規模症例集積 |
| **L4** | {{ l4_count }} | 前臨床研究／メカニズム研究 |
| **L5** | {{ l5_count }} | モデル予測のみ |

---

## 医薬品全リスト

{% assign all_drugs = site.drugs | sort: 'title' %}

| 医薬品 | エビデンスレベル | 適応症数 |
|---------|---------|---------|
{% for drug in all_drugs %}| [{{ drug.title }}]({{ drug.url | relative_url }}) | {{ drug.evidence_level }} | {{ drug.indication_count }} |
{% endfor %}

---

<div class="disclaimer">
<strong>免責事項</strong><br>
本レポートは学術研究の参考のみを目的としており、<strong>医療アドバイスを構成するものではありません</strong>。必ず医師の指示に従ってください。自己判断で薬剤を調整しないでください。ドラッグリポジショニングに関するいかなる決定にも、完全な臨床検証と規制当局の審査が必要です。
<br><br>
<small>審査者：藥提醒科技有限公司 (yao.care)</small>
</div>
