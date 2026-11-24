"""正文許可證張數的程式改寫（2026-11-24 建，用戶決定；做法移植 KrTxGNN／MyTxGNN／HkTxGNN 的 count_prose，規則是本站日文句型）。

用戶 2026-11-24 決定：正文裡「承認 N 件」這類件數敘述，由程式依許可證快照（snapshots/jp_licenses.json.gz 的 facts：医薬品マスター收載品目，
「薬価削除」算 cancelled——薬価基準からの削除は承認の取消しを意味しない）改寫，每週資料更新後跟著改，不逐筆寫查核紀錄
（同 Tw／Kr／My／Hk：程式改寫的件數敘述是程式產生的正文）。

只改「句型明確、數字確定是本藥承認／收載件數」的地方，其餘一律不動：
  - 數字是阿拉伯數字＋「件」（漢數字「二件」「三件」不改，只列出跟事實與程式表列數都不符的）；句子要有「承認／収載／品目／薬価」
    （在市場段落「日本市販情報」裡可不寫），且沒有試験／文献／報告／症例／予測等字樣（那些「N 件」不是承認）。
  - 跳過：查核框（<!-- review -->）、程式許可證區塊（<!-- licenses -->）、受管的販売名區塊（<!-- brand-names -->）、表格列、標題、front matter；
    查核紀錄 replacement／anchor 所在的句子（改了紀錄會對不上；那些句子的件數要改請同 id 重發紀錄）。
  - 整句不動（hedged/subset）：有保留（少なくとも、以上、一部、可能性、記録）、相對數（他に、ほかに、このほか、残り）、講資料或查詢
    （収録、含まれ、本レポート用、整理した、検索）、劑型或廠商子集（錠、注射、点眼、外用、テープ、mg、「…」、社、配合…；只看數字所在的子句）；
    事實層 partial（證據包只收部分品目）的頁整頁不動。
  - 數字不動（display）：顯示筆數（上記は、上表は、主要な、以下の、記載、掲載、示します）。
角色（看數字左右幾個字）：「N 件は薬価基準から削除済み」「削除済みの N 件」→註銷；「有効な承認は N 件」「うち N 件が有効」→有效；
「単剤／単一成分」→單剤（同時有効→有效單剤）；「配合」→配合剤；其餘→總數。「X 件のうち／中 Y 件」的 X 一律是總數。
同一行只要有一句含件數而被略過，整行都不動（免得前後句數字對不上）。
同一句另有明確的有効／削除數字時，沒有限定詞的總數就是全部件數。
單剤／配合剤的數字只驗、不改（列為 single-combo）：医薬品マスターの成分欄是品名、事實層 single_total 把每張都算單剤；本站依品名「配合」
算（快照 mix），只換數字會留下錯的「単剤」字樣，要改整句請寫查核紀錄。
數字已等於該角色的任一合理讀法（沒有限定詞的「N 件」＝總數或有效數）就不動；不等於時，兩種讀法相同才改，不同就列為 ambiguous。
原數字是 0 的句子不改、列為 zero-premise；要改成 0 的也不改、列為 to-zero（前提變了）。
前提檢查（premise）：句子說「すべて有効／いずれも有効／削除済みはなし」而有效≠總數、「すべて単剤」而單剤≠總數時整句不動、列出（要改請寫查核紀錄）。
"""
from __future__ import annotations

import re

from . import site as C

SENT_SPLIT = re.compile(r"(?<=[。！？])")
NUM = re.compile(r"(?<![\d.,A-Za-z０-９-])(\d[\d,]*)(\s*)件(?!数)")
WNUM = re.compile(r"(?<![一-鿿])([一二三四五六七八九十]{1,2})件")
LICENSE = re.compile(r"承認|収載|品目|薬価|医薬品コード")
NOT_LICENSE = re.compile(r"試験|治験|文献|論文|研究|報告|PMID|NCT|jRCT|UMIN|症例|患者|例の|例で|相互作用|有害事象|副作用|予測|候補|スコア|"
                         r"エビデンス|ランク|上位|疾患|適応|ニュース|記事|PubMed|ClinicalTrials")
