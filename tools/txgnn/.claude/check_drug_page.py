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
N1 noindex（--noindex 時才查）：no_pred_noindex 的頁要有 noindex: true，其他頁不得有
用法（母目錄）：python3 .claude/check_drug_page.py [--selftest] [--noindex] [--pages site:page,...] [站 ...]
輸出 .claude/audit_20261016/check/results.tsv（site, page, code, detail）；有錯 exit 1。
"""
import csv
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / ".claude/audit_20261016/check"
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
}


# 2026-10-30（用戶選「沿用現有來源排程」）：這些站的「本地資料」不是主管機關許可證資料，狀態列照實陳述來源，
# 不寫成「已許可、上市中」。{v}／{n}＝在列筆數（同原本的有效／總數）；部分紀錄用第二個模板。
SOURCE_STATUS = {
    "NZTxGNN": ("Listed on the Pharmac Pharmaceutical Schedule ({v} of {n} items) – Medsafe licence status is not included in this data",
                "Listed on the Pharmac Pharmaceutical Schedule (at least {v} items) – Medsafe licence status is not included in this data"),
    "UkTxGNN": ("Listed in NHSBSA BNF presentation codes ({v} of {n}) – MHRA licence status is not included in this data",
                "Listed in NHSBSA BNF presentation codes (at least {v}) – MHRA licence status is not included in this data"),
    "ARTxGNN": ("Incluido en el listado de medicamentos de PAMI ({v} de {n}) – el estado del registro en ANMAT no está incluido en estos datos",
                "Incluido en el listado de medicamentos de PAMI (al menos {v}) – el estado del registro en ANMAT no está incluido en estos datos"),
    "AuTxGNN": ("Listed on the PBS Schedule ({v} of {n} items) – TGA (ARTG) registration status is not included in this data",
                "Listed on the PBS Schedule (at least {v} items) – TGA (ARTG) registration status is not included in this data"),
    "InTxGNN": ("Listed in a compiled Indian medicine price dataset ({v} of {n}) – CDSCO approval status is not included in this data",
                "Listed in a compiled Indian medicine price dataset (at least {v}) – CDSCO approval status is not included in this data"),
    "PhTxGNN": ("Listed in the Philippine National Formulary ({v} of {n}) – FDA Philippines registration status is not included in this data",
                "Listed in the Philippine National Formulary (at least {v}) – FDA Philippines registration status is not included in this data"),
}
# TH 2026-10-31 移出：原本的許可證號是程式編造的，改用 Thai FDA 查詢系統（pertento）的真實許可證，狀態列回到一般寫法


def marketed_text(site, lang, v, n, partial):
    """事實是 Marketed 時的狀態列：來源不是許可證資料的站用 SOURCE_STATUS，其他站用 mv2.T"""
    if site in SOURCE_STATUS:
        return SOURCE_STATUS[site][1 if partial else 0].format(v=v, n=n)
    tl = mv2.T.get(lang) or mv2.T["en"]
    return (tl[1] if partial else tl[0]).format(v=v, n=n)


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
}


def cancelled_text(site, lang, n):
    """事實是 Cancelled only 時的狀態列"""
    return (SCOPE_CANCELLED.get(site) or CANCELLED.get(lang, CANCELLED["en"])).format(n=n)


def not_reg_text(site, lang):
    """查無許可紀錄時的狀態列：EMA 代理站用資料範圍句，其他站用 NOT_REG"""
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
    r"\bnessun[a]?\b[^.\n]{0,40}valid|\bgeen\b[^.\n]{0,40}geldig|\binga\b[^.\n]{0,40}giltig|\btiada\b[^.\n]{0,40}sah", re.I)
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


LOCAL_EN = re.compile(r"^\**(.+?)\**\s*[（(]\s*\**([A-Za-z][^()（）]*?(?:\([^()]*\)[^()（）]*?)?)\**\s*[)）]\s*\**$")


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
    m = LOCAL_EN.match(str(name).strip())
    if m:
        return norm_name(m.group(2))
    n = norm_name(name)
    if n in local_names(site):
        return n  # 本身就是英文病名
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


def strip_managed(body):
    """人工查核框（Tw drug_reviews）與販売名區塊（Jp brand_names）是另外維護的內容，P5／M3 不查（2026-10-29）"""
    return MANAGED.sub("", body)


def check_page(site, f, cls, want_noindex):
    errs = []
    E = lambda code, detail="": errs.append((code, detail))
    t = f.read_bytes().decode("utf-8").replace("\r\n", "\n")
    if 'http-equiv="refresh"' in t[:3000]:
        return []
    fm, _, body = t[4:].partition("\n---")
    lang = LANG.get(site, "en")
    b = amf.load_bundle(BASE / site, f.stem)
    if b is None:
        return [("P1", "找不到證據包")]
    d = b.get("drug") or {}
    preds = {norm_name(p["disease_name"]): p for p in d.get("predicted_indications") or [] if p.get("disease_name")}
    top = [p["disease_name"] for p in d.get("predicted_indications") or [] if (p.get("txgnn_score") or 0) >= kf.SCORE_MIN][:10]
    kept = kf.kept_predictions(BASE / site, b) if cls not in ("no_pred_keep", "no_pred_noindex") else []
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
    if not ids:
        if kept:
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
    elif kept:
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
                want_s = marketed_text(site, lang, v, n, partial)
                if st[1] != want_s:
                    E("M1", f"狀態列「{st[1][:40]}」≠「{want_s}」")
            elif ms == "Approved, not marketed":
                want_s = NOT_MKT.get(lang, NOT_MKT["en"]).format(n=n)
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
        lic = {mv2.norm_id(k): s for k, s in (fc.get("licenses") or {}).items()}
        if site != "TwTxGNN":
            for cells in all_rows:
                k = mv2.norm_id(cells[0]) if cells else ""
                if lic.get(k) == "valid" and mv2.TABLE_NEG.search(" ".join(cells[1:])):
                    E("M1", f"有效許可證 {cells[0]} 寫成註銷")
    # M3（pm C1）：正文市場說法與事實矛盾
    if fc:
        ms, v = fc.get("market_status"), fc.get("valid") or 0
        for line in strip_managed(body).split("\n") + [desc]:
            if line.startswith("|") or line.startswith("#"):
                continue
            for s in sentences(line):
                if v > 0 and (ALL_CANCEL.search(s) or NOT_MKT_CLAIM.search(s) or (NOT_MKT_LOOSE.search(s) and not POS_VALID.search(s))) \
                        and not (still_valid_ok(s) and not NOT_MKT_CLAIM.search(s)):
                    E("M3", f"事實有效 {v} 張，正文寫全部註銷：{s[:60]}")
                elif ms in ("Cancelled only", "Not marketed") and (marketed_word(lang) in s or MKT_CLAIM_EXTRA.search(s)) and not mv2.NEG.search(s):
                    E("M3", f"事實 {ms}，正文寫上市中：{s[:60]}")
    # N1
    if want_noindex:
        has = bool(re.search(r"^noindex:\s*true", fm, re.M))
        if (cls == "no_pred_noindex") != has:
            E("N1", f"class={cls} noindex={has}")
    return errs


# ---------- 自我測試 ----------
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
                got = int(note[6:]) > 0 and bool(ALL_CANCEL.search(text) or NOT_MKT_CLAIM.search(text) or
                                                 (NOT_MKT_LOOSE.search(text) and not POS_VALID.search(text))) \
                    and not (still_valid_ok(text) and not NOT_MKT_CLAIM.search(text))
            else:
                got = (marketed_word(lang) in text or bool(MKT_CLAIM_EXTRA.search(text))) and not mv2.NEG.search(text)
        elif code == "P3C6":  # text＝「已移除病名|句子」：正文提到已移除（非已知用途）的病名（含常見縮寫），已知用途句除外
            name, s = text.split("|", 1)
            rxs = [re.compile(r"(?<![A-Za-z])" + re.escape(name) + r"(?![A-Za-z])", re.I)] + \
                  [re.compile(r"(?<![A-Za-z0-9])" + re.escape(a) + r"(?![A-Za-z0-9])") for a in _abbrs(name, {})]
            known_only = KNOWN_USE_OK.search(s) and not (score_tokens(s) or SCORE_PRED_STRICT.search(s))
            got = any(rx.search(s) for rx in rxs) and not known_only
        elif code == "INDEX_EN":  # text＝「站|search-index 病名」，note＝應得的英文病名
            site, name = text.split("|", 1)
            got = index_english(site, name) == note
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
