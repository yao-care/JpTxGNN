"""Test normalizer module"""

import pytest
from jptxgnn.mapping.normalizer import (
    normalize_ingredient,
    extract_ingredients,
    get_all_synonyms,
    translate_japanese_to_english,
    JAPANESE_DRUG_DICT,
)


class TestNormalizeIngredient:
    """Test normalize_ingredient function"""

    def test_empty_string(self):
        assert normalize_ingredient("") == ""

    def test_simple_name(self):
        assert normalize_ingredient("aspirin") == "ASPIRIN"

    def test_removes_parentheses(self):
        assert normalize_ingredient("FAMOTIDINE (EQ TO GASTER)") == "FAMOTIDINE"

    def test_normalizes_whitespace(self):
        assert normalize_ingredient("  METFORMIN   HCL  ") == "METFORMIN HCL"

    def test_fullwidth_parentheses(self):
        assert normalize_ingredient("アスピリン（解熱剤）") == "アスピリン"


class TestExtractIngredients:
    """Test extract_ingredients function"""

    def test_empty_string(self):
        assert extract_ingredients("") == []

    def test_single_ingredient(self):
        result = extract_ingredients("ASPIRIN")
        assert result == ["ASPIRIN"]

    def test_multiple_semicolon(self):
        result = extract_ingredients("ASPIRIN;CAFFEINE")
        assert result == ["ASPIRIN", "CAFFEINE"]

    def test_double_semicolon(self):
        result = extract_ingredients("ASPIRIN;;CAFFEINE")
        assert result == ["ASPIRIN", "CAFFEINE"]

    def test_removes_duplicates(self):
        result = extract_ingredients("ASPIRIN;ASPIRIN")
        assert result == ["ASPIRIN"]


class TestTranslateJapaneseToEnglish:
    """Test translate_japanese_to_english function"""

    def test_known_drug_famotidine(self):
        assert translate_japanese_to_english("ファモチジン") == "FAMOTIDINE"

    def test_known_drug_aspirin(self):
        assert translate_japanese_to_english("アスピリン") == "ASPIRIN"

    def test_known_drug_metformin(self):
        assert translate_japanese_to_english("メトホルミン") == "METFORMIN"

    def test_with_dosage_suffix(self):
        # Should extract base name and translate
        result = translate_japanese_to_english("ファモチジン散２％")
        assert result == "FAMOTIDINE"

    def test_unknown_drug(self):
        # Unknown drugs return uppercase original
        result = translate_japanese_to_english("テスト薬")
        assert result == "テスト薬".upper()

    def test_empty_string(self):
        assert translate_japanese_to_english("") == ""


class TestGetAllSynonyms:
    """Test get_all_synonyms function"""

    def test_empty_string(self):
        assert get_all_synonyms("") == []

    def test_simple_name(self):
        result = get_all_synonyms("ASPIRIN")
        assert len(result) == 1
        assert result[0][0] == "ASPIRIN"

    def test_with_eq_to(self):
        result = get_all_synonyms("FAMOTIDINE (EQ TO GASTER)")
        assert len(result) == 1
        assert result[0][0] == "FAMOTIDINE"
        assert "GASTER" in result[0][1]

    def test_japanese_name_adds_english_synonym(self):
        result = get_all_synonyms("ファモチジン")
        assert len(result) == 1
        # Should have FAMOTIDINE as synonym
        assert "FAMOTIDINE" in result[0][1]

    def test_multiple_ingredients(self):
        result = get_all_synonyms("ASPIRIN;CAFFEINE")
        assert len(result) == 2


class TestJapaneseDrugDict:
    """Test JAPANESE_DRUG_DICT coverage"""

    def test_dict_not_empty(self):
        assert len(JAPANESE_DRUG_DICT) > 0

    def test_common_drugs_present(self):
        common_drugs = [
            "アスピリン",
            "ファモチジン",
            "メトホルミン",
            "アムロジピン",
            "オメプラゾール",
        ]
        for drug in common_drugs:
            assert drug in JAPANESE_DRUG_DICT, f"{drug} should be in dictionary"

    def test_all_values_uppercase(self):
        for jp_name, en_name in JAPANESE_DRUG_DICT.items():
            assert en_name == en_name.upper(), f"{en_name} should be uppercase"
