"""Base collector interface for all data sources."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class CollectorResult:
    """Result from a single collector query."""

    source: str  # e.g., "clinicaltrials", "pubmed", "unified_ddi"
    query: dict  # The query parameters used
    data: Any  # The collected data (format depends on source)
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    error_message: str | None = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "source": self.source,
            "query": self.query,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success,
            "error_message": self.error_message,
        }


class BaseCollector(ABC):
    """Abstract base class for all data collectors.

    Each collector is responsible for fetching data from a single source
    (e.g., ClinicalTrials.gov, PubMed, UnifiedDDI).
    """

    source_name: str = "base"

    @abstractmethod
    def search(self, drug: str, disease: str | None = None) -> CollectorResult:
        """Search for data about a drug-disease pair.

        Args:
            drug: Drug name (INN or brand name)
            disease: Disease/indication name (optional for some collectors)

        Returns:
            CollectorResult with the fetched data
        """
        pass

    def batch_search(
        self, pairs: list[tuple[str, str | None]]
    ) -> list[CollectorResult]:
        """Search for multiple drug-disease pairs.

        Default implementation calls search() for each pair.
        Subclasses can override for more efficient batch operations.

        Args:
            pairs: List of (drug, disease) tuples

        Returns:
            List of CollectorResult objects
        """
        results = []
        for drug, disease in pairs:
            try:
                result = self.search(drug, disease)
                results.append(result)
            except Exception as e:
                results.append(
                    CollectorResult(
                        source=self.source_name,
                        query={"drug": drug, "disease": disease},
                        data=None,
                        success=False,
                        error_message=str(e),
                    )
                )
        return results

    def _make_result(
        self,
        query: dict,
        data: Any,
        success: bool = True,
        error_message: str | None = None,
    ) -> CollectorResult:
        """Helper to create a CollectorResult."""
        return CollectorResult(
            source=self.source_name,
            query=query,
            data=data,
            success=success,
            error_message=error_message,
        )
