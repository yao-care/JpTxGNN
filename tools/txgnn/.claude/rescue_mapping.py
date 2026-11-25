#!/usr/bin/env python3
"""補救 drug_mapping.csv 裡失敗的成分（2026-10-12 盤點 E 項，見 .claude/AUDIT_20261011.md 環節 1）。

只動 mapping_success != True 的列，成功的列一律不碰；規則都是確定性的，且只接受「唯一命中」：
  1. 去重音、轉大寫、去劑量字樣（10 MG、5%）
  2. 括號內外各試一次（NORTRIPTYLINE (NORTRIPTYLINE HYDROCHLORIDE)）
  3. 去多語鹽類／水合物／介詞（CLORHIDRATO、BÉSILATE D'、FUMARATE DIHYDRATE、NATRIUM…）
  4. 酸類語序（ÁCIDO X-ICO / ACIDE X-IQUE / ACIDUM X-ICUM → X-IC ACID）
  5. 語尾規則（-O/-A、-INA→-INE、-OLO→-OLE、-ID→-IDE、-IN→-INE、-UM/-INUM、-E…）與 K→C、F→PH 拼字
  6. 長字（≥8）容許 1 個字元差，仍須唯一
  7. 複方（; , + / " Y " " ET " " UND "）拆開逐一比對，命中的成分各自成一列（同 license_id）
改過的列 mapping_source = "rescue_20261012:<規則>"。原檔備份為 drug_mapping.csv.bak_20261012（已存在就不覆蓋）。

用法: python3 .claude/rescue_mapping.py [--apply] [--sample N] [<ProjDir> ...]   （預設空跑、30 站）
"""
import sys as _sys, pathlib as _pl; _sys.path.insert(0, str(_pl.Path(__file__).resolve().parent)); import site_registry as _site_registry  # noqa: E402  # 30 站名單（不含 CnTxGNN）
import csv
import os
import re
import shutil
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

csv.field_size_limit(10**9)
BASE = Path("/Users/lightman/yao.care/TxGNN")
TAG = "rescue_20261012"

# 詞表：預設讀 ESTxGNN 的共用 drugbank_vocab.csv（母目錄批次用）；各站 tools/txgnn 複本由站上程式在 import 前設
# RESCUE_MAPPING_VOCAB 指向本站 data/external/drugbank_vocab.csv（2026-11-25 第七輪，取代 AR、SE 的站上複本）
VOCAB_FILE = Path(os.environ.get("RESCUE_MAPPING_VOCAB") or BASE / "ESTxGNN/data/external/drugbank_vocab.csv")
vocab = {}
for r in csv.DictReader(open(VOCAB_FILE, encoding="utf-8")):
    vocab[r["drug_name_upper"]] = r["drugbank_id"]
# 常見 INN／BAN 異名 → DrugBank 名稱（目標都已確認在 vocab）
ALIASES = {"PARACETAMOL": "ACETAMINOPHEN", "ADRENALINE": "EPINEPHRINE", "NORADRENALINE": "NOREPINEPHRINE",
           "LIGNOCAINE": "LIDOCAINE", "FRUSEMIDE": "FUROSEMIDE", "GLYCERYL TRINITRATE": "NITROGLYCERIN",
           "COLECALCIFEROL": "CHOLECALCIFEROL", "ALBUTEROL": "SALBUTAMOL", "ACIDUM ACETYLSALICYLICUM": "ACETYLSALICYLIC ACID",
           "ASPIRIN": "ACETYLSALICYLIC ACID", "CICLOSPORIN": "CYCLOSPORINE", "CICLOSPORINE": "CYCLOSPORINE",
           "OESTRADIOL": "ESTRADIOL", "ETHINYLOESTRADIOL": "ETHINYLESTRADIOL", "DIMETICONE": "SIMETHICONE",
           "LEVOTHYROXINE SODIUM": "LEVOTHYROXINE", "BENZYLPENICILLIN": "BENZYLPENICILLIN"}
for k, v in list(ALIASES.items()):
    if v in vocab:
        vocab.setdefault(k, vocab[v])
