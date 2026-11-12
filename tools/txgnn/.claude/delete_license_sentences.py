"""刪除藥物頁正文裡跟許可證事實矛盾的句子（2026-11-05，用戶決定 7 站比照 Za 修；全程不用 AI、不改寫）。

判定與 check_drug_page.py 共用（m3_verdict＝M3／M3a–M3d，TW_LEFTOVER＝M5），所以刪完 checker 的 M3／M5 會歸零；
另讀本站 scripts/license_sentence_fixes.json 的人工清單（頁 → [{sentence, reason}]，checker 抓不到但已用新資料核對過的句子）。
規則：
- 正文（front matter、標題、概覽表狀態／張數列以外）跟事實矛盾的句子整句刪除；整行空掉就拿掉該行，連續空行併成一行。
- 表格列：只刪 M5（台灣模板殘留的狀態列、taiwan_regulatory dump 列）；表格只剩表頭時整張拿掉。
- 緊接在被刪句後面、以指代詞開頭的句子（DEPENDENT，各語言）一併刪除，避免留下失去指涉的半句。
- 刪掉的句子逐句寫進 --log（頁、規則、原句、依據）。
用法（工作目錄，先跑 dump_license_facts）：python3 .claude/delete_license_sentences.py <站> [--dry-run] [--log out.tsv] [--pages a,b]
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
_s = importlib.util.spec_from_file_location("ck", BASE / ".claude/check_drug_page.py")
ck = importlib.util.module_from_spec(_s); _s.loader.exec_module(ck)

ABBR = [("e.g.", "e‧g‧"), ("i.e.", "i‧e‧"), ("vs.", "vs‧"), ("No.", "No‧"), ("et al.", "et al‧"), ("approx.", "approx‧"), ("Vet.", "Vet‧"),
        ("p. ej.", "p‧ ej‧"), ("aprox.", "aprox‧"), ("fx.", "fx‧"), ("bl.a.", "bl‧a‧"), ("mht.", "mht‧"), ("Inc.", "Inc‧"), ("Ltd.", "Ltd‧"),
        ("S.A.", "S‧A‧"), ("U.S.", "U‧S‧"), ("Dr.", "Dr‧"), ("St.", "St‧"), ("Co.", "Co‧"), ("spp.", "spp‧"), ("Sdn.", "Sdn‧"), ("Bhd.", "Bhd‧"),
        ("S.r.l.", "S‧r‧l‧"), ("S.p.A.", "S‧p‧A‧"), ("B. Braun", "B‧ Braun"), ("F.C.", "F‧C‧"), ("B.P.", "B‧P‧")]
  # 公司名、產品名裡的點（Sg 2026-11-06）
# 2026-11-06 第二批站：該語言的縮寫（只在該語言的頁、以詞界比對，避免「Africa.」被當成「ca.」）
ABBR_X = {"de": ["bzw.", "z. B.", "z.B.", "u. a.", "u.a.", "ggf.", "ca.", "Nr.", "d. h.", "d.h.", "v. a.", "inkl.", "evtl.", "sog.", "vgl.", "Abs.", "Art."],
          "fr": ["p. ex.", "cf.", "env.", "n°."], "it": ["ad es.", "ecc.", "cfr.", "n."], "nl": ["bijv.", "o.a.", "m.b.t.", "i.p.v.", "ca."],
          "sv": ["t.ex.", "t. ex.", "bl.a.", "m.m.", "ca.", "s.k."], "no": ["f.eks.", "bl.a.", "ca.", "mm."], "fi": ["esim.", "ns.", "mm.", "n."],
          "pt": ["p. ex.", "ex.", "Ltda.", "Dra.", "aprox."], "es": []}


DEPENDENT = {
    "en": re.compile(r"^\W*(It|Its|This|These|They|Their|Those|As noted above|See the note above|Without these|Under these)\b"),
    "es": re.compile(r"^\W*(Esto|Este|Esta|Estos|Estas|Ello|Por ello|Por lo tanto|Dicho|Dicha)\b"),
    "ko": re.compile(r"^\W*(이는|이것은|이러한|따라서 이|그러므로 이|이 때문에|이 중|그중|그 중|이 가운데|그 가운데|나머지는|나머지 \d+건|아래는 그중|위 표는 그중)"),
    "ms": re.compile(r"^\W*(Ini|Hal ini|Oleh itu|Perkara ini)\b"),
    "da": re.compile(r"^\W*(Det|Dette|Disse|De|Derfor|Den siger|Listen er)\b"),
    "de": re.compile(r"^\W*(Dies|Diese|Dieser|Dieses|Daher|Deshalb|Somit|Damit|Demnach)\b"),
    "fi": re.compile(r"^\W*(Tämä|Tämän|Nämä|Näiden|Siksi|Sen vuoksi|Siten|Näin ollen)\b"),
    "no": re.compile(r"^\W*(Dette|Denne|Disse|Derfor|Dermed|Det betyr)\b"),
    "it": re.compile(r"^\W*(Ciò|Questo|Questa|Questi|Queste|Pertanto|Quindi|Per questo)\b"),
    "sv": re.compile(r"^\W*(Detta|Denna|Dessa|Därför|Därmed|Det innebär)\b"),
    "fr": re.compile(r"^\W*(Cela|Ceci|Ce|Cette|Ces|Par conséquent|Ainsi|Donc)\b"),
    "pt": re.compile(r"^\W*(Isso|Isto|Este|Esta|Estes|Estas|Portanto|Assim|Dessa forma)\b"),
    "nl": re.compile(r"^\W*(Dit|Deze|Daarom|Hierdoor|Daardoor|Dat)\b"),
}


# 2026-11-05 用戶決定：同一句混有藥物身分、療效或機轉內容時，只刪跟事實矛盾的子句（原句文字照舊，只做刪除）
CLAIM = [ck.MKT_CLAIM_EN, ck.VALID_COUNT, ck.NONE_CANCEL, ck.VALID_CLAIM, ck.NOREG_CLAIM,
         re.compile(r"\bmarketed (in|as|under)\b[^,;.]*", re.I), re.compile(r"\b\d+ valid\b[^,;.]*", re.I)]
for _R in ck.X_LOCAL.values():
    CLAIM += [_R["mkt"], _R["valid"], _R["none_cancel"], _R["noreg"]] + list(_R["count"])
CLAIM += list(getattr(ck, "NOREG_EXTRA", {}).values())  # 站別補充寫法（CO）
CLAIM += list(getattr(ck, "CANC_NONE", {}).values())  # 全部有效時的「已註銷」說法（Eu）
# 處方／給付清單站（Uk、NZ、Ph）：清單品項寫成許可的說法只對該站生效（clause_cut 裡依站加上，Ph 的「FDA」不影響 Us 等站）
CLAIM += list(getattr(ck, "SCOPE_NOMKT", {}).values())  # 只陳述資料範圍的站：「沒有上市」斷言（Sg、Eu）
CLAIM += list(getattr(ck, "ALLC_X", []))  # 英文「全部（或唯一）許可已註銷」的寫法（Us，2026-11-06）
if hasattr(ck, "TOTAL_SPAN"):
    CLAIM.append(ck.TOTAL_SPAN)  # 英文總數說法的張數子句（「, with 6 of 6 licenses valid」，2026-11-06）
if hasattr(ck, "VET_ONLY_CLAIM"):
    CLAIM.append(ck.VET_ONLY_CLAIM)  # 「唯一許可是獸用」（Dk）
START = re.compile(r",\s|;\s|\s(?:that|which|with|and|but|y|con|que|aunque|pero|e|dan|serta|kerana|memandangkan|og|men|med)\s|\s\(", re.I)
END = re.compile(r",\s|;\s|\s(?:but|and|aunque|pero|y|e|dan|men|og)\s|\.\s*$|$", re.I)


def _cuts(m):
    """人工清單的 cut：字串或字串清單（同一句要刪兩個片段時）"""
    c = m.get("cut")
    return [c] if isinstance(c, str) else list(c or [])


_LISTISH = re.compile(r"licen[cs]|authori[sz]|regist|\brecords?\b|\bvalid\b|\blisted\b|\bmarketed\b|\bproducts?\b|\bentr(y|ies)\b|evidence pack", re.I)
_GARBLE = re.compile(r"\b(the|a|an|of|for|with|to|from|in|are|is|was|were|list|lists|contains?|single-ingredient|show|shows|record|records)\s*[,.;]|\b(the|a|an|MHRA|UK) and\b", re.I)  # 刪掉中間片段後留下「Completion of the, including」「A verified MHRA and」
_VERIFY = re.compile(r"\b(verify|verified|check|checked|confirm|consult|refer)\b", re.I)


def _site_claim(site):
    rx = getattr(ck, "LIST_CLAIM", {}).get(site)
    return ([rx] + ([ck.LIST_PIPE] if hasattr(ck, "LIST_PIPE") else [])) if rx else []  # LIST_PIPE：「去抓許可資料／重跑擷取」（2026-11-06）


def list_cut_ok(cut, core=None):
    """處方／給付清單站（ck.LIST_CLAIM）的子句刪除：只接受刪掉句尾子句（留下的是原句開頭），留下的部分至少 4 個字、不以連接詞／冠詞收尾（「…, since only oral」）、
    沒有語法殘缺，而且不再講紀錄／許可（「Verify … with MHRA」這類下一步除外）；句中挖掉一段常留下「Both New Zealand, and …」，改整句刪"""
    if core is not None and not re.sub(r"^\W+", "", core).startswith(re.sub(r"^\W+", "", cut).rstrip(" .;:")):
        return False
    if len(re.findall(r"[A-Za-z]+", cut)) < 4 or _GARBLE.search(cut) or re.search(r"\b(since|as|because|given|although|while|with|and|or|but|only|the|a|an|of|that)\W*$", cut, re.I):
        return False
    return not _LISTISH.search(cut) or bool(_VERIFY.search(cut))


def clause_cut(site, lang, core, fc, rule):
    """只刪矛盾子句；回傳刪後的句子，做不到（子句就是整句、刪完仍矛盾、剩太短）回 None"""
    if lang == "ar":
        return clause_cut_ar(site, lang, core, fc, rule) if rule not in ("MANUAL", "DEPENDENT") else None
    if lang == "th":
        return clause_cut_th(site, lang, core, fc, rule) if rule not in ("MANUAL", "DEPENDENT") else None
    if lang in CUTX:
        return clause_cut_x(site, lang, core, fc, rule) if rule not in ("MANUAL", "DEPENDENT") else None
    if lang == "ko" and rule != "MANUAL":
        hits = [m for rx in (CLAIM + _site_claim(site)) + [ck.TW_LEFTOVER] for m in rx.finditer(core)]
        return clause_cut_ko(site, lang, core, fc, hits) if hits and rule != "DEPENDENT" else None
    if rule in ("M5", "MANUAL", "DEPENDENT"):
        return None
    hits = [m for rx in (CLAIM + _site_claim(site)) for m in rx.finditer(core)]
    if not hits:
        return None
    if lang == "ko":
        return clause_cut_ko(site, lang, core, fc, hits)
    m = min(hits, key=lambda x: x.start())
    st = [x for x in START.finditer(core[:m.start() + 1])]
    a = st[-1].start() if st else None
    if lang == "ms" and rule == "M3c":
        return None  # 馬來文的張數句（「Kesemua 29 pendaftaran berstatus sah dan …」）整句都是許可說法：整句刪
    if lang == "ms":  # 矛盾說法整個在括號裡：刪整個括號（「NPRA (memandangkan produk tidak berdaftar …, rujuk …)」）
        for g in re.finditer(r"\s*\(([^()]*)\)", core):
            if g.start() < m.start() < g.end():
                cand = (core[:g.start()] + core[g.end():]).strip()
                if len(re.findall(r"\w+", cand)) >= 4 and not ck.m3_verdict(site, lang, cand, fc):
                    return cand
                return None
    loose = a is None
    if lang == "ms":
        c2 = clause_cut_ms(site, lang, core, fc, m)
        if c2 or loose or re.match(r"\W*(Tambahan pula|Selain itu|Di samping itu|Walau bagaimanapun|Menurut|Berdasarkan|Mengikut)\b[^,]*$", core[:a]):
            return c2
    if a is None:
        a = m.start() - 1 if m.start() > 0 and core[m.start() - 1] == " " else None
    intro = a is not None and re.fullmatch(r"\W*(Además|Asimismo|Sin embargo|Por otra parte|Por otro lado|También|Also|However|Moreover|In addition|Furthermore)", core[:a], re.I)
    if a is None or (a < 12 and not intro):
        return None
    back = re.search(r",?\s*\b(dado|ya|puesto|debido a|por lo|lo|así|de modo|de manera|considerando)\s*$", core[:a], re.I)
    if back and core[a:a + 5].strip().lower().startswith("que"):
        a = back.start()  # 「…, dado que <矛盾>」：連接詞一起刪
        if a < 12:
            return None
    e = END.search(core, m.end())
    b = e.start()
    while True:  # 緊接著的下一個矛盾說法（「… tidak berdaftar di Malaysia dan tiada lesen tempatan」）一起刪
        nxt = [h for h in hits if b <= h.start() <= b + 6]
        if not nxt:
            break
        b = END.search(core, max(h.end() for h in nxt)).start()
    if loose and len(re.findall(r"\w+", core[b:])) < 2:
        return None  # 矛盾的是句末的受詞（「…registrerer nul tilladelser.」），刪掉只剩半句：整句刪
    sep = re.match(r",?\s+(y|and|dan|og|e)\s+", core[b:], re.I)
    if intro and not sep:
        return None  # 「Además, <矛盾>.」整句都是許可說法
    if sep and core[a:a + 2] == ", " and len(re.findall(r"\w+", core[b + sep.end():])) >= 3:
        cand = core[:a] + ", " + core[b + sep.end():]  # 「Además, <矛盾> y <其他>」→「Además, <其他>」：對等連接詞一起刪
    else:
        cand = core[:a] + core[b:]
    cand = re.sub(r"\s+([,.;])", r"\1", cand).replace(",,", ",").strip()
    cand = re.sub(r"[,;]+(?=[.!?]?\W*$)", "", cand)  # 刪到句末時，前面留下的逗號一併去掉（「Tiada ujian klinikal,.」）
    if not cand.endswith((".", "!", "?", ":", "。")) and core.rstrip().endswith("."):
        cand += "."
    if len(re.findall(r"\w+", cand)) < 3 or ck.m3_verdict(site, lang, cand, fc) or re.search(r"\(\s*\)", cand):
        return None
    body = re.sub(r"[\s.!?:;*_`)]+$", "", cand)
    cand = re.sub(r"\.\.$", ".", cand)
    if re.search(r"\b(dado|ya|puesto|debido a|por lo|lo|que|y|o|de|del|en|con|los|las|el|la|al|a|porque|pues|actualmente|también|además|se suman?|and|or|the|of|to|that|dan|og|men)$", body, re.I) \
            or re.search(r"\b(a|de|y|con|en|por|para|al|del)\s*,", cand, re.I) \
            or re.search(r"[:;,]\s*[,.;:]", cand) or re.search(r"\b(los|las|el|la|un|una|del|de|the|a)\s+(y|o|and|or)\b", cand, re.I) \
            or re.match(r"[\W\d]*[a-záéíóúñ]", cand):
        return None  # 刪完留下懸空的連接詞、標點連在一起或小寫開頭的殘句：整句刪
    if re.search(r"\.\s+[A-ZÁÉÍÓÚ]", core[a:b]) or re.search(r",\s*(y|o),|\w y que\b|^\W*\w+,\s+(por )?lo que\b", cand) \
            or re.search(r":\**\s+\S+(\s+\S+){0,2}[,;]", cand) or re.search(r":\**\s+[^.]{0,25}[;,]\s", cand):
        return None  # 刪掉的範圍跨過句點（S.A. 等縮寫造成）、留下「, y,」「X, lo que」「標籤:** 主語,」：整句刪
    if lang.startswith("en") and (re.search(r"\b(given|noting|since|although|because|while|whereas|with)\W*$", body, re.I)
                                  or re.search(r"\b(given|noting)\s+and\b", cand, re.I) or re.match(r"\s*,?\s*(are|is|were|was)\b", core[a:b], re.I)):
        return None  # 英文：刪完留下懸空的 given／noting、或只剩主詞（「Both licences, and …」）：整句刪
    if lang.startswith("en") and re.search(r"\b(the|a|an|of|for|to|with|and|or|regulatory|reasons?)\s*[,.;]", cand, re.I):
        return None  # 英文：刪掉中間片段後留下「Clarification of the, to confirm …」「Clarification of regulatory.」這類殘句（Us 2026-11-06）：整句刪
    if cand.count("(") != cand.count(")") or (lang == "ms" and re.match(r"\W*(Menurut|Berdasarkan|Mengikut)\b[^,]*[.]?\W*$", cand)):
        return None  # 括號不成對、或只剩「Menurut data …」這類引導語：整句刪
    return cand


# 2026-11-06 第二批 15 站的子句刪除：依該語言的對等／從屬連接詞切成子句，只拿掉跟事實矛盾的子句（或括號）。
#   tail：句中可整段拿掉的分隔（後面那段矛盾時，連分隔一起刪）；head：句首那段矛盾時，可連同其後分隔一起刪的對等連接
#   （刪後下一段要像獨立子句的開頭 subj，首字母改大寫）；lead：刪完句首留下的連接詞（中文「且」）一併拿掉
CUTX = {
    "de": dict(tail=r",\s+(?:und|sowie|aber|doch|jedoch|da|weil|wobei|sodass|so dass|zumal|während|denn)\s+|;\s+|,\s+(?=(?:die|der|das|alle|beide|sämtliche|seine|ihre|zudem|\d+)\s)|\s+(?=angesichts\s)",
               head=r",\s+(?:und|sowie|aber|doch)\s+|;\s+|,\s+", nosubj=r"^(dass|ob|wenn|weil|da|wie|warum|welche[rsn]?|der aktuellen)\b", consep=r",\s+(?:sodass|so dass|weshalb|was)\s+",
               subsep=r",\s+(?:da|weil|wobei|sodass|so dass|zumal|während|denn)\s+",
               subj=r"(?:(?:der|die|das|den|dem|des|ein|eine|einen|es|er|sie|man|zudem|außerdem|auch|weitere|mehrere|viele|einige|keine?|für|bei|in|zu)\b|[A-ZÄÖÜ0-9])",
               verb=r"\b(ist|sind|war|waren|wird|werden|wurde|wurden|hat|haben|hatte|gibt|gab|fehlt|fehlen|besteht|bestehen|liegt|liegen|kann|können|muss|müssen|"
                    r"soll|sollte|sollten|spricht|sprechen|erfordert|erfordern|bleibt|bleiben|zeigt|zeigen|stützt|stützen|deutet|deuten|betrifft|betreffen|"
                    r"existiert|existieren|enthält|enthalten|birgt|wiegt|erscheint|scheint|reicht|reichen|lässt|lassen|exprimiert|steht|stehen|gilt|gelten)\b"),
    "fi": dict(tail=r",\s+(?:ja|eikä|mutta|joten|koska|sillä|kun|vaikka|mikä|minkä)\s+|;\s+|,\s+|\s+ja\s+",
               head=r",\s+(?:ja|mutta)\s+|;\s+|,\s+|\s+ja\s+", subj=r"\w", subord=r"^\W*(Koska|Kun|Vaikka|Jos|Mikäli|Sillä|Että)\b", nosubj=r"^(että|jos|kun|koska|joka|jotka|mikä|miten|miksi|onko|ovatko|sekä)\b", consep=r",\s+(?:joten|mikä|minkä vuoksi)\s+", subsep=r",\s+(?:koska|sillä|kun|vaikka|mikä|minkä|joten)\s+",
               verb=r"\b(on|ovat|oli|olivat|ei|eivät|eikä|puuttu\w*|tuke\w*|viittaa\w*|edellyttä\w*|rajoitta\w*|vaati\w*|voi|voidaan|jää\w*|liitty\w*|"
                    r"perustu\w*|näyttää|osoitta\w*|tuo|tuovat|estää|estävät|sisältää|kuuluu|löytyy|nostaa|heikentää|lisää|liittää|liittävät|"
                    r"vaikeutta\w*|edistää|aiheutta\w*|kohdistu\w*|vastaa|vastaavat|pysyy|jatkuu|puoltaa|puoltavat|riittää|tarvitaan|on|olisi)\b"),
    "no": dict(tail=r",\s+(?:og|men|så|siden|fordi|ettersom|noe som|mens)\s+|;\s+|,\s+|\s+og\s+",
               head=r",\s+(?:og|men)\s+|;\s+|,\s+|\s+og\s+", subj=r"\w", subord=r"^\W*(Siden|Fordi|Ettersom|Når|Selv om|Hvis|Da|At|Om)\b", nosubj=r"^(om|at|hvis|når|som|hvorfor|hvordan|der|da|av)\b", consep=r",\s+(?:så|noe som)\s+", subsep=r",\s+(?:siden|fordi|ettersom|noe som|mens|så)\s+",
               verb=r"\b(er|var|har|hadde|mangler|finnes|fins|gir|viser|tyder|kan|må|bør|skal|vil|blir|ble|støtter|begrenser|krever|gjør|ligger|"
                    r"foreligger|svekker|peker|innebærer|øker|gjelder|omfatter|inneholder)\b"),
    "it": dict(tail=r",\s+(?:e|ma|mentre|poiché|perché|dato che|visto che|quindi|per cui|pertanto)\s+|;\s+|,\s+|\s+e\s+",
               head=r",\s+(?:e|ma)\s+|;\s+|,\s+|\s+e\s+", subj=r"\w", subord=r"^\W*(Poiché|Dato che|Visto che|Sebbene|Benché|Anche se|Se|Quando|Perché)\b",
               nosubj=r"^(che|se|quando|perché|poiché|dato|visto|come|cui|il quale|la quale|per cui|quindi|il che|e|ma|ne|non ne)\b", subsep=r",\s+(?:poiché|perché|dato che|visto che|per cui|pertanto|quindi)\s+",
               consep=r",\s+(?:per cui|quindi|pertanto|il che|sicché)\s+",
               verb=r"\b(è|sono|era|erano|ha|hanno|manca|mancano|resta|restano|rimane|rimangono|risulta|risultano|richiede|richiedono|limita|limitano|può|possono|"
                    r"deve|devono|esiste|esistono|c'è|ci sono|vi sono|vi è|rende|rendono|indica|indicano|mostra|mostrano|suggerisce|suggeriscono|sostiene|sostengono|"
                    r"presenta|presentano|riguarda|riguardano|aumenta|riduce|appare|appaiono|sembra|sembrano|costituisce|offre|supporta|supportano)\b"),
    "sv": dict(tail=r",\s+(?:och|men|eftersom|då|vilket|så att|medan)\s+|;\s+|,\s+(?=(?:det|de|den|alla|samtliga|båda|inget|ingen|dessutom|\d+)\s)|\s+och\s+(?=(?:det|de|den|alla|samtliga|båda|inget|ingen|produkt\w*|läkemedl\w*)\b)",
               head=r",\s+(?:och|men)\s+|;\s+|,\s+|\s+och\s+", subj=r"\w", subord=r"^\W*(Eftersom|Då|När|Om|Även om|Att)\b",
               nosubj=r"^(att|om|som|eftersom|när|vilket|vilka|då|och|(inget|ingen)( av dem)? (har|är))\b", subsep=r",\s+(?:eftersom|då|medan)\s+", consep=r",\s+(?:vilket|så att|så)\s+",
               verb=r"\b(är|var|har|hade|saknas|saknar|finns|fanns|kan|måste|bör|ska|skall|blir|blev|talar|visar|tyder|stöder|begränsar|kräver|gör|ligger|"
                    r"innebär|ökar|gäller|omfattar|innehåller|behöver|framgår|bygger|pekar|utgör|förefaller|verkar|minskar)\b"),
    "fr": dict(tail=r",\s+(?:et|mais|car|puisque|alors que|tandis que|ce qui|si bien que|donc)\s+|;\s+|,\s+(?=(?:l'|la\b|le\b|les\b|toutes\b|tous\b|son\b|ses\b|sa\b|aucune?\b|de plus\b|\d+))|\s+et\s+(?=(?:l'|la\b|le\b|les\b|toutes\b|son\b|ses\b|sa\b|aucune?\b))",
               head=r",\s+(?:et|mais)\s+|;\s+|,\s+|\s+et\s+", subj=r"\w", subord=r"^\W*(Puisque|Comme|Bien que|Alors que|Si|Quand|Lorsque|Étant donné)\b",
               nosubj=r"^(que|qui|si|puisque|car|dont|où|ce qui|et|mais|aucune n')", subsep=r",\s+(?:car|puisque|alors que|tandis que)\s+", consep=r",\s+(?:ce qui|si bien que|donc)\s+",
               verb=r"\b(est|sont|était|étaient|a|ont|avait|reste|restent|manque|manquent|limite|limitent|rend|rendent|existe|existent|peut|peuvent|doit|doivent|"
                    r"semble|semblent|apparaît|paraît|constitue|nécessite|nécessitent|repose|reposent|concerne|concernent|demeure|demeurent|justifie|pèse|pèsent|"
                    r"offre|soutient|suggère|indique|montre|s'agit|faut|fait|font|porte|portent|relève|n'est|n'ont|n'a|n'existe|n'y a|présente|présentent|"
                    r"comporte|comportent|expose|exposent|renforce|renforcent|complique|compliquent|bloque|bloquent|empêche|empêchent|freine|freinent|réduit|réduisent)\b"),
    "pt": dict(tail=r",\s+(?:e|mas|pois|porque|já que|dado que|uma vez que|enquanto|portanto|o que)\s+|;\s+|,\s+(?=(?:o|os|a|as|todos|todas|seu|seus|sua|nenhum|não|\d+)\b)|\s+e\s+(?=(?:o|os|a|as|todos|seu|seus|sua|não|nenhum)\b)",
               head=r",\s+(?:e|mas)\s+|;\s+|,\s+|\s+e\s+", subj=r"\w", subord=r"^\W*(Como|Embora|Já que|Dado que|Uma vez que|Se|Quando|Porque)\b",
               nosubj=r"^(que|se|quando|porque|pois|já que|o que|cujo|onde|e|mas)\b", subsep=r",\s+(?:pois|porque|já que|dado que|uma vez que)\s+", consep=r",\s+(?:o que|portanto)\s+",
               verb=r"\b(é|são|está|estão|era|eram|foi|foram|tem|têm|há|possui|possuem|falta|faltam|limita|limitam|torna|tornam|existe|existem|pode|podem|deve|devem|"
                    r"parece|parecem|constitui|necessita|exige|exigem|permanece|permanecem|depende|baseia|indica|indicam|mostra|mostram|sugere|apresenta|apresentam|"
                    r"impede|impedem|consta|constam|reforça|reforçam|dificulta|dificultam|agrava|agravam|aponta|apontam|refere|referem)\b"),
    "nl": dict(tail=r",\s+(?:en|maar|omdat|aangezien|want|terwijl|wat|waardoor|zodat)\s+|;\s+|,\s+(?=(?:de|het|alle|beide|zijn|haar|geen|\d+)\b)|\s+en\s+(?=(?:de|het|alle|beide|zijn|haar|geen)\b)",
               head=r",\s+(?:en|maar)\s+|;\s+|,\s+|\s+en\s+", subj=r"\w", subord=r"^\W*(Omdat|Aangezien|Hoewel|Als|Wanneer|Doordat)\b",
               nosubj=r"^(dat|of|als|wanneer|omdat|wat|waardoor|die|en|maar)\b", subsep=r",\s+(?:omdat|aangezien|want|terwijl)\s+", consep=r",\s+(?:wat|waardoor|zodat)\s+",
               verb=r"\b(is|zijn|was|waren|heeft|hebben|had|ontbreekt|ontbreken|blijft|blijven|kan|kunnen|moet|moeten|lijkt|lijken|vormt|vormen|beperkt|beperken|"
                    r"vereist|vereisen|maakt|maken|wijst|wijzen|bestaat|bestaan|biedt|bieden|ligt|liggen|past|passen|sluit|blokkeert|staat|staan|wordt|worden|gaat|"
                    r"geeft|geven|toont|tonen|suggereert|ondersteunt|bevat|bevatten|pleit|pleiten)\b"),
    "ja": dict(tail=r"(?!x)x", head=r"(?!x)x", subj=r"."),  # 日文只刪括號，其他整句刪（「、」後的子句刪了常留下連用形殘句）
    "zh": dict(tail=r"，(?:且|而且|並且|但|但是|然而|因此|所以|故|此外|另外|同時)?|；", head=r"，(?:且|而且|並且|但|但是|此外|另外|同時)?|；", subj=r".",
               lead=r"^(且|而且|並且|並|而|但|但是|此外|另外|同時|亦|也|因此|所以|故)"),
}


_BULLET = [False]  # 目前處理的句子是不是清單項目（清單項目常是沒有動詞的名詞片語，「Clarification du statut réglementaire, l'AMM étant annulée」）


def clause_cut_x(site, lang, core, fc, rule=None):
    """第二批站的子句刪除；做不到回 None（整句刪）"""
    P = CUTX.get(lang)
    if not P:
        return None

    def bad(x):
        return bool(ck.m3_verdict(site, lang, x, fc) or ck.tw_left(site, x))

    def ok(c):
        if bad(c) or c.count("(") != c.count(")") or c.count("„") > c.count("“") + c.count('"'):
            return False
        words = re.findall(r"\w+", c)
        if (len(words) < 3 and lang not in ("zh", "ja", "th")) or (lang in ("zh", "ja") and len(re.sub(r"\W", "", c)) < 6):
            return False
        if re.search(r"\(\s*\)|[,;:]\s*[.;:,]|\s[,.;]", c):
            return False
        return True

    mk = re.search(r"[*_`]+$", core.rstrip())  # 句末的強調記號（「…TFDA-tietoja.*」）：刪完補回
    trail = mk.group(0) if mk else ""
    core = core.rstrip()[:len(core.rstrip()) - len(trail)] if trail else core
    end = "." if core.rstrip().endswith(".") else ("。" if core.rstrip().endswith("。") else "")
    for g in re.finditer(r"\s*[（(]([^()（）]{2,200})[)）]", core):  # 括號裡的矛盾說法：只刪括號
        if bad(g.group(1)) and not bad(core[:g.start()] + core[g.end():]):
            cand = re.sub(r"\s+([,.;:])", r"\1", (core[:g.start()] + core[g.end():]).strip())
            return cand if ok(cand) else None
    if rule == "M5":
        return None  # 台灣模板殘留常夾在名詞片語裡（「…PDF TFDA-verkkosivustolta …」），只刪括號；其他整句刪或人工清單指定片段
    parts = re.split("(" + P["tail"] + ")", core)
    segs, seps = parts[0::2], parts[1::2]
    if len(segs) < 2:
        return None
    flags = [bad(x) for x in segs]
    if all(flags) or not any(flags):
        return None
    if P.get("consep"):  # 接在矛盾子句後面的結果子句（「…註銷, per cui …」「…, joten …」）依附被刪的前提，一起刪
        for i in range(1, len(segs)):
            if flags[i - 1] and re.fullmatch(P["consep"], seps[i - 1]):
                flags[i] = True
        if all(flags):
            return None
    if P.get("subsep"):  # 從屬子句（「…, siden X er avregistrert og Y」）被刪時，以無逗號連接詞接在後面的片段屬於同一個從屬子句，一起刪
        for i in range(1, len(segs)):
            if flags[i] and re.fullmatch(P["subsep"], seps[i - 1]):
                j = i + 1
                while j < len(segs) and not seps[j - 1].lstrip().startswith((",", ";")):
                    flags[j] = True
                    j += 1
    out = ""
    for i, sgm in enumerate(segs):
        if flags[i]:
            if i == 0:
                if not re.fullmatch(P["head"], seps[0]) or (P.get("subord") and re.match(P["subord"], sgm)):
                    return None  # 第一段是從屬子句（因為…、雖然…）：後面的主句依附它，整句刪
                continue
            continue
        if out == "" and i > 0:
            if not flags[0] or not re.match(P["subj"], sgm) or (P.get("verb") and not re.search(P["verb"], sgm)) \
                    or (lang in ("de", "nl", "sv", "no", "da") and P.get("verb") and re.match(P["verb"], sgm, re.I)) \
                    or (P.get("nosubj") and re.match(P["nosubj"], sgm)):
                return None  # 第一段刪掉後，下一段不像獨立子句的開頭（沒有主詞或沒有限定動詞）
            sgm = sgm[:1].upper() + sgm[1:]
        elif i > 0:
            out += seps[i - 1]
        out += sgm
    if not flags[0] and len(flags) > 1 and flags[1] and len(re.findall(r"\w+", segs[0])) <= 2:
        return None  # 留下的開頭只是引導詞（「Inoltre, … e …」「In Italia, inoltre, …」）：整句刪
    if P.get("verb"):
        for i in range(len(segs) - 1):
            bare_comma = re.fullmatch(r",\s+", seps[i]) or not re.search(r"[,;]", seps[i])  # 只有逗號、或沒有逗號的連接詞（列舉）
            bare_conj = not re.search(r"[,;]", seps[i])
            cont = i + 2 < len(segs) and not flags[i + 2]  # 被刪片段後面句子還有接續
            if not flags[i] and flags[i + 1] and bare_comma and not re.search(P["verb"], segs[i], re.I) and (not _BULLET[0] or cont):
                return None  # 留下的片段（逗號前）沒有動詞，被刪的是它的述語（「Dos 5 registros brasileiros, todos os 5 estão válidos」「No ciclo atual de análise, o modelo …」）
            if flags[i] and not flags[i + 1] and i == 0 and bare_conj and not re.search(P["verb"], segs[i], re.I):
                return None  # 被刪的是並列主詞的一部分（「A ausência de registros … e a falta do DrugBank ID impedem …」）
    for i in range(1, len(segs) - 1):  # 刪掉的子句後面以無逗號連接詞接著「動詞開頭」的片段：兩者共用主詞（「il farmaco non è più in commercio e presenta …」），整句刪
        if flags[i] and not flags[i + 1] and not re.search(r"[,;]", seps[i]) and P.get("verb") and re.match(P["verb"], segs[i + 1], re.I):
            return None
    via_sub = any(flags[i] and P.get("subsep") and re.fullmatch(P["subsep"], seps[i - 1]) for i in range(1, len(segs)))
    enum_cut = any(flags[i] and not re.search(r"[;]|,\s+\w+\s", seps[i - 1] + " x") for i in range(1, len(segs)))  # 以逗號或無逗號連接詞（列舉）接著的片段被刪
    if P.get("verb") and enum_cut and re.search(P["verb"], core, re.I) and not re.search(P["verb"], out, re.I) and not via_sub:
        return None  # 原句的動詞在被刪的片段裡（「La resistenza…, l'esistenza… e l'autorizzazione annullata rendono…」）：整句刪
    out = re.sub(r"[,;:\s–]+$", "", out.rstrip(". "))
    if P.get("lead"):
        out = re.sub(P["lead"], "", out)
    cand = (out + end if end and not out.endswith(end) else out) + trail
    if trail and trail.count("*") % 2 == 1 and cand.count("*") % 2 == 1 and not cand.lstrip("> -").startswith("*"):
        return None
    return cand if ok(cand) else None


AR_CONSEQ = re.compile(r"^(وهذا|وهو ما|وهو أمر|وهو (قيد|عائق|عامل)|مما|ما\s|فهذا|فت|وبالتالي|لذا|لذلك|ولذلك|وذلك|فلا|فقد|فأي|فإن)")  # 接在被刪子句後的結果／說明子句
AR_NOTMKT = re.compile(r"(لا|ولا|غير)[^،.]{0,25}(مسو[ّ]?ق|تسويق)|غير متوفر في السوق|غير متاح في السوق")
AR_REREG = re.compile(r"إعادة (ال)?تسجيل|إعادة (ال)?ترخيص|تسجيل جديد|ترخيص جديد")  # 以「已註銷」為前提的「重新註冊」說法
AR_WFUNC = re.compile(r"^و(?=(ال|لا\b|لم\b|لن\b|قد\b|هو\b|هي\b|هذا\b|هذه\b|هناك\b|كما\b|ليس|لكن|إن\b|أن\b|له\b|لها\b|لديه\b|لديها\b))|^(مع|بينما|في حين أن|في حين) (?=\w)")
AR_LEADIN = re.compile(r"^(إضافة إلى ذلك|بالإضافة إلى ذلك|علاوة على ذلك|كذلك|كما|أيضاً|أيضًا|أيضا|من جهة أخرى|في المقابل)$")


def clause_cut_ar(site, lang, core, fc, rule=None):
    """阿拉伯文（SATxGNN）：以「،」切子句；刪矛盾子句與依附它的結果子句；做不到回 None（整句刪）"""
    def bad(x):
        return bool(ck.m3_verdict(site, lang, x, fc) or ck.tw_left(site, x))

    def ok(c):
        if bad(c) or c.count("(") != c.count(")"):
            return False
        if len(re.findall(r"\w+", c)) < 3 or AR_LEADIN.match(c.strip(" .")):
            return False
        return not re.search(r"\(\s*\)|[،,;:]\s*[.;:،,]|\s[،,.;]", c)

    mk = re.search(r"[*_`]+$" if not core.lstrip().startswith("(") else r"[*_`]*\)$", core.rstrip())  # 整句包在括號裡（「(عُرضت … ملغى أيضًا.)」）：右括號當句尾記號
    trail = mk.group(0) if mk else ""
    body = core.rstrip()[:len(core.rstrip()) - len(trail)] if trail else core.rstrip()
    end = "." if body.endswith(".") else ""
    body = body[:-1] if end else body
    for g in re.finditer(r"\s*[（(]([^()（）]{2,200})[)）]", body):
        if bad(g.group(1)) and not bad(body[:g.start()] + body[g.end():]):
            cand = (body[:g.start()] + body[g.end():]).strip() + end + trail
            return cand if ok(cand) and not AR_REREG.search(cand) else None
    if rule == "M5":
        return None
    segs = re.split(r"\s*،\s*", body)
    if len(segs) < 2:
        return None
    flags = [bad(x) for x in segs]
    for i in range(1, len(segs)):
        if flags[i - 1] and (AR_CONSEQ.match(segs[i]) or AR_NOTMKT.search(segs[i])):
            flags[i] = True
    if any(flags):
        for i in range(len(segs)):
            if AR_REREG.search(segs[i]):
                flags[i] = True
    if all(flags) or not any(flags):
        return None
    for i in range(len(segs) - 1):
        if not flags[i] and flags[i + 1] and AR_LEADIN.match(segs[i].strip()):
            return None  # 「في المقابل، [被刪]، و…」：引導詞後面接的子句被刪，整句刪
    kept = [x for x, f in zip(segs, flags) if not f]
    if flags[0]:
        kept[0] = AR_WFUNC.sub("", kept[0])
    out = "، ".join(kept).strip()
    cand = out + (end if not out.endswith(".") else "") + trail
    if trail and cand.count("*") % 2 == 1:
        return None
    return cand if ok(cand) else None


TH_SPLIT = re.compile(r"\s+(?=(?:และ|จึง|เพราะ|เนื่องจาก|ทำให้|แต่|อีกทั้ง|นอกจากนี้|ซึ่ง|ขณะที่|ดังนั้น|ปัจจุบันจึง|โดย|รวมถึง|ส่วน)|[(（])|\s+(?=\S)")
TH_CONSEQ = re.compile(r"^(จึง|ทำให้|ดังนั้น|ปัจจุบันจึง|ซึ่ง)")
TH_REREG = re.compile(r"ขึ้นทะเบียนใหม่|ยื่นทะเบียน\S*ใหม่|ทะเบียนตำรับยาใหม่|ขอทะเบียนใหม่")  # 以「已註銷」為前提的「重新註冊」
TH_CONN_ONLY = re.compile(r"^(นอกจากนี้|และ|อีกทั้ง|ประกอบกับ|ทั้ง|แต่|รวมถึง)$")
TH_LEAD = re.compile(r"^(และ|อีกทั้ง|แต่|ขณะที่|โดย)\s*")


def clause_cut_th(site, lang, core, fc, rule=None):
    """泰文（ThTxGNN）：以空白切語段（泰文以空白分子句），刪矛盾語段與依附它的結果語段；做不到回 None（整句刪）"""
    def bad(x):
        return bool(ck.m3_verdict(site, lang, x, fc) or ck.tw_left(site, x))

    def ok(c):
        if bad(c) or c.count("(") != c.count(")") or c.count("**") % 2:
            return False
        return len(re.sub(r"\W", "", c)) >= 8
    body = core.rstrip()
    for g in re.finditer(r"\s*[（(]([^()（）]{2,200})[)）]", body):
        if bad(g.group(1)) and not bad(body[:g.start()] + body[g.end():]):
            cand = (body[:g.start()] + body[g.end():]).strip()
            return cand if ok(cand) else None
    if rule == "M5":
        return None
    segs = re.split(r"\s+", body)
    if len(segs) < 2:
        return None
    # 合併：一個矛盾說法常橫跨幾個語段（「ทะเบียนนี้ **ถูกยกเลิกแล้ว**」）；逐段往後延伸到不再是「延伸後才矛盾」為止
    flags = [False] * len(segs)
    i = 0
    while i < len(segs):
        for j in range(i, min(i + 4, len(segs))):
            if bad(" ".join(segs[i:j + 1])) and not any(bad(" ".join(segs[i + 1:k + 1])) for k in range(i + 1, j + 1)) \
                    and (i == 0 or not bad(" ".join(segs[i - 1:j + 1])) or True):
                for k in range(i, j + 1):
                    flags[k] = True
                break
        i += 1
    for i in range(1, len(segs)):
        if flags[i - 1] and not flags[i] and TH_CONSEQ.match(segs[i]):
            j = i
            while j < len(segs) and not (j > i and re.match(r"^(และ|แต่|อีกทั้ง|นอกจากนี้)", segs[j])):
                flags[j] = True
                j += 1
    if any(flags):
        for i in range(len(segs)):
            if TH_REREG.search(segs[i]):
                flags[i] = True
        for i in range(len(segs) - 1):
            if not flags[i] and flags[i + 1] and TH_CONN_ONLY.match(segs[i]):
                flags[i] = True  # 只剩連接詞（「นอกจากนี้ [被刪]」）
    if all(flags) or not any(flags):
        return None
    kept = [x for x, f in zip(segs, flags) if not f]
    if flags[0]:
        kept[0] = TH_LEAD.sub("", kept[0])
    out = " ".join(x for x in kept if x).strip()
    out = re.sub(r"(:\s*)(?:และ|อีกทั้ง)\s*", r"\1", out)
    out = re.sub(r"\s+(และ|แต่|อีกทั้ง)$", "", out)
    return out if ok(out) else None


KO_TOPIC = re.compile(r"(?<=[가-힣A-Za-z0-9\)\]])(은|는|에는|에서는) ")
KO_CONN = re.compile(r"^[^,.;]{0,8}?((으며|이며|며|고|어|아|여|으나|나|지만|는데|이고|로),\s|(고|며|어) (?=\S))")


def clause_cut_ko(site, lang, core, fc, hits):
    """韓文：矛盾的是以連接語尾（-며／-고／-어／-로…）加逗號結尾的前置子句時，刪掉該子句（主題語「X는」保留）；
    子句在句末（整句就是許可證說法）或刪後仍矛盾、留下台灣字樣時回 None（整句刪）"""
    m = min(hits, key=lambda x: x.start())
    tail = KO_CONN.match(core[max(m.end(), max(h.end() for h in hits if h.start() < m.end() + 12)):])
    if not tail:
        return None
    end = max(m.end(), max(h.end() for h in hits if h.start() < m.end() + 12)) + tail.end()
    tops = [t for t in KO_TOPIC.finditer(core[:m.start()])]
    a = tops[-1].end() if tops else 0
    if "," in core[a:m.start()]:
        a = core.rindex(",", a, m.start()) + 2
    rest = core[end:]
    if re.search(r"이 중|그중|그 중|이 가운데|그 가운데", rest):
        return None  # 留下的子句指涉被刪掉的張數（「이 중 2건은…」），整句刪
    if a and re.search(r"(허가증?|허가 ?건수|품목|제품|등록)(은|는) $", core[:a]):
        a = core[:a].rfind(", ") + 2 if ", " in core[:a] else 0  # 後半句有自己的主題語：前面的主題語一起刪（「허가증은 위 표는…」）
    cand = (core[:a] + core[end:]).strip()
    if len(cand) < 15 or ck.m3_verdict(site, lang, cand, fc) or ck.tw_left(site, cand) or re.search(r"\(\s*\)", cand):
        return None
    return cand


PAREN = re.compile(r"\s*[（(]([^()（）|]{2,80})[)）]")


def paren_cut(site, lang, row, fc):
    """表格儲存格裡的括號附註跟事實矛盾（「확인 불가 (허가 이력 없음)」「(대만 허가 이력 없음)」）：只刪該括號，儲存格其他文字保留。
    回傳 (新列, 規則, 依據)；括號以外還有矛盾、或刪後儲存格變空時回 None"""
    if lang not in ("ko", "da", "ms") or any(x in row for x in ck.MARKET_LABELS.get(site, ())):
        return None  # 概覽表狀態／張數列由程式產生，不在這裡動
    out, why = row, None
    for m in list(PAREN.finditer(row))[::-1]:
        inner = m.group(1)
        h = ck.m3_verdict(site, lang, inner, fc)
        tw = ck.tw_left(site, inner)
        if h or tw:
            cell_l = out.rfind("|", 0, m.start()); cell_r = out.find("|", m.end())
            rest = out[cell_l + 1:m.start()] + out[m.end():cell_r if cell_r >= 0 else len(out)]
            if not rest.strip():
                return None
            out = out[:m.start()] + out[m.end():]
            why = (h[0] if h else "M5") + "（括號）", (h[1] if h else "TwTxGNN 模板殘留的台灣許可說法") + f"；只刪括號，保留：{out.strip()}"
    if not why or ck.tw_left(site, out):
        return None
    return out, why[0], why[1]


def clause_cut_ms(site, lang, core, fc, m):
    """馬來文：矛盾說法是句子的主要述語（「Ubat ini juga tidak berdaftar di Malaysia, dan graf …」），前面只有短主語、
    後面是「, dan」帶出的獨立子句時，刪掉「主語＋矛盾子句＋, dan」，留下的子句首字母改大寫；其他情形整句刪（回 None）"""
    pre = core[:m.start()]
    intro = re.match(r"\W*(Tambahan pula|Selain itu|Di samping itu|Walau bagaimanapun),\s+", pre)
    lead = intro.group(0) if intro else ""
    pre = pre[len(lead):]
    if len(re.findall(r"\w+", pre)) > 5 or re.search(r"[,;:(]", pre):
        return None
    e = re.compile(r",?\s+dan\s+").search(core, m.end())
    if not e or re.search(r"[.;,]", core[m.end():e.start()]):
        return None
    rest = core[e.end():].strip()
    if len(re.findall(r"\w+", rest)) < 3:
        return None
    if re.match(r"\d", rest) or rest.count("(") != rest.count(")"):
        return None
    if re.match(r"(me|ber|di|ter)\w+\b", rest) and not pre.strip():
        return None  # 沒有主語、後半句只是動詞片語（「Mengandungi bahan tunggal.」）
    if re.match(r"(me|ber|di|ter)\w+\b", rest):
        cand = lead + pre + rest  # 「Ubat ini juga tidak didaftarkan … dan mempunyai …」→「Ubat ini juga mempunyai …」
    else:
        cand = lead + rest if lead else rest[:1].upper() + rest[1:]
    if ck.m3_verdict(site, lang, cand, fc) or ck.tw_left(site, cand):
        return None
    return cand


_SS = {}


def site_status(site, lic):
    """證據包紀錄以外的許可證號：用站上 license_adapter 讀 Release 的原始狀態檔（valid／not_marketed／cancelled；查不到回 None）"""
    if site not in _SS:
        _SS[site] = {}
        ap = BASE / site / "scripts/license_adapter.py"
        if ap.exists():
            try:
                sp = importlib.util.spec_from_file_location("ad_" + site, ap); ad = importlib.util.module_from_spec(sp); sp.loader.exec_module(ad)
                raw = json.loads((BASE / site / "data" / ad.RAW_FILE).read_text(encoding="utf-8"))
                for k, v in ad.status_index(raw).items():
                    cls = v[1] if isinstance(v, (list, tuple)) and len(v) > 1 else getattr(ad, "CLASS", {}).get(str(v).strip().lower())
                    if cls:
                        _SS[site][mv_norm(k)] = cls
            except Exception:  # noqa: BLE001 — 沒有可用的狀態檔就不查
                _SS[site] = {}
    return _SS[site].get(mv_norm(lic))


def mv_norm(x):
    return re.sub(r"[\s\-]", "", str(x)).upper()


def split_sentences(line, lang=None):
    t = line
    for a, b in ABBR:
        t = t.replace(a, b)
    for a in ABBR_X.get(lang or "", []):
        t = re.sub(r"(?<![\w.])" + re.escape(a), a.replace(".", "‧"), t)
    parts = re.split(r"(?<=[。！？])(\s*)", t) if lang in ("ja", "zh") else re.split(r"(?<=[.!?。！？])(\s+)", t)  # 中日文句號後沒有空白
    out = []
    for i in range(0, len(parts), 2):
        s = parts[i]
        for a, b in ABBR:
            s = s.replace(b, a)
        s = s.replace("‧", ".")
        out.append((s, parts[i + 1] if i + 1 < len(parts) else ""))
    return out


def process(site, lang, page, fc, manual):
    raw = page.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw[:500]
    t = raw.replace("\r\n", "\n")
    if "layout: id_redirect" in t[:3000] or 'http-equiv="refresh"' in t[:3000]:
        return None, []
    fm_end = t.index("\n---", 4) + 4 if t.startswith("---") else 0
    lines = t.split("\n")
    start = t[:fm_end].count("\n") + 1
    log = []
    man = manual.get(page.stem, [])
    dep = DEPENDENT.get("en" if lang == "en-us" else lang)
    in_managed = False
    tdel = set()
    # front matter 的 description 是從摘要表「原適應症」格組出來的：該格的矛盾括號附註刪了，description 裡同一段也刪（只刪不改寫）
    for i in range(1, start):
        if lines[i].startswith("description:") and fc and lang in ("ko", "da", "ms"):
            d = lines[i]
            ms_ = list(PAREN.finditer(d)) + list(re.finditer(r"\s*[（(]([^()（）|]{2,80})(?=…\"?\s*$)", d))  # 後者：description 被截斷、括號沒收尾
            for m in sorted(ms_, key=lambda x: x.start())[::-1]:
                if ck.m3_verdict(site, lang, m.group(1), fc) or ck.tw_left(site, m.group(1)):
                    d = d[:m.start()] + d[m.end():]
            if d != lines[i]:
                log.append((page.stem, "description（括號）", lines[i].strip(), "摘要表原適應症格的矛盾括號附註一併刪"))
                lines[i] = d
    for i in range(start, len(lines)):
        l = lines[i]
        if re.search(r"<!-- (review:begin \S+|brand-names:start) -->", l):
            in_managed = True
        if re.search(r"<!-- (review:end \S+|brand-names:end) -->", l):
            in_managed = False
            continue
        if l.startswith("#"):
            hc = next((m for m in man if isinstance(m.get("cut"), str) and m["sentence"] in l and m["cut"] in l), None)
            if hc and not in_managed:  # 標題裡的矛盾片段：只刪人工核對過的片段
                log.append((page.stem, "MANUAL（標題）", l.strip(), hc["reason"] + f"；刪除片段：{hc['cut']}"))
                lines[i] = l.replace(hc["cut"], "", 1)
                if hc.get("capitalize"):  # 刪掉的是標題開頭的字：留下的標題首字母大寫（人工核對過）
                    mm = re.search(r"[^\W\d_]", lines[i].lstrip("#"))
                    if mm:
                        k = len(lines[i]) - len(lines[i].lstrip("#")) + mm.start()
                        lines[i] = lines[i][:k] + lines[i][k].upper() + lines[i][k + 1:]
            continue
        if in_managed or not l.strip() or l.startswith(("{:", "<", "---")):
            continue
        if l.startswith("|"):
            crow = next((m for m in man if isinstance(m.get("cut"), str) and m["sentence"] in l and m["cut"] in l), None)
            if crow:  # 表格列裡只刪指定片段（人工核對過）
                log.append((page.stem, "MANUAL（儲存格）", l.strip(), crow["reason"] + f"；刪除片段：{crow['cut']}"))
                lines[i] = l.replace(crow["cut"], "", 1)
                continue
            mrow = next((m for m in man if not m.get("keep") and not m.get("cut") and m["sentence"] in l), None)
            if mrow:
                log.append((page.stem, "MANUAL", l.strip(), mrow["reason"]))
                lines[i] = None
                tdel.add(i)
                continue
            idn = re.match(r"^\|\s*([0-9][\w./-]*)\s*\((cancelad[oa]s?|vencid[oa]|vigente)\)\s*\|", l, re.I) if fc else None
            if idn:  # 許可證號格裡的狀態註記跟事實不符（CO「20019826 (cancelado)」，2026-10-03 reviewer 誤判）：只刪註記
                now = {mv_norm(k): v for k, v in (fc.get("licenses") or {}).items()}.get(mv_norm(idn.group(1))) or site_status(site, idn.group(1))
                said = "valid" if idn.group(2).lower() == "vigente" else "cancelled"
                if now and (now == "cancelled") != (said == "cancelled"):
                    nl = l[:idn.start(1)] + idn.group(1) + " " + l[idn.end(2) + 1:].lstrip()
                    nl = re.sub(r"^(\|\s*\S+)\s+\|", r"\1 |", nl)
                    log.append((page.stem, "M1（許可證號註記）", l.strip(), f"事實：{idn.group(1)} 是 {now}，刪掉「({idn.group(2)})」"))
                    lines[i] = nl
                    continue
            pc = paren_cut(site, lang, l, fc) if fc else None
            if pc:
                log.append((page.stem, pc[1], l.strip(), pc[2]))
                lines[i] = pc[0]
                continue
            if ck.tw_left(site, l) and not re.fullmatch(r"[\s|:\-]+", l):
                log.append((page.stem, "M5", l.strip(), "TwTxGNN 模板殘留的台灣上市狀態列／taiwan_regulatory 欄位，與本站無關"))
                lines[i] = None
                tdel.add(i)
            continue
        sents = split_sentences(l, lang)
        keep, changed, prev_del = [], False, False
        for s, sp in sents:
            core = re.sub(r"^\s*([-*>]\s*|\d+\.\s+)+", "", s.strip())
            why = None
            cutm = next((m for m in man if m.get("cut") and m["sentence"] in s and all(c in s for c in _cuts(m))), None)
            if cutm:
                log.append((page.stem, "MANUAL（子句）", s.strip(), cutm["reason"] + f"；刪除片段：{' ／ '.join(_cuts(cutm))}"))
                ns = s
                for c in _cuts(cutm):
                    ns = ns.replace(c, "", 1)
                if cutm.get("capitalize"):  # 刪掉的是句首子句：留下的句子首字母大寫（人工核對過）
                    mm = re.search(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]", ns)
                    ns = ns[:mm.start()] + ns[mm.start()].upper() + ns[mm.start() + 1:] if mm else ns
                keep.append((ns, sp)); changed = True; prev_del = False
                continue
            if any(m.get("keep") and m["sentence"] in s for m in man):
                keep.append((s, sp)); prev_del = False
                continue
            for m in man:
                if not m.get("keep") and m["sentence"] in s:
                    why = ("MANUAL", m["reason"])
            if not why and fc and re.search(r"\w{3}", core):
                h = ck.m3_verdict(site, lang, core, fc)
                if h:
                    why = (h[0], h[1].split("，正文")[0].split("：")[0])
            if not why and ck.tw_left(site, core):
                why = ("M5", "TwTxGNN 模板殘留的台灣許可說法，與本站無關")
            if not why and prev_del and dep and dep.search(core) and (lang == "ko" or re.match(r"\W*(Den siger|Listen er)", core) or re.search(ck._LIC + r"|market|comerciali|시판|허가|dipasarkan|lesen|pendaftaran|berdaftar|markedsfør|regist", core, re.I)):  # 韓文的指代開頭（이 중／나머지는…）本身就指張數
                why = ("DEPENDENT", "緊接在被刪句後、以指代詞開頭；前句刪除後失去指涉對象（不改寫，一併刪除）")
            if why:
                _BULLET[0] = bool(re.match(r"^\s*([-*]|\d+\.)\s", s))
                lead = s[:len(s) - len(s.lstrip())] + re.match(r"^\s*(([-*>]\s*|\d+\.\s+)*)", s.strip()).group(1)
                cut = clause_cut(site, lang, core, fc, why[0]) if fc else None
                if cut and site in getattr(ck, "LIST_CLAIM", {}) and not list_cut_ok(cut, core):
                    cut = None  # 處方／給付清單站：留下的半句仍在講紀錄／許可、或太短，整句刪（2026-11-06）
                if cut:
                    log.append((page.stem, why[0] + "（子句）", s.strip(), why[1] + f"；只刪子句，保留：{cut}"))
                    keep.append((lead + cut, sp)); changed = True; prev_del = False
                    continue
                log.append((page.stem, why[0], s.strip(), why[1]))
                changed = prev_del = True
                continue
            prev_del = False
            keep.append((s, sp))
        if changed:
            new = "".join(s + sp for s, sp in keep).rstrip()
            bullet = re.match(r"^(\s*[-*]\s+|\s*\d+\.\s+|>\s*)", l)
            if not re.sub(r"^\s*([-*]|\d+\.|>)\s*", "", new).strip(" *_>"):
                new = None
            elif bullet and not new.startswith(bullet.group(1)):
                new = bullet.group(1) + new.lstrip(" -*>")
            lines[i] = new
    # 刪過列的表格若只剩表頭（＋分隔列）就整張拿掉
    k = start
    while k < len(lines):
        if lines[k] is not None and lines[k].startswith("|"):
            j = k
            while j < len(lines) and (lines[j] is None or lines[j].startswith("|")):
                j += 1
            rest = [x for x in lines[k:j] if x is not None]
            if tdel & set(range(k, j)) and len(rest) <= 2 and (len(rest) < 2 or re.fullmatch(r"[\s|:\-]+", rest[-1])):
                for x in range(k, j):
                    lines[x] = None
            k = j
        else:
            k += 1
    out = [x for x in lines if x is not None]
    if not log:
        return None, log
    t2 = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    if t2 == t:
        return None, log
    return (t2.replace("\n", "\r\n") if crlf else t2), log


def main(argv):
    site = next(a for a in argv if a.endswith("TxGNN"))
    lang = ck.LANG.get(site, "en")
    dry = "--dry-run" in argv
    logf = argv[argv.index("--log") + 1] if "--log" in argv else None
    only = set(argv[argv.index("--pages") + 1].split(",")) if "--pages" in argv else None
    facts = json.loads((BASE / ".claude/cache/license_facts" / f"{site}.json").read_text(encoding="utf-8"))
    mf = BASE / site / "scripts/license_sentence_fixes.json"
    manual = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else {}
    all_log, n = [], 0
    for page in sorted((BASE / site / "docs/_drugs").glob("*.md")):
        if only and page.stem not in only:
            continue
        fc = facts.get(page.stem) or facts.get(page.stem.replace("-", "_")) or facts.get(page.stem.replace("_", "-"))
        new, log = process(site, lang, page, fc, manual)
        all_log += log
        if new is not None:
            n += 1
            if not dry:
                page.write_bytes(new.encode("utf-8"))
    if logf:
        Path(logf).write_text("頁\t規則\t原句\t依據\n" + "\n".join("\t".join(x) for x in all_log) + "\n", encoding="utf-8")
    print(f"{site}：改頁 {n}；刪句 {len(all_log)}")


if __name__ == "__main__":
    main(sys.argv[1:])
