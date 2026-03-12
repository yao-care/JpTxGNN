"""Unified DDI collector - integrates DDInter and PHARMACOLOGY sources."""

from pathlib import Path

from .base import BaseCollector, CollectorResult
from .ddinter import DDInterCollector
from .pharmacology import PharmacologyCollector


class UnifiedDDICollector(BaseCollector):
    """Unified collector for drug-drug interaction data.

    Integrates data from two sources:
    - DDInter: Direct DDI information with severity levels
    - PHARMACOLOGY: Drug-target interactions (Guide to PHARMACOLOGY)

    Automatically merges results from both sources and removes duplicates.
    """

    source_name = "unified_ddi"

    def __init__(
        self,
        ddinter_data_dir: str | Path | None = None,
        pharmacology_data_file: str | Path | None = None,
    ):
        """Initialize the unified DDI collector.

        Args:
            ddinter_data_dir: Path to DDInter data directory (optional)
            pharmacology_data_file: Path to PHARMACOLOGY CSV file (optional)
        """
        self.ddinter = DDInterCollector(data_dir=ddinter_data_dir)
        self.pharmacology = PharmacologyCollector(data_file=pharmacology_data_file)

    def search(self, drug: str, disease: str | None = None) -> CollectorResult:
        """Search for DDI data from both sources.

        Note: disease parameter is ignored for DDI lookup.

        Args:
            drug: Drug name (case-insensitive)
            disease: Ignored for DDI lookup

        Returns:
            CollectorResult with merged DDI data from both sources
        """
        query = {"drug": drug}

        # Query both sources
        ddinter_result = self.ddinter.search(drug)
        pharmacology_result = self.pharmacology.search(drug)

        # Merge results and remove duplicates
        merged_data = []
        seen_drugs = set()

        # Add DDInter results first (they have severity levels)
        if ddinter_result.success and ddinter_result.data:
            for interaction in ddinter_result.data:
                interacting_drug_normalized = (
                    interaction["interacting_drug"].lower().strip()
                )
                if interacting_drug_normalized not in seen_drugs:
                    seen_drugs.add(interacting_drug_normalized)
                    merged_data.append(
                        {
                            "interacting_drug": interaction["interacting_drug"],
                            "level": interaction["level"],
                            "source": "ddinter",
                            "details": interaction,
                        }
                    )

        # Add PHARMACOLOGY results (targets)
        if pharmacology_result.success and pharmacology_result.data:
            for record in pharmacology_result.data:
                # For PHARMACOLOGY, we're interested in the targets
                # We can consider each target as a potential "interaction"
                target_name = record.get("target", "")
                if target_name:
                    target_key = target_name.lower().strip()
                    # Only add if not already seen (avoid duplicates with DDInter)
                    if target_key not in seen_drugs:
                        seen_drugs.add(target_key)
                        merged_data.append(
                            {
                                "interacting_drug": target_name,
                                "level": None,  # PHARMACOLOGY doesn't have severity levels
                                "source": "pharmacology",
                                "details": record,
                            }
                        )

        return self._make_result(
            query=query,
            data=merged_data,
            success=True,
        )

    def get_severe_interactions(
        self, drug: str, min_level: str = "Major"
    ) -> list[dict]:
        """Get only severe DDI interactions.

        Note: Only includes interactions from DDInter (which has severity levels).
        PHARMACOLOGY data doesn't include severity levels.

        Args:
            drug: Drug name
            min_level: Minimum severity level to include.
                      Levels from most to least severe: Major, Moderate, Minor

        Returns:
            List of severe DDI entries (only from DDInter)
        """
        level_order = {"Major": 0, "Moderate": 1, "Minor": 2}
        min_severity = level_order.get(min_level, 1)

        result = self.search(drug)
        if not result.success or not result.data:
            return []

        severe = []
        for interaction in result.data:
            # Only consider DDInter interactions (which have severity levels)
            if interaction["source"] == "ddinter":
                level = interaction.get("level")
                if level in level_order and level_order[level] <= min_severity:
                    severe.append(interaction)

        return severe

    def get_stats(self) -> dict:
        """Get statistics from both data sources.

        Returns:
            Dictionary with statistics from DDInter and PHARMACOLOGY
        """
        # Get available drugs from both sources
        ddinter_drugs = set(self.ddinter.get_available_drugs())
        pharmacology_drugs = set(self.pharmacology.get_available_drugs())

        # Count total interactions in DDInter
        ddinter_total_interactions = 0
        for drug in ddinter_drugs:
            ddinter_total_interactions += self.ddinter.get_interaction_count(drug)

        # Count total target records in PHARMACOLOGY
        pharmacology_total_targets = 0
        for drug in pharmacology_drugs:
            result = self.pharmacology.search(drug)
            if result.success and result.data:
                pharmacology_total_targets += len(result.data)

        return {
            "ddinter": {
                "drugs_count": len(ddinter_drugs),
                "total_interactions": ddinter_total_interactions,
                "data_dir": str(self.ddinter.data_dir),
            },
            "pharmacology": {
                "drugs_count": len(pharmacology_drugs),
                "total_target_records": pharmacology_total_targets,
                "data_file": str(self.pharmacology.data_file),
            },
            "unified": {
                "total_drugs": len(ddinter_drugs | pharmacology_drugs),
                "common_drugs": len(ddinter_drugs & pharmacology_drugs),
            },
        }

    def get_available_drugs(self) -> list[str]:
        """Get list of drugs with available DDI data from both sources.

        Returns:
            Sorted list of unique drug names
        """
        ddinter_drugs = set(self.ddinter.get_available_drugs())
        pharmacology_drugs = set(self.pharmacology.get_available_drugs())

        # Merge and sort
        all_drugs = ddinter_drugs | pharmacology_drugs
        return sorted(all_drugs)

    def get_interaction_count(self, drug: str) -> int:
        """Get total number of interactions for a drug from both sources.

        Args:
            drug: Drug name

        Returns:
            Total number of interactions (DDInter + PHARMACOLOGY targets)
        """
        result = self.search(drug)
        if result.success and result.data:
            return len(result.data)
        return 0

    def get_ddinter_only(self, drug: str) -> list[dict]:
        """Get interactions from DDInter source only.

        Args:
            drug: Drug name

        Returns:
            List of DDInter interactions
        """
        result = self.search(drug)
        if not result.success or not result.data:
            return []

        return [i for i in result.data if i["source"] == "ddinter"]

    def get_pharmacology_only(self, drug: str) -> list[dict]:
        """Get interactions from PHARMACOLOGY source only.

        Args:
            drug: Drug name

        Returns:
            List of PHARMACOLOGY target interactions
        """
        result = self.search(drug)
        if not result.success or not result.data:
            return []

        return [i for i in result.data if i["source"] == "pharmacology"]