HEDGED = re.compile(r"少なくとも|以上|一部|可能性|記録|他に|ほかに|このほか|その他|残り|残る|約\s*\d|超|およそ|最大|まで|"
                    r"収録|含まれ|本レポート用|整理した|検索|ヒット|エビデンスパック|証拠パック")
SUBSET = re.compile(r"錠|カプセル|注射|静注|点滴|点眼|点鼻|点耳|外用|内用|経口|テープ|貼付|パップ|軟膏|クリーム|ゲル|ローション|坐剤|坐薬|"
                    r"散剤|顆粒|細粒|シロップ|液|吸入|噴霧|ｍｇ|mg|ｍＬ|mL|％|%|「|」|社|メーカー|製造販売|後発|先発|ジェネリック|"
                    r"ブランド|配合|小児|徐放|口腔内|剤形|規格|\d{9}")
DISPLAY_LEFT = re.compile(r"(上記は|上記の|上表は|上表の|上の表は|表は|表の|表に|主要な|主な|代表的な|以下の|下記の|一覧は|リストは)\s*(は|の)?\s*$")
DISPLAY_RIGHT = re.compile(r"^\s*(を|が|は)?\s*(記載|掲載|示し|示す|挙げ|列挙|表に|上記|上表|一覧に)")
BLOCK = re.compile(r"<!-- (review|licenses):begin.*?<!-- \1:end[^>]*-->|<!-- brand-names:start -->.*?<!-- brand-names:end -->", re.S)
CANC_L = re.compile(r"(削除済み|削除された|取消済み|取り消された|整理済み|失効した)(の)?(承認|もの|品目)?(は|が)?\s*$")
CANC_R = re.compile(r"^\s*(の承認)?(は|が)?(すでに|既に)?(薬価基準から|薬価収載から|薬価基準より)?(の)?(削除|取消|取り消|整理|失効)")
VALID_L = re.compile(r"(有効な(承認|販売承認|もの|品目)?|有効|うち(現在)?)\s*(は|が)?\s*$")  # 「有効な承認は合計 N 件」は checker が總數と読むので有効扱いしない
VALID_R = re.compile(r"^\s*(の承認|の販売承認)?(が|は)?\s*(現在)?\s*(有効|承認有効)(?!性)")
SINGLE_L = re.compile(r"(単剤|単一成分)(の|として|で)?(承認|製剤|品目)?(は|が)?\s*(計|合計)?\s*$")
SINGLE_R = re.compile(r"^\s*[\(（]?\s*(の)?(単剤|単一成分)")
COMBO_L = re.compile(r"配合(剤)?(の)?(承認|品目)?(は|が)?\s*$")
COMBO_R = re.compile(r"^\s*(の)?配合")
OF = re.compile(r"^\s*(の承認|の販売承認|の品目)?\s*(のうち|うち|中)")
ALL_VALID = re.compile(r"(すべて|全て|いずれも|全件|ともに|とも)\s*(が|は)?\s*(現在)?\s*有効(?!性)|"
                       r"(削除|取消|取り消|整理|失効)(済み)?(の承認|のもの)?(は|が)?\s*(なし|ありません|ない|なく|0\s*件)")
ALL_SINGLE = re.compile(r"(すべて|全て|いずれも)\s*(が|は)?\s*(単剤|単一成分)|配合剤(は|が)?\s*(なし|ありません|ない|なく)")
ALL_COMBO = re.compile(r"(すべて|全て|いずれも)\s*(が|は)?\s*配合")
_WN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}

CLAUSE_SEP = "、，,；;：:（）()。"


def _clause(s, a, b):
    """數字所在的子句：劑型、廠商等子集字樣只看這一段"""
    i = max(s.rfind(c, 0, a) for c in CLAUSE_SEP)
    j = min([k for k in (s.find(c, b) for c in CLAUSE_SEP) if k >= 0] or [len(s)])
    return s[i + 1:j]


