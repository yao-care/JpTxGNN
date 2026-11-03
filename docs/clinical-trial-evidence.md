---
layout: default
title: "新規適応症に臨床試験エビデンスがある医薬品"
parent: 医薬品レポート
nav_order: 4
permalink: /clinical-trial-evidence/
description: "PMDA 承認情報の医薬品のうち、TxGNN が予測した新規適応症に臨床試験エビデンス（L1–L2）があるもの：予測適応症、エビデンスレベル、登録試験数。"
last_modified_at: 2026-11-03
---
{%- comment -%}
2026-11-03：回答 AI 搜尋常問的「本國藥物中，哪些新適應症有臨床試驗證據」。全表由 Liquid 從藥物頁產生，不寫死藥名或數字。
收錄＝公開藥物頁（排除 id_redirect 與 noindex）中 evidence_level 為 L1 或 L2（本站 evidence-high 標準：L1 多個 Phase 3 RCT／系統性回顧，
L2 單一 RCT 或多個 Phase 2 試驗）。預測新適應症與等級註記取自各藥物頁快速總覽表；下列欄名是本站藥物頁實際用到的寫法（建頁時逐頁核對），
新寫法抓不到時顯示「レポート参照」、等級仍取 front matter。試驗數＝該藥物頁引用的不重複 NCT 編號數。
{%- endcomment -%}
{%- assign ind_labels = "予測新規適応症" | split: "|" -%}
{%- assign lev_labels = "エビデンスレベル" | split: "|" -%}
{%- assign listed = site.drugs | where_exp: "d", "d.layout != 'id_redirect'" | where_exp: "d", "d.noindex != true" -%}
{%- assign l1 = listed | where: "evidence_level", "L1" | sort: "title" -%}
{%- assign l2 = listed | where: "evidence_level", "L2" | sort: "title" -%}
{%- assign trial_drugs = l1 | concat: l2 -%}
{%- assign latest = trial_drugs | sort: "last_modified_at" | last -%}
{%- assign latest_date = latest.last_modified_at | date: "%Y-%m-%d" -%}

# 新規適応症に臨床試験エビデンスがある国内医薬品

<p class="key-answer" data-question="日本の医薬品のうち、新しい適応症に臨床試験のエビデンスがあるのはどれですか？">
JpTxGNN にレポートがある医薬品 {{ listed.size }} 品目のうち <strong>{{ trial_drugs.size }}</strong> 品目は、TxGNN が予測した新規適応症のエビデンスレベルが <strong>L1 または L2</strong>（L1：{{ l1.size }} 品目、L2：{{ l2.size }} 品目）で、臨床試験のエビデンス（ランダム化比較試験、Phase 2–3 試験またはシステマティックレビュー）が見つかっています。
</p>

対象の医薬品は[PMDA](https://www.pmda.go.jp/)の承認情報に基づきます。一覧は {{ latest_date }} 時点で最終更新された医薬品レポートを反映しています。

<div class="key-takeaway">
予測適応症に試験エビデンスがあっても、有効性が証明されたわけではありません。以下の候補はいずれも、臨床使用の前に<strong>臨床検証</strong>と規制当局の審査が引き続き必要です。
</div>

---

## 試験エビデンスのある医薬品（L1–L2）

<div class="table-wrapper"><table>
<thead>
<tr><th>医薬品</th><th>予測新規適応症</th><th>エビデンスレベル</th><th>引用された登録試験（NCT）</th></tr>
</thead>
<tbody>
{%- for drug in trial_drugs -%}
{%- assign indication = "" -%}
{%- for lab in ind_labels -%}{%- if indication == "" -%}{%- assign needle = "<td>" | append: lab | append: "</td>" -%}{%- assign qo = drug.content | split: needle -%}{%- if qo.size > 1 -%}{%- assign indication = qo[1] | split: "</td>" | first | split: "<td>" | last | strip -%}{%- endif -%}{%- endif -%}{%- endfor -%}
{%- assign level_cell = "" -%}
{%- for lab in lev_labels -%}{%- if level_cell == "" -%}{%- assign needle = "<td>" | append: lab | append: "</td>" -%}{%- assign lv = drug.content | split: needle -%}{%- if lv.size > 1 -%}{%- assign level_cell = lv[1] | split: "</td>" | first | split: "<td>" | last | strip -%}{%- endif -%}{%- endif -%}{%- endfor -%}
{%- assign parts = drug.content | split: "NCT" -%}
{%- capture nct_ids -%}{%- for p in parts offset: 1 -%}{%- assign id = p | slice: 0, 8 -%}{%- assign rest = id | remove: "0" | remove: "1" | remove: "2" | remove: "3" | remove: "4" | remove: "5" | remove: "6" | remove: "7" | remove: "8" | remove: "9" -%}{%- if id.size == 8 and rest == "" -%}{{ id }},{%- endif -%}{%- endfor -%}{%- endcapture -%}
{%- assign nct_count = nct_ids | split: "," | uniq | size %}
<tr><td><a href="{{ drug.url | relative_url }}">{{ drug.title }}</a></td><td>{% if indication != "" %}{{ indication }}{% else %}レポート参照{% endif %}</td><td>{{ drug.evidence_level }}{% if level_cell != "" and level_cell != drug.evidence_level %} <a href="{{ drug.url | relative_url }}" title="{{ level_cell | strip_html | escape }}">（留保あり）</a>{% endif %}</td><td>{{ nct_count }}</td></tr>
{%- endfor %}
</tbody>
</table></div>

## 一覧の見方

- **エビデンスレベル**は本サイトの[基準]({{ '/evidence-high/' | relative_url }})に従います：L1＝複数の Phase 3 RCT / システマティックレビュー、L2＝単一の RCT または複数の Phase 2 試験。「（留保あり）」はレポートがレベルに留保を付けていることを示します。判断の前にレポート内の注記をお読みください。
- **予測新規適応症**は各レポートの主な予測です。TxGNN 知識グラフに既に記録されている適応症・禁忌は除外していますが、既存の用途と重なる予測が残る場合があり、その場合はレポートで説明しています。
- **引用された登録試験**は、レポートで引用している ClinicalTrials.gov（NCT）番号の数です。レポートは見つかった試験の一部を引用しています。0 はレポートが登録試験を引用していないことを示し、レベルの根拠は文献エビデンスの節にあります。
- すべてのレベルと手法の詳細は[高エビデンスレベル]({{ '/evidence-high/' | relative_url }})、[全医薬品一覧]({{ '/drugs/' | relative_url }})、[方法論]({{ '/methodology/' | relative_url }})をご覧ください。

---

<div class="disclaimer">
<strong>免責事項</strong><br>
本レポートは学術研究の参考のみを目的としており、<strong>医療アドバイスを構成するものではありません</strong>。必ず医師の指示に従ってください。自己判断で薬剤を調整しないでください。ドラッグリポジショニングに関するいかなる決定にも、完全な臨床検証と規制当局の審査が必要です。
<br><br>
<small>審査者：藥提醒科技有限公司 (yao.care)</small>
</div>
