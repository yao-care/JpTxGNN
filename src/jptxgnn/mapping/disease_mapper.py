"""疾病映射模組 - 日本語適応症から TxGNN 疾病オントロジーへのマッピング"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd


# 日本語 → 英語 疾病対照表 (約200項目)
DISEASE_DICT = {
    # === 心血管系統 (20 個) ===
    "高血圧": "hypertension",
    "高血圧症": "hypertension",
    "低血圧": "hypotension",
    "低血圧症": "hypotension",
    "心臓病": "heart disease",
    "心筋梗塞": "myocardial infarction",
    "狭心症": "angina",
    "不整脈": "arrhythmia",
    "心房細動": "atrial fibrillation",
    "動悸": "palpitation",
    "心不全": "heart failure",
    "うっ血性心不全": "congestive heart failure",
    "動脈硬化": "atherosclerosis",
    "動脈硬化症": "atherosclerosis",
    "静脈瘤": "varicose veins",
    "血栓症": "thrombosis",
    "深部静脈血栓症": "deep vein thrombosis",
    "脳卒中": "stroke",
    "脳梗塞": "cerebral infarction",
    "脳出血": "cerebral hemorrhage",

    # === 呼吸系統 (15 個) ===
    "喘息": "asthma",
    "気管支喘息": "bronchial asthma",
    "気管支炎": "bronchitis",
    "慢性気管支炎": "chronic bronchitis",
    "肺炎": "pneumonia",
    "肺結核": "tuberculosis",
    "結核": "tuberculosis",
    "咳嗽": "cough",
    "風邪": "common cold",
    "感冒": "common cold",
    "インフルエンザ": "influenza",
    "鼻炎": "rhinitis",
    "アレルギー性鼻炎": "allergic rhinitis",
    "副鼻腔炎": "sinusitis",
    "呼吸困難": "dyspnea",
    "肺気腫": "emphysema",
    "慢性閉塞性肺疾患": "chronic obstructive pulmonary disease",
    "COPD": "chronic obstructive pulmonary disease",

    # === 消化系統 (20 個) ===
    "胃炎": "gastritis",
    "急性胃炎": "acute gastritis",
    "慢性胃炎": "chronic gastritis",
    "胃潰瘍": "gastric ulcer",
    "十二指腸潰瘍": "duodenal ulcer",
    "消化性潰瘍": "peptic ulcer",
    "消化不良": "dyspepsia",
    "下痢": "diarrhea",
    "便秘": "constipation",
    "腸炎": "enteritis",
    "大腸炎": "colitis",
    "潰瘍性大腸炎": "ulcerative colitis",
    "クローン病": "crohn disease",
    "過敏性腸症候群": "irritable bowel syndrome",
    "肝炎": "hepatitis",
    "肝硬変": "cirrhosis",
    "胆石症": "gallstone",
    "胆嚢炎": "cholecystitis",
    "膵炎": "pancreatitis",
    "悪心": "nausea",
    "嘔吐": "vomiting",
    "胃酸過多": "hyperacidity",
    "逆流性食道炎": "gastroesophageal reflux disease",

    # === 神経系統 (15 個) ===
    "てんかん": "epilepsy",
    "癲癇": "epilepsy",
    "頭痛": "headache",
    "片頭痛": "migraine",
    "偏頭痛": "migraine",
    "めまい": "vertigo",
    "眩暈": "dizziness",
    "不眠症": "insomnia",
    "睡眠障害": "sleep disorder",
    "神経痛": "neuralgia",
    "坐骨神経痛": "sciatica",
    "パーキンソン病": "parkinson disease",
    "アルツハイマー病": "alzheimer disease",
    "認知症": "dementia",
    "多発性硬化症": "multiple sclerosis",
    "髄膜炎": "meningitis",
    "末梢神経障害": "peripheral neuropathy",

    # === 精神疾病 (12 個) ===
    "うつ病": "depression",
    "鬱病": "depression",
    "大うつ病": "major depressive disorder",
    "不安症": "anxiety disorder",
    "不安障害": "anxiety disorder",
    "全般性不安障害": "generalized anxiety disorder",
    "双極性障害": "bipolar disorder",
    "躁うつ病": "bipolar disorder",
    "統合失調症": "schizophrenia",
    "パニック障害": "panic disorder",
    "強迫性障害": "obsessive-compulsive disorder",
    "心的外傷後ストレス障害": "post-traumatic stress disorder",
    "PTSD": "post-traumatic stress disorder",

    # === 内分泌系統 (15 個) ===
    "糖尿病": "diabetes",
    "1型糖尿病": "type 1 diabetes",
    "2型糖尿病": "type 2 diabetes",
    "甲状腺機能亢進症": "hyperthyroidism",
    "バセドウ病": "graves disease",
    "甲状腺機能低下症": "hypothyroidism",
    "橋本病": "hashimoto thyroiditis",
    "肥満": "obesity",
    "肥満症": "obesity",
    "痛風": "gout",
    "高尿酸血症": "hyperuricemia",
    "高脂血症": "hyperlipidemia",
    "脂質異常症": "dyslipidemia",
    "高コレステロール血症": "hypercholesterolemia",
    "メタボリックシンドローム": "metabolic syndrome",
    "クッシング症候群": "cushing syndrome",

    # === 肌肉骨骼系統 (15 個) ===
    "関節炎": "arthritis",
    "関節リウマチ": "rheumatoid arthritis",
    "変形性関節症": "osteoarthritis",
    "骨粗鬆症": "osteoporosis",
    "骨折": "fracture",
    "筋肉痛": "myalgia",
    "腰痛": "back pain",
    "腰痛症": "back pain",
    "背部痛": "back pain",
    "肩こり": "shoulder pain",
    "頸部痛": "neck pain",
    "捻挫": "sprain",
    "打撲": "contusion",
    "腱鞘炎": "tendinitis",
    "線維筋痛症": "fibromyalgia",

    # === 皮膚疾病 (15 個) ===
    "湿疹": "eczema",
    "アトピー性皮膚炎": "atopic dermatitis",
    "蕁麻疹": "urticaria",
    "乾癬": "psoriasis",
    "皮膚炎": "dermatitis",
    "接触性皮膚炎": "contact dermatitis",
    "水虫": "tinea pedis",
    "白癬": "tinea",
    "爪白癬": "onychomycosis",
    "にきび": "acne",
    "ざ瘡": "acne",
    "疥癬": "scabies",
    "帯状疱疹": "herpes zoster",
    "皮膚そう痒症": "pruritus",
    "熱傷": "burn",
    "やけど": "burn",

    # === 泌尿系統 (12 個) ===
    "尿道炎": "urethritis",
    "膀胱炎": "cystitis",
    "腎炎": "nephritis",
    "腎盂腎炎": "pyelonephritis",
    "腎結石": "kidney stone",
    "尿路結石": "urolithiasis",
    "前立腺肥大症": "prostatic hyperplasia",
    "前立腺炎": "prostatitis",
    "尿失禁": "urinary incontinence",
    "頻尿": "urinary frequency",
    "過活動膀胱": "overactive bladder",
    "慢性腎臓病": "chronic kidney disease",

    # === 眼科 (8 個) ===
    "結膜炎": "conjunctivitis",
    "緑内障": "glaucoma",
    "白内障": "cataract",
    "ドライアイ": "dry eye",
    "乾燥性角結膜炎": "dry eye",
    "近視": "myopia",
    "遠視": "hyperopia",
    "加齢黄斑変性": "age-related macular degeneration",

    # === 耳鼻喉 (8 個) ===
    "中耳炎": "otitis media",
    "外耳炎": "otitis externa",
    "耳鳴り": "tinnitus",
    "難聴": "hearing loss",
    "咽頭炎": "pharyngitis",
    "扁桃炎": "tonsillitis",
    "喉頭炎": "laryngitis",
    "メニエール病": "meniere disease",

    # === 感染症 (15 個) ===
    "細菌感染": "bacterial infection",
    "細菌感染症": "bacterial infection",
    "ウイルス感染": "viral infection",
    "ウイルス感染症": "viral infection",
    "真菌感染": "fungal infection",
    "真菌感染症": "fungal infection",
    "寄生虫感染": "parasitic infection",
    "敗血症": "sepsis",
    "蜂窩織炎": "cellulitis",
    "ヘルペス": "herpes",
    "単純ヘルペス": "herpes simplex",
    "HIV感染症": "HIV infection",
    "AIDS": "acquired immunodeficiency syndrome",
    "マラリア": "malaria",
    "新型コロナウイルス感染症": "COVID-19",

    # === 過敏 (8 個) ===
    "アレルギー": "allergy",
    "アレルギー反応": "allergic reaction",
    "花粉症": "hay fever",
    "食物アレルギー": "food allergy",
    "薬物アレルギー": "drug allergy",
    "アナフィラキシー": "anaphylaxis",
    "血管性浮腫": "angioedema",
    "喘息発作": "asthma attack",

    # === 婦科 (12 個) ===
    "月経不順": "menstrual disorder",
    "月経困難症": "dysmenorrhea",
    "生理痛": "dysmenorrhea",
    "更年期障害": "menopause syndrome",
    "子宮内膜症": "endometriosis",
    "膣炎": "vaginitis",
    "子宮筋腫": "uterine fibroid",
    "多嚢胞性卵巣症候群": "polycystic ovary syndrome",
    "乳腺炎": "mastitis",
    "骨盤内炎症性疾患": "pelvic inflammatory disease",
    "妊娠悪阻": "hyperemesis gravidarum",
    "妊娠高血圧症候群": "preeclampsia",

    # === 腫瘍/癌症 (15 個) ===
    "がん": "cancer",
    "癌": "cancer",
    "悪性腫瘍": "malignant tumor",
    "良性腫瘍": "benign tumor",
    "腫瘍": "tumor",
    "白血病": "leukemia",
    "リンパ腫": "lymphoma",
    "肺がん": "lung cancer",
    "乳がん": "breast cancer",
    "胃がん": "gastric cancer",
    "大腸がん": "colorectal cancer",
    "肝臓がん": "liver cancer",
    "前立腺がん": "prostate cancer",
    "膵臓がん": "pancreatic cancer",
    "骨髄腫": "myeloma",

    # === 一般症狀 (20 個) ===
    "発熱": "fever",
    "熱": "fever",
    "疼痛": "pain",
    "痛み": "pain",
    "炎症": "inflammation",
    "浮腫": "edema",
    "むくみ": "edema",
    "倦怠感": "fatigue",
    "疲労": "fatigue",
    "貧血": "anemia",
    "出血": "bleeding",
    "痙攣": "spasm",
    "けいれん": "seizure",
    "脱水": "dehydration",
    "ショック": "shock",
    "意識障害": "altered consciousness",
    "食欲不振": "anorexia",
    "体重減少": "weight loss",
    "かゆみ": "itching",
    "発疹": "rash",
}


def load_disease_vocab(filepath: Optional[Path] = None) -> pd.DataFrame:
    """TxGNN 疾病語彙表を読み込む"""
    if filepath is None:
        filepath = Path(__file__).parent.parent.parent.parent / "data" / "external" / "disease_vocab.csv"
    return pd.read_csv(filepath)


def build_disease_index(disease_df: pd.DataFrame) -> Dict[str, Tuple[str, str]]:
    """疾病名インデックスを構築（キーワード -> (disease_id, disease_name)）"""
    index = {}

    for _, row in disease_df.iterrows():
        disease_id = row["disease_id"]
        disease_name = row["disease_name"]
        name_upper = row["disease_name_upper"]

        # 完全名
        index[name_upper] = (disease_id, disease_name)

        # キーワード抽出（スペースとカンマで分割）
        keywords = re.split(r"[,\s\-]+", name_upper)
        for kw in keywords:
            kw = kw.strip()
            if len(kw) > 3 and kw not in index:
                index[kw] = (disease_id, disease_name)

    return index


def extract_indications(indication_str: str) -> List[str]:
    """適応症テキストから個別の適応症を抽出

    日本語の一般的な区切り文字を使用
    """
    if not indication_str:
        return []

    text = indication_str.strip()

    # 句点と読点で分割
    parts = re.split(r"[。；・]", text)

    indications = []
    for part in parts:
        # 読点とカンマでさらに分割
        sub_parts = re.split(r"[、，,]", part)
        for sub in sub_parts:
            sub = sub.strip()
            # 一般的な接頭辞を削除
            sub = re.sub(r"^(における|による|の治療|治療|緩和|予防|改善)", "", sub)
            # 一般的な接尾辞を削除
            sub = re.sub(r"(等の症状|の治療|に伴う|による|における)$", "", sub)
            sub = sub.strip()
            if sub and len(sub) >= 2:
                indications.append(sub)

    return indications


def translate_indication(indication: str) -> List[str]:
    """日本語の適応症を英語キーワードに翻訳"""
    keywords = []

    for jp_term, en_term in DISEASE_DICT.items():
        if jp_term in indication:
            keywords.append(en_term.upper())

    return keywords


def map_indication_to_disease(
    indication: str,
    disease_index: Dict[str, Tuple[str, str]],
) -> List[Tuple[str, str, float]]:
    """単一の適応症を TxGNN 疾病にマッピング

    Returns:
        [(disease_id, disease_name, confidence), ...]
    """
    results = []

    # 英語キーワードに翻訳
    keywords = translate_indication(indication)

    for kw in keywords:
        # 完全一致
        if kw in disease_index:
            disease_id, disease_name = disease_index[kw]
            results.append((disease_id, disease_name, 1.0))
            continue

        # 部分一致
        for index_kw, (disease_id, disease_name) in disease_index.items():
            if kw in index_kw or index_kw in kw:
                results.append((disease_id, disease_name, 0.8))

    # 重複除去と信頼度でソート
    seen = set()
    unique_results = []
    for disease_id, disease_name, conf in sorted(results, key=lambda x: -x[2]):
        if disease_id not in seen:
            seen.add(disease_id)
            unique_results.append((disease_id, disease_name, conf))

    return unique_results[:5]


def map_fda_indications_to_diseases(
    fda_df: pd.DataFrame,
    disease_df: Optional[pd.DataFrame] = None,
    indication_field: str = "効能・効果",
    license_field: str = "承認番号",
    brand_field: str = "販売名",
) -> pd.DataFrame:
    """PMDA 薬品の適応症を TxGNN 疾病にマッピング"""
    if disease_df is None:
        disease_df = load_disease_vocab()

    disease_index = build_disease_index(disease_df)

    results = []

    for _, row in fda_df.iterrows():
        indication_str = row.get(indication_field, "")
        if not indication_str:
            continue

        # 個別適応症を抽出
        indications = extract_indications(indication_str)

        for ind in indications:
            # 翻訳とマッピング
            matches = map_indication_to_disease(ind, disease_index)

            if matches:
                for disease_id, disease_name, confidence in matches:
                    results.append({
                        "license_id": row.get(license_field, ""),
                        "brand_name": row.get(brand_field, ""),
                        "original_indication": indication_str[:100],
                        "extracted_indication": ind,
                        "disease_id": disease_id,
                        "disease_name": disease_name,
                        "confidence": confidence,
                    })
            else:
                results.append({
                    "license_id": row.get(license_field, ""),
                    "brand_name": row.get(brand_field, ""),
                    "original_indication": indication_str[:100],
                    "extracted_indication": ind,
                    "disease_id": None,
                    "disease_name": None,
                    "confidence": 0,
                })

    return pd.DataFrame(results)


def get_indication_mapping_stats(mapping_df: pd.DataFrame) -> dict:
    """適応症マッピングの統計を計算"""
    total = len(mapping_df)

    # Handle empty DataFrames
    if total == 0 or "disease_id" not in mapping_df.columns:
        return {
            "total_indications": 0,
            "mapped_indications": 0,
            "mapping_rate": 0,
            "unique_indications": 0,
            "unique_diseases": 0,
        }

    mapped = mapping_df["disease_id"].notna().sum()
    unique_indications = mapping_df["extracted_indication"].nunique()
    unique_diseases = mapping_df[mapping_df["disease_id"].notna()]["disease_id"].nunique()

    return {
        "total_indications": total,
        "mapped_indications": int(mapped),
        "mapping_rate": mapped / total if total > 0 else 0,
        "unique_indications": unique_indications,
        "unique_diseases": unique_diseases,
    }
