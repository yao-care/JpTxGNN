#!/usr/bin/env python3
"""Test the evidence collectors.

Tests PMDA, JPRN, ClinicalTrials.gov, and PubMed collectors.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from jptxgnn.collectors import (
    PMDACollector,
    JPRNCollector,
    ClinicalTrialsCollector,
    PubMedCollector,
)


def test_pmda_collector():
    """Test PMDA collector with a known drug."""
    print("\n" + "=" * 60)
    print("Testing PMDACollector")
    print("=" * 60)

    collector = PMDACollector()

    # Test with ファモチジン (Famotidine)
    result = collector.search("ファモチジン")

    print(f"Success: {result.success}")
    print(f"Query: {result.query}")

    if result.success and result.data:
        print(f"Total results: {result.data.get('total', 0)}")
        if result.data.get('results'):
            print("Sample results:")
            for r in result.data['results'][:3]:
                print(f"  - {r.get('brand_name', 'N/A')}")
    else:
        print(f"Error: {result.error_message}")

    return result.success


def test_jprn_collector():
    """Test JPRN collector (UMIN-CTR and JapicCTI)."""
    print("\n" + "=" * 60)
    print("Testing JPRNCollector")
    print("=" * 60)

    collector = JPRNCollector(max_results=10)

    # Test with common cancer drug
    result = collector.search("pembrolizumab", "cancer")

    print(f"Success: {result.success}")
    print(f"Query: {result.query}")

    if result.success and result.data:
        print(f"Total trials: {result.data.get('total', 0)}")
        print(f"Sources: {result.data.get('sources', [])}")
        if result.data.get('trials'):
            print("Sample trials:")
            for t in result.data['trials'][:3]:
                print(f"  - [{t.get('registry')}] {t.get('id')}: {t.get('title', 'N/A')[:50]}...")
    else:
        print(f"Error: {result.error_message}")

    return result.success


def test_clinicaltrials_collector():
    """Test ClinicalTrials.gov collector."""
    print("\n" + "=" * 60)
    print("Testing ClinicalTrialsCollector")
    print("=" * 60)

    collector = ClinicalTrialsCollector(max_results=10)

    # Test with a drug and disease
    result = collector.search("metformin", "diabetes")

    print(f"Success: {result.success}")
    print(f"Query: {result.query}")

    if result.success and result.data:
        # ClinicalTrials returns a list directly
        trials = result.data if isinstance(result.data, list) else result.data.get('trials', [])
        print(f"Total trials: {len(trials)}")
        if trials:
            print("Sample trials:")
            for t in trials[:3]:
                title = t.get('title', 'N/A')
                if len(title) > 50:
                    title = title[:50] + "..."
                print(f"  - {t.get('id', 'N/A')}: {title}")
    else:
        print(f"Error: {result.error_message}")

    return result.success


def test_pubmed_collector():
    """Test PubMed collector."""
    print("\n" + "=" * 60)
    print("Testing PubMedCollector")
    print("=" * 60)

    collector = PubMedCollector(max_results=5)

    # Test with drug repurposing search
    result = collector.search("famotidine", "COVID-19")

    print(f"Success: {result.success}")
    print(f"Query: {result.query}")

    if result.success and result.data:
        # PubMed returns 'results' key
        articles = result.data.get('results', [])
        print(f"Total articles: {len(articles)}")
        if articles:
            print("Sample articles:")
            for a in articles[:3]:
                title = a.get('title', 'N/A')
                if len(title) > 60:
                    title = title[:60] + "..."
                print(f"  - PMID {a.get('pmid', 'N/A')}: {title}")
    else:
        print(f"Error: {result.error_message}")

    return result.success


def main():
    """Run all collector tests."""
    print("=" * 60)
    print("JpTxGNN Collector Tests")
    print("=" * 60)

    results = {}

    # Test PMDA
    results['PMDA'] = test_pmda_collector()

    # Test JPRN
    results['JPRN'] = test_jprn_collector()

    # Test ClinicalTrials.gov
    results['ClinicalTrials'] = test_clinicaltrials_collector()

    # Test PubMed
    results['PubMed'] = test_pubmed_collector()

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {name}: {status}")

    total_passed = sum(1 for v in results.values() if v)
    print(f"\nTotal: {total_passed}/{len(results)} passed")

    return all(results.values())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