def _wnum(w):
    if len(w) == 1:
        return _WN.get(w)
    if w[0] == "十":
        return 10 + _WN.get(w[1], 0)
    if w[1] == "十":
        return _WN.get(w[0], 0) * 10
    return None


def _role(s, a, b):
    left, right = s[max(0, a - 12):a], s[b:b + 12]
    if re.search(r"[A-Za-zＡ-Ｚ][A-Za-zＡ-Ｚ.&）)」]*\s*$", left):
        return "named"
    if DISPLAY_LEFT.search(left) or DISPLAY_RIGHT.match(right):
        return "display"
    if CANC_L.search(left) or CANC_R.match(right):
        return "cancelled"
    valid = bool(VALID_L.search(left) or VALID_R.match(right))
    if SINGLE_L.search(left) or SINGLE_R.match(right):
        return "valid_single" if valid else "single"
    if COMBO_L.search(left) or COMBO_R.match(right):
        return "valid_combo" if valid else "combo"
    return "valid" if valid else "total"


def _readings(role, f, explicit):
    """(可接受的值, 改寫用的值)。改寫用的值是 None：兩種讀法不同、又沒有限定詞，判斷不了。"""
    t, v, c = f.get("total"), f.get("valid"), f.get("cancelled")
    st, sc, vs, vc = f.get("single_total"), f.get("combo_total"), f.get("valid_single"), f.get("valid_combo")
    if role == "cancelled":
        return {c}, c
    if role == "valid":
        return {v}, v
    if role == "valid_single":
        return {vs}, vs
    if role == "valid_combo":
        return {vc}, vc
    if role == "single":
        return ({st}, st) if explicit else ({st, vs}, st if st == vs else None)
    if role == "combo":
        return ({sc}, sc) if explicit else ({sc, vc}, sc if sc == vc else None)
    return ({t}, t) if explicit else ({t, v}, t if t == v else None)


def _premise_ok(sent, f, roles):
    if ALL_VALID.search(sent) and f.get("valid") != f.get("total"):
        return False
    if ALL_SINGLE.search(sent) and f.get("single_total") != f.get("total"):
        return False
    if ALL_COMBO.search(sent) and f.get("combo_total") != f.get("total"):
        return False
    return True


def rewrite_sentence(sent, f, market=False):
    """回傳 (新句子, 跳過理由或 None)。market：句子在市場段落「日本市販情報」裡，「N 件」不寫「承認」也算。"""
    licish = (LICENSE.search(sent) or market) and not NOT_LICENSE.search(sent)
    if not licish:
        return sent, None
    nums = list(NUM.finditer(sent))
    if not nums:
        for m in WNUM.finditer(sent):  # 漢數字：不改，只在跟事實不符時列出
            role = _role(sent, m.start(), m.end())
            if role == "display" or HEDGED.search(sent) or SUBSET.search(_clause(sent, m.start(), m.end())):
                continue
            ok, _ = _readings(role, f, False)
            w = _wnum(m.group(1))
            if w is not None and w not in ok and w != f.get("_shown"):
                return sent, "numeral-word"
        return sent, None
    if HEDGED.search(sent) or any(SUBSET.search(_clause(sent, m.start(), m.end())) for m in nums):
        return sent, "hedged/subset"
    if any(_role(sent, m.start(), m.end()) == "named" for m in nums):
        return sent, "hedged/subset"
    found = []
    for i, m in enumerate(nums):
        role = _role(sent, m.start(), m.end())
        if i + 1 < len(nums) and OF.match(sent[m.end():nums[i + 1].start()]) and role in ("total", "valid", "display"):
            # 「X 件のうち Y 件」「承認 X 件中、有効なものは Y 件」「有効な承認は X 件中 Y 件」：X 一定是總數
            role = "total_xv" if role == "valid" else "total_x"
        if i and found and found[-1][1] in ("total_x", "total_xv") and role == "total":
            gap = sent[nums[i - 1].end():m.start()]
            right = sent[m.end():m.end() + 12]
            if found[-1][1] == "total_xv" or re.search(r"有効", gap) or re.match(r"^\s*(が|は)?\s*(現在)?\s*有効(?!性)", right):
                role = "valid"
            elif re.search(r"削除|取消|整理|失効", gap + right[:8]):
                role = "cancelled"
            else:
                role = "display"  # 「X 件のうち 5 件を記載」
        found.append((m, role))
    roles = [r for _, r in found if r != "display"]
    explicit = any(r in ("valid", "cancelled", "total_x", "total_xv") for r in roles)
    subs = []
    for m, role in found:
        if role == "display":
            continue
        role = "total" if role in ("total_x", "total_xv") else role
        old = int(m.group(1).replace(",", ""))
        ok, v = _readings(role, f, explicit)
        if None in ok and len(ok) == 1:
            return sent, "no-fact"
        if old in ok:
            continue
        if role in ("single", "combo", "valid_single", "valid_combo"):
            return sent, "single-combo"
        if v is None:
            return sent, "ambiguous"
        if old == 0:
            return sent, "zero-premise"
        if v == 0:
            return sent, "to-zero"
        subs.append((m, v))
    if not _premise_ok(sent, f, roles):
        return sent, "premise"
    if not subs:
        return sent, None
    out, pos = [], 0
    for m, v in subs:
        out.append(sent[pos:m.start(1)])
        out.append(f"{v:,}" if "," in m.group(1) else str(v))
        pos = m.end(1)
    out.append(sent[pos:])
    return "".join(out), None


