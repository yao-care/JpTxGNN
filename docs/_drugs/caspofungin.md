---
noindex: true
sitemap: false
layout: default
title: Caspofungin
parent: モデル予測のみ (L5)
nav_order: 41
evidence_level: L5
indication_count: 1
last_modified_at: 2026-09-17
---

# Caspofungin
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

# Caspofungin：抗真菌薬から胃泌素分泌異常への探索

## 一言まとめ

Caspofungin（カスポファンギン） はキャンディン系抗真菌薬で、侵襲性アスペルギルス症およびカンジダ感染症に用いられる。
TxGNN モデルは、本剤が**胃泌素分泌異常 (gastrin secretion abnormality)** に有効である可能性を予測しているが、
この予測を裏づける**臨床試験や文献は現時点でない**。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：esophageal candidiasis、candidemia） |
| 予測新適応症 | 胃泌素分泌異常 (gastrin secretion abnormality) |
| TxGNN 予測スコア | 99.44% |
| エビデンスレベル | L5 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Hold |

## この予測が妥当な理由

Caspofungin はキャンディン系抗真菌薬であり、その作用機序は次のとおりである。

1. **細胞壁合成の阻害**：1,3-beta-D-glucan 合成酵素を阻害し、真菌の細胞壁を破壊する
2. **選択的作用**：主にカンジダ属とアスペルギルス属に有効

**予測適応症との潜在的関連の分析**：
- 現時点では、caspofungin と胃泌素分泌調節との関連を支持する明確な生物学的機序はない
- この予測は知識グラフ上の間接的な関連に由来する可能性があるが、実質的なエビデンスを欠く
- 胃泌素分泌異常は通常、Zollinger-Ellison 症候群などの内分泌疾患に関連し、抗真菌治療とは直接の関係がない

## 臨床試験エビデンス

caspofungin による胃泌素分泌異常の治療を対象とした臨床試験は、現時点でない。

## 文献エビデンス

caspofungin の胃泌素分泌異常への使用を支持する関連文献は、現時点でない。

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

**重要な警告**：
- 肝機能のモニタリングが必要であり、肝機能障害患者では用量調整が必要
- 輸注関連反応（発熱、悪寒、潮紅など）を起こすことがある
- 中等度の肝機能障害（Child-Pugh 7-9 点）では減量して使用する

**薬物相互作用**：
- Dexamethasone（Major）：caspofungin の血中濃度を低下させる可能性がある
- Leflunomide（Major）：肝毒性のリスクを増加させる可能性がある
- Teriflunomide（Major）：肝毒性のリスクを増加させる可能性がある
- Tacrolimus（Moderate）：Caspofungin が tacrolimus の血中濃度を低下させる可能性がある
- Cyclosporine（Moderate）：caspofungin の血中濃度と肝毒性のリスクを増加させる可能性がある
- Naltrexone（Moderate）：相互作用を起こす可能性がある
- Lumacaftor（Moderate）：caspofungin の濃度を低下させる可能性がある

**重症度不明の多様な相互作用**：
Calcitriol、Pantoprazole、Doxycycline、Morphine、Omeprazole、Lansoprazole、Vancomycin、Fluconazole などが含まれ、臨床使用時には慎重なモニタリングを推奨する。

## 結論と次のステップ

**判断：Hold**

**理由：**
この予測には生物学的な妥当性と臨床的エビデンスの裏づけがない。Caspofungin は抗真菌薬であり、その作用機序と胃泌素分泌調節との間に明確な関連はない。さらなる前臨床または臨床のエビデンスが得られるまでは、この適応症の探索は推奨しない。

**推進に必要な事項：**
- caspofungin と胃泌素分泌との潜在的な関連を解明する基礎研究
- 前臨床の動物実験による検証
- 明確な作用機序の仮説
- 臨床試験デザインの妥当性の論証


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
