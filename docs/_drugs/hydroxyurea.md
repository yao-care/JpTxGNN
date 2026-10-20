---
layout: default
title: Hydroxyurea
parent: 高エビデンス (L1-L2)
nav_order: 82
evidence_level: L2
indication_count: 1
last_modified_at: 2026-04-19
description: "Hydroxyurea：予測新適応症は女性乳癌 (female breast carcinoma)（エビデンスレベル L2）。既存適応症：日本の承認適応症は本サイトのデータに未収載"
---

# Hydroxyurea
{: .fs-9 }

エビデンスレベル: **L2** | 予測適応症: **1** 件
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

# Hydroxyurea：血液腫瘍から女性乳癌へ

## 一言まとめ

Hydroxyurea は本来、慢性骨髄性白血病、骨髄線維症および真性赤血球増加症の治療に用いられています。
TxGNN モデルは、本剤が**女性乳癌 (female breast carcinoma)** に有効な可能性があると予測しており、
現在 **20 篇を超える文献**がこの研究の方向性を支持しています。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：melanoma、sickle cell anemia、hereditary persistence of fetal hemoglobin、ovarian cancer、ovarian adenocarcinoma、hereditary breast ovarian cancer syndrome） |
| 予測新適応症 | 女性乳癌 (female breast carcinoma) |
| TxGNN 予測スコア | 99.97% |
| エビデンスレベル | L2 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Hydroxyurea はリボヌクレオチド還元酵素阻害薬であり、DNA 合成を阻害することで抗腫瘍作用を示します。
細胞が G1 期から S 期へ移行するのを抑制し、細胞の放射線感受性を高めることができます。

**予測の妥当性の分析：**
- Hydroxyurea は複数の固形腫瘍（卵巣癌、頭頸部癌）に対して承認されている
- 乳癌の大量化学療法レジメンでの使用経験がある
- 放射線増感剤として、放射線治療と併用できる
- 他の薬剤（valproic acid など）との相乗作用を示す研究がある

**作用機序による裏付け：**
- DNA の合成と修復を阻害する
- 複製ストレスを誘導し、DNA 二本鎖切断を増加させる
- valproic acid との併用により相同組換え修復を抑制できる（PMID: 28837865）
- 脂質-薬物複合体により細胞への取り込み率を高められる（PMID: 38211596）

## 臨床試験エビデンス

文献で報告されている臨床経験は以下のとおりです。

| 研究タイプ | 年 | 雑誌 | 主な所見 |
|---------|------|------|---------|
| Phase I | 1991 | Am J Clin Oncol | 進行乳癌における FU-LV-HU 併用レジメンの Phase I 試験 |
| Phase I/II | 1994 | Bone Marrow Transplant | 転移性乳癌に対する、自家幹細胞移植を併用した大量 CY-Thiotepa-HU |
| Phase I | 1992 | Cancer Chemother Pharmacol | 5-FU、LV、HU と cisplatin の放射線療法併用における臨床薬理学的研究 |

## 文献エビデンス

| PMID | 年 | タイプ | 雑誌 | 主な所見 |
|------|-----|------|------|---------|
| [38211596](https://pubmed.ncbi.nlm.nih.gov/38211596/) | 2024 | in silico | Drug Res | PI3K/AKT/mTOR 経路を標的とする HU 脂質-薬物複合体の設計 |
| [28837865](https://pubmed.ncbi.nlm.nih.gov/28837865/) | 2017 | in vitro 研究 | DNA Repair | Valproic acid による乳癌細胞の HU への反応性の増感 |
| [32795962](https://pubmed.ncbi.nlm.nih.gov/32795962/) | 2020 | in vitro 研究 | DNA Repair | 2-hexyl-4-pentynoic acid と HU の併用による乳癌の抑制 |
| [7914447](https://pubmed.ncbi.nlm.nih.gov/7914447/) | 1994 | Phase I/II | Bone Marrow Transplant | 転移性乳癌に対する固定化治療としての大量 CY-Thiotepa-HU |
| [21730979](https://pubmed.ncbi.nlm.nih.gov/21730979/) | 2011 | in vitro 研究 | Br J Cancer | 乳癌・卵巣癌細胞における ATR 阻害薬と HU の効果 |

## 細胞毒性

| 項目 | 内容 |
|------|------|
| 細胞毒性分類 | 従来型の細胞毒性薬 |
| 骨髄抑制リスク | 高度 |
| 催吐性分類 | 低度 |
| モニタリング項目 | CBC（分画含む）、肝腎機能、MCV |
| 取り扱い時の防護 | 細胞毒性薬の取り扱い規定に従って操作すること |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **薬物相互作用**：文献では多くの場合、他の化学療法薬との併用で使用されている
- **注意事項**：
  - 骨髄抑制が最も主要な用量制限毒性である
  - 長期使用により二次性白血病のリスクが高まる可能性がある
  - 皮膚毒性（色素沈着、潰瘍）
  - 巨赤芽球性貧血
- **乳癌への適用に関する考慮**：
  - 現在は主に大量化学療法レジメンで用いられている
  - 既存の標準治療との比較を考慮する必要がある

安全性情報は添付文書をご参照ください。

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
- HU の乳癌における活性を支持する in vitro 研究が豊富にある
- 特に大量化学療法レジメンにおいて、Phase I/II の臨床経験がすでにある
- 新規の薬物送達システム（脂質複合体など）により効果が改善する可能性がある
- 他の薬剤との相乗作用により併用療法の機会が得られる

**推進に必要な事項：**
- 現代の乳癌治療における HU の役割を評価する（CDK4/6 阻害薬、免疫療法との比較または併用）
- 腫瘍への標的性を高めるため、より有効な薬物送達システムを開発する
- 最も適した乳癌サブタイプ（トリプルネガティブ乳癌など）を特定する
- valproic acid やその他の増感剤との併用レジメンを設計する


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
