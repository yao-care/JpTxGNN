---
layout: default
title: 藥物總覽
nav_order: 5
---

# 藥物總覽
{: .fs-9 }

共 191 個藥物的驗證報告
{: .fs-6 .fw-300 }

---

## 統計摘要

| 證據等級 | 藥物數 | 說明 |
|---------|--------|------|
| **L1** | 6 | 多個 RCT / 系統性回顧 |
| **L2** | 12 | 單一 RCT / Phase 2 試驗 |
| **L3** | 16 | 觀察性研究 / 大型病例系列 |
| **L4** | 19 | 前臨床 / 機轉研究 |
| **L5** | 138 | 僅模型預測 |

---

## 完整藥物列表

{% assign all_drugs = site.drugs | sort: 'title' %}

| 藥物名稱 | 證據等級 | 適應症數 |
|---------|---------|---------|
{% for drug in all_drugs %}| [{{ drug.title }}]({{ drug.url | relative_url }}) | {{ drug.evidence_level }} | {{ drug.indication_count }} |
{% endfor %}
