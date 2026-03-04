"""Data collectors for evidence gathering."""

from .base import BaseCollector, CollectorResult
from .bundle import BundleAggregator, CandidateInfo, EvidenceBundle
from .clinicaltrials import ClinicalTrialsCollector
from .drug_bundle import (
    DrugBundle,
    DrugBundleAggregator,
    DrugCandidate,
    PredictedIndication,
    load_predictions_for_drug,
)
from .drugbank import DrugBankCollector
from .ictrp import ICTRPCollector
from .jprn import JPRNCollector
from .known_relations import KnownRelationsChecker
from .pmda import PMDACollector
from .pubmed import PubMedCollector

__all__ = [
    "BaseCollector",
    "BundleAggregator",
    "CandidateInfo",
    "ClinicalTrialsCollector",
    "CollectorResult",
    "DrugBundle",
    "DrugBundleAggregator",
    "DrugCandidate",
    "DrugBankCollector",
    "EvidenceBundle",
    "ICTRPCollector",
    "JPRNCollector",
    "KnownRelationsChecker",
    "PMDACollector",
    "PredictedIndication",
    "PubMedCollector",
    "load_predictions_for_drug",
]
