---
layout: default
title: 統合可能アプリケーション評価
parent: SMART on FHIR
nav_order: 5
description: JpTxGNN と統合可能な医療アプリケーションの評価と分析
permalink: /smart/integration-candidates/
---

# 統合可能アプリケーション評価

本ページでは、JpTxGNN との統合が有望な医療アプリケーションを評価します。

---

## 評価基準

| 基準 | 説明 | 重要度 |
|------|------|--------|
| FHIR 対応 | FHIR R4 サポート | 必須 |
| CDS Hooks | CDS Hooks サポート | 高 |
| オープンソース | コード公開状況 | 中 |
| 日本市場 | 日本での展開状況 | 中 |
| 用薬データ | MedicationRequest 対応 | 必須 |

---

## 統合候補一覧

### EHR システム

| システム | FHIR | CDS Hooks | 評価 |
|---------|------|-----------|------|
| Epic | R4 | ✅ | ⭐⭐⭐⭐⭐ |
| Cerner | R4 | ✅ | ⭐⭐⭐⭐⭐ |
| Allscripts | R4 | 部分的 | ⭐⭐⭐⭐ |
| 日本国内システム | 検討中 | - | ⭐⭐⭐ |

### CDS サービス

| サービス | 説明 | 統合可能性 |
|---------|------|-----------|
| CDS Hooks Sandbox | テスト環境 | 高 |
| Inferno Test Suite | 互換性テスト | 高 |

### データ分析ツール

| ツール | 説明 | 統合可能性 |
|---------|------|-----------|
| Jupyter Notebooks | データ分析 | 中 |
| R Shiny | ダッシュボード | 中 |

---

## 統合パターン

### パターン 1: SMART App Launch

```
EHR → SMART Launch → JpTxGNN App → 結果表示
```

**適用場面**: 臨床医がカルテを見ながら確認

### パターン 2: CDS Hooks

```
EHR イベント → CDS Hook → JpTxGNN CDS Service → カード表示
```

**適用場面**: 処方時に自動的に提案

### パターン 3: バッチ処理

```
EHR FHIR API → バッチ取得 → JpTxGNN 分析 → レポート出力
```

**適用場面**: 研究目的での一括分析

---

## 次のステップ

1. **Epic Sandbox でのテスト** - Epic Open.fhir での動作確認
2. **日本市場調査** - 国内 EHR ベンダーとの連携可能性
3. **CDS Service 開発** - CDS Hooks 対応サービスの実装

---

## 関連ドキュメント

- [SMART on FHIR 技術文書]({{ '/smart/technical-docs/' | relative_url }})
- [CDS Hooks アーキテクチャ設計]({{ '/smart/cds-hooks-architecture/' | relative_url }})
