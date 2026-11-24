---
layout: default
title: Tizanidine
parent: 高エビデンスレベル
nav_order: 309
evidence_level: L2
indication_count: 5
monitor_inn: "Tizanidine"
predicted_indications: ["migraine disorder", "migraine with brainstem aura", "atrophoderma vermiculata", "Tourette syndrome", "ulerythema ophryogenesis"]
last_modified_at: 2026-11-24
description: "Tizanidine：予測新適応症は片頭痛 (migraine disorder)（エビデンスレベル L2）。既存適応症：脊髄小脳変性症、多発性硬化症、筋萎縮性側索硬化症（鎮痙薬・筋弛緩薬）"
---

# Tizanidine
{: .fs-9 }

エビデンスレベル: **L2** | 予測適応症: **5** 件
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

## チザニジン：脊髄小脳変性症・多発性硬化症・筋萎縮性側索硬化症にともなう痙縮から片頭痛へ
{: .text-alpha }

## 一言要約

チザニジンはα2アドレナリン受容体作動性の鎮痙薬・筋弛緩薬で、元々は脊髄小脳変性症、多発性硬化症、筋萎縮性側索硬化症に関連する痙縮の治療に使用されていました。
TxGNN モデルは**片頭痛 (migraine disorder)** に有効である可能性を予測しており、現在 **Phase 3 試験 1 件（結果未公開）**と**文献 17 編**（慢性連日性頭痛を対象としたプラセボ対照二重盲検 RCT 1 件を含む）がこの方向性を支持しています。

## クイック概要

| 項目 | 内容 |
|------|------|
| 既存適応症 | 脊髄小脳変性症、多発性硬化症、筋萎縮性側索硬化症（鎮痙薬・筋弛緩薬） |
| 予測新規適応症 | 片頭痛 (migraine disorder) |
| TxGNN 予測スコア | 0.9979 |
| エビデンスレベル | L2 |
| 日本市販状況 | 販売中（有効な承認 9 件／全 10 件） |
| 承認番号数 | 10 件（有効 9 件） |
| 推奨決定 | Proceed with Guardrails |

## この予測が妥当である理由

米国 FDA が承認した Tizanidine の添付文書（Prescribing Information）の「Mechanism of Action」の項によると（非公式訳）、「チザニジンは中枢性α2アドレナリン受容体作動薬であり、運動ニューロンのシナプス前抑制を増強することにより痙縮を軽減すると推定される。チザニジンの作用は多シナプス経路において最も大きい。これらの作用の全体的な効果として、脊髄運動ニューロンの促通が減少すると考えられている。」英語原文："Tizanidine is a central alpha-2-adrenergic receptor agonist and presumably reduces spasticity by increasing presynaptic inhibition of motor neurons. The effects of tizanidine are greatest on polysynaptic pathways. The overall effect of these actions is thought to reduce facilitation of spinal motor neurons."（[DailyMed: Zanaflex (tizanidine hydrochloride) prescribing information, Legacy Pharma USA, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=60c27d35-7349-4fc6-86ad-70fffdbe3e08)、版 2026-01-02、参照日 2026-11-19）。既知の情報によると、チザニジンは中枢性のα2アドレナリン受容体作動薬で、脊髄での反射亢進や筋緊張を抑える薬剤です。

片頭痛と痙縮は一見異なる疾患です。ただし、チザニジンは三叉神経系や脳幹での痛み伝達を抑え、筋緊張を和らげる可能性があります。この点が、頭痛や片頭痛の予防に役立つと考えられています。

実際に、慢性連日性頭痛の予防を対象とした二重盲検プラセボ対照試験や、複数のレビューでチザニジンが予防薬候補として取り上げられています。ただし、これらは主に慢性連日性頭痛（慢性片頭痛、緊張型頭痛を含む）を対象とした知見です。純粋な片頭痛への有効性は、今後の検証が必要です。

## 臨床試験エビデンス

