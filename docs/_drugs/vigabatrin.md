---
noindex: true
sitemap: false
layout: default
title: Vigabatrin
parent: モデル予測のみ (L5)
nav_order: 189
evidence_level: L5
indication_count: 1
last_modified_at: 2026-09-17
---

# Vigabatrin
{: .fs-9 }

エビデンスレベル: **L5** | 予測適応症: **1** 件
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

# Vigabatrin：抗てんかん薬の補助療法

## 一言まとめ

Vigabatrin（ビガバトリン） は抗てんかん薬の補助療法に用いられる薬剤です。
TxGNN モデルは新たな適応症を**予測していません**。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 抗てんかん薬の補助療法 |
| 予測新適応症 | なし |
| TxGNN 予測スコア | N/A |
| エビデンスレベル | N/A |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | 再利用候補なし |

## 新しい適応症が予測されない理由

Vigabatrin は選択的な GABA トランスアミナーゼ（GABA-T）の不可逆的阻害薬で、4-aminobutyrate aminotransferase を阻害することで脳内 GABA 濃度を上昇させます。作用機序は非常に特異性が高く、主にてんかんに関連する神経伝達の異常を標的とするため、TxGNN の知識グラフ解析では他の疾患との有意な関連は認められませんでした。

## 臨床試験エビデンス

新適応症に関連する臨床試験はありません。

## 文献エビデンス

新適応症に関連する文献エビデンスはありません。

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

### 重大な薬物相互作用（Major）

| 相互作用薬 | 重症度 |
|-------------|--------|
| Hydrocortisone | Major |
| Triamcinolone | Major |
| Dexamethasone | Major |
| Betamethasone | Major |
| Budesonide | Major |
| Prednisone | Major |
| Prednisolone | Major |
| Methylprednisolone | Major |
| Deflazacort | Major |
| Deferoxamine | Major |
| Chloroquine | Major |
| Hydroxychloroquine | Major |
| Quinine | Major |
| Tamoxifen | Major |

### 中等度の薬物相互作用（Moderate）

多くの鎮静薬、抗ヒスタミン薬およびオピオイド系薬剤と中等度の相互作用があり、中枢神経抑制作用が増強する可能性があります。代表的なものとして、Morphine、Codeine、Cetirizine、Diphenhydramine、Ethanol などが挙げられます。

### 作用標的

- Vesicular inhibitory amino acid transporter (SLC32A1)
- 4-aminobutyrate aminotransferase (ABAT)

## 結論と次のステップ

**判断：再利用候補なし**

**理由：**
Vigabatrin の作用機序は GABA 作動性神経伝達に高度に特異的であり、TxGNN モデルでは十分なエビデンスに裏付けられた新適応症候補は認められませんでした。

**注意事項：**
- Vigabatrin は不可逆的な視野欠損を引き起こす可能性があるため、定期的な視力モニタリングが必要です
- コルチコステロイドとの併用では相互作用に特に注意が必要です


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
