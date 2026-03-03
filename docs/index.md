---
layout: default
title: ドラッグリポジショニング検証報告
nav_order: 1
description: "AI を用いて日本医療用医薬品の潜在的新適応症を予測。3,824 種の医薬品に対する 155,638 件の予測候補を提供。"
permalink: /
image: /assets/images/og-default.png
---

# ドラッグリポジショニング、データからエビデンスへ

<p class="key-answer" data-question="JpTxGNN ドラッグリポジショニング検証報告とは？">
<strong>JpTxGNN</strong> は、ハーバード大学 TxGNN モデルに基づくドラッグリポジショニング予測プラットフォームです。AI により <strong>155,638</strong> 件のドラッグリポジショニング候補を予測し、<strong>3,824</strong> 種の日本医療用医薬品に対して予測から検証までの完全なレポートを提供します。
</p>

<div class="key-takeaway">
「有効かもしれない」だけでなく、「エビデンスはどこにあるか」までお伝えします。予測スコアと信頼度により、研究者が迅速に候補を評価できます。
</div>

<p style="margin-top: 1.5rem;">
  <a href="{{ '/drugs/' | relative_url }}" style="display: inline-block; padding: 0.75rem 1.5rem; background: #2E7D32; color: white; text-decoration: none; border-radius: 4px; font-weight: 600; margin-right: 0.5rem;">医薬品を検索</a>
  <a href="{{ '/methodology/' | relative_url }}" style="display: inline-block; padding: 0.75rem 1.5rem; background: #f5f5f5; color: #333; text-decoration: none; border-radius: 4px; font-weight: 500;">方法論を見る</a>
</p>

---

## 医薬品検索

<p class="key-answer" data-question="医薬品や疾患のドラッグリポジショニング可能性をどのように検索しますか？">
<strong>医薬品名</strong>または<strong>疾患名</strong>を入力して、ドラッグリポジショニングの可能性を検索できます。英語学名、日本語商品名、疾患キーワードに対応。
</p>

<div class="drug-lookup-container">
  <div class="lookup-search-box">
    <div class="lookup-input-wrapper">
      <input type="text" id="lookup-input" placeholder="医薬品名または疾患名を入力..." autocomplete="off">
      <button id="lookup-clear" class="lookup-clear-btn" style="display: none;">✕</button>
    </div>
    <button id="lookup-search" class="lookup-search-btn">検索</button>
  </div>
  <div class="lookup-filters">
    <span class="filter-label">スコア：</span>
    <label><input type="checkbox" class="level-filter" value="99" checked> 99%+</label>
    <label><input type="checkbox" class="level-filter" value="95" checked> 95%+</label>
    <label><input type="checkbox" class="level-filter" value="90" checked> 90%+</label>
  </div>
  <div id="lookup-results" class="lookup-results"></div>
</div>

<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.0.0"></script>
<script>
  window.JPTXGNN_CONFIG = {
    searchIndexUrl: '{{ "/data/search-index.json" | relative_url }}',
    drugsBaseUrl: '{{ "/drugs/" | relative_url }}'
  };
</script>
<script src="{{ '/assets/js/drug-lookup.js' | relative_url }}"></script>

---

## 私たちの差別化

