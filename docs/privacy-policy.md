---
layout: default
title: プライバシーポリシー
parent: 説明
nav_order: 4
description: "個人情報の取り扱いについて"
permalink: /privacy-policy/
---

# プライバシーポリシー

最終更新日: 2026年11月5日

## はじめに

JpTxGNN（以下「本サービス」）は、ユーザーのプライバシーを尊重し、
個人情報の保護に努めています。本ポリシーでは、本サービスにおける
情報の取り扱いについて説明します。

## 収集する情報

### 自動的に収集される情報

本サービスは GitHub Pages でホストされており、以下の情報が
自動的に収集される場合があります：

- IPアドレス
- ブラウザの種類
- アクセス日時
- 参照元URL

これらの情報は GitHub のプライバシーポリシーに従って処理されます。

また、本サービスは Google Analytics 4 を使用しており、分析用 Cookie によって閲覧ページ、参照元、スクロール量、ページ滞在時間などの利用状況を収集し、アクセス統計に利用します。Cookie はページの読み込み時に設定されます。検索語、フォームの内容、URL のクエリ文字列は送信しません。

### ユーザーが提供する情報

本サービスでは、ユーザーからの個人情報の入力を求めません。
検索機能はブラウザ上でローカルに実行され、サーバーには送信されません。

## 情報の利用目的

収集された情報は、以下の目的でのみ使用されます：

- サービスの提供と維持
- アクセス統計の分析
- サービスの改善

## Cookie の使用

本サービスは、Google Analytics 4 の分析用 Cookie（`_ga` など）を使用し、
アクセス統計に利用します。サイトの機能のための Cookie は使用していません。
ユーザーはブラウザの設定で Cookie を無効にすることができます。

## 第三者との情報共有

本サービスは、以下の場合を除き、収集した情報を第三者と共有しません：

- 法律で要求される場合
- ユーザーの同意がある場合
- サービス提供に必要な場合（ホスティングプロバイダー等）

## 第三者サービス

本サービスは以下の第三者サービスを利用しています：

| サービス | 目的 | プライバシーポリシー |
|----------|------|----------------------|
| GitHub Pages | ホスティング | [GitHub Privacy](https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement) |
| Google Analytics 4 (www.googletagmanager.com, google-analytics.com) | アクセス統計（閲覧ページ、参照元）。分析用 Cookie を使用します。検索語、フォームの内容、URL のクエリ文字列は送信しません。 | [Google プライバシーポリシー](https://policies.google.com/privacy) |
| cdn.jsdelivr.net | スクリプトライブラリ：全ページの d3 グラフ、SMART ページの Fuse.js（名称照合）と SMART on FHIR クライアント、トップページの医薬品検索 | [jsDelivr プライバシーポリシー](https://www.jsdelivr.com/terms/privacy-policy-jsdelivr-net) |
| clinicaltrials.gov | SMART ページの臨床試験検索：検索を指示したときだけ、医薬品名と適応症名を ClinicalTrials.gov API に送信します | [NLM ウェブポリシー](https://www.nlm.nih.gov/web_policies.html) |
| rxnav.nlm.nih.gov | SMART アプリ：電子カルテから読み取った医薬品の RxNorm コードを、成分名を調べるため米国国立医学図書館（NLM）の RxNav API に送信します（患者を特定する情報は含みません） | [NLM ウェブポリシー](https://www.nlm.nih.gov/web_policies.html) |

## データセキュリティ

本サービスは HTTPS を使用して通信を暗号化しています。
ただし、インターネット上での情報送信には固有のリスクがあり、
完全なセキュリティを保証することはできません。

## 子どものプライバシー

本サービスは、13歳未満の子どもから意図的に個人情報を収集しません。

<!-- privacy-law:start（母目錄 .claude/gen_local_pages_20261119.py 產生，勿手改；法規與連結見 .claude/privacy_text_20261119.py）-->
## 適用される法律

日本の利用者には[個人情報の保護に関する法律（個人情報保護法）](https://laws.e-gov.go.jp/law/415AC0000000057)が適用され、[個人情報保護委員会](https://www.ppc.go.jp/)が所管しています。本サイトは氏名・メールアドレス・診療記録を取得しません。関係する個人関連情報は、Google Analytics 4 が分析 Cookie で収集する閲覧統計のみで、Google が日本国外で処理します。

## あなたの権利と行使方法

- 保有個人データの開示請求（第 33 条）。
- 訂正・追加・削除の請求（第 34 条）。
- 利用停止・消去の請求（第 35 条）。分析 Cookie をブロックすれば収集も止まります。
- 個人情報保護委員会の相談窓口への相談。

請求・お問い合わせ：service@yao.care。本サイトにはアカウントがないため、Google Analytics が保有するデータについては、訪問日やページなど特定できる情報をお知らせいただいた場合に限り対応できます。分析 Cookie はブラウザでいつでもブロック・削除できます。

## 著作権とデータの出典

本サイトの文章は[著作権法](https://laws.e-gov.go.jp/law/345AC0000000048)で保護されています。 本サイトのプログラムは [GitHub リポジトリ](https://github.com/yao-care/JpTxGNN) で MIT ライセンスにより公開しています。レポート本文の著作権は藥提醒科技有限公司 (yao.care)に帰属します。

本サイトが使うデータの出典と利用条件：

- **TxGNN** の予測データ（Harvard Dataverse）：CC0 1.0（パブリックドメイン提供）。引用時は Huang et al., *Nature Medicine* 2024 を明記してください。
- **ClinicalTrials.gov**・**PubMed**：米国国立医学図書館。[ClinicalTrials.gov の利用条件](https://clinicaltrials.gov/about-site/terms-conditions)と [NCBI のポリシー](https://www.ncbi.nlm.nih.gov/home/about/policies/)を参照（PubMed の抄録には出版社の著作権が残るものがあります）。
- **DrugBank** の識別子とデータ：[DrugBank](https://go.drugbank.com/) のライセンス条件（非商用）に従います。
- **国内データセット**：[社会保険診療報酬支払基金 医薬品マスター](https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html), 社会保険診療報酬支払基金 が公開しているデータで、再利用には公開者の利用条件が適用されます。本サイトが追加の権利を許諾することはありません。

<!-- privacy-law:end -->

---

## ポリシーの変更

本ポリシーは予告なく変更される場合があります。
重要な変更がある場合は、本ページで告知します。

## お問い合わせ

本ポリシーに関するご質問は、プロジェクト概要ページの
連絡先情報を参照してください。

## 関連ページ

- [プロジェクト概要](/about/)
- [使用ガイド](/guide/)
