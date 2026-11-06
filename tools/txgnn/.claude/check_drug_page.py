"""藥物頁固定檢查（規則 2026-10-23 與 pm 鎖定，之後不再改；本版依 pm 對 90dd204 的實作審查修正漏判）。全站 0 錯才算過。

第 1 類（醫療事實）由人看，不在程式內。
第 2 類 已知用途／分數／KG
  P1 front matter predicted_indications＝kept（順序、內容；可解析多行 YAML）、indication_count＝len(kept)；
     已知用途頁／無預測頁 kept 必須是空的、count 0、evidence_level N/A
  P2 頁面上所有預測分數（表格與本文；0–1 小數或 0–100 百分比）都屬於 kept 的分數且 ≥0.99
  P3 被排除的病名（證據包 ≥0.99 前 10 但不在 kept）以英文或該站當地病名（站內頁面／search-index 的「當地名 (English)」對照）
     出現在 H1、description、概覽表「預測新適應症」列（依列標題）、帶分數的預測列 → 錯；已知用途頁只豁免已知用途表
  P4 每個標 L1–L4 的預測（逐列對應各自的預測），證據包 clinical_trials／ictrp_trials／literature（相容 pubmed_articles、pubmed）
     至少一筆直接研究該病（regen gate 的 direct_evidence）
  P5 KG 不是預測／分數來源：逐句判斷（句界＝句號等後接空白或換行，數字小數點不算）；
     k_findings_patterns.tsv 各語言句型、或同句同時有 KG 詞（含縮寫 KG）與分數／預測／排名詞、或 KG_AS_PRED；同句命中 ok_exempt 不算
  P6 分數不寫成百分比（%、％、٪，含阿拉伯數字），表格與本文都查；分數同一行不得出現信心類字眼
  P7 FHIR ClinicalUseDefinition 與 search-index.json 的預測＝kept（病名正規化後比對）、分數 ≥0.99；
     找不到 MedicationKnowledge 要報錯；FHIR 不得寫「TxGNN Knowledge Graph」
  P3 另含：因門檻／刷新移除（非已知用途）的預測，正文仍當預測或給分數（英文、當地名、頁內縮寫；pm C6）；
     H1、description 的主預測必須是 kept[0]
  K1 已知用途頁：依分區（核准／同類別／KG）判斷，只有 KG 或同類別出處的條目不得放在核准區
第 3 類 市場狀態（license_facts；沒有 facts 要報錯）
  M1 本站的狀態列（不是他國狀態列）＝軌 5 字彙；張數列數字＝total／valid（部分紀錄要有「至少」字樣）；
     許可證表裡有效的許可證不得寫成註銷；kr 只檢查狀態列＝Unknown (source lacks cancellation status)
  M2 事實是已註銷／過期／核准未上市，狀態列不得寫成上市中（kr 不查）
  M3 正文（非表格）說全部註銷／沒有有效許可證但事實有效數 >0，或事實全部註銷／未上市但正文說上市中（kr 不查；pm C1）
     M3 擴充（2026-11-05，英文站、M3X_SITES 啟用）：M3a 未上市卻寫有效、M3b 有效卻寫未註冊／查無註冊、M3c 有註銷卻寫全部有效／沒有註銷／有效張數過多
     M3 英文「全部註銷」漏網寫法（2026-11-06，ALLC_X_SITES 啟用：Us，同日加 Eu、NZ、Au、In、Sg、Uk、Ca、Ph、Za）：all／both／the／only／sole … listings／records／BLAs … cancelled、
     「The US licences are all cancelled」「the cancelled US market status」、另有 N 張註銷但 N 多於事實、點名的申請號其實有效（all_cancel_x）
     M3 英文「總數說法」跟事實不符（2026-11-06，TOTAL_X_SITES，同上 10 站）：In total／overall／Of N records／A of the N／all N／N valid … of N／N … in total 的
     總數、有效、註銷張數跟事實不符（total_x；表格子集合、至少 N、部分紀錄、交互作用筆數不算）
     M3 英文「有效張數」說法跟事實不符（2026-11-06，VALIDX_SITES，同上 10 站）：「with N valid …」「N valid authorizations」「N licences are valid」寫的有效張數
     不等於事實（valid_under；至少 N、部分紀錄、表外另有 N 張、表格列出的 N 張、單方張數不少於事實單方有效張數的不算）
     M3 英文「單方／複方」說法跟事實不符（2026-11-06，COMBO_X_SITES：10 個英文站；Us、Au、In、Ca 修好各站 reviewer 的成分數判定後啟用）：
     寫全部單方／沒有複方但有效許可有複方、寫只有複方但有單方、單方張數多於事實（combo_x）
     M3l 清單站（Uk、NZ、Ph）第四輪（2026-11-06）：說許可資料應去 MHRA／Medsafe／FDA PH 擷取、重跑擷取流程、許可資料／紀錄不完整或尚未載入（LIST_PIPE；仿單缺漏不算）
D1 一頁只能有一份報告（2026-11-03 用戶決定）：報告標題＝H2 後一行是「{: .text-alpha }」；兩個以上就錯
   （過去產生時殘留的第二份舊報告、或模型自己「更正標題」留下的第二個標題；修法見 drop_duplicate_reports_20261103.py）
N1 noindex（--noindex 時才查）：no_pred_noindex 的頁、站上 docs/_data/force_noindex.json 列的頁要有 noindex: true，其他頁不得有
用法（母目錄）：python3 .claude/check_drug_page.py [--selftest] [--noindex] [--pages site:page,...] [站 ...]
輸出 .claude/audit_20261016/check/results.tsv（site, page, code, detail）；有錯 exit 1。
"""
import csv
import importlib.util
import json
import os
import re
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get("CK_OUT", BASE / ".claude/audit_20261016/check"))  # CK_OUT：逐站在雲端跑時各自的輸出目錄（可平行）
RULES = BASE / ".claude/check_rules"


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


kf = _load("kf", BASE / ".claude/known_use_filter.py")
amf = _load("amf", BASE / ".claude/add_monitor_fields.py")
mv2 = _load("mv2", BASE / ".claude/rewrite_market_v2_20261021.py")
rr = _load("rr", BASE / ".claude/regen_run_20261021.py")
kup = _load("kup", BASE / ".claude/known_use_pages_20261022.py")

LANG = dict(mv2.LANG)
for _s in ("AuTxGNN", "EuTxGNN", "InTxGNN", "NZTxGNN", "SgTxGNN", "UkTxGNN", "ZaTxGNN"):
    LANG.setdefault(_s, "en")

# ---------- 文字正規化 ----------
_AR = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹٫٬", "01234567890123456789.,")


def norm_digits(s):
    return (s or "").translate(_AR).replace("％", "%").replace("٪", "%")


def norm_name(s):
    return re.sub(r"\s+", " ", str(s or "").replace(" ", " ")).strip().lower()


def sentences(text):
    """句界：。！？，或 .!? 後接空白／行尾；數字裡的小數點（前後都是數字）不算。"""
    out = []
    for part in text.split("\n"):
        buf = ""
        for i, ch in enumerate(part):
            buf += ch
            nxt = part[i + 1] if i + 1 < len(part) else ""
            if ch in "。！？" or (ch in ".!?" and (nxt == "" or nxt.isspace())):
                out.append(buf.strip()); buf = ""
        if buf.strip():
            out.append(buf.strip())
    return [s for s in out if s]


# ---------- P5 ----------
_rows = list(csv.DictReader(open(RULES / "k_findings_patterns.tsv", encoding="utf-8"), delimiter="\t"))
KG_WORD = re.compile(next(r["pattern"] for r in _rows if r["lang"] == "any").replace("(?i)", "") +
                     r"|\bgraph(?:s|e|es|en)?\b|\bGraph-|\bgrafo(?:s)?\b|\bgrafi\b|\bgraf(?:en|et)?\b|\bgraaf\b|圖譜|图谱|グラフ|그래프|กราฟ|الرسم البياني|رسم بياني", re.I)
KG_ABBR = re.compile(r"(?<![A-Za-z])(?<!Co\. )(?<!Co )(?<!& )KG(?![A-Za-z])")  # 2026-10-29：「GmbH & Co. KG」是公司型態，不是知識圖譜
# GNN 的說法不是知識圖譜（「graph neural network」等）：判斷 KG 詞前先拿掉
GNN_PHRASE = re.compile(r"graph[- ]?neural[- ]?network\w*|graph[- ]based neural|\bGNN\b|graphbasiert\w* neuronal\w*|Graph-Neuronal\w*|"
                        r"graphbaserede? neurale|graafineuroverk\w*|grafneural\w*|grafnevral\w*|grafbaserade? neurala|"
                        r"red(es)? neuronal(es)? de grafos|rede(s)? neura(l|is) de grafos|réseaux? de neurones sur graphes|reti neurali a grafo|"
                        r"graph neural|圖神經網路|图神经网络|グラフニューラルネットワーク|그래프 신경망|rangkaian neural graf|الشبكة العصبية البيانية|"
                        r"الشبكات العصبية الرسومية|شبكة عصبية رسومية|โครงข่ายประสาทเทียมแบบกราฟ|Graph Neural Network", re.I)
OK_EXEMPT = re.compile(next(r["pattern"] for r in _rows if r["lang"] == "ok_exempt"))
KPAT = defaultdict(list)
for r in _rows:
    if r["lang"] not in ("any", "ok_exempt"):
        KPAT[r["lang"]].append((re.compile(r["pattern"]), r.get("fix_hint", "")))
SCORE_OR_PRED = re.compile(r"scor\w*|\bpunt\w*|\bpontua\w*|\bpunteggi\w*|\bpistem\w*|\bpoäng\w*|\bpoeng\w*|\bskor\w*|\bWert\w*|"
                           r"\bpredict\w*|\bprédi\w*|\bprevis\w*|\bpredic\w*|\bprevist\w*|\bvorhersag\w*|\bvoorspel\w*|\bprediks\w*|"
                           r"\bpredikt\w*|\bforudsig\w*|\bennust\w*|\bramal\w*|\bförutsäg\w*|\bförutsag\w*|"
                           r"分數|分数|スコア|점수|درجة|คะแนน|預測|预测|予測|예측|التنبؤ|تنبؤ|คาดการณ์|ทำนาย|"
                           # 2026-10-23（pm 對抗句）：排名／候選類
                           r"\brank\w*|\bcandidat\w*|\bRang\w*|\bKandidat\w*|\bclassement\w*|\bclasificaci\w*|\bclassifica\w*|"
                           r"\brangering\w*|\bsijoitu\w*|\behdok\w*|\bperingkat\w*|\bcalon\w*|順位|候補|排名|候選|候选|순위|후보|"
                           r"الترتيب|مرشح|อันดับ|ผู้สมัคร", re.I)
KG_AS_PRED = rr.KG_AS_PRED
# ok_exempt 的「已知用途」例外補各語言說法（2026-10-23 Sg alendronic_acid「The one known use … recorded in the knowledge graph」誤判）
KNOWN_USE_OK = re.compile(r"recorded|registrad[oa]s?|registrert|verzeichnet|enregistr|registrat[ae]|geregistreerd|registreret|registrerad|"
                          r"kirjattu|direkodkan|記錄|记录|記録|기록된|기록|المسجلة|مسجلة|บันทึก|known use|已知用途|既知の用途|既知用途|기존 용도|알려진 용도|uso conocido|usos conocidos|uso conhecido|usos conhecidos|"
                          r"usage connu|usages connus|uso noto|usi noti|bekannte Anwendung|kendt anvendelse|kendte anvendelser|kjent bruk|"
                          r"känd användning|kända användningar|tunnettu käyttö|tunnetut käytöt|bekend gebruik|kegunaan (yang )?diketahui|"
                          r"الاستخدامات المعروفة|استخدام معروف|การใช้ที่ทราบ", re.I)
LANG2 = {"en-us": "en"}


SCORE_PRED_STRICT = re.compile(r"scor\w*|\bpunt\w*|\bpontua\w*|\bpunteggi\w*|\bpistem\w*|\bpoäng\w*|\bpoeng\w*|\bskor\w*|"
                               r"\bpredict\w*|\bprédi\w*|\bprevis\w*|\bpredic\w*|\bprevist\w*|\bvorhersag\w*|\bvoorspel\w*|\bprediks\w*|"
                               r"\bpredikt\w*|\bforudsig\w*|\bennust\w*|\bramal\w*|\bförutsäg\w*|\bförutsag\w*|"
                               r"分數|分数|スコア|점수|درجة|คะแนน|預測|预测|予測|예측|التنبؤ|تنبؤ|คาดการณ์|ทำนาย", re.I)


CONTRA_OK = re.compile(r"موانع الاستعمال|موانع|ข้อห้ามใช้|금기|禁忌|vasta-aihe|kontraindikation|contraindicatie|kontraindikasjon|"
                       r"kontraindikation|controindicazion|contre-indication|contraindicaç|contraindicaci|Gegenanzeige|tegenindicatie", re.I)
SCORE_ONLY = re.compile(r"scor\w*|\bpunt\w*|\bpontua\w*|\bpunteggi\w*|\bpistem\w*|\bpoäng\w*|\bpoeng\w*|\bskor\w*|"
                        r"分數|分数|スコア|점수|درجة|คะแนน", re.I)


# 2026-10-23 pm（A 案）：KG 當成禁忌／注意／安全關聯的來源是允許的。同句有這類字、或位在這類小節標題底下，
# 而且同句沒有分數數字、沒有預測或分數字樣 → 豁免（連字號有無都收，18 語）
SAFETY_OK = re.compile(r"contra-?indic|kontra-?indik|kontraindikasjon|vasta-?aihe|Gegenanzeige|tegen-?indicatie|controindic|contre-?indic|"
                       r"contraindica|contra-?indica|caution|precaution|précaution|precauci[oó]n|precauç|precauzion|cautela|cuidado|"
                       r"Vorsicht|Warnhinweis|Sicherheit|voorzichtig|aandachtspunt|bijsluitertekst|veiligheid|waarschuwing|"
                       r"forsigtig|advarsel|sikkerhed|sikkerhet|forsiktig|försiktig|varning|säkerhet|varoitus|varovaisuu|turvallisuu|"
                       r"amaran|berhati-?hati|keselamatan|langkah berjaga|safety|warning|avertissement|sécurité|advertencia|seguridad|"
                       r"segurança|advertência|sicurezza|avvertenz|not label text|not (?:in|from) the label|"
                       r"注意事項|注意事项|警告|慎重投与|禁忌|安全性|주의|경고|금기|안전성|ข้อควรระวัง|คำเตือน|ข้อห้าม|ความปลอดภัย|"
                       r"تحذير|احتياط|موانع|السلامة", re.I)


def p5_hits(text, lang, section=""):
    """違規句（逐句）。2026-10-23 pm C2／C3：
    - TSV 各語言 KG 來源句型或 KG_AS_PRED 命中 → 一律算（不看豁免）
    - 否則句中有 KG 詞（含單獨的 graph／grafo／圖譜…、大寫縮寫 KG；GNN 說法先拿掉）就算，
      除非同句是 ok_exempt 情境（排除、訓練資料、禁忌、論文引用；同句沒有分數才成立），
      或已知用途句（KNOWN_USE_OK；同句沒有分數也沒有預測詞才成立）"""
    lg = LANG2.get(lang, lang)
    pats = [p for p, _ in KPAT.get(lg, [])] + ([p for p, _ in KPAT["en"]] if lg != "en" else [])
    out = []
    for line in norm_digits(text).split("\n"):
        line = re.sub(r"\bCo\.?\s*KG\b", "CoKG", line, flags=re.I)  # 公司型態「GmbH & Co. KG」：句點會把 KG 切成獨立一句，先遮掉
        if line.lstrip().startswith("#"):
            section = line
        out += _p5_line(line, pats, section)
    return out


def _p5_line(line, pats, section):
    out = []
    for s0 in sentences(line):
        s = re.sub(r"(\d)[.,](\d)", r"\1\2", s0)  # 句型裡的 [^.\n] 不該被分數的小數點截斷
        if any(p.search(s) for p in pats) or KG_AS_PRED.search(s):
            out.append(s0); continue
        s2 = GNN_PHRASE.sub(" ", s0)
        if not (KG_WORD.search(s2) or KG_ABBR.search(s2)):
            continue
        num = bool(score_tokens(s0))
        if (OK_EXEMPT.search(s0) or CONTRA_OK.search(s0)) and not (num or SCORE_ONLY.search(s2)):
            continue  # 排除／訓練資料／禁忌／論文引用情境：同句沒有分數才豁免
        if KNOWN_USE_OK.search(s0) and not (num or SCORE_PRED_STRICT.search(s2)):
            continue  # 已知用途句：同句沒有分數也沒有預測詞才豁免（C3）
        if (SAFETY_OK.search(s0) or (section and SAFETY_OK.search(section))) and not (num or SCORE_PRED_STRICT.search(s2)):
            continue  # 禁忌／注意／安全關聯（句中字詞或小節標題）：同句沒有分數也沒有預測／分數字樣才豁免（pm A 案）
        out.append(s0)
    return out


# ---------- 分數（P2、P6） ----------
NUM_PCT = re.compile(r"(?<![\d.,])(\d{1,3}(?:[.,]\d+)?)\s?%")
NUM_DEC = re.compile(r"(?<![\d.,])([01][.,]\d{2,6})(?![\d%])")
CONF = re.compile(r"confiden|confianza|confiança|confiance|confidenza|fiducia|Konfidenz|Zuversicht|fiabilité|betrouwbaar|tillförlit|"
                  r"tillit|pålitelig|pålidelig|luotettav|varmuus|keyakinan|信心|信賴|可信度|信頼度|確信|신뢰도|확신|ความเชื่อมั่น|ثقة|"
                  r"certainty|certeza", re.I)
SCORE_HDR = re.compile(r"scor\w*|\bpunt\w*|\bpontua\w*|\bpunteggi\w*|\bpistem\w*|\bpoäng\w*|\bpoeng\w*|\bskor\w*|Wert|"
                       r"分數|分数|スコア|점수|درجة|คะแนน", re.I)
SCORE_CTX = re.compile(SCORE_HDR.pattern + r"|TxGNN", re.I)


THRESHOLD = re.compile(r"(≥|≧|>=|>|⩾|at least|no less than|mindestens|au moins|al menos|pelo menos|almeno|vähintään|minst|mindst|"
                       r"minstens|sekurang-kurangnya|至少|以上|이상|على الأقل|อย่างน้อย)\s*$", re.I)


def score_tokens(text):
    """[(值 0–1, 是否百分比, 原字串)]；門檻寫法（≥ 0.99、至少 0.99、0.99 以上）不算分數"""
    t = norm_digits(text)
    _thr = r"(?:0[.,]99(?![\d])|99(?:[.,]0+)?\s?%)"  # 2026-10-23 pm C4：只豁免 0.99／99% 本身
    t = re.sub(r"(?<![\d.,])" + _thr + r"\s*(以上|이상|or (higher|above|more|greater)|eller högre|eller højere|eller høyere|eller mer|oder (höher|mehr)|ou plus|"
                                           r"ou (mais|superior)|o (más|superior|superiore|più)|tai (enemmän|yli|korkeampi)|of (hoger|meer)|"
                                           r"atau (lebih|ke atas)|หรือ(มากกว่า|สูงกว่า)|أو أكثر|أو أعلى|以上)", " ", t, flags=re.I)
    t = re.sub(r"(≥|≧|>=|>|⩾|at least|no less than|above|over|greater than|higher than|über|au-dessus de|supérieur à|por encima de|superior a|"
               r"acima de|sopra|yli|över|boven|melebihi|เกิน|أعلى من|mindestens|au moins|al menos|pelo menos|almeno|vähintään|minst|mindst|minstens|"
               r"sekurang-kurangnya|至少|이상|على الأقل|อย่างน้อย|igual ou superior a|igual o superior a|igual o mayor (?:a|que)|"
               r"pari o superiore a|supérieur ou égal à|supérieure ou égale à|größer oder gleich|gleich oder größer als|"
               r"lika med eller högre än|lik eller høyere enn|lig med eller højere end|yhtä suuri tai suurempi kuin|"
               r"gelijk aan of hoger dan|ไม่น้อยกว่า|لا تقل عن)\s*" + _thr, " ", t, flags=re.I)
    out = []
    for m in NUM_PCT.finditer(t):
        v = float(m.group(1).replace(",", ".")) / 100
        if 0 <= v <= 1:
            out.append((v, True, m.group(0)))
    for m in NUM_DEC.finditer(t):
        v = float(m.group(1).replace(",", "."))
        if 0 <= v <= 1:
            out.append((v, False, m.group(0)))
    return out


def matches_kept(v, kept_sc):
    return v >= 0.99 and any(abs(v - k) < 0.00005 or abs(round(k * 100, 2) - v * 100) < 0.005 or abs(round(k, 4) - v) < 0.00005
                             for k in kept_sc)


# ---------- 表格 ----------
def tables(body):
    """[(header_cells, [row_cells], [row_lines], 表格前最近的標題)]"""
    out, cur, head = [], None, ""
    for line in body.split("\n"):
        if line.startswith("#"):
            head = line
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cur is None:
                cur = [cells, [], [], head]
            elif re.fullmatch(r"[\s|:\-]+", line):
                continue
            else:
                cur[1].append(cells); cur[2].append(line)
        elif cur:
            out.append(tuple(cur)); cur = None
    if cur:
        out.append(tuple(cur))
    return out


_NEW = r"(new|nueva|nova|neue|\bny\b|uusi|nouvelle|nuova|baharu|nieuwe|新|신규|الجديد|ใหม่)"
_PRD = r"(predict|predich|previst|vorhergesagt|forudsagt|ennustettu|prédite|prevista|diramal|voorspeld|predikert|förutsagd|預測|予測|예측|المتوقع|ทำนาย|คาดการณ์)"
PCT_SCORE = re.compile(r"[（(]\s*9\d[.,]\d{2}\s?[%％٪]|(?<![\d.,])99[.,]\d{2}\s?[%％٪]")
PRED_ROW = re.compile(_NEW + ".*" + _PRD + "|" + _PRD + ".*" + _NEW, re.I)
# 概覽表「原適應症」列（欄名規則同 drug_meta_description.ORIG_LABEL）
ORIG_ROW = re.compile(r"Original|originaria|originario|Alkuperäinen|原適應症|既存適応症|Ursprüngliche|origen|d.origine|originale|Opprinnelig|Ursprunglig|Oprindelig|Oorspronkelijke|الأصلي|기존 적응증|asal|เดิม", re.I)
LEVEL_ROW = re.compile(r"evidenc|evidên|evidenz|evidens|preuve|evidenza|näytön|bewijs|bukti|証據|證據|エビデンス|근거|الأدلة|หลักฐาน", re.I)
LEVEL = re.compile(r"(?<![A-Za-z0-9])\**(L[1-5])\**(?![A-Za-z0-9])")
LIC_WORD = re.compile(r"licen|label|authori[sz]|\bARTG\b|\bDINs?\b|\bAMM\b|\bNDAs?\b|許可證|仿單|承認|添付文書|허가|Zulassung|Fachinformation|"
                      r"autoriza|registro|registr|autorizzazion|myyntilup|valmisteyhteenveto|markedsføringstilladelse|produktresumé|"
                      r"godkjenning|godkännande|vergunning|bijsluiter|pendaftaran|ترخيص|تراخيص|نشرة|ทะเบียน|ใบอนุญาต|เอกสารกำกับ|\bBNF\b|"
                      r"marketed products", re.I)
