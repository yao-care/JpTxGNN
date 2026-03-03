---
layout: default
title: 使用ガイド
parent: SMART on FHIR
nav_order: 1
description: "図解チュートリアル：JpTxGNN SMART App で電子カルテシステムから用薬を読み取り、ドラッグリポジショニング候補を検索する方法"
permalink: /smart/guide/
---

# SMART on FHIR 使用ガイド

<p class="key-answer" data-question="JpTxGNN SMART App の使い方は？">
JpTxGNN SMART App は、電子カルテシステム（EHR）から患者の用薬を読み取り、ドラッグリポジショニング候補を自動検索できます。本ガイドでは 2 つの使用方法を説明します：<strong>スタンドアロンテストモード</strong>（初心者向け）と <strong>SMART Launcher テスト</strong>。
</p>

---

## 🏥 医療機関との統合テスト歓迎

<p class="key-answer" data-question="JpTxGNN を病院のシステムに統合するには？">
貴院の EHR システムが SMART on FHIR をサポートしている場合、以下の方法で統合テストを行えます。IT チームが接続を迅速に検証できるよう、2 つのテストモードを提供しています。
</p>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
  <div style="padding: 1.5rem; background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-radius: 12px; border: 2px solid #4caf50;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
    <strong style="font-size: 1.1rem; color: #2e7d32;">方法 1：スタンドアロンテストモード</strong>
    <p style="color: #555; margin: 0.5rem 0 1rem;">EHR 接続不要、医薬品名を直接入力して機能をテスト</p>
    <span style="display: inline-block; padding: 4px 12px; background: #4caf50; color: white; border-radius: 16px; font-size: 0.85rem;">クイック体験</span>
  </div>
  <div style="padding: 1.5rem; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-radius: 12px; border: 2px solid #2196f3;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔗</div>
    <strong style="font-size: 1.1rem; color: #1565c0;">方法 2：SMART Launcher テスト</strong>
    <p style="color: #555; margin: 0.5rem 0 1rem;">完全な OAuth 認証フローと EHR 統合をテスト</p>
    <span style="display: inline-block; padding: 4px 12px; background: #2196f3; color: white; border-radius: 16px; font-size: 0.85rem;">IT 統合検証</span>
  </div>
</div>

---

## 方法 1：スタンドアロンテストモード

<p class="key-answer" data-question="スタンドアロンテストモードの使い方は？">
スタンドアロンテストモードでは、EHR システムに接続せずに、医薬品名を直接入力して JpTxGNN の医薬品マッピングとドラッグリポジショニング検索機能をテストできます。
</p>

### ステップ 1：スタンドアロンテストページを開く

<div style="background: #f8f9fa; border-radius: 8px; padding: 1.5rem; margin: 1rem 0;">
  <p style="margin-bottom: 1rem;">下のボタンをクリックしてスタンドアロンテストページを開きます：</p>
  <div style="display: flex; flex-wrap: wrap; gap: 12px;">
    <a href="{{ '/smart/standalone.html' | relative_url }}?drugs=Famotidine,Omeprazole" target="_blank" style="display: inline-block; padding: 12px 24px; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: 500;">🚀 サンプルで直接表示 ↗</a>
    <a href="{{ '/smart/standalone.html' | relative_url }}" target="_blank" style="display: inline-block; padding: 12px 24px; background: #e0e0e0; color: #333; text-decoration: none; border-radius: 8px; font-weight: 500;">空白ページを開く ↗</a>
  </div>
</div>

### ステップ 2：医薬品を表示または追加

「サンプルで直接表示」リンクで開くと、システムが自動的にサンプル医薬品をロードします。他の医薬品を手動で追加することもできます：

| 入力タイプ | 例 |
|----------|------|
| 英語学名 | Famotidine, Omeprazole, Metformin |
| 日本語名 | ファモチジン, オメプラゾール |
| RxCUI コード | 855332, 1161611 |

<div style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 1rem; margin: 1rem 0; border-radius: 0 8px 8px 0;">
  <strong>💡 ヒント：</strong>最適なマッチング結果を得るために英語学名の使用をお勧めします
</div>

### ステップ 3：ドラッグリポジショニング候補を表示

「検索」ボタンをクリックすると、システムは：

<ol class="actionable-steps">
  <li><strong>医薬品名マッピング</strong>：入力名を JpTxGNN データベースとマッチング</li>
  <li><strong>予測結果検索</strong>：その医薬品のドラッグリポジショニング候補適応症を検索</li>
  <li><strong>スコア表示</strong>：各予測にスコア（信頼度）を表示</li>
