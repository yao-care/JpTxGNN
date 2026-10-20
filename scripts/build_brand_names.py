"""日本產品名（販売名）→ 成分頁 對照表（2026-10-17，U-03 後續；U-03b 改寫）。

來源：data/processed/drug_mapping.csv（承認番号／販売名／原始主成分／標準化成分／drugbank_id），
以及 data/raw/jp_fda_drugs.json 的「商品名一覧」。

- 單方：drugbank_id 對到可收錄的成分頁。離子類 ID（CALCIUM／IRON／ZINC／MAGNESIUM／LITHIUM）
  只收成分名真的是該離子的鹽（例：グルコン酸カルシウム、クエン酸第一鉄ナトリウム），
  ヘパリンカルシウム這種「別的藥的鹽」不收。沒有 drugbank_id 的列，用成分名（去掉規格、劑形、鹽類）對單方索引。
- 複方（成分名含「配合」）：拆成各成分，分別對到成分頁，列在每個成分頁的「配合剤」；不用 mapping 裡只對到一個成分的 drugbank_id。
- 商品名：「商品名一覧」裡「後発品」那行之前的先發品名，加上先發品販売名去掉規格劑形（ノルバスク錠2.5mg → ノルバスク）；
  成分學名或以學名開頭的名稱（後發品）不算商品名。
輸出 docs/_data/brand_names.json：{成分頁檔名: {"trade": [...], "hanbai": [...], "combo": [...]}}。
用法：uv run python scripts/build_brand_names.py
之後必跑（json 改了頁面不會自己變；scripts/check_seo_docs.py 第 5 項會擋）：
  母目錄 python3 .claude/apply_brand_names.py JpTxGNN && python3 .claude/rebuild_search_index.py JpTxGNN
"""
import csv, json, re, unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRUGS = ROOT / "docs/_drugs"
OUT = ROOT / "docs/_data/brand_names.json"
ION = {"CALCIUM": "カルシウム", "IRON": "鉄", "ZINC": "亜鉛", "MAGNESIUM": "マグネシウム", "LITHIUM": "リチウム"}
FORM = re.compile(r"(口腔内崩壊錠|徐放錠|腸溶錠|フィルムコーティング錠|チュアブル錠|錠|カプセル|注射液|注射用|注|散|顆粒|細粒|"
                  r"シロップ|ドライシロップ|内用液|液|点眼|点鼻|軟膏|クリーム|ゲル|テープ|パップ|貼付剤|坐剤|吸入|キット|"
                  r"エキス|末|原末|点滴静|点滴|眼科用|眼|パウダー|OD|ＯＤ).*$")
SALT = re.compile(r"(ベシル酸塩|塩酸塩|硫酸塩|酢酸塩|マレイン酸塩|酒石酸塩|フマル酸塩|メシル酸塩|臭化水素酸塩|リン酸塩|"
                  r"ナトリウム|カリウム|カルシウム|水和物|エステル)+$")


def nfkc(s):
    return unicodedata.normalize("NFKC", s or "").strip()


def norm(s):
    return re.sub(r"[\s_・\-－（）()「」『』､、,，.]", "", nfkc(s)).lower()


def base_name(s):
    """成分名去掉括號、規格、劑形：アムロジピン5mg → アムロジピン；テルミサルタン錠40mg → テルミサルタン。"""
    s = re.sub(r"[（(][^）)]*[）)]", "", nfkc(s))
    if re.match(r"^d[\-−‐ｰー]?クロルフェニラミン", s, re.I):
        return "デクスクロルフェニラミン"  # d-体（DrugBank 另有 dexchlorpheniramine），不是 chlorpheniramine
    s = re.sub(r"^(dl|d|l)[\-−‐]", "", s, flags=re.I)
    s = re.split(r"[\d.]+\s*(mg|g|μg|mL|%|単位|U)", s, flags=re.I)[0]
    s = FORM.sub("", s).strip(" 　・")
    return re.sub(r"[\d.]+$", "", s).strip()  # 不帶單位的規格（…0.1）


def components(ing):
    """複方成分名 → 各成分基本名；不是複方回傳 None。"""
    s = nfkc(ing)
    if "配合" not in s:
        return None
    s = s.split("配合")[0]
    parts = [base_name(p) for p in s.split("・")]
    return [p for p in parts if p and not p.endswith("等")] or None


