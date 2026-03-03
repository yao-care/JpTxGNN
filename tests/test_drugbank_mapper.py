"""Test drugbank_mapper module"""

import pytest
import pandas as pd
from pathlib import Path

from jptxgnn.mapping.drugbank_mapper import (
    load_drugbank_vocab,
    build_name_index,
    map_ingredient_to_drugbank,
    map_fda_drugs_to_drugbank,
    get_mapping_stats,
)


class TestBuildNameIndex:
    """Test build_name_index function"""

    def test_creates_index(self):
        df = pd.DataFrame({
            "drug_name_upper": ["ASPIRIN", "METFORMIN"],
            "drugbank_id": ["DB00945", "DB00331"],
        })
        index = build_name_index(df)
        assert "ASPIRIN" in index
        assert index["ASPIRIN"] == "DB00945"

    def test_handles_salt_suffixes(self):
        df = pd.DataFrame({
            "drug_name_upper": ["METFORMIN HCL"],
            "drugbank_id": ["DB00331"],
        })
        index = build_name_index(df)
        # Should have both full name and base name
        assert "METFORMIN HCL" in index
        assert "METFORMIN" in index

    def test_includes_synonyms(self):
        df = pd.DataFrame({
            "drug_name_upper": ["ACETAMINOPHEN"],
            "drugbank_id": ["DB00316"],
        })
        index = build_name_index(df)
        # PARACETAMOL should map to ACETAMINOPHEN
        assert "PARACETAMOL" in index
        assert index["PARACETAMOL"] == "DB00316"


class TestMapIngredientToDrugbank:
    """Test map_ingredient_to_drugbank function"""

    @pytest.fixture
    def sample_index(self):
        return {
            "ASPIRIN": "DB00945",
            "METFORMIN": "DB00331",
            "METFORMIN HCL": "DB00331",
            "FAMOTIDINE": "DB00927",
        }

    def test_exact_match(self, sample_index):
        result = map_ingredient_to_drugbank("ASPIRIN", sample_index)
        assert result == "DB00945"

    def test_case_insensitive(self, sample_index):
        result = map_ingredient_to_drugbank("aspirin", sample_index)
        assert result == "DB00945"

    def test_removes_salt_suffix(self, sample_index):
        result = map_ingredient_to_drugbank("METFORMIN HYDROCHLORIDE", sample_index)
        assert result == "DB00331"

    def test_unknown_returns_none(self, sample_index):
        result = map_ingredient_to_drugbank("UNKNOWN_DRUG", sample_index)
        assert result is None

    def test_empty_string(self, sample_index):
        result = map_ingredient_to_drugbank("", sample_index)
        assert result is None


class TestMapFdaDrugsToDrugbank:
    """Test map_fda_drugs_to_drugbank function"""

    @pytest.fixture
    def sample_fda_df(self):
        return pd.DataFrame({
            "承認番号": ["A001", "A002"],
            "販売名": ["Drug A", "Drug B"],
            "有効成分": ["ASPIRIN", "UNKNOWN"],
        })

    @pytest.fixture
    def sample_drugbank_df(self):
        return pd.DataFrame({
            "drug_name_upper": ["ASPIRIN"],
            "drugbank_id": ["DB00945"],
        })

    def test_maps_known_drugs(self, sample_fda_df, sample_drugbank_df):
        result = map_fda_drugs_to_drugbank(
            sample_fda_df,
            sample_drugbank_df,
            ingredient_field="有効成分",
            license_field="承認番号",
            name_field="販売名",
        )
        assert len(result) == 2
        # ASPIRIN should be mapped
        aspirin_row = result[result["標準化成分"] == "ASPIRIN"].iloc[0]
        assert aspirin_row["drugbank_id"] == "DB00945"
        assert aspirin_row["映射成功"] == True

    def test_unknown_drugs_not_mapped(self, sample_fda_df, sample_drugbank_df):
        result = map_fda_drugs_to_drugbank(
            sample_fda_df,
            sample_drugbank_df,
            ingredient_field="有効成分",
            license_field="承認番号",
            name_field="販売名",
        )
        unknown_row = result[result["標準化成分"] == "UNKNOWN"].iloc[0]
        assert unknown_row["映射成功"] == False


class TestGetMappingStats:
    """Test get_mapping_stats function"""

    def test_calculates_stats(self):
        df = pd.DataFrame({
            "標準化成分": ["A", "B", "C"],
            "drugbank_id": ["DB001", None, "DB001"],
            "映射成功": [True, False, True],
        })
        stats = get_mapping_stats(df)
        assert stats["total_ingredients"] == 3
        assert stats["mapped_ingredients"] == 2
        assert stats["mapping_rate"] == pytest.approx(2/3)
        assert stats["unique_drugbank_ids"] == 1

    def test_empty_dataframe(self):
        df = pd.DataFrame({
            "標準化成分": pd.Series([], dtype=str),
            "drugbank_id": pd.Series([], dtype=str),
            "映射成功": pd.Series([], dtype=bool),
        })
        stats = get_mapping_stats(df)
        assert stats["total_ingredients"] == 0
        assert stats["mapping_rate"] == 0
