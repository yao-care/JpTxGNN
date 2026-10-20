---
layout: default
title: Salicylamide
parent: 中エビデンス (L3-L4)
nav_order: 152
evidence_level: L4
indication_count: 1
last_modified_at: 2026-09-17
description: "Salicylamide：予測新適応症は感冒 (common cold)、咽頭炎 (pharyngitis)（エビデンスレベル L4）。既存適応症：日本の承認適応症は本サイトのデータに未収載"
---

# Salicylamide
{: .fs-9 }

エビデンスレベル: **L4** | 予測適応症: **1** 件
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

# Salicylamide：解熱鎮痛から感冒関連疾患へ

## 一言まとめ

Salicylamide（サリチルアミド） は元来、解熱鎮痛に用いられてきた。TxGNN モデルは、本剤が**感冒 (common cold)** および**咽頭炎 (pharyngitis)** に有効である可能性を予測しており、これらの予測は複数の過去の文献により裏付けられている。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：headache disorder） |
| 予測新適応症 | 感冒 (common cold)、咽頭炎 (pharyngitis) |
| TxGNN 予測スコア | 99.93% (咽頭炎)、99.26% (感冒) |
| エビデンスレベル | L4 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Worth Exploring |

## この予測が妥当な理由

Salicylamide はサリチル酸のアミド誘導体であり、以下の薬理学的特性を有する。

1. **解熱作用**：プロスタグランジンの合成を抑制し、発熱反応を低下させる。

2. **鎮痛作用**：感冒に伴う頭痛、咽頭痛などの症状を緩和する。

3. **抗炎症作用**：上気道感染に伴う炎症反応を軽減する。

4. **配合剤での使用経験**：歴史的に他の成分と組み合わせて感冒薬の配合剤とされることが多く、実際の臨床使用経験がある。

## 臨床試験エビデンス

現時点で新たな臨床試験の登録はないが、歴史的には多数の臨床使用経験がある。

## 文献エビデンス

### 咽頭炎関連文献（3 件）

1. **Fichsel (1963)** - Kinderarztliche Praxis
   - タイトル：Experiences with a new antipyretic and analgesic in a new rectal capsule form
   - 要点：小児科での使用経験であり、咽頭炎などの上気道感染を含む
   - [PubMed リンク](https://pubmed.ncbi.nlm.nih.gov/14126993/)

2. **Ricciardiello (1969)** - Minerva Medica
   - タイトル：Double-blind study of 2 bismuth preparations in pharyngo-tonsillitis
   - 種類：二重盲検試験
   - 要点：Salicylamide を含む製剤を咽頭扁桃炎に用いた
   - [PubMed リンク](https://pubmed.ncbi.nlm.nih.gov/5354503/)

3. **Guaschino (1953)** - Gazzetta Medica Italiana
   - タイトル：Therapy of catarrhal tonsillitis in infancy with o-hydroxybenzamide (salicylamide) associated with sodium p-aminobenzoate
   - 要点：乳幼児のカタル性扁桃炎の治療経験
   - [PubMed リンク](https://pubmed.ncbi.nlm.nih.gov/13060598/)

### 感冒関連文献（9 件）

1. **McEwan (1959)** - Scottish Medical Journal
   - タイトル：Dilacol in the common cold
   - 要点：Salicylamide を含む配合剤を感冒に用いた
   - [PubMed リンク](https://pubmed.ncbi.nlm.nih.gov/13646666/)

2. **Nishi et al. (1990)** - Journal of Chromatography
   - タイトル：Separation and determination of the ingredients of a cold medicine by micellar electrokinetic chromatography with bile salts
   - 要点：感冒薬中の Salicylamide の分析方法
   - [PubMed リンク](https://pubmed.ncbi.nlm.nih.gov/2307715/)

3. **Rohr (1962)** - Praxis
   - タイトル：Serial studies with a larger group for the testing of the prophylactic and therapeutic properties of NO-FLU in colds
   - 要点：Salicylamide を含む感冒薬の予防および治療効果に関する研究
   - [PubMed リンク](https://pubmed.ncbi.nlm.nih.gov/14493422/)

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

### 薬物相互作用

現時点で DDInter データベースには、Salicylamide の重大な薬物相互作用の記録はない。

### 特殊な注意事項

- **過量投与による毒性**：過量使用により毒性反応が生じたとの文献報告がある
- **肝代謝**：主にグルクロン酸抱合により代謝されるため、肝機能障害のある患者では注意が必要
- **サリチル酸類似反応**：アスピリンに類似したアレルギー反応が起こる可能性がある

### アスピリンとの違い

文献によれば、アスピリンアレルギーのある患者でも、シクロオキシゲナーゼ阻害能が弱いことから Salicylamide を安全に使用できる可能性がある。

## 結論と次のステップ

**判断：Worth Exploring**

**理由：**
1. 薬理学的機序が感冒関連症状への使用を支持している
2. 過去の臨床使用経験と文献による裏付けがある
3. 既知の用途：知識グラフまたは承認情報に記録済み（本サイトのデータに未収載の日本市販状況とは別に、すでに既知の用途として扱われています）
4. 安全性プロファイルは比較的良好である

**推進に必要な事項：**
- 有効性を評価する現代的なランダム化比較試験
- 用量および投与方法の標準化
- 既存の感冒薬との比較研究
- 配合剤開発の可能性の検討


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
