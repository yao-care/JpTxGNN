"""已知用途的子型／上位詞過濾（2026-10-17，N-01）。

KnownRelationsChecker 只排除名稱完全相同的已知適應症；這裡再排除兩種「其實是已知用途」的預測：
  1. 在 TxGNN 知識圖譜疾病階層（disease_disease 邊，.claude/cache/disease_hierarchy.json）中與已知適應症直接相連
  2. 名稱與已知適應症互相包含（例：dermatitis ⊂ atopic dermatitis、myeloid leukemia ⊂ acute myeloid leukemia）
已知適應症＝該站 data/external/drug_disease_relations.csv 的 indication 與 off-label use，
再加上該國許可證適應症（N-04，2026-10-17）：證據包裡許可證紀錄的 indication 欄，
英文直接用；非英文用該站 src/*/mapping/disease_mapper.py 的 DISEASE_DICT 轉成英文病名。
第二輪（同日）：許可證適應症改為 30 站依 DrugBank ID 合併（.claude/cache/license_terms_by_db.json，
`python3 .claude/known_use_filter.py --build-license-cache` 重建），並加上 CATEGORIES 疾病類別規則。
"""
import csv, json, re
from functools import lru_cache
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def _n(s):
    s = re.sub(r"\((disease|disorder)\)", "", (s or "").lower())
    s = s.replace("leukaemia", "leukemia").replace("tumour", "tumor").replace("oesophag", "esophag").replace("haem", "hem")
    return re.sub(r"\s+", " ", s).strip()


@lru_cache(maxsize=1)
def _graph():
    d = json.loads((BASE / ".claude/cache/disease_hierarchy.json").read_text())
    by_name, nb = {}, {}
    for i, n in d["names"].items():
        by_name.setdefault(_n(n), set()).add(i)
    for a, b in d["edges"]:
        nb.setdefault(a, set()).add(b)
        nb.setdefault(b, set()).add(a)
    return by_name, nb


@lru_cache(maxsize=64)
def _known(rel_path: str):
    k, ci = {}, {}
    p = Path(rel_path)
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["relation"] in ("indication", "off-label use") and "susceptibility" not in r["y_name"].lower():  # 第七輪：susceptibility 不是適應症
                    k.setdefault(r["x_id"], set()).add(_n(r["y_name"]))
                    k.setdefault(r["x_name"].lower(), set()).add(_n(r["y_name"]))
                elif r["relation"] == "contraindication":
                    ci.setdefault(r["x_id"], set()).add(_n(r["y_name"]))
                    ci.setdefault(r["x_name"].lower(), set()).add(_n(r["y_name"]))
    # 第四輪：KG 同時記成 indication 與 contraindication 的（loperamide↔dysentery）矛盾，不當已知用途
    #（第五輪：有許可證佐證者在 filter_predictions 加回，見 conflicts()）
    return {x: v - ci.get(x, set()) for x, v in k.items()}, {x: v & ci.get(x, set()) for x, v in k.items()}


@lru_cache(maxsize=1)
def _kg_exclude():
    f = BASE / ".claude/known_use_kg_exclude.json"
    d = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    out = {}
    for k, v in d.items():
        if k.startswith("_"):
            continue
        names = {_n(x) for x in v.get("names", [])}
        out[k] = names
        if v.get("drug"):
            out[v["drug"].lower()] = names  # known_set 也會用藥名查
    return out


def known_set(proj: Path, drug_key: str):
    return (_known(str(proj / "data/external/drug_disease_relations.csv"))[0].get(drug_key) or set()) - _kg_exclude().get(drug_key, set())


def conflicts(proj: Path, drug_key: str):
    return _known(str(proj / "data/external/drug_disease_relations.csv"))[1].get(drug_key) or set()


# 名稱包含但其實是不同疾病（2026-10-17：例如 pulmonary hypertension 不是 hypertension 的子型）
DISTINCT = [
    (r"\bhypertension\b", r"\b(pulmonary|portal|intracranial|ocular|intraocular)\b"),
    (r"\bhypotension\b", r"\b(intracranial)\b"),
    (r"\bdiabetes\b", r"\binsipidus\b"),
]


def _distinct(pred: str, known: str) -> bool:
    longer, shorter = (pred, known) if len(pred) >= len(known) else (known, pred)
    return any(re.search(a, shorter) and re.search(b, longer) and not re.search(b, shorter) for a, b in DISTINCT)


