"""Drug-centric bundle for analyzing one drug with multiple predicted indications."""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass
class CollectionStatus:
    """Tracks the status of data collection for a single source."""

    source: str  # e.g., "clinicaltrials", "pubmed", "pmda", "ddi"
    query_params: dict  # The query parameters used
    queried_at: str  # ISO timestamp
    status: str  # "success", "error", "not_found"
    result_count: int = 0
    error_message: str | None = None

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "query_params": self.query_params,
            "queried_at": self.queried_at,
            "status": self.status,
            "result_count": self.result_count,
            "error_message": self.error_message,
        }


@dataclass
class PredictedIndication:
    """A single predicted new indication for a drug."""

    disease_name: str
    txgnn_score: float
    txgnn_rank: int | None = None
    # Disease-specific evidence (collected per indication)
    clinical_trials: list[dict] = field(default_factory=list)
    pubmed_articles: list[dict] = field(default_factory=list)
    ictrp_trials: list[dict] = field(default_factory=list)
    # Analysis results
    evidence_level: str | None = None  # L1-L5
    mechanistic_link: str | None = None
    similarity_to_original: str | None = None  # High/Medium/Low

    def to_dict(self) -> dict:
        return {
            "disease_name": self.disease_name,
            "txgnn_score": self.txgnn_score,
            "txgnn_rank": self.txgnn_rank,
            "clinical_trials": self.clinical_trials,
            "pubmed_articles": self.pubmed_articles,
            "ictrp_trials": self.ictrp_trials,
            "evidence_level": self.evidence_level,
            "mechanistic_link": self.mechanistic_link,
            "similarity_to_original": self.similarity_to_original,
        }


@dataclass
class DrugCandidate:
    """Information about a drug being evaluated for repurposing."""

    inn: str  # International Nonproprietary Name
    drugbank_id: str | None = None
    brand_name_zh: str | None = None
    # Original approved indications (from PMDA)
    original_indications: list[str] = field(default_factory=list)
    original_moa: str | None = None  # Mechanism of Action
    # Predicted new indications
    predicted_indications: list[PredictedIndication] = field(default_factory=list)
    # Knowledge graph status
    is_novel_check_done: bool = False

    def to_dict(self) -> dict:
        return {
            "inn": self.inn,
            "drugbank_id": self.drugbank_id,
            "brand_name_zh": self.brand_name_zh,
            "original_indications": self.original_indications,
            "original_moa": self.original_moa,
            "predicted_indications": [p.to_dict() for p in self.predicted_indications],
            "is_novel_check_done": self.is_novel_check_done,
        }


