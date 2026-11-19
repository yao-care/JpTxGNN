---
layout: default
title: 高エビデンスレベル
parent: 医薬品レポート
nav_order: 1
description: "本サイト（日本）のエビデンスレベル L1–L2 の 17 品目（例：Doxorubicin, Tacrolimus, Atorvastatin）。各品目の主な予測新適応症、医薬品コード（薬価基準収載品目）の件数、確認記録を掲載。"
permalink: /evidence-high/
---

# 高エビデンスレベル薬物

<!-- tier-facts:start（母目錄 .claude/gen_local_pages_20261119.py 產生，勿手改）-->
{% assign ev_share = site.data.evidence_tier_facts.high.count | times: 100.0 | divided_by: site.data.drug_stats.total_drugs %}
このページには、本サイトでレポートを公開している **{{ site.data.drug_stats.total_drugs }}** 品目のうち **{{ site.data.evidence_tier_facts.high.count }}** 品目（{{ site.data.evidence_tier_facts.high.count | times: 100.0 | divided_by: site.data.drug_stats.total_drugs | round: 1 }}%）を掲載しています：L1 **{{ site.data.evidence_tier_facts.high.by_level.L1 }}**、L2 **{{ site.data.evidence_tier_facts.high.by_level.L2 }}**。
30 の TxGNN サイトにおける L1–L2 の割合の中央値：{{ site.data.evidence_tier_facts.high.cross.median_share }}%。 {% if ev_share > site.data.evidence_tier_facts.high.cross.median_share %}本サイトは中央値を上回っています。{% elsif ev_share < site.data.evidence_tier_facts.high.cross.median_share %}本サイトは中央値を下回っています。{% else %}本サイトは中央値と同じです。{% endif %}

{% if site.data.evidence_tier_facts.high.count > 0 %}
国内データ（医薬品コード（薬価基準収載品目））では、これらのうち **{{ site.data.evidence_tier_facts.high.with_current }}** 品目に収載中のコードが 1 件以上あり、**{{ site.data.evidence_tier_facts.high.none_current }}** 品目はコードがあるもののすべて収載中ではなく、**{{ site.data.evidence_tier_facts.high.without_data }}** 品目は国内データにありません。 **{{ site.data.evidence_tier_facts.high.with_reviews }}** 品目は確認記録に記載があります（医薬品ページ上の承認・収載情報の訂正）。 **{{ site.data.evidence_tier_facts.high.cross.unique_drugs }}** 品目には、同じ医薬品について他の TxGNN サイトにない予測適応症があります。
{% if site.data.evidence_tier_facts.high.none_current_list.size > 0 %}

コードはあるが収載中のものがない品目：{% for r in site.data.evidence_tier_facts.high.none_current_list %}[{{ r.t }}]({{ r.u | relative_url }}){% unless forloop.last %}、{% endunless %}{% endfor %}。{% endif %}
{% endif %}

全レベルの定義：[方法論]({{ '/methodology/' | relative_url }})。
<!-- tier-facts:end -->

<p style="font-size: 1.25rem; color: #666; margin-bottom: 1.5rem;">
臨床評価段階への優先的移行が可能な候補薬
</p>

これらの医薬品のうち、予測新規適応症に試験エビデンスがあるのはどれか、登録試験はいくつ引用されているか――[新規適応症に臨床試験エビデンスがある国内医薬品]({{ '/clinical-trial-evidence/' | relative_url }})をご覧ください。

---

## エビデンス基準

| レベル | 定義 | 臨床的意義 |
|--------|------|-----------|
| **L1** | 複数の Phase 3 RCT / システマティックレビュー | 強力な支持、臨床使用を検討可能 |
| **L2** | 単一の RCT または複数の Phase 2 試験 | 中等度の支持、検証試験の設計が可能 |

---

## 薬物リスト

{% assign l1_drugs = site.drugs | where: "evidence_level", "L1" | where_exp: "d", "d.noindex != true" | sort: "title" %}
{% assign l2_drugs = site.drugs | where: "evidence_level", "L2" | where_exp: "d", "d.noindex != true" | sort: "title" %}

### L1 レベル ({{ site.data.evidence_tier_facts.high.by_level.L1 }} 件)

<!-- tier-table:start L1（母目錄 .claude/gen_local_pages_20261119.py 產生，勿手改）-->

| 医薬品 | レベル | 主な予測新適応症 | 医薬品コード（薬価基準収載品目）：収載中／全件 | 確認記録 | 本サイトのみ |
|---|---|---|---|---|---|
{% for r in site.data.evidence_tier_facts.high.rows %}{% if r.l == "L1" %}| [{{ r.t | replace: '|', '/' }}]({{ r.u | relative_url }}) | {{ r.l }} | {{ r.i | replace: '|', '/' }} | {% if r.lt %}{{ r.lv }} / {{ r.lt }}{% else %}—{% endif %} | {{ r.r }}{% if r.rs and r.rs != '' %}: {{ r.rs | replace: '|', '/' }}{% endif %} | {% if r.x and r.x > 0 %}あり ({{ r.x }}){% else %}—{% endif %} |
{% endif %}{% endfor %}

<!-- tier-table:end -->

### L2 レベル ({{ site.data.evidence_tier_facts.high.by_level.L2 }} 件)

<!-- tier-table:start L2（母目錄 .claude/gen_local_pages_20261119.py 產生，勿手改）-->

| 医薬品 | レベル | 主な予測新適応症 | 医薬品コード（薬価基準収載品目）：収載中／全件 | 確認記録 | 本サイトのみ |
|---|---|---|---|---|---|
{% for r in site.data.evidence_tier_facts.high.rows %}{% if r.l == "L2" %}| [{{ r.t | replace: '|', '/' }}]({{ r.u | relative_url }}) | {{ r.l }} | {{ r.i | replace: '|', '/' }} | {% if r.lt %}{{ r.lv }} / {{ r.lt }}{% else %}—{% endif %} | {{ r.r }}{% if r.rs and r.rs != '' %}: {{ r.rs | replace: '|', '/' }}{% endif %} | {% if r.x and r.x > 0 %}あり ({{ r.x }}){% else %}—{% endif %} |
{% endif %}{% endfor %}

<!-- tier-table:end -->

---

<div style="background: #d1ecf1; padding: 1rem; border-left: 4px solid #17a2b8; border-radius: 4px; margin: 1rem 0;">
<strong>注意：</strong>本サイトの情報は研究参考用であり、医療アドバイスを構成するものではありません。臨床決定については、必ず医療専門家にご相談ください。
</div>
