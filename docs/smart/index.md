---
layout: default
title: SMART on FHIR
nav_order: 2
has_children: true
description: JpTxGNN SMART on FHIR アプリケーション - EHR から用薬を読み取り、ドラッグリポジショニング候補を検索
permalink: /smart/
---

# SMART on FHIR アプリケーション

JpTxGNN は SMART on FHIR 統合を提供し、医療機関が電子カルテシステム（EHR）から患者の用薬データを読み取り、関連するドラッグリポジショニング候補を自動的に検索できます。

---

## SMART on FHIR とは？

SMART on FHIR は、医療アプリケーションが電子カルテシステムのデータに安全にアクセスできるオープン標準です。この標準により：

- アプリケーションは EHR システムから認証を取得
- 患者の用薬記録、診断などのデータを読み取り
- EHR ワークフロー内でシームレスに統合

---

## 機能特徴

| 機能 | 説明 |
|------|------|
| **患者用薬読み取り** | EHR から患者の現在の用薬リストを自動取得 |
| **医薬品マッピング** | RxNorm 薬物コードを JpTxGNN データベースにマッピング |
| **ドラッグリポジショニング検索** | 各医薬品の予測新適応症候補を表示 |
| **予測スコア表示** | 各予測のスコア（信頼度）を明示 |
| **臨床試験検索** | ClinicalTrials.gov 関連臨床試験をリアルタイム検索 |

---

## クイックスタート

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
  <div style="padding: 1.5rem; background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-radius: 12px; border: 2px solid #4caf50;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
    <strong style="font-size: 1.1rem; color: #2e7d32;">スタンドアロンテストモード</strong>
    <p style="color: #555; margin: 0.5rem 0 1rem;">EHR 接続不要、医薬品名を直接入力して機能をテスト</p>
    <a href="standalone.html" style="display: inline-block; padding: 8px 16px; background: #4caf50; color: white; text-decoration: none; border-radius: 6px; font-size: 0.9rem;">今すぐ体験 →</a>
  </div>
  <div style="padding: 1.5rem; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-radius: 12px; border: 2px solid #2196f3;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📖</div>
    <strong style="font-size: 1.1rem; color: #1565c0;">使用ガイド</strong>
    <p style="color: #555; margin: 0.5rem 0 1rem;">図解チュートリアル：JpTxGNN SMART App の使い方</p>
    <a href="guide/" style="display: inline-block; padding: 8px 16px; background: #2196f3; color: white; text-decoration: none; border-radius: 6px; font-size: 0.9rem;">ガイドを見る →</a>
  </div>
  <div style="padding: 1.5rem; background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); border-radius: 12px; border: 2px solid #ff9800;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚙️</div>
    <strong style="font-size: 1.1rem; color: #e65100;">技術文書</strong>
    <p style="color: #555; margin: 0.5rem 0 1rem;">OAuth 設定、FHIR API、医薬品マッピングフロー</p>
    <a href="technical-docs/" style="display: inline-block; padding: 8px 16px; background: #ff9800; color: white; text-decoration: none; border-radius: 6px; font-size: 0.9rem;">技術仕様 →</a>
  </div>
  <div style="padding: 1.5rem; background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-radius: 12px; border: 2px solid #9c27b0;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔗</div>
    <strong style="font-size: 1.1rem; color: #7b1fa2;">統合リソース</strong>
    <p style="color: #555; margin: 0.5rem 0 1rem;">ClinicalTrials.gov、DDI チェック、CDS Hooks</p>
    <a href="integrations/" style="display: inline-block; padding: 8px 16px; background: #9c27b0; color: white; text-decoration: none; border-radius: 6px; font-size: 0.9rem;">統合を見る →</a>
  </div>
</div>

---

## ドキュメント構成

| ページ | 説明 |
|------|------|
| [使用ガイド](guide/) | 図解チュートリアル、一般ユーザー向け |
| [技術文書](technical-docs/) | FHIR 設定、API エンドポイント、開発者向け |
| [統合リソース](integrations/) | 外部リソース統合とリンク |
| [SMART App Gallery 参考](app-gallery-reference/) | SMART App Gallery の参考情報 |
| [統合可能アプリケーション評価](integration-candidates/) | 統合候補アプリの評価 |
| [FHIR API 仕様](api-spec/) | API 仕様の詳細 |
| [Project Introduction (English)](project-intro-en/) | 英語版プロジェクト紹介 |
| [ClinicalTrials.gov API v2 技術ノート](clinicaltrials-api-notes/) | CT.gov API 技術メモ |
| [CQL 構文学習ノート](cql-notes/) | Clinical Quality Language ノート |
| [HL7 PDDI-CDS IG 技術ノート](pddi-cds-notes/) | 薬物相互作用 CDS ノート |
| [CDS Hooks アーキテクチャ設計](cds-hooks-architecture/) | CDS Hooks 設計パターン |

---

## 免責事項

<div style="background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 16px; margin: 20px 0;">
<strong>重要なお知らせ</strong><br>
本ウェブサイトのコンテンツは研究参考のみを目的としており、専門的な医療アドバイスに代わるものではありません。すべてのドラッグリポジショニング予測結果は、臨床検証を経て初めて適用できます。健康上の問題がある場合は、資格のある医療専門家にご相談ください。
</div>
