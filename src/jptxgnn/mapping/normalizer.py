"""主成分名稱標準化"""

import re
from typing import List, Tuple


# 日本語（カタカナ）→ 英語 薬物名対照表
# 一般的な医薬品約200種
JAPANESE_DRUG_DICT = {
    # === 解熱鎮痛薬 ===
    "アセトアミノフェン": "ACETAMINOPHEN",
    "アスピリン": "ASPIRIN",
    "イブプロフェン": "IBUPROFEN",
    "ロキソプロフェン": "LOXOPROFEN",
    "ジクロフェナク": "DICLOFENAC",
    "インドメタシン": "INDOMETHACIN",
    "ナプロキセン": "NAPROXEN",
    "セレコキシブ": "CELECOXIB",
    "メロキシカム": "MELOXICAM",
    "ピロキシカム": "PIROXICAM",

    # === 消化器系 ===
    "ファモチジン": "FAMOTIDINE",
    "ラニチジン": "RANITIDINE",
    "オメプラゾール": "OMEPRAZOLE",
    "ランソプラゾール": "LANSOPRAZOLE",
    "エソメプラゾール": "ESOMEPRAZOLE",
    "ラベプラゾール": "RABEPRAZOLE",
    "メトクロプラミド": "METOCLOPRAMIDE",
    "ドンペリドン": "DOMPERIDONE",
    "スクラルファート": "SUCRALFATE",
    "ミソプロストール": "MISOPROSTOL",

    # === 循環器系 ===
    "アムロジピン": "AMLODIPINE",
    "ニフェジピン": "NIFEDIPINE",
    "ベラパミル": "VERAPAMIL",
    "ジルチアゼム": "DILTIAZEM",
    "アテノロール": "ATENOLOL",
    "メトプロロール": "METOPROLOL",
    "プロプラノロール": "PROPRANOLOL",
    "カルベジロール": "CARVEDILOL",
    "ビソプロロール": "BISOPROLOL",
    "エナラプリル": "ENALAPRIL",
    "リシノプリル": "LISINOPRIL",
    "ロサルタン": "LOSARTAN",
    "バルサルタン": "VALSARTAN",
    "カンデサルタン": "CANDESARTAN",
    "テルミサルタン": "TELMISARTAN",
    "フロセミド": "FUROSEMIDE",
    "スピロノラクトン": "SPIRONOLACTONE",
    "ヒドロクロロチアジド": "HYDROCHLOROTHIAZIDE",
    "ワルファリン": "WARFARIN",
    "アスピリン": "ASPIRIN",
    "クロピドグレル": "CLOPIDOGREL",

    # === 糖尿病薬 ===
    "メトホルミン": "METFORMIN",
    "グリベンクラミド": "GLYBURIDE",
    "グリクラジド": "GLICLAZIDE",
    "グリメピリド": "GLIMEPIRIDE",
    "ピオグリタゾン": "PIOGLITAZONE",
    "シタグリプチン": "SITAGLIPTIN",
    "リナグリプチン": "LINAGLIPTIN",
    "エンパグリフロジン": "EMPAGLIFLOZIN",
    "ダパグリフロジン": "DAPAGLIFLOZIN",
    "インスリン": "INSULIN",

    # === 抗生物質 ===
    "アモキシシリン": "AMOXICILLIN",
    "アンピシリン": "AMPICILLIN",
    "セファレキシン": "CEPHALEXIN",
    "セフトリアキソン": "CEFTRIAXONE",
    "セフェピム": "CEFEPIME",
    "アジスロマイシン": "AZITHROMYCIN",
    "クラリスロマイシン": "CLARITHROMYCIN",
    "エリスロマイシン": "ERYTHROMYCIN",
    "レボフロキサシン": "LEVOFLOXACIN",
    "シプロフロキサシン": "CIPROFLOXACIN",
    "モキシフロキサシン": "MOXIFLOXACIN",
    "メトロニダゾール": "METRONIDAZOLE",
    "バンコマイシン": "VANCOMYCIN",
    "ゲンタマイシン": "GENTAMICIN",
    "ドキシサイクリン": "DOXYCYCLINE",
    "テトラサイクリン": "TETRACYCLINE",

    # === 抗真菌薬 ===
    "フルコナゾール": "FLUCONAZOLE",
    "イトラコナゾール": "ITRACONAZOLE",
    "ボリコナゾール": "VORICONAZOLE",
    "ナイスタチン": "NYSTATIN",
    "ミコナゾール": "MICONAZOLE",
    "クロトリマゾール": "CLOTRIMAZOLE",
    "テルビナフィン": "TERBINAFINE",

    # === 抗ウイルス薬 ===
    "アシクロビル": "ACYCLOVIR",
    "バラシクロビル": "VALACYCLOVIR",
    "オセルタミビル": "OSELTAMIVIR",
    "ザナミビル": "ZANAMIVIR",
    "リバビリン": "RIBAVIRIN",
    "ラミブジン": "LAMIVUDINE",
    "テノホビル": "TENOFOVIR",

    # === 精神神経系 ===
    "ジアゼパム": "DIAZEPAM",
    "ロラゼパム": "LORAZEPAM",
    "アルプラゾラム": "ALPRAZOLAM",
    "クロナゼパム": "CLONAZEPAM",
    "ゾルピデム": "ZOLPIDEM",
    "エスゾピクロン": "ESZOPICLONE",
    "フルオキセチン": "FLUOXETINE",
    "セルトラリン": "SERTRALINE",
    "パロキセチン": "PAROXETINE",
    "エスシタロプラム": "ESCITALOPRAM",
    "ベンラファキシン": "VENLAFAXINE",
    "デュロキセチン": "DULOXETINE",
    "ミルタザピン": "MIRTAZAPINE",
    "アミトリプチリン": "AMITRIPTYLINE",
    "ノルトリプチリン": "NORTRIPTYLINE",
    "リスペリドン": "RISPERIDONE",
    "オランザピン": "OLANZAPINE",
    "クエチアピン": "QUETIAPINE",
    "アリピプラゾール": "ARIPIPRAZOLE",
    "ハロペリドール": "HALOPERIDOL",
    "リチウム": "LITHIUM",
    "バルプロ酸": "VALPROIC ACID",
    "カルバマゼピン": "CARBAMAZEPINE",
    "フェニトイン": "PHENYTOIN",
    "レベチラセタム": "LEVETIRACETAM",
    "ラモトリギン": "LAMOTRIGINE",
    "トピラマート": "TOPIRAMATE",
    "ガバペンチン": "GABAPENTIN",
    "プレガバリン": "PREGABALIN",

    # === 呼吸器系 ===
    "サルブタモール": "ALBUTEROL",
    "サルメテロール": "SALMETEROL",
    "フォルモテロール": "FORMOTEROL",
    "フルチカゾン": "FLUTICASONE",
    "ブデソニド": "BUDESONIDE",
    "ベクロメタゾン": "BECLOMETHASONE",
    "モンテルカスト": "MONTELUKAST",
    "テオフィリン": "THEOPHYLLINE",
    "デキストロメトルファン": "DEXTROMETHORPHAN",
    "コデイン": "CODEINE",

    # === アレルギー・抗ヒスタミン ===
    "セチリジン": "CETIRIZINE",
    "ロラタジン": "LORATADINE",
    "フェキソフェナジン": "FEXOFENADINE",
    "デスロラタジン": "DESLORATADINE",
    "ジフェンヒドラミン": "DIPHENHYDRAMINE",
    "クロルフェニラミン": "CHLORPHENIRAMINE",
    "プロメタジン": "PROMETHAZINE",

    # === ステロイド ===
    "プレドニゾロン": "PREDNISOLONE",
    "プレドニゾン": "PREDNISONE",
    "メチルプレドニゾロン": "METHYLPREDNISOLONE",
    "デキサメタゾン": "DEXAMETHASONE",
    "ヒドロコルチゾン": "HYDROCORTISONE",
    "ベタメタゾン": "BETAMETHASONE",
    "トリアムシノロン": "TRIAMCINOLONE",

    # === 消化管運動・制吐薬 ===
    "オンダンセトロン": "ONDANSETRON",
    "グラニセトロン": "GRANISETRON",
    "プロクロルペラジン": "PROCHLORPERAZINE",
    "ロペラミド": "LOPERAMIDE",
    "センノシド": "SENNOSIDES",
    "ラクツロース": "LACTULOSE",
    "ビサコジル": "BISACODYL",

    # === 泌尿器系 ===
    "タムスロシン": "TAMSULOSIN",
    "シロドシン": "SILODOSIN",
    "フィナステリド": "FINASTERIDE",
    "デュタステリド": "DUTASTERIDE",
    "オキシブチニン": "OXYBUTYNIN",
    "ソリフェナシン": "SOLIFENACIN",
    "シルデナフィル": "SILDENAFIL",
    "タダラフィル": "TADALAFIL",

    # === 甲状腺 ===
    "レボチロキシン": "LEVOTHYROXINE",
    "メチマゾール": "METHIMAZOLE",
    "プロピルチオウラシル": "PROPYLTHIOURACIL",

    # === 骨粗鬆症 ===
    "アレンドロネート": "ALENDRONATE",
    "リセドロネート": "RISEDRONATE",
    "ゾレドロン酸": "ZOLEDRONIC ACID",
    "デノスマブ": "DENOSUMAB",
    "カルシトニン": "CALCITONIN",

    # === 高脂血症 ===
    "アトルバスタチン": "ATORVASTATIN",
    "ロスバスタチン": "ROSUVASTATIN",
    "シンバスタチン": "SIMVASTATIN",
    "プラバスタチン": "PRAVASTATIN",
    "フェノフィブラート": "FENOFIBRATE",
    "エゼチミブ": "EZETIMIBE",

    # === 痛風・高尿酸血症 ===
    "アロプリノール": "ALLOPURINOL",
    "フェブキソスタット": "FEBUXOSTAT",
    "コルヒチン": "COLCHICINE",

    # === 抗凝固薬・抗血栓薬 ===
    "ヘパリン": "HEPARIN",
    "エノキサパリン": "ENOXAPARIN",
    "ダビガトラン": "DABIGATRAN",
    "リバーロキサバン": "RIVAROXABAN",
    "アピキサバン": "APIXABAN",
    "エドキサバン": "EDOXABAN",
    "チクロピジン": "TICLOPIDINE",
    "プラスグレル": "PRASUGREL",

    # === 免疫抑制薬 ===
    "タクロリムス": "TACROLIMUS",
    "シクロスポリン": "CYCLOSPORINE",
    "アザチオプリン": "AZATHIOPRINE",
    "ミコフェノール酸": "MYCOPHENOLIC ACID",
    "メトトレキサート": "METHOTREXATE",
    "シクロホスファミド": "CYCLOPHOSPHAMIDE",

    # === 抗癌剤（一部） ===
    "パクリタキセル": "PACLITAXEL",
    "ドセタキセル": "DOCETAXEL",
    "シスプラチン": "CISPLATIN",
    "カルボプラチン": "CARBOPLATIN",
    "フルオロウラシル": "FLUOROURACIL",
    "カペシタビン": "CAPECITABINE",
    "ゲムシタビン": "GEMCITABINE",
    "ドキソルビシン": "DOXORUBICIN",
    "イマチニブ": "IMATINIB",
    "エルロチニブ": "ERLOTINIB",
    "ゲフィチニブ": "GEFITINIB",

    # === 局所麻酔・麻酔補助 ===
    "リドカイン": "LIDOCAINE",
    "プロカイン": "PROCAINE",
    "ブピバカイン": "BUPIVACAINE",
    "ロピバカイン": "ROPIVACAINE",
    "プロポフォール": "PROPOFOL",
    "ケタミン": "KETAMINE",
    "フェンタニル": "FENTANYL",
    "モルヒネ": "MORPHINE",
    "オキシコドン": "OXYCODONE",
    "トラマドール": "TRAMADOL",

    # === ビタミン・ミネラル ===
    "ビタミンＢ１": "THIAMINE",
    "チアミン": "THIAMINE",
    "ビタミンＢ２": "RIBOFLAVIN",
    "リボフラビン": "RIBOFLAVIN",
    "ビタミンＢ６": "PYRIDOXINE",
    "ピリドキシン": "PYRIDOXINE",
    "ビタミンＢ１２": "CYANOCOBALAMIN",
    "シアノコバラミン": "CYANOCOBALAMIN",
    "ビタミンＣ": "ASCORBIC ACID",
    "アスコルビン酸": "ASCORBIC ACID",
    "ビタミンＤ": "CHOLECALCIFEROL",
    "コレカルシフェロール": "CHOLECALCIFEROL",
    "ビタミンＥ": "TOCOPHEROL",
    "トコフェロール": "TOCOPHEROL",
    "ビタミンＫ": "PHYTONADIONE",
    "フィトナジオン": "PHYTONADIONE",
    "葉酸": "FOLIC ACID",
    "カルシウム": "CALCIUM",
    "マグネシウム": "MAGNESIUM",
    "亜鉛": "ZINC",
    "鉄": "IRON",

    # === 眼科 ===
    "チモロール": "TIMOLOL",
    "ラタノプロスト": "LATANOPROST",
    "ピロカルピン": "PILOCARPINE",
    "アトロピン": "ATROPINE",
    "トロピカミド": "TROPICAMIDE",
}