by_len_prefix = defaultdict(list)
for v in vocab:
    if len(v) >= 8 and " " not in v:
        by_len_prefix[(v[:3], len(v))].append(v)

SALTS = set("""
HYDROCHLORIDE HCL CHLORHYDRATE CLORHIDRATO HIDROCLORURO CLORIDRATO CLORIDRATO HYDROCHLORID HYDROKLORID HYDROCHLORIDUM
HYDROCHLORIDI DIHYDROCHLORIDE DICLORHIDRATO DICHLORHYDRATE HYDROBROMIDE BROMHIDRATO BROMHYDRATE HYDROBROMID
SODIUM SODICO SODICA SODIQUE SODICO NATRIUM NATRII NATRIUMSALT SODIO DISODIUM DISODICO DISODIQUE
POTASSIUM POTASICO POTASICA POTASSIQUE KALIUM KALII POTASSIO DIPOTASSIUM
CALCIUM CALCICO CALCICA CALCIQUE CALCII CALCIO MAGNESIUM MAGNESICO MAGNESIQUE MAGNESII MAGNESIO
ZINC ZINCO ZINKI MALEATE MALEATO MALEAS MALEAAT FUMARATE FUMARATO FUMARAS FUMARAAT HEMIFUMARATE HEMIFUMARATO
SULFATE SULFATO SULFAS SULPHATE SULFAAT SULFAT MESYLATE MESILATO MESILAS MESILATE MESYLAAT METHANESULFONATE
BESYLATE BESILATO BESILATE BESILAS BESYLAAT BESILAT TARTRATE TARTRATO TARTRAS BITARTRATE CITRATE CITRATO CITRAS
ACETATE ACETATO ACETAS ACETAAT PHOSPHATE FOSFATO PHOSPHAS FOSFAAT FOSFAT SUCCINATE SUCCINATO SUCCINAS
BROMIDE BROMURO BROMIDUM BROMID CHLORIDE CLORURO CHLORIDUM KLORID NITRATE NITRATO NITRAS OXALATE OXALATO
DIHYDRATE DIHIDRATO DIHYDRAS DIHYDRAAT DIHYDRAT MONOHYDRATE MONOHIDRATO MONOHYDRAS MONOHYDRAT HEMIHYDRATE
HEMIHIDRATO TRIHYDRATE TRIHIDRATO SESQUIHYDRATE HYDRATE HIDRATO HYDRAS HYDRAT ANHYDROUS ANHIDRO ANHYDRE ANHYDRICUM
ERBUMINE ERBUMINA TROMETHAMINE TROMETAMOL TROMETAMINA MEDOXOMIL MEDOXOMILO CILEXETIL CILEXETILO PROXETIL AXETIL
DIPROPIONATE DIPROPIONATO PROPIONATE PROPIONATO FUROATE FUROATO VALERATE VALERATO DECANOATE DECANOATO DECANOAS
PALMITATE PALMITATO PALMITAT ENANTATE ENANTATO LACTATE LACTATO GLUCONATE GLUCONATO HYCLATE HICLATO
MICRONISED MICRONIZED MICRONIZADO BASE EQ EQUIVALENT TO AS
ARGININE ARGININA LYSINE LISINA MEGLUMINE MEGLUMINA TERT BUTYLAMINE TERBUTILAMINA DIETHYLAMINE DIETILAMONIO DIETILAMINA
CAMSYLATE CAMSILATO EMBONATE EMBONATO PAMOATE PAMOATO HEMITARTRATE HEMITARTRATO BISULFATE BISULFATO BITARTRATO
ISETHIONATE ISETIONATO DIISETIONAS TOSYLATE TOSILATO MALATE MALATO NAPSYLATE XINAFOATE XINAFOATO CARBONATE CARBONATO
OLAMINE OLAMINA HYCLAS STEARATE ESTEARATO ESTOLATE ESTOLATO ETHYLSUCCINATE ETILSUCCINATO DIACETATE AMMONIUM AMONIO
DE DI DU DES D DEL LA LE DER VON
""".split())
FORM_WORDS = set("MG MCG G ML UI IU MG/ML % TABLET TABLETS CAPSULE CAPSULES".split())
# 劑型／描述詞：單字或末字規則命中後，剩下的字必須全是鹽類或這些詞才接受
DESCRIPTORS = set("""COATED GRANULES GRANULOS MICROGRANULOS EQUIVALENTE EQUIVALENTES EQUIV EQUV A AL DIRECT COMPRESION
DIRECTA POUR PREPARATIONS HOMEOPATHIQUES CRYSTALLISED CRISTALIZADO POWDER POLVO SOLUTION SOLUCION LIPOSOMAL PEGYLATED
CONCENTRATE CONCENTRADO PURIFIED PURIFICADO DRIED SECO EXTENDED RELEASE SR XR CR MR ORAL TOPICAL INJ INJECTION
SOLUBLE MICRONIZADA ANHIDRA HEMIHIDRATADA MONOHIDRATADA DIHIDRATADA TRIHIDRATADA EN POR DOSIS DOSE FORM""".split())
ACID_WORDS = {"ACID", "ACIDO", "ACIDE", "ACIDUM", "ACIDI", "ACIDO,", "AC", "SAURE", "SYRE", "ZUUR", "HAPPO"}

