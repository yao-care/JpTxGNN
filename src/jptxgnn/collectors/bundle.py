"""Bundle aggregator for combining results from multiple collectors."""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .base import BaseCollector, CollectorResult


@dataclass
class CandidateInfo:
    """Information about the drug-disease candidate being evaluated."""

    inn: str  # International Nonproprietary Name
    drugbank_id: str | None = None
    brand_name_zh: str | None = None
    license_id: str | None = None
    indication_raw: str | None = None
    txgnn_score: float | None = None
    txgnn_rank: int | None = None
    model_version: str | None = None
    run_date: str | None = None
    # Knowledge graph relation status
    is_novel: bool | None = None  # True if not in KG, None if not checked
    kg_relation_type: str | None = None  # 'indication', 'contraindication', or None
    kg_relation_note: str | None = None  # Explanation of relation status

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "inn": self.inn,
            "drugbank_id": self.drugbank_id,
            "brand_name_zh": self.brand_name_zh,
            "license_id": self.license_id,
            "indication_raw": self.indication_raw,
            "txgnn_score": self.txgnn_score,
            "txgnn_rank": self.txgnn_rank,
            "model_version": self.model_version,
            "run_date": self.run_date,
            "is_novel": self.is_novel,
            "kg_relation_type": self.kg_relation_type,
            "kg_relation_note": self.kg_relation_note,
        }


