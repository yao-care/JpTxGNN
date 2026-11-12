"""本站查核機制的在地設定（JpTxGNN，日文；2026-11-12 建）。

程式（page_format、licenses、withdrawn、scripts/apply_drug_reviews.py、build_license_snapshot.py、reviews_from_edits.py、
check_original_indications.py）的核心流程比照 TwTxGNN／UsTxGNN，本站的字樣、規則細節、提交清單集中在這裡。
本站的許可證資料是「医薬品マスター」（薬価基準収載品目），事實層只涵蓋收載品目（checker X_SCOPE）。
「日本での販売名」區塊（apply_brand_names 產生，<!-- brand-names:start/end -->）是受管區塊，查核框不插進去。
"""
import re

SITE = "JpTxGNN"
CODE = "jp"

# ---- 頁首等級（page_format）----
OVERVIEW_LEVEL_LABELS = ["エビデンスレベル"]
HEADER_LABEL = "エビデンスレベル"
# 2026-11-12 實測：296 頁有總覽等級，頁首全部＝總覽格第一個等級（主予測），0 頁例外 → first（不照 Tw 整格取最高）。
# 列表頁標題沒有等級範圍（「高エビデンスレベル」等），parent 依檔名對應：evidence-high＝L1–L2、medium＝L3–L4、low＝L5
HEADER_RULE = "first"
HEADER_KEEP_NA = True
HEADER_EXCEPTIONS: dict = {}
WITHDRAWN_RE = re.compile(r"^\s*(\*\*)?撤回")
DESC_LEVEL_WORD = r"エビデンスレベル"
DESC_LEVEL_DEFAULT = "エビデンスレベル"
NA_DESC = "既知の用途のみ"

# ---- 許可證（licenses）----
MARKET_SECTIONS = ["日本市販情報"]

# ---- 查核框與查核紀錄表（apply_drug_reviews）----
DISCLAIMER_RE = re.compile(r"^## 免責事項", re.M)
LOG_HEAD = "## 確認記録"
LOG_COLS = "| 確認日 | 項目 | 対応 | 出典 |"
LABEL = {"correct": "確認による訂正", "annotate": "確認による注記", "rereview": "再評価待ち", "rereview_result": "再評価結果"}
ACTION = {"correct": "訂正", "annotate": "注記を追加", "rereview": "再評価待ちに設定", "section": "出典付きの節を追加",
          "rereview_result": "再評価完了", "header_level": "見出しのエビデンスレベルをクイック概要から再計算",
          "description_level": "ページ説明のエビデンスレベルを見出しに合わせて更新"}
VERDICT = {"maintain": "維持", "downgrade": "引き下げ", "upgrade": "引き上げ", "withdraw": "撤回"}
BOX_HEAD = "> **{label}（{date}）**："
ORIG_STATED = "元の記載は「{claim}」でした。"
SPACE, FULL_STOP, SENT_END = "", "。", "。！？）」"
PAREN = "（{}）"
JOIN, LIST_SEP, ITEM_SEP = "／", "；", "、"
SOURCE_WORD = "出典："
DECISION = "判断に関する提案："
TABLE_UPDATED = "このページの{labels}は再評価結果に合わせて更新しました。元の値は下の確認記録にあります。"
LEVEL_SAME = "エビデンスレベル {o} は変更なし"
LEVEL_CHANGE = "エビデンスレベル {o}→{n}"
ACT_REREVIEWED = "再評価待ち → 再評価済み（下記の再評価結果を参照）"
ACT_HEADER = "見出しのエビデンスレベルをクイック概要から再計算（{o}→{n}）"
ACT_HEADER_WD = "主予測を再評価で撤回し、見出しのエビデンスレベルを再計算（{o}→{n}）"
ACT_NA_LIST = "、「{title}」に掲載"
ACT_RESULT = "再評価：{verdict}、{change}"
ACT_TABLE = "；{label}：「{a}」→「{b}」"
ACT_DESC = "ページ説明（description）の「エビデンスレベル {o}」を「{n}」に変更（見出しのレベルに合わせたもので、他の文言は変更なし。原文は記録に保存）"
ACT_REVISED = "（{d} 改訂、旧版は記録に保存）"
ST_SUPERSEDED = "プログラム生成の承認情報表に置き換え（元の対応：{act}）"
ST_REGEN = "レポート再生成後はこの記載なし（{d}：{note}；元の対応：{act}）"
ST_PROGRAM = "プログラム修正後はこの記載なし（{d}：{note}；元の対応：{act}）"
ST_WITHDRAWN = "確認を撤回（{d}：{note}；元の対応：{act}）"
INTRO = ("以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。"
         "訂正は基本的な事実の記載に限り、モデルの予測、エビデンスレベル、結論は書き換えていません。")