SUFFIX_RULES = [  # (regex on single token, replacement)
    (r"OLO$", "OLE"), (r"OLA$", "OLE"), (r"INA$", "INE"), (r"INO$", "INE"), (r"ATO$", "ATE"), (r"ICO$", "IC"),
    (r"ONA$", "ONE"), (r"IDA$", "IDE"), (r"IDO$", "IDE"), (r"ILO$", "IL"), (r"ANO$", "AN"), (r"ENO$", "ENE"),
    (r"O$", ""), (r"A$", ""), (r"E$", ""), (r"ID$", "IDE"), (r"IN$", "INE"), (r"ON$", "ONE"), (r"AT$", "ATE"),
    (r"OL$", "OLE"), (r"INUM$", "INE"), (r"OLUM$", "OL"), (r"ICUM$", "IC"), (r"UM$", ""), (r"UM$", "E"),
    (r"US$", ""), (r"I$", ""), (r"IS$", ""), (r"ONUM$", "ONE"), (r"IDUM$", "IDE"), (r"ATUM$", "ATE"),
    (r"YL$", "YL"), (r"INE$", "IN"),
]
SPELL_RULES = [("K", "C"), ("F", "PH"), ("Y", "I"), ("I", "Y"), ("CC", "C"), ("C", "CC"), ("TH", "T"), ("T", "TH")]


def deaccent(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).upper()


GLUED = sorted([w for w in SALTS if len(w) >= 5], key=len, reverse=True)


def unglue(tok: str) -> list[str]:
    for w in GLUED:
        if tok.endswith(w) and len(tok) - len(w) >= 5:
            return [tok[: -len(w)], w]
    return [tok]


def clean_tokens(s: str) -> list[str]:
    s = re.sub(r"\b\d+([.,]\d+)?\s*(MG|MCG|G|ML|%|UI|IU)\b", " ", s)
    toks = [t for t in re.split(r"[\s\-'’]+", s) if t]
    out = [t.strip(".,") for t in toks if t.strip(".,") and not re.fullmatch(r"[\d.,/%]+", t) and t not in FORM_WORDS]
    return [u for t in out for u in (unglue(t) if t not in vocab else [t])]


def hit(name: str):
    return vocab.get(name)


def one_edit(a: str):
    """長字容許 1 個字元差（替換／增刪），唯一才回傳。"""
    if len(a) < 8:
        return None
    cands = set()
    for L in (len(a) - 1, len(a), len(a) + 1):
        for v in by_len_prefix.get((a[:3], L), []):
            if _dist1(a, v):
                cands.add(v)
    return cands.pop() if len(cands) == 1 else None


def _dist1(a: str, b: str) -> bool:
    if a == b:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if abs(len(a) - len(b)) != 1:
        return False
    s, l = (a, b) if len(a) < len(b) else (b, a)
    i = 0
    while i < len(s) and s[i] == l[i]:
        i += 1
    return s[i:] == l[i + 1:]