# 泛稱：名稱包含它不代表是同一種病（lamivudine 的 hepatitis B ≠ hepatitis C；atenolol 的 heart disease ≠ 肺心症）
BROAD = {"hepatitis", "leukemia", "lymphoma", "dermatitis", "carcinoma", "cancer", "sarcoma", "tumor", "neoplasm", "infection",
         "arthritis", "anemia", "nephritis", "conjunctivitis", "keratitis", "bronchitis", "pneumonia", "eczema", "neuropathy",
         "nephropathy", "myopathy", "cardiomyopathy", "heart disease", "lung disease", "liver disease", "kidney disease",
         "skin disease", "eye disease", "bone disease", "pain", "edema", "ulcer", "fever", "inflammation", "allergy",
         "hypersensitivity", "insufficiency", "failure", "deficiency", "syndrome", "disease", "disorder",
         "thrombosis", "thrombocytopenia", "vaginitis", "vulvovaginitis", "keratoconjunctivitis", "hypertrichosis",
         "sinusitis", "alopecia", "lymphedema"}

_STOP = {"disease", "diseases", "disorder", "syndrome", "type", "with", "and", "the", "due", "of", "to", "susceptibility", "chronic", "acute"}


def _content(s: str) -> set:
    return {w for w in re.findall(r"[a-z]{4,}", s) if w not in _STOP}


def _within(a: str, b: str) -> bool:
    """a 以完整詞出現在 b 裡（dermatitis 不算在 acrodermatitis 裡）。"""
    return re.search(r"(?<![a-z])" + re.escape(a) + r"(?![a-z])", b) is not None


def is_known_variant(pred: str, known: set) -> bool:
    p = _n(pred)
    if not p or not known:
        return False
    if p in known:
        return True
    for k in known:
        # 第四輪（2026-10-20）：只有泛稱（BROAD：hepatitis、leukemia、dermatitis、heart disease…）不拿來比「預測名包含已知名」；
        # 第三輪對所有單字一律不比，把 goiter、endometriosis、rickets、plague 這類具體病名的子型也放回了
        if len(k) > 4 and len(p) > 4 and ((_within(k, p) and k not in BROAD) or _within(p, k)):
            if _distinct(p, k):
                continue
            return True
    # 第八輪（pm 第 8 點）：已知病名是單一長詞時，預測名的詞以它結尾也算變體（laryngopharyngitis ⊃ pharyngitis）
    for k in known:
        if " " not in k and len(k) >= 8 and k not in BROAD and any(w != k and w.endswith(k) for w in p.split()):
            return True
    # 疾病階層（直接相連＝子型或上位詞）：第三輪起要求兩者共用一個實詞，擋掉 acne↔dermatitis、bronchitis↔COPD 這種鄰接
    by_name, nb = _graph()
    ids = by_name.get(p, set())
    for k in known:
        shared = _content(p) & _content(k)  # 還要共用一個實詞（擋掉 inflammatory bowel disease ↔ crohn disease 這種上位詞）
        if shared and len(k.split()) >= 2 and any(nb.get(i, set()) & by_name.get(k, set()) for i in ids):
            return True
    return False


@lru_cache(maxsize=64)
def _disease_dict(proj_str: str) -> tuple:
    import ast
    for f in Path(proj_str).glob("src/*/mapping/disease_mapper.py"):
        t = f.read_text(encoding="utf-8")
        m = re.search(r"DISEASE_DICT\s*(?::[^=]*)?=\s*\{", t)
        if not m:
            continue
        depth, i = 0, m.end() - 1
        for j in range(i, len(t)):
            depth += t[j] == "{"
            depth -= t[j] == "}"
            if depth == 0:
                try:
                    d = ast.literal_eval(t[i:j + 1])
                    return tuple(sorted(((k.lower(), _n(v)) for k, v in d.items() if isinstance(v, str)), key=lambda x: -len(x[0])))
                except Exception:
                    break
    return ()


GENERIC = {"cancer", "tumour", "tumor", "infection", "infections", "bleeding", "pain", "disease", "diseases", "disorder",
           "inflammation", "fever", "neoplasms", "carcinoma", "headache", "allergy", "poisoning", "anemia", "anaemia"}


# 第四輪：這兩站證據包的 indication 欄不是適應症（br＝ANVISA 藥理分類「ANTIDIABETICOS」、co＝INVIMA 成分名）
NOT_INDICATION = {"BrTxGNN", "COTxGNN"}
_NEG = re.compile(r"should not|must not|not be used|not indicated|not recommended|contraindicat|do not use|no debe|nicht angewendet", re.I)


