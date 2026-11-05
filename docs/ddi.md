---
layout: default
title: 薬物-薬物相互作用
parent: 安全性データ
nav_order: 1
description: "DDI（薬物-薬物相互作用）データベース"
permalink: /ddi/
---

# 薬物-薬物相互作用（DDI）

<p class="key-answer" data-question="DDI とは？">
DDI（Drug-Drug Interaction）は、2 種類以上の医薬品を併用した際に生じる相互作用です。効果の増強・減弱、副作用の増加など、様々な影響を及ぼす可能性があります。
</p>

---

## 概要

ドラッグリポジショニング候補を検討する際、既存の併用薬との相互作用は重要な安全性考慮事項です。

---

## データの状況

<div style="background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 16px; margin: 20px 0;">
<strong>現在の状況</strong><br>
薬物-薬物相互作用（DDI）は DDInter のダウンロードファイル（<code>ddinter_code_*.csv</code>：222,383 行、重複を除いた 160,235 組の薬物ペア）を取得済みで、薬物レポートの作成時に参照し、一部のレポートの安全性の項に相互作用を記載しています。サイト上で DDI を検索・チェックする機能はまだ提供していません。DDSI・DFI・DHI のデータは未取得です。
</div>

---

## 相互作用の重大度

| レベル | 説明 | 対応 |
|--------|------|------|
| **重大** | 生命に関わる可能性 | 併用禁忌 |
| **中等度** | 注意が必要 | モニタリング推奨 |
| **軽度** | 臨床的意義は限定的 | 経過観察 |

---

## 関連リンク

- [DDInter 2.0](https://ddinter2.scbdd.com/)
- [安全性データに戻る]({{ '/safety/' | relative_url }})
