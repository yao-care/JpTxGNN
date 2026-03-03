---
layout: default
title: SMART App Gallery 参考
parent: SMART on FHIR
nav_order: 4
description: SMART Health IT App Gallery の参考情報と既存アプリケーションの分析
permalink: /smart/app-gallery-reference/
---

# SMART App Gallery 参考

SMART Health IT App Gallery は、SMART on FHIR 標準に準拠する医療アプリケーションのカタログです。本ページでは、参考となるアプリケーションを分析します。

---

## App Gallery について

[SMART Health IT App Gallery](https://apps.smarthealthit.org/) は：

- SMART on FHIR アプリケーションの公式カタログ
- 審査済みの医療健康アプリを収録
- 開発者と医療機関の両方に価値ある情報を提供

---

## 参考アプリケーション

### 臨床決定支援系

| アプリ名 | 説明 | 参考ポイント |
|---------|------|-------------|
| CDS Hooks Sandbox | CDS Hooks テスト環境 | フック実装パターン |
| Medication Advisor | 処方支援ツール | UI/UX 設計 |
| Drug Interaction Checker | 薬物相互作用チェッカー | DDI 表示方法 |

### 患者向け

| アプリ名 | 説明 | 参考ポイント |
|---------|------|-------------|
| Apple Health Records | 健康記録アプリ | データ同期パターン |
| MyChart | 患者ポータル | 認証フロー |

---

## JpTxGNN アプリ仕様

### 基本情報

| 項目 | 内容 |
|------|------|
| **アプリ名** | jptxgnn-smart-app |
| **Application Type** | SMART App |
| **FHIR Compatibility** | R4 |
| **Designed for** | Patients & Clinicians |
| **Platform** | Web |
| **Pricing** | Free / Open Source |
| **Privacy Policy** | [https://jptxgnn.yao.care/privacy-policy/]({{ '/privacy-policy/' | relative_url }}) |

### 機能概要

1. **用薬読み取り** - EHR から患者の用薬リストを取得
2. **ドラッグリポジショニング検索** - 各医薬品の予測新適応症を表示
3. **スコア表示** - TxGNN 予測スコアを明示
4. **詳細リンク** - 各医薬品の詳細ページへのリンク

---

## App Gallery 登録要件

### 必須要件

- [ ] SMART on FHIR R4 準拠
- [ ] HTTPS 必須
- [ ] プライバシーポリシーの公開
- [ ] スクリーンショット/デモビデオ

### 推奨事項

- [ ] アクセシビリティ対応（WCAG 2.1）
- [ ] モバイルレスポンシブ
- [ ] 多言語サポート

---

## 関連リンク

- [SMART Health IT App Gallery](https://apps.smarthealthit.org/)
- [SMART App 開発ガイド](http://docs.smarthealthit.org/)
- [HL7 FHIR App Launch](https://build.fhir.org/ig/HL7/smart-app-launch/)
