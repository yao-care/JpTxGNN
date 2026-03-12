"""DDInter DDI collector - reads local CSV files."""

import csv
from pathlib import Path

from .base import BaseCollector, CollectorResult


class DDInterCollector(BaseCollector):
    """Collector for DDInter drug-drug interaction data.

    Reads from local CSV files in data/external/ddi/ddinter/.
    Files are named ddinter_code_*.csv and contain DDI information.
    """

    source_name = "ddinter"

    def __init__(self, data_dir: str | Path | None = None):
        """Initialize the DDInter collector.

        Args:
            data_dir: Path to the directory containing CSV files.
                     Defaults to data/external/ddi/ddinter/
        """
        if data_dir is None:
            # Default to project's data directory
            self.data_dir = (
                Path(__file__).parent.parent.parent.parent
                / "data"
                / "external"
                / "ddi"
                / "ddinter"
            )
        else:
            self.data_dir = Path(data_dir)

        # Cache for loaded data
        self._cache: dict[str, list[dict]] | None = None

    def _load_all_data(self) -> dict[str, list[dict]]:
        """Load all DDI data from CSV files.

        Returns:
            Dictionary mapping drug names (lowercase) to list of interactions
        """
        if self._cache is not None:
            return self._cache

        drug_interactions: dict[str, list[dict]] = {}

        if not self.data_dir.exists():
            self._cache = {}
            return self._cache

        # Load all CSV files
        for csv_file in self.data_dir.glob("ddinter_code_*.csv"):
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Extract both directions of interaction
                    drug_a = row["Drug_A"].strip()
                    drug_b = row["Drug_B"].strip()
                    level = row["Level"].strip()

                    # Normalize drug names for lookup (case-insensitive)
                    drug_a_key = drug_a.lower()
                    drug_b_key = drug_b.lower()

                    # Add interaction from Drug_A perspective
                    if drug_a_key not in drug_interactions:
                        drug_interactions[drug_a_key] = []
                    drug_interactions[drug_a_key].append(
                        {
                            "interacting_drug": drug_b,
                            "level": level,
                            "source": self.source_name,
                        }
                    )

                    # Add interaction from Drug_B perspective
                    if drug_b_key not in drug_interactions:
                        drug_interactions[drug_b_key] = []
                    drug_interactions[drug_b_key].append(
                        {
                            "interacting_drug": drug_a,
                            "level": level,
                            "source": self.source_name,
                        }
                    )

        self._cache = drug_interactions
        return self._cache

    def search(self, drug: str, disease: str | None = None) -> CollectorResult:
        """Search for DDI data for a drug.

        Note: disease parameter is ignored for DDI lookup.

        Args:
            drug: Drug name (case-insensitive)
            disease: Ignored for DDI lookup

        Returns:
            CollectorResult with DDI data
        """
        query = {"drug": drug}

        # Load all data if not cached
        all_interactions = self._load_all_data()

        # Normalize drug name for lookup
        drug_key = drug.lower().strip()

        # Get interactions for this drug
        interactions = all_interactions.get(drug_key, [])

        return self._make_result(
            query=query,
            data=interactions,
            success=True,
        )

    def get_available_drugs(self) -> list[str]:
        """Get list of drugs with available DDI data.

        Returns:
            List of drug names (sorted, case-preserved from original data)
        """
        all_interactions = self._load_all_data()

        # Get unique drug names (case-preserved)
        drugs_set = set()
        for interactions in all_interactions.values():
            for interaction in interactions:
                drugs_set.add(interaction["interacting_drug"])

        return sorted(drugs_set)

    def get_severe_interactions(
        self, drug: str, min_level: str = "Major"
    ) -> list[dict]:
        """Get only severe DDI interactions.

        Args:
            drug: Drug name
            min_level: Minimum severity level to include.
                      Levels from most to least severe: Major, Moderate, Minor

        Returns:
            List of severe DDI entries
        """
        level_order = {"Major": 0, "Moderate": 1, "Minor": 2}
        min_severity = level_order.get(min_level, 1)

        result = self.search(drug)
        if not result.success or not result.data:
            return []

        severe = []
        for ddi in result.data:
            level = ddi.get("level", "")
            if level in level_order and level_order[level] <= min_severity:
                severe.append(ddi)

        return severe

    def get_interaction_count(self, drug: str) -> int:
        """Get the total number of interactions for a drug.

        Args:
            drug: Drug name

        Returns:
            Number of interactions
        """
        result = self.search(drug)
        if result.success and result.data:
            return len(result.data)
        return 0
