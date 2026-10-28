---
layout: default
title: "既知の用途のみ（新規予測なし）"
nav_order: 24
permalink: /known-uses/
description: "これらの薬剤では、TxGNN モデルの候補はすべて既知の用途（知識グラフまたは承認情報に記録済み）であり、新たな予測適応症はありません。各ページに既知の用途と国内の販売状況を掲載しています。"
---

# 既知の用途のみ（新規予測なし）

これらの薬剤では、TxGNN モデルの候補はすべて既知の用途（知識グラフまたは承認情報に記録済み）であり、新たな予測適応症はありません。各ページに既知の用途と国内の販売状況を掲載しています。

{% assign known_drugs = site.drugs | where: "evidence_level", "N/A" | sort: "title" %}

**{{ known_drugs.size }} 剤**

| 薬剤 | レポート |
|------|------|
{% for drug in known_drugs %}| **{{ drug.title }}** | [表示]({{ drug.url | relative_url }}) |
{% endfor %}