INTRO_HEADER = ("以下はこのページの確認記録です。見出しのエビデンスレベルはクイック概要に合わせています。"
                "モデルの予測、概要表、結論は書き換えていません。")
INTRO_RERE = ("以下はこのページの確認記録です。内容は医薬品マスター（薬価基準収載品目）の収載情報と照合しました。訂正は基本的な事実の記載に限り、"
              "モデルの予測本文は書き換えていません。エビデンスレベルと判断は再評価結果（引き下げ、引き上げ、撤回）による場合のみ更新し、元の値は下の表にあります。")

# ---- 刪改轉紀錄（reviews_from_edits）----
# 2026-10-31～11-06 の許可證刪改：ed18b30a「国内未承認」78 頁依 KEGG 一般名・商品名對照藥價基準マスター改正、
# 34c5102b 第二批掃描刪矛盾子句。排除表、AI 重產、description、空行修正、免責聲明補段不算。
COMMITS = ["ed18b30a", "34c5102b"]
REGEN_COMMITS = ["89a01614", "530ce3ab", "177dc291", "51e8276b", "2387e9c3", "17585e7e", "057e30fe"]
SOURCES = [{"title": "医薬品マスター ダウンロードページ", "url": "https://www.hpdx.or.jp/seikyushiharai/tensuhyo/kihonmasta/kihonmasta_04.html"},
           {"title": "医薬品医療機器総合機構（PMDA）", "url": "https://www.pmda.go.jp/"}]
SENT = re.compile(r"(?<=[。！？])|\n")
CLASS_EXTRA = {"cancel": re.compile(r"未承認|未収載|承認(は|が)?(取り消|失効)|販売中止|経過措置")}
NOTES = {
    "tw": "削除：台湾サイトのテンプレートから残っていた台湾食品薬物管理署（TFDA）の記載で、この日本のページには当てはまりません。",
    "cancel": "削除：国内未承認・未収載、または承認が取り消されたという記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（{date}）。",
    "count": "削除：承認・収載の件数または状態の記載が、医薬品マスター（薬価基準収載品目）の収載情報と一致しませんでした（{date}）。",
    "generic": "削除：医薬品マスター（薬価基準収載品目）の収載情報と一致しない記載でした（{date}）。",
}
FIGURES = "データ上の収載は {total} 件、うち有効 {valid} 件です。最新の件数はクイック概要と日本市販情報にあります。"
SUMMARY = "削除：「{text}」"
STRIP_CHARS = " 、，；。,;.\n-（）()"
REGEN_NOTE = "レポートは 2026 年 11 月に再生成され、この記載はなくなっています"

# ---- 原適應症交叉驗證（check_original_indications）----
ORIGINAL_LABELS = ["既存適応症"]
ORIGINAL_NONE_RE = re.compile(r"^\s*(日本の承認情報に適応症の記載なし|記載なし|なし|不明|未記載)")
PHRASE_SPLIT = re.compile(r"[；;、，,/（）()・]+|及び|または")
PHRASE_MIN = 2