@dataclass
class DrugBundle:
    """Bundle of evidence for one drug with multiple predicted indications.

    This is the new drug-centric data structure for repurposing analysis.
    """

    drug: DrugCandidate
    # Drug-level data (collected once)
    pmda: dict = field(default_factory=lambda: {"found": False, "records": []})
    safety: dict = field(
        default_factory=lambda: {"label_sources": [], "key_warnings": [], "ddi": []}
    )
    # Enhanced data from new collectors (v3)
    drugbank: dict = field(default_factory=lambda: {"found": False})
    package_insert: dict = field(default_factory=lambda: {"found": False})
    # Collection status tracking (v4)
    collection_log: list[CollectionStatus] = field(default_factory=list)
    # Metadata
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Add metadata after initialization."""
        if "created_at" not in self.metadata:
            self.metadata["created_at"] = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "drug": self.drug.to_dict(),
            "pmda": self.pmda,
            "safety": self.safety,
            "drugbank": self.drugbank,
            "package_insert": self.package_insert,
            "collection_log": [cs.to_dict() for cs in self.collection_log],
            "metadata": self.metadata,
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def save(self, output_dir: str | Path | None = None) -> Path:
        """Save the bundle to a JSON file."""
        from ..paths import get_bundles_dir, slugify

        if output_dir is None:
            drug_slug = slugify(self.drug.inn)
            output_dir = get_bundles_dir() / drug_slug

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / "drug_bundle.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

        return output_path

    @classmethod
    def load(cls, path: str | Path) -> "DrugBundle":
        """Load a bundle from a JSON file."""
        path = Path(path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Reconstruct predicted indications
        predicted_indications = [
            PredictedIndication(**pi)
            for pi in data["drug"].get("predicted_indications", [])
        ]

        drug = DrugCandidate(
            inn=data["drug"]["inn"],
            drugbank_id=data["drug"].get("drugbank_id"),
            brand_name_zh=data["drug"].get("brand_name_zh"),
            original_indications=data["drug"].get("original_indications", []),
            original_moa=data["drug"].get("original_moa"),
            predicted_indications=predicted_indications,
            is_novel_check_done=data["drug"].get("is_novel_check_done", False),
        )

        # Reconstruct collection_log
        collection_log = [
            CollectionStatus(**cs) for cs in data.get("collection_log", [])
        ]

        return cls(
            drug=drug,
            pmda=data.get("pmda", {"found": False, "records": []}),
            safety=data.get("safety", {"label_sources": [], "key_warnings": [], "ddi": []}),
            drugbank=data.get("drugbank", {"found": False}),
            package_insert=data.get("package_insert", {"found": False}),
            collection_log=collection_log,
            metadata=data.get("metadata", {}),
        )

    def get_summary_table(self) -> str:
        """Generate a markdown summary table."""
        lines = [
            "| 預測新適應症 | TxGNN 分數 | 臨床試驗 | 文獻 | 證據等級 |",
            "|-------------|-----------|---------|------|---------|",
        ]
        for pi in self.drug.predicted_indications:
            trials = len(pi.clinical_trials) + len(pi.ictrp_trials)
            articles = len(pi.pubmed_articles)
            level = pi.evidence_level or "待評估"
            lines.append(
                f"| {pi.disease_name} | {pi.txgnn_score:.4%} | {trials} | {articles} | {level} |"
            )
        return "\n".join(lines)


def load_predictions_for_drug(
    drug_name: str,
    predictions_path: str | Path | None = None,
    top_n: int = 10,
    min_score: float = 0.99,
) -> list[PredictedIndication]:
    """Load predicted indications for a specific drug from predictions CSV.

    Args:
        drug_name: Drug name (INN)
        predictions_path: Path to predictions CSV. If None, uses default.
        top_n: Maximum number of predictions to return
        min_score: Minimum TxGNN score threshold

    Returns:
        List of PredictedIndication objects
    """
    from ..paths import get_data_dir
    from .known_relations import KnownRelationsChecker

    if predictions_path is None:
        predictions_path = get_data_dir() / "processed" / "txgnn_dl_predictions.csv"

    predictions_path = Path(predictions_path)
    if not predictions_path.exists():
        return []

    df = pd.read_csv(predictions_path)

    # Filter by drug name (case-insensitive)
    drug_df = df[df["drug_name"].str.lower() == drug_name.lower()]

    # Filter by score
    drug_df = drug_df[drug_df["txgnn_score"] >= min_score]

    # Sort by score descending
    drug_df = drug_df.sort_values("txgnn_score", ascending=False)

    # Check known relations
    checker = KnownRelationsChecker()
    results = []

    for _, row in drug_df.iterrows():
        disease = row["潛在新適應症"]

        # Skip known indications/contraindications
        if not checker.is_novel(drug_name, disease):
            continue

        results.append(
            PredictedIndication(
                disease_name=disease,
                txgnn_score=row["txgnn_score"],
                txgnn_rank=row.get("rank"),
            )
        )

        # top_n <= 0 means no limit
        if top_n > 0 and len(results) >= top_n:
            break

    return results


class DrugBundleAggregator:
    """Aggregates evidence for one drug with multiple predicted indications.

    This is the drug-centric approach:
    1. Collect drug-level data once (PMDA, safety/DDI)
    2. Load predicted indications for the drug
    3. Collect disease-specific data for each indication (trials, pubmed)
    """

    def __init__(self, save_collected: bool = True):
        """Initialize the aggregator.

        Args:
            save_collected: Whether to save collected data to disk
        """
        self.save_collected = save_collected
        self._collectors: dict = {}
        self._collection_log: list[CollectionStatus] = []

    def _record_status(
        self,
        source: str,
        query_params: dict,
        success: bool,
        result_count: int = 0,
        error_message: str | None = None,
    ) -> None:
        """Record a collection status entry."""
        status = "success" if success else ("error" if error_message else "not_found")
        self._collection_log.append(
            CollectionStatus(
                source=source,
                query_params=query_params,
                queried_at=datetime.now().isoformat(),
                status=status,
                result_count=result_count,
                error_message=error_message,
            )
        )

    def _get_collector(self, name: str):
        """Lazy-load collectors as needed."""
        if name not in self._collectors:
            if name == "pmda":
                from .pmda import PMDACollector
                self._collectors[name] = PMDACollector()
            elif name == "drugbank":
                from .drugbank import DrugBankCollector
                self._collectors[name] = DrugBankCollector()
            elif name == "clinicaltrials":
                from .clinicaltrials import ClinicalTrialsCollector
                self._collectors[name] = ClinicalTrialsCollector()
            elif name == "ictrp":
                from .ictrp import ICTRPCollector
                self._collectors[name] = ICTRPCollector()
            elif name == "jprn":
                from .jprn import JPRNCollector
                self._collectors[name] = JPRNCollector()
            elif name == "pubmed":
                from .pubmed import PubMedCollector
                self._collectors[name] = PubMedCollector()
            # DDI collector not yet implemented for Japan
        return self._collectors.get(name)

    def collect_drug_level_data(self, drug_name: str) -> tuple[dict, dict, dict, dict]:
        """Collect drug-level data (PMDA, safety, DrugBank).

        These are collected once per drug, regardless of indications.

        Args:
            drug_name: Drug name (INN)

        Returns:
            Tuple of (pmda_data, safety_data, drugbank_data, package_insert_data)
        """
        from ..paths import get_collected_dir, slugify

        pmda_data = {"found": False, "records": []}
        safety_data = {"label_sources": [], "key_warnings": [], "ddi": []}
        drugbank_data = {"found": False}
        package_insert_data = {"found": False}

        drug_slug = slugify(drug_name)

        # Collect PMDA data (Japan regulatory)
        pmda_collector = self._get_collector("pmda")
        if pmda_collector:
            try:
                result = pmda_collector.search(drug=drug_name, disease="")
                if result.success and result.data:
                    pmda_data = result.data
                    record_count = len(pmda_data.get("records", []))
                    self._record_status("pmda", {"drug": drug_name}, True, record_count)
                    if self.save_collected:
                        collected_dir = get_collected_dir("pmda")
                        collected_dir.mkdir(parents=True, exist_ok=True)
                        with open(collected_dir / f"{drug_slug}.json", "w", encoding="utf-8") as f:
                            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
                else:
                    self._record_status("pmda", {"drug": drug_name}, False, 0)
            except Exception as e:
                pmda_data["error"] = str(e)
                self._record_status("pmda", {"drug": drug_name}, False, 0, str(e))

        # Collect DrugBank data (MOA, description, pharmacodynamics)
        drugbank_collector = self._get_collector("drugbank")
        if drugbank_collector:
            try:
                result = drugbank_collector.search(drug=drug_name)
                if result.success and result.data:
                    drugbank_data = result.data
                    self._record_status("drugbank", {"drug": drug_name}, True, 1)
                    if self.save_collected:
                        collected_dir = get_collected_dir("drugbank")
                        collected_dir.mkdir(parents=True, exist_ok=True)
                        with open(collected_dir / f"{drug_slug}.json", "w", encoding="utf-8") as f:
                            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
                else:
                    self._record_status("drugbank", {"drug": drug_name}, False, 0)
            except Exception as e:
                drugbank_data["error"] = str(e)
                self._record_status("drugbank", {"drug": drug_name}, False, 0, str(e))

        return pmda_data, safety_data, drugbank_data, package_insert_data

    def collect_indication_data(
        self,
        drug_name: str,
        indication: PredictedIndication,
    ) -> PredictedIndication:
        """Collect disease-specific data for one predicted indication.

        Args:
            drug_name: Drug name (INN)
            indication: The predicted indication to collect data for

        Returns:
            Updated PredictedIndication with collected evidence
        """
        from ..paths import get_collected_dir, slugify

        drug_slug = slugify(drug_name)
        disease_slug = slugify(indication.disease_name)
        pair_slug = f"{drug_slug}_{disease_slug}"

        # Collect clinical trials
        ct_collector = self._get_collector("clinicaltrials")
        query_params = {"drug": drug_name, "disease": indication.disease_name}
        if ct_collector:
            try:
                result = ct_collector.search(drug=drug_name, disease=indication.disease_name)
                if result.success and result.data:
                    indication.clinical_trials = result.data
                    self._record_status("clinicaltrials", query_params, True, len(result.data))
                    if self.save_collected:
                        collected_dir = get_collected_dir("clinicaltrials")
                        collected_dir.mkdir(parents=True, exist_ok=True)
                        with open(collected_dir / f"{pair_slug}.json", "w", encoding="utf-8") as f:
                            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
                else:
                    self._record_status("clinicaltrials", query_params, True, 0)
            except Exception as e:
                indication.clinical_trials = [{"error": str(e)}]
                self._record_status("clinicaltrials", query_params, False, 0, str(e))

        # Collect ICTRP trials
        ictrp_collector = self._get_collector("ictrp")
        if ictrp_collector:
            try:
                result = ictrp_collector.search(drug=drug_name, disease=indication.disease_name)
                if result.success and result.data:
                    indication.ictrp_trials = result.data
                    self._record_status("ictrp", query_params, True, len(result.data))
                    if self.save_collected:
                        collected_dir = get_collected_dir("ictrp")
                        collected_dir.mkdir(parents=True, exist_ok=True)
                        with open(collected_dir / f"{pair_slug}.json", "w", encoding="utf-8") as f:
                            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
                else:
                    self._record_status("ictrp", query_params, True, 0)
            except Exception as e:
                indication.ictrp_trials = [{"error": str(e)}]
                self._record_status("ictrp", query_params, False, 0, str(e))

        # Collect PubMed articles
        pubmed_collector = self._get_collector("pubmed")
        if pubmed_collector:
            try:
                result = pubmed_collector.search(drug=drug_name, disease=indication.disease_name)
                if result.success and result.data:
                    articles = result.data.get("results", [])
                    indication.pubmed_articles = articles
                    self._record_status("pubmed", query_params, True, len(articles))
                    if self.save_collected:
                        collected_dir = get_collected_dir("pubmed")
                        collected_dir.mkdir(parents=True, exist_ok=True)
                        with open(collected_dir / f"{pair_slug}.json", "w", encoding="utf-8") as f:
                            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
                else:
                    self._record_status("pubmed", query_params, True, 0)
            except Exception as e:
                indication.pubmed_articles = [{"error": str(e)}]
                self._record_status("pubmed", query_params, False, 0, str(e))

        return indication

    def collect(
        self,
        drug_name: str,
        drugbank_id: str | None = None,
        top_n: int = 10,
        min_score: float = 0.99,
        predictions_path: str | Path | None = None,
    ) -> DrugBundle:
        """Collect all evidence for a drug with its predicted indications.

        Args:
            drug_name: Drug name (INN)
            drugbank_id: Optional DrugBank ID
            top_n: Maximum number of predicted indications to include
            min_score: Minimum TxGNN score threshold
            predictions_path: Optional path to predictions CSV

        Returns:
            DrugBundle with all collected evidence
        """
        # Clear collection log for this run
        self._collection_log = []

        # Step 1: Load predicted indications
        predicted_indications = load_predictions_for_drug(
            drug_name=drug_name,
            predictions_path=predictions_path,
            top_n=top_n,
            min_score=min_score,
        )

        # Step 2: Collect drug-level data once
        pmda_data, safety_data, drugbank_data, package_insert_data = self.collect_drug_level_data(drug_name)

        # Extract original indications from PMDA
        original_indications = []
        original_moa = None
        brand_name_zh = None
        drugbank_id_found = None

        if pmda_data.get("found") and pmda_data.get("records"):
            for record in pmda_data["records"]:
                # Support both English and Chinese field names
                indication = record.get("indication", record.get("適應症"))
                if indication:
                    original_indications.append(indication)
                brand_zh = record.get("brand_name_zh", record.get("中文品名"))
                if brand_zh and not brand_name_zh:
                    brand_name_zh = brand_zh

        # Extract MOA and DrugBank ID from DrugBank data
        if drugbank_data.get("found"):
            original_moa = drugbank_data.get("mechanism_of_action")
            drugbank_id_found = drugbank_data.get("drugbank_id")

        # Step 3: Collect disease-specific data for each indication
        for indication in predicted_indications:
            self.collect_indication_data(drug_name, indication)

        # Step 4: Build the DrugBundle
        # Use provided drugbank_id or the one found from DrugBank lookup
        final_drugbank_id = drugbank_id or drugbank_id_found

        drug = DrugCandidate(
            inn=drug_name,
            drugbank_id=final_drugbank_id,
            brand_name_zh=brand_name_zh,
            original_indications=list(set(original_indications)),
            original_moa=original_moa,
            predicted_indications=predicted_indications,
            is_novel_check_done=True,
        )

        bundle = DrugBundle(
            drug=drug,
            pmda=pmda_data,
            safety=safety_data,
            drugbank=drugbank_data,
            package_insert=package_insert_data,
            collection_log=self._collection_log.copy(),
            metadata={
                "top_n": top_n,
                "min_score": min_score,
                "indications_found": len(predicted_indications),
            },
        )

        return bundle
