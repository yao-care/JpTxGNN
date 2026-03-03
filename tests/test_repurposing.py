"""Test repurposing prediction module"""

import pytest
import pandas as pd

from jptxgnn.predict.repurposing import (
    build_drug_indication_map,
    find_repurposing_candidates,
    generate_repurposing_report,
)


class TestBuildDrugIndicationMap:
    """Test build_drug_indication_map function"""

    def test_creates_mapping(self):
        df = pd.DataFrame({
            "x_name": ["aspirin", "aspirin", "metformin"],
            "y_name": ["headache", "fever", "diabetes"],
            "relation": ["indication", "indication", "indication"],
        })
        result = build_drug_indication_map(df)
        assert "ASPIRIN" in result
        assert "headache" in result["ASPIRIN"]
        assert "fever" in result["ASPIRIN"]

    def test_filters_indication_relations(self):
        df = pd.DataFrame({
            "x_name": ["aspirin", "aspirin"],
            "y_name": ["headache", "stomach"],
            "relation": ["indication", "contraindication"],
        })
        result = build_drug_indication_map(df)
        assert "headache" in result["ASPIRIN"]
        assert "stomach" not in result["ASPIRIN"]

    def test_includes_off_label(self):
        df = pd.DataFrame({
            "x_name": ["aspirin"],
            "y_name": ["heart disease"],
            "relation": ["off-label use"],
        })
        result = build_drug_indication_map(df)
        assert "heart disease" in result["ASPIRIN"]


class TestFindRepurposingCandidates:
    """Test find_repurposing_candidates function"""

    @pytest.fixture
    def sample_drug_mapping(self):
        return pd.DataFrame({
            "承認番号": ["A001", "A002"],
            "販売名": ["Drug A", "Drug B"],
            "標準化成分": ["ASPIRIN", "METFORMIN"],
            "同義詞": ["ASPIRIN", "METFORMIN"],
            "drugbank_id": ["DB00945", "DB00331"],
        })

    @pytest.fixture
    def sample_indication_mapping(self):
        return pd.DataFrame({
            "license_id": ["A001"],
            "disease_name": ["headache"],
        })

    @pytest.fixture
    def sample_relations(self):
        return pd.DataFrame({
            "x_name": ["aspirin", "aspirin", "metformin"],
            "y_name": ["headache", "fever", "diabetes"],
            "relation": ["indication", "indication", "indication"],
        })

    def test_finds_new_indications(
        self, sample_drug_mapping, sample_indication_mapping, sample_relations
    ):
        result = find_repurposing_candidates(
            sample_drug_mapping,
            sample_indication_mapping,
            sample_relations,
            license_field="承認番号",
            name_field="販売名",
        )
        # Should find fever as new indication for aspirin (headache is existing)
        assert len(result) > 0

    def test_empty_drug_mapping(self, sample_indication_mapping, sample_relations):
        empty_df = pd.DataFrame({
            "承認番号": [],
            "販売名": [],
            "標準化成分": [],
            "同義詞": [],
            "drugbank_id": [],
        })
        result = find_repurposing_candidates(
            empty_df,
            sample_indication_mapping,
            sample_relations,
            license_field="承認番号",
            name_field="販売名",
        )
        assert len(result) == 0


class TestGenerateRepurposingReport:
    """Test generate_repurposing_report function"""

    def test_with_candidates(self):
        df = pd.DataFrame({
            "承認番号": ["A001", "A001", "A002"],
            "藥物成分": ["ASPIRIN", "ASPIRIN", "METFORMIN"],
            "潛在新適應症": ["fever", "cold", "obesity"],
        })
        report = generate_repurposing_report(df)
        assert report["total_candidates"] == 3
        assert report["unique_drugs"] == 2
        assert report["unique_diseases"] == 3

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        report = generate_repurposing_report(df)
        assert report["total_candidates"] == 0
        assert report["unique_drugs"] == 0
        assert report["unique_diseases"] == 0

    def test_top_diseases(self):
        df = pd.DataFrame({
            "承認番号": ["A001", "A002", "A003"],
            "藥物成分": ["ASPIRIN", "METFORMIN", "IBUPROFEN"],
            "潛在新適應症": ["fever", "fever", "headache"],
        })
        report = generate_repurposing_report(df)
        assert "fever" in report["top_diseases"]
        assert report["top_diseases"]["fever"] == 2