# 原始成分欄只有品牌讀音、拆不出成分的產品：明確列組成（2026-10-17，U-03b 第二輪；只收組成確定的品牌）。
# 值是各成分的 DrugBank ID 候選（同一成分不同鹽的 ID 用「|」），空串列＝不歸任何成分頁。
BRANDS = {
    "アドエア": ["DB00938", "DB00588|DB13867"],          # salmeterol + fluticasone propionate
    "レルベア": ["DB09082", "DB08906|DB13867"],          # vilanterol + fluticasone furoate
    "エピデュオ": ["DB00210", "DB09096"],                # adapalene + benzoyl peroxide
    "ミドリンP": ["DB00809", "DB00388"],                 # tropicamide + phenylephrine
    "複方オキシコドン": ["DB00497"],                      # oxycodone + hydrocotarnine（後者無 DrugBank 頁）
    "ネオメドロールEE": ["DB00959", "DB00452|DB00994"],   # methylprednisolone + fradiomycin
    "テトラサイクリン・プレステロン": ["DB00759"],         # tetracycline + epidihydrocholesterin
    "リンデロン-VG": ["DB00443", "DB00798"],             # betamethasone valerate + gentamicin
    "リンデロン−VG": ["DB00443", "DB00798"],
    "眼・耳科用リンデロンA": ["DB00443", "DB00452|DB00994"],  # betamethasone + fradiomycin
    "テラ・コートリル": ["DB00595", "DB00741"],           # oxytetracycline + hydrocortisone
    "歯科用キシロカイン": ["DB00281", "DB00668"],         # lidocaine + epinephrine
    "マドパー": ["DB01235", "DB12783"],                  # levodopa + benserazide
    "スタレボ": ["DB01235", "DB00190", "DB00494"],        # levodopa + carbidopa + entacapone
    "エプジコム": ["DB01048", "DB00709"],                # abacavir + lamivudine
    "ティーエスワン": ["DB09256", "DB09257", "DB03209"],  # tegafur + gimeracil + oteracil
    "ユーエフティ": ["DB09256", "DB03419"],              # tegafur + uracil
    "シナール": ["DB00126", "DB01783"],                  # ascorbic acid + calcium pantothenate
    "ユナシン-S": ["DB00415", "DB09324"],                # ampicillin + sulbactam
    "ユナシン−S": ["DB00415", "DB09324"],
    "スルバシリン": ["DB00415", "DB09324"],
    "強力レスタミンコーチゾンコーワ": ["DB01075", "DB00741"],  # diphenhydramine + hydrocortisone acetate
    "ネオレスタミンコーワ": ["DB01114"],                  # 單方 chlorpheniramine（mapping 誤對 diphenhydramine）
    "ブライアン": [],                                    # edetate calcium disodium，不是 calcium
    "ワンタキソテール": ["DB01248"],                     # docetaxel（主成分欄是讀音，會被當成タキソテール的變體）
    "セレスタミン": ["DB00443", ""],                     # betamethasone + d-chlorpheniramine（後者本站無頁）
    "ポララミン": [],                                    # dexchlorpheniramine（本站無成分頁），不是 chlorpheniramine
}


def brand_override(name):
    n = nfkc(name)
    for k in sorted(BRANDS, key=len, reverse=True):
        if nfkc(k) in n:  # 含前綴（小児用レルベア）也算
            return BRANDS[k]
    return None


def ion_ok(syn, name):
    """離子類 ID 只收該離子本身的鹽；「片假名藥名＋カルシウム」（ヘパリンカルシウム）不收。"""
    w = ION.get((syn or "").upper())
    if not w:
        return True
    n = nfkc(name)
    if w not in n:
        return False
    return not re.search(r"[ァ-ヶー]{3,}" + re.escape(w), n)