OWN = {"ARTxGNN": r"argentin", "AuTxGNN": r"australi|ARTG", "BrTxGNN": r"brasil|brazil", "CHTxGNN": r"schweiz|swiss|switzerland",
       "COTxGNN": r"colombi", "CaTxGNN": r"canad", "DETxGNN": r"deutschland|german", "DkTxGNN": r"danmark|denmark|dansk",
       "ESTxGNN": r"españa|spain|español", "EuTxGNN": r"\bEU\b|europ|\bEMA\b", "FITxGNN": r"suom|finland", "FRTxGNN": r"france|français",
       "HkTxGNN": r"香港|hong kong", "ITTxGNN": r"itali", "InTxGNN": r"india", "JpTxGNN": r"日本|国内|japan", "KrTxGNN": r"한국|국내|korea",
       "MyTxGNN": r"malaysia", "NOTxGNN": r"norge|norway|norsk", "NZTxGNN": r"new zealand|\bNZ\b", "NlTxGNN": r"nederland|netherlands",
       "PhTxGNN": r"philippin", "SATxGNN": r"السعودية|saudi", "SETxGNN": r"sverige|sweden|svensk", "SgTxGNN": r"singapore|\bHSA\b",
       "ThTxGNN": r"ไทย|thai", "TwTxGNN": r"台灣|臺灣|taiwan|國內", "UkTxGNN": r"\bUK\b|united kingdom|britain|\bNHS\b",
       "UsTxGNN": r"\bUS\b|united states|U\.S\.|\bFDA\b", "ZaTxGNN": r"south africa|SAHPRA"}
FOREIGN_ANY = re.compile(r"taiwan|台灣|臺灣|japan|日本|korea|한국|deutschland|germany|france|españa|spain|italia|ital|brasil|brazil|argentin|"
                         r"colombi|canad|australi|new zealand|india|malaysia|singapore|philippin|thai|ไทย|saudi|السعودية|sverige|sweden|norge|"
                         r"norway|danmark|denmark|suom|finland|nederland|netherlands|schweiz|switzerland|hong kong|香港|united kingdom|\bUK\b|"
                         r"united states|\bUS\b|south africa|\bEU\b|europ", re.I)
# 核准未上市（各語言；軌 5 v5 寫入用同一份）
NOT_MKT = {"en": "Approved but not marketed (approvals on record: {n})", "en-us": "Approved but not marketed (approvals on record: {n})",
           "es": "Autorizado pero no comercializado (registros: {n})", "pt": "Aprovado, mas não comercializado (registros: {n})",
           "de": "Zugelassen, aber nicht im Handel (Zulassungen: {n})", "da": "Godkendt, men ikke markedsført (tilladelser: {n})",
           "fi": "Hyväksytty, mutta ei markkinoilla (lupia: {n})", "fr": "Autorisé mais non commercialisé (autorisations : {n})",
           "zh": "已核准但未上市（許可證 {n} 張）", "it": "Autorizzato ma non in commercio (autorizzazioni: {n})",
           "ja": "承認済み・未販売（承認 {n} 件）", "ko": "허가되었으나 미시판 (허가 {n}건)",
           "ms": "Diluluskan tetapi tidak dipasarkan (pendaftaran: {n})", "nl": "Goedgekeurd, maar niet in de handel (vergunningen: {n})",
           "no": "Godkjent, men ikke markedsført (godkjenninger: {n})", "ar": "معتمد ولكنه غير مسوَّق (التراخيص: {n})",
           "sv": "Godkänd men inte marknadsförd (godkännanden: {n})", "th": "ได้รับอนุมัติแต่ยังไม่วางจำหน่าย (ทะเบียน {n} รายการ)"}
# 全部註銷／查無許可證（各語言；軌 5 v5 寫入用同一份；都含 NEG 字樣，M2 不會誤判成上市中）
CANCELLED = {"en": "Not marketed (licences cancelled: {n} of {n})",
"en-us": "Not marketed (licenses canceled: {n} of {n})",
"es": "No comercializado (registros anulados: {n} de {n})",
"pt": "Não comercializado (registros cancelados: {n} de {n})",
"de": "Nicht im Handel (erloschene Zulassungen: {n} von {n})",
"da": "Ikke markedsført (afregistrerede tilladelser: {n} af {n})",
"fi": "Ei markkinoilla (perutut luvat: {n}/{n})",
"fr": "Non commercialisé (autorisations annulées : {n} sur {n})",
"zh": "未上市（已註銷許可證 {n} 張／共 {n} 張）",
"it": "Non in commercio (autorizzazioni revocate: {n} su {n})",
"ja": "販売なし（承認 {n} 件すべて取消・整理済み）",
"ko": "미시판 (취소된 허가 {n}건 / 전체 {n}건)",
"ms": "Tidak dipasarkan (pendaftaran dibatalkan: {n} daripada {n})",
"nl": "Niet in de handel (ingetrokken vergunningen: {n} van {n})",
"no": "Ikke markedsført (avregistrerte godkjenninger: {n} av {n})",
"ar": "غير مسوق (أُلغيت جميع التراخيص، وعددها {n})",
"sv": "Inte marknadsförd (avregistrerade godkännanden: {n} av {n})",
"th": "ไม่มีจำหน่าย (ทะเบียนที่ถูกยกเลิก {n} จาก {n} รายการ)"}
# 2026-10-30（pm 選 b）：DE、FI、NO 的許可證來源只有 EMA 集中許可，沒有國家級許可（BfArM、Fimea、DMP）。
# 這三站「查無許可紀錄」時不能寫「未上市」（沒有資料可以證明），狀態列只陳述資料範圍。
NO_CENTRAL = {
    "DETxGNN": "Keine zentrale EU-Zulassung (EMA) erfasst – nationale Zulassungen (BfArM) sind in den hier ausgewerteten Daten nicht enthalten",
    "FITxGNN": "Keskitettyä EU-myyntilupaa (EMA) ei ole kirjattu – kansallisia myyntilupia (Fimea) ei ole tässä käytetyissä tiedoissa",
    "NOTxGNN": "Ingen sentral EU-godkjenning (EMA) registrert – nasjonale markedsføringstillatelser (DMP) finnes ikke i dataene som er brukt her",
    # 2026-10-31：TH 的來源是 Thai FDA 查詢系統（只收ทะเบียนตำรับยาแผนปัจจุบัน），查不到不等於沒有藥（例：morphine 在國家基本藥物目錄裡）
    "ThTxGNN": "ไม่พบทะเบียนตำรับยาในระบบค้นหาข้อมูลผลิตภัณฑ์ยาของ อย.",
    # 2026-10-31（pm）：JP 的來源是藥價基準收載醫藥品マスター，不收 OTC 等未收載品目，查不到不等於國內未承認
    "JpTxGNN": "本サイトのデータ（薬価基準収載医薬品マスター）に該当品目なし（国内の承認状況は未確認）",
    # 2026-11-06（用戶決定）：SG 的來源是 HSA 現行註冊清單（data.gov.sg，只列現行註冊），不在清單不等於沒有藥；
    # EU 的來源只有 EMA 集中許可，各會員國的國家許可不在資料裡。兩站都只陳述資料範圍，不寫 Not marketed
    "UkTxGNN": "Not listed in the NHSBSA BNF prescribing code list – MHRA licence status is not included in this data",
    "NZTxGNN": "Not listed on the Pharmac Pharmaceutical Schedule (Community Medicines) – Medsafe licence status is not included in this data",
    "PhTxGNN": "Not listed in the Philippine National Formulary (PNF) Essential Medicines List – FDA Philippines registration status is not included in this data",
    "SgTxGNN": "Not in the current HSA register of therapeutic products (data.gov.sg listing) – registrations no longer listed are not included in this data",
    "EuTxGNN": "No EMA central authorisation on record – national authorisations in EU member states are not included in this data",
}


# 2026-10-30（用戶選「沿用現有來源排程」）：這些站的「本地資料」不是主管機關許可證資料，狀態列照實陳述來源，
# 不寫成「已許可、上市中」。{v}／{n}＝在列筆數（同原本的有效／總數）；部分紀錄用第二個模板。
SOURCE_STATUS = {
    # 2026-11-06（用戶決定）：NZ 依成分重建 Pharmac 給付清單筆數；狀態列只陳述資料範圍（給付清單，不含 Medsafe 許可狀態）
    "NZTxGNN": ("Listed on the Pharmac Pharmaceutical Schedule ({n} Community Medicines items) – Medsafe licence status is not included in this data",
                "Listed on the Pharmac Pharmaceutical Schedule (at least {v} Community Medicines items) – Medsafe licence status is not included in this data"),
    # 2026-11-06（用戶決定）：UK 依成分重建 BNF 處方代碼清單筆數；狀態列只陳述資料範圍（處方代碼清單，不含 MHRA 許可狀態）
    "UkTxGNN": ("Listed in the NHSBSA BNF prescribing code list ({n} presentation codes) – MHRA licence status is not included in this data",
                "Listed in the NHSBSA BNF prescribing code list (at least {v} presentation codes) – MHRA licence status is not included in this data"),
    "ARTxGNN": ("Incluido en el listado de medicamentos de PAMI ({v} de {n}) – el estado del registro en ANMAT no está incluido en estos datos",
                "Incluido en el listado de medicamentos de PAMI (al menos {v}) – el estado del registro en ANMAT no está incluido en estos datos"),
    "AuTxGNN": ("Listed on the PBS Schedule ({v} of {n} items) – TGA (ARTG) registration status is not included in this data",
                "Listed on the PBS Schedule (at least {v} items) – TGA (ARTG) registration status is not included in this data"),
    "InTxGNN": ("Listed in a compiled Indian medicine price dataset ({v} of {n}) – CDSCO approval status is not included in this data",
                "Listed in a compiled Indian medicine price dataset (at least {v}) – CDSCO approval status is not included in this data"),
    # 2026-11-06（用戶決定）：PH 依成分重建 PNF 品項數（PNF-EML 2022）；狀態列只陳述資料範圍（處方集，不含 FDA Philippines 註冊狀態）
    "PhTxGNN": ("Listed in the Philippine National Formulary (PNF entries: {n}) – FDA Philippines registration status is not included in this data",
                "Listed in the Philippine National Formulary (PNF entries: at least {v}) – FDA Philippines registration status is not included in this data"),
}
# TH 2026-10-31 移出：原本的許可證號是程式編造的，改用 Thai FDA 查詢系統（pertento）的真實許可證，狀態列回到一般寫法


# 狀態未知的許可（My 2026-11-05 用戶決定）：fc["unknown"]＝現行與撤銷清單都查不到、也還沒到期的登記號數，不算有效也不算註銷；
# 狀態列與張數列另列一項。沒有有效許可、但有狀態未知的 → 市場狀態「Status unknown」（不寫成已註銷）
UNKNOWN_ST = {"MyTxGNN": {"extra": "; status tidak dapat disahkan: {u}", "count": "{n} (sah: {v}; status tidak dapat disahkan: {u})",
                          "only": "Status tidak dapat disahkan (pendaftaran: {n}; sah: 0; dibatalkan atau tamat tempoh: {c}; status tidak dapat disahkan: {u})"}}


def unknown_status_text(site, lang, fc):
    cfg = UNKNOWN_ST.get(site)
    return cfg["only"].format(n=fc.get("total"), c=fc.get("cancelled") or 0, u=fc.get("unknown") or 0) if cfg else None


# 狀態未經主管機關確認、但照樣算有效的許可（Za 2026-11-06 用戶決定）：fc["unconfirmed"]＝只在 MPR 價格登錄有、SAHPRA 匯出查不到的
# 有效註冊數（含在 valid 裡，不是另一種狀態）。狀態列與張數列加註，許可證表該列狀態格寫「Valid (status not confirmed by SAHPRA)」
UNCONFIRMED_ST = {"ZaTxGNN": {"extra": "; {u} of the valid not confirmed by SAHPRA", "count": "{n} (valid: {v}, of which {u} not confirmed by SAHPRA)"}}


def _with_unknown(site, text, fc):
    cfg = UNKNOWN_ST.get(site)
    if cfg and fc and (fc.get("unknown") or 0) and text.endswith(")"):
        return text[:-1] + cfg["extra"].format(u=fc["unknown"]) + ")"
    cfg = UNCONFIRMED_ST.get(site)
    if cfg and fc and (fc.get("unconfirmed") or 0) and not fc.get("partial") and text.endswith(")"):
        return text[:-1] + cfg["extra"].format(u=fc["unconfirmed"]) + ")"
    return text


def marketed_text(site, lang, v, n, partial, fc=None):
    """事實是 Marketed 時的狀態列：來源不是許可證資料的站用 SOURCE_STATUS，SPLIT_STATUS 的站分開寫核准未上市／註銷，其他站用 mv2.T"""
    if site in SPLIT_STATUS:
        cfg = SPLIT_STATUS[site]
        if "fn" in cfg:
            return cfg["fn"](v, n, partial, fc)
        return cfg["part" if partial else "full"].format(v=v, n=n, extra=_split_extra(cfg, fc))
    if site in SOURCE_STATUS:
        return SOURCE_STATUS[site][1 if partial else 0].format(v=v, n=n)
    tl = mv2.T.get(lang) or mv2.T["en"]
    return _with_unknown(site, (tl[1] if partial else tl[0]).format(v=v, n=n), fc)


# 2026-10-30（pm）：概覽表本站狀態列／張數列的標準欄位名（各站主流寫法；主流寫法不準確的修正：US 不只 NDA、
# 來源不是許可證資料的站照實寫來源）。Tw 由 Tw 自己的 tfda 程式產生，不在此表。
MARKET_LABELS = {
    "ARTxGNN": ("Estado de Mercado en Argentina", "Número de productos en el listado PAMI"),
    "AuTxGNN": ("Australia Market Status", "Number of PBS Items"),
    "BrTxGNN": ("Situação no Mercado Brasileiro", "Número de Registros"),
    "CHTxGNN": ("Marktstatus Schweiz", "Anzahl Zulassungen"),
    "COTxGNN": ("Estado de Mercado en Colombia", "Número de Registros Sanitarios"),
    "CaTxGNN": ("Canada Market Status", "Number of DINs"),
    "DETxGNN": ("Marktstatus in Deutschland", "Anzahl der Zulassungen"),
    "DkTxGNN": ("Markedsstatus i Danmark", "Antal markedsføringstilladelser"),
    "ESTxGNN": ("Estado de Mercado en España", "Número de Autorizaciones"),
    "EuTxGNN": ("EU Market Status", "Number of Authorizations"),
    "FITxGNN": ("Markkinatilanne Suomessa", "Myyntilupien määrä"),
    "FRTxGNN": ("Statut de Marché en France", "Nombre d'AMM"),
    "HkTxGNN": ("香港上市", "許可證數"),
    "ITTxGNN": ("Stato di mercato in Italia", "Numero di autorizzazioni"),
    "InTxGNN": ("India Market Status", "Number of Listed Products"),
    "JpTxGNN": ("日本市販状況", "承認番号数"),
    "KrTxGNN": ("한국 시판 현황", "허가증 수"),
    "MyTxGNN": ("Status Pasaran di Malaysia", "Bilangan Pendaftaran"),
    "NOTxGNN": ("Markedsstatus i Norge", "Antall godkjenninger"),
    "NZTxGNN": ("New Zealand Market Status", "Number of Pharmac Schedule Items"),
    "NlTxGNN": ("Marktstatus in Nederland", "Aantal vergunningen"),
    "PhTxGNN": ("Philippines Market Status", "Number of PNF Entries"),
    "SATxGNN": ("حالة السوق في السعودية", "عدد التراخيص"),
    "SETxGNN": ("Marknadsstatus i Sverige", "Antal godkännanden"),
    "SgTxGNN": ("Singapore Market Status", "Number of Registrations"),
    "ThTxGNN": ("สถานะการวางจำหน่ายในไทย", "จำนวนทะเบียนตำรับยา"),
    "UkTxGNN": ("UK Market Status", "Number of BNF Presentation Codes"),
    "UsTxGNN": ("US Market Status", "Number of FDA Applications"),
    "ZaTxGNN": ("South Africa Market Status", "Number of SAHPRA Registrations"),
}


# 2026-10-31：TH 的許可證來源是 Thai FDA 公開查詢系統（ระบบค้นหาข้อมูลผลิตภัณฑ์ยา，只收「ทะเบียนตำรับยาแผนปัจจุบัน」）。
# 查到的許可證全部已註銷時，只陳述查詢結果，不寫「未上市」：diazepam、lorazepam 等在國家基本藥物目錄裡，但這個系統裡的許可證都已註銷。
# DE、FI、NO 同理（NO_CENTRAL 的延伸）：只有 EMA 集中許可，集中許可撤銷不等於國內沒有藥，只陳述集中許可已撤銷與資料範圍。
SCOPE_CANCELLED = {
    "ThTxGNN": "ไม่พบทะเบียนที่ยังมีผลในระบบค้นหาข้อมูลผลิตภัณฑ์ยาของ อย. (ทะเบียนที่ถูกยกเลิก {n} จาก {n} รายการ)",
    "DETxGNN": "Zentrale EU-Zulassung (EMA) erloschen ({n} von {n}) – nationale Zulassungen (BfArM) sind in den hier ausgewerteten Daten nicht enthalten",
    "FITxGNN": "Keskitetty EU-myyntilupa (EMA) peruttu ({n}/{n}) – kansallisia myyntilupia (Fimea) ei ole tässä käytetyissä tiedoissa",
    "NOTxGNN": "Sentral EU-godkjenning (EMA) avregistrert ({n} av {n}) – nasjonale markedsføringstillatelser (DMP) finnes ikke i dataene som er brukt her",
    "EuTxGNN": "No valid EMA central authorisation (withdrawn, lapsed or expired: {n} of {n}) – national authorisations in EU member states are not included in this data",
}
# 只陳述資料範圍的站（NO_CENTRAL／SCOPE_CANCELLED），事實是查無或全部註銷時，正文斷言「在本國／歐盟沒有上市、買不到」超出資料範圍（2026-11-06，Sg、Eu）
SCOPE_NOMKT = {
    "SgTxGNN": re.compile(r"\bnot (currently |yet )?(marketed|available|sold|launched)\b[^.;]{0,25}\b(in Singapore|locally|on the (Singapore|local) market)\b|"
                          r"\bno longer (marketed|available|sold)\b[^.;]{0,25}\b(in Singapore|locally)\b|\b(unavailable|off the market) in Singapore\b|"
                          r"\bnot on the (Singapore|local) market\b", re.I),
    "EuTxGNN": re.compile(r"\bnot (currently |yet )?(marketed|available|sold|authori[sz]ed|launched)\b[^.;]{0,25}\b(in (the )?(EU|European Union|Europe|EEA))\b|"
                          r"\bno longer (marketed|available|sold|authori[sz]ed)\b[^.;]{0,25}\b(in (the )?(EU|European Union|Europe|EEA))\b|"
                          r"\b(unavailable|off the market) in (the )?(EU|European Union|Europe)\b|\bnot on the (EU|European) market\b", re.I),
}


def cancelled_text(site, lang, n):
    """事實是 Cancelled only 時的狀態列"""
    return (SCOPE_CANCELLED.get(site) or CANCELLED.get(lang, CANCELLED["en"])).format(n=n)


# 只有獸用許可（人用 0 張）時的狀態列（2026-11-05，用戶決定；Dk 依 ATC Q 開頭或品名含 Vet. 分出獸用，證據包 veterinary_records）
VET_ONLY = {"DkTxGNN": "Kun godkendt som veterinærlægemiddel"}


def not_reg_text(site, lang, fc=None):
    """查無許可紀錄時的狀態列：EMA 代理站用資料範圍句，只有獸用許可的站用 VET_ONLY，其他站用 NOT_REG"""
    if site in VET_ONLY and fc and (fc.get("veterinary") or 0) > 0:
        return VET_ONLY[site]
    return NO_CENTRAL.get(site) or NOT_REG.get(lang, NOT_REG["en"])


NOT_REG = {"en": "Not marketed (no licence on record)",
"en-us": "Not marketed (no license on record)",
"es": "No comercializado (sin registro)",
"pt": "Não comercializado (sem registro)",
"de": "Nicht im Handel (keine Zulassung erfasst)",
"da": "Ikke markedsført (ingen tilladelse registreret)",
"fi": "Ei markkinoilla (ei lupaa rekisterissä)",
"fr": "Non commercialisé (aucune autorisation enregistrée)",
"zh": "未上市（查無許可證）",
"it": "Non in commercio (nessuna autorizzazione registrata)",
"ja": "国内未承認（承認記録なし）",
"ko": "미시판 (허가 기록 없음)",
"ms": "Tidak dipasarkan (tiada pendaftaran direkodkan)",
"nl": "Niet in de handel (geen vergunning geregistreerd)",
"no": "Ikke markedsført (ingen godkjenning registrert)",
"ar": "غير مسوق (لا يوجد ترخيص مسجل)",
"sv": "Inte marknadsförd (inget godkännande registrerat)",
"th": "ไม่มีจำหน่าย (ไม่พบทะเบียน)"}
KR_UNKNOWN = "Unknown (source lacks cancellation status)"  # Kr 舊規則用語（2026-10-31 起 Kr 依 nedrug 註銷狀態，與其他站相同）
# M3（pm C1）：正文說全部註銷／沒有有效許可證，但事實有有效許可證；或事實全部註銷，正文卻說上市中
_LIC = r"(licen[cs]es?|authori[sz]ations?|registrations?|NDAs?|approvals?|registros?|autorizaci\w+|Zulassungen|AMM|autorisations?|" \
       r"autorizzazioni|vergunningen|registraties|tilladelser|godkjenninger|tillatelser|godkännanden|tillstånd|lupa\w*|pendaftaran|التراخيص|تراخيص|ทะเบียน)"