| 試験番号 | フェーズ | 状態 | 被験者数 | 主な知見 |
|---------|--------|------|----------|---------|
| [NCT05484349](https://clinicaltrials.gov/study/NCT05484349) | Phase 3 | 不明 | 189 | 成人の反復性片頭痛発作予防における塩酸チザニジン経口投与の有効性・安全性・忍容性を評価する多施設共同無作為化二重盲検プラセボ対照試験（2023年6月開始、完了予定 2025年12月）。結果は未公開 |
| [NCT02403687](https://clinicaltrials.gov/study/NCT02403687) | N/A | 完了 | 300 | 外用 NSAIDs による疼痛緩和の24週間観察研究。チザニジン・片頭痛に特化した設計ではなく、間接的な示唆にとどまる |

## 文献エビデンス

| PMID | 年 | タイプ | ジャーナル | 主な知見 |
|------|-----|------|------|---------|
| [12167135](https://pubmed.ncbi.nlm.nih.gov/12167135/) | 2002 | RCT | Headache | 慢性連日性頭痛（慢性片頭痛、片頭痛様頭痛、緊張型頭痛）に対する補助的予防療法としてのチザニジンとプラセボを比較する二重盲検多施設試験 |
| [12696998](https://pubmed.ncbi.nlm.nih.gov/12696998/) | 2003 | Review | CNS Drugs | バクロフェン、チザニジン、ボツリヌス毒素Aなど筋緊張に作用する薬剤の、片頭痛・緊張型頭痛予防への役割を検討 |
| [17115988](https://pubmed.ncbi.nlm.nih.gov/17115988/) | 2006 | Review | Headache | 慢性連日性頭痛の予防治療。チザニジンは検討された薬剤の一つ |
| [15115635](https://pubmed.ncbi.nlm.nih.gov/15115635/) | 2004 | Review | Current Pain and Headache Reports | 片頭痛予防の新たな選択肢として、チザニジンを含む複数の薬剤を概説 |
| [20464578](https://pubmed.ncbi.nlm.nih.gov/20464578/) | 2010 | Review | Neurological Sciences | 慢性片頭痛の薬物予防に関する二重盲検プラセボ対照試験のレビュー |
| [31365643](https://pubmed.ncbi.nlm.nih.gov/31365643/) | 2019 | Review | Arquivos de Neuro-Psiquiatria | ブラジル頭痛学会による慢性片頭痛治療のコンセンサス |
| [11318882](https://pubmed.ncbi.nlm.nih.gov/11318882/) | 2001 | 非盲検試験 | Headache | 慢性連日性頭痛の予防におけるチザニジン錠の用量漸増非盲検試験（有効性・忍容性） |
| [11903539](https://pubmed.ncbi.nlm.nih.gov/11903539/) | 2002 | 臨床報告 | Headache | 低用量チザニジンと NSAIDs を併用した、鎮痛薬反跳頭痛からの離脱療法 |
| [40983294](https://pubmed.ncbi.nlm.nih.gov/40983294/) | 2025 | In vitro | Journal of Controlled Release | チザニジンとメロキシカムの超分子自己組織化による抗片頭痛効果の相乗的増強 |
| [23293866](https://pubmed.ncbi.nlm.nih.gov/23293866/) | 2013 | レビュー | Headache | 慢性片頭痛管理へのアプローチ。チザニジンは選択肢の一つとして言及 |

## 日本市販情報

<!-- licenses:begin -->

| 医薬品コード | 医薬品名・規格名 | 状態 |
|------|------|------|
| 611240378 | テルネリン錠１ｍｇ | 有効 |
| 611240463 | テルネリン顆粒０．２％ | 有効 |
| 620194001 | チザニジン錠１ｍｇ「サワイ」 | 有効 |
| 620194201 | チザニジン錠１ｍｇ「テバ」 | 薬価削除（2026-09-30、後継コード 622717500） |
| 621228112 | チザニジン錠１ｍｇ「日医工」 | 有効 |

上表はデータ上の 10 件のうち 5 件です。

<!-- licenses:end -->

承認には有効なものと薬価基準から削除済みのものがあります（件数はクイック概要を参照）。

<!-- review:begin jp-lic-20261117-tizanidine-1 -->

> **確認による訂正（2026-11-17）**：元の記載は「承認は全 10 件で、10 件すべてが有効です。」でした。訂正：医薬品マスター（薬価基準収載品目）の 2026-11-12 全件ファイルでは、次の承認が経過措置期間満了などにより薬価基準から削除されています（620194201（廃止年月日 2026-09-30、後継コード 622717500））。薬価基準からの削除は承認の取消しを意味するものではなく、承認状況はこのデータでは確認できません。出典：[医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx)。

<!-- review:end jp-lic-20261117-tizanidine-1 -->

## 安全性に関する考慮事項

- **禁忌（関連疾患）**：医薬品知識グラフ上では、肝不全、腎疾患、精神疾患（精神病性障害、統合失調症様障害、統合失調感情障害）、低血圧性障害との関連が示されています。これは添付文書の記載ではなく、モデル側の関連情報です。
- **薬物相互作用**：100 件が検出されました。主なものは次のとおりです。
  - 重大（Major）：ファモチジン、シメチジン、モルヒネ、ドラセトロン、オベチコール酸
  - 中等度（Moderate）：クラリスロマイシン、レボフロキサシン、メトクロプラミド、ナルトレキソン、アトロピン、ヒヨスチアミン、ロペラミドなど

詳細は添付文書を参照してください。

## 結論と次のステップ

**決定：Proceed with Guardrails**

**理由：**
- 片頭痛に直接対応する Phase 3 のプラセボ対照試験（NCT05484349）が登録されており、慢性連日性頭痛を対象とした RCT も存在します。一方、Phase 3 試験は状態が不明で結果が未公開です。また、慢性連日性頭痛の知見を片頭痛へ外挿する点には注意が必要です。

**進める場合に必要なもの：**
- NCT05484349 の結果、または進捗状況の確認
- 添付文書（警告・禁忌）の取得と安全性評価
- 詳細な作用機序データ（MOA）の補充
- 肝・腎機能障害、低血圧、精神疾患のある患者に対する安全性モニタリング計画
- 強い相互作用薬（CYP1A2 阻害薬であるシメチジン、ファモチジンなど）の併用管理方針
- 日本での供給状況・再承認の可能性の確認

### 補足：その他の予測候補

| 予測疾患 | TxGNN スコア | エビデンスレベル | 推奨 |
|---------|-------------|----------------|------|
| 脳幹性前兆を伴う片頭痛 | 0.9971 | L5 | Research Question |
| トゥレット症候群 | 0.9917 | L5 | Hold |
| 蠕虫状萎縮性皮膚症 | 0.9931 | L5 | Hold |
| 眉毛部紅斑性毛包性角化症 | 0.9913 | L5 | Hold |

片頭痛の亜型は一般的な片頭痛予防からの推測にとどまります。皮膚疾患 2 件は機序的な裏付けがなく、モデル予測のみです。

<!-- review:begin log -->

## 確認記録

以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。

| 確認日 | 項目 | 対応 | 出典 |
|------|------|------|------|
| 2026-11-17 | 訂正：承認の件数・状態を医薬品マスターの最新収載状況に合わせました | 訂正（2026-11-24 改訂、旧版は記録に保存） | [医薬品マスター（全件ファイル y_ALL20261112.zip・改定分ファイル）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html)；[経過措置年月日又は商品名医薬品コード使用期限一覧（令和8年度分）](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.files/keikasoti_R08_20261112.xlsx) |
| 2026-11-19 | 「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え | 作用機序データがないとする記述を、出典付きの抜粋に置き換え | [DailyMed: Zanaflex (tizanidine hydrochloride) prescribing information, Legacy Pharma USA, Inc.](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=60c27d35-7349-4fc6-86ad-70fffdbe3e08) |

<!-- review:end log -->

## 免責事項

本コンテンツは研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用の前に臨床的検証が必要です。

---

<!-- brand-names:start -->
## 日本での販売名

同じ成分を含む日本の医薬品です。以下の名称でも検索できます。

**商品名**：テルネリン

**販売名（規格別）**：チザニジン塩酸塩1mg錠、チザニジン錠1mg、テルネリン錠1mg、テルネリン顆粒0.2%
<!-- brand-names:end -->