def _single_records(bundle) -> list:
    """許可證紀錄，只取單方（複方的適應症不能算到每個成分頭上：lidocaine 複方軟膏的 tinea corporis）。"""
    out = []
    dr = (bundle or {}).get("drug") or {}
    # 英文成分欄要含該藥名的第一個詞（Tw 舊證據包用全文比對，把 Keytruda 掛在 enfortumab vedotin 底下）
    stem = next((w for w in re.findall(r"[a-z]{5,}", str(dr.get("inn") or dr.get("name") or "").lower())), "")
    for v in (bundle or {}).values():
        if isinstance(v, dict) and isinstance(v.get("records"), list):
            for r in v["records"]:
                if not isinstance(r, dict):
                    continue
                ing = str(r.get("ingredients") or r.get("主成分略述") or "")
                ings = [i for i in ing.split(";;") if i.strip()]
                if r.get("kind") == "combo" or len(ings) > 1 or str(r.get("active_ingredient") or "").count("[") > 1:
                    continue
                if stem and re.fullmatch(r"[A-Za-z0-9 ,.()\-]+", ing) and stem[:5] not in ing.lower():
                    continue
                out.append(r)
    return out


def _clean_indication(r) -> str:
    """適應症文字去掉網址與否定句（「should not be used in hemophilia」不是適應症）。"""
    t = str(r.get("indication") or "")
    if t.startswith("http"):
        # Kr：MFDS 효능효과 PDF 網址 → 用 .claude/kr_mfds_ee_20261023.py 轉好的文字（2026-10-23）
        m = re.match(r"https://nedrug\.mfds\.go\.kr/pbp/cmn/pdfDownload/(\d+)/EE", t)
        c = BASE / ".claude/cache/kr_mfds_ee" / f"{m.group(1)}.txt" if m else None
        if not (c and c.exists()):
            return ""
        t = c.read_text(encoding="utf-8")
    return " ".join(s for s in re.split(r"(?<=[.;。])\s+|\n", t) if not _NEG.search(s))


def license_terms(proj: Path, bundle: dict) -> set:
    """N-04：該國許可證適應症 → 英文病名集合。"""
    texts = [_clean_indication(r) for r in _single_records(bundle)] if proj.name not in NOT_INDICATION else []
    out = set()
    dd = _disease_dict(str(proj))
    for t in texts:
        out |= {"cat:" + c for c in _cats(t)}  # 第二輪：整段許可證文字（含 EMA 長句）直接比對疾病類別
        if re.fullmatch(r"[A-Za-z0-9 ,.;:'()/\-\n]+", t or ""):
            # 英文（含 EMA 的 MeSH 詞）：只用分號／換行拆；「Dermatitis, Atopic」轉成「atopic dermatitis」
            for p in re.split(r"[;\n]", t):
                p = p.strip().strip(".")
                m = re.fullmatch(r"([^,]+), ([A-Za-z\- ]+)", p)
                if m:
                    p = f"{m.group(2)} {m.group(1)}"
                p = _n(p)
                if len(p) >= 6 and p not in GENERIC:
                    out.add(p)
        else:
            low = (t or "").lower()
            for k, en in dd:
                if k and k in low and len(en) >= 6 and en not in GENERIC:
                    out.add(en)
    return out