ALL_CANCEL = re.compile(
    r"\b(all|every)\b[^.\n]{0,40}" + _LIC + r"[^.\n]{0,30}\b(cancel+ed|revoked|withdrawn|expired|lapsed|inactive)|"
    r"\bno (currently )?(valid|active) (licen|authori|registration|approval)|\bnone (of them )?(is|are) (valid|active)|"
    r"\btod[oa]s\b[^.\n]{0,40}" + _LIC + r"[^.\n]{0,30}(anulad|cancelad|revocad|caducad|inativ)|ningún registro (vigente|válido)|"
    r"sin registros? vigentes?|nenhum registro (ativo|válido|vigente)|\balle\b[^.\n]{0,40}" + _LIC +
    r"[^.\n]{0,30}(erloschen|widerrufen|zurückgezogen|ingetrokken|doorgehaald|vervallen|afmeldt|afregistrer|tilbagekaldt|avregistrer|tilbakekalt|trukket)|"
    r"keine gültige Zulassung|\btou(tes|s) les?\b[^.\n]{0,40}" + _LIC + r"[^.\n]{0,30}(annulé|abrogé|retiré)|aucune (AMM|autorisation) (valide|active|en vigueur)|"
    r"\btutt[ei]\b[^.\n]{0,40}" + _LIC + r"[^.\n]{0,30}(revocat|annullat|cessat)|nessuna autorizzazione (valida|attiva)|geen geldige vergunning|"
    r"ingen gyldig|\balla\b[^.\n]{0,40}" + _LIC + r"[^.\n]{0,30}(avregistrerade|återkallade)|inga giltiga|\bkaikki\b[^.\n]{0,40}" + _LIC +
    r"[^.\n]{0,30}perut|ei voimassa olevaa lupaa|(全部|皆|均|都)(已)?(註銷|撤銷|失效)|無有效許可證|沒有有效許可證|已無有效|"
    r"すべて(取消|取り消|整理|失効)|有効な承認(は)?(なし|ありません)|모두 취소|유효한 허가(가)? 없|"
    r"\b(kesemua|semua)\b[^.\n]{0,40}pendaftaran[^.\n]{0,30}dibatalkan|tiada pendaftaran (yang )?sah|"
    r"جميع التراخيص[^.\n]{0,40}(ملغا|ملغى|ملغية|أُلغيت|ألغيت)|لا توجد تراخيص سارية|لا يوجد ترخيص ساري|"
    r"(ทั้งหมด|ทุกรายการ)[^.\n]{0,30}ยกเลิก|ไม่มีทะเบียนที่ยังมีผล", re.I)
# 2026-11-06（用戶決定修誤判）：「全部…許可…註銷」那一類（all／todos／alle／toutes／tutti／alla／kaikki／semua…開頭）
# 若「全部」與註銷字之間有否定或有效字樣，講的是「全部有效、沒有註銷」，不是全部註銷
# （「All four licences are valid, and none has been cancelled.」「Todos los registros están vigentes y ninguno fue cancelado.」）
_ALL_LEAD = re.compile(r"^(all|every|tod[oa]s|alle|tou(tes|s)|tutt[ei]|alla|kaikki|kesemua|semua|جميع|ทั้งหมด|ทุกรายการ)\b", re.I)
# 2026-11-06 修 333c1aeb 的漏判：葡萄牙文「no Brasil」的 no 是介系詞（in the），阿拉伯文「لا」原本當子字串比對，
# 「الثلاثة」「الاثنا」裡就有，真正的「全部註銷」（todos os registros no Brasil estão cancelados、جميع التراخيص الثلاثة ملغاة）被當成否定略過。
# 拿掉單獨的 no（英文的「全部有效、沒有註銷」都另有 valid／none 等字），阿拉伯文 لا 要是獨立的詞
_ALL_NEGV = re.compile(r"\b(none|not|neither|nor|never|without|valid|active|current(ly)? (valid|active)|ninguno|ninguna|ningún|ni|sin|vigentes?|"
                       r"válid[oa]s?|nenhum[a]?|ativ[oa]s?|keine?n?|kein|gültig\w*|aucune?|valides?|nessun[oa]?|validi|valide|geen|geldig\w*|"
                       r"ingen|giltig\w*|gyldig\w*|ei|voimassa\w*|tiada|sah)\b|ยังมีผล|ไม่มี|السارية|سارية|(?<!\w)و?لا(?!\w)", re.I)


def all_cancel(s):
    """ALL_CANCEL 命中、且不是「全部有效、沒有註銷」的說法"""
    for m in ALL_CANCEL.finditer(s):
        g = m.group(0)
        if _ALL_LEAD.search(g) and _ALL_NEGV.search(g[3:]):
            continue
        return True
    return False


# 2026-10-31（pm 退件 BR）：「只有註銷的許可」這類說法（沒寫未上市、但說只剩註銷登記），事實有有效許可時跟狀態列矛盾。
# 句中同時提到有效／現行許可（POS_VALID）的不算（例：「2 張註銷、3 張有效」）。單純提到「另有 4 個註銷登記」不算，
# 只抓括號斷言「(registro cancelado)」與「apenas／solo … cancelado」這類「只有」的說法。
ONLY_CANCEL = re.compile(
    r"\bonly\b[^.\n]{0,30}(cancel+ed|revoked|withdrawn|expired|lapsed|inactive)\b|\bno (currently )?(valid|active) product|"
    r"\b(apenas|somente|só)\b[^.\n]{0,30}(cancelad|inativ)|\(registros? cancelados?\)|sem produto (atualmente )?(válido|ativo|vigente)|"
    r"\b(solo|sólo|únicamente)\b\s+(\w+\s+){0,3}(registros?|autorizaci\w+|una autorizaci\w+)[^.\n;]{0,20}(anulad|cancelad|revocad)|\(registros? (anulad|cancelad)[oa]s?\)|sin producto (actualmente )?(válido|vigente)|"
    r"\b(uniquement|seulement)\b[^.\n]{0,30}(annulé|abrogé|retiré)|\bnur\b[^.\n]{0,30}(erloschen|widerrufen|zurückgezogen)|"
    r"\bsolo\b\s+(\w+\s+){0,3}autorizzazion\w*[^.\n;]{0,20}(revocat|annullat|cessat)|\balleen\b[^.\n]{0,30}(ingetrokken|doorgehaald|vervallen)|"
    r"\bendast\b[^.\n]{0,30}(avregistrer|återkall)|\bkun\b[^.\n]{0,30}(avregistrer|afregistrer|tilbakekall|tilbagekald)|"
    r"\bvain\b[^.\n]{0,30}perut|(取消|整理|失効)(済み|された承認)?のみ|취소된 허가(만|뿐)|(僅有|只有|僅存)已?(註銷|撤銷)|"
    r"\bhanya\b[^.\n]{0,30}dibatalkan|فقط[^.\n]{0,30}(ملغا|ملغى|ملغية)|มีเพียง[^.\n]{0,30}ยกเลิก", re.I)
NOT_MKT_CLAIM = re.compile(
    r"\bnot (currently )?marketed\b|\bno longer (marketed|available|has any valid)|\bno longer on the market|"
    r"\bno (longer has any |currently )?valid licen|\bdoes not have any valid|\bhas no valid|"
    r"\bnone of\b[^.\n]{0,40}\b(is|are) (currently )?(valid|active|marketed)|未上市|未在.{0,8}上市|不在.{0,8}上市|"
    r"ikke markedsført|ikke på markedet|nicht im Handel|nicht (mehr )?vermarktet|keine gültige|no (está )?comercializad|"
    r"no se comercializa|não (é |está )?comercializad|non commercialis|n'est pas commercialis|non (è )?in commercio|non commercializzat|"
    r"niet in de handel|inte marknadsförd|ei markkinoilla|tidak dipasarkan|غير مسوق|لا يُسوَّق|ไม่มีจำหน่าย|ไม่ได้วางจำหน่าย|미시판|"
    r"시판되지 않|販売されていない|販売なし|未承認|aucune autorisation valide|ningún registro vigente|nenhum registro (ativo|válido|vigente)|"
    r"nessuna autorizzazione (valida|attiva)|geen geldige|inga giltiga|ingen gyldig|ei voimassa|"
    # 否定詞直接修飾「有效」本身（pm 2026-10-23）
    r"\b(none|no|not a single|not one)\s+(\w+\s+){0,3}(remains?|is|are|was|were)\s+(still\s+|currently\s+)?(valid|active)\b|"
    r"\bno (licen\w+|authori\w+|registration\w*|approval\w*) (is|are|remains?) (still |currently )?(valid|active)|"
    r"沒有(一張|任何)?(許可證)?(是)?有效|無(一張)?有效|有效\s*0\s*張|有效 0|有効\s*0|유효\s*0|vigentes:?\s*0\b|gültig:?\s*0\b|"
    r"valides\s*:?\s*0\b|gyldige:?\s*0\b|\b0 (remain|are|is) (still )?valid", re.I)
# 寬鬆：否定詞與 valid 有距離；同句有正數有效張數時不算
NOT_MKT_LOOSE = re.compile(
    r"\b(none|no|not a single|not one)\b[^.\n]{0,40}\b(valid|active)\b|\bingen\b[^.\n]{0,40}gyldig|\bkeine?\b[^.\n]{0,40}gültig|"
    r"\baucune?\b[^.\n]{0,40}valide|\bningun[oa]?\b[^.\n]{0,40}vigente|\bnenhum[a]?\b[^.\n]{0,40}(válid|vigente|ativ)|"
    r"\bnessun[a]?\b[^.\n]{0,40}valid|\bgeen\b[^.\n]{0,40}geldig|\binga\b[^.\n]{0,40}giltig|\btiada\b[^.\n]{0,40}\bsah\b", re.I)
# 正數有效張數（N>0）
POS_VALID = re.compile(
    r"\b[1-9]\d*\s+(\w+\s+){0,2}(remain|remains|are|is|sind|ist|er|sont|est|är|ovat|on|zijn|is|são|é|sono|è|siguen|son)\s+(still\s+|stadig\s+|noch\s+|toujours\s+)?"
    r"(valid|active|gültig|gyldige?|valides?|giltiga?|voimassa|geldig|válid[oa]s?|validi|valida|vigentes?|ativ[oa]s?)\b|"
    r"有效\s*[1-9]\d*\s*張|仍有效\s*[1-9]|有効\s*[1-9]|유효\s*[1-9]|(vigentes|gültig|valides|valide|gyldige|giltiga|voimassa|geldig|sah|السارية|ยังมีผล)\s*:?\s*[1-9]", re.I)
NEG_BEFORE = re.compile(r"\b(none|no|not a single|not one|zero|ingen|ingen af|keine?n?|kein|aucune?|ninguna?|ningún|nenhuma?|nessuna?|nessun|"
                        r"geen|inga?|yksikään|tiada|tidak ada)\b|沒有|無|皆非|لا|ไม่มี|없|なし|ゼロ", re.I)


def still_valid_ok(s):
    """「仍有效 N」豁免：前面 30 字內有否定詞，或數字是 0，就不成立（pm 2026-10-23）"""
    for m in STILL_VALID.finditer(s):
        before = s[max(0, m.start() - 30): m.start()]
        nums = re.findall(r"\d+", m.group(0)) or re.findall(r"(\d+)\s*$", before)
        if NEG_BEFORE.search(before + " " + m.group(0)) or (nums and all(int(x) == 0 for x in nums)):
            continue
        return True
    return False


STILL_VALID = re.compile(r"\b(remain|remains|still) (valid|active)|\d+ (are|is|remain) (still )?(valid|active)|仍有效|有效許可證 \d|有效 \d|"
                         r"siguen vigentes|vigentes: \d|gültig: \d|valides : \d|valide: \d|gyldige: \d|giltiga: \d|voimassa: \d|"
                         r"geldig: \d|sah: \d|السارية: \d|ยังมีผล \d|유효 \d|有効 \d", re.I)
MKT_CLAIM_EXTRA = re.compile(r"\bis (currently )?marketed\b|\bremains on the market\b|上市中|已上市|販売中|시판 중|\bim Handel\b|"
                             r"\bcomercializad[oa]\b|\bcommercialisé|\bin commercio\b|\bin de handel\b|\bmarkedsført\b|\bmarknadsförd\b|"
                             r"\bmarkkinoilla\b|\bdipasarkan\b|مسوق|วางจำหน่าย", re.I)
AT_LEAST = re.compile(r"at least|al menos|pelo menos|mindestens|mindst|vähintään|au moins|至少|almeno|以上|최소|sekurang-kurangnya|minstens|"
                      r"\bminst\b|على الأقل|อย่างน้อย|≥", re.I)

# M3 擴充（2026-11-05，Za 概覽 vs 內文矛盾稽核找到的三種漏網寫法；英文站）：
#   M3a 事實是全部註銷／查無許可，正文寫有效（valid status、currently valid、valid registration、小寫 marketed in…）
#   M3b 事實有有效許可，正文寫未註冊／查無註冊（not registered、no SAHPRA registrations、zero registrations、total licences: 0、
#       data retrieval failure 這類「查無結果」說法）
#   M3c 事實有註銷張數（非部分紀錄），正文寫全部有效／沒有註銷，或正文寫的有效張數多於事實
# 只在 M3X_SITES 的站啟用：新規則上線前，該站頁面要先清到 0（否則許可證排程的 checker 會擋下整批）；selftest 一律測。
M3X_SITES = {"COTxGNN", "CaTxGNN", "DkTxGNN", "ESTxGNN", "KrTxGNN", "EuTxGNN", "MyTxGNN", "NZTxGNN", "PhTxGNN", "SgTxGNN", "UkTxGNN", "UsTxGNN", "ZaTxGNN"}
M3X_LANGS = ("en", "en-us")
VALID_CLAIM = re.compile(r"\bvalid status\b|\b(is|are|remains?) (currently |still )?valid\b|\bcurrently valid\b|"
                         r"\bvalid (single[\w-]*|registrations?|licen[cs]es?|authori[sz]ations?|approvals?|SAHPRA|products?|records?|entr(y|ies))\b|"
                         r"\(\s*[^()]*\bvalid\s*\)|\bmarketed in\b(?! other (jurisdictions?|countries|markets|regions)\b)|(?<!indication )\bis (widely )?(registered|marketed)\b", re.I)
# 2026-11-05（Za d5c6364b6，站上副本先改、11-06 補回母 repo）：「No oral arginine product was identified」講的是某劑型沒有產品，不是沒有註冊；
#   「no <劑型> product(s) were found」不算 M3b
# 2026-11-06（Us 依成分重建後續）：「may be marketed in other jurisdictions」不是講本國、「no original indication is registered」是適應症登記，都不是有效許可的說法
NOREG_CLAIM = re.compile(r"\bnot (currently )?registered\b|\bno (SAHPRA|local|South African|national)[- ](registrations?|licen[cs]es?|registered (products?|medicines?|formulations?))\b|"
                         r"\bholds? no (\w+ ){0,3}(registrations?|licen[cs]es?|marketing authori[sz]ations?)\b|"
                         r"\bzero (\w+ ){0,3}(registrations?|licen[cs]es?)\b|\bzero[- ](registration|licen[cs]e) (result|finding)|"
                         r"\bno (?:(?!cancel|revok|withdraw|combination)\w+ ){0,3}registrations? (on record|on file|were found|was found|were identified|were located|are recorded|"
                         r"(were |are )?recorded|found|returned)\b|\(total licen[cs]es?: 0\)|\b0[- ]registration|\bno registration (records?|data)\b|"
                         r"\breturned zero (\w+ ){0,2}(registrations?|licen[cs]es?|products?|records?)\b|\bdata (retrieval|collection|matching) (failure|gap|issue|error)|\bretrieval or matching failure|"
                         r"\bno (?!(?:\w+ ){0,2}?(?:oral|ophthalmic|topical|injectable|nasal|inhaled|rectal|eye|ear|dermal|vaginal|intravenous|parenteral)\b)"
                         r"(\w+ ){0,2}(registered |pharmaceutical )?products? (were|was) (found|identified|returned|listed)\b|"
                         r"\babsence of (SAHPRA |local |any )?registration|\bregistration (data|records?) (was|were) not (collected|retrieved)\b|"
                         r"\bSection 21 unregistered|\bunregistered medicine (provisions?|authori[sz]ation)|"
                         r"\bno recorded (\w+ ){0,3}(authori[sz]ations?|licen[cs]es?|DINs?|approvals?|applications?)\b|\(0 (DINs?|licen[cs]es?|NDAs?)\)|"
                         r"\bzero (DINs?|NDAs?|applications?|authori[sz]ations?)\b|\bno (Canadian |Health Canada )?DINs? (on record|were found|found|recorded)\b", re.I)
REG_WORD = re.compile(r"regist|licen[cs]|authori[sz]|market|products?\b|records?\b", re.I)
REGISTRY_CTX = re.compile(r"trial|SANCTR|PACTR|ICTRP|clinicaltrials|NCT\d|\bregistry\b|\bstud(y|ies)\b", re.I)
NONE_CANCEL = re.compile(r"\bnone (of them |of these )?(is |are |was |were )?(cancel+ed|revoked|withdrawn)\b|"
                         r"\bno (cancel+ed|revoked|withdrawn)( or [\w-]+)? (registrations?|licen[cs]es?|authori[sz]ations?|approvals?|ones)\b|"
                         r"\bno (registrations?|licen[cs]es?) (is|are|was|were) cancel+ed\b|\bnone cancel+ed\b", re.I)
ALL_VALID = re.compile(r"\b(all|both)\b[^.;\n]{0,70}?\b(are|is|remain|remains)\s+(currently |still )?valid\b|"
                       r"\b(all|both)\b[^.;\n]{0,50}\bwith valid status\b|\ball (\w+ ){0,3}valid\b", re.I)
NUM_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
             "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
             "eighteen": 18, "nineteen": 19, "twenty": 20}
_NUM = r"(\d+|" + "|".join(NUM_WORDS) + r")"
VALID_COUNT = re.compile(r"\b" + _NUM + r"\b((?:[\s-]+(?!of\b|and\b|are\b|is\b)[\w-]+){0,4}?)\s+(are|is|remain)\s+(currently |still )?valid\b|"
                         r"\b" + _NUM + r"\s+valid\b", re.I)


def _num(x):
    return int(x) if x.isdigit() else NUM_WORDS.get(x.lower())


def m3x(lang, s, fc, site=None):
    """M3 擴充規則；回傳子類（M3a／M3b／M3c）或 None。fc＝license_facts 一筆（market_status、valid、total、cancelled、partial）"""
    if lang not in M3X_LANGS or not fc or REGISTRY_CTX.search(s):
        return None
    ms, v = fc.get("market_status"), fc.get("valid") or 0
    c = fc.get("cancelled") or 0
    if ms in ("Cancelled only", "Not marketed") and VALID_CLAIM.search(s) and not mv2.NEG.search(s):
        return "M3a"
    if v > 0 and (NOREG_CLAIM.search(s) or (site in NOREG_EXTRA and NOREG_EXTRA[site].search(s))) and not POS_VALID.search(s) and REG_WORD.search(s):
        return "M3b"
    if v > 0 and c == 0 and not fc.get("partial") and site in CANC_NONE and CANC_NONE[site].search(s) and not CANC_NONE_EXCL.search(s) \
            and not NONE_CANCEL.search(s):
        return "M3b"
    if c > 0 and (not fc.get("partial") or site in M3X_PARTIAL):
        if NONE_CANCEL.search(s) or (ALL_VALID.search(s) and not re.search(r"cancel", s, re.I)):
            return "M3c"
        vl = v + ((fc.get("not_marketed") or 0) if site in LEGAL_NM_VALID else 0)
        for m in VALID_COUNT.finditer(s):
            n = _num(m.group(1) or m.group(5))
            pre = s[max(0, m.start() - 14):m.start()]
            if n and n > vl and not AT_LEAST.search(pre) and not (m.group(1) and re.search(r"\bof (the )?$", pre, re.I)):
                return "M3c"
    return None


# 2026-11-05（7 站概覽 vs 內文稽核，用戶決定比照 Za 修）：
# M3d 事實是「核准未上市」，正文寫上市中（marketed in <國>、is marketed、currently marketed…）
# LEGAL_NM_VALID：該站的「核准未上市」（Ca DORMANT、ES no comercializada、CO Temp. no comerc - Vigente）法律上仍是有效許可，
#   M3c 的「有效張數過多」以 有效＋核准未上市 比；M3X_PARTIAL：部分紀錄的頁，已收錄紀錄裡有註銷時也查「沒有註銷／全部有效」。
LEGAL_NM_VALID = {"CaTxGNN", "ESTxGNN", "COTxGNN"}
M3X_PARTIAL = {"CaTxGNN", "ESTxGNN", "COTxGNN", "UsTxGNN", "KrTxGNN", "MyTxGNN", "DkTxGNN"}
MKT_CLAIM_EN = re.compile(r"\bmarketed in (Canada|the (US|U\.S\.|United States)|Denmark|Malaysia|Korea|Spain|Colombia)\b|"
                          r"\b(is|are|remains?) (currently |still |actively |widely |already )?marketed\b|\bcurrently marketed\b|"
                          r"\bmarketed (in [A-Z][a-z]+ )?(as|under the brand name)\b|\bon the (Canadian|US|U\.S\.) market\b", re.I)
FORMER = re.compile(r"\b(formerly|previously|was once|no longer|used to be|had been|discontinued|dormant|cancel)", re.I)
TW_LEFTOVER = re.compile(r"Taiwan (Market(ing)? Status|Approved Licen|regulatory|TFDA)|Market Status \(Taiwan\)|Licenses? \(Taiwan\)|"
                         r"Number of Taiwan Licen|\b\d+ Taiwan licen|No Taiwan licen[cs]e records?|TFDA database|"
                         r"taiwan_regulatory|not in Taiwan TFDA|TFDA (query|records?|licen|official|package insert)|parse the TFDA|for the Taiwan context|"
                         r"대만[^.|]{0,12}(허가|시판|식약|미허가|규제|등록)|\(대만\)|대만\(한국\)|台灣上市|臺灣上市", re.I)


_KEEP = {}


def license_keep(site):
    """scripts/license_sentence_fixes.json 裡 keep=true 的句子（與事實矛盾、但混有療效或機轉內容，用戶決定前不刪）"""
    if site not in _KEEP:
        p = BASE / site / "scripts/license_sentence_fixes.json"
        d = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        _KEEP[site] = {pg: [m["sentence"] for m in v if m.get("keep")] for pg, v in d.items()}
    return _KEEP[site]


# 站別補充的「沒有有效註冊」寫法（只在該站啟用，已上線的站維持原判定；CO 2026-11-05）
NOREG_EXTRA = {"COTxGNN": re.compile(
    r"\b(se encuentra[n]?|quedan?|quedaron|figura[n]?)\s+(\w+\s+){0,2}(cancelad|anulad|revocad|vencid)|"
    r"\b(registros?|autorizaci\w+)\b[^.;]{0,80}?\by (est[aá]n?|se encuentran?|fueron) (\w+\s+)?(cancelad|anulad|revocad|vencid)|"
    r"\bno (cuenta|tiene|dispone) (actualmente |hoy )?(con )?(ning[uú]n |un )?registros?( sanitarios?)? vigentes?|"
    r"\b(est[aá]n?|es|son) (\w+\s+){0,2}(cancelad[oa]s?)\b(?![^.;]{0,30}vigente)|\bno hay (\w+ ){0,2}presentaciones (\w+ )?vigentes|\bno existe (\w+ ){0,2}(comercializaci\w+|registros?)( sanitarios?)? vigentes?|"
    r"\((actualmente |hoy )?cancelad[oa]s?\)|\b(hoy|actualmente|ya) cancelad[oa]s?\b|\bfigura (hoy )?como cancelad", re.I)}