ORTHO = [("HIDRO", "HYDRO"), ("CLORO", "CHLORO"), ("CLOR", "CHLOR"), ("TIAZ", "THIAZ"), ("FENO", "PHENO"),
         ("FEN", "PHEN"), ("METIL", "METHYL"), ("ETIL", "ETHYL"), ("TROMB", "THROMB"), ("TEOF", "THEOPH"),
         ("CEFTRIAXONA", "CEFTRIAXONE"), ("KLOR", "CHLOR"), ("KARB", "CARB"), ("KALC", "CALC"), ("SULFAMETOX", "SULFAMETHOX")]


def ortho(t: str) -> str:
    for a, b in ORTHO:
        t = t.replace(a, b)
    return t


def token_variants(t: str):
    seen = [t]
    o = ortho(t)
    if o != t:
        seen.append(o)
        for rx, rep in SUFFIX_RULES:
            v = re.sub(rx, rep, o)
            if v != o and len(v) >= 4 and v not in seen:
                seen.append(v)
    for rx, rep in SUFFIX_RULES:
        v = re.sub(rx, rep, t)
        if v != t and len(v) >= 4 and v not in seen:
            seen.append(v)
    for v in list(seen):
        for a, b in SPELL_RULES:
            w = v.replace(a, b)
            if w != v and w not in seen:
                seen.append(w)
    return seen


def window_match(core: list[str]):
    """最長連續片語優先；命中後剩下的字必須全是鹽類／描述詞／與命中重複，否則放棄（避免 DIGOXIN IMMUNE FAB → DIGOXIN）。"""
    n = len(core)
    for size in range(min(n, 4), 0, -1):
        for i in range(0, n - size + 1):
            win = core[i:i + size]
            if size == 1 and len(win[0]) < 6:
                continue
            for cand in _window_variants(win):
                if not hit(cand):
                    continue
                cand_toks = set(cand.split()) | set(win)
                rest = core[:i] + core[i + size:]
                if all(len(t) == 1 or t in SALTS or t in DESCRIPTORS or t in cand_toks or any(t.startswith(w[:6]) for w in win if len(w) >= 6) for t in rest):
                    return cand, "window" if size > 1 or rest else "token"
    return None


def _window_variants(win: list[str]):
    from itertools import product
    if len(win) == 1:
        return token_variants(win[0])
    return [" ".join(c) for c in product(*[token_variants(t)[:8] for t in win])]


def match_component(raw: str):
    """回傳 (drugbank_name, rule) 或 None。"""
    base = deaccent(raw).strip()
    if not base:
        return None
    pieces = [base]
    inner = re.findall(r"\(([^)]*)\)", base)
    outer = re.sub(r"\([^)]*\)", " ", base).strip()
    if outer and outer != base:
        pieces.append(outer)
    pieces += inner
    for piece in pieces:
        toks = clean_tokens(piece)
        if not toks:
            continue
        full = " ".join(toks)
        if hit(full):
            return full, "exact"
        core = [t for t in toks if t not in SALTS]
        if not core:
            continue
        # 酸類
        if any(t in ACID_WORDS for t in core):
            rest = [t for t in core if t not in ACID_WORDS]
            if rest:
                for v in token_variants(rest[-1] if len(rest) == 1 else " ".join(rest)):
                    for cand in (f"{v} ACID", f"{v}IC ACID" if not v.endswith("IC") else None):
                        if cand and hit(cand):
                            return cand, "acid"
        phrase = " ".join(core)
        if hit(phrase):
            return phrase, "salt"
        # 多字：最後一個字套語尾規則；單字：整字套
        head, last = core[:-1], core[-1]
        for v in token_variants(last):
            cand = " ".join(head + [v])
            if hit(cand):
                return cand, "suffix"
        if 2 <= len(core) <= 3:  # 每個字都套變體再組合（FIBRINOGENUM HUMANUM → FIBRINOGEN HUMAN）
            from itertools import product
            for combo in product(*[token_variants(t)[:12] for t in core]):
                cand = " ".join(combo)
                if hit(cand):
                    return cand, "suffix_multi"
        if len(core) == 1:
            for v in token_variants(last):
                m = one_edit(v)
                if m:
                    return m, "edit1"
        # 單一成分才試子片語；含複方分隔符的交給 rescue_ingredient 拆開，避免只抓到其中一個
        if COMBO_SPLIT.search(base):
            continue
        m = window_match(core)
        if m:
            return m
    return None