<p class="key-answer" data-question="JpTxGNN と他の予測ツールの違いは？">
多くのドラッグリポジショニング予測ツールは「有効かもしれない」というスコアのみを提供し、研究者は自ら臨床エビデンスを探す必要があります。JpTxGNN は異なります：各予測について TxGNN 知識グラフと深層学習モデルの両方からスコアを統合し、エビデンスレベルとともに提示します。
</p>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin: 1.5rem 0;">
  <div style="padding: 1.5rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #2E7D32;">
    <strong style="font-size: 1.1rem;">KG + DL 二重予測</strong><br>
    <span style="color: #666;">知識グラフ法と深層学習法の両方で予測。DL スコアにより予測の信頼度を定量化。</span>
  </div>
  <div style="padding: 1.5rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #1976D2;">
    <strong style="font-size: 1.1rem;">日本医薬品に特化</strong><br>
    <span style="color: #666;">SSK 医療用医薬品データと KEGG 薬効情報を統合。PMDA 許可医薬品に対応。</span>
  </div>
  <div style="padding: 1.5rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #FB8C00;">
    <strong style="font-size: 1.1rem;">FHIR R4 準拠 API</strong><br>
    <span style="color: #666;">HL7 FHIR R4 標準に準拠した API を提供。医療システムとの統合が容易。</span>
  </div>
  <div style="padding: 1.5rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #9B59B6;">
    <strong style="font-size: 1.1rem;">オープンソース</strong><br>
    <span style="color: #666;">すべてのコードとデータは GitHub で公開。研究コミュニティへの貢献を歓迎。</span>
  </div>
</div>

---

## 予測統計

<style>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}
.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
}
.stat-number {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
}
.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
  margin-top: 0.5rem;
}
</style>

<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-number">3,824</div>
    <div class="stat-label">対象医薬品</div>
  </div>
  <div class="stat-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
    <div class="stat-number">142</div>
    <div class="stat-label">DrugBank マッピング</div>
  </div>
  <div class="stat-card" style="background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);">
    <div class="stat-number">155,638</div>
    <div class="stat-label">統合予測候補</div>
  </div>
  <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
    <div class="stat-number">90%+</div>
    <div class="stat-label">信頼度閾値</div>
  </div>
</div>

---

## クイックナビゲーション

| 分類 | 説明 | リンク |
|------|------|------|
| **医薬品検索** | 3,824 種の医薬品（検索可能） | [医薬品リスト]({{ '/drugs/' | relative_url }}) |
| **SMART on FHIR** | EHR システム統合 | [SMART App]({{ '/smart/' | relative_url }}) |
| **FHIR API** | プログラムによるアクセス | [API 仕様]({{ '/fhir-api/' | relative_url }}) |
| **データダウンロード** | CSV / JSON 形式 | [ダウンロード]({{ '/downloads/' | relative_url }}) |
| **意見・フィードバック** | 問題報告、機能提案 | [GitHub Issues](https://github.com/yao-care/JpTxGNN/issues/new/choose) |

---

## 本プロジェクトについて

<p class="key-answer" data-question="JpTxGNN はどのような技術で予測を行っていますか？">
本システムは、ハーバード大学 Zitnik Lab が <em>Nature Medicine</em> に発表した <a href="https://www.nature.com/articles/s41591-024-03233-x">TxGNN</a> 深層学習モデルを使用し、日本医療用医薬品の潜在的新適応症を予測します。
</p>

<blockquote class="expert-quote">
「TxGNN は、臨床医向けに設計された初のドラッグリポジショニング基盤モデルであり、知識グラフと深層学習を統合して、希少疾患に対する薬物の潜在的効果を予測します。」
<cite>— Huang et al., Nature Medicine (2024)</cite>
</blockquote>

### データ規模

| 項目 | 数量 |
|------|------|
| 医薬品レポート | 3,824 件 |
| KG 予測候補 | 33,901 件 |
| DL 予測候補 | 2,419,822 件 |
| 統合予測（≥90%） | 155,638 件 |

### 予測フロー

<ol class="actionable-steps">
<li><strong>データ収集</strong>：SSK 医療用医薬品 + KEGG 薬効情報を統合</li>
<li><strong>DrugBank マッピング</strong>：成分名を DrugBank ID にマッピング</li>
<li><strong>KG 予測</strong>：TxGNN 知識グラフから既知の関係を抽出</li>
<li><strong>DL 予測</strong>：深層学習モデルで新規関係を予測</li>
<li><strong>統合・フィルタリング</strong>：信頼度 ≥90% の予測を抽出</li>
</ol>

[詳細を見る]({{ '/about/' | relative_url }}) | [方法論]({{ '/methodology/' | relative_url }}) | [データソース]({{ '/sources/' | relative_url }})

---

## データソース

<p class="key-answer" data-question="JpTxGNN のデータソースは何ですか？">
本プラットフォームは複数の権威ある公開データソースを統合し、予測結果のトレーサビリティと学術的価値を確保しています。
</p>

<style>
.data-source-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
}
.data-source-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.25rem 1rem;
  background: white;
  border-radius: 10px;
  text-decoration: none;
  color: #333;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}
