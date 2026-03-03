---
layout: default
title: 説明
nav_order: 7
has_children: true
description: "JpTxGNN の方法論、使用ガイド、プロジェクト情報"
permalink: /help/
---

# 説明

<p class="key-answer" data-question="JpTxGNN の説明セクションとは？">
JpTxGNN プロジェクトの方法論、使用方法、プロジェクト情報、プライバシーポリシーなどの説明ドキュメントを提供しています。
</p>

---

## ドキュメント一覧

<style>
.help-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}
.help-card {
  display: flex;
  align-items: center;
  padding: 1.25rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
  border-left: 5px solid;
}
.help-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.help-card.methodology { border-color: #1565C0; }
.help-card.guide { border-color: #2E7D32; }
.help-card.about { border-color: #7B1FA2; }
.help-card.privacy { border-color: #E65100; }

.help-card-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  flex-shrink: 0;
  font-size: 1.5rem;
}
.help-card.methodology .help-card-icon { background: #E3F2FD; }
.help-card.guide .help-card-icon { background: #E8F5E9; }
.help-card.about .help-card-icon { background: #F3E5F5; }
.help-card.privacy .help-card-icon { background: #FFF3E0; }

.help-card-info {
  flex: 1;
}
.help-card-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #333;
}
.help-card-desc {
  font-size: 0.8rem;
  color: #666;
}
</style>

<div class="help-cards">
  <a href="{{ '/methodology/' | relative_url }}" class="help-card methodology">
    <div class="help-card-icon">🔬</div>
    <div class="help-card-info">
      <div class="help-card-title">方法論</div>
      <div class="help-card-desc">TxGNN モデルと予測手法の詳細</div>
    </div>
  </a>

  <a href="{{ '/guide/' | relative_url }}" class="help-card guide">
    <div class="help-card-icon">📖</div>
    <div class="help-card-info">
      <div class="help-card-title">使用ガイド</div>
      <div class="help-card-desc">本サイトの使用方法</div>
    </div>
  </a>

  <a href="{{ '/about/' | relative_url }}" class="help-card about">
    <div class="help-card-icon">💡</div>
    <div class="help-card-info">
      <div class="help-card-title">プロジェクトについて</div>
      <div class="help-card-desc">JpTxGNN プロジェクトの概要</div>
    </div>
  </a>

  <a href="{{ '/privacy-policy/' | relative_url }}" class="help-card privacy">
    <div class="help-card-icon">🔒</div>
    <div class="help-card-info">
      <div class="help-card-title">プライバシーポリシー</div>
      <div class="help-card-desc">個人情報の取り扱いについて</div>
    </div>
  </a>
</div>

---

## よくある質問

### このサイトの目的は何ですか？

JpTxGNN は、日本 PMDA 承認医薬品のドラッグリポジショニング（既存薬再利用）候補を探索するための研究支援ツールです。AI/ML 技術を活用して、既存の医薬品の新しい治療適応症を予測します。

### データはどこから来ていますか？

| カテゴリ | ソース |
|----------|--------|
| **薬物データ** | 日本 SSK 医療用医薬品、KEGG データベース |
| **予測モデル** | Harvard TxGNN 知識グラフおよび深層学習モデル |
| **エビデンス** | PubMed、ClinicalTrials.gov |
| **安全性情報** | DDInter 2.0（開発中） |

### 臨床で使用できますか？

<div style="background: #ffebee; padding: 1rem; border-left: 4px solid #f44336; border-radius: 4px; margin: 1rem 0;">
<strong>重要</strong>: 本サイトの情報は研究参考用であり、医療アドバイスを構成するものではありません。すべての候補薬は臨床検証を経る必要があります。
</div>

### 予測スコアの意味は？

TxGNN スコアは、医薬品と疾患のペアに対するモデルの予測信頼度を表します：

| 閾値 | 意味 |
|------|------|
| ≥ 99% | 非常に高い信頼度 |
| ≥ 90% | 高い信頼度 |
| ≥ 50% | 中程度の信頼度 |
| < 50% | 低い信頼度 |

### FHIR API はどのように使用できますか？

JpTxGNN は HL7 FHIR R4 準拠の API を提供しています。詳細は [FHIR API 仕様]({{ '/smart/api-spec/' | relative_url }}) をご参照ください。

---

## お問い合わせ

- **GitHub**: [github.com/yao-care/JpTxGNN](https://github.com/yao-care/JpTxGNN)
- **Issues**: バグ報告や機能リクエストは GitHub Issues へ

---

## 免責事項

<div class="disclaimer">
<strong>重要なお知らせ</strong><br>
本サイトの情報は研究参考目的のみで提供されており、医療アドバイスを構成するものではありません。臨床的な判断や治療方針の決定は、必ず医療専門家にご相談ください。
</div>