</ol>

---

## 方法 2：SMART Launcher テスト

<p class="key-answer" data-question="SMART Launcher テストの使い方は？">
SMART Launcher は、EHR システムが SMART App を起動する完全なフローをシミュレートする公式テストツールで、OAuth 2.0 認証を含みます。
</p>

### ステップ 1：SMART Launcher に移動

<div style="background: #f8f9fa; border-radius: 8px; padding: 1.5rem; margin: 1rem 0;">
  <p style="margin-bottom: 1rem;">下のリンクをクリックして、事前設定済みの SMART Launcher を開きます：</p>
  <a href="https://launch.smarthealthit.org/?launch_url=https%3A%2F%2Fjptxgnn.yao.care%2Fsmart%2Flaunch.html&launch=WzAsIiIsIiIsIkFVVE8iLDAsMCwwLCIiLCIiLCIiLCIiLCIiLCIiLCIiLDAsMSwiIl0" target="_blank" style="display: inline-block; padding: 12px 24px; background: #333; color: white; text-decoration: none; border-radius: 8px; font-weight: 500;">🚀 SMART Launcher に移動（設定済み）↗</a>
</div>

### ステップ 2：テスト患者を選択

開いた後、Launch URL は自動設定されています。次に：

1. **Select Patient(s)** セクションを展開
2. フィルター条件を使用して用薬記録のある患者を検索

<div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 1rem; margin: 1rem 0; border-radius: 0 8px 8px 0;">
  <strong>⚠️ 注意：</strong>SMART Launcher は Synthea 合成データ（米国医薬品）を使用しているため、一部の医薬品は JpTxGNN データベース（日本医薬品）と完全にマッチしない場合があります。
</div>

### ステップ 3：起動と認証

1. **Launch** ボタンをクリック
2. ページが JpTxGNN SMART App にリダイレクト
3. 認証ページが表示されたら **Authorize** をクリック
4. システムが自動的に患者の用薬を読み取り、ドラッグリポジショニング候補を表示

---

## フロー比較

| 比較項目 | 🎯 スタンドアロンモード | 🔗 SMART Launcher |
|----------|------------------------|-------------------|
| 接続必要 | ❌ 不要 | ✅ 必要 |
| OAuth 認証 | ❌ テストなし | ✅ 完全テスト |
| 医薬品ソース | 手動入力 | EHR 自動読み取り |
| マッチング率 | ✅ 高（指定可能） | ⚠️ 低（米国医薬品） |
| 対象者 | 一般ユーザー | 開発者 / IT 担当者 |

---

## よくある質問

### 一部の医薬品が「マッチ不可」と表示されるのはなぜですか？

JpTxGNN データベースは主に**日本医療用医薬品**を対象としていますが、SMART Launcher は**米国 Synthea 合成データ**を使用しています。一部の医薬品名が異なるか、日本で未承認のため、マッチできない場合があります。

**解決策**：スタンドアロンテストモードを使用し、JpTxGNN データベース内の医薬品名を直接入力してください。

### 正式な EHR システムでの使用方法は？

EHR システム管理者に連絡し、以下の情報を提供して設定してください：

| 項目 | 値 |
|------|------|
| Launch URL | `https://jptxgnn.yao.care/smart/launch.html` |
| Redirect URI | `https://jptxgnn.yao.care/smart/app.html` |
| Client ID | `jptxgnn-smart-app` |
| Scopes | `launch patient/MedicationRequest.read openid fhirUser` |

### 患者データは安全ですか？

はい。JpTxGNN SMART App は：
- 患者データを**保存しません**
- すべての処理は**ブラウザ側**で行われます
- **PKCE** で OAuth フローを保護
- **最小限の権限**のみを要求

---

## 技術文書

より詳細な技術仕様が必要な場合は、以下を参照してください：

<div style="margin: 1rem 0;">
  <a href="{{ '/smart/' | relative_url }}" style="display: inline-block; padding: 10px 20px; background: #f5f5f5; color: #333; text-decoration: none; border-radius: 8px; border: 1px solid #e0e0e0;">📚 SMART on FHIR 技術文書</a>
</div>

---

<div class="disclaimer">
<strong>免責事項</strong><br>
本ウェブサイトのコンテンツは研究参考のみを目的としており、専門的な医療アドバイスに代わるものではありません。すべてのドラッグリポジショニング予測結果は、臨床検証を経て初めて適用できます。健康上の問題がある場合は、資格のある医療専門家にご相談ください。
</div>
