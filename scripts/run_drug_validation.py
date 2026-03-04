#!/usr/bin/env python3
"""Run the drug-centric validation pipeline for a drug with multiple predicted indications.

This is the new drug-centric approach:
1. Input: A drug name
2. Collect drug-level data once (PMDA, DDI, safety)
3. Load predicted indications from TxGNN results
4. Collect disease-specific data for each indication (trials, pubmed)
5. Generate comprehensive drug-centric reports

Usage:
    python scripts/run_drug_validation.py --drug "Minoxidil" --top-n 5

    # Skip data collection, use existing bundle
    python scripts/run_drug_validation.py --drug "Minoxidil" --skip-collection

    # Skip evidence pack generation, use existing
    python scripts/run_drug_validation.py --drug "Minoxidil" --skip-evidence-pack
"""

import argparse
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from jptxgnn.collectors import (
    DrugBundle,
    DrugBundleAggregator,
    load_predictions_for_drug,
)
from jptxgnn.reviewer import DrugEvidencePackGenerator
from jptxgnn.writer import DrugPharmacistNotesWriter, DrugSponsorNotesWriter
from jptxgnn.paths import get_bundles_dir, get_evidence_packs_dir, get_notes_dir, slugify


def run_pipeline(
    drug: str,
    drugbank_id: str | None = None,
    top_n: int = 10,
    min_score: float = 0.99,
    skip_collection: bool = False,
    skip_evidence_pack: bool = False,
    predictions_path: str | None = None,
    prompt_version: str = "v4",
) -> dict[str, Path]:
    """Run the drug-centric validation pipeline.

    Args:
        drug: Drug name (INN)
        drugbank_id: Optional DrugBank ID
        top_n: Maximum number of predicted indications to include
        min_score: Minimum TxGNN score threshold
        skip_collection: Skip data collection (use existing bundle)
        skip_evidence_pack: Skip evidence pack generation (use existing)
        predictions_path: Optional path to predictions CSV
        prompt_version: Prompt version to use (v4 or v5)

    Returns:
        Dict with paths to all generated files
    """
    results = {}

    drug_slug = slugify(drug)
    drug_dir = drug_slug

    print("=" * 60)
    print(f"TxGNN Drug-Centric Validation Pipeline")
    print("=" * 60)
    print(f"Drug: {drug}")
    print(f"DrugBank ID: {drugbank_id or 'N/A'}")
    print(f"Top N indications: {top_n}")
    print(f"Min TxGNN score: {min_score:.2%}")
    print("=" * 60)

    # Check how many predicted indications exist
    if not skip_collection:
        predicted = load_predictions_for_drug(
            drug_name=drug,
            predictions_path=predictions_path,
            top_n=top_n,
            min_score=min_score,
        )
        print(f"\nFound {len(predicted)} novel predicted indications:")
        for i, pi in enumerate(predicted[:5], 1):
            print(f"  {i}. {pi.disease_name} (score: {pi.txgnn_score:.4%})")
        if len(predicted) > 5:
            print(f"  ... and {len(predicted) - 5} more")
        print("-" * 60)

    # Step 1: Data Collection
    bundle_path = get_bundles_dir() / drug_dir / "drug_bundle.json"

    if not skip_collection:
        print("\n[Step 1] Collecting data...")

        aggregator = DrugBundleAggregator()
        bundle = aggregator.collect(
            drug_name=drug,
            drugbank_id=drugbank_id,
            top_n=top_n,
            min_score=min_score,
            predictions_path=predictions_path,
        )

        # Report collected data
        print(f"  - Drug: {bundle.drug.inn}")
        print(f"  - Original indications: {len(bundle.drug.original_indications)}")
        for ind in bundle.drug.original_indications[:3]:
            print(f"      - {ind[:50]}...")
        print(f"  - Predicted indications: {len(bundle.drug.predicted_indications)}")
        print(f"  - PMDA found: {bundle.pmda.get('found', False)}")
        print(f"  - DDI entries: {len(bundle.safety.get('ddi', []))}")

        # Report per-indication data
        print("\n  Per-indication data collected:")
        for pi in bundle.drug.predicted_indications:
            trials = len(pi.clinical_trials) + len(pi.ictrp_trials)
            articles = len(pi.pubmed_articles)
            print(f"    - {pi.disease_name[:40]}: {trials} trials, {articles} articles")

        # Save bundle
        saved_path = bundle.save()
        print(f"\n  - Bundle saved: {saved_path}")
        results['bundle'] = saved_path
    else:
        print("\n[Step 1] Skipping data collection (using existing bundle)")
        bundle = DrugBundle.load(bundle_path)
        results['bundle'] = bundle_path
        print(f"  - Loaded bundle: {bundle_path}")
        print(f"  - Drug: {bundle.drug.inn}")
        print(f"  - Predicted indications: {len(bundle.drug.predicted_indications)}")

    # Step 2: Evidence Pack Generation
    evidence_pack_dir = get_evidence_packs_dir() / drug_dir
    evidence_pack_json = evidence_pack_dir / f"{drug_slug}_drug_evidence_pack.json"
    evidence_pack_md = evidence_pack_dir / f"{drug_slug}_drug_evidence_pack.md"

    if not skip_evidence_pack:
        print("\n[Step 2] Generating Drug Evidence Pack (calling LLM)...")

        generator = DrugEvidencePackGenerator()
        json_path, md_path = generator.generate_and_save(
            bundle=bundle,
            output_dir=evidence_pack_dir,
        )

        print(f"  - JSON: {json_path}")
        print(f"  - Markdown: {md_path}")
        results['evidence_pack_json'] = json_path
        results['evidence_pack_md'] = md_path
    else:
        print("\n[Step 2] Skipping Evidence Pack generation (using existing)")
        if evidence_pack_json.exists():
            results['evidence_pack_json'] = evidence_pack_json
            results['evidence_pack_md'] = evidence_pack_md
        else:
            print(f"  WARNING: Evidence pack not found at {evidence_pack_json}")
            print("  Please run without --skip-evidence-pack first.")
            return results

    # Step 3: Notes Generation
    print("\n[Step 3] Generating Notes (calling LLM)...")

    notes_dir = get_notes_dir() / drug_dir
    notes_dir.mkdir(parents=True, exist_ok=True)

    # Load evidence pack for notes generation
    with open(results['evidence_pack_json'], 'r', encoding='utf-8') as f:
        evidence_pack = json.load(f)

    # Generate Drug Pharmacist Notes
    print(f"  - Generating Drug Pharmacist Notes (prompt {prompt_version})...")
    pharmacist_writer = DrugPharmacistNotesWriter(prompt_version=prompt_version)
    pharmacist_path = notes_dir / "drug_pharmacist_notes.md"
    pharmacist_writer.generate_and_save(evidence_pack, pharmacist_path)
    print(f"    Saved: {pharmacist_path}")
    results['pharmacist_notes'] = pharmacist_path

    # Generate Drug Sponsor Notes (only for v4, v5 is unified)
    if prompt_version == "v4":
        print("  - Generating Drug Sponsor Notes...")
        sponsor_writer = DrugSponsorNotesWriter()
        sponsor_path = notes_dir / "drug_sponsor_notes.md"
        sponsor_writer.generate_and_save(evidence_pack, sponsor_path)
        print(f"    Saved: {sponsor_path}")
        results['sponsor_notes'] = sponsor_path
    else:
        print("  - Skipping Sponsor Notes (v5 is unified report)")

    print("\n" + "=" * 60)
    print("Pipeline completed!")
    print("=" * 60)
    print("\nGenerated files:")
    for name, path in results.items():
        print(f"  - {name}: {path}")

    # Print summary table
    print("\n" + "-" * 60)
    print("Summary Table:")
    print("-" * 60)
    print(bundle.get_summary_table())

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Run the drug-centric TxGNN validation pipeline"
    )
    parser.add_argument("--drug", required=True, help="Drug name (INN)")
    parser.add_argument("--drugbank-id", help="DrugBank ID")
    parser.add_argument("--top-n", type=int, default=10,
                       help="Maximum number of predicted indications (default: 10)")
    parser.add_argument("--min-score", type=float, default=0.99,
                       help="Minimum TxGNN score threshold (default: 0.99)")
    parser.add_argument("--predictions-path",
                       help="Path to predictions CSV (default: data/processed/txgnn_dl_predictions.csv)")
    parser.add_argument("--skip-collection", action="store_true",
                       help="Skip data collection, use existing bundle")
    parser.add_argument("--skip-evidence-pack", action="store_true",
                       help="Skip evidence pack generation, use existing")
    parser.add_argument("--prompt-version", default="v4", choices=["v4", "v5"],
                       help="Prompt version to use (v4: detailed template, v5: storytelling)")

    args = parser.parse_args()

    run_pipeline(
        drug=args.drug,
        drugbank_id=args.drugbank_id,
        top_n=args.top_n,
        min_score=args.min_score,
        skip_collection=args.skip_collection,
        skip_evidence_pack=args.skip_evidence_pack,
        predictions_path=args.predictions_path,
        prompt_version=args.prompt_version,
    )


if __name__ == "__main__":
    main()
