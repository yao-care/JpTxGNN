---
layout: default
title: Amcinonide
parent: 中エビデンス (L3-L4)
nav_order: 20
evidence_level: L3
indication_count: 1
last_modified_at: 2026-04-19
description: "Amcinonide：予測新適応症は皮膚炎 (dermatitis)（エビデンスレベル L3）。既存適応症：日本の承認適応症は本サイトのデータに未収載、atopic eczema、dermatitis, atopic…"
---

# Amcinonide
{: .fs-9 }

エビデンスレベル: **L3** | 予測適応症: **1** 件
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

## Amcinonide：アトピー性皮膚炎から皮膚炎へ
{: .text-alpha }

## 一言まとめ

Amcinonide（アムシノニド） はもともと、アトピー性皮膚炎、接触皮膚炎、乾癬などの急性・慢性皮膚疾患の治療に用いられてきた薬剤です。
TxGNN モデルは、本剤が**皮膚炎 (dermatitis)** に有効である可能性を予測しており、
現在 **20 件の文献**がこの方向性を支持しています。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：exanthem (disease)、atopic eczema、dermatitis, atopic、contact dermatitis、occupational dermatitis、seborrheic dermatitis） |
| 予測新適応症 | 皮膚炎 (dermatitis) |
| TxGNN 予測スコア | 99.30% |
| エビデンスレベル | L3 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Already Approved (既存適応症の範囲内) |

## この予測が妥当な理由

Amcinonide は高力価の外用ステロイドで、副腎皮質ホルモン系の薬剤に分類されます。作用機序には以下が含まれます。

1. **抗炎症作用**：炎症性メディエーターの放出を抑制し、血管拡張と浮腫を軽減する
2. **抗アレルギー作用**：肥満細胞を安定化し、ヒスタミンの放出を減少させる
3. **免疫調節**：免疫細胞の活性化と遊走を抑制する

予測された適応症「皮膚炎」は、実際には既存適応症の範囲内（アトピー性皮膚炎や接触皮膚炎はいずれも皮膚炎に含まれる）にあたります。この予測は、モデルが本剤の適応症を正しく識別していることを裏付けるものです。

## 臨床試験エビデンス

現時点では、Amcinonide を広義の皮膚炎に用いる新たな臨床試験の登録は確認されていません。

## 文献エビデンス

| PMID | 発表年 | 種類 | 雑誌 | 主な知見 |
|------|-----|------|------|---------|
| [6383735](https://pubmed.ncbi.nlm.nih.gov/6383735/) | 1984 | RCT | Cutis | 湿疹性皮膚炎の治療で amcinonide と halcinonide を比較し、両者とも有効であった |
| [7030645](https://pubmed.ncbi.nlm.nih.gov/7030645/) | 1981 | RCT | Cutis | Amcinonide は灼熱痛の緩和において halcinonide より有意に優れていた |
| [391500](https://pubmed.ncbi.nlm.nih.gov/391500/) | 1979 | RCT | Cutis | 湿疹性皮膚炎の治療で、amcinonide は betamethasone valerate より効果が優れていた |
| [820519](https://pubmed.ncbi.nlm.nih.gov/820519/) | 1976 | CCT | Curr Ther Res | 二重盲検比較試験で、amcinonide と betamethasone valerate の効果は同等であった |
| [32555122](https://pubmed.ncbi.nlm.nih.gov/32555122/) | 2020 | Review | Med Lett Drugs Ther | アトピー性皮膚炎治療薬の総説。amcinonide などの外用ステロイドを含む |

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

- **薬物相互作用**：
  - **軽度の相互作用**：複数の血糖降下薬（Metformin、Glimepiride、各種インスリンなど）との併用により、血糖コントロールに影響する可能性がある
- **外用時の注意事項**：
  - 長期使用により、皮膚萎縮や毛細血管拡張が生じる可能性がある
  - 広範囲への使用や密封療法では、全身吸収のリスクが高まる可能性がある
- **過敏反応**：文献では、一部の患者で amcinonide による接触皮膚炎が報告されており、交差アレルギーに注意が必要

## 結論と次のステップ

**判断：Already Approved (既存適応症の範囲内)**

**理由：**
予測された適応症「皮膚炎」は、実際には既に承認されている適応症に含まれています。Amcinonide は高力価の外用ステロイドとして、各種皮膚炎に効果があります。この予測は、モデルが薬剤と疾患の関係を正しく識別していることを裏付けています。

**臨床上の推奨：**
- 皮膚炎の重症度に応じて、適切な力価のステロイドを選択する
- 使用部位に注意する（顔面や間擦部では高力価のステロイドを避ける）
- 長期使用に伴う局所の副作用をモニタリングする


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
