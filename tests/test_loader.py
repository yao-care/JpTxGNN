"""Test data loader module"""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock

from jptxgnn.data.loader import (
    load_fda_drugs,
    filter_active_drugs,
)


class TestLoadFdaDrugs:
    """Test load_fda_drugs function"""

    def test_returns_dataframe(self):
        # This test requires actual data file
        try:
            df = load_fda_drugs()
            assert isinstance(df, pd.DataFrame)
        except FileNotFoundError:
            pytest.skip("Data file not found")

    def test_has_required_columns(self):
        try:
            df = load_fda_drugs()
            required_cols = ["承認番号", "販売名", "有効成分"]
            for col in required_cols:
                assert col in df.columns, f"Missing column: {col}"
        except FileNotFoundError:
            pytest.skip("Data file not found")


class TestFilterActiveDrugs:
    """Test filter_active_drugs function"""

    def test_filters_active_status(self):
        df = pd.DataFrame({
            "承認番号": ["A001", "A002", "A003"],
            "販売名": ["Drug A", "Drug B", "Drug C"],
            "承認状況": ["有効", "販売中止", "有効"],
        })
        result = filter_active_drugs(df)
        assert len(result) == 2
        assert all(result["承認状況"] == "有効")

    def test_empty_dataframe(self):
        df = pd.DataFrame({
            "承認番号": [],
            "販売名": [],
            "承認状況": [],
        })
        result = filter_active_drugs(df)
        assert len(result) == 0

    def test_no_status_column(self):
        df = pd.DataFrame({
            "承認番号": ["A001"],
            "販売名": ["Drug A"],
        })
        # Should return all rows if no status column
        result = filter_active_drugs(df)
        assert len(result) == 1

    def test_all_inactive(self):
        df = pd.DataFrame({
            "承認番号": ["A001", "A002"],
            "販売名": ["Drug A", "Drug B"],
            "承認状況": ["販売中止", "取消"],
        })
        result = filter_active_drugs(df)
        assert len(result) == 0
