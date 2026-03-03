#!/usr/bin/env python3
"""
ニュース監視用キーワードリストを生成

既存データから抽出：
- 薬物名（英語 + 日本語商品名）
- 元の適応症（日本語）
- 予測適応症（英語）

出力：data/news/keywords.json
"""

import json
import re
from datetime import datetime
from pathlib import Path

# プロジェクトルートディレクトリ
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DATA_DIR = PROJECT_ROOT / "docs" / "data"


def load_json(path: Path) -> dict | list:
    """JSONファイルを読み込む"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_japanese_terms(text: str) -> list[str]:
    """日本語テキストから独立した語彙を抽出（読点、句点などで分割）"""
    if not text:
        return []
    # 区切り文字：読点、句点、カンマ、セミコロン、スラッシュ
    terms = re.split(r"[、。，；,;/・]", text)
    # 空白を削除し、空文字列をフィルタリング
    return [t.strip() for t in terms if t.strip() and len(t.strip()) >= 2]


def get_brand_names_from_fda(fda_data: list, drug_name: str) -> list[str]:
    """FDAデータから薬物の日本語商品名を取得"""
    brand_names = set()
    drug_name_lower = drug_name.lower()

    for item in fda_data:
        # 成分が一致するかチェック
        ingredient = item.get("成分名", "") or item.get("ingredient", "")
        if drug_name_lower in ingredient.lower():
            japanese_name = item.get("品名", "") or item.get("name", "")
            if japanese_name:
                # ブランド名部分のみを取得（数字や単位の前）
                # 例：「ガスター散２％」から「ガスター」
                match = re.match(r"^([^\s\d０-９（(]+)", japanese_name)
                if match:
                    brand = match.group(1).strip()
                    if len(brand) >= 2:
                        brand_names.add(brand)

    return list(brand_names)[:5]  # 最大5つの商品名


def load_synonyms(path: Path) -> dict:
    """日本語同義語対照表を読み込む"""
    if not path.exists():
        return {"indication_synonyms": {}, "drug_synonyms": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


GENERIC_KEYWORD_PATTERNS = {
    "_generic_cancer": [
        "cancer", "carcinoma", "tumor", "tumour", "neoplasm", "malignant",
        "leukemia", "lymphoma", "melanoma", "sarcoma", "myeloma"
    ],
    "_cardiovascular": [
        "cardiovascular", "atherosclerosis", "arteriosclerosis",
        "coronary", "vascular disease"
    ],
    "_heart_disease": [
        "heart disease", "heart failure", "cardiac", "myocardial",
        "arrhythmia", "angina", "cardiomyopathy"
    ],
    "stroke": ["stroke", "ischemic stroke", "cerebrovascular"],
    "herpes zoster": ["herpes", "zoster", "varicella"],
    "dementia": ["dementia", "alzheimer", "cognitive impairment"],
    "pancreatic cancer": ["pancreatic cancer", "pancreatic carcinoma", "pancreatic neoplasm"],
    "menopause": ["menopause", "postmenopaus", "estrogen-receptor", "hormone-resistant"],
}


def build_indication_index(search_index: dict, synonyms: dict) -> dict:
    """適応症インデックスを構築、各適応症が関連する薬物を記録"""
    indication_map = {}
    indication_synonyms = synonyms.get("indication_synonyms", {})

    # まず同義語エントリを追加（_generic_cancerなどの汎用キーワードを含む）
    for en_name, ja_list in indication_synonyms.items():
        key = en_name.lower()
        if key not in indication_map:
            indication_map[key] = {
                "name": en_name.lstrip("_"),  # 先頭のアンダースコアを削除
                "keywords_en": [en_name] if not en_name.startswith("_") else [],
                "keywords_ja": ja_list.copy(),
                "related_drugs": []
            }
            # 各日本語同義語にもインデックスを作成
            for ja in ja_list:
                ja_key = ja.lower()
                if ja_key not in indication_map:
                    indication_map[ja_key] = {
                        "name": ja,
                        "keywords_en": [en_name] if not en_name.startswith("_") else [],
                        "keywords_ja": [ja],
                        "related_drugs": []
                    }

    for drug in search_index.get("drugs", []):
        drug_slug = drug.get("slug", "")

        # 予測適応症を処理
        for ind in drug.get("indications", []):
            ind_name = ind.get("name", "").lower()
            if ind_name:
                if ind_name not in indication_map:
                    # 同義語を検索
                    ja_synonyms = indication_synonyms.get(ind.get("name", ""), [])
                    indication_map[ind_name] = {
                        "name": ind.get("name", ""),
                        "keywords_en": [ind.get("name", "")],
                        "keywords_ja": ja_synonyms.copy(),
                        "related_drugs": []
                    }
                # 日本語同義語にも独立インデックスを作成
                for ja in indication_synonyms.get(ind.get("name", ""), []):
                    ja_key = ja.lower()
                    if ja_key not in indication_map:
                        indication_map[ja_key] = {
                            "name": ja,
                            "keywords_en": [ind.get("name", "")],
                            "keywords_ja": [ja],
                            "related_drugs": []
                        }
                    if drug_slug not in indication_map[ja_key]["related_drugs"]:
                        indication_map[ja_key]["related_drugs"].append(drug_slug)

                if drug_slug not in indication_map[ind_name]["related_drugs"]:
                    indication_map[ind_name]["related_drugs"].append(drug_slug)

        # 元の適応症（日本語）から中国語キーワードを追加
        original = drug.get("original", "")
        if original:
            ja_terms = extract_japanese_terms(original)
            for term in ja_terms:
                term_key = term.lower()
                if term_key not in indication_map:
                    indication_map[term_key] = {
                        "name": term,
                        "keywords_en": [],
                        "keywords_ja": [term],
                        "related_drugs": []
                    }
                else:
                    if term not in indication_map[term_key]["keywords_ja"]:
                        indication_map[term_key]["keywords_ja"].append(term)

                if drug_slug not in indication_map[term_key]["related_drugs"]:
                    indication_map[term_key]["related_drugs"].append(drug_slug)

    # 汎用キーワードを関連適応症の薬物とリンク
    for generic_key, patterns in GENERIC_KEYWORD_PATTERNS.items():
        generic_key_lower = generic_key.lower()
        if generic_key_lower not in indication_map:
            continue

        # パターンに一致するすべての薬物を検索
        for drug in search_index.get("drugs", []):
            drug_slug = drug.get("slug", "")
            for ind in drug.get("indications", []):
                ind_name = ind.get("name", "").lower()
                # パターンに一致するかチェック
                for pattern in patterns:
                    if pattern.lower() in ind_name:
                        if drug_slug not in indication_map[generic_key_lower]["related_drugs"]:
                            indication_map[generic_key_lower]["related_drugs"].append(drug_slug)
                        break

        # 同時にこの汎用キーワードの日本語同義語エントリも更新
        ja_list = indication_synonyms.get(generic_key, [])
        for ja in ja_list:
            ja_key = ja.lower()
            if ja_key in indication_map:
                for drug_slug in indication_map[generic_key_lower]["related_drugs"]:
                    if drug_slug not in indication_map[ja_key]["related_drugs"]:
                        indication_map[ja_key]["related_drugs"].append(drug_slug)

    return indication_map


def main():
    print("データファイルを読み込み中...")

    # データを読み込む
    search_index_path = DOCS_DATA_DIR / "search-index.json"
    fda_data_path = DATA_DIR / "raw" / "jp_fda_drugs.json"
    synonyms_path = DATA_DIR / "news" / "synonyms.json"

    if not search_index_path.exists():
        print(f"エラー: {search_index_path} が見つかりません")
        return

    search_index = load_json(search_index_path)

    fda_data = []
    if fda_data_path.exists():
        fda_data = load_json(fda_data_path)
        print(f"  - jp_fda_drugs.json: {len(fda_data)} 件のFDAデータ")
    else:
        print(f"  - jp_fda_drugs.json: ファイルが見つかりません（スキップ）")

    synonyms = load_synonyms(synonyms_path)

    drug_count = len(search_index.get("drugs", []))
    print(f"  - search-index.json: {drug_count} 薬物")
    print(f"  - synonyms.json: {len(synonyms.get('indication_synonyms', {}))} 適応症同義語")

    # 薬物キーワードリストを構築
    drugs_keywords = []

    for drug in search_index.get("drugs", []):
        drug_name = drug.get("name", "")
        drug_slug = drug.get("slug", "")

        # 英語キーワード
        keywords_en = [drug_slug]

        # ブランド名を追加（search-indexから）
        for brand in drug.get("brands", []):
            if brand.lower() not in keywords_en:
                keywords_en.append(brand.lower())

        # 日本語商品名（FDAデータから）
        keywords_ja = []
        if fda_data:
            keywords_ja = get_brand_names_from_fda(fda_data, drug_slug)

        # 薬物名自体を日本語キーワードに追加
        if drug_name and drug_name not in keywords_ja:
            # 商品名の基本部分を抽出
            match = re.match(r"^([^\s\d０-９（(]+)", drug_name)
            if match:
                base_name = match.group(1).strip()
                if base_name and base_name not in keywords_ja:
                    keywords_ja.append(base_name)

        drugs_keywords.append({
            "slug": drug_slug,
            "name": drug_name,
            "keywords": {
                "en": keywords_en,
                "ja": keywords_ja
            },
            "url": f"/drugs/{drug_slug}/"
        })

    print(f"\n薬物キーワードを処理: {len(drugs_keywords)} 個の薬物")

    # 適応症キーワードリストを構築
    indication_map = build_indication_index(search_index, synonyms)

    # リスト形式に変換（関連薬物があるキーワードのみ保持）
    indications_keywords = []
    for key, data in indication_map.items():
        # 関連薬物がある適応症のみ保持
        if data["related_drugs"]:
            indications_keywords.append({
                "name": data["name"],
                "keywords": {
                    "en": data["keywords_en"],
                    "ja": data["keywords_ja"]
                },
                "related_drugs": data["related_drugs"]
            })

    print(f"適応症キーワードを処理: {len(indications_keywords)} 個の適応症")

    # 出力
    output = {
        "generated": datetime.now().strftime("%Y-%m-%d"),
        "drug_count": len(drugs_keywords),
        "indication_count": len(indications_keywords),
        "drugs": drugs_keywords,
        "indications": indications_keywords
    }

    output_path = DATA_DIR / "news" / "keywords.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n出力: {output_path}")
    print(f"  - 薬物キーワード: {len(drugs_keywords)} 個")
    print(f"  - 適応症キーワード: {len(indications_keywords)} 個")


if __name__ == "__main__":
    main()