def main():
    rows = list(csv.DictReader(open(ROOT / "data/processed/drug_mapping.csv", encoding="utf-8-sig")))
    # drugbank_id → 可收錄成分頁
    id2page = {}
    def indexable(p):
        t = p.read_text(encoding="utf-8", errors="replace")[:3000]
        return 'http-equiv="refresh"' not in t and not re.search(r"^noindex:\s*true", t, re.M)
    for f in DRUGS.glob("*.md"):
        m = re.search(r"^drugbank_id:\s*(DB\d+)", f.read_text(encoding="utf-8", errors="replace")[:3000], re.M)
        if m and indexable(f):
            id2page.setdefault(m.group(1), f.stem)
    for b in (ROOT / "data/bundles").glob("*/drug_bundle.json"):
        try:
            db = json.load(open(b, encoding="utf-8"))["drug"].get("drugbank_id")
        except Exception:
            continue
        p = DRUGS / f"{b.parent.name}.md"
        if db and p.exists() and indexable(p):
            id2page.setdefault(db, b.parent.name)

    # 同一 DrugBank ID 底下若有「另一個基本名＋前綴」（ジヒドロコデイン ⊃ コデイン、レミフェンタニル ⊃ フェンタニル），
    # 前者是 mapping 用子字串對錯的別的藥，不收
    db_bases = defaultdict(set)
    for r in rows:
        if r.get("drugbank_id"):
            db_bases[r["drugbank_id"]].add(norm(SALT.sub("", base_name(r["原始主成分"] or r["標準化成分"]))))
    def prefixed_variant(db, ing):
        b = norm(SALT.sub("", base_name(ing)))
        b = re.sub(r"^(スイヨウセイ|水溶性|ショウニヨウ|小児用)", "", b)  # 劑型前綴（水溶性プレドニン）不是別的藥
        return any(o != b and len(o) >= 3 and b.endswith(o) for o in db_bases.get(db, ()))
    # 單方成分名索引（基本名與去鹽名），只收不衝突的
    idx = defaultdict(set)
    for r in rows:
        db = r.get("drugbank_id")
        ing = r["原始主成分"] or r["標準化成分"]
        if not db or components(ing) or "配合" in nfkc(r["販売名"]) or not ion_ok(r.get("同義詞"), ing) or "類似物質" in nfkc(ing):
            continue
        b = base_name(ing)
        if prefixed_variant(db, ing):
            continue
        for k in {norm(b), norm(SALT.sub("", b)), norm(re.sub(r"(?<=[ァ-ヶー])(K|Na|Ca)$", "", b))}:  # ロサルタンK
            if len(k) >= 3:
                idx[k].add(db)
    def by_name(name):
        b = base_name(name)
        if b == "デクスクロルフェニラミン":
            return None  # mapping 把 d-体對到 chlorpheniramine 的 ID
        for k in (norm(b), norm(SALT.sub("", b)), norm(re.sub(r"(?<=[ァ-ヶー])(K|Na|Ca)$", "", b))):
            c = idx.get(k)
            if c and len(c) == 1:
                return next(iter(c))
        return None

    hanbai, combo, trade = defaultdict(set), defaultdict(set), defaultdict(set)
    num2pages = {}
    for r in rows:
        name = nfkc(r["販売名"])
        if not name:
            continue
        ing = r["原始主成分"] or r["標準化成分"]
        ov = brand_override(name)
        if ov is not None:
            pages = set()
            for alt in ov:
                pages |= {next((id2page[d] for d in alt.split("|") if d in id2page), None)} - {None}
            kind = "combo" if len(ov) > 1 or any(x in name for x in ("複方", "配合", "・")) else "single"
            for p in pages:
                (combo if kind == "combo" else hanbai)[p].add(name)
            if pages:
                num2pages[r["承認番号"]] = (kind, pages)
            continue
        comps = components(ing) or components(name)
        if not comps and "・" in name:  # 「A・B」寫法沒有「配合」二字（アンピシリンナトリウム・スルバクタムナトリウム）
            parts = [base_name(x) for x in name.split("・")]
            if len(parts) >= 2 and all(len(x) >= 4 for x in parts) and (any(by_name(x) for x in parts) or r.get("drugbank_id")):
                comps = parts
        if comps:
            pages = {id2page.get(by_name(c)) for c in comps} - {None}
            if "・" in name and "配合" not in name and r.get("drugbank_id") and not prefixed_variant(r["drugbank_id"], ing):
                pages |= {id2page.get(r["drugbank_id"])} - {None}  # 成分名對不到索引時，至少歸到 mapping 對到的成分
            if (not pages and r.get("drugbank_id") and ion_ok(r.get("同義詞"), ing) and "類似物質" not in nfkc(ing)
                    and any(norm(SALT.sub("", c)) in db_bases.get(r["drugbank_id"], ()) for c in comps)):  # 成分名要與該 ID 的單方成分名相同（ジヒドロコデイン≠コデイン）
                pages = {id2page.get(r["drugbank_id"])} - {None}  # ヘモポリゾン（大腸菌死菌・ヒドロコルチゾン）、マルファ（水酸化マグネシウム）
            for p in pages:
                combo[p].add(name)
            num2pages[r["承認番号"]] = ("combo", pages)
            continue
        if "類似物質" in nfkc(ing):
            continue  # ヘパリン類似物質（ヒルドイド）不是ヘパリン
        if "デクスクロルフェニラミン" in (base_name(ing), base_name(name)):
            continue
        db = r.get("drugbank_id") if ion_ok(r.get("同義詞"), ing) else None
        if db and prefixed_variant(db, ing):
            db = None
        db = db or by_name(ing) or by_name(name)
        p = id2page.get(db) if db else None
        if p:
            hanbai[p].add(name)
            num2pages[r["承認番号"]] = ("single", {p})

    try:
        raw = json.load(open(ROOT / "data/raw/jp_fda_drugs.json", encoding="utf-8"))
    except Exception:
        raw = []
    # 成分學名集合：商品名不可以是學名，也不可以用學名開頭（アムロジピン錠「サワイ」是後發品販売名）
    generic = set()
    kegg = {str(d.get("承認番号")): d.get("KEGG_ID") for d in raw}
    for r in rows:
        for s in (r["原始主成分"], r["標準化成分"]):
            if norm(base_name(s)) == norm(base_name(r["販売名"])) and not kegg.get(r["承認番号"]):
                continue  # 主成分欄只是販売名讀音、KEGG 也沒有藥物 ID（アマリール1MG），不是學名；アザチオプリン錠有 D00238，是學名
            for c in components(s) or [base_name(s)]:
                generic |= {norm(c), norm(SALT.sub("", c))}
    for d in raw:
        for s in (d.get("一般名"), d.get("有効成分")):
            if norm(base_name(s)) == norm(base_name(d.get("販売名"))) and not d.get("KEGG_ID"):
                continue
            generic |= {norm(base_name(s)), norm(SALT.sub("", base_name(s)))}
    generic = {g for g in generic if len(g) >= 3}
    # 乾淨的學名來源（SSK 主成分欄混有品牌讀音，如ネオレスタミンコーワ）：PMDA 一般名＋後發品販売名（帶「屋号」）去規格劑形
    clean = {norm(SALT.sub("", base_name(d.get("一般名")))) for d in raw if d.get("一般名")}
    clean |= {norm(SALT.sub("", base_name(r["販売名"]))) for r in rows if re.search(r"[「『]", nfkc(r["販売名"]))}
    clean = {g for g in clean if len(g) >= 4}
    chem = re.compile(r"塩酸|硫酸塩|酢酸塩|水和物|酸化|塩化|炭酸|リン酸|クエン酸|ナトリウム|カリウム|カルシウム|マグネシウム|石灰")
    def is_generic(nm):
        if chem.search(nfkc(nm)):
            return True  # 化學名（モルヒネ塩酸塩、重質酸化マグネシウム）不是商品名
        n = norm(nm)
        return (n in generic or norm(SALT.sub("", nm)) in generic or any(n.startswith(g) for g in generic if len(g) >= 4)
                or (len(n) >= 4 and any(g.startswith(n) for g in clean)) or norm(SALT.sub("", base_name(nm))) in clean)  # 學名的前半（ベクロメタゾン ⊂ ベクロメタゾンプロピオン酸エステル）
    # 先發品販売名本身就帶商品名（ノルバスク錠2.5mg → ノルバスク）
    for r in rows:
        kind, pages = num2pages.get(r["承認番号"], (None, set()))
        b = re.sub(r"配合.*$", "", base_name(r["販売名"]))
        if kind == "single" and b and len(b) <= 20 and not is_generic(b):
            for p in pages:
                trade[p].add(b)
    for d in raw:
        kind, pages = num2pages.get(str(d.get("承認番号", "")), (None, set()))
        if not pages:
            continue
        for line in str(d.get("商品名一覧", "")).split("\n"):
            if line.strip().startswith("後発品"):
                break  # 之後是後發品（多為成分學名）
            nm = nfkc(re.sub(r"\s*[(（][^)）]*[)）]\s*$", "", line))
            if not nm or len(nm) > 30 or is_generic(nm):
                continue
            for p in pages:
                (combo if kind == "combo" else trade)[p].add(nm)

    def dedupe(names):
        # 去掉廠商後綴「…」與「(選)」再去重（同一規格不同廠商只列一次）
        seen, out_ = set(), []
        for x in sorted(names):
            y = re.sub(r"[「『][^」』]*[」』]|\(選\)", "", x).strip()
            if y and y not in seen:
                seen.add(y)
                out_.append(y)
        return out_
    # 「商品名一覧」是 KEGG 依同類藥列的，會把別的產品掛進來（エンペラシン配合錠是 d-クロルフェニラミン，掛到 chlorpheniramine）：
    # 名稱本身就是某個販売名時，以該販売名自己的歸屬為準
    own = defaultdict(set)
    for r in rows:
        if r["承認番号"] in num2pages:
            own[nfkc(r["販売名"])] |= num2pages[r["承認番号"]][1]
        else:
            own.setdefault(nfkc(r["販売名"]), set())
    for d_ in (combo, hanbai):
        for k in list(d_):
            d_[k] = {x for x in d_[k] if x not in own or k in own[x]}
    out = {}
    for k in sorted(set(hanbai) | set(trade) | set(combo)):
        t = dedupe(trade.get(k, set()))
        h = [x for x in dedupe(hanbai.get(k, set())) if x not in t]
        c = dedupe(combo.get(k, set()))
        out[k] = {"trade": t, "hanbai": h, "combo": c}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"成分頁 {len(out)} 頁、商品名 {sum(len(v['trade']) for v in out.values())} 個、"
          f"販売名 {sum(len(v['hanbai']) for v in out.values())} 個、配合剤 {sum(len(v['combo']) for v in out.values())} 個 → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
