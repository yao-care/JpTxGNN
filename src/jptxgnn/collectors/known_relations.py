"""Check if drug-disease pairs are known relations in the knowledge graph."""

import pandas as pd
from pathlib import Path
from typing import Literal

from ..paths import get_data_dir


class KnownRelationsChecker:
    """Check if drug-disease pairs are already known in the knowledge graph.

    This class helps filter out predictions that are already established
    indications or contraindications.
    """

    def __init__(self, relations_path: str | Path | None = None):
        """Initialize the checker.

        Args:
            relations_path: Path to the drug_disease_relations.csv file.
                          If None, uses the default path.
        """
        if relations_path is None:
            relations_path = get_data_dir() / "external" / "drug_disease_relations.csv"

        self.relations_path = Path(relations_path)
        self._indications: set[tuple[str, str]] | None = None
        self._contraindications: set[tuple[str, str]] | None = None
        self._all_relations: pd.DataFrame | None = None

    def _load_relations(self) -> None:
        """Load relations from CSV file."""
        if not self.relations_path.exists():
            self._indications = set()
            self._contraindications = set()
            return

        df = pd.read_csv(self.relations_path)

        # Normalize names for matching
        df['drug_lower'] = df['x_name'].str.lower().str.strip()
        df['disease_lower'] = df['y_name'].str.lower().str.strip()

        # Build sets for fast lookup
        indications = df[df['relation'] == 'indication']
        contraindications = df[df['relation'] == 'contraindication']

        self._indications = set(zip(
            indications['drug_lower'],
            indications['disease_lower']
        ))
        self._contraindications = set(zip(
            contraindications['drug_lower'],
            contraindications['disease_lower']
        ))
        self._all_relations = df

    @property
    def indications(self) -> set[tuple[str, str]]:
        """Get set of known indication pairs (drug, disease)."""
        if self._indications is None:
            self._load_relations()
        return self._indications  # type: ignore

    @property
    def contraindications(self) -> set[tuple[str, str]]:
        """Get set of known contraindication pairs (drug, disease)."""
        if self._contraindications is None:
            self._load_relations()
        return self._contraindications  # type: ignore

    def check(
        self,
        drug: str,
        disease: str
    ) -> dict[str, bool | str | None]:
        """Check if a drug-disease pair is a known relation.

        Args:
            drug: Drug name (INN)
            disease: Disease name

        Returns:
            Dictionary with:
            - is_novel: True if this is a novel prediction (not known)
            - relation_type: 'indication', 'contraindication', or None
            - should_exclude: True if this should be excluded from analysis
        """
        drug_lower = drug.lower().strip()
        disease_lower = disease.lower().strip()
        pair = (drug_lower, disease_lower)

        if pair in self.indications:
            return {
                "is_novel": False,
                "relation_type": "indication",
                "should_exclude": True,
                "reason": "Already approved indication in knowledge graph"
            }

        if pair in self.contraindications:
            return {
                "is_novel": False,
                "relation_type": "contraindication",
                "should_exclude": True,
                "reason": "Known contraindication - drug should NOT be used for this disease"
            }

        return {
            "is_novel": True,
            "relation_type": None,
            "should_exclude": False,
            "reason": None
        }

    def is_novel(self, drug: str, disease: str) -> bool:
        """Quick check if a drug-disease pair is novel (not in KG).

        Args:
            drug: Drug name (INN)
            disease: Disease name

        Returns:
            True if novel, False if known
        """
        return self.check(drug, disease)["is_novel"]

    def is_contraindicated(self, drug: str, disease: str) -> bool:
        """Check if a drug is contraindicated for a disease.

        Args:
            drug: Drug name (INN)
            disease: Disease name

        Returns:
            True if contraindicated
        """
        drug_lower = drug.lower().strip()
        disease_lower = disease.lower().strip()
        return (drug_lower, disease_lower) in self.contraindications

    def get_stats(self) -> dict[str, int]:
        """Get statistics about known relations.

        Returns:
            Dictionary with counts
        """
        return {
            "total_indications": len(self.indications),
            "total_contraindications": len(self.contraindications),
            "total_relations": len(self.indications) + len(self.contraindications),
        }
