---
layout: default
title: モデル予測のみ
parent: 医薬品レポート
nav_order: 3
description: "本サイト（日本）のエビデンスレベル L5 の 255 品目（例：Loxoprofen, Epinastine, Fexofenadine）。各品目の主な予測新適応症、医薬品コード（薬価基準収載品目）の件数、確認記録を掲載。"
permalink: /evidence-low/
---

# モデル予測のみの薬物

<!-- tier-facts:start（母目錄 .claude/gen_local_pages_20261119.py 產生，勿手改）-->
{% assign ev_share = site.data.evidence_tier_facts.low.count | times: 100.0 | divided_by: site.data.drug_stats.total_drugs %}
このページには、本サイトでレポートを公開している **{{ site.data.drug_stats.total_drugs }}** 品目のうち **{{ site.data.evidence_tier_facts.low.count }}** 品目（{{ site.data.evidence_tier_facts.low.count | times: 100.0 | divided_by: site.data.drug_stats.total_drugs | round: 1 }}%）を掲載しています：L5 **{{ site.data.evidence_tier_facts.low.by_level.L5 }}**。
30 の TxGNN サイトにおける L5 の割合の中央値：{{ site.data.evidence_tier_facts.low.cross.median_share }}%。 {% if ev_share > site.data.evidence_tier_facts.low.cross.median_share %}本サイトは中央値を上回っています。{% elsif ev_share < site.data.evidence_tier_facts.low.cross.median_share %}本サイトは中央値を下回っています。{% else %}本サイトは中央値と同じです。{% endif %}

{% if site.data.evidence_tier_facts.low.count > 0 %}
国内データ（医薬品コード（薬価基準収載品目））では、これらのうち **{{ site.data.evidence_tier_facts.low.with_current }}** 品目に収載中のコードが 1 件以上あり、**{{ site.data.evidence_tier_facts.low.none_current }}** 品目はコードがあるもののすべて収載中ではなく、**{{ site.data.evidence_tier_facts.low.without_data }}** 品目は国内データにありません。 **{{ site.data.evidence_tier_facts.low.with_reviews }}** 品目は確認記録に記載があります（医薬品ページ上の承認・収載情報の訂正）。 **{{ site.data.evidence_tier_facts.low.cross.unique_drugs }}** 品目には、同じ医薬品について他の TxGNN サイトにない予測適応症があります。
{% if site.data.evidence_tier_facts.low.none_current_list.size > 0 %}

コードはあるが収載中のものがない品目：{% for r in site.data.evidence_tier_facts.low.none_current_list %}[{{ r.t }}]({{ r.u | relative_url }}){% unless forloop.last %}、{% endunless %}{% endfor %}。{% endif %}

収載中のコードがある品目を先に並べています。
{% endif %}

全レベルの定義：[方法論]({{ '/methodology/' | relative_url }})。
<!-- tier-facts:end -->

<p style="font-size: 1.25rem; color: #666; margin-bottom: 1.5rem;">
TxGNN モデルによる予測はあるが、臨床エビデンスの支持がない候補薬
</p>

---

## エビデンス基準

| レベル | 定義 | 臨床的意義 |
|--------|------|-----------|
| **L5** | モデル予測のみ、臨床エビデンスなし | 研究仮説として使用可能、さらなる検証が必要 |

<div style="background: #fff3cd; padding: 1rem; border-left: 4px solid #ffc107; border-radius: 4px; margin: 1rem 0;">
<strong>注意：</strong>L5 レベルの薬物はモデル予測のみで、直接的な臨床エビデンスの支持がありません。臨床決定に直接使用することは推奨されず、研究方向の参考としてご利用ください。
</div>

---

## 薬物リスト

{% assign l5_drugs = site.drugs | where: "evidence_level", "L5" | where_exp: "d", "d.noindex != true" | sort: "title" %}

### L5 レベル ({{ site.data.evidence_tier_facts.low.by_level.L5 }} 件)

<!-- tier-table:start L5（母目錄 .claude/gen_local_pages_20261119.py 產生，勿手改）-->

| 医薬品 | レベル | 主な予測新適応症 | 医薬品コード（薬価基準収載品目）：収載中／全件 | 確認記録 | 本サイトのみ |
|---|---|---|---|---|---|
{% for r in site.data.evidence_tier_facts.low.rows %}{% if r.l == "L5" %}| [{{ r.t | replace: '|', '/' }}]({{ r.u | relative_url }}) | {{ r.l }} | {{ r.i | replace: '|', '/' }} | {% if r.lt %}{{ r.lv }} / {{ r.lt }}{% else %}—{% endif %} | {{ r.r }}{% if r.rs and r.rs != '' %}: {{ r.rs | replace: '|', '/' }}{% endif %} | {% if r.x and r.x > 0 %}あり ({{ r.x }}){% else %}—{% endif %} |
{% endif %}{% endfor %}

<!-- tier-table:end -->

---

<div style="background: #d1ecf1; padding: 1rem; border-left: 4px solid #17a2b8; border-radius: 4px; margin: 1rem 0;">
<strong>注意：</strong>本サイトの情報は研究参考用であり、医療アドバイスを構成するものではありません。臨床決定については、必ず医療専門家にご相談ください。
</div>