# 2026-10-17（N-01 第二輪）：同一疾病類別的子型視為已知用途。只列明確的臨床類別，
# 不用「同一個上位詞」這種寬鬆規則（lung cancer 與 breast cancer 不是同一類）。
CATEGORIES = [
    ("epilepsy", r"epilep|seizure|status epilepticus|てんかん|癲癇|癫痫|痙攣発作"),
    ("glaucoma", r"glaucoma|ocular hypertension|intraocular pressure|緑内障|青光眼|高眼壓|高眼圧|hydrophthalm|buphthalm"),
    ("migraine", r"migraine|صداع نصفي|الصداع النصفي|片頭痛|偏頭痛"),
    ("peptic ulcer", r"(peptic|gastric|duodenal|gastrojejunal|stomach) ulcer|ulcer of (stomach|duodenum)|peptic ulcer|胃潰瘍|十二指腸潰瘍|消化性潰瘍|胃腸潰瘍"),
    ("breast cancer", r"breast (cancer|carcinoma|adenocarcinoma|neoplasm|tumou?r)|carcinoma of (the )?breast|乳癌|乳がん"),
    ("gastric cancer", r"(gastric|stomach) (cancer|carcinoma|adenocarcinoma|neoplasm)|carcinoma of (the )?stomach|gastric (cardia|tubular|signet)|胃癌|胃がん"),
    ("cll", r"chronic lymphocytic leukemia|small lymphocytic lymphoma|慢性リンパ性白血病|慢性淋巴性白血病"),
    ("dermatophytosis", r"tinea|dermatophyt|ringworm|白癬|癬|majocchi"),
    ("skin fungal infection", r"tinea|dermatophyt|cutaneous candidiasis|superficial mycosis|(skin|cutaneous|superficial) fungal|fungal (skin|infection of (the )?skin)|白癬|皮膚真菌|皮膚糸状菌|黴菌|癬"),
    ("tuberculosis", r"tubercul|結核"),
    ("copd", r"chronic obstructive pulmonary|copd|chronic obstructive lung|慢性閉塞性肺疾患|慢性阻塞性肺"),
    ("asthma", r"asthma|喘息|氣喘|哮喘"),
    ("psoriasis", r"psoria|乾癬"),
    ("rheumatoid arthritis", r"rheumatoid arthritis|関節リウマチ|類風濕"),
    ("hypertension", r"^(essential |primary |secondary |malignant |renovascular |resistant )*hypertension|hypertensive (disorder|disease)|本態性高血圧|^高血圧|^高血壓|高血圧症"),
    ("diabetes mellitus", r"diabetes mellitus|type [12] diabetes|糖尿病"),
    ("heart failure", r"heart failure|cardiac failure|心不全|心衰竭|心臟衰竭"),
    ("schizophrenia", r"schizophren|統合失調症|精神分裂"),
    ("depression", r"depressi(on|ve disorder)|melanchol|dysthym|うつ病|憂鬱症|抑鬱"),
    ("preeclampsia", r"eclampsia|子癇"),
    ("gonorrhea", r"gonorrh|gonococcal|淋病"),
    ("glioma", r"astrocyt|glioma|glioblastoma|oligodendrogli|ependymoma|神経膠腫|膠質瘤"),
    ("urothelial cancer", r"urothelial|bladder (cancer|carcinoma)|尿路上皮"),
    ("als", r"amyotrophic lateral sclerosis|筋萎縮性側索硬化"),
    ("mds", r"myelodysplastic|骨髄異形成|deletion of the long arm of chromosome 5|del\(5q\)|5q[- ]?(deletion|syndrome)"),
    ("otitis media", r"otitis media|中耳炎"),
    ("gastritis", r"gastritis|gastroduodenitis|胃炎"),
    ("hypoparathyroidism", r"hypoparathyroid|dahlberg-borer-newcomer|副甲状腺機能低下|副甲狀腺功能低下"),
    ("spondyloarthritis", r"spondyloarthr|ankylosing spondylitis|inflammatory spondylopathy|axial spondyloarthritis|強直性脊椎炎|脊椎関節"),
    ("stroke", r"\bstroke\b|cerebral infarction|cerebrovascular accident|ischemic cerebrovascular|脳梗塞|腦梗塞|腦中風|脳卒中"),
    ("rhinitis", r"rhinitis|鼻炎"),
    ("parkinson", r"parkinson|パーキンソン|巴金森|帕金森"),
    ("gout", r"\bgout|痛風"),
    ("osteoporosis", r"osteoporo|骨粗鬆症|骨質疏鬆"),
    ("hiv", r"\bhiv\b|human immunodeficiency virus|(?<!feline )\baids\b|(?<!feline )acquired immunodeficiency"),
    ("hepatitis b", r"hepatitis b|b型肝炎|b型慢性肝炎"),
    ("hepatitis c", r"hepatitis c|c型肝炎|c型慢性肝炎"),
    ("influenza", r"influenza|インフルエンザ|流感|流行性感冒"),
    ("multiple myeloma", r"multiple myeloma|plasma cell myeloma|多発性骨髄腫|多發性骨髓瘤"),
    ("prostate cancer", r"prostat\w* (cancer|carcinoma|adenocarcinoma|neoplasm)|前立腺癌|前立腺がん|攝護腺癌|前列腺癌"),
    ("ovarian cancer", r"ovar\w* (cancer|carcinoma|adenocarcinoma|neoplasm)|卵巣癌|卵巣がん|卵巢癌"),
    ("colorectal cancer", r"(colorectal|colon|rectal) (cancer|carcinoma|adenocarcinoma|neoplasm)|大腸癌|結腸癌|直腸癌|結腸・直腸癌"),
    ("lung cancer", r"(lung|pulmonary) (cancer|carcinoma|adenocarcinoma|neoplasm)|lung \w+ carcinoma|non-small cell lung|small cell lung|肺癌|肺がん"),
    ("aml", r"acute myeloid leukemia|acute myelogenous leukemia|急性骨髄性白血病|急性骨髓性白血病"),
    ("all", r"acute lymphoblastic leukemia|acute lymphocytic leukemia|急性リンパ性白血病|急性淋巴性白血病"),
    ("melanoma", r"melanoma|黒色腫|黑色素瘤"),
    ("angina", r"angina|狭心症|狹心症|心絞痛"),
    ("urticaria", r"urticaria|蕁麻疹|じんましん|荨麻疹"),
    ("insomnia", r"insomnia|initiating and maintaining sleep|不眠症|失眠|불면"),
    ("hypercholesterolemia", r"hypercholesterol|hyperlipoproteinemia|hyperlipidemia|dyslipidemia|高コレステロール血症|高膽固醇血症|脂質異常症"),
    ("urinary tract infection", r"urinary tract infection|尿路感染"),
    ("cml", r"chronic myel\w* leukemia|慢性骨髄性白血病|慢性骨髓性白血病"),
]
_CAT = [(c, re.compile(r, re.I)) for c, r in CATEGORIES]


