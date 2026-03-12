"""Guide to PHARMACOLOGY DDI collector - reads local CSV file."""

import csv
from pathlib import Path

from .base import BaseCollector, CollectorResult


class PharmacologyCollector(BaseCollector):
    """Collector for Guide to PHARMACOLOGY drug-target interaction data.

    Reads from local CSV file: approved_drug_detailed_interactions.csv
    Contains ligand-target interaction information from GtoPdb.
    """

    source_name = "pharmacology"

    def __init__(self, data_file: str | Path | None = None):
        """Initialize the PHARMACOLOGY collector.

        Args:
            data_file: Path to the CSV file.
                      Defaults to data/external/ddi/pharmacology/approved_drug_detailed_interactions.csv
        """
        if data_file is None:
            # Default to project's data directory
            self.data_file = (
                Path(__file__).parent.parent.parent.parent
                / "data"
                / "external"
                / "ddi"
                / "pharmacology"
                / "approved_drug_detailed_interactions.csv"
            )
        else:
            self.data_file = Path(data_file)

        # Cache for loaded data: {normalized_drug_name: [records]}
        self._cache: dict[str, list[dict]] = {}
        self._loaded = False

    def _normalize_drug_name(self, drug: str) -> str:
        """Normalize drug name for lookup (lowercase, stripped)."""
        return drug.lower().strip()

    def _load_data(self) -> None:
        """Load and parse the CSV file into cache.

        Organizes data by ligand name and synonyms for fast lookup.
        """
        if self._loaded:
            return

        if not self.data_file.exists():
            # File doesn't exist, mark as loaded to avoid repeated checks
            self._loaded = True
            return

        with open(self.data_file, "r", encoding="utf-8") as f:
            # Skip comment lines at the beginning (may be quoted like "# ...")
            first_line = f.readline()
            if first_line.strip().startswith("#") or first_line.strip().startswith('"#'):
                # Comment line, continue from here (next line is header)
                pass
            else:
                # Not a comment, reset to beginning
                f.seek(0)

            # Now read with DictReader
            reader = csv.DictReader(f)

            for row in reader:
                ligand = row.get("Ligand", "")
                if not ligand:
                    continue

                # Create a target record
                target_record = {
                    "ligand": ligand,
                    "ligand_id": row.get("Ligand ID", ""),
                    "type": row.get("Type", ""),
                    "synonyms": row.get("Ligand Synonyms", ""),
                    "smiles": row.get("SMILES", ""),
                    "cas_number": row.get("CAS Number", ""),
                    "clinical_use": row.get("Clinical Use Comment", ""),
                    "bioactivity": row.get("Bioactivity Comment", ""),
                    "target": row.get("Target", ""),
                    "target_id": row.get("Target ID", ""),
                    "target_entrez_gene_id": row.get("Target Entrez Gene ID", ""),
                    "target_ensembl_gene_id": row.get("Target Ensembl Gene ID", ""),
                    "target_gene_name": row.get("Target Gene Name", ""),
                    "target_ligand": row.get("Target Ligand", ""),
                    "target_ligand_id": row.get("Target Ligand ID", ""),
                    "target_species": row.get("Target Species", ""),
                }

                # Index by normalized ligand name
                normalized_ligand = self._normalize_drug_name(ligand)
                if normalized_ligand not in self._cache:
                    self._cache[normalized_ligand] = []
                self._cache[normalized_ligand].append(target_record)

                # Also index by synonyms (split by |)
                synonyms_str = row.get("Ligand Synonyms", "")
                if synonyms_str:
                    synonyms = [s.strip() for s in synonyms_str.split("|")]
                    for synonym in synonyms:
                        if synonym:
                            normalized_synonym = self._normalize_drug_name(synonym)
                            if normalized_synonym not in self._cache:
                                self._cache[normalized_synonym] = []
                            # Avoid duplicates
                            if target_record not in self._cache[normalized_synonym]:
                                self._cache[normalized_synonym].append(target_record)

        self._loaded = True

    def search(self, drug: str, disease: str | None = None) -> CollectorResult:
        """Search for drug-target interaction data for a drug.

        Note: disease parameter is ignored for target lookup.

        Args:
            drug: Drug name (INN or brand name)
            disease: Ignored for target lookup

        Returns:
            CollectorResult with target interaction data
        """
        query = {"drug": drug}

        # Ensure data is loaded
        self._load_data()

        # Look up the drug
        normalized = self._normalize_drug_name(drug)
        data = self._cache.get(normalized, [])

        return self._make_result(
            query=query,
            data=data,
            success=True,  # Not finding data is not an error
            error_message=None,
        )

    def get_available_drugs(self) -> list[str]:
        """Get list of drugs with available target data.

        Returns:
            Sorted list of drug names (ligands)
        """
        self._load_data()

        # Extract unique ligand names (not normalized)
        drugs = set()
        for records in self._cache.values():
            for record in records:
                if record["ligand"]:
                    drugs.add(record["ligand"])

        return sorted(drugs)

    def get_targets_for_drug(self, drug: str) -> list[dict]:
        """Get all target interactions for a specific drug.

        Args:
            drug: Drug name

        Returns:
            List of target records with simplified structure
        """
        result = self.search(drug)
        if not result.success or not result.data:
            return []

        # Extract and simplify target information
        targets = []
        seen = set()  # To avoid duplicates
        for record in result.data:
            target_key = (record["target"], record["target_gene_name"])
            if target_key not in seen:
                seen.add(target_key)
                targets.append(
                    {
                        "target_name": record["target"],
                        "target_gene": record["target_gene_name"],
                        "target_species": record["target_species"],
                        "entrez_gene_id": record["target_entrez_gene_id"],
                        "ensembl_gene_id": record["target_ensembl_gene_id"],
                    }
                )

        return targets

    def get_human_targets(self, drug: str) -> list[dict]:
        """Get only human target interactions for a drug.

        Args:
            drug: Drug name

        Returns:
            List of human target records
        """
        all_targets = self.get_targets_for_drug(drug)
        return [t for t in all_targets if t["target_species"] == "Human"]