def translate_japanese_to_english(name: str) -> str:
    """日本語薬物名を英語に変換

    Args:
        name: 日本語薬物名（カタカナ）

    Returns:
        英語薬物名、見つからない場合は元の名前
    """
    if not name:
        return ""

    # 全角数字・記号を除去して基本名を抽出
    base_name = re.sub(r'[０-９0-9]+', '', name)
    base_name = re.sub(r'[％%ｇg錠mg散].*$', '', base_name)
    base_name = base_name.strip()

    # 辞書で検索
    if base_name in JAPANESE_DRUG_DICT:
        return JAPANESE_DRUG_DICT[base_name]

    # 部分一致を試行（より長いキーを優先）
    for jp_name in sorted(JAPANESE_DRUG_DICT.keys(), key=len, reverse=True):
        if jp_name in name:
            return JAPANESE_DRUG_DICT[jp_name]

    return name.upper()


def normalize_ingredient(name: str) -> str:
    """標準化單一成分名稱

    處理邏輯：
    1. 移除括號內的同義詞（EQ TO ...）
    2. 移除其他括號內容（如 VIT B2）
    3. 統一大小寫
    4. 移除多餘空白

    Args:
        name: 原始成分名稱

    Returns:
        標準化後的名稱
    """
    if not name:
        return ""

    # 統一全形括號為半形
    name = name.replace("（", "(").replace("）", ")")

    # 移除括號內容（包含 EQ TO 的同義詞、VIT 等）
    # 但保留括號前的主名稱
    name = re.sub(r"\s*\([^)]*\)", "", name)

    # 移除鹽類後綴的多餘資訊（保留鹽類如 HCL, SODIUM 等）
    name = name.strip()

    # 統一大寫
    name = name.upper()

    # 移除多餘空白
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def extract_ingredients(ingredient_str: str) -> List[str]:
    """從主成分略述欄位提取所有成分

    FDA 資料中多成分以 ; 或 ;; 分隔

    Args:
        ingredient_str: 主成分略述欄位原始值

    Returns:
        標準化後的成分列表
    """
    if not ingredient_str:
        return []

    # 統一分隔符號
    # 有些用 ;; 有些用 ;
    ingredient_str = ingredient_str.replace(";;", ";").replace("；", ";")

    # 分割
    parts = ingredient_str.split(";")

    # 標準化每個成分
    ingredients = []
    for part in parts:
        normalized = normalize_ingredient(part)
        if normalized and normalized not in ingredients:
            ingredients.append(normalized)

    return ingredients