_COMPLICATION = re.compile(r"perforat|hemorrha|bleed|obstruct|associated|cataract|retinopath|neuropath|nephropath|穿孔|出血")


def _cats(name: str) -> set:
    n = _n(name)
    if _COMPLICATION.search(n):
        return set()  # 併發症（peptic ulcer perforation）不等於已知用途本身
    if re.search(r"polyposis", n):
        return set()  # 遺傳性息肉症候群（GAPPS）不是癌症本身（第六輪）
    return {c for c, r in _CAT if r.search(n)}


@lru_cache(maxsize=1)
def _global_license():
    """N-04 第二輪：30 站許可證適應症依 DrugBank ID 合併（任一國核准即算已知用途）。快取由 build_license_cache() 產生。"""
    f = BASE / ".claude/cache/license_terms_by_db.json"
    out = {k: set(v) for k, v in json.loads(f.read_text()).items()} if f.exists() else {}
    # 人工補充（.claude/known_use_extra.json）：資料源沒收錄、但有官方仿單可查的核准適應症，每筆附出處
    x = BASE / ".claude/known_use_extra.json"
    for db, v in (json.loads(x.read_text()) if x.exists() else {}).items():
        out.setdefault(db, set()).update(x if x.startswith("cat:") else _n(x) for x in v["terms"])  # 與其他已知用途同樣正規化（IgE 大寫對不上）
    return out


def build_license_cache():
    out = {}
    for proj in sorted(BASE.glob("*TxGNN")):
        for b in proj.glob("data/bundles/*/drug_bundle.json"):
            try:
                bd = json.loads(b.read_text(encoding="utf-8"))
            except Exception:
                continue
            db = (bd.get("drug") or {}).get("drugbank_id")
            if db:
                out.setdefault(db, set()).update(license_terms(proj, bd))
                for v in bd.values():  # 第三輪：英文許可證長句，另存成 text: 供片語比對
                    if isinstance(v, dict) and isinstance(v.get("records"), list):
                        for r in (_single_records({"x": v, "drug": bd.get("drug")}) if proj.name not in NOT_INDICATION else []):
                            s = _n(_clean_indication(r))
                            if len(s) > 40 and re.search(r"[a-z]{4,} [a-z]{4,}", s) and not s.startswith("http"):
                                out[db].add("text:" + s[:3000])
    # 日本 PMDA 原始資料（JpTxGNN 證據包的 indication 欄是空的，改讀 jp_fda_drugs.json 的「効能・効果」）
    jp = BASE / "JpTxGNN"
    try:
        raw = json.loads((jp / "data/raw/jp_fda_drugs.json").read_text(encoding="utf-8"))
        with open(jp / "data/processed/drug_mapping.csv", encoding="utf-8-sig") as f:
            mp = {r["承認番号"]: r.get("drugbank_id") for r in csv.DictReader(f)}
        for d in raw:
            db = mp.get(str(d.get("承認番号")))
            if db:
                out.setdefault(db, set()).update(license_terms(jp, {"pmda": {"records": [{"indication": d.get("効能・効果", "")}]}}))
    except FileNotFoundError:
        pass
    (BASE / ".claude/cache/license_terms_by_db.json").write_text(
        json.dumps({k: sorted(v) for k, v in sorted(out.items()) if v}, ensure_ascii=False, indent=0))
    return out