# SG（2026-11-06，英文）：舊版 Evidence Pack 頁的「查無註冊」寫法（no registered products、0 registered products、
# registration records are absent、currently unregistered、total_licenses: 0…）；只在本站有有效註冊時判（m3x 的 M3b）
NOREG_EXTRA["SgTxGNN"] = re.compile(
    r"\bno (Singapore |HSA |local )?(registered products?|approval records?|licen[cs]e records?)\b|\b0 registered products?\b|"
    r"\bno (Singapore )?(HSA )?(regulatory )?registrations?\b(?! (are|were|is|was) (cancel|revok))|\bno Singapore (regulatory |registration |market )+(records?|data|registrations?)\b|"
    r"\b(registration|regulatory) (registration )?records? (are|is) absent\b|\bcurrently unregistered\b|\bunregistered in Singapore\b|"
    r"\bregulatory data returned zero\b|\bnot present in regulatory data\b|\btotal_licen[cs]es\W{0,3}[:=]\s*0\b|\bno local regulatory data\b|"
    r"\bno approved registration\b|\bno Singapore market registration\b|\bno Singapore regulatory\b", re.I)
# EU（2026-11-06，英文）：舊頁依當時的單筆紀錄寫「本藥（唯一）的 EU 許可已註銷」；本站有有效集中許可時判 M3b
# （「earlier／previously／in 2017」這類講過去某個許可的句子不算）
NOREG_EXTRA["EuTxGNN"] = re.compile(
    r"^(?!.*\b(earlier|previous(ly)?|formerly|in (19|20)\d\d|re-?authori[sz]ed)\b)(?=.*("
    r"\b(the|its|this|sole|only)( only| sole)?( EU| EMA| centrali[sz]ed| marketing| reference product'?s?)? (authori[sz]ation|licen[cs]e)\b[^.;]{0,40}?\b(is|was|has been|are|were)( also| currently| now)*( recorded| listed| shown)?( as)? (cancel+ed|withdrawn|revoked|lapsed|expired)\b|"
    r"\bauthori[sz]ation status is (cancel+ed|withdrawn)\b|\bshows the licen[cs]e as cancel+ed\b|"
    r"\bthe product'?s? (EU )?(authori[sz]ation )?(is|was|has been) (also )?(cancel+ed|withdrawn)\b|"
    r"\bmarketing authori[sz]ation has (also )?been (cancel+ed|withdrawn)\b))", re.I)
# EU（2026-11-06）：本藥的 EMA 集中許可全部有效、沒有註銷（c＝0）時，正文說許可已註銷（cancelled／cancellation、authorisation was withdrawn）
# 一定與事實矛盾（舊頁依當時誤判的狀態寫成）。講過去的事（earlier／previously／historically／in 2017）、「沒有註銷」的否定句不算
CANC_NONE = {"EuTxGNN": re.compile(r"\bcancel+ed\b|\bcancell?ations?\b|\bauthori[sz]ations? (was|were|has been|have been) withdrawn\b", re.I)}
CANC_NONE_EXCL = re.compile(r"\b(previously|formerly|earlier|historically|in (19|20)\d\d|from the market (as|for)|later withdrawn)\b|"
                            r"\b(no|none|not|without|neither|nor)\b[^.;]{0,40}\bcancel|\bcancel+ed:? 0\b", re.I)
# CO：沒有任何註銷許可（c＝0）時，提到「registro cancelado／estado cancelado／solo cancelados」就是 2026-10-03 誤判留下的錯句
CANC_NOUN = {"COTxGNN": re.compile(r"\b(registros?|productos?|presentaci\w+)( sanitarios?)?( \w+){0,3} cancelad[oa]s?\b|\bregistros?,? (también |hoy |todos )?cancelad|\bestado( de mercado)? cancelado\b|\bsolo cancelad|"
                                   r"\bcancelad[oa]s?\b(?=[^.;]{0,40}\b(registro|INVIMA|Colombia))", re.I)}
# 站別較窄的「這句講的是臨床試驗」判斷：CO 的錯句常與「sin ensayos clínicos」同句，原本整句被當成試驗語境略過
CTX_NARROW = {"COTxGNN": re.compile(r"NCT\d|registro de ensayos?|EudraCT|REEC|ClinicalTrials", re.I)}

# 判定前先拿掉 Markdown 粗體／斜體記號的站（「están **cancelados**」原本對不上；只在新上線的站啟用，已上線的站維持原判定）
EMPH_STRIP = {"COTxGNN", "NZTxGNN", "PhTxGNN", "SgTxGNN", "UkTxGNN"}

# M3 擴充（2026-11-06，Us 用戶決定）：英文「全部註銷」的漏網寫法。ALL_CANCEL 只認「all … licence … cancelled」且許可字在 all 後 40 字內，
# 漏掉（例 Us 依成分重建後仍留在正文的舊句）：
#   「All nine US listings … are marked as cancelled」（listings／records／entries／products／BLAs 不在 _LIC）、
#   「There are 9 authorizations in total, and all are cancelled」「12 US authorizations, all with cancelled status」（all 在許可字後面）、
#   「The US licences are all cancelled」「Both US NDAs are cancelled」「The US license is (also listed as) cancelled」
#   「Idelalisib's sole US license is cancelled」「the product's US market status is "Cancelled only"」「Neither product is currently active」。
# 判定（fc＝license_facts 一筆）：
#   全部類（all／both／the／only／sole／neither）：事實有有效許可（valid>0）就矛盾；
#   部分類（N further／more／other／remaining／a sixth… 也註銷）：N 多於事實的註銷張數就矛盾（沒有任何註銷時一定矛盾）；
#   句中點名的申請號（NDA／ANDA／BLA＋6 碼）全部有效、句子卻說註銷：矛盾。
# 「全部有效、沒有註銷」（none／no／not … cancelled）不算（同 333c1aeb 的修正）。只在 ALLC_X_SITES 啟用（新規則上線前該站頁面要先清到 0）。
# 2026-11-06 用戶決定：Eu 8 句、NZ 1 句錯句刪完後，英文站 Eu、NZ 與掃過為 0 的 Au、In、Sg、Uk、Ca、Ph、Za 一併啟用。
ALLC_X_SITES = {"UsTxGNN", "EuTxGNN", "NZTxGNN", "AuTxGNN", "InTxGNN", "SgTxGNN", "UkTxGNN", "CaTxGNN", "PhTxGNN", "ZaTxGNN"}
_LICX = r"(?:licen[cs]es?|authori[sz]ations?|registrations?|approvals?|applications?|listings?|records?|entr(?:y|ies)|products?|A?NDAs?|BLAs?)"
_US = r"(?:(?:US|U\.S\.|FDA|American|biologics?|generic|marketing|product)\s+)*"
_CANC_W = r"(?:\*\*|\")?(?:cancel+ed|Cancelled only)\b"
_STATUS_V = r"(?:\s+(?:also|currently|now|still|both|all|marked|listed|recorded|shown|reported|as|in|with|a|status|of))*\s+"
ALLC_X = [
    # all／every／both … 許可字 … cancelled
    re.compile(r"\b(?:all|every|both)\b[^.;\n]{0,60}?\b" + _LICX + r"\b[^.;\n]{0,70}?" + _CANC_W, re.I),
    # 許可字 … all／both（are all cancelled、, and all are cancelled、, all with cancelled status、, all cancelled）
    re.compile(r"\b" + _LICX + r"\b[^.;\n]{0,80}?\b(?:all|both)\b(?:\s+(?:are|were|have been|is|currently|now|also|listed|recorded|marked|shown|with|have|in|as|of them)\b)*[^.;\n]{0,20}?" + _CANC_W, re.I),
    # 定冠詞／所有格＋（only／sole／single）＋許可字 … is／are（listed as）cancelled
    re.compile(r"\b(?:the|its|their|this|[A-Z][\w-]*'s)\s+(?:(?:only|sole|single|one)\s+)?" + _US + _LICX + r"(?:\s+records?)?\b[^.;,\n]{0,50}?\b(?:is|are|was|were|has been|have been)"
               + _STATUS_V + r"(?:\(?)" + _CANC_W, re.I),
    # 市場狀態寫成「Cancelled only」
    re.compile(r"\bmarket(?:ing)? status\b[^.;\n]{0,50}?\"?Cancelled only", re.I),
    re.compile(r"\b(?:licen[cs]e|authori[sz]ation|NDA|BLA)\s+is\s+cancel+ed\s+only\b", re.I),
    # 「one authorization, and it is marked as cancelled」
    re.compile(r"\b(?:one|single|only)\s+" + _US + _LICX + r"\b[^.;\n]{0,30}?\b(?:it|which)\s+(?:is|was|has been)" + _STATUS_V + _CANC_W, re.I),
    # 句首就是許可字（checker 的句界把「U.S. licenses」切開，剩「licenses are cancelled, …」）
    re.compile(r"^\W*" + _US + _LICX + r"\b[^.;,\n]{0,30}?\s(?:is|are)" + _STATUS_V + _CANC_W, re.I),
    # 「US licenses are cancelled」「why US licenses are cancelled」（冠以國名、沒有限定詞＝本國全部許可）
    re.compile(r"\b(?:US|U\.S\.|FDA)\s+(?:(?:biologics?|generic|marketing)\s+)?" + _LICX + r"\s+(?:is|are|were)" + _STATUS_V + _CANC_W, re.I),
    # 「All 11 are listed as cancelled.」（主詞省略、承上句的許可）
    re.compile(r"^\W*(?:all|both)\s+(?:" + _NUM + r"\s+)?(?:are|were|have been)" + _STATUS_V + _CANC_W, re.I),
]
# Neither … is (currently) active／valid
ALLC_NEITHER = re.compile(r"\bneither\b(?:\s+(?:of them|of the|product|products|authori[sz]ations?|licen[cs]es?|applications?|NDAs?|BLAs?))+\s+(?:is|are)\s+(?:currently\s+|still\s+)?(?:active|valid)\b", re.I)
# 「the cancelled US market status」「given the cancelled status of all authorizations」「the cancellation of all US authorizations」
# 「The US market status is listed as cancelled」：講的是本藥（全部）的市場／許可狀態已註銷，事實有有效許可就矛盾
ALLC_STATUS = re.compile(r"\bcancel+ed(?:[- ]only)?\s+(?:US\s+|FDA\s+)?(?:market(?:ing)?|regulatory|licen[cs](?:e|ing|ure)|authori[sz]ation|BLA|NDA|US)\s+status\b|"
                         r"\bcancel+ed\s+status\s+of\s+all\b|\bcancell?ation\s+of\s+all\b|\bcancel+ed[- ]only\s+status\b|"
                         r"\bmarket(?:ing)?\s+status\b[^.;,\n]{0,30}?\b(?:is|was)\b[^.;,\n]{0,25}?\bcancel+ed\b", re.I)
# 事實沒有任何停產／註銷的申請（cancelled＝0）時，說許可／申請／市場狀態「已註銷」「註銷的理由」一定矛盾（比照 Eu 的 CANC_NONE）
ALLC_CANC_ANY = re.compile(r"\bcancel+ed\b|\bcancell?ations?\b", re.I)
ALLC_LIC_CTX = re.compile(r"licen[cs]|authori[sz]|\b(A?NDA|BLA)s?\b|\bmarket(ing)? status|\bregulatory status|\brecords?\b|\blistings?\b|\bproducts?\b|\bentr(y|ies)\b", re.I)
_ALLC_SUBSET = re.compile(r"\b(?:further|more|other|remaining|additional|another|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\b(?:[\s,]+[\w()'.-]+){0,4}?[\s,]+" + _LICX + r"\b", re.I)
_ALLC_NEG = re.compile(r"\b(?:no|none|not|neither|nor|never|without|zero)\b[^.;,\n]{0,35}\bcancel|\bcancel+ed:?\s*0\b|\b0\s+(?:\w+\s+)?(?:(?:are|is|were)\s+)?cancel|\bwhether\s+(?:the\s+)?(?:\w+\s+){0,4}(?:is|are|was|were|has been|have been)\s+(?:\w+\s+)?cancel", re.I)
_ALLC_SOME = re.compile(r"\bcancel+ed\b", re.I)
_ALLC_N = re.compile(r"\b(?:(" + _NUM + r")\s+(?:\w+\s+){0,3}?(?:further|more|additional|other)|(?:remaining|other|additional|further)\s+(" + _NUM + r"))\b", re.I)
_APPL_ID = re.compile(r"\b(NDA|ANDA|BLA)\s*(\d{6})\b")


def all_cancel_x(s, fc):
    """M3 擴充（英文、ALLC_X_SITES）：回傳說明或 None"""
    if not fc or _ALLC_NEG.search(s) and not re.search(r"\bneither\b[^.;]{0,60}\b(active|valid)\b", s, re.I):
        return None
    v, c = fc.get("valid") or 0, fc.get("cancelled") or 0
    s2 = re.sub(r"\b(Inc|Ltd|Co|Corp|Labs?)\.", r"\1", s.replace("**", "").replace("U.S.", "US"))
    lic = {mv2.norm_id(k): x for k, x in (fc.get("licenses") or {}).items()}
    ids = [mv2.norm_id(m.group(1) + m.group(2)) for m in _APPL_ID.finditer(s2)]
    if ids and _ALLC_SOME.search(s2) and any(lic.get(i) == "valid" for i in ids) and not re.search(r"\b(valid|active)\b", s2, re.I):
        ok = [i for i in ids if lic.get(i) == "valid"]
        return f"點名的申請號 {', '.join(ok[:4])} 事實有效，正文寫成註銷：{s[:60]}"
    if ids and _ALLC_SOME.search(s2) and all(lic.get(i) == "cancelled" for i in ids):
        return None  # 點名的申請號確實都已註銷（停產）
    if c == 0 and v > 0 and ALLC_CANC_ANY.search(s2) and ALLC_LIC_CTX.search(s2) and not CANC_NONE_EXCL.search(s2):
        return f"事實沒有任何停產／註銷的申請（有效 {v} 張），正文寫已註銷：{s[:60]}"
    if v > 0 and ALLC_STATUS.search(s2) and not _ALLC_SUBSET.search(s2):
        return f"事實有效 {v} 張，正文寫本藥的市場／許可狀態已註銷：{s[:60]}"
    if _ALLC_SUBSET.search(s2) and _ALLC_SOME.search(s2):
        m = _ALLC_N.search(s2)
        n = next((_num(w) for w in re.findall(r"\w+", m.group(0)) if w.isdigit() or w.lower() in NUM_WORDS), 1) if m else 1
        if n and n > c:
            return f"事實註銷 {c} 張，正文寫另有 {n} 張註銷：{s[:60]}"
        return None
    if v > 0 and (ALLC_NEITHER.search(s2) or any(m and not re.search(r"\b(valid|active)\b", m.group(0), re.I) for m in (rx.search(s2) for rx in ALLC_X))):
        return f"事實有效 {v} 張，正文寫全部（或唯一）許可已註銷：{s[:60]}"
    return None


# M3 擴充（2026-11-06，Us 用戶決定）：正文的「總數說法」跟事實不符。舊頁依當時的部分紀錄寫了總數或有效／註銷張數
# （「In total, 10 licences are valid and 1 is cancelled」「Of 7 US licence records, 5 are valid and 2 are cancelled」
# 「Five of the six licences are currently valid」「All 16 US licenses are recorded as valid」「The local data hold 6 licence records in total」），
# 依成分重建後事實的總數／有效／註銷張數不同就判 M3。只認「總數」語境（in total／overall／altogether／in all／a total of／Of N … records／
# A of the N／all N／N … in total），句中講的是表格列出的子集（listed／shown／in the table／above／below）、或「至少 N」不算；
# 部分紀錄的頁（total 未知）不判。數字比對：總數＝事實 total（Us 另認 total＋列名產品數），有效＝valid（LEGAL_NM_VALID 另認 valid＋核准未上市），
# 註銷＝cancelled。只在 TOTAL_X_SITES 啟用（新規則上線前該站頁面要先清到 0）。
TOTAL_X_SITES = {"UsTxGNN", "EuTxGNN", "NZTxGNN", "AuTxGNN", "InTxGNN", "SgTxGNN", "UkTxGNN", "CaTxGNN", "PhTxGNN", "ZaTxGNN"}
_TLIC = r"(?:(?:US|U\.S\.|FDA|EU|EMA|centrali[sz]ed|single-ingredient|generic|marketing|licen[cs]e|local|recorded|current|human|valid|active|cancel+ed)\s+){0,3}" \
        r"(?:licen[cs]es?|authori[sz]ations?|registrations?|approvals?|applications?|A?NDAs?|BLAs?|DINs?|records?|entries|listings?)\b"
_TN = r"(\d+|" + "|".join(NUM_WORDS) + r")"
TOTAL_CUE = re.compile(r"\b(in total|overall|altogether|in all|a total of|total of)\b|^\W*(?:Of|Among)\s+(?:the\s+)?(?:" + _TN + r"\s+)?" + _TLIC +
                       r"|\b" + _TN + r"\s+of\s+(?:the|these|its|all)?\s*" + _TN + r"\s+" + _TLIC +
                       r"|\b(?:all|both)\s+" + _TN + r"\s+" + _TLIC +
                       r"|\b" + _TN + r"\s+(?:valid|active)\s+" + _TLIC + r"\s+(?:out\s+)?of\s+" + _TN + r"\b", re.I)
TOTAL_NOTLIC = re.compile(r"interact|\bDDIs?\b|\brated (Major|Moderate|Minor)\b|\bdrugs? (were )?identified\b|\binteracting\b", re.I)  # 交互作用筆數不是許可證
TOTAL_SUBSET = re.compile(r"\b(listed|shown|displayed|in the table|in this table|above|below|on this page|in the list)\b(?!\s+in total)", re.I)
_T_TOTAL = [re.compile(r"^\W*(?:Of|Among)\s+(?:the\s+)?" + _TN + r"\s+" + _TLIC, re.I),
            re.compile(r"\b" + _TN + r"\s+of\s+(?:the|these|its|all)?\s*" + _TN + r"\s+" + _TLIC, re.I),  # group(2)
            re.compile(r"\b(?:all|both)\s+" + _TN + r"\s+" + _TLIC, re.I),
            re.compile(r"\ba total of\s+" + _TN + r"\b", re.I),
            re.compile(r"\b" + _TN + r"\s+" + _TLIC + r"(?:\s+(?:are|were|is)\s+(?:listed|recorded|held|on record))?\s+in total\b", re.I),
            re.compile(r"\bhold\s+" + _TN + r"\s+" + _TLIC + r"[^.;,]{0,20}\bin total\b", re.I),
            re.compile(r"\b" + _TN + r"\s+(?:valid|active)\s+" + _TLIC + r"\s+(?:out\s+)?of\s+" + _TN + r"\b", re.I)]  # 「3 valid licences of 3」：group(2)
_T_VALID = [re.compile(r"\b" + _TN + r"\s+of\s+(?:the|these|its|all)?\s*" + _TN + r"\s+" + _TLIC + r"\s+(?:are|is)\s+(?:currently\s+|still\s+)?(?:valid|active)\b", re.I),
            re.compile(r"(?<!of )(?<!total of )\b" + _TN + r"\s+(?:(?:US|FDA)\s+)?(?:" + _TLIC + r"\s+)?(?:are|is)\s+(?:currently\s+|still\s+)?(?:valid|active)\b", re.I),
            re.compile(r"\b" + _TN + r"\s+(?:valid|active)\b(?!\s+(?:and|or)\s+\d)", re.I)]
_T_CANC = [re.compile(r"\b" + _TN + r"\s+(?:(?:US|FDA)\s+)?(?:" + _TLIC + r"\s+)?(?:\([^()]{0,40}\)\s+)?(?:are|is|was|were)\s+(?:also\s+|currently\s+)?cancel+ed\b", re.I),
           re.compile(r"\b" + _TN + r"\s+cancel+ed\b", re.I)]
# 刪句工具（delete_license_sentences.CLAIM）用來定位要刪的張數子句（「, with 6 of 6 licenses valid」「(3 of 3 licences are valid)」）
TOTAL_SPAN = re.compile(r"\b(?:all\s+)?" + _TN + r"\s+of\s+(?:its\s+|the\s+)?" + _TN + r"\s+" + _TLIC + r"(?:\s+(?:are|is))?\s+(?:currently\s+)?(?:valid|active)\b|"
                        r"\ball\s+" + _TN + r"\s+" + _TLIC + r"\s+(?:are|is)\s+(?:currently\s+)?(?:valid|active)\b|"
                        r"\(?\b" + _TN + r"\s+(?:valid|active)\s+" + _TLIC + r"\s+(?:out\s+)?of\s+" + _TN + r"\b\)?", re.I)
_T_ALLV = re.compile(r"\b(?:all|both)\s+(?:" + _TN + r"\s+)?" + _TLIC + r"[^.;,]{0,40}?\b(?:are|is)\s+(?:currently\s+|still\s+)?(?:recorded\s+as\s+|listed\s+as\s+|counted\s+as\s+|marked\s+as\s+)?(?:valid|active)\b", re.I)


def total_x(site, s, fc):
    """總數說法跟事實不符（英文、TOTAL_X_SITES）：回傳說明或 None"""
    if not fc or fc.get("partial") or fc.get("total") is None:
        return None
    s2 = re.sub(r"\b(Inc|Ltd|Co|Corp|Labs?)\.", r"\1", s.replace("**", "").replace("U.S.", "US"))
    if not TOTAL_CUE.search(s2) or AT_LEAST.search(s2) or re.search(r"\bmay be partial\b|\bpartial list\b", s2, re.I) or TOTAL_NOTLIC.search(s2):
        return None
    if TOTAL_SUBSET.search(s2) and not re.search(r"\b(in total|overall|altogether|in all|a total of)\b", s2, re.I):
        return None
    if REGISTRY_CTX.search(re.sub(r"\b(NDA|ANDA|BLA)\s*\d{6}\b", "", s2)) and not re.search(r"licen[cs]|authori[sz]|\b(A?NDA|BLA)s?\b", s2, re.I):
        return None
    n, v, c = fc.get("total") or 0, fc.get("valid") or 0, fc.get("cancelled") or 0
    ok_n = {n, n + (fc.get("listed") or 0)}
    ok_v = {v, v + ((fc.get("not_marketed") or 0) if site in LEGAL_NM_VALID else 0)}
    bad = []
    for i, rx in enumerate(_T_TOTAL):
        m = rx.search(s2)
        if m:
            k = _num(m.group(2) if i in (1, len(_T_TOTAL) - 1) else m.group(1))
            if k is not None and k not in ok_n:
                bad.append(f"總數 {k}≠{n}")
            break
    for rx in _T_VALID:
        m = rx.search(s2)
        if m:
            k = _num(m.group(1))
            if k is not None and k not in ok_v:
                bad.append(f"有效 {k}≠{v}")
            break
    for rx in _T_CANC:
        m = rx.search(s2)
        if m:
            k = _num(m.group(1))
            if k is not None and k != c:
                bad.append(f"註銷 {k}≠{c}")
            break
    if c > 0 and _T_ALLV.search(s2) and not re.search(r"\bcancel", s2, re.I):
        bad.append(f"全部有效≠註銷 {c} 張")
    if bad:
        return f"總數說法跟事實不符（{'、'.join(bad)}；事實 {n} 張、有效 {v}、註銷 {c}）：{s[:60]}"
    return None