@dataclass
class EvidenceBundle:
    """Bundle of evidence from multiple sources.

    This is the input format expected by the Evidence Pack Reviewer.
    """

    candidate: CandidateInfo
    pmda: dict = field(default_factory=lambda: {"found": False, "records": []})
    trials: dict = field(
        default_factory=lambda: {"clinicaltrials_gov": [], "who_ictrp": []}
    )
    pubmed: dict = field(default_factory=lambda: {"query": "", "results": []})
    safety: dict = field(
        default_factory=lambda: {"label_sources": [], "key_warnings": [], "ddi": []}
    )
    other: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Add metadata after initialization."""
        if "created_at" not in self.metadata:
            self.metadata["created_at"] = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "candidate": self.candidate.to_dict(),
            "pmda": self.pmda,
            "trials": self.trials,
            "pubmed": self.pubmed,
            "safety": self.safety,
            "other": self.other,
            "metadata": self.metadata,
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def save(self, output_dir: str | Path | None = None) -> Path:
        """Save the bundle to a JSON file.

        Args:
            output_dir: Directory to save to. If None, uses default bundles dir.

        Returns:
            Path to the saved file
        """
        from ..paths import get_bundles_dir, slugify

        if output_dir is None:
            drug_slug = slugify(self.candidate.inn)
            disease_slug = slugify(self.candidate.indication_raw or "unknown")
            output_dir = get_bundles_dir() / f"{drug_slug}_{disease_slug}"

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / "bundle.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

        return output_path

    @classmethod
    def load(cls, path: str | Path) -> "EvidenceBundle":
        """Load a bundle from a JSON file.

        Args:
            path: Path to the bundle JSON file

        Returns:
            EvidenceBundle instance
        """
        path = Path(path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        candidate = CandidateInfo(**data["candidate"])
        return cls(
            candidate=candidate,
            pmda=data.get("pmda", {"found": False, "records": []}),
            trials=data.get("trials", {"clinicaltrials_gov": [], "who_ictrp": []}),
            pubmed=data.get("pubmed", {"query": "", "results": []}),
            safety=data.get("safety", {"label_sources": [], "key_warnings": [], "ddi": []}),
            other=data.get("other", {}),
            metadata=data.get("metadata", {}),
        )


class BundleAggregator:
    """Aggregates results from multiple collectors into an EvidenceBundle."""

    def __init__(
        self,
        save_collected: bool = True,
        check_known_relations: bool = True,
    ):
        """Initialize the aggregator.

        Args:
            save_collected: Whether to save collected data to disk
            check_known_relations: Whether to check if drug-disease pairs
                                  are known relations in the knowledge graph
        """
        self.collectors: dict[str, BaseCollector] = {}
        self.save_collected = save_collected
        self.check_known_relations = check_known_relations
        self._relations_checker = None

    @property
    def relations_checker(self):
        """Lazy-load the relations checker."""
        if self._relations_checker is None and self.check_known_relations:
            from .known_relations import KnownRelationsChecker
            self._relations_checker = KnownRelationsChecker()
        return self._relations_checker

    def annotate_candidate(self, candidate: CandidateInfo) -> CandidateInfo:
        """Annotate a candidate with knowledge graph relation status.

        Args:
            candidate: The candidate to annotate

        Returns:
            The annotated candidate (modified in place)
        """
        if not self.check_known_relations or not candidate.indication_raw:
            return candidate

        checker = self.relations_checker
        if checker is None:
            return candidate

        result = checker.check(candidate.inn, candidate.indication_raw)
        candidate.is_novel = result["is_novel"]
        candidate.kg_relation_type = result["relation_type"]
        candidate.kg_relation_note = result["reason"]

        return candidate

    def register_collector(self, name: str, collector: BaseCollector) -> None:
        """Register a collector for a specific data source."""
        self.collectors[name] = collector

    def collect(
        self,
        candidate: CandidateInfo,
        sources: list[str] | None = None,
        save_bundle: bool = True,
        skip_known: bool = False,
    ) -> EvidenceBundle | None:
        """Collect evidence from all registered collectors.

        Args:
            candidate: Information about the drug-disease candidate
            sources: Optional list of source names to query.
                    If None, queries all registered collectors.
            save_bundle: Whether to save the bundle to disk
            skip_known: If True, skip candidates that are known indications
                       or contraindications. Returns None for skipped candidates.

        Returns:
            EvidenceBundle with all collected data, or None if skipped
        """
        from ..paths import get_collected_dir, slugify

        # Annotate candidate with KG relation status
        self.annotate_candidate(candidate)

        # Skip if this is a known relation
        if skip_known and candidate.is_novel is False:
            return None

        bundle = EvidenceBundle(candidate=candidate)

        sources_to_query = sources or list(self.collectors.keys())
        collected_paths = {}

        for source_name in sources_to_query:
            if source_name not in self.collectors:
                continue

            collector = self.collectors[source_name]
            try:
                result = collector.search(
                    drug=candidate.inn,
                    disease=candidate.indication_raw,
                )
                self._merge_result(bundle, source_name, result)

                # Save collected data
                if self.save_collected and result.success and result.data:
                    drug_slug = slugify(candidate.inn)
                    disease_slug = slugify(candidate.indication_raw or "unknown")
                    filename = f"{drug_slug}_{disease_slug}.json"

                    collected_dir = get_collected_dir(source_name)
                    collected_dir.mkdir(parents=True, exist_ok=True)
                    collected_path = collected_dir / filename

                    with open(collected_path, "w", encoding="utf-8") as f:
                        json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

                    collected_paths[source_name] = str(collected_path)

            except Exception as e:
                # Record error in metadata
                if "errors" not in bundle.metadata:
                    bundle.metadata["errors"] = {}
                bundle.metadata["errors"][source_name] = str(e)

        bundle.metadata["sources_queried"] = sources_to_query
        bundle.metadata["collected_paths"] = collected_paths

        # Save bundle
        if save_bundle:
            bundle_path = bundle.save()
            bundle.metadata["bundle_path"] = str(bundle_path)

        return bundle

    def _merge_result(
        self,
        bundle: EvidenceBundle,
        source_name: str,
        result: CollectorResult,
    ) -> None:
        """Merge a collector result into the bundle."""
        if not result.success or result.data is None:
            return

        # Map collector results to bundle fields
        if source_name == "pmda":
            bundle.pmda = result.data
        elif source_name == "clinicaltrials":
            bundle.trials["clinicaltrials_gov"] = result.data
        elif source_name == "ictrp":
            bundle.trials["who_ictrp"] = result.data
        elif source_name == "pubmed":
            bundle.pubmed = result.data
        elif source_name in ("unified_ddi", "ddi"):
            bundle.safety["ddi"] = result.data
        else:
            # Store in 'other' for unknown sources
            bundle.other[source_name] = result.data
