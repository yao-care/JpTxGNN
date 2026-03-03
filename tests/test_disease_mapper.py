"""Test disease_mapper module"""

import pytest
import pandas as pd

from jptxgnn.mapping.disease_mapper import (
    DISEASE_DICT,
    translate_indication,
    extract_indications,
    get_indication_mapping_stats,
)


class TestDiseaseDict:
    """Test DISEASE_DICT coverage"""

    def test_dict_not_empty(self):
        assert len(DISEASE_DICT) > 0

    def test_has_minimum_entries(self):
        # Should have at least 150 entries as per SOP
        assert len(DISEASE_DICT) >= 150

    def test_common_diseases_present(self):
        common_diseases = [
            "高血圧",
            "糖尿病",
            "喘息",
            "胃潰瘍",
            "うつ病",
        ]
        for disease in common_diseases:
            assert disease in DISEASE_DICT, f"{disease} should be in dictionary"

    def test_all_values_are_strings(self):
        for jp_name, en_name in DISEASE_DICT.items():
            assert isinstance(en_name, str), f"{en_name} should be a string"
            assert len(en_name) > 0, f"Value for {jp_name} should not be empty"

    def test_cardiovascular_coverage(self):
        cardio_terms = ["高血圧", "心筋梗塞", "狭心症", "不整脈"]
        for term in cardio_terms:
            assert term in DISEASE_DICT

    def test_respiratory_coverage(self):
        resp_terms = ["喘息", "気管支炎", "肺炎"]
        for term in resp_terms:
            assert term in DISEASE_DICT

    def test_digestive_coverage(self):
        digest_terms = ["胃炎", "胃潰瘍", "肝炎"]
        for term in digest_terms:
            assert term in DISEASE_DICT


class TestTranslateIndication:
    """Test translate_indication function"""

    def test_known_disease(self):
        result = translate_indication("高血圧")
        assert "HYPERTENSION" in result

    def test_unknown_returns_empty_list(self):
        result = translate_indication("未知の疾患XYZ")
        assert result == []

    def test_partial_match(self):
        # Should find match even with extra text
        result = translate_indication("高血圧症の治療")
        assert "HYPERTENSION" in result

    def test_empty_string(self):
        result = translate_indication("")
        assert result == []


class TestExtractIndications:
    """Test extract_indications function"""

    def test_empty_string(self):
        assert extract_indications("") == []

    def test_single_indication(self):
        result = extract_indications("高血圧")
        assert len(result) >= 1

    def test_comma_separated(self):
        result = extract_indications("高血圧、糖尿病")
        assert len(result) >= 2

    def test_period_separated(self):
        result = extract_indications("高血圧。糖尿病")
        assert len(result) >= 1  # May or may not split on period


class TestGetIndicationMappingStats:
    """Test get_indication_mapping_stats function"""

    def test_with_data(self):
        df = pd.DataFrame({
            "extracted_indication": ["高血圧", "糖尿病", "未知"],
            "disease_id": ["D001", "D002", None],
            "disease_name": ["hypertension", "diabetes", None],
        })
        stats = get_indication_mapping_stats(df)
        assert stats["total_indications"] == 3
        assert stats["mapped_indications"] == 2
        assert stats["mapping_rate"] == pytest.approx(2/3)

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        stats = get_indication_mapping_stats(df)
        assert stats["total_indications"] == 0
        assert stats["mapping_rate"] == 0

    def test_missing_columns(self):
        df = pd.DataFrame({"other_col": [1, 2, 3]})
        stats = get_indication_mapping_stats(df)
        assert stats["total_indications"] == 0
