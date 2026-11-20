#!/usr/bin/env python3
"""藥物頁「作用機轉資料不可得」句改成附出處的作用機轉（JpTxGNN，2026-11-19 建；做法照 NZTxGNN 同名程式，改成本站的頁面語言與句型）。

為什麼要有這支：
  藥師報告在證據包沒有 DrugBank 作用機轉文字時（drugbank.source＝vocab_only），AI 寫成「作用機轉資料不可得」
  （本站語言的寫法見下方 L 的 KW／DATA／NEG）。作用機轉是藥物本身的基本藥理事實（不是模型預測），所以照查核機制補：
  每一段都節錄官方仿單原文、附可點的出處與取用日期，不自己寫作用機轉。

資料來源（理由見本站 CLAUDE.md「作用機轉段的資料來源與查核機制」）：
  1. 美國 FDA 核准仿單（openFDA drug label；連結到 NLM DailyMed 同一份 SPL）：PLR 格式的「12.1 Mechanism of Action」，
     抗感染藥 12.1 只有一句時接 12.4 Microbiology 的「Mechanism of Action」小標，舊格式用「Clinical Pharmacology」段開頭的藥理說明。
     只用單一成分、主成分名（去鹽類；酯類要相同）跟本頁相同的處方藥仿單；多份時依序取全身給藥→節錄夠長→有 12.1→有品牌名→版本新。
     美國只有複方仿單的，只節錄 12.1 裡講本藥成分的句子並寫明是複方。文字照仿單原句節錄 2～4 句（拿掉「[see …]」交互參照與段落編號），不改寫。
     查詢：預設用 openFDA drug label API（https://api.fda.gov/drug/label.json，免金鑰每日 1,000 次）；
     --fda-bulk <目錄> 改用 openFDA 的 drug label 全量下載檔（download.open.fda.gov，同一批資料，只留 human prescription 仿單），不吃 API 配額。
  2. 美國沒有仿單的藥：ChEMBL drug mechanism 表（CC BY-SA 3.0）備援；ChEMBL 從雲端很慢，可先 --chembl-down 跳過。
  3. 都沒有：不補，寫進 docs/_data/drug_reviews_uncertain.json（source＝mechanism of action），列原因。
  頁面文字是日本語（用戶 2026-11-19 決定「當地語言摘要＋英文原文」）：替換句用本站語言寫明出處段落，接節錄的忠實翻譯（標明為非官方翻譯），
  再附英文原文（照引、為準）與出處連結、版本、取用日期。翻譯與原文都存在紀錄的 sources（translation、excerpt）。
  翻譯是 AI 輔助的忠實翻譯（不增不減、藥名與受體符號照原文），存在 --translations 指定的 JSON（key＝tr_key(excerpt)）；
  沒有翻譯的節錄寫到 --need，這些頁這次不寫紀錄。

紀錄：docs/_data/drug_reviews.json 的 action＝mechanism（id：jp-moa-<查核日>-<藥>-1）。claim＝頁面上「不可得」那句，
  replacement＝附出處的作用機轉。scripts/apply_drug_reviews.py 套用（可重複執行）；頁面查核紀錄表列原句與出處。模型預測與其他正文不動。

用法：
  python3 scripts/build_mechanism_reviews.py --cache <目錄> [--fda-bulk <目錄>] [--chembl-down 說明] [--translations <檔> --need <檔>]
  python3 scripts/build_mechanism_reviews.py --list       # 只列出公開頁仍寫「不可得」的句子（不連網）
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRUGS = ROOT / "docs" / "_drugs"
REVIEWS = ROOT / "docs" / "_data" / "drug_reviews.json"
UNCERTAIN = ROOT / "docs" / "_data" / "drug_reviews_uncertain.json"
UNCERTAIN_SOURCE = "mechanism of action"
PREFIX = "jp-moa"
LANG = "ja"
# 本站語言的字樣（偵測「不可得」句、替換句、查核紀錄表）
L = {'KW': '作用機序',
 'DATA': 'データ|情報',
 'NEG': 'ありません|含まれていません|得られていません|ない|なし',
 'EXCL': '結論|次のステップ|安全性|一言要約|クイック概要|査読記録|確認記録|免責事項|目次|市販情報|臨床試験|文献|販売名',
 'maxlen': 150,
 'cjk': True,
 'q': ('「', '」'),
 'sec1': '{a}の項',
 'sec2': '{a}および{b}の項',
 'tpl': '米国 FDA が承認した {name}{combo} の添付文書（Prescribing Information）の{sec}によると（非公式訳）、{qo}{tr}{qc}英語原文："{ex}"（[{title}]({url})、版 {ver}、参照日 '
        '{acc}）。',
 'combo': '（{name}を含む配合剤）',
 'act': '作用機序データがないとする記述を、出典付きの抜粋に置き換え',
 'intro_only': '以下はこのページの確認記録です。作用機序データがないとする記述を、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。モデルの予測、エビデンスレベル、結論は書き換えていません。',
 'intro_add': '作用機序データがないとする記述は、引用した公式の添付文書の抜粋（非公式訳つき）に置き換えました。',
 'summary': '「作用機序データはありません」の記述を米国添付文書の抜粋に置き換え',
 'lang_name': '日本語',
 'chembl_tpl': 'ChEMBL（EMBL-EBI）に登録されている {name} の作用機序（非公式訳）：{qo}{tr}{qc}。英語原文："{ex}"（[{title}]({url})、CC BY-SA 3.0、参照日 {acc}）。'}
REGULATOR_LOCAL = False  # True＝本站就是美國（寫「FDA-approved」，不加「US」）

KW = re.compile(L["KW"], re.I)
DATA = re.compile(L["DATA"], re.I)
NEG = re.compile(L["NEG"], re.I)
EXCL = re.compile(L["EXCL"], re.I)
REVIEW_BLOCK = re.compile(r"<!-- review:begin (\S+) -->.*?<!-- review:end \1 -->", re.S)
if L.get("cjk"):
    SENT_SPLIT = re.compile(r"(?<=[。！？])")
elif L.get("thai"):
    SENT_SPLIT = re.compile(r"(?<=\S)(?= )")
else:
    SENT_SPLIT = re.compile(r"(?<=[.!?])(?=\s+(?:\*\*)?[\"'“«„(\[A-ZÀ-ɏ؀-ۿ가-힯0-9])")
# 英文站：照 NZ 的寫法，「不可得」子句在句首、後面接 so／but／and 的後半句是 AI 推論，保留
NA_CLAUSE = (r"(?:Currently, )?(?:[Dd]etailed|A detailed) mechanism[- ]of[- ]action (?:data|text|entry|information)"
             r"[^.;\n]*?\b(?:is|are|was|were) (?:currently )?not available[^.;,\n]*")
NA_SENTENCE_EN = re.compile(r"^(" + NA_CLAUSE + r")(\.|, (?:so|but|and) |; )")


def public_pages():
    for p in sorted(DRUGS.glob("*.md")):
        t = p.read_text(encoding="utf-8")
        fm = t.split("---", 2)[1] if t.startswith("---") else ""
        if re.search(r"^layout:\s*id_redirect|^noindex:\s*true", fm, re.M) or 'http-equiv="refresh"' in t[:3000]:
            continue
        yield p, t, fm


def is_na(sentence):
    s = sentence.strip()
    if not s or len(s) > L.get("maxlen", 320):
        return False
    return bool(KW.search(s) and DATA.search(s) and NEG.search(s))


# 2026-11-20：節錄後面若接著 AI 說明「上面這段描述的依據」的句子（This description reflects／is based on…），
# 留在節錄後面會讀成美國仿單的出處；那句移到節錄前面（原文一字不改，只換順序）。英文站才有接回的後半句與下一句。
SRC_TAIL = re.compile(r"(?:This|The)(?: general| mechanistic| class)? (?:description|reasoning|rationale|explanation|class assignment|"
                      r"mechanism described (?:above|here)|mechanism above|pharmacology above|description (?:above|here)|reasoning above|above)\b"
                      r"[^.]*?\b(?:is (?:based|drawn|derived)|was drawn|reflects|relies|rests|comes|draws|derives)\b|This is based on")
_SENT_END = re.compile(r"[.!?](?=\s|$)")

# 非英文站：下一句是講「上面描述依據」的句子時（2026-11-20 逐句標註校準的本站寫法）
SRC_LOCAL = re.compile(r"(?:ここでの|上記の|この)説明は[^。]*?(?:基づ|による)")


def reorder_src_tail(text, claim, rep):
    """回傳 (claim, rep)：claim 後面（同一句的後半或下一句）是講「上面描述依據」的句子時，claim 延伸涵蓋那句、rep 改成「那句＋節錄」。"""
    j = text.find(claim)
    if j < 0:
        return claim, rep
    rest = text[j + len(claim):].split("\n", 1)[0]
    if LANG != "en":
        if SRC_LOCAL is None:
            return claim, rep
        body = rest.lstrip()
        sep = rest[:len(rest) - len(body)]
        segs = [x for x in SENT_SPLIT.split(body) if x]
        sent = segs[0].rstrip() if segs else ""
        if sent and SRC_LOCAL.match(sent) and body.startswith(sent):
            return claim + sep + sent, sent + (sep or "") + rep
        return claim, rep
    if claim and claim[-1].islower() and rep[-2:-1] == " ":   # 同一句的後半（claim 以「, so t」收尾、rep 以「 T」收尾）
        m = _SENT_END.search(rest)
        if not m:
            return claim, rep
        sent = rep[-1] + rest[:m.end()]
        if SRC_TAIL.match(sent):
            return claim + rest[:m.end()], sent + " " + rep[:-2].rstrip()
        return claim, rep
    lead = len(rest) - len(rest.lstrip(" "))
    if lead != 1:
        return claim, rep
    m = _SENT_END.search(rest, 1)
    if not m:
        return claim, rep
    sent = rest[1:m.end()]
    if SRC_TAIL.match(sent):
        return claim + rest[:m.end()], sent + " " + rep
    return claim, rep

# 2026-11-20：同頁上方已引用同一段節錄（同頁兩句「不可得」相鄰時）就不再重複引用，改成指向上方節錄的一句
POINTER_SENTENCE = '作用機序は、出典とともに上記に引用しています。'


def pointer_sentence(src):
    """指向上方節錄的一句，附同一個來源連結（mechanism 的 replacement 一律要附來源連結）。"""
    link = f"[{'DailyMed' if 'dailymed' in src['url'] else 'ChEMBL'}]({src['url']})"
    s = POINTER_SENTENCE
    if s[-1] in "。":
        return s[:-1] + f"（{link}）" + s[-1]
    if s[-1] not in ".!?":
        return s + f" ({link})"
    return s[:-1] + f" ({link})" + s[-1]


def _excerpt(r):
    s = r.get("sources")
    s = s[0] if isinstance(s, list) and s else s
    return (s or {}).get("excerpt", "")


def find_claim(text, protect=()):
    """回傳 (claim, tail)：claim 是頁面上要換掉的原文（整句；英文站句首子句＋連接詞），tail 是 replacement 要接回的後半句開頭。
    只看正文章節（排除結論／下一步、安全性、摘要、總覽表、查核紀錄、免責聲明等，見 L["EXCL"]）、不看表格列與查核框。"""
    body = text.split("---", 2)[2] if text.startswith("---") else text
    body = REVIEW_BLOCK.sub(lambda m: "\n" * m.group(0).count("\n"), body)
    sec_ok = False
    for line in body.split("\n"):
        if line.startswith("#"):
            sec_ok = line.startswith("## ") and not EXCL.search(line) or (line.startswith("###") and sec_ok)
            continue
        if not sec_ok or line.lstrip().startswith("|") or "<!--" in line:
            continue
        for seg in SENT_SPLIT.split(line):
            s = seg.strip()
            s = re.sub(r"^(?:[-*+]\s+|\d+\.\s+)", "", s)
            if not is_na(s):
                continue
            if any(s in x or (x and x in s) for x in protect):
                continue  # 句子是別筆查核紀錄的更正文字或錨點，不動
            if LANG == "en":
                m = NA_SENTENCE_EN.match(s)
                if m:
                    clause, conn = m.group(1), m.group(2)
                    if conn == ".":
                        return clause + ".", ""
                    rest = s[m.end():]
                    if rest:
                        return clause + conn + rest[0], rest[0].upper()
                n = NEG2.search(s) or NEG.search(s)  # 2026-11-20：新增寫法的否定詞也要算（不然會在否定詞前面的 , but 切開、換錯半句）
                m2 = re.compile(r", (?:so|but) ").search(s, n.end() if n else 0)
                if m2 and m2.end() < len(s):
                    return s[:m2.end() + 1], s[m2.end()].upper()
            if s.startswith("**") and not s.endswith("**"):
                continue
            return s, ""
    return None, None


def front(fm, key):
    m = re.search(rf'^{key}:\s*"?([^"\n]+)"?', fm, re.M)
    return m.group(1).strip() if m else ""


def protected(records, fname):
    """同頁紀錄的更正文字與錨點（含已套上的作用機轉節錄）：這些句子由那些紀錄管，不再當成「不可得」句。"""
    out = []
    for r in records:
        if r.get("file") == fname:
            for k in ("replacement", "anchor"):
                v = (r.get(k) or "").strip()
                if len(v) >= 8:
                    out.append(v)
    return out


def http_json(url, cache, key, tries=4):
    f = cache / (re.sub(r"[^\w.-]+", "_", key)[:150] + ".json")
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "txgnn-site-review/1.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                data = {}
                break
            if e.code == 429:
                raise RuntimeError("openFDA API quota exceeded (HTTP 429)")
            if k == tries - 1:
                raise
            time.sleep(5 * (k + 1))
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(5 * (k + 1))
    f.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    time.sleep(0.3)
    return data


BULK = {"dir": None, "rows": None, "idx": None}


def _tokens(s):
    return set(t for t in re.split(r"[^a-z0-9]+", s.lower()) if t)


def fda_results(base, cache):
    """openFDA 仿單查詢：generic_name 含 base 的每個字。快取檔名同 NZ（fda_<base>.json），各站共用同一個快取目錄。"""
    f = cache / (re.sub(r"[^\w.-]+", "_", "fda_" + base)[:150] + ".json")
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    if BULK["dir"]:
        import glob
        import gzip
        if BULK["rows"] is None:
            rows = []
            for p in sorted(glob.glob(str(Path(BULK["dir"]) / "labels_*.json.gz"))):
                rows += json.load(gzip.open(p, "rt", encoding="utf-8"))
            idx = {}
            for i, r in enumerate(rows):
                for g in (r.get("openfda", {}).get("generic_name") or []):
                    for t in _tokens(g):
                        idx.setdefault(t, set()).add(i)
            BULK["rows"], BULK["idx"] = rows, idx
        toks = base.split()
        hit = set.intersection(*[BULK["idx"].get(t, set()) for t in toks]) if toks else set()
        res = [BULK["rows"][i] for i in sorted(hit)
               if any(set(toks) <= _tokens(g) for g in BULK["rows"][i].get("openfda", {}).get("generic_name") or [])]
        data = {"results": res, "meta": {"source": "openFDA drug label bulk download (human prescription labels)"}}
        f.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return data
    q = " AND ".join(f'openfda.generic_name:"{t}"' for t in base.split())
    url = "https://api.fda.gov/drug/label.json?" + urllib.parse.urlencode({"search": q, "limit": 100})
    return http_json(url, cache, "fda_" + base)


SALTS = {"hydrochloride", "hcl", "dihydrochloride", "sodium", "potassium", "calcium", "magnesium", "maleate", "mesylate",
         "mesilate", "besylate", "besilate", "sulfate", "sulphate", "acetate", "citrate", "tartrate", "bitartrate",
         "fumarate", "succinate", "phosphate", "bromide", "chloride", "hydrobromide", "monohydrate", "dihydrate",
         "trihydrate", "hemihydrate", "anhydrous", "disodium", "dipropionate", "propionate", "valerate", "furoate",
         "lactate", "gluconate", "nitrate", "tosylate", "hyclate", "malate", "pamoate", "decanoate", "enanthate",
         "cypionate", "embonate", "xinafoate", "trometamol", "tromethamine", "meglumine", "lysine", "arginine",
         "hydrogen", "dimesylate", "oxalate", "salicylate", "camsylate", "napsylate", "base", "usp", "acetonide", "hexacetonide"}
# 酯類是不同的藥（fluticasone furoate ≠ fluticasone propionate）：頁名有酯類字樣時，仿單要有同一個字樣
ESTERS = {"propionate", "dipropionate", "furoate", "valerate", "acetonide", "hexacetonide", "decanoate", "enanthate", "cypionate"}


def ester_ok(page_name, label_name):
    pe = {t for t in re.split(r"[^a-z]+", page_name.lower()) if t in ESTERS}
    le = {t for t in re.split(r"[^a-z]+", label_name.lower()) if t in ESTERS}
    return not pe or pe == le


def norm_base(name):
    s = re.sub(r"-[a-z]{4}\b", "", name.lower())  # 生物相似藥的 4 字母字尾（insulin glargine-yfgn）
    toks = [t for t in re.split(r"[^a-z0-9]+", s) if t and t not in SALTS]
    return " ".join(toks)


def front(fm, key):
    m = re.search(rf'^{key}:\s*"?([^"\n]+)"?', fm, re.M)
    return m.group(1).strip() if m else ""


LEAD_HEAD = re.compile(r"^(?:(?i:Pharmacologic Properties|ACTIONS?|Mechanisms? of action)\s*|\d+(?:\.\d+)*\.?\s*|CLINICAL PHARMACOLOGY\s*|Clinical Pharmacology\s*|Mechanisms? of (?:\w+ )?Action\s*|"
                       r"MECHANISM OF ACTION\s*|Pharmacodynamics\s*|General\s*|Action\s*|Actions\s*|[:;,.\-–]\s*|[a-z]\s+(?=[A-Z]))*")


def clean_label(s):
    s = re.sub(r"\[\s*see [^\]]*\]", "", s, flags=re.I)
    s = re.sub(r"\(\s*\d+(?:\.\d+)*\s*\)", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = LEAD_HEAD.sub("", s)  # 段落編號與小標（「12.1 Mechanism of Action」「Pharmacodynamics」）
    s = re.sub(r"\s+([.,;:])", r"\1", s)
    return s.strip()


ABBR = re.compile(r"(?:\b(?:e\.g|i\.e|approx|ca|vs|Fig|al|No|U\.S|Inc|Ltd)\.|\b[A-Z]\.)$")


def sentences(s):
    out, cur = [], ""
    for part in re.split(r"(?<=[.!?])\s+(?=[A-Z(\[0-9])", s):
        cur = f"{cur} {part}".strip() if cur else part
        if ABBR.search(cur):
            continue
        out.append(cur)
        cur = ""
    if cur:
        out.append(cur)
    return out


MOA_WORDS = re.compile(r"inhibit|block|bind|agonist|antagonist|receptor|enzyme|mechanism|acts? |suppress|stimulat|"
                       r"interfer|chelat|analog|reduc|increas|decreas|depolari|alkylat|crosslink|cross-link|synthesis|activity|mode of action|"
                       r"neurotransmission|neuronal transmission|anticholinergic|antihistamin|vasodilat|fungicid|bactericid", re.I)
MOA_STRICT = re.compile(r"inhibit|block|binds?\b|binding|agonist|antagonist|receptor|enzyme|mechanism|acts? |suppress|stimulat|"
                        r"interfer|chelat", re.I)
START_BAD = re.compile(r"\bdo(?:es)? not\b|\bresistan|^In clinical (?:studies|trials)", re.I)
PK_WORDS = re.compile(r"absorb|absorption|half-life|bioavailab|plasma concentration|peak|volume of distribution|excret|"
                      r"following (?:oral|intravenous) administration|after (?:oral|intravenous) administration|metaboli[sz]ed in|metabolism|serum levels|blood levels|radioactivity", re.I)
STOP_HEAD = re.compile(r"\b(?:Pharmacodynamics|Pharmacokinetics|Absorption|Distribution|Metabolism|Elimination|"
                       r"Microbiology|Mechanism of Resistance|Cardiac Electrophysiology|Resistance(?= [A-Z])|Cross[- ][Rr]esistance|"
                       r"Antiviral Activity|Antibacterial Activity|Antimicrobial Activity|Antifungal Activity|Activity in [Cc]ell)\b")


def excerpt(text, from_cp=False, key=""):
    s = re.sub(r"\s+", " ", text)
    if from_cp:
        # Clinical Pharmacology 段：有「Mechanism of Action」小標（標題大小寫、不是句中的 mechanism of action）就從那裡開始
        m = re.search(r"(?:^|(?<=[.:)] )|(?<=\d ))Mechanisms? of Action\s*:?\s*(?=[A-Z])", s)
        headed = bool(m)
        if m:
            s = s[m.end():]
    s = clean_label(s)
    # 到下一個小標（Pharmacokinetics、12.3 …）為止
    m = re.search(r"(?:\b\d+(?:\.\d+)+\s+[A-Z]|" + STOP_HEAD.pattern + ")", s)
    if m and m.start() > 0:
        s = s[:m.start()].strip()
    sents = [x for x in sentences(s) if len(x) > 15]
    if from_cp:
        # 舊格式 Clinical Pharmacology 段常先講藥動學：沒有「Mechanism of Action」小標時，第一句要講作用、不講藥動學，
        # 否則不用；節錄到第一句藥動學句為止（只取連續的句子，不跳著挑）
        if not headed:
            # 沒有小標：從前 12 句裡第一句講作用、不講藥動學的句子開始（連續節錄，不跳著挑）
            start = next((i for i, x in enumerate(sents[:12]) if (MOA_WORDS if i == 0 else MOA_STRICT).search(x)
                          and not PK_WORDS.search(x) and not START_BAD.search(x)
                          and (not key or key in x.lower() or i == 0)), None)
            if start is None:
                return ""
            sents = sents[start:]
        cut = next((i for i, x in enumerate(sents) if PK_WORDS.search(x)), len(sents))
        sents = sents[:cut]
    picked = []
    for x in sents[:4]:
        if picked and len(" ".join(picked + [x])) > 650:
            break
        picked.append(x)
        if len(picked) >= 2 and len(" ".join(picked)) >= 220:
            break
    # 節錄要講到本藥：前面幾句只講生理背景（例 candesartan 先講 angiotensin II）時，接上第一句提到本藥的句子（中間以「[…]」標示省略）
    if key and not any(key in x.lower() for x in picked):
        later = next((x for x in sents[len(picked):8] if key in x.lower()), None)
        if later:
            picked = picked[:2] + ["[…]", later]
    txt = " ".join(picked).strip()
    if not txt or not txt.endswith((".", ")")) or len(txt) < 20:
        return ""
    if re.search(r"homeopath", txt, re.I):
        return ""
    return txt


# 紐西蘭用 INN／英式寫法，美國仿單用 USAN：只收同一個藥的寫法（查仿單時用，頁面上的藥名不改）
US_NAME = {"clomifene": "clomiphene", "paracetamol": "acetaminophen", "salbutamol": "albuterol", "adrenaline": "epinephrine",
           "noradrenaline": "norepinephrine", "glibenclamide": "glyburide", "frusemide": "furosemide", "ciclosporin": "cyclosporine",
           "lignocaine": "lidocaine", "levothyroxine": "levothyroxine", "thyroxine": "levothyroxine", "rifampicin": "rifampin",
           "cefalexin": "cephalexin", "amoxicillin clavulanate": "amoxicillin clavulanate", "oestradiol": "estradiol",
           "colecalciferol": "cholecalciferol", "ergocalciferol": "ergocalciferol", "dosulepin": "dothiepin",
           "mesalazine": "mesalamine", "sulfasalazine": "sulfasalazine", "aciclovir": "acyclovir", "valaciclovir": "valacyclovir",
           "ganciclovir": "ganciclovir", "bendroflumethiazide": "bendroflumethiazide", "chlorphenamine": "chlorpheniramine",
           "trimeprazine": "trimeprazine", "pethidine": "meperidine", "methylthioninium": "methylene blue",
           "isoprenaline": "isoproterenol", "orciprenaline": "metaproterenol", "dexamfetamine": "dextroamphetamine",
           "glyceryl trinitrate": "nitroglycerin", "beclometasone": "beclomethasone", "flucloxacillin": "flucloxacillin",
           "sodium cromoglicate": "cromolyn", "cromoglicate": "cromolyn", "sodium cromoglycate": "cromolyn",
           "tretinoin": "tretinoin", "busulfan": "busulfan", "ciclopirox": "ciclopirox", "phenobarbitone": "phenobarbital",
           "procaine benzylpenicillin": "penicillin g procaine", "benzylpenicillin": "penicillin g", "phenoxymethylpenicillin": "penicillin v",
           "amylobarbitone": "amobarbital", "thiopentone": "thiopental", "suxamethonium": "succinylcholine",
           "levomepromazine": "methotrimeprazine", "pizotifen": "pizotyline", "hydroxocobalamin": "hydroxocobalamin",
           "ipratropium": "ipratropium", "tiotropium": "tiotropium", "zuclopenthixol": "zuclopenthixol",
           "metamizole": "dipyrone", "cinacalcet": "cinacalcet", "sodium valproate": "valproate", "valproic acid": "valproic acid",
           "dimeticone": "dimethicone", "povidone iodine": "povidone-iodine", "liquid paraffin": "mineral oil",
           "chlormethine": "mechlorethamine", "mitozantrone": "mitoxantrone", "teicoplanin": "teicoplanin",
           "calcitriol": "calcitriol", "alfacalcidol": "alfacalcidol", "lysine acetylsalicylate": "aspirin", "benzatropine": "benztropine",
           "trastuzumab deruxtecan": "fam trastuzumab deruxtecan", "enfortumab vedotin": "enfortumab vedotin",
           "acetylsalicylic acid": "aspirin", "nicotinic acid": "niacin", "nicotinamide": "niacinamide"}


def label_source(inn, cache):
    src, why = _label_source(inn, cache)
    us = US_NAME.get(norm_base(inn))
    if not src and us and us != norm_base(inn):
        src, why2 = _label_source(us, cache)
        why = why if src is None else ""
        if src:
            src["us_name"] = us
    return src, why


def _label_source(inn, cache):
    base = norm_base(inn)
    if not base:
        return None, "no INN"
    d = fda_results(base, cache)
    cands = []
    for r in d.get("results", []):
        o = r.get("openfda", {})
        gens = o.get("generic_name") or []
        subs = o.get("substance_name") or []
        if len(gens) != 1 or len(subs) > 1 or re.search(r",| AND |\band\b", gens[0], re.I):
            continue
        if norm_base(gens[0]) != base or not ester_ok(inn, gens[0]):
            continue
        if "HUMAN PRESCRIPTION DRUG" not in (o.get("product_type") or []):
            continue
        moa = (r.get("mechanism_of_action") or [""])[0]
        key = base.split()[0]
        ex, field = (excerpt(moa, key=key), "12.1 Mechanism of Action") if moa else ("", "")
        if not ex:
            ex, field = excerpt((r.get("clinical_pharmacology") or [""])[0], from_cp=True, key=key), "Clinical Pharmacology"
        # 抗感染藥的 12.1 常只有一句「X is an antibacterial drug」，作用機轉寫在 12.4 Microbiology 的「Mechanism of Action」小標下
        # （有的仿單 Microbiology 是獨立欄，有的併在 Clinical Pharmacology 段裡）
        micro = re.sub(r"\s+", " ", (r.get("microbiology") or [""])[0])
        if not micro:
            cp = re.sub(r"\s+", " ", (r.get("clinical_pharmacology") or [""])[0])
            mi = re.search(r"\bMicrobiology\b", cp)
            micro = cp[mi.end():] if mi else ""
        mm = re.search(r"Mechanism of (?:\w+ )?Action\s*:?\s*(?=[A-Z])", micro)
        if not ex and mm:
            ex, field = excerpt(micro[mm.end():], key=key), "Clinical Pharmacology; Microbiology"
        if not ex:
            continue
        if len(ex) < 120 and mm and not field.endswith("Microbiology"):
            ex2 = excerpt(micro[mm.end():], key=key)
            if ex2:
                ex, field = f"{ex} […] {ex2}", ("12.1 Mechanism of Action; 12.4 Microbiology" if field.startswith("12.1")
                                                 else "Clinical Pharmacology; Microbiology")
        if len(ex) < 40:
            continue
        brand = (o.get("brand_name") or [""])[0]
        branded = 1 if brand and norm_base(brand) != base else 0  # 有品牌名的多半是原廠仿單
        routes = set(o.get("route") or [])
        systemic = 1 if routes & {"ORAL", "INTRAVENOUS", "INTRAMUSCULAR", "SUBCUTANEOUS", "SUBLINGUAL", "BUCCAL"} else 0
        # 排序：全身給藥優先（外用仿單常寫「X 治療痤瘡的機轉不明」，不是藥物本身的作用機轉）→ 有 12.1 → 原廠 → 版本新
        cands.append((systemic, 1 if len(ex) >= 120 else 0, 1 if field.startswith("12.1") else 0, branded,
                      r.get("effective_time", ""), r, ex, field))
    combo = False
    if not cands:
        # 美國只有複方仿單（例 glecaprevir／pibrentasvir、sacubitril／valsartan）：只節錄 12.1 裡講本藥成分的句子
        key = base.split()[0]
        for r in d.get("results", []):
            o = r.get("openfda", {})
            gens = o.get("generic_name") or []
            if len(gens) != 1 or "HUMAN PRESCRIPTION DRUG" not in (o.get("product_type") or []):
                continue
            parts = [norm_base(x) for x in re.split(r",|\band\b|/", gens[0], flags=re.I)]
            if base not in parts or len(parts) < 2:
                continue
            moa = (r.get("mechanism_of_action") or [""])[0]
            sents = [x for x in sentences(clean_label(moa)) if re.search(rf"\b{re.escape(key)}\b", x, re.I) and len(x) > 30
                     and MOA_WORDS.search(x)
                     and not re.search(r"described below|individual components|combination product containing|metabolism of|plasma levels", x, re.I)]
            if not sents:
                continue
            ex = " ".join(sents[:2]) if len(" ".join(sents[:2])) <= 650 else sents[0]
            if not ex.endswith((".", ")")):
                continue
            brand = (o.get("brand_name") or [""])[0]
            cands.append((1, 1, 1, 1 if brand else 0, r.get("effective_time", ""), r, ex, "12.1 Mechanism of Action"))
        combo = bool(cands)
    if not cands:
        return None, f"no single-ingredient US prescription label for '{base}' with a mechanism or clinical pharmacology section in openFDA"
    cands.sort(key=lambda c: c[:5], reverse=True)
    eff, r, ex, field = cands[0][4:]
    o = r["openfda"]
    brand = (o.get("brand_name") or [""])[0]
    gen = o["generic_name"][0].lower()
    mfr = (o.get("manufacturer_name") or [""])[0]
    title = f"DailyMed: {brand.title() + ' (' + gen + ')' if brand and brand.lower() != gen else gen} prescribing information" + (f", {mfr}" if mfr else "")
    return {
        "kind": "us_label",
        "title": title,
        "url": f"https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid={r['set_id']}",
        "set_id": r["set_id"],
        "label_version": f"{eff[:4]}-{eff[4:6]}-{eff[6:8]}" if len(eff) == 8 else eff,
        "section": field,
        "excerpt": ex,
        "via": "openFDA drug label API (https://open.fda.gov/apis/drug/label/)",
        "combination": gen if combo else "",
    }, ""


def chembl_source(inn, cache):
    base = norm_base(inn)
    url = "https://www.ebi.ac.uk/chembl/api/data/molecule.json?" + urllib.parse.urlencode({"pref_name__iexact": base, "limit": 10})
    d = http_json(url, cache, "chembl_pref_" + base)
    mol = None
    for m in d.get("molecules", []):
        names = {norm_base(m.get("pref_name") or "")} | {norm_base(s.get("molecule_synonym", "")) for s in m.get("molecule_synonyms") or []}
        if base in names and str(m.get("max_phase")) in ("4", "4.0"):
            mol = m
            break
    if not mol:
        return None, f"no approved ChEMBL molecule named '{base}'"
    cid = mol["molecule_chembl_id"]
    mech = http_json("https://www.ebi.ac.uk/chembl/api/data/mechanism.json?" + urllib.parse.urlencode(
        {"molecule_chembl_id": cid, "limit": 20}), cache, "chembl_mech_" + cid).get("mechanisms", [])
    rows = []
    for m in mech:
        moa = (m.get("mechanism_of_action") or "").strip()
        if moa and moa not in rows:
            rows.append(moa)
    if not rows:
        return None, f"ChEMBL {cid} has no mechanism entry"
    return {
        "kind": "chembl",
        "title": f"ChEMBL {cid} ({mol.get('pref_name', '').lower()}): drug mechanism",
        "url": f"https://www.ebi.ac.uk/chembl/explore/compound/{cid}",
        "chembl_id": cid,
        "excerpt": "; ".join(rows[:4]),
        "via": "ChEMBL web services (https://www.ebi.ac.uk/chembl/api/data/docs), CC BY-SA 3.0",
    }, ""


def md_safe(t):
    """仿單原文放進 markdown 段落：避免被當成 HTML、強調或表格（只換符號，不改字）。"""
    return t.replace("<", "&lt;").replace("*", "\\*").replace("|", "&#124;").replace('"', "'")




def tr_key(excerpt):
    return hashlib.sha1(("%s|%s" % (LANG, excerpt)).encode("utf-8")).hexdigest()[:16]


def section_names(src):
    secs = {"12.1 Mechanism of Action": ("Mechanism of Action",),
            "12.1 Mechanism of Action; 12.4 Microbiology": ("Mechanism of Action", "Microbiology"),
            "Clinical Pharmacology; Microbiology": ("Clinical Pharmacology", "Microbiology")}.get(src["section"], ("Clinical Pharmacology",))
    return secs


def replacement_text(name, src, accessed, translation=None):
    ex = md_safe(src["excerpt"])
    if src["kind"] != "us_label" and LANG != "en":
        qo, qc = L["q"]
        return L["chembl_tpl"].format(name=name, qo=qo, qc=qc, tr=md_safe(translation), ex=ex,
                                      title=src["title"], url=src["url"], acc=accessed)
    if src["kind"] != "us_label":
        return (f"ChEMBL (EMBL-EBI) records the mechanism of action of {name.lower()} as: {ex} "
                f"([{src['title']}]({src['url']}), CC BY-SA 3.0; accessed {accessed}.)")
    secs = section_names(src)
    if LANG == "en":
        sec = {1: f"{secs[0]} section"}.get(len(secs), f"{secs[0]} and {secs[-1]} sections")
        fda = "FDA-approved prescribing information" if REGULATOR_LOCAL else "US FDA-approved prescribing information"
        if src.get("combination"):
            return (f"According to the {sec} of the {fda} for {src['combination']} "
                    f"(a combination product containing {name.lower()}): "
                    f"\"{ex}\" ([{src['title']}]({src['url']}), label version {src['label_version']}; accessed {accessed}.)")
        return (f"According to the {sec} of the {fda} for {name.lower()}: "
                f"\"{ex}\" ([{src['title']}]({src['url']}), label version {src['label_version']}; accessed {accessed}.)")
    qo, qc = L["q"]
    quoted = [f"{qo}{s}{qc}" if not L.get("cjk") else f"「{s}」" for s in secs]
    sec = L["sec1"].format(a=quoted[0]) if len(quoted) == 1 else L["sec2"].format(a=quoted[0], b=quoted[1])
    if src.get("combination"):
        nm, combo = src["combination"], L["combo"].format(name=name)
    else:
        nm, combo = name, ""
    return L["tpl"].format(sec=sec, name=nm, combo=combo, qo=qo, qc=qc, tr=md_safe(translation), ex=ex,
                           title=src["title"], url=src["url"], ver=src["label_version"], acc=accessed)


def gate_errors():
    """給 scripts/check_seo_docs.py：公開頁寫「作用機轉資料不可得」、卻沒有 mechanism 紀錄也沒有列在待查清單（說明為什麼補不到）的頁。
    有紀錄卻沒套上的頁由 apply_drug_reviews.check_errors 擋。"""
    rev = load_json(REVIEWS, {"records": []})
    rev = rev["records"] if isinstance(rev, dict) else rev
    unc = load_json(UNCERTAIN, {"items": []})
    unc = unc.get("items", []) if isinstance(unc, dict) else unc
    covered = {r["file"] for r in rev if r.get("action") == "mechanism"}
    covered |= {i.get("file") for i in unc if i.get("source") == UNCERTAIN_SOURCE and i.get("status") in ("open", "unresolvable")}
    listed = {i.get("file") for i in unc if i.get("source") == UNCERTAIN_SOURCE and i.get("status") in ("open", "unresolvable")}
    bad = [p.name for p, t, _ in public_pages() if p.name not in listed and find_claim(t, protected(rev, p.name))[0]]
    if not bad:
        return []
    return [f"公開藥物頁寫「作用機轉資料不可得」、沒有附出處的作用機轉紀錄也沒列待查 {len(bad)} 頁：{'、'.join(bad[:8])}"
            "（跑 python3 scripts/build_mechanism_reviews.py --cache <目錄> 再跑 scripts/apply_drug_reviews.py）"]


def load_json(p, default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None, help="openFDA／ChEMBL 回應快取目錄（當不受信任資料；各站可共用）")
    ap.add_argument("--fda-bulk", default=None, help="openFDA drug label 全量下載檔整理後的目錄（labels_*.json.gz）；給了就不打 API")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--chembl-down", metavar="說明",
                    help="ChEMBL API 連不上或太慢時：不查 ChEMBL，補不到的頁照樣列進待查清單，原因寫這段說明")
    ap.add_argument("--no-chembl", action="store_true", help="只查美國仿單，補不到的頁不列待查（之後再跑一次）")
    ap.add_argument("--translations", default=None, help="非英文站：節錄的翻譯檔（JSON，key＝tr_key(excerpt)）")
    ap.add_argument("--need", default=None, help="非英文站：還沒有翻譯的節錄寫到這個檔（JSON），翻好後再跑一次")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--out", help="--dry-run 時把全部新紀錄寫到這個檔")
    ap.add_argument("drugs", nargs="*")
    a = ap.parse_args()
    rev0 = load_json(REVIEWS, {"records": []})
    rev0 = rev0["records"] if isinstance(rev0, dict) else rev0
    targets = []
    for p, t, fm in public_pages():
        if a.drugs and p.stem not in a.drugs:
            continue
        claim, tail = find_claim(t, protected(rev0, p.name))
        if claim:
            targets.append((p, fm, claim, tail, t))
    if a.list:
        for p, _, claim, _, _ in targets:
            print(f"{p.name}\t{claim}")
        print(f"公開頁仍寫「作用機轉資料不可得」：{len(targets)} 頁")
        return 0
    if not a.cache:
        sys.exit("要給 --cache <目錄>（API 回應快取；當不受信任資料）")
    cache = Path(a.cache)
    cache.mkdir(parents=True, exist_ok=True)
    BULK["dir"] = a.fda_bulk
    trans = load_json(Path(a.translations), {}) if a.translations else {}
    rev = load_json(REVIEWS, {"records": []})
    records = rev["records"] if isinstance(rev, dict) else rev
    unc = load_json(UNCERTAIN, {"items": []})
    have = {r["file"] for r in records if r.get("action") == "mechanism"}
    nmech = {}
    for r in records:
        if r.get("action") == "mechanism":
            nmech[r["file"]] = nmech.get(r["file"], 0) + 1
    listed = {i.get("file") for i in (unc.get("items", []) if isinstance(unc, dict) else unc)
              if i.get("source") == UNCERTAIN_SOURCE and i.get("status") in ("open", "unresolvable")}
    added, missing, need = [], [], {}
    for p, fm, claim, tail, page_text in targets:
        # 已有紀錄的頁：只處理還留著的「不可得」句（同頁第二句起）；已列待查的頁不重抓
        if p.name in listed and p.name not in have:
            continue
        name = front(fm, "title") or p.stem.replace("_", " ")
        inn = front(fm, "monitor_inn") or name
        try:
            src, why = label_source(inn, cache)
            if not src and inn.lower() != name.lower():
                src, why2 = label_source(name, cache)
        except Exception as e:  # 單一藥抓取失敗不擋其他藥；下次重跑會補（快取只存成功的回應）
            if "quota" in str(e):
                print("openFDA 配額用完，停在", p.name, file=sys.stderr)
                break
            src, why = None, f"openFDA fetch failed ({e})"
        why2 = ("ChEMBL not queried in this run" if a.no_chembl else
                f"ChEMBL not queried: {a.chembl_down}" if a.chembl_down else "")
        if not src and not a.no_chembl and not a.chembl_down:
            try:
                src, why2 = chembl_source(inn, cache)
            except Exception as e:
                src, why2 = None, f"ChEMBL fetch failed ({e})"
        if not src:
            if p.name not in have:
                missing.append({"file": p.name, "drug": p.stem, "reason": f"{why}; {why2}"})
            continue
        translation = None
        if LANG != "en":
            k = tr_key(src["excerpt"])
            translation = (trans.get(k) or {}).get("translation") if isinstance(trans.get(k), dict) else trans.get(k)
            if not translation:
                need[k] = {"lang": LANG, "excerpt": src["excerpt"], "drug": p.stem}
                continue
        s = {k: v for k, v in {
            "title": src["title"], "url": src["url"], "accessed": a.date, "excerpt": src["excerpt"],
            "label_version": src.get("label_version"), "section": src.get("section"), "via": src["via"],
            "set_id": src.get("set_id"), "chembl_id": src.get("chembl_id")}.items() if v}
        if translation:
            s["translation"] = translation
            s["translation_lang"] = LANG
            s["translation_note"] = ("unofficial translation of the English excerpt (machine-assisted, 2026-11-19); "
                                     "the English original quoted on the page is authoritative")
        # 同一頁可能有不只一句「不可得」：每句各一筆紀錄（-1、-2…），換掉一句再找下一句
        n, text_local, prot = nmech.get(p.name, 0), page_text, protected(rev0, p.name)
        while n < 8:
            if text_local is not page_text or n > nmech.get(p.name, 0):
                claim, tail = find_claim(text_local, prot)
                if not claim:
                    break
            core = replacement_text(name, src, a.date, translation)
            cpos = text_local.find(claim)
            if any(r.get("file") == p.name and _excerpt(r) == src["excerpt"] and 0 <= text_local.find(r.get("replacement", "\0")) < cpos
                   for r in list(rev0) + added):
                core = pointer_sentence(src)
            rep = core + (" " + tail if tail else "")
            claim, rep = reorder_src_tail(text_local, claim, rep)
            rec = {
                "id": f"{PREFIX}-{a.date.replace('-', '')}-{p.stem}-{n + 1}",
                "drug": p.stem,
                "file": p.name,
                "action": "mechanism",
                "claim": claim,
                "replacement": rep,
                "summary": L.get("summary") or f"\"{claim.rstrip('.,;: ').strip()}\" replaced with a sourced mechanism-of-action statement",
                "finding": ("頁面寫作用機轉資料不可得（證據包 drugbank.source＝vocab_only）；作用機轉是藥物本身的藥理事實，"
                            f"依 {'美國 FDA 仿單 ' + src['section'] if src['kind'] == 'us_label' else 'ChEMBL drug mechanism 表'} 原文節錄補上"
                            f"{'（附非官方翻譯，英文原文為準）' if translation else ''}，模型預測與其他正文不動。"),
                "sources": [s],
                "checked": a.date,
                "method": "scripts/build_mechanism_reviews.py（2026-11-19 建）",
            }
            added.append(rec)
            j = text_local.find(claim)
            text_local = text_local[:j] + rep + text_local[j + len(claim):] if j >= 0 else text_local + "\n"
            prot = prot + [rep]
            n += 1
    print(f"目標 {len(targets)} 頁；新紀錄 {len(added)}（仿單 {sum(r['sources'][0].get('set_id') is not None for r in added)}、"
          f"ChEMBL {sum('chembl_id' in r['sources'][0] for r in added)}）；找不到來源 {len(missing)}；待翻譯 {len(need)}")
    if a.need:
        Path(a.need).write_text(json.dumps(need, ensure_ascii=False, indent=1), encoding="utf-8")
    if a.dry_run:
        if a.out:
            Path(a.out).write_text(json.dumps({"added": added, "missing": missing}, ensure_ascii=False, indent=1), encoding="utf-8")
        return 0
    records.extend(added)
    REVIEWS.write_text(json.dumps(rev, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if not a.no_chembl:
        items = unc["items"] if isinstance(unc, dict) else unc
        open_items = {(i.get("file"), i.get("source")) for i in items}
        for m in missing:
            if (m["file"], UNCERTAIN_SOURCE) in open_items:
                continue
            items.append({"file": m["file"], "drug": m["drug"], "source": UNCERTAIN_SOURCE, "status": "open",
                          "added": a.date, "issue": "Page says mechanism-of-action data is not available; no citable source found",
                          "searched": ["openFDA drug label (US prescribing information)"] +
                                      ([] if a.chembl_down else ["ChEMBL drug mechanism"]),
                          "reason": m["reason"]})
        UNCERTAIN.write_text(json.dumps(unc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
