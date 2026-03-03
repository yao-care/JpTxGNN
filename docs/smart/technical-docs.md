---
layout: default
title: 技術文書
parent: SMART on FHIR
nav_order: 2
description: JpTxGNN SMART on FHIR 技術仕様、OAuth 設定、FHIR API エンドポイント、医薬品マッピングフロー
permalink: /smart/technical-docs/
---

# SMART on FHIR 技術文書

本ページでは、開発者と IT 担当者向けに JpTxGNN SMART App の技術仕様を提供します。

---

## 技術仕様

### SMART on FHIR 設定

| 項目 | 値 |
|------|------|
| FHIR バージョン | R4 |
| Client ID | `jptxgnn-smart-app` |
| Launch URI | `/smart/launch.html` |
| Redirect URI | `/smart/app.html` |
| 認証方式 | OAuth 2.0 with PKCE |

### 要求する権限スコープ（Scopes）

```
launch
patient/MedicationRequest.read
patient/MedicationStatement.read
openid
fhirUser
```

### 医薬品マッピングフロー

<div style="display: flex; flex-direction: column; align-items: center; gap: 0; margin: 2rem 0;">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600; text-align: center;">
    EHR MedicationRequest
  </div>
  <div style="width: 2px; height: 24px; background: #667eea;"></div>
  <div style="width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-top: 10px solid #667eea;"></div>

  <div style="background: #f8f9fa; border: 2px solid #e0e0e0; padding: 12px 24px; border-radius: 8px; text-align: center; margin-top: -5px;">
    <strong>1. RxCUI 抽出</strong><br>
    <span style="color: #666; font-size: 0.9rem;">RxNorm 医薬品コード</span>
  </div>
  <div style="width: 2px; height: 16px; background: #e0e0e0;"></div>
  <div style="width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 8px solid #e0e0e0;"></div>

  <div style="background: #f8f9fa; border: 2px solid #e0e0e0; padding: 12px 24px; border-radius: 8px; text-align: center; margin-top: -5px;">
    <strong>2. RxNorm API</strong><br>
    <span style="color: #666; font-size: 0.9rem;">医薬品成分名を取得</span>
  </div>
  <div style="width: 2px; height: 16px; background: #e0e0e0;"></div>
  <div style="width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 8px solid #e0e0e0;"></div>

  <div style="background: #f8f9fa; border: 2px solid #e0e0e0; padding: 12px 24px; border-radius: 8px; text-align: center; margin-top: -5px;">
    <strong>3. 名前正規化</strong><br>
    <span style="color: #666; font-size: 0.9rem;">塩類接尾辞の削除、同義語マッチング</span>
  </div>
  <div style="width: 2px; height: 16px; background: #e0e0e0;"></div>
  <div style="width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 8px solid #e0e0e0;"></div>

  <div style="background: #f8f9fa; border: 2px solid #e0e0e0; padding: 12px 24px; border-radius: 8px; text-align: center; margin-top: -5px;">
    <strong>4. Fuse.js ファジーマッチング</strong><br>
    <span style="color: #666; font-size: 0.9rem;">JpTxGNN データベースとマッチング</span>
  </div>
  <div style="width: 2px; height: 24px; background: #28a745;"></div>
  <div style="width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-top: 10px solid #28a745;"></div>

  <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600; text-align: center; margin-top: -5px;">
    ドラッグリポジショニング候補を表示
  </div>
</div>

---

## FHIR API

JpTxGNN は静的 FHIR API を提供し、他のシステムが医薬品予測データを照会できます。

### エンドポイント

| エンドポイント | 説明 |
|------|------|
| `/fhir/metadata` | CapabilityStatement |
| `/fhir/MedicationKnowledge/{id}.json` | 単一医薬品リソース |
| `/fhir/Bundle/all-predictions.json` | 全予測結果 |

### 例

```bash
# Famotidine の医薬品知識リソースを取得
curl https://jptxgnn.yao.care/fhir/MedicationKnowledge/famotidine.json
```

---

## テスト環境

### SMART Health IT Launcher でテスト

1. [SMART Launcher](https://launch.smarthealthit.org/) に移動
2. 設定：
   - **Launch Type**: Provider EHR Launch
   - **FHIR Version**: R4
   - **App Launch URL**: `https://jptxgnn.yao.care/smart/launch.html`
3. テスト患者を選択
4. Launch をクリックしてテスト開始

### サポートされる EHR システム

理論上、SMART on FHIR R4 標準に準拠するすべての EHR システムをサポートします：

- Epic
- Cerner (Oracle Health)
- Allscripts
- その他 FHIR R4 互換システム

---

## プライバシーとセキュリティ

- **データ保存なし**：アプリケーションはサーバー側で患者データを保存しません
- **純フロントエンド処理**：すべてのデータ処理はブラウザ内で行われます
- **PKCE 保護**：OAuth 2.0 PKCE フローで認証を保護
- **最小権限**：必要な読み取り権限のみを要求

詳細は[プライバシーポリシー](/privacy-policy/)を参照してください。

---

## 関連リンク

- [SMART on FHIR 公式ドキュメント](http://docs.smarthealthit.org/)
- [HL7 FHIR 仕様](https://www.hl7.org/fhir/)
- [RxNorm API ドキュメント](https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html)