.data-source-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.data-source-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  padding: 10px;
}
.data-source-card strong {
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}
.data-source-card small {
  font-size: 0.75rem;
  color: #666;
  text-align: center;
}
</style>

<div class="data-source-grid">
  <a href="https://zitniklab.hms.harvard.edu/projects/TxGNN/" target="_blank" rel="noopener" class="data-source-card">
    <div class="data-source-icon" style="background: #FDE8E8;">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#A51C30" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="3"/>
        <circle cx="12" cy="5" r="1.5"/>
        <circle cx="19" cy="12" r="1.5"/>
        <circle cx="12" cy="19" r="1.5"/>
        <circle cx="5" cy="12" r="1.5"/>
        <line x1="12" y1="9" x2="12" y2="6.5"/>
        <line x1="15" y1="12" x2="17.5" y2="12"/>
        <line x1="12" y1="15" x2="12" y2="17.5"/>
        <line x1="9" y1="12" x2="6.5" y2="12"/>
      </svg>
    </div>
    <strong style="color: #A51C30;">TxGNN</strong>
    <small>Harvard Zitnik Lab</small>
  </a>
  <a href="https://go.drugbank.com/" target="_blank" rel="noopener" class="data-source-card">
    <div class="data-source-icon" style="background: #FDEDEC;">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#E74C3C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10.5 2.5a2.5 2.5 0 0 1 3 0l6.5 5.2a2.5 2.5 0 0 1 1 2v4.6a2.5 2.5 0 0 1-1 2l-6.5 5.2a2.5 2.5 0 0 1-3 0l-6.5-5.2a2.5 2.5 0 0 1-1-2V9.7a2.5 2.5 0 0 1 1-2l6.5-5.2z"/>
        <line x1="12" y1="8" x2="12" y2="16"/>
        <line x1="8" y1="12" x2="16" y2="12"/>
      </svg>
    </div>
    <strong style="color: #E74C3C;">DrugBank</strong>
    <small>医薬品データベース</small>
  </a>
  <a href="https://www.kegg.jp/kegg/drug/" target="_blank" rel="noopener" class="data-source-card">
    <div class="data-source-icon" style="background: #E8F5E9;">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#388E3C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2L4 6v6c0 5.5 3.4 10.3 8 12 4.6-1.7 8-6.5 8-12V6l-8-4z"/>
        <polyline points="9 12 11 14 15 10"/>
      </svg>
    </div>
    <strong style="color: #388E3C;">KEGG DRUG</strong>
    <small>薬効情報</small>
  </a>
  <a href="https://www.pmda.go.jp/" target="_blank" rel="noopener" class="data-source-card">
    <div class="data-source-icon" style="background: #E3F2FD;">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
        <line x1="9" y1="9" x2="15" y2="9"/>
        <line x1="9" y1="13" x2="15" y2="13"/>
        <line x1="9" y1="17" x2="13" y2="17"/>
      </svg>
    </div>
    <strong style="color: #1565C0;">SSK</strong>
    <small>医療用医薬品</small>
  </a>
</div>

---

<div class="disclaimer">
<strong>免責事項</strong><br>
本レポートは学術研究参考のみを目的としており、<strong>医療アドバイスを構成するものではありません</strong>。医薬品の使用は医師の指示に従ってください。ドラッグリポジショニングの決定には、完全な臨床検証と規制審査が必要です。
<br><br>
<small>最終更新：2026-03-03 | 審査者：JpTxGNN Research Team</small>
</div>