# M3 擴充（2026-11-06，用戶決定）：正文的「有效張數」說法跟事實不符（多半是舊頁依當時的部分紀錄寫的，說少了；例 amlodipine
# 「The drug is marketed in the US, with 11 valid authorizations」，事實有效 68 張）。認得 VALID_COUNT 的寫法（「with N valid …」
# 「N valid authorizations」「N licences are (currently) valid」）；說「單方」時跟事實的單方有效張數（valid_single）比。
# 不算：至少 N、部分紀錄的頁、表外「另有 N 張」（further／more／other／remaining／additional／another，張數不超過事實）、
# 「Of the N listed／shown」這類表格子集合、「A of the N」（由 total_x 管）。只在 VALIDX_SITES 啟用（新規則上線前該站頁面要先清到 0）。
VALIDX_SITES = {"UsTxGNN", "EuTxGNN", "NZTxGNN", "AuTxGNN", "InTxGNN", "SgTxGNN", "UkTxGNN", "CaTxGNN", "PhTxGNN", "ZaTxGNN"}
_VX_LIC = re.compile(r"licen[cs]|authori[sz]|registration|approval|application|\b(A?NDA|BLA|DIN)s?\b|\brecords?\b|\bproducts?\b|\blistings?\b|\bentr(y|ies)\b", re.I)
_VX_ADD = re.compile(r"\b(further|more|other|remaining|additional|another)\b", re.I)
_VX_SUBSET = re.compile(r"^\W*(?:Of|Among)\s+(?:the\s+)?(?:" + _NUM + r"\s+)?[\w\s-]{0,30}?\b(listed|shown|displayed|above|below|in the table)\b", re.I)


def valid_under(site, s, fc):
    """有效張數說法跟事實不符（英文、VALIDX_SITES）：回傳說明或 None"""
    if not fc or fc.get("partial") or fc.get("total") is None:
        return None
    s2 = s.replace("**", "").replace("U.S.", "US")
    if TOTAL_NOTLIC.search(s2) or _VX_SUBSET.search(s2) or not _VX_LIC.search(s2):
        return None
    v = fc.get("valid") or 0
    ok = {v, v + ((fc.get("not_marketed") or 0) if site in LEGAL_NM_VALID else 0)}
    vs = fc.get("valid_single") if re.search(r"\bsingle[- ]ingredient\b|\bsingle[- ]agent\b|\bmono-?(component|substance)\b", s2, re.I) else None
    for m in VALID_COUNT.finditer(s2):
        k = _num(m.group(1) or m.group(5))
        pre = s2[max(0, m.start() - 30):m.start()]
        if k is None or k in ok or AT_LEAST.search(pre[-16:]) or re.search(r"\bof (the )?$", pre[-14:], re.I):
            continue
        if vs is not None and k >= vs:
            continue  # 說「單方 N 張」：不少於事實的單方有效張數就不判（單方／複方的歸類不在這條規則管）
        if re.search(r"\bof\s+(?:the\s+|its\s+)?" + _NUM + r"\b", s2[m.end():m.end() + 30], re.I):
            continue  # 「3 valid licences of 3」由 total_x 管
        if re.match(r"\s+listed\b", s2[m.end(1) if m.group(1) else m.end(5):]) or re.search(r"\b" + _NUM + r"\s+listed\s+" , m.group(0), re.I):
            continue  # 「All three listed authorizations are valid」：講的是表格列出的那幾張
        if _VX_ADD.search(pre[-25:] + " " + m.group(0)) and k <= v:
            continue  # 表外另有 N 張有效（Two further licences are valid: …）
        return f"有效張數說法跟事實不符（寫 {k} 張，事實有效 {v} 張{'（單方 ' + str(vs) + '）' if vs is not None else ''}）：{s[:60]}"
    return None

# M3 擴充（2026-11-06，用戶決定）：正文的「單方／複方」說法跟事實不符。事實層 valid_single／single_total 是該站 reviewer
# 依許可成分數判定的單方張數（kind＝single／combo）。判定（部分紀錄的頁不判、事實沒有 kind 的頁不判）：
#   全部單方（All five registrations are valid single-ingredient products、all single-ingredient、no combination products）：有效許可裡有複方就矛盾；
#   全部複方（only available as a combination、no single-ingredient …）：有單方有效許可就矛盾；
#   單方張數（N valid single-ingredient …）多於事實的單方張數就矛盾（少於事實由 valid_under 管）。
# 「All 5 single-ingredient licences are valid」（主詞是單方那幾張）不算。只在 COMBO_X_SITES 啟用（新規則上線前該站頁面要先清到 0）。
# 啟用站＝事實層 kind 能分出複方的站。Us、Au、In、Ca 原本一律算成單方（reviewer 只認「;;」分隔），2026-11-06 各站改 reviewer 依官方資料的
# 成分數判定（Us Drugs@FDA／NDC、Ca DPD 的「; 」，Au PBS 品項的「 + 」，In 資料集的 short_composition2）後一併啟用
COMBO_X_SITES = {"SgTxGNN", "ZaTxGNN", "UkTxGNN", "NZTxGNN", "EuTxGNN", "PhTxGNN", "UsTxGNN", "AuTxGNN", "InTxGNN", "CaTxGNN"}
_SI = r"single[- ](?:ingredient|agent|substance|component)s?|mono-?(?:component|substance)"
_CX_ALL_SINGLE = re.compile(r"\b(?:all|both|each|every)\b(?!\s+(?:the\s+)?(?:\w+\s+)?(?:" + _SI + r")\s+\w+\s+(?:are|is|were)\b)[^.;]{0,70}?\b(?:" + _SI + r")\b|"
                            r"\b(?:entirely|exclusively)\s+(?:of\s+)?(?:" + _SI + r")\b|"
                            r"\bno\s+(?:combination|fixed-dose|multi-ingredient)\b|\bnone\s+(?:is|are)\s+(?:a\s+)?(?:combination|fixed-dose)\b|\bnot\s+(?:a\s+)?combination\s+product", re.I)
_CX_ALL_COMBO = re.compile(r"\bonly\s+(?:(?:available|marketed|registered|authori[sz]ed|licensed)\s+)?(?:as|in)\s+(?:a\s+|an?\s+)?(?:fixed-dose\s+)?combination|"
                           r"\bno\s+(?:" + _SI + r")\b|\b(?:all|both)\b[^.;]{0,50}\b(?:are|is)\s+(?:\w+\s+)?(?:combination|fixed-dose|multi-ingredient)\s+(?:products?|preparations?|registrations?|licen[cs]es?|authori[sz]ations?)", re.I)
_CX_COUNT = re.compile(r"\b" + _NUM + r"\s+(valid\s+)?(?:" + _SI + r")\b", re.I)


def combo_x(site, s, fc):
    """單方／複方說法跟事實不符（英文、COMBO_X_SITES）：回傳說明或 None"""
    if not fc or fc.get("partial") or fc.get("valid_single") is None:
        return None
    s2 = s.replace("**", "").replace("U.S.", "US")
    if TOTAL_NOTLIC.search(s2) or not _VX_LIC.search(s2) or re.search(r"\btrials?\b|\bNCT\d|\bregimens?\b|\bcombination (?:with|of|therapy)\b|\bin combination\b|\bwhich\b[^.;]{0,30}\b(?:single|combination)", s2, re.I):
        return None
    v, vs, st = fc.get("valid") or 0, fc.get("valid_single") or 0, fc.get("single_total") or 0
    if _CX_ALL_SINGLE.search(s2) and vs < v:
        return f"單方說法跟事實不符（寫全部單方／沒有複方，事實有效 {v} 張中單方 {vs} 張）：{s[:60]}"
    if _CX_ALL_COMBO.search(s2) and vs > 0:
        return f"複方說法跟事實不符（寫只有複方／沒有單方，事實單方有效 {vs} 張）：{s[:60]}"
    for m in _CX_COUNT.finditer(s2):
        k = _num(m.group(1))
        vsl = vs + ((fc.get("not_marketed") or 0) if site in LEGAL_NM_VALID else 0)  # Ca 等站的「有效」另含核准未上市
        if k is not None and not AT_LEAST.search(s2[max(0, m.start() - 14):m.start()]) and k > (vsl if m.group(2) else max(vsl, st)):
            return f"單方張數說法跟事實不符（寫 {k} 張，事實單方有效 {vs} 張、單方共 {st} 張）：{s[:60]}"
    return None

def m3_verdict(site, lang, s, fc):
    """正文一句跟事實矛盾時回傳 (子類, 說明)；checker 與刪句程式共用（2026-11-05）"""
    if site in EMPH_STRIP:
        s = s.replace("**", "").replace("__", "")
    ms, v = fc.get("market_status"), fc.get("valid") or 0
    if (fc.get("veterinary") or 0) > 0 and v == 0 and not re.search(r"\bhuman|menneske", s, re.I):
        return None  # 只有獸用許可的頁：正文說許可有效／上市，講的是獸用品（是對的）；只有明講人用時才判
    if (fc.get("veterinary") or 0) > 0 and VET_CTX.search(s) and not (v > 0 and VET_ONLY_CLAIM.search(s)):
        return None  # 講的是獸用許可（只有獸用許可的頁說它有效、上市是對的）；但有人用許可時「唯一許可是獸用」仍算矛盾
    if v > 0 and site in M3X_SITES and VET_ONLY_CLAIM.search(s):
        return "M3b", f"M3b 事實有人用有效許可 {v} 張，正文寫唯一／全部許可是獸用：{s[:60]}"
    if v > 0 and (all_cancel(s) or NOT_MKT_CLAIM.search(s) or ((NOT_MKT_LOOSE.search(s) or ONLY_CANCEL.search(s)) and not POS_VALID.search(s))) \
            and not (still_valid_ok(s) and not NOT_MKT_CLAIM.search(s)):
        return "M3", f"事實有效 {v} 張，正文寫全部註銷：{s[:60]}"
    if site in ALLC_X_SITES and lang in M3X_LANGS and not REGISTRY_CTX.search(re.sub(r"\b(NDA|ANDA|BLA)\s*\d{6}\b", "", s)) \
            or site in ALLC_X_SITES and lang in M3X_LANGS and re.search(r"licen[cs]|authori[sz]|\b(A?NDA|BLA)s?\b|\bmarket(ing)? status\b|\blistings?\b", s):
        h = all_cancel_x(s, fc)
        if h:
            return "M3", h
    if site in TOTAL_X_SITES and lang in M3X_LANGS:
        h = total_x(site, s, fc)
        if h:
            return "M3", h
    if site in VALIDX_SITES and lang in M3X_LANGS:
        h = valid_under(site, s, fc)
        if h:
            return "M3", h
    if site in COMBO_X_SITES and lang in M3X_LANGS:
        h = combo_x(site, s, fc)
        if h:
            return "M3", h
    if ms in ("Cancelled only", "Not marketed") and (marketed_word(lang) in s or MKT_CLAIM_EXTRA.search(s)) and not mv2.NEG.search(s):
        return "M3", f"事實 {ms}，正文寫上市中：{s[:60]}"
    if site in LIST_CLAIM and LIST_PIPE.search(s) and not re.search(r"package insert|SmPC|data sheet", s, re.I):
        return "M3l", f"M3l 本站資料是處方／給付清單（{fc.get('total')} 筆），依設計不含許可資料；正文說許可資料應擷取／缺漏／擷取失敗：{s[:60]}"
    if site in LIST_CLAIM and (LIST_CLAIM[site].search(s) and not REGISTRY_CTX.search(s) or LIST_STRONG[site].search(s)) \
            and not LIST_EXCL.search(s) and not (LIST_REQUEST.search(s) and not LIST_NONE.search(s) and not LIST_STATUS.search(s)):
        return "M3l", f"M3l 本站資料是處方／給付清單（{fc.get('total')} 筆），不含許可狀態，正文寫成許可／有效／註銷／查無許可：{s[:60]}"
    if ms in ("Not marketed", "Cancelled only") and site in SCOPE_NOMKT and SCOPE_NOMKT[site].search(s):
        return "M3s", f"M3s 事實 {ms}（資料只含 {('HSA 現行註冊' if site == 'SgTxGNN' else 'EMA 集中許可')}），正文斷言沒有上市：{s[:60]}"
    if site in M3X_SITES:
        if ms == "Approved, not marketed" and lang in M3X_LANGS and MKT_CLAIM_EN.search(s) and not FORMER.search(s) and not REGISTRY_CTX.search(s):
            return "M3d", f"M3d 事實 {ms}，正文寫上市中：{s[:60]}"
        sub = m3x(lang, s, fc, site) or m3x_local(lang, s, fc, site)
        if sub:
            return sub, f"{sub} 事實 {ms}（有效 {v}／註銷 {fc.get('cancelled') or 0}），正文：{s[:60]}"
    return None


# 狀態列／張數列的站別寫法（2026-11-05）：Ca 把 DPD 的 DORMANT（核准、未銷售，DIN 未註銷）與 CANCELLED 分開寫
# US（2026-11-05，用戶決定）：FDA 核准申請（NDA／ANDA／BLA）與 OTC monograph／未核准類別的 NDC 列名產品分開寫；
# 列名產品沒有 FDA 申請號，不算許可（fc["listed"]＝列名產品數）
def _us_status(v, n, partial, fc):
    k = (fc or {}).get("listed") or 0
    lst = f"; OTC monograph / unapproved listings: {k}" if k else ""
    if partial:
        return f"Marketed (active FDA-approved applications on record: at least {v}{lst})"
    if n:
        return f"Marketed (active FDA-approved applications: {v} of {n}{lst})"
    return f"Marketed (no FDA-approved application; OTC monograph / unapproved listings: {k})"


def _us_count(fc):
    n, v = fc.get("total"), fc.get("valid") or 0
    if fc.get("partial"):
        return f"at least {n if n is not None else len(fc.get('licenses') or {})}"
    return f"{n} (active: {v})" if n else "0"


SPLIT_STATUS = {
    "UsTxGNN": {"fn": _us_status, "count_fn": _us_count},
    "ESTxGNN": {"full": "Comercializado (autorizaciones comercializadas: {v} de {n}{extra})",
                "part": "Comercializado (autorizaciones comercializadas: al menos {v}{extra})",
                "nm": "autorizadas no comercializadas: {k}", "c": "revocadas o suspendidas: {k}",
                "count_full": "{n} (comercializadas: {v})", "count_part": "al menos {n}", "sep": "; "},
    "CaTxGNN": {"full": "Marketed (marketed DINs: {v} of {n}{extra})", "part": "Marketed (marketed DINs on record: at least {v}{extra})",
                "nm": "dormant: {k}", "c": "cancelled: {k}", "count_full": "{n} (marketed: {v})", "count_part": "at least {n}",
                "sep": "; "},
}


def _split_extra(cfg, fc):
    parts = []
    if fc and (fc.get("not_marketed") or 0):
        parts.append(cfg["nm"].format(k=fc["not_marketed"]))
    if fc and (fc.get("cancelled") or 0):
        parts.append(cfg["c"].format(k=fc["cancelled"]))
    return (cfg["sep"] + cfg["sep"].join(parts)) if parts else ""


# 本地資料是處方／給付清單、不是許可證的站（2026-11-06）：張數列只寫清單筆數，不寫「有效 N」
SOURCE_COUNT = {"UkTxGNN": "{n}", "NZTxGNN": "{n}", "PhTxGNN": "{n}"}

# 這些站的事實是清單筆數，正文把清單品項說成許可、說有效／註銷、說查無許可證／資料抓取失敗，都跟事實矛盾（M3l）
_LICW = r"(licen[cs]es?|authori[sz]ations?|registrations?|PL numbers?|marketing authori[sz]ations?)"
def _list_claim(C, R):
    """C＝國名寫法、R＝主管機關（regex 片段）"""
    return re.compile((
    r"\b(valid|cancel+ed|revoked|withdrawn|expired|lapsed)\b[^.;:]{0,25}\b" + _LICW + r"|"
    r"\b" + _LICW + r"\b[^.;:]{0,30}\b(is|are|remains?|was|were)( currently| still| all)? (valid|cancel+ed|revoked|withdrawn|expired)\b|"
    r"\b(with (a )?valid status|its status is valid|status is (currently )?valid|listed as valid)\b|"
    r"\b(zero|no|0)[- ]({C} |{R} |valid |current |local )*(marketing )?(licen[cs]es?|licen[cs]e|authori[sz]ations?|registrations?)\b[^.;]{0,40}\b(recorded|returned|found|on record|result|retrieved|in (this|the) (evidence pack|data))|"
    r"\b(zero|no)[- ]licen[cs]e (result|record|finding)|\brecords? of zero\b|"
    r"\b(data|retrieval|ingestion|collection|mapping|pipeline|lookup) (ingestion |retrieval |mapping )?(failure|error)\b[^.;]{0,60}\b({R}|licen|authori|regist)|"
    r"\b({R}|licen|authori|regist)\w*\b[^.;]{0,60}\b(data|retrieval|ingestion|collection|mapping|pipeline|lookup) (failure|error)\b|"
    # 清單品項說成許可的張數（「Only one authorisation record is available」「one UK licence recorded」「The three authorisations below」）
    r"\b(only |the )?(one|1|two|three|four|five|six|seven|eight|nine|ten|a single|\d+) ({C} |{R} |marketing |single-ingredient |valid |current |local )*(authori[sz]ations?|licen[cs]es?|registrations?)\b|"
    r"\b(the )?(only|single|sole) ({C} |{R} |marketing )*(authori[sz]ation|licen[cs]e|registration)\b|"
    r"\b(zero|0) (active |{C} |{R} |current |valid )*(marketing )?(authori[sz]ations?|licen[cs]es?|registrations?)\b|"
    r"\bno ({C} |{R} |current |valid )*(marketing )?(authori[sz]ation|licen[cs]e|registration) (records?|data)\b|"
    r"\b(licen[cs]e|authori[sz]ation) (records?|table)\b|\(single-ingredient, valid\)|\bvalid\)|"
    # 說本藥在該國已許可／未許可（本站資料不含主管機關許可狀態）
    r"\bholds? (no |numerous |several |multiple |a |an )?(\w+ ){0,2}(marketing authori[sz]ations?|{R} (marketing )?authori[sz]ations?|{C} licen[cs]es?)\b|"
    r"\b(is|are) (currently )?(not )?(licensed|authori[sz]ed|registered)( for marketing)? in {IN}\b|"
    r"\bnot (currently )?authori[sz]ed for marketing\b|\bexpected to hold\b[^.;]{0,30}authori[sz]ations?|"
    r"\b(regulatory history)\b[^.;]{0,60}\b(pipeline|mapping|retrieval|ingestion) (error|failure)|"
    r"\bno ({C} |{R} )?marketing authori[sz]ations?\b|\b(no|without) ({C} )?licen[cs]e number\b|\bmarketing authori[sz]ation details recorded\b|"
    r"\bthe (licen[cs]e |authori[sz]ation )?record (gives|carries|contains|lists|has|does|is)\b|\b(is|are) currently authori[sz]ed\b|"
    r"\bthe (one|single|only) (authori[sz]ation|licen[cs]e) on record\b|"
    # 2026-11-06 第二輪（NZ／Uk 上線後掃出的漏網寫法）
    r"\b" + _LICW + r"\b[^.;:]{0,80}?\b(is|are|was|were|has been|have been|remains?)( also| currently| still| all| both| now)*( recorded as| listed as| marked as)? (valid|cancel+ed|revoked|withdrawn|expired|lapsed)\b|"
    r"\b(both|all|each)( \w+){0,4} (are|is|were|was|have been|has been)( also| currently| all| both)* (valid|cancel+ed|revoked|withdrawn|expired)\b|"
    r"\b" + _LICW + r"\s+(valid|cancel+ed|revoked|withdrawn|expired)\b|\blicen[cs]e validity\b|"
    r"\bno longer (actively )?(licensed|registered|authori[sz]ed|marketed)\b|"
    r"\b(zero|no|0) ({C} |{R} |registered |licensed |authori[sz]ed |valid |current |local |product )+(marketing )?(authori[sz]ations?|licen[cs]es?|registrations?)\b|"
    r"\b(one|two|three|four|five|six|seven|eight|nine|ten|\d+|a sixth|a fifth|one further|two further|three further|four further)( [\w-]+){0,3} (licen[cs]es?|authori[sz]ations?|registrations?)\b|"
    r"\bno ({R}-)?(registered|licensed|authori[sz]ed) products?\b|"
    r"\b(were|was|has been|have been)( previously)? (licensed|registered|authori[sz]ed)\b|"
    r"\bin fact (\w+ )?(authori[sz]ed|licensed|registered)\b|\bdespite the evidence pack\b|\bdata-source discrepancy\b|"
    r"\b" + _LICW + r"\b[^.;:]{0,40}\bas (valid|cancel+ed|revoked|withdrawn|expired)\b|"
    r"\b" + _LICW + r"\b[^.;:]{0,80}?\b(has|have)( also| now)? been (cancel+ed|revoked|withdrawn)\b|"
    r"\b(cancel+ed|revoked|withdrawn|expired|lapsed) ((registration|licen[cs]e|authori[sz]ation|market) )?status\b|\bstatus \((valid|cancel+ed|revoked|withdrawn|expired)\)|"
    r"\b(is|are) (currently )?(registered|licensed|authori[sz]ed) and marketed\b|\bno longer validly (registered|licensed|authori[sz]ed)\b|"
    # 2026-11-06 第三輪（Uk、NZ、Ph 全站逐句掃出的漏網寫法）：清單品項／紀錄說成有效或註銷、資料裡的「市場狀態」、
    # 註銷的名詞寫法（registration cancellation、reason for cancellation）、清單紀錄說成「許可紀錄」
    r"\bvalid (single[\w-]* |(?!regulatory )\w+ ){0,2}(products?|records?|entr(y|ies)|listings?|presentations?)\b|"
    r"\b(records?|products?|listings?|entr(y|ies)|presentations?)\b[^.;:]{0,60}?\b(is|are|was|were)( currently| also| still| all| both| now)*( recorded| listed| shown| marked)?( as)? (valid|cancel+ed|revoked|withdrawn|expired)\b|"
    r"\b(records?|listings?|entr(y|ies))\b[^.;:]{0,60}?\b(is|are)( currently)? marketed\b|"
    r"\band (it|they|both|all|each) (is|are) (currently |still |all |also )?((recorded|listed|shown|marked) )?(as )?(valid|cancel+ed)\b|"
    r"\b(no|zero|0) cancel+ed (products?|records?|entries|listings?)\b|\b(listing|record|entry) is a (single )?marketed\b|"
    r"\bmarket(ing)? status\b(?! (is|are) not included)[^.;]{0,60}?\b(is|was|as|recorded|listed|reported|shown|appears)\b[^.;]{0,25}?\b(marketed|cancel+ed)\b|"
    r"\b(overall|local) (market(ing)? )?status\b(?! (is|are) not included)|\b(overall )?status:\W{0,3}marketed\b|\brecord status\b|"
    r"\b(recorded|listed|shown|reported) as (currently )?marketed\b|"
    r"\b(records?|data)\b[^.;]{0,30}\b(show|shows|list|lists|holds?)\b[^.;]{0,40}\bas (currently )?marketed\b|"
    r"\b(registration|licen[cs]e|authori[sz]ation)s? cancell?ation\b|\bcancell?ation of the (\w+ ){0,3}(licen[cs]es?|registrations?|authori[sz]ations?)\b|"
    r"\breason for (the )?(\w+ )?cancell?ation\b|\bcancel+ed ((\w+ ){0,2})?(regulatory|registration|market) status\b|"
    r"\bmarket status is (marketed|cancel+ed)\b|\bsingle-ingredient (registration|licen[cs]e|authori[sz]ation)\b|"
    r"\b(local )?(registration|licen[cs]e|authori[sz]ation) records?\b|"
    # 舊證據包頁說本地資料查不到（search artefact、failed lookup、gap in the evidence pack…）：重建後清單有紀錄，這些說法與事實矛盾
    r"\b(search|data collection|lookup|query) arte?fact\b|\bfailed lookup\b|\bautomated pull\b[^.;]{0,40}\bfail|\bgap in the evidence pack\b|"
    r"\bpipeline failures? rather than\b|\babsence of an? ({C} |{R} )?marketing authori[sz]ation\b|\bJapanese-style drug code\b").replace("{C}", "(?:" + C + ")").replace("{R}", "(?:" + R + ")")
        .replace("{IN}", "(the )?(?:" + C + ")"), re.I)