def extract_primary_ingredient(ingredient_str: str) -> str:
    """提取主要成分（第一個成分）

    Args:
        ingredient_str: 主成分略述欄位原始值

    Returns:
        主要成分名稱（標準化後）
    """
    ingredients = extract_ingredients(ingredient_str)
    return ingredients[0] if ingredients else ""


def get_all_synonyms(ingredient_str: str) -> List[Tuple[str, List[str]]]:
    """提取成分及其所有同義詞

    從括號中的 EQ TO 提取同義詞，並嘗試日語→英語翻譯

    Args:
        ingredient_str: 主成分略述欄位原始值

    Returns:
        [(主名稱, [同義詞列表]), ...]
    """
    if not ingredient_str:
        return []

    # 統一分隔符號
    ingredient_str = ingredient_str.replace(";;", ";").replace("；", ";")
    parts = ingredient_str.split(";")

    results = []
    for part in parts:
        part = part.strip()
        if not part:
            continue

        # 統一括號
        part = part.replace("（", "(").replace("）", ")")

        # 提取主名稱（括號前的部分）
        main_match = re.match(r"^([^(]+)", part)
        if not main_match:
            continue

        main_name = main_match.group(1).strip()
        main_name_upper = main_name.upper()
        main_name_upper = re.sub(r"\s+", " ", main_name_upper)

        # 提取所有 EQ TO 同義詞
        synonyms = []
        eq_matches = re.findall(r"EQ TO\s+([^)]+)", part, re.IGNORECASE)
        for match in eq_matches:
            syn = match.strip().upper()
            syn = re.sub(r"\s+", " ", syn)
            # 清理可能的尾部括號內容
            syn = re.sub(r"\s*\(.*$", "", syn)
            if syn and syn != main_name_upper:
                synonyms.append(syn)

        # 嘗試日語→英語翻譯（如果主名稱包含日語字符）
        if re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', main_name):
            english_name = translate_japanese_to_english(main_name)
            if english_name != main_name.upper() and english_name not in synonyms:
                synonyms.insert(0, english_name)  # 英語名優先

        results.append((main_name_upper, synonyms))

    return results