def _line(ln, f, protect, skipped, market=False):
    if ln.startswith(("|", "#", ">", "<!--")) or not ln.strip():
        return ln
    parts = SENT_SPLIT.split(ln)
    new, held = [], False
    for s in parts:
        if any(p and (p in s or s in p) for p in protect if s.strip()):
            new.append(s)
            continue
        ns, why = rewrite_sentence(s, f, market)
        if why:
            skipped.append((why, s.strip()))
            held = True
        new.append(ns)
    if held:  # 同一行有句子判斷不了：整行不動
        return ln
    return "".join(new)


def merged(facts, mix):
    f = dict(facts or {})
    if mix:
        f.update(mix)
    return f


def rewrite(text, facts, mix=None, protect=()):
    """text：整頁 markdown。facts：快照的 facts；mix：快照的單剤／配合剤件數。回傳 (新內容, skipped)。
    front matter、查核框、程式區塊、販売名區塊、表格、標題不動。"""
    skipped = []
    if not facts or facts.get("partial") or facts.get("total") is None:
        return text, skipped
    f = merged(facts, mix)
    pb = re.search(r"<!-- licenses:begin -->(.*?)<!-- licenses:end -->", text, re.S)
    f["_shown"] = len(re.findall(r"^\| (?!医薬品コード)[^-|][^|]*\|", pb.group(1), re.M)) if pb else None  # 程式表列出的件數
    protect = [p.strip() for p in protect if p and len(p.strip()) >= 6]
    fm_end = 0
    if text.startswith("---"):
        j = text.find("\n---", 3)
        fm_end = j + 4 if j > 0 else 0
    body = text[fm_end:]
    keep = []

    def hold(m):
        keep.append(m.group(0))
        return f"\x00{len(keep) - 1}\x00"
    body = BLOCK.sub(hold, body)
    lines, market, mlv = [], False, 0
    for ln in body.split("\n"):
        h = re.match(r"^(#{1,6}) (.+?)\s*$", ln)
        if h:
            lv = len(h.group(1))
            if h.group(2) in C.MARKET_SECTIONS:
                market, mlv = True, lv
            elif market and lv <= mlv:
                market = False
        lines.append(ln if "\x00" in ln else _line(ln, f, protect, skipped, market))
    body = re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], "\n".join(lines))
    return text[:fm_end] + body, skipped
