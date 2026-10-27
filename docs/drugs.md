---
layout: default
title: 全医薬品一覧
nav_order: 20
permalink: /drugs/
description: "JpTxGNN における全医薬品の検証レポートとエビデンスレベル統計。"
---
{%- comment -%}2026-10-27 build gate：站上各頁的藥物數讀 site.data.drug_stats；它和實際公開藥物頁數／等級分布不一致時，
故意 include 不存在的檔讓 Jekyll 建置失敗，錯誤訊息即修法。{%- endcomment -%}
{%- assign gate_listed = site.drugs | where_exp: "d", "d.layout != 'id_redirect'" | where_exp: "d", "d.noindex != true" -%}
{%- assign gate_ds = site.data.drug_stats -%}
{%- assign gate_l1 = gate_listed | where: "evidence_level", "L1" | size -%}
{%- assign gate_l2 = gate_listed | where: "evidence_level", "L2" | size -%}
{%- assign gate_l3 = gate_listed | where: "evidence_level", "L3" | size -%}
{%- assign gate_l4 = gate_listed | where: "evidence_level", "L4" | size -%}
{%- assign gate_l5 = gate_listed | where: "evidence_level", "L5" | size -%}
{%- if gate_listed.size != gate_ds.total_drugs or gate_l1 != gate_ds.level_counts.L1 or gate_l2 != gate_ds.level_counts.L2 or gate_l3 != gate_ds.level_counts.L3 or gate_l4 != gate_ds.level_counts.L4 or gate_l5 != gate_ds.level_counts.L5 -%}
{% include ERROR-docs-data-drug_stats-json-out-of-sync--run-python3-scripts-generate_drug_stats-py.html %}
{%- endif %}
{%- comment -%}2026-10-16：列表不含舊 ID 轉址頁與 noindex 頁{%- endcomment -%}
{% assign listed_drugs = site.drugs | where_exp: "d", "d.layout != 'id_redirect'" | where_exp: "d", "d.noindex != true" %}
{% assign l1_count = listed_drugs | where: "evidence_level", "L1" | size %}
{% assign l2_count = listed_drugs | where: "evidence_level", "L2" | size %}
{% assign l3_count = listed_drugs | where: "evidence_level", "L3" | size %}
{% assign l4_count = listed_drugs | where: "evidence_level", "L4" | size %}
{% assign l5_count = listed_drugs | where: "evidence_level", "L5" | size %}

# 全医薬品一覧

{{ listed_drugs.size }} 件の医薬品検証レポート

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

{% assign all_drugs = listed_drugs | sort: 'title' %}

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
