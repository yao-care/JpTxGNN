---
noindex: true
sitemap: false
layout: default
title: Caplacizumab
parent: モデル予測のみ (L5)
nav_order: 37
evidence_level: L5
indication_count: 1
last_modified_at: 2026-09-17
description: "Caplacizumab：予測新適応症は血小板放出障害 (primary release disorder of platelets)（エビデンスレベル L5）。既存適応症：後天性血栓性血小板減少性紫斑病 (aTTP)、血漿交換及び免疫抑制剤との併用"
---

# Caplacizumab
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

# Caplacizumab：後天性TTPから血小板原発放出障害へ

## 一言まとめ
Caplacizumab（カプラシズマブ） は後天性血栓性血小板減少性紫斑病(aTTP)の治療に用いられる抗von Willebrand因子ナノボディであり、TxGNN は血小板原発放出障害(primary release disorder of platelets)に対する治療可能性を予測しています。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：thrombocytopenic purpura） |
| 予測新適応症 | 血小板原発放出障害 (primary release disorder of platelets) |
| TxGNN 予測スコア | 99.9998% |
| エビデンスレベル | L5 (予測のみ) |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Hold |

## この予測が妥当な理由
Caplacizumab はヒト化二価ナノボディ(Nanobody)です：

1. **作用機序**：von Willebrand 因子(vWF)のA1ドメインに結合し、血小板とvWFの相互作用を阻害します
2. **抗血栓作用**：vWF多量体上での血小板の異常凝集を防ぎます
3. **高い予測スコア**：TxGNN は極めて高いスコア(99.9998%)を付与しており、順位は第8位です

ただし、この予測は慎重に捉える必要があります：
- 血小板原発放出障害は血小板機能欠損症であり、血小板の放出反応の異常を伴います
- Caplacizumab は vWF-血小板軸に作用するものであり、血小板の放出機構に直接影響するものではありません
- 理論上、caplacizumab は血小板機能障害を改善するどころか、悪化させる可能性があります

## 臨床試験エビデンス
血小板原発放出障害に対する caplacizumab の臨床試験は現時点ではありません。

**既存適応症(aTTP)に関連する主な臨床試験**：

1. **HERCULES 試験 (NCT02553317)** - Phase III
   - 145例の患者が参加
   - caplacizumab により血小板数の回復までの期間が有意に短縮することを実証
   - aTTP の再発および関連死亡を減少

2. **Post-HERCULES (NCT02878603)** - 長期追跡
   - caplacizumab の長期安全性を評価
   - 104例の患者が追跡を完了

3. **日本 Phase 2/3 試験 (NCT04074187)**
   - 日本人患者21例
   - アジア人集団における有効性と安全性を確認

## 文献エビデンス
既存適応症(aTTP)に関する主な文献：

1. **Scully M ら (2019)** - *New England Journal of Medicine*
   - HERCULES 試験の結果を報告
   - aTTP 治療における caplacizumab の位置づけを確立

2. **Peyvandi F ら (2016)** - *New England Journal of Medicine*
   - Phase II 試験で caplacizumab の有効性を初めて実証

3. **Zheng XL ら (2020)** - *Journal of Thrombosis and Haemostasis*
   - ISTH による TTP 治療ガイドライン
   - caplacizumab を標準治療の選択肢として収載

血小板原発放出障害に関する文献はありません。

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項
### 主な副作用
- 出血事象(鼻出血、歯肉出血が最も多い)
- 頭痛
- 蕁麻疹

### 重大な警告
- 出血リスクの増加
- 使用期間中は手術および侵襲的処置を避けること
- 出血徴候のモニタリングが必要

### 薬物相互作用(主なもの)

| 相互作用のある薬剤 | 重症度 |
|-------------|---------|
| アスピリン | 重度 |
| 抗凝固薬(apixaban, rivaroxaban等) | 重度 |
| 血小板抑制薬 | 重度 |
| Fondaparinux | 重度 |
| NSAIDs | 中等度 |

## 結論と次のステップ
**エビデンスレベル**：L5 (TxGNN の予測のみで、臨床的・薬理学的裏付けなし)

**推奨**：Hold (当面は推奨しない)
1. 血小板原発放出障害と caplacizumab の作用機序には明確な関連がありません
2. vWF-血小板相互作用の抑制は、理論上、血小板放出機能を改善するどころか悪化させる可能性があります
3. 極めて高い TxGNN スコアは、治療上の真の関連ではなく、血小板関連疾患の知識グラフ上で両者の位置が近いことを反映している可能性があります

**次のステップ**：
- 臨床での探索は推奨しません
- 臨床で aTTP に血小板機能障害を合併した症例に遭遇した場合は、関連データを収集して解明に役立てることが考えられます
- 非典型HUSなど、他の血栓性微小血管症における caplacizumab の潜在的応用研究に注力することを推奨します

**特記事項**：この予測は TxGNN アルゴリズムによる偽陽性の可能性があり、臨床上、この予測に基づいて治療を決定すべきではありません。


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