COMBO_SPLIT = re.compile(r"\s*(?:;|,|\+|/| Y | ET | UND | AND | E | OG | EN | OCH | JA | WITH | CON | MIT | MED | AVEC )\s*")


# 疫苗、過敏原萃取：成分字串裡的殘留物（如 POLYMYXIN B）會被誤配成藥，整筆不救
NON_DRUG = re.compile(r"TOXOID|VACCIN|VAKSIN|VACUNA|VAKZIN|IMPFSTOFF|VIRUS|ANTIGEN|BORDETELL|POLIOMYEL|HEPATITID|"
                      r"INFLUENZA|ALLERGEN|POLLEN|POLLINI|MILBE|ACARI|VENOM|GIFT")


def rescue_ingredient(raw: str):
    """回傳 [(drugbank_name, rule), ...]；複方會有多個。"""
    if NON_DRUG.search(deaccent(raw)):
        return []
    parts = [p for p in COMBO_SPLIT.split(deaccent(raw)) if p.strip()]
    if len(parts) < 2:
        m = match_component(raw)
        return [m] if m else []
    m = match_component(raw)
    if m and m[1] == "exact":  # 整串本身就是 DrugBank 名稱（例：AMOXICILLIN AND CLAVULANATE 若有）
        return [m]
    out, seen = [], set()
    for p in parts:
        mm = match_component(p)
        if mm and mm[0] not in seen:
            seen.add(mm[0])
            out.append((mm[0], "combo_" + mm[1]))
    return out


def process(proj: Path, apply: bool, sample: int):
    f = proj / "data/processed/drug_mapping.csv"
    if not f.exists():
        return None
    rows = list(csv.reader(open(f, encoding="utf-8-sig")))
    head, body = rows[0], rows[1:]
    have = {r[5] for r in body if len(r) > 6 and r[6] == "True" and r[5]}
    new_body, changed, new_ids, examples = [], 0, set(), []
    cache = {}
    for r in body:
        if len(r) <= 7 or r[6] == "True":
            new_body.append(r)
            continue
        ing = r[3] or r[2]
        if ing not in cache:
            cache[ing] = rescue_ingredient(ing)
        res = cache[ing]
        if not res:
            new_body.append(r)
            continue
        for k, (name, rule) in enumerate(res):
            nr = list(r)
            nr[5], nr[6], nr[7] = vocab[name], "True", f"{TAG}:{rule}"
            if len(res) > 1:
                nr[3] = name
            new_body.append(nr)
            if vocab[name] not in have:
                new_ids.add(vocab[name])
        changed += 1
        if len(examples) < sample:
            examples.append(f"{ing[:45]!r} -> {' + '.join(n for n, _ in res)} [{','.join(rl for _, rl in res)}]")
    if apply and changed:
        bak = f.with_name("drug_mapping.csv.bak_20261012")
        if not bak.exists():
            shutil.copy2(f, bak)
        with open(f, "w", encoding="utf-8", newline="") as fo:
            w = csv.writer(fo)
            w.writerow(head)
            w.writerows(new_body)
    return changed, len(body), len(have), new_ids, examples


def main():
    apply = "--apply" in sys.argv
    sample = 0
    if "--sample" in sys.argv:
        sample = int(sys.argv[sys.argv.index("--sample") + 1])
    args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and sys.argv[i - 1] != "--sample"]
    targets = [BASE / a for a in args] or sorted(_site_registry.glob_sites(BASE))
    tot_new = 0
    for p in targets:
        r = process(p, apply, sample)
        if r is None:
            continue
        changed, n, had, new_ids, ex = r
        tot_new += len(new_ids)
        print(f"{p.name:10} rows={n:6} rescued_rows={changed:5} drugs_before={had:5} new_drugs={len(new_ids):4}")
        for e in ex:
            print("    ", e)
    print(("applied" if apply else "dry-run"), "total new drugs", tot_new)


if __name__ == "__main__":
    main()