def filter_predictions(proj: Path, drugbank_id: str, inn: str, names: list, bundle: dict = None) -> list:
    lic = license_terms(proj, bundle) | _global_license().get(drugbank_id or "", set())
    known = known_set(proj, drugbank_id) | known_set(proj, (inn or "").lower()) | lic
    # 第五輪：KG 矛盾關係（indication＋contraindication）若有許可證／仿單佐證，仍算已知用途
    lic_plain = {x for x in lic if not x.startswith(("cat:", "text:"))}
    lic_cats = {x[4:] for x in lic if x.startswith("cat:")} | set().union(*(_cats(x) for x in lic_plain)) if lic else set()
    for c in conflicts(proj, drugbank_id) | conflicts(proj, (inn or "").lower()):
        if c in lic_plain or is_known_variant(c, lic_plain) or (_cats(c) & lic_cats):
            known.add(c)
    texts = [k[5:] for k in known if k.startswith("text:")]
    # 第五輪：複合病名（therapy related AML and MDS）不觸發類別，否則只核准 AML 的藥也會排掉 MDS
    kc = set().union(*(({k[4:]} if k.startswith("cat:") else (set() if " and " in k else _cats(k))) for k in known if not k.startswith("text:"))) if known else set()
    kc |= set().union(*(_cats(x) for x in texts)) if texts else set()
    known = {k for k in known if not k.startswith(("cat:", "text:"))}
    def in_text(n):  # 預測名（至少兩個字）整句出現在許可證長句裡：myeloid leukemia ⊂ "acute myeloid leukaemia"
        p = _n(n)
        return len(p.split()) >= 2 and any(_within(p, x) for x in texts)
    return [n for n in names if not is_known_variant(n, known) and not (_cats(n) & kc) and not in_text(n)]


if __name__ == "__main__":
    import sys
    if "--build-license-cache" in sys.argv:
        print(len(build_license_cache()), "個 DrugBank ID")


SCORE_MIN = 0.99  # 2026-10-22：30 站統一門檻（th 等站證據包收了 0.5 以上的候選，網站寫的是只列 ≥0.99）


def kept_predictions(proj: Path, bundle: dict) -> list:
    """證據包 → 頁面該列的預測：分數 ≥0.99 的前 10 名，再排除已知用途。各環節（reviewer、sync、監測欄位、重生名單）共用。"""
    d = (bundle or {}).get("drug") or {}
    def sc(p):
        # 2026-10-23（pm）：沒有 DL 分數（txgnn_score）就不算預測，不再退回 kg_score
        v = p.get("txgnn_score")
        return v if v is not None else 0
    names = [p.get("disease_name", "").strip() for p in (d.get("predicted_indications") or [])
             if p.get("disease_name") and sc(p) >= SCORE_MIN][:10]
    # pm 第 9 點：susceptibility 是遺傳易感性，不是能用藥治療的病，不當預測顯示（主預測順延）
    names = [n for n in names if "susceptibility" not in n.lower()]
    if not names:
        return []
    inn = (d.get("inn") or d.get("name") or "").strip()
    dbid = d.get("drugbank_id") or _dl_dbid(proj).get(inn.lower(), "")  # My 證據包多數沒有 drugbank_id／inn，查不到 KG 已知用途（streptokinase 心肌梗塞漏判）
    return filter_predictions(proj, dbid, inn, names, bundle)


_DLID = {}


def _dl_dbid(proj: Path) -> dict:
    """該站 DL 預測檔的 藥名(小寫) → DrugBank ID，給缺 ID 的證據包補查已知用途。"""
    key = str(proj)
    if key not in _DLID:
        import csv, gzip
        m = {}
        p = Path(proj) / "data/processed/txgnn_dl_predictions.csv.gz"
        if p.exists():
            with gzip.open(p, "rt", encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
                    m.setdefault((r.get("drug_name") or "").lower(), r.get("drugbank_id") or "")
        _DLID[key] = m
    return _DLID[key]