def _list_strong(C, R):
    """清單站：國名／主管機關直接修飾許可字、或「N valid licences of N」的說法；句子同時講臨床試驗也照判（2026-11-06 第三輪：
    「…no clinical trials…, and the only New Zealand authorisation has been cancelled」原本被 REGISTRY_CTX 略過）"""
    L = r"(licen[cs]es?|authori[sz]ations?|registrations?)"
    return re.compile((
        r"\b(only|sole|single|the|its|this|product'?s?|both|all|two|three|four|five)( \w+)? ({C}|{R})( \w+)? " + L + r"\b[^.;]{0,30}?"
        r"\b(is|are|was|were|has been|have been)( all| also| now| currently)? (cancel+ed|revoked|withdrawn|expired|lapsed|valid)\b|"
        r"\b(cancel+ed|valid) ({C} |{R} )+" + L + r"\b|\b\d+ valid ({C} |{R} )?" + L + r" (of|out of) \d+\b|"
        r"\bwith all (\w+ )?" + L + r" valid\b|\bvalid (single-ingredient )?(licen[cs]es?|authori[sz]ations?)\b(?! numbers?)").replace("{C}", "(?:" + C + ")")
        .replace("{R}", "(?:" + R + ")"), re.I)


LIST_STRONG = {"UkTxGNN": _list_strong(r"UK|United Kingdom|British", r"MHRA"),
               "NZTxGNN": _list_strong(r"NZ|New Zealand", r"Medsafe"),
               "PhTxGNN": _list_strong(r"Philippines?|Philippine|PH|Filipino", r"FDA Philippines|PFDA")}
LIST_CLAIM = {"UkTxGNN": _list_claim(r"UK|United Kingdom|British", r"MHRA"),
              "NZTxGNN": _list_claim(r"NZ|New Zealand", r"Medsafe"),
              "PhTxGNN": _list_claim(r"Philippines?|Philippine|PH|Filipino", r"FDA Philippines|FDA|PFDA")}
# 「下一步需要的資料」條目（Verification of the UK authorisation record…、Approved indication text from the UK licence record…）
# 是要去查主管機關資料，不是說本藥許可如何，不算；但條目裡說「查無許可」的（zero-licence result）仍算
LIST_REQUEST = re.compile(r"^\W*(Verification|Verify|Confirmation|Confirm|Clarification|Clarify|Review|Retrieval|Retrieve|Obtain|Check|Complete|Completion|An assessment of whether|Assessment of whether|"
                          r"Approved indication|Original licensed|The approved indication|The authori[sz]ed indication|"
                          r"A (clear |verified )?(UK |MHRA |NZ |New Zealand |Medsafe |Philippines? |Philippine |FDA )?(licen[cs]e|authori[sz]ation|registration) record)\b", re.I)
LIST_NONE = re.compile(r"\bzero\b|\b0 (marketing )?(licen|authori|regist)|\bno (UK |MHRA |NZ |Medsafe |Philippines? |Philippine |FDA )?(marketing )?(licen|authori|regist)|"
                       r"\b(one|two|three|four|five|six|seven|eight|nine|ten|\d+|only|single|sole) (UK |MHRA |NZ |Medsafe |Philippines? |Philippine |FDA )?(marketing )?(authori[sz]ations?|licen[cs]es?|registrations?)\b", re.I)
# 下一步條目裡夾著「因為許可已註銷／N 張有效」這種說法時不豁免（只刪那個子句）；「valid licence number」是要號碼，不算
LIST_STATUS = re.compile(r"\b(cancel+ed|cancell?ation|revoked|withdrawn|expired|lapsed)\b|\b(is|are)( currently| all| also)? valid\b|"
                         r"\bvalid (licen[cs]es?|authori[sz]ations?|registrations?)\b(?! number)|\b\d+ (of|out of) \d+\b|\bis marketed\b|\bmarketed (in|with)\b", re.I)
LIST_EXCL = re.compile(r"status is not included in (this|the) data|not included in (this|the) data|rather than an? (MHRA|Medsafe|FDA)|unlicen[cs]ed|"
                       r"not (stated|recorded|listed|available) in the (\w+ ){0,2}(licen[cs]e|registration) records?|"
                       r"(licen[cs]e|registration) records? (compiled for this report )?(does|do) not (state|record|list|include)", re.I)  # 原適應症欄「Not stated in the licence record」講的是缺適應症文字


# 清單站（Uk、NZ、Ph）第四輪（2026-11-06 用戶決定）：舊頁說「去 MHRA／Medsafe／FDA PH 抓許可資料補進資料」「重跑資料擷取流程」
# 「許可資料／許可紀錄不完整、有誤、尚未載入」「這次資料擷取漏了許可」：本站資料依設計是處方／給付清單、不含許可，這些前提與事實不符（M3l）。
# 下一步條目（LIST_REQUEST）、試驗語境的句子也照判；仿單（package insert／SmPC）缺漏不算。
_PIPE_R = r"(?:MHRA|Medsafe|FDA(?: Philippines)?|PFDA|regulatory|licen[cs]e|licensing|marketing authori[sz]ation|PL)"
LIST_PIPE = re.compile(
    r"\bre-?(?:run|query|queried)\b[^.;]{0,60}\b(?:MHRA|Medsafe|FDA|PFDA|licen[cs]e|PL)\b(?! SmPC)|\b" + _PIPE_R + r"\b[^.;]{0,40}\b(?:ingestion|data pipeline|data collection step|data pull|database query)\b|"
    r"\bre-?run the data ingestion\b|\bregulatory data pull\b|\bmissed in the (?:current )?data pull\b|\bpopulate `?licen[cs]es`? array\b|\bPL numbers are expected\b|"
    r"\b" + _PIPE_R + r"\s+(?:licen[cs]e\s+|regulatory\s+)?(?:data|records?|details|entry)\b[^.;]{0,40}\b(?:(?:should|must) be (?:retrieved|loaded|ingested)|(?:have|has) not been loaded|"
    r"(?:is|are) correctly ingested|(?:is|are) (?:also )?incomplete|appears? erroneous)|\bregulatory entry is incomplete\b|\blicen[cs]e-level records\b|"
    r"\bdata pipeline has not (?:yet )?been populated\b|\bretrieve (?:current )?PL numbers\b|\bObtain MHRA marketing authori[sz]ation data\b|"
    r"\babsence of a standalone (?:MHRA |Medsafe )?marketing authori[sz]ation\b|\bClarification of the local licen[cs]e record\b|"
    r"\blocal (?:licen[cs]e|regulatory) records?\b(?=[^.;]{0,60}\b(?:missing|absent|incomplete))|\b(?:and|,)\s+local regulatory records\b|"
    r"\bUK (?:licen[cs]e record|authori[sz]ation details)\b[^.;]{0,60}\b(?:is|are) incomplete\b|\bUK licensing data compiled\b|\blicen[cs]e data are (?:also )?incomplete\b|"
    r"\bMHRA regulatory records\b|\bmarketing authori[sz]ation data (?:must|should) be loaded\b|\bMHRA Product Licen[cs]e (?:Search|Register)\b[^.;]{0,120}\b(?:re-?run|PL numbers|populate)", re.I)


def count_text(site, lang, fc):
    """張數列應有的值（M4 與各寫入程式共用）"""
    tl = mv2.T.get(lang) or mv2.T["en"]
    n, v, partial = fc.get("total"), fc.get("valid") or 0, fc.get("partial")
    if site in SOURCE_COUNT and not partial:
        return SOURCE_COUNT[site].format(n=n or 0, v=v)
    ex = _export_text(site, fc, "count")
    if ex:
        return ex
    if UNKNOWN_ST.get(site) and (fc.get("unknown") or 0) and not fc.get("partial"):
        return UNKNOWN_ST[site]["count"].format(n=fc.get("total"), v=fc.get("valid") or 0, u=fc["unknown"])
    if UNCONFIRMED_ST.get(site) and (fc.get("unconfirmed") or 0) and not fc.get("partial"):
        return UNCONFIRMED_ST[site]["count"].format(n=fc.get("total"), v=fc.get("valid") or 0, u=fc["unconfirmed"])
    cfg = SPLIT_STATUS.get(site)
    if cfg and "count_fn" in cfg:
        return cfg["count_fn"](fc)
    if partial:
        k = n if n is not None else len(fc.get("licenses") or {})
        return (cfg["count_part"] if cfg else tl[3]).format(n=k)
    return (cfg["count_full"] if cfg else tl[2]).format(n=n, v=v)


# 有效許可全部是只供出口的品目（Kr 수출용，2026-11-05 用戶決定）：核准未上市，張數列分開寫國內與出口。
# fc 的 export_only／export_total／export_valid／domestic_total 由該站 reviewer._local_regulatory 算（非部分紀錄才套用）
EXPORT_ONLY = {"KrTxGNN": {"status": "허가되었으나 미시판 (수출용 허가만 유효: {v}건 / 전체 {n}건)",
                           "count": "{n}건 (국내 {d}건 · 유효 0건 / 수출용 {e}건 · 유효 {v}건)"}}


def _export_text(site, fc, key):
    cfg = EXPORT_ONLY.get(site)
    if not cfg or not fc or not fc.get("export_only"):
        return None
    return cfg[key].format(v=fc.get("export_valid") or fc.get("valid") or 0, n=fc.get("total"), d=fc.get("domestic_total") or 0,
                           e=fc.get("export_total") or 0)


def not_marketed_text(site, lang, fc):
    """核准未上市的狀態列；部分紀錄（total 為空）時寫「至少 N」（2026-11-05 修 CO「registros: None」）"""
    ex = _export_text(site, fc, "status")
    if ex:
        return ex
    n = fc.get("total")
    if n is None:
        k = len(fc.get("licenses") or {})
        tl = mv2.T.get(lang) or mv2.T["en"]
        n = tl[3].format(n=k)
    return NOT_MKT.get(lang, NOT_MKT["en"]).format(n=n)



# 其他語言的 M3 擴充（2026-11-05，7 站逐站加；判定邏輯與 m3x 相同，只換該站語言的寫法）
_NUMW_ES = {"un": 1, "una": 1, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
            "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciséis": 16, "diecisiete": 17, "dieciocho": 18,
            "diecinueve": 19, "veinte": 20, "ambas": 2, "ambos": 2}
_NES = r"(\d+|" + "|".join(sorted(_NUMW_ES, key=len, reverse=True)) + r")"
X_LOCAL = {
    "es": dict(
        neg=re.compile(r"\b(no|ning[uú]n[oa]?|sin|ni|nunca)\b[^.;]{0,35}(vigente|comercializ|activ)", re.I),
        valid=re.compile(r"\b(est[aá]n?|son|es|figuran?|se encuentran?|sigue[n]?)\s+(tod[oa]s\s+)?vigentes?\b|\bEstado: vigente|"
                         r"\b(autorizaci\w+|registros?(\s+sanitarios?)?)\s+(\w+\s+){0,3}vigentes?\b|\bmonof[aá]rmacos? vigentes?\b", re.I),
        mkt=re.compile(r"\bcomercializad[oa]s? en (Españ|Colombi)|\b(est[aá]|se encuentra|queda) (ya |actualmente )?comercializad|"
                       r"\bse comercializan? (en|como)\b|\bya est[aá] comercializad|\bautorizad[oa] y comercializad", re.I),
        noreg=re.compile(r"\bno (tiene|cuenta con|dispone de|hay|posee)\b[^.;]{0,30}\b(registros?|autorizaci\w+|productos?)\b[^.;]{0,30}(vigente|activ|en (Españ|Colombi))|"
                         r"\bsin (ning[uú]n )?registros? (sanitarios? )?(vigentes?|activos?)|\bning[uú]n registro (sanitario )?(vigente|activo)|"
                         r"\bno figura con ning[uú]n registro|\b0 licencias\b|"
                         r"\b(registros?|autorizaci\w+)\b[^.;]{0,70}?\b(est[aá]n?|figuran?|son|es|fue|fueron|consta[n]?)\s+(tod[oa]s\s+|actualmente\s+|también\s+|como\s+)*(cancelad|anulad|revocad)|"
                         r"\b(tod[oa]s|ambos|ambas|el único|la única|su único|su única)\b[^.;]{0,70}?\b(cancelad|anulad|revocad)|"
                         r"\bno hay (un )?productos? vigentes?|\bno hay registros? (sanitarios? )?vigentes?", re.I),
        none_cancel=re.compile(r"\bning[uú]n[oa]? (\w+ ){0,3}(est[aá] )?(cancelad|anulad|revocad)|\bsin (\w+ ){0,2}(cancelad|anulad|revocad|cancelaciones|anulaciones)|"
                               r"\bno hay (\w+ ){0,3}(cancelad|anulad|revocad)", re.I),
        all_valid=re.compile(r"\btod[oa]s\b[^.;]{0,60}?\b(est[aá]n|son|figuran)\s+(\w+\s+){0,2}vigentes?|\btod[oa]s (\w+ ){0,3}vigentes\b|"
                             r"\b(ambas|ambos) (autorizaciones|registros)[^.;]{0,40}vigentes", re.I),
        count=[re.compile(r"\b" + _NES + r"\s+(autorizaciones|registros(?: sanitarios)?)\s+(\w+\s+){0,2}?(vigentes|activos|en vigor)\b", re.I),
               re.compile(r"\b(?:las|los)\s+" + _NES + r"\s+(autorizaciones|registros(?: sanitarios)?)\b[^.;]{0,50}?\b(est[aá]n|son|figuran)\s+(\w+\s+){0,2}vigentes", re.I)],
        partner=re.compile(r"\b(de las|de los|de)\s+" + _NES + r"\s*$", re.I),
        numw=_NUMW_ES, ctx=re.compile(r"ensayo|NCT\d|estudio|registro de ensayos|EudraCT|REEC", re.I)),
}


# 韓文（KrTxGNN，2026-11-05）：韓文否定在後（「유효한 허가가 없」「허가 이력이 없」），valid／mkt 以負向前瞻排除
_KNEG = r"(?![^.;,()]{0,14}(없|않|아니|미확인|확인되지 않|불가))"
X_LOCAL["ko"] = dict(
    neg=re.compile(r"(유효|시판|판매|허가)[^.;,]{0,14}(없|않|아니)"),
    valid=re.compile(r"유효(한|하며|합니다|하고|하다|함|상태|허가|하게)" + _KNEG + r"|정상 상태" + _KNEG + r"|허가되어 있(습니다|으며|고|는)|"
                     r"(현재|국내에서?|한국에서) (\w+ ){0,3}허가된" + _KNEG),
    mkt=re.compile(r"시판 ?중(인|이며|입니다|이다|이고)?" + _KNEG + r"|시판되(고|어) 있" + _KNEG + r"|판매 ?중(인|이며|입니다)?" + _KNEG),
    noreg=re.compile(r"(허가|시판 허가|시판) ?(이력|기록|내역)(이|은|가|도)? ?(없|전무|부재|0건)|(국내|한국) ?미허가|미허가 (약물|의약품|성분|상태)|"
                     r"허가(받은|된) (이력|기록|제품|품목)(이|은|가)? ?없|허가증?(이|은|가)? (없|존재하지 않)|허가 기록 0건|"
                     r"(모두|전부|모든 허가가?) (취소|취하|만료)|유효한 (허가|품목|제품)(증)?(이|은|가)? (없|존재하지 않)"),
    none_cancel=re.compile(r"(취소|취하)(된|건|된 허가|된 품목)?(은|는|이|가)? ?(없|0건)|(취소|취하) 0건"),
    all_valid=re.compile(r"(모두|전부|전체가?|모든 허가가?)\s+(\S+\s+){0,2}?(유효|정상)(?![^.;,]{0,8}(없|않|아니))"),
    count=[re.compile(r"(?<!최소 )(?<![\d.])(\d+)건(?!\s*이상)(의|이|은|가)?\s*((?!\d+건|중\s)\S+\s+){0,3}?(유효|정상)(?![^.;,]{0,8}(없|않|아니))")],
    partner=re.compile(r"(\d+건\s*(중|가운데)|최소|적어도)\s*$"),
    numw={}, ctx=re.compile(r"임상|NCT\d|시험|연구|CRIS|등록 ?번호"), cw=r"취소|취하|만료|cancel")


# 丹麥文（DkTxGNN，2026-11-05）
VET_CTX = re.compile(r"veterinær|dyrelæge|\bVet\.|til dyr\b|husdyr", re.I)
VET_ONLY_CLAIM = re.compile(r"\b(den|det) eneste\b[^.;]{0,60}(veterinær|dyrelæge)|\b(alle|begge)\b[^.;]{0,50}(er|gælder)[^.;]{0,20}(veterinær|dyrelæge)|"
                            r"\bregistreret (som|i ét|i et|i én|i en)\b[^.;]{0,25}(veterinær|dyrelæge)|\bgodkendt som dyrelægemiddel|"
                            r"\b(fundne|registrerede|danske) (tilladelser|godkendelser|produkter)\b[^.;]{0,20}\ber veterinær|"
                            r"\b(det|de) registrerede (produkt|produkter|præparat|præparater)\b[^.;]{0,15}\ber (et |en )?veterinær", re.I)
X_LOCAL["da"] = dict(
    neg=re.compile(r"\b(ikke|ingen|nul|uden)\b[^.;]{0,30}(gyldig|markedsført|godkendt)", re.I),
    valid=re.compile(r"\b(er|var) (\w+ ){0,2}gyldig(e|t)?\b|\bgyldige (tilladelser|markedsføringstilladelser|godkendelser)\b", re.I),
    mkt=re.compile(r"\b(er|bliver) (\w+ ){0,2}markedsført\b|\bmarkedsført i Danmark\b", re.I),
    noreg=re.compile(r"\b(nul|ingen) (?!annuller|tilbagekald|afregistrer|inaktiv)(\w+ ){0,2}(danske )?(markedsførings)?(tilladelser|godkendelser?)\b|\bikke markedsført i Danmark\b|"
                     r"\bingen dansk godkendelse\b|\bikke godkendt i Danmark\b|\bikke (registreret|godkendt) til (human|menneske)|"
                     r"\bikke godkendt til human brug\b|\bikke registreret (\w+ ){0,2}humane? (præparat|produkt|lægemid)|"
                     r"\bikke registreret som markedsført\b|\bikke (\w+ ){0,2}tilgængeligt? på det danske marked\b", re.I),
    none_cancel=re.compile(r"(?!x)x"), all_valid=re.compile(r"(?!x)x"), count=[], partner=re.compile(r"(?!x)x"),
    numw={}, ctx=re.compile(r"klinisk|NCT\d|forsøg|studie|EudraCT", re.I), cw=r"tilbagekald|afregistrer|cancel",
    preneg=r"\b(ikke|ingen|nul)\b[^.;]{0,30}$")


