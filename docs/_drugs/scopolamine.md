---
noindex: true
sitemap: false
layout: default
title: Scopolamine
parent: モデル予測のみ (L5)
nav_order: 154
evidence_level: L5
indication_count: 0
last_modified_at: 2026-09-17
predicted_indications: []
---

# Scopolamine
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **0** 件
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

## Scopolamine：解痙薬から神経・眼科疾患への探索
{: .text-alpha }

## 一言まとめ

Scopolamine（スコポラミン） は主に胃腸管、胆道および尿路の痙攣の緩和に用いられる。
TxGNN モデルは、本剤が**馬尾症候群 (Cauda Equina Syndrome)** および**神経因性膀胱**に有効である可能性を予測しているが、
これらの新適応症を裏付ける臨床試験および文献は現時点では存在しない。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：peptic ulcer disease、allergic rhinitis、vasomotor rhinitis、uveitis、iris disease、ciliary body disease） |
| 予測新適応症 | Cauda Equina Syndrome（馬尾症候群） |
| TxGNN 予測スコア | 99.99% |
| エビデンスレベル | L5 |
| 日本市販状況 | 国内未承認（承認記録なし） |
| 承認番号数 | 0 件（有効 0 件） |
| 推奨判断 | Hold |

## この予測が妥当な理由

Scopolamine（スコポラミン）は抗コリン薬であり、ムスカリン受容体拮抗薬として
副交感神経の活動を抑制し、鎮痙および分泌抑制の効果を示す。

**TxGNN が予測した新適応症と作用機序との関連性の分析：**

| 順位 | 予測適応症 | 予測スコア | TxGNN 順位 | 作用機序との関連性 |
|------|-----------|---------|-----------|----------|

馬尾症候群および神経因性膀胱の予測は比較的妥当である。Scopolamine の抗コリン作用が、膀胱の過活動や痙攣症状を緩和し得るためである。
一方、結膜炎関連の予測は、既知の作用機序との関連性が弱い。

## 臨床試験エビデンス

予測適応症を対象とした臨床試験の登録は現時点では確認されていない。

## 文献エビデンス

予測適応症を対象とした PubMed 文献は現時点では確認されていない。

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **主な薬物相互作用（重大）**：
  - Topiramate、Zonisamide：体温調節障害のリスクを高める可能性がある

- **中等度の薬物相互作用**：
  - オピオイド系薬剤：Fentanyl、Morphine、Codeine、Hydrocodone、Tramadol、Buprenorphine など
  - 抗コリン薬：Atropine、Hyoscyamine、Glycopyrronium、Benzatropine など
  - 抗精神病薬：Aripiprazole、Asenapine、Brexpiprazole など
  - 抗ヒスタミン薬：Chlorpheniramine、Brompheniramine など
  - β遮断薬：Atenolol、Bisoprolol、Acebutolol など
  - その他：Ethanol、Amantadine、Amitriptyline、Loperamide

- **軽度の薬物相互作用**：
  - Acetaminophen、Hydrochlorothiazide

安全性情報は添付文書をご参照ください。

## 結論と次のステップ

**判断：Hold**

**理由：**
TxGNN が予測した馬尾症候群および神経因性膀胱の適応症は、Scopolamine の抗コリン作用機序とある程度の関連があるが、
現時点では臨床試験および文献による裏付けがない。結膜炎関連の予測は、既知の作用機序との関連性が弱い。

**推進に必要な事項：**
- 神経因性膀胱を対象とした臨床試験データ
- 馬尾症候群に関連する膀胱機能障害に対する Scopolamine の応用の検討
- 長期使用時の安全性の評価、特に他の抗コリン薬との併用時

---

<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
