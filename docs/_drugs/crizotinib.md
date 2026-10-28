---
layout: default
title: Crizotinib
parent: モデル予測のみ
nav_order: 97
evidence_level: L5
indication_count: 9
monitor_inn: "Crizotinib"
predicted_indications: ["fibromatosis, gingival", "fibroma of lung", "hamartoma of lung", "lung benign neoplasm", "pulmonary sulcus neoplasm", "lung germ cell tumor", "inclusion body myopathy with early-onset Paget disease with or without frontotemporal dementia", "junctional epidermolysis bullosa", "Leukomelanoderma-infantilism-intellectual disability-hypodontia-hypotrichosis syndrome"]
last_modified_at: 2026-10-28
description: "Crizotinib：予測新適応症は歯肉線維腫症 (fibromatosis, gingival)（エビデンスレベル L5）。既存適応症：日本の承認情報に適応症の記載なし"
---

# Crizotinib
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **9** 件
{: .fs-6 .fw-300 }

---

## 目次
{: .no_toc .text-delta }

1. TOC
{:toc}

---

<div id="pharmacist" markdown="1">

## 薬剤師評価レポート

</div>

## クリゾチニブ：ALK/ROS1/MET チロシンキナーゼ阻害薬 → 歯肉線維腫症 (fibromatosis, gingival)
{: .text-alpha }

## 一言要約

クリゾチニブは ALK・ROS1・MET を阻害するチロシンキナーゼ阻害薬です。
TxGNN モデルは**歯肉線維腫症 (fibromatosis, gingival)** に有効である可能性を予測していますが、この疾患を直接検討した臨床試験・文献は **0 件**で、予測のみの段階です。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認情報に適応症の記載なし |
| 予測新規適応症 | 歯肉線維腫症 (fibromatosis, gingival) |
| TxGNN 予測スコア | 0.9981 |
| エビデンスレベル | L5 |
| 日本市販状況 | 販売中（有効な承認 2 件／全 2 件） |
| 承認番号数 | 2 件（有効 2 件） |
| 推奨決定 | Hold |

## この予測が妥当である理由

詳細な作用機序データは、本レポート用に集めたデータには含まれていません。クリゾチニブは ALK、ROS1、MET の各チロシンキナーゼを阻害する薬剤として知られています。

歯肉線維腫症とこれらの標的との間に、確立した関連はありません。したがって、機序面の裏付けは現時点では乏しく、この予測はモデルによるスコアに基づくものにとどまります。

## 臨床試験エビデンス

現在、関連する臨床試験の登録はありません。

## 文献エビデンス

現在、関連する文献はありません。

## 日本市販情報

| 承認番号 | 商品名 | 剤形 |
|---------|------|------|
| 622149601 | ザーコリカプセル２００ｍｇ | カプセル２００ｍｇ |
| 622149701 | ザーコリカプセル２５０ｍｇ | カプセル２５０ｍｇ |

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 分子標的薬（ALK/ROS1/MET チロシンキナーゼ阻害薬） |
| 骨髄抑制リスク | 添付文書の警告および注意事項を参照してください |
| 催吐性分類 | 添付文書の警告および注意事項を参照してください |
| モニタリング項目 | CBC、肝機能、腎機能、心電図（QT 延長・徐脈の報告あり） |
| 取り扱い防護 | 添付文書および施設の抗悪性腫瘍薬取り扱い規程に従ってください |

## 安全性に関する考慮事項

- **薬物相互作用**：相互作用 100 件が確認されています。主なものは以下のとおりです。
  - 重大 (Major)：クラリスロマイシン、シサプリド、ドラセトロン、エリグルスタット、グラニセトロン
  - 中等度 (Moderate)：ファモチジン、メトホルミン、ロペラミド、ブプロピオン、アプレピタント、デキサメタゾン、ブデソニド など

その他の安全性情報については添付文書を参照してください。

## 結論と次のステップ

**決定：Hold**

**理由：**
歯肉線維腫症を直接検討した臨床試験や文献がなく、機序的な裏付けも確認できません。エビデンスはモデル予測のみ（L5）です。

**進める場合に必要なもの：**
- 歯肉線維腫症の病態と ALK/ROS1/MET 経路の関連を示す前臨床・機序研究
- 詳細な作用機序データ（MOA）
- 添付文書（PMDA）の警告・禁忌情報の取得と安全性評価
- 非腫瘍性疾患に対する抗腫瘍性キナーゼ阻害薬の利益・リスク評価
## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：ザーコリ

**販売名（規格別）**：ザーコリカプセル200mg、ザーコリカプセル250mg
<!-- brand-names:end -->