# 馬來文（MyTxGNN，2026-11-05）
_NUMW_MS = {"satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5, "enam": 6, "tujuh": 7, "lapan": 8, "sembilan": 9, "sepuluh": 10}
_NMS = r"(\d+|" + "|".join(_NUMW_MS) + r")"
X_LOCAL["ms"] = dict(
    neg=re.compile(r"\b(tidak|tiada|tanpa|bukan|belum)\b[^.;]{0,25}\b(sah|dipasarkan|berdaftar)\b", re.I),
    valid=re.compile(r"\bberstatus sah\b|\b(pendaftaran|lesen)( yang)? sah\b|\bmasih sah\b|\badalah sah\b", re.I),
    mkt=re.compile(r"\b(sedang |telah |masih )?dipasarkan di Malaysia\b|\b(sedang|masih) dipasarkan\b", re.I),
    noreg=re.compile(r"\btidak (berdaftar|didaftarkan)\b|\btidak (mempunyai|ada) (sebarang )?(pendaftaran|lesen|produk (yang )?berdaftar)\b|"
                     r"\btiada (sebarang )?(pendaftaran|lesen)\b(?![^.;]{0,40}\btunggal\b)|\(0 lesen\)|\bjumlah (lesen|pendaftaran): 0\b|"
                     r"\btiada lesen tempatan\b", re.I),
    none_cancel=re.compile(r"\btiada (\w+ ){0,2}(yang )?(dibatalkan|dibatal)\b|\btiada pembatalan\b|\b0 (dibatalkan|pembatalan)\b", re.I),
    all_valid=re.compile(r"\b(kesemua|semua)\b[^.;]{0,40}?\b(berstatus sah|adalah sah|masih sah)\b|\b(kesemua|semua) (\w+ ){0,3}(pendaftaran|lesen) (yang )?sah\b", re.I),
    count=[re.compile(r"\b" + _NMS + r" (pendaftaran|lesen)\b[^.;]{0,20}?\b(yang )?(sah|berstatus sah)\b", re.I),
           re.compile(r"\b(?:kesemua|semua) " + _NMS + r" (pendaftaran|lesen)\b[^.;]{0,30}?\b(berstatus sah|adalah sah|sah)\b", re.I)],
    partner=re.compile(r"\b(daripada|dari)\s*$", re.I), numw=_NUMW_MS,
    ctx=re.compile(r"NCT\d|pendaftaran (ujian|percubaan)|ClinicalTrials|daftar (ujian|percubaan)", re.I),
    cw=r"batal|cancel|tamat|expir", preneg=r"\b(tidak|tiada|tanpa|bukan|belum)\b[^.;]{0,30}$")


def m3x_local(lang, s, fc, site):
    """M3a／M3b／M3c／M3d 的非英文寫法（X_LOCAL 有該語言才查）"""
    R = X_LOCAL.get(lang)
    if not R or not fc or CTX_NARROW.get(site, R["ctx"]).search(s):
        return None
    ms, v, c, nm = fc.get("market_status"), fc.get("valid") or 0, fc.get("cancelled") or 0, fc.get("not_marketed") or 0
    negd = bool(R["neg"].search(s))
    if ms in ("Cancelled only", "Not marketed") and (R["valid"].search(s) or R["mkt"].search(s)) and not negd:
        return "M3a"
    if ms == "Approved, not marketed" and R["mkt"].search(s) and not negd:
        return "M3d"
    cw = R.get("cw", r"cancel|anul|revoc")
    if ms == "Approved, not marketed" and c > 0 and R["all_valid"].search(s) and not re.search(cw, s, re.I):
        return "M3c"
    posv = any(not re.search(R.get("preneg", r"\b(no|ning[uú]n[oa]?|sin|ni|no hay)\b[^.;]{0,30}$"), s[:m.start()], re.I) for m in R["valid"].finditer(s))
    if v > 0 and c == 0 and site in CANC_NOUN and CANC_NOUN[site].search(s) and not R["none_cancel"].search(s):
        return "M3b"
    if v > 0 and (R["noreg"].search(s) or (site in NOREG_EXTRA and NOREG_EXTRA[site].search(s))) and not R["none_cancel"].search(s) and not posv:
        return "M3b"
    if c > 0 and (not fc.get("partial") or site in M3X_PARTIAL):
        if R["none_cancel"].search(s) or (R["all_valid"].search(s) and not re.search(cw, s, re.I)):
            return "M3c"
        vl = v + (nm if site in LEGAL_NM_VALID else 0)
        for rx in (R["count"] if not (fc.get("partial") and lang == "ko") else ()):  # 部分紀錄的 v 只是下限（Kr，2026-11-05）
            for m in rx.finditer(s):
                g = m.group(1).lower()
                k = int(g) if g.isdigit() else R["numw"].get(g)
                pre = s[max(0, m.start() - 14):m.start()]
                if k and k > vl and not AT_LEAST.search(pre) and not R["partner"].search(pre) and not (re.search(r"\bde( las| los)?\s*$", pre, re.I) and re.search(r"\b(est[aá]n|son|figuran)\b", m.group(0), re.I)):
                    return "M3c"
    return None


def marketed_word(lang):
    return re.split(r"[（(]", (mv2.T.get(lang) or mv2.T["en"])[0])[0].strip()


def is_count_label(label):
    return bool(mv2.COUNT_LABEL.search(label) and LIC_WORD.search(label) and not SCORE_HDR.search(label))


def _pick_own(site, cands):
    own = re.compile(OWN.get(site, r"$^"), re.I)
    for r in cands:
        if own.search(r[0]):
            return r
    for r in cands:
        if not FOREIGN_ANY.search(r[0]):
            return r
    return None


STATUS_LABEL = re.compile(mv2.LABEL.pattern + r"|comercializ|commercialis|commercializ|vermarkt|markedsfør|markkinoill|dipasarkan", re.I)


def status_row(site, rows):
    std = (MARKET_LABELS.get(site) or ("", ""))[1]
    return _pick_own(site, [r for r in rows if len(r) >= 2 and STATUS_LABEL.search(r[0]) and not is_count_label(r[0]) and r[0] != std])


def count_row(site, rows):
    std = (MARKET_LABELS.get(site) or ("", ""))[1]  # 字串檔的標準欄位名（例：Number of PBS Items 不含許可證字樣）也認，且優先
    exact = [r for r in rows if len(r) >= 2 and std and r[0] == std]
    return exact[0] if exact else _pick_own(site, [r for r in rows if len(r) >= 2 and is_count_label(r[0])])


# ---------- 資料 ----------
@lru_cache(maxsize=None)
def classification():
    out = {}
    with open(BASE / ".claude/audit_20261016/m2/classification.tsv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            out[(r["site"], r["page"])] = r["class"]
    return out


@lru_cache(maxsize=None)
def facts(site):
    p = BASE / ".claude/cache/license_facts" / f"{site}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


@lru_cache(maxsize=None)
def fhir(site):
    cud, mk = defaultdict(list), {}
    root = BASE / site / "docs/fhir"
    res = []
    for f in list((root / "MedicationKnowledge").glob("*.json")) + list((root / "ClinicalUseDefinition").glob("*.json")):
        try:
            res.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            pass
    for f in (root / "Bundle").glob("*.json"):
        try:
            res += [e.get("resource") or {} for e in json.loads(f.read_text(encoding="utf-8")).get("entry", [])]
        except Exception:
            pass
    seen = set()
    for d in res:
        if d.get("resourceType") == "MedicationKnowledge":
            names = {norm_name(d.get("id")), norm_name((d.get("code") or {}).get("text"))}
            names |= {norm_name(c.get("code")) for c in (d.get("code") or {}).get("coding", [])}
            names |= {norm_name(c.get("display")) for c in (d.get("code") or {}).get("coding", [])}
            mk[str(d.get("id"))] = names - {""}
        elif d.get("resourceType") == "ClinicalUseDefinition" and d.get("type") == "indication":
            if d.get("id") in seen:
                continue
            seen.add(d.get("id"))
            ext = {e.get("url", "").rsplit("/", 1)[-1]: e for e in d.get("extension", [])}
            status = (ext.get("prediction-status") or {}).get("valueCode")
            if status and status != "predicted":
                continue
            subj = ((d.get("subject") or [{}])[0].get("reference") or "").split("/")[-1]
            text = (((d.get("indication") or {}).get("diseaseSymptomProcedure") or {}).get("concept") or {}).get("text", "")
            sc = next((e.get("valueDecimal") for k, e in ext.items() if "score" in k), None)
            cud[subj].append((norm_name(text), sc, json.dumps(d, ensure_ascii=False)))
    return cud, mk


@lru_cache(maxsize=None)
def search_index(site):
    for p in ("docs/data/search-index.json", "docs/assets/data/search-index.json", "docs/search-index.json"):
        f = BASE / site / p
        if f.exists():
            d = json.loads(f.read_text(encoding="utf-8"))
            drugs = d.get("drugs", []) if isinstance(d, dict) else d
            return {str(x.get("slug", "")).lower(): x for x in drugs if isinstance(x, dict)}
    return {}


LOCAL_EN = re.compile(r"^\**(.+?)\**\s*[（(]\s*\**([A-Za-z0-9][^()（）]*?(?:\([^()]*\)[^()（）]*?)?)\**\s*[)）]\s*\**$")


@lru_cache(maxsize=None)
def local_names(site):
    """英文病名（小寫）→ 當地名稱集合；來源＝站內頁面的表格儲存格、粗體與 search-index 的「當地名 (English)」"""
    en2loc = defaultdict(set)
    if LANG.get(site, "en") in ("en", "en-us"):
        return en2loc  # 英文站的當地名就是英文；「病名 (說明文字)」不是對照（2026-10-23 Us abacavir 誤判）

    def add(cell):
        m = LOCAL_EN.match(cell.strip())
        # 括號裡要像病名：不是證據等級（L4）、分數或純數字（2026-10-23 Th amoxicillin「monoclonal gammopathy (L4)」誤判）
        if m and re.fullmatch(r"L[1-5]|[\d.,%\s]+|score.*|pontua.*|punt.*", m.group(2).strip(), re.I):
            return
        if m and norm_name(m.group(1)) != norm_name(m.group(2)) and len(m.group(1)) <= 80:
            en2loc[norm_name(m.group(2))].add(m.group(1).strip().strip("*"))
    for f in (BASE / site / "docs/_drugs").glob("*.md"):
        t = f.read_text(encoding="utf-8", errors="replace")
        for line in t.split("\n"):
            if line.startswith("|"):
                for c in line.strip("|").split("|"):
                    add(c)
            for bb in re.findall(r"\*\*([^*]{2,120})\*\*", line):
                add(bb)
    for x in search_index(site).values():
        for i in x.get("indications") or []:
            add(str(i.get("name", "")))
    # pm 核對過的譯名（main_by_score 全量核對結果）：site、english、local
    vt = RULES / "verified_translations.tsv"
    if vt.exists():
        for r in csv.DictReader(open(vt, encoding="utf-8"), delimiter="\t"):
            if r.get("site") == site and r.get("english") and r.get("local"):
                en2loc[norm_name(r["english"])].add(r["local"].strip())
    return en2loc


@lru_cache(maxsize=None)
def name_regexes(site, en):
    out = [re.compile(r"(?<![A-Za-z])" + re.escape(en) + r"(?![A-Za-z])", re.I)]
    for loc in local_names(site).get(norm_name(en), ()):
        if re.search(r"[A-Za-z]", loc):
            out.append(re.compile(r"(?<![A-Za-zÀ-ÿ])" + re.escape(loc) + r"(?![A-Za-zÀ-ÿ])", re.I))
        else:
            out.append(re.compile(re.escape(loc)))
    return tuple(out)


@lru_cache(maxsize=None)
def _loc2en(site):
    m = {}
    for en, locs in local_names(site).items():
        for l in locs:
            m.setdefault(norm_name(l), en)
    return m


def index_english(site, name):
    if LANG.get(site, "en") in ("en", "en-us"):
        # 英文站沒有「當地名 (English)」對照：「amenorrhea (disease)」的括號是 TxGNN 病名的一部分
        #（2026-11-03 Us：198 頁 search-index 因此被誤判 P7，與 local_names 的英文站處理一致）
        return norm_name(name)
    m = LOCAL_EN.match(str(name).strip())
    if m and norm_name(m.group(2)) not in ("disease", "disorder"):
        return norm_name(m.group(2))
    # 「transient ischemic attack (disease)」：括號裡只是 TxGNN 病名的限定詞，整串就是英文病名（2026-11-03 非英文站同一誤判）
    m2 = None if m else re.match(r"^(.*[^\x00-\x7f].*?)\s*[（(]\s*([^（）()]*[A-Za-z][^（）()]*)\s*[)）]\s*$", str(name).strip())
    if m2:  # 當地名本身含全形括號、英文名以數字開頭（Hk「46,XY 性發育異常（睪丸類固醇合成缺陷） (46,XY disorder …)」，2026-11-03）
        return norm_name(m2.group(2))
    n = norm_name(name)
    if n in local_names(site) or kf._n(name) in kf._graph()[0]:
        return n  # 本身就是英文病名（含 TxGNN 疾病節點名稱：站內對照偶有反向或縮寫，例 Nl「kattenaids」、SE「DFSP」，2026-11-03）
    return _loc2en(site).get(n, n)


def parse_fm_list(fm, key):
    m = re.search(rf"^{key}:\s*(\[.*\])\s*$", fm, re.M)
    if m:
        return json.loads(m.group(1))
    m = re.search(rf"^{key}:\s*\n((?:[ \t]*-[ \t].*\n?)+)", fm, re.M)
    if m:
        return [re.sub(r"^\s*-\s*", "", l).strip().strip('"').strip("'") for l in m.group(1).split("\n") if l.strip()]
    return []


def evidence_titles(p):
    out = []
    for k in ("clinical_trials", "ictrp_trials", "literature", "pubmed_articles", "pubmed"):
        v = p.get(k) or []
        if isinstance(v, dict):
            v = v.get("results") or []
        out += [str(x.get("title", "")) for x in v if isinstance(x, dict)]
    return " ".join(out)


# C6：常見縮寫（頁內有「病名 (縮寫)」定義的也算）
COMMON_ABBR = {"rheumatoid arthritis": ["RA"], "multiple sclerosis": ["MS"], "amyotrophic lateral sclerosis": ["ALS"],
               "systemic lupus erythematosus": ["SLE"], "chronic obstructive pulmonary disease": ["COPD"],
               "attention deficit hyperactivity disorder": ["ADHD"], "attention deficit-hyperactivity disorder": ["ADHD"],
               "acute myeloid leukemia": ["AML"], "chronic lymphocytic leukemia": ["CLL"], "acute lymphoblastic leukemia": ["ALL"],
               "chronic myelogenous leukemia": ["CML"], "non-small cell lung carcinoma": ["NSCLC"], "inflammatory bowel disease": ["IBD"],
               "gastroesophageal reflux disease": ["GERD"], "polycystic ovary syndrome": ["PCOS"], "parkinson disease": ["PD"],
               "alzheimer disease": ["AD"], "human immunodeficiency virus infectious disease": ["HIV"], "HIV infectious disease": ["HIV"],
               "myelodysplastic syndrome": ["MDS"], "pulmonary arterial hypertension": ["PAH"], "deep vein thrombosis": ["DVT"]}
_GEN = {"heart", "liver", "kidney", "lung", "skin", "blood", "bone", "eye", "brain", "muscle"}


def _abbrs(name, page_abbr):
    n = norm_name(name)
    out = set(COMMON_ABBR.get(n, []))
    for k, v in page_abbr.items():
        if k.endswith(n):
            out |= v
    return out


def _generic_removed(name):
    core = [w for w in re.findall(r"[a-z]+", name.lower()) if w not in rr.GENERIC_WORDS]
    return len(core) <= 1 and (not core or core[0] in _GEN)


MAIN_BY_SCORE = []  # 主預測只靠「概覽分數唯一等於 kept[0]」放行的頁（pm M5 抽查）


# ---------- 單頁 ----------
MANAGED = re.compile(r"<!-- (review:begin \S+|brand-names:start) -->.*?<!-- (review:end \S+|brand-names:end) -->", re.S)


REPORT_TITLE = re.compile(r"^(## .*)\n\{: \.text-alpha \}[ \t]*$", re.M)


def report_titles(body):
    """D1：報告標題（H2 下一行是 {: .text-alpha }）的標題文字清單"""
    return [m.group(1) for m in REPORT_TITLE.finditer(body)]


def strip_managed(body):
    """人工查核框（Tw drug_reviews）與販売名區塊（Jp brand_names）是另外維護的內容，P5／M3 不查（2026-10-29）"""
    return MANAGED.sub("", body)


# Tw（2026-11-06）：已核准用途排除表（known_use_overlap_exclude.json）的預測，Tw 依該站規則不刪 front matter、不改 H1，
# 改寫成重審「撤回」紀錄（docs/_data/drug_reviews.json 的 rereview_result＋verdict=withdraw＋known_use_exclusion[].predicted，
# tw_known_use_withdraw_20261103.py 寫的；頁面不發布撤回預測由 Tw 自己的 gate 第 7d 項檢查）。
# 所以 Tw 的「頁面該列的預測」裡，排除表命中、而且本頁有撤回紀錄的照舊算數；沒有撤回紀錄的照樣排除（P1 會報）。
OVERLAP_VIA_REVIEW = {"TwTxGNN"}
_WD = {}


def review_withdrawn(site):
    """{頁面檔名: {正規化病名}}：本站 drug_reviews.json 裡 verdict=withdraw 的已核准用途撤回"""
    if site not in _WD:
        p = BASE / site / "docs/_data/drug_reviews.json"
        out = {}
        recs = (json.loads(p.read_text(encoding="utf-8")).get("records") or []) if p.exists() else []
        for r in recs:
            if r.get("action") == "rereview_result" and r.get("verdict") == "withdraw":
                stem = (r.get("file") or "").removesuffix(".md")
                for e in r.get("known_use_exclusion") or []:
                    if e.get("predicted"):
                        out.setdefault(stem, set()).add(norm_name(e["predicted"]))
        _WD[site] = out
    return _WD[site]


def check_page(site, f, cls, want_noindex):
    errs = []
    E = lambda code, detail="": errs.append((code, detail))
    t = f.read_bytes().decode("utf-8").replace("\r\n", "\n")
    if 'http-equiv="refresh"' in t[:3000]:
        return []
    fm, _, body = t[4:].partition("\n---")
    lang = LANG.get(site, "en")
    rt = report_titles(body)
    if len(rt) > 1:  # D1：不需要證據包，先查
        E("D1", f"一頁 {len(rt)} 份報告標題，第二個：{rt[1][:60]}")
    b = amf.load_bundle(BASE / site, f.stem)
    if b is None:
        return errs + [("P1", "找不到證據包")]
    d = b.get("drug") or {}
    preds = {norm_name(p["disease_name"]): p for p in d.get("predicted_indications") or [] if p.get("disease_name")}
    top = [p["disease_name"] for p in d.get("predicted_indications") or [] if (p.get("txgnn_score") or 0) >= kf.SCORE_MIN][:10]
    kept = kf.kept_predictions(BASE / site, b) if cls not in ("no_pred_keep", "no_pred_noindex") else []
    if site in OVERLAP_VIA_REVIEW and kept is not None and cls not in ("no_pred_keep", "no_pred_noindex"):
        wd = review_withdrawn(site).get(f.stem, set())
        if wd:  # 排除表命中、而且本頁有撤回紀錄的預測放回原位（Tw 的 front matter、H1 依該站規則不改）
            kn = {norm_name(k) for k in kept}
            kept = [k for k in kf.kept_predictions(BASE / site, b, overlap=False) if norm_name(k) in kn or norm_name(k) in wd]
    keptn = {norm_name(k) for k in kept}
    excluded = [x for x in top if norm_name(x) not in keptn]
    kept_sc = [preds[norm_name(k)]["txgnn_score"] for k in kept if norm_name(k) in preds]

    # P1
    shown = parse_fm_list(fm, "predicted_indications")
    if [norm_name(x) for x in shown] != [norm_name(x) for x in kept]:
        E("P1", f"front matter {len(shown)} 項≠kept {len(kept)} 項")
    cnt = re.search(r"^indication_count:\s*(\d+)", fm, re.M)
    if not cnt or int(cnt.group(1)) != len(kept):
        E("P1", f"indication_count={cnt.group(1) if cnt else None}≠{len(kept)}")
    lvl = (re.search(r"^evidence_level:\s*(\S+)", fm, re.M) or [None, ""])[1]
    if cls in ("known_use", "no_pred_keep", "no_pred_noindex"):
        if kept:
            E("P1", "已知用途／無預測頁但 kept 不是空的")
        if lvl != "N/A":
            E("P1", f"無預測／已知用途頁 evidence_level={lvl}")

    tbs = tables(body)
    ov_rows = tbs[0][1] if tbs else []
    pred_row = next((r for r in ov_rows if len(r) >= 2 and PRED_ROW.search(r[0])), None)
    lvl_row = next((r for r in ov_rows if len(r) >= 2 and LEVEL_ROW.search(r[0]) and LEVEL.search(r[1])), None)

    score_rows = []
    for hdr, rows, lines, head in tbs:
        si = next((i for i, h in enumerate(hdr) if SCORE_HDR.search(h)), None)
        for cells, line in zip(rows, lines):
            if si is not None and si < len(cells) and score_tokens(cells[si]):
                score_rows.append((cells, line, cells[si]))
            elif len(cells) >= 2 and SCORE_HDR.search(cells[0]) and score_tokens(cells[1]):
                score_rows.append((cells, line, cells[1]))
    # P2、P6（表格）
    for cells, line, cell in score_rows:
        toks = score_tokens(cell)
        if any(not matches_kept(v, kept_sc) for v, _, _ in toks):
            E("P2", f"分數「{cell[:20]}」不屬於 kept 或 <0.99")
        if any(pct for _, pct, _ in toks):
            E("P6", f"分數寫成百分比：{cell[:20]}")
        if CONF.search(line):
            E("P6", f"分數列出現信心字眼：{line[:60]}")
    # P2、P6（本文：同句有分數字樣或 TxGNN 的數字才當分數）
    for line in body.split("\n"):
        if line.startswith("|"):
            continue
        for s in sentences(line):
            if not SCORE_CTX.search(s):
                continue
            toks = [x for x in score_tokens(s) if x[0] >= 0.5]
            if not toks:
                continue
            if any(not matches_kept(v, kept_sc) for v, _, _ in toks):
                E("P2", f"本文分數不屬於 kept 或 <0.99：{s[:60]}")
            if any(pct for _, pct, _ in toks):
                E("P6", f"本文分數寫成百分比：{s[:60]}")
            if CONF.search(s):
                E("P6", f"本文分數寫成信心：{s[:60]}")
    # P6（2026-10-28 pm）：沒有分數字樣也算——括號裡的 9x.xx%（「Agoraphobia (99.84%, L3)」）或任何 99.xx%（兩位小數）
    #     都是分數寫成百分比；臨床數據（95.9% 治癒率、一位小數）不算。表格列（快速總覽以外）也查。
    for line in body.split("\n"):
        for s in (sentences(line) if not line.startswith("|") else [line]):
            if SCORE_CTX.search(s) and not line.startswith("|"):
                continue  # 上面已判
            if PCT_SCORE.search(norm_digits(s)):
                E("P6", f"本文分數寫成百分比：{s[:60]}")

    # P3
    # 報告標題：`# ` 開頭，或 2026-10-27 起降級後的「`## ` ＋下一行 {: .text-alpha }」（每頁只留一個 h1）
    _bl = body.split("\n")
    h1 = "\n".join(l for k, l in enumerate(_bl) if l.startswith("# ") or
                   (l.startswith("## ") and k + 1 < len(_bl) and _bl[k + 1].strip() == "{: .text-alpha }"))
    desc = (re.search(r"^description:\s*(.*)$", fm, re.M) or [None, ""])[1]
    hay = {"H1": h1, "description": desc, "概覽預測列": " ".join(pred_row[1:]) if pred_row else "",
           "預測列": "\n".join(l for _, l, _ in score_rows)}
    # 2026-10-27 pm：命中的字串剛好就是本地許可證記載的原適應症（概覽表原適應症格，且同一規則也命中許可證適應症文字）→ 不算
    lic_ind = [r.get("indication") or "" for r in ((b.get("tfda") or {}).get("records") or []) if (r.get("indication") or "").strip()]
    orig_cell = next((r[1] for r in (tbs[0][1] if tbs else []) if len(r) >= 2 and ORIG_ROW.search(r[0])), "")
    for x in excluded:
        for rx in name_regexes(site, x):
            if any(rx.search(k) for k in kept):
                continue
            def hit(h):
                # 2026-10-28 pm：已排除病名只是 kept 名稱的一部分（dermatitis ⊂ atopic dermatitis）不算 → 命中位置落在 kept 名稱命中範圍內就略過
                kspans = [m2.span() for k in kept for krx in name_regexes(site, k) for m2 in krx.finditer(h)]
                for m in rx.finditer(h):
                    if any(a <= m.start() and m.end() <= z for a, z in kspans):
                        continue
                    if re.fullmatch(r"L[1-5]", m.group(0).strip()):  # 2026-10-29：縮寫比對撞到證據等級 L1–L5，不是病名
                        continue
                    if not (orig_cell and m.group(0).lower() in orig_cell.lower() and any(rx.search(t) for t in lic_ind)):
                        return True
                return False
            where = next((w for w, h in hay.items() if hit(h)), None)
            if where:
                E("P3", f"已排除「{x}」出現在{where}"); break

    # P3（pm C6）：因分數門檻／刷新而移除、但不是已知用途的預測，正文仍當預測或給分數（英文、當地名、頁內縮寫）
    removed = set()
    bk = BASE / ".claude/cache/bundle_backup_20261022" / site / f.stem / "drug_bundle.json"
    if not bk.exists():
        bk = BASE / ".claude/cache/bundle_backup_20261022" / site / f.stem.replace("-", "_") / "drug_bundle.json"
    old_names = [p.get("disease_name") for p in (json.loads(bk.read_text(encoding="utf-8"))["drug"].get("predicted_indications") or [])] if bk.exists() else []
    old_names += [p.get("disease_name") for p in d.get("predicted_indications") or []]
    old_names += parse_fm_list(fm, "predicted_indications")
    cand = sorted({x for x in old_names if x and norm_name(x) not in keptn})
    if cand:
        not_known = set(kf.filter_predictions(BASE / site, d.get("drugbank_id") or "", (d.get("inn") or d.get("name") or "").strip(), cand, b))
        removed = [x for x in cand if x in not_known]
    abbr = {}
    for m in re.finditer(r"([A-Za-z][A-Za-z' \-]{3,80}?)\s*\(([A-Z][A-Z0-9-]{1,6})\)", body):
        abbr.setdefault(norm_name(m.group(1).split(",")[-1]), set()).add(m.group(2))
    if removed:
        for line in body.split("\n") + [desc]:
            if line.startswith("|") and not score_tokens(line):
                continue  # 表格只看帶分數的列（已知用途表、原適應症列不算）
            if line.startswith("#"):
                continue
            for s in sentences(line):
                if KNOWN_USE_OK.search(s) and not (score_tokens(s) or SCORE_PRED_STRICT.search(s)):
                    continue  # 已知用途句
                hit = None
                for x in removed:
                    if _generic_removed(x):
                        continue
                    rxs = list(name_regexes(site, x)) + [re.compile(r"(?<![A-Za-z0-9])" + re.escape(a) + r"(?![A-Za-z0-9])")
                                                         for a in _abbrs(x, abbr)]
                    if any(rx.search(s) for rx in rxs) and not any(rx.search(s) for k in kept for rx in name_regexes(site, k)):
                        hit = x; break
                if hit:
                    E("P3", f"已移除的「{hit}」仍在正文：{s[:60]}")
    # P3（pm）：H1、description 的主預測必須是 kept[0]
    if kept and cls not in ("known_use", "no_pred_keep", "no_pred_noindex"):
        rx0 = list(name_regexes(site, kept[0]))
        cell = " ".join(pred_row[1:]) if pred_row else ""
        other = [x for x in kept[1:] + excluded if any(rx.search(cell) for rx in name_regexes(site, x))]
        is_main = bool(cell) and any(rx.search(cell) for rx in rx0)
        if cell and not is_main and not other:
            # 對照表沒收到的譯名：概覽表分數列要唯一等於 kept[0] 的分數，才可認定是 kept[0]（pm 2026-10-23：不可預設為對）
            sc_row = next((r for r in ov_rows if len(r) >= 2 and SCORE_HDR.search(r[0]) and score_tokens(r[1])), None)
            if sc_row and kept[0] and norm_name(kept[0]) in preds:
                v = score_tokens(sc_row[1])[0][0]
                same = [x for x in kept + excluded if norm_name(x) in preds and
                        abs(round(preds[norm_name(x)]["txgnn_score"], 4) - v) < 0.00005 or
                        (norm_name(x) in preds and abs(round(preds[norm_name(x)]["txgnn_score"] * 100, 2) - v * 100) < 0.005)]
                is_main = same == [kept[0]] or (len(same) == 1 and norm_name(same[0]) == norm_name(kept[0]))
                if is_main:
                    MAIN_BY_SCORE.append((site, f.stem, cell, kept[0]))
        if cell and not is_main:
            E("P3", f"概覽表預測列不是 kept[0]「{kept[0]}」：{(other[0] if other else cell)[:40]}")
        elif cell:
            loc = re.sub(r"[（(][^()（）]*[)）]", "", cell).strip(" *")
            if loc and len(loc) >= 2:
                rx0.append(re.compile(re.escape(loc), re.I))
        for where, h in (("H1", h1), ("description", desc)):
            if h and not any(rx.search(h) for rx in rx0):
                E("P3", f"{where} 的主預測不是 kept[0]「{kept[0]}」")

    # P4（逐列）
    def pred_of(text):
        for k in kept:
            if any(rx.search(text) for rx in name_regexes(site, k)):
                return preds.get(norm_name(k))
        v = [x for x, _, _ in score_tokens(text)]
        for k in kept:
            p = preds.get(norm_name(k))
            if p and v and any(abs(round(p["txgnn_score"] * 100, 2) - y * 100) < 0.005 or abs(round(p["txgnn_score"], 4) - y) < 0.00005 for y in v):
                return p
        return None
    lv_items = []
    for hdr, rows, lines, head in tbs:
        li = next((i for i, h in enumerate(hdr) if LEVEL_ROW.search(h)), None)
        if li is None:
            continue
        for cells, line in zip(rows, lines):
            if li < len(cells) and LEVEL.search(cells[li]):
                lv_items.append((LEVEL.search(cells[li]).group(1), line))
    if lvl_row and pred_row:
        lv_items.append((LEVEL.search(lvl_row[1]).group(1), " ".join(pred_row[1:])))
    for lv, text in lv_items:
        if lv == "L5":
            continue
        p = pred_of(text)
        if p is not None and not rr.direct_evidence(p["disease_name"], evidence_titles(p)):
            E("P4", f"{lv} 但證據包沒有直接研究「{p['disease_name']}」")

    # P5
    for s in p5_hits(strip_managed(body) + "\n" + desc, lang):
        E("P5", s[:80])

    # P7
    cud, mk = fhir(site)
    keys = {norm_name(f.stem), norm_name(f.stem.replace("_", "-")), norm_name(f.stem.replace("-", "_")),
            norm_name(d.get("drugbank_id")), norm_name(d.get("inn")), norm_name(d.get("name"))} - {""}
    ids = [i for i, names in mk.items() if names & keys]
    want = sorted(keptn)
    # 站上 force_noindex.json 列的頁（用戶核准下架；Us 2026-11-06 PEG 3500）衍生檔依決定拿掉了本藥：不報「找不到」，有的話仍檢查內容
    _ffp = BASE / site / "docs/_data/force_noindex.json"
    forced7 = _ffp.exists() and f.stem in json.loads(_ffp.read_text(encoding="utf-8")).get("pages", {})
    if not ids:
        if kept and not forced7:
            E("P7", "找不到 MedicationKnowledge")
    for i in ids:
        rows7 = cud.get(i, [])
        if sorted(x[0] for x in rows7) != want:
            E("P7", f"FHIR {len(rows7)} 筆≠kept {len(kept)}")
        if any(sc is not None and sc < 0.99 for _, sc, _ in rows7):
            E("P7", "FHIR 有 <0.99 分數")
        if any("TxGNN Knowledge Graph" in raw for _, _, raw in rows7):
            E("P7", "FHIR 來源寫成 TxGNN Knowledge Graph")
    si = search_index(site)
    x = si.get(f.stem.lower()) or si.get(f.stem.replace("_", "-").lower())
    if x is not None:
        inds = x.get("indications") or []
        if sorted(index_english(site, i.get("name", "")) for i in inds) != want:
            E("P7", f"search-index 病名≠kept（{len(inds)}／{len(kept)}）")
        if any(float(i.get("score") or 0) < 99 for i in inds):
            E("P7", "search-index 有 <0.99 分數")
    elif kept and not forced7:
        E("P7", "search-index 沒有此藥")

    # K1（依分區）
    if cls == "known_use":
        for hdr, rows, lines, head in tbs:
            if not head.startswith("###"):
                continue
            zone = "kg" if KG_WORD.search(head) else (
                "related" if re.search(r"categor|類別|同類|カテゴリ|범주|Kategori|catégorie|categoría|luokka|kategori|فئة|หมวด", head, re.I) else "approved")
            if zone != "approved":
                continue
            for line in lines:
                for xn in excluded:
                    if any(rx.search(line) for rx in name_regexes(site, xn)):
                        z = kup.classify(site, b, xn)
                        if not z or not z[0].startswith("approved"):
                            E("K1", f"「{xn}」出處是 {z[0] if z else '無'}，卻放在核准區")

    # M1／M2
    fc = facts(site).get(f.stem) or facts(site).get(f.stem.replace("-", "_")) or facts(site).get(f.stem.replace("_", "-"))
    all_rows = [r for _, rows, _, _ in tbs for r in rows]
    st = status_row(site, all_rows)
    if not fc:
        E("M1", "沒有 license_facts")
    else:
        ms, v, n, partial = fc.get("market_status"), fc.get("valid"), fc.get("total"), fc.get("partial")
        tl = mv2.T.get(lang) or mv2.T["en"]
        if st is None:
            E("M1", "找不到本站狀態列")
        else:
            if ms == "Marketed":
                want_s = marketed_text(site, lang, v, n, partial, fc)
                if st[1] != want_s:
                    E("M1", f"狀態列「{st[1][:40]}」≠「{want_s}」")
            elif ms == "Approved, not marketed":
                want_s = not_marketed_text(site, lang, fc)
                if st[1] != want_s:
                    E("M1", f"狀態列「{st[1][:40]}」≠「{want_s}」")
            elif ms == "Status unknown" and site in UNKNOWN_ST:
                want_s = unknown_status_text(site, lang, fc)
                if st[1] != want_s:
                    E("M1", f"狀態列「{st[1][:40]}」≠「{want_s}」")
            elif ms == "Not marketed" and site in VET_ONLY:
                want_s = not_reg_text(site, lang, fc)
                if st[1] != want_s:
                    E("M1", f"狀態列「{st[1][:40]}」≠「{want_s}」")
            elif ms == "Not marketed" and site in NO_CENTRAL:
                want_s = NO_CENTRAL[site]
                if st[1] != want_s:
                    E("M1", f"狀態列「{st[1][:40]}」≠ 資料範圍句（{site} 只有 EMA 集中許可）")
            nm_prefix = re.split(r"[（(]", NOT_MKT.get(lang, NOT_MKT["en"]))[0].strip()
            if ms != "Marketed" and (marketed_word(lang) in st[1] or "✓" in st[1]) and not mv2.NEG.search(st[1]) and nm_prefix not in st[1]:
                E("M2", f"事實 {ms}，狀態列寫成上市中：{st[1][:40]}")
        cr = count_row(site, all_rows)
        if cr is None:
            E("M1", "找不到張數列")
        elif n is not None:
            if site == "TwTxGNN":
                a = re.search(r"^(\d+)", cr[1].strip())
                vv = sum(int(x) for x in re.findall(r"有效[單複]方\s*(\d+)", cr[1]))
                ok = bool(a) and int(a.group(1)) == n and (ms != "Marketed" or vv == v)
            else:
                nums = [int(x) for x in re.findall(r"\d+", norm_digits(cr[1]))]
                ok = n in nums and (v is None or ms != "Marketed" or v in nums)
                if partial and not AT_LEAST.search(cr[1]):
                    ok = False
            if not ok:
                E("M1", f"張數列「{cr[1][:40]}」≠ 共 {n}／有效 {v}{'（部分紀錄）' if partial else ''}")
        # M4（2026-10-31 pm 退件 BR）：張數列要跟狀態列同一套事實、同一套寫法（部分紀錄也要檢查），不得有括號內部註記
        # （例「20 (todos cancelados)」配「pelo menos 20」的狀態列、「0 (consulta realizada com grafia incorreta…)」）。Tw 格式不同，不查。
        if cr is not None and site != "TwTxGNN" and (n is not None or partial):
            want_c = count_text(site, lang, fc)
            if cr[1] != want_c:
                E("M4", f"張數列「{cr[1][:50]}」≠「{want_c}」")
        lic = {mv2.norm_id(k): s for k, s in (fc.get("licenses") or {}).items()}
        if site != "TwTxGNN":
            for cells in all_rows:
                k = mv2.norm_id(cells[0]) if cells else ""
                if lic.get(k) == "valid" and mv2.TABLE_NEG.search(" ".join(cells[1:])):
                    E("M1", f"有效許可證 {cells[0]} 寫成註銷")
            for code_, detail in row_status_conflicts(site, all_rows, lic):
                E(code_, detail)
    # M3（pm C1）：正文市場說法與事實矛盾
    if fc:
        ms, v = fc.get("market_status"), fc.get("valid") or 0
        for line in strip_managed(body).split("\n") + [desc]:
            if line.startswith("|") or line.startswith("#"):
                continue
            for s in sentences(line):
                hit = m3_verdict(site, lang, s, fc)
                if hit and any(k in s for k in license_keep(site).get(f.stem, ())):
                    continue  # 人工核對過：句子混有療效／機轉內容，不刪（scripts/license_sentence_fixes.json 的 keep 項）
                if hit:
                    E("M3", hit[1])
        # M5（2026-11-05）：非 Tw 站殘留 TwTxGNN 模板的台灣上市狀態列／taiwan_regulatory 欄位／「台灣無許可」句
        if site != "TwTxGNN":
            for line in strip_managed(body).split("\n"):
                if TW_LEFTOVER.search(line) and not any(k in line for k in license_keep(site).get(f.stem, ())):
                    E("M5", f"殘留台灣模板：{line.strip()[:60]}")
    # N1
    if want_noindex:
        has = bool(re.search(r"^noindex:\s*true", fm, re.M))
        # 站上 docs/_data/force_noindex.json 列的頁（用戶核准、附依據；Us 2026-11-06 PEG 3500）一律 noindex
        _ff = BASE / site / "docs/_data/force_noindex.json"
        forced = _ff.exists() and f.stem in json.loads(_ff.read_text(encoding="utf-8")).get("pages", {})
        if (cls == "no_pred_noindex" or forced) != has:
            E("N1", f"class={cls} noindex={has}")
    return errs


# ---------- 自我測試 ----------
# M1 擴充（2026-11-06，Us 用戶決定）：許可證表的號碼格夾著狀態字（「NDA208743 (cancelled)」「ANDA… (Hikma), cancelled」），
# 或狀態寫在別欄（「Not specified (valid)」），而狀態跟事實層不一致 → M1。原本的檢查只認號碼格「恰好是號碼」的列，這種寫法漏掉
# （Us 2026-11-06：144 頁把有效寫成註銷、44 頁把停產寫成有效）。號碼樣式各站不同，只在 TABLE_ROW_STATUS 的站查。
TABLE_ROW_STATUS = {"UsTxGNN": re.compile(r"\b(NDA|ANDA|BLA)\s*(\d{6})\b")}
_ROW_NEG = re.compile(mv2.TABLE_NEG.pattern + r"|discontinu", re.I)
_ROW_POS = re.compile(r"\bvalid\b|\bactive\b", re.I)


def row_status_word(cells):
    """表格列（含號碼格）寫的狀態：cancelled／valid／None"""
    txt = " ".join(cells)
    if _ROW_NEG.search(txt):
        return "cancelled"
    return "valid" if _ROW_POS.search(txt) else None


def row_status_conflicts(site, rows, lic):
    """[(代碼, 說明)]：號碼格含本站許可證號（可夾別的字）、列上寫的狀態跟事實相反"""
    rx = TABLE_ROW_STATUS.get(site)
    out = []
    for cells in rows if rx else []:
        m = rx.search(cells[0]) if cells else None
        if not m:
            continue
        st = lic.get(mv2.norm_id(m.group(1) + m.group(2)))
        said = row_status_word(cells)
        if st == "valid" and said == "cancelled":
            out.append(("M1", f"有效許可證 {cells[0]} 寫成註銷（列上的狀態字）"))
        elif st == "cancelled" and said == "valid":
            out.append(("M1", f"已停產／註銷的許可證 {cells[0]} 寫成有效（列上的狀態字）"))
    return out


def selftest():
    rows = list(csv.DictReader(open(RULES / "test_cases.tsv", encoding="utf-8"), delimiter="\t"))
    bad = 0
    for r in rows:
        code, lang, text, expect, note = r["code"], r["lang"], r["text"], r["expect"], r.get("note") or ""
        if code == "P5":
            got = bool(p5_hits(text, lang, note[8:] if note.startswith("section=") else ""))
        elif code == "P6":
            toks = [x for x in score_tokens(text) if x[0] >= 0.5]
            got = any(p for _, p, _ in toks) or (bool(toks) and bool(CONF.search(text)))
        elif code == "P2":  # kept 分數固定 0.9950；句子要有分數字樣
            got = bool(SCORE_CTX.search(text)) and any(not matches_kept(v, [0.995]) for v, _, _ in score_tokens(text) if v >= 0.5)
        elif code == "COUNT_LABEL":
            got = is_count_label(text)
        elif code == "PRED_ROW":
            got = bool(PRED_ROW.search(text))
        elif code == "M3":  # note＝valid=<n> 或 cancelled（事實）
            if note.startswith("valid="):
                got = int(note[6:]) > 0 and bool(all_cancel(text) or NOT_MKT_CLAIM.search(text) or
                                                 (NOT_MKT_LOOSE.search(text) and not POS_VALID.search(text))) \
                    and not (still_valid_ok(text) and not NOT_MKT_CLAIM.search(text))
            else:
                got = (marketed_word(lang) in text or bool(MKT_CLAIM_EXTRA.search(text))) and not mv2.NEG.search(text)
        elif code == "M3X":  # note＝ms=<市場狀態>;valid=<n>;cancelled=<n>[;partial=1]（2026-11-05 M3 擴充）
            kv = dict(x.split("=", 1) for x in note.split(";") if "=" in x)
            got = bool(m3x(lang, text, {"market_status": kv.get("ms"), "valid": int(kv.get("valid", 0)),
                                        "cancelled": int(kv.get("cancelled", 0)), "partial": kv.get("partial") == "1"}))
        elif code == "M3V":  # note＝site=<站>;ms=…;valid=…;not_marketed=…;cancelled=…[;partial=1][;lic=號碼:狀態,…]：m3_verdict（含 M3d、站別規則，2026-11-05）
            kv = dict(x.split("=", 1) for x in note.split(";") if "=" in x)
            fcv = {"market_status": kv.get("ms"), "valid": int(kv.get("valid", 0)), "not_marketed": int(kv.get("not_marketed", 0)),
                   "cancelled": int(kv.get("cancelled", 0)), "partial": kv.get("partial") == "1",
                   **({"total": int(kv["total"])} if "total" in kv else {}), **({"listed": int(kv["listed"])} if "listed" in kv else {}),
                   **({"valid_single": int(kv["vs"]), "single_total": int(kv.get("st", kv["vs"]))} if "vs" in kv else {}),
                   "licenses": dict(x.split(":", 1) for x in kv.get("lic", "").split(",") if ":" in x)}  # lic=NDA123456:valid,ANDA…:cancelled
            M3X_SITES.add(kv.get("site"))  # 測試案例的站一律啟用
            got = bool(m3_verdict(kv.get("site"), lang, text, fcv))
        elif code == "M5":  # text＝一行；非 Tw 站的台灣模板殘留
            got = bool(TW_LEFTOVER.search(text))
        elif code == "P3C6":  # text＝「已移除病名|句子」：正文提到已移除（非已知用途）的病名（含常見縮寫），已知用途句除外
            name, s = text.split("|", 1)
            rxs = [re.compile(r"(?<![A-Za-z])" + re.escape(name) + r"(?![A-Za-z])", re.I)] + \
                  [re.compile(r"(?<![A-Za-z0-9])" + re.escape(a) + r"(?![A-Za-z0-9])") for a in _abbrs(name, {})]
            known_only = KNOWN_USE_OK.search(s) and not (score_tokens(s) or SCORE_PRED_STRICT.search(s))
            got = any(rx.search(s) for rx in rxs) and not known_only
        elif code == "INDEX_EN":  # text＝「站|search-index 病名」，note＝應得的英文病名
            site, name = text.split("|", 1)
            got = index_english(site, name) == note
        elif code == "D1":  # text 裡的「\\n」是換行：兩個以上報告標題（H2＋{: .text-alpha }）才算
            got = len(report_titles(text.replace("\\n", "\n"))) > 1
        elif code == "ROW_STATUS":  # text＝「站|表格列」，note＝事實（號碼=valid|cancelled）
            site, row = text.split("|", 1)
            k, s = note.split("=", 1)
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            got = bool(row_status_conflicts(site, [cells], {mv2.norm_id(k): s}))
        elif code == "STATUS_ROW":  # text＝「站|列標題1;列標題2」，note＝應選中的列標題
            site, labels = text.split("|", 1)
            pick = status_row(site, [[l, "x"] for l in labels.split(";")])
            got = bool(pick) and pick[0] == note
        else:
            print("未知代碼", code); bad += 1; continue
        if got != (expect == "hit"):
            bad += 1
            print("FAIL", code, lang, expect, text[:100])
    print(f"selftest {len(rows) - bad}/{len(rows)} 通過")
    return bad == 0


def main(argv):
    if "--selftest" in argv:
        sys.exit(0 if selftest() else 1)
    want_noindex = "--noindex" in argv
    pages = None
    if "--pages" in argv:
        pages = {tuple(x.split(":", 1)) for x in argv[argv.index("--pages") + 1].split(",")}
    sites = [a for a in argv if a.endswith("TxGNN")] or sorted({p[0] for p in pages} if pages else (p.name for p in BASE.glob("*TxGNN")))
    OUT.mkdir(parents=True, exist_ok=True)
    cl = classification()
    rows, per = [], Counter()
    for s in sites:
        for f in sorted((BASE / s / "docs/_drugs").glob("*.md")):
            if pages is not None and (s, f.stem) not in pages:
                continue
            cls = cl.get((s, f.stem))
            if cls is None:
                continue  # 轉址頁、原本就 noindex 的頁不在範圍
            for code, detail in check_page(s, f, cls, want_noindex):
                rows.append((s, f.stem, code, detail)); per[(s, code)] += 1
        print(s, {c: per[(s, c)] for c in sorted({c for (x, c) in per if x == s})}, flush=True)
    with open(OUT / "results.tsv", "w", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["site", "page", "code", "detail"]); w.writerows(rows)
    with open(OUT / "main_by_score.tsv", "w", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["site", "page", "overview_cell", "kept0"]); w.writerows(MAIN_BY_SCORE)
    tot = Counter(r[2] for r in rows)
    print("合計", dict(tot), "頁數", len({(r[0], r[1]) for r in rows}), "主預測靠分數放行", len(MAIN_BY_SCORE))
    sys.exit(1 if rows else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
