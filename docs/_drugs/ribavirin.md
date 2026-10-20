---
layout: default
title: Ribavirin
parent: 中エビデンス (L3-L4)
nav_order: 146
evidence_level: L3
indication_count: 1
last_modified_at: 2026-09-17
description: "Ribavirin：予測新適応症は慢性 B 型肝炎ウイルス感染症 (Chronic HBV Infection)（エビデンスレベル L3）。既存適応症：日本の承認適応症は本サイトのデータに未収載"
---

# Ribavirin
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

# Ribavirin：C 型肝炎から慢性 B 型肝炎ウイルス感染症へ

## 一言まとめ

Ribavirin（リバビリン） は抗ウイルス薬で、もともとインターフェロンや他の抗ウイルス薬と併用して慢性 C 型肝炎の治療に用いられます。TxGNN モデルは、本薬が**慢性 B 型肝炎ウイルス感染症 (Chronic Hepatitis B Virus Infection)** に有効である可能性を予測しており、現在、この研究の方向性を支持する **30 件以上の臨床試験**があります。

## 概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 日本の承認適応症は本サイトのデータに未収載（知識グラフ上の適応症：chronic hepatitis C virus infection、hepatitis C virus infection、respiratory syncytial virus infectious disease） |
| 予測新適応症 | 慢性 B 型肝炎ウイルス感染症 (Chronic HBV Infection) |
| TxGNN 予測スコア | 99.86% |
| エビデンスレベル | L3 |
| 日本市販状況 | 本サイトのデータに未収載 |
| 承認番号数 | — |
| 推奨判断 | Proceed with Guardrails |

## この予測が妥当な理由

Ribavirin はヌクレオシド類似体で、広範な抗ウイルス活性を有します。作用機序には以下が含まれます。
- ウイルス RNA ポリメラーゼの阻害
- ウイルスゲノムへの変異の誘導
- 宿主の免疫応答の調節

Ribavirin は主に C 型肝炎の治療薬として承認されていますが、その広範な抗ウイルス活性から、B 型肝炎ウイルスを含む他のウイルスに対しても治療効果を示す可能性があります。特に B 型・C 型肝炎の重複感染や D 型肝炎（B 型肝炎ウイルスをヘルパーウイルスとして必要とする）の患者では、ribavirin とインターフェロンの併用が検討されてきました。

ただし、現在の B 型肝炎の標準治療はヌクレオシド類似体（entecavir、tenofovir など）またはインターフェロンであり、ribavirin は標準レジメンには含まれていない点に注意が必要です。

## 臨床試験エビデンス

| 試験番号 | 相 | 状態 | 人数 | 主な所見 |
|---------|------|------|------|---------|
| [NCT00117533](https://clinicaltrials.gov/study/NCT00117533) | Phase 4 | 不明 | 20 | Peginterferon alfa-2b + ribavirin による B 型・D 型肝炎重複感染の治療 |
| [NCT01318694](https://clinicaltrials.gov/study/NCT01318694) | Phase 3 | 完了 | 1081 | Alisporivir + peginterferon + ribavirin による C 型肝炎の治療 |

（注：臨床試験の大半は C 型肝炎を対象としており、一部は B 型・C 型肝炎の重複感染を扱っています）

## 文献エビデンス

現在の主な文献は C 型肝炎の治療に集中しており、B 型肝炎ウイルス単独感染を対象とした研究は限られています。

## 日本市販情報

日本の承認情報は本サイトのデータに未収載です。

## 安全性に関する考慮事項

**主な警告：**
- 溶血性貧血：最も多くみられる重篤な副作用
- 催奇形性：妊婦には禁忌。治療期間中および治療終了後 6 か月間は避妊が必要
- 心毒性：心疾患を悪化させる可能性

**禁忌：**
- 妊娠中または妊娠している可能性のある女性
- 重篤な心疾患
- ヘモグロビン異常
- 自己免疫性肝炎

## 結論と次のステップ

**判断：Proceed with Guardrails**

**理由：**
Ribavirin は広範な抗ウイルス活性を有し、B 型・D 型肝炎の重複感染での使用を検討した研究もありますが、慢性 B 型肝炎に対する単独使用を支持する十分なエビデンスは現時点では不足しています。既存の B 型肝炎標準治療（entecavir、tenofovir）は有効性と安全性が確認されています。

**推進に必要な事項：**
- ribavirin と既存の B 型肝炎治療の有効性を比較する対照試験の実施
- B 型肝炎治療における ribavirin の位置づけ（補助療法か、特定のサブグループか）の明確化
- 既存のヌクレオシド類似体との併用における安全性と有効性の評価
- 溶血性貧血などの重篤な副作用のモニタリングに特に注意すること


---


<div class="disclaimer" style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin-top: 2rem;">
<strong>⚠️ 免責事項</strong><br>
本レポートは学術研究目的のみであり、<strong>医療アドバイスを構成するものではありません</strong>。
薬の使用は必ず医師の指示に従ってください。自己判断で投薬を変更しないでください。
ドラッグ・リポジショニングの決定には、完全な臨床検証と規制審査が必要です。
</div>
