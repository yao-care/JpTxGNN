#!/usr/bin/env python3
"""Batch generate Evidence Packs and Notes for all collected bundles.

This script processes all drug bundles and generates:
1. Evidence Pack (LLM analysis)
2. Pharmacist Notes (LLM report)

Usage:
    # Generate reports for all bundles
    python scripts/batch_generate_reports.py --all

    # Generate for specific drugs
    python scripts/batch_generate_reports.py --drugs "Warfarin,Minoxidil"

    # Only generate for bundles without reports
    python scripts/batch_generate_reports.py --missing-only

    # Process a range (for parallel execution)
    python scripts/batch_generate_reports.py --all --offset 0 --limit 100
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def get_all_bundles() -> list[Path]:
    """Get all bundle directories."""
    bundles_dir = Path("data/bundles")
    if not bundles_dir.exists():
        return []

    bundles = []
    for drug_dir in sorted(bundles_dir.iterdir()):
        if drug_dir.is_dir() and (drug_dir / "drug_bundle.json").exists():
            bundles.append(drug_dir)
    return bundles


def get_missing_reports(predictions_only: bool = False) -> list[Path]:
    """Get bundles that don't have notes yet.

    Args:
        predictions_only: If True, only include bundles that have predicted_indications.
    """
    notes_dir = Path("data/notes")
    bundles = get_all_bundles()

    missing = []
    for bundle_dir in bundles:
        drug_name = bundle_dir.name
        notes_path = notes_dir / drug_name / "drug_pharmacist_notes.md"
        if not notes_path.exists():
            if predictions_only:
                bundle_path = bundle_dir / "drug_bundle.json"
                with open(bundle_path, "r", encoding="utf-8") as f:
                    bundle_data = json.load(f)
                if not bundle_data.get("drug", {}).get("predicted_indications"):
                    continue
            missing.append(bundle_dir)

    return missing


def generate_report_for_drug(
    drug_name: str,
    prompt_version: str = "v5",
    skip_existing: bool = True,
    model: str | None = "sonnet",
) -> dict:
    """Generate Evidence Pack and Notes for a single drug.

    Returns:
        dict with status, paths, and timing info
    """
    from jptxgnn.collectors.drug_bundle import DrugBundle
    from jptxgnn.reviewer import DrugEvidencePackGenerator
    from jptxgnn.writer import DrugPharmacistNotesWriter

    result = {
        "drug": drug_name,
        "status": "pending",
        "evidence_pack": None,
        "notes": None,
        "error": None,
        "duration_seconds": 0,
    }

    start_time = time.time()
    data_dir = Path("data")

    try:
        # Load bundle
        bundle_path = data_dir / "bundles" / drug_name / "drug_bundle.json"
        if not bundle_path.exists():
            raise FileNotFoundError(f"Bundle not found: {bundle_path}")

        bundle = DrugBundle.load(bundle_path)

        # Check if notes already exist
        notes_path = data_dir / "notes" / drug_name / "drug_pharmacist_notes.md"
        if skip_existing and notes_path.exists():
            result["status"] = "skipped"
            result["notes"] = str(notes_path)
            return result

        # Step 1: Generate Evidence Pack
        ep_dir = data_dir / "evidence_packs" / drug_name
        ep_generator = DrugEvidencePackGenerator(model=model)
        json_path, md_path = ep_generator.generate_and_save(
            bundle=bundle,
            output_dir=ep_dir,
        )
        result["evidence_pack"] = str(json_path)

        # Step 2: Generate Notes
        with open(json_path, 'r', encoding='utf-8') as f:
            evidence_pack = json.load(f)

        notes_dir = data_dir / "notes" / drug_name
        notes_dir.mkdir(parents=True, exist_ok=True)

        pharmacist_writer = DrugPharmacistNotesWriter(prompt_version=prompt_version, model=model)
        pharmacist_path = notes_dir / "drug_pharmacist_notes.md"
        pharmacist_writer.generate_and_save(evidence_pack, pharmacist_path)

        result["status"] = "success"
        result["notes"] = str(pharmacist_path)

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    result["duration_seconds"] = round(time.time() - start_time, 2)
    return result


def main():
    parser = argparse.ArgumentParser(description="Batch generate reports for drug bundles")
    parser.add_argument("--drugs", type=str, help="Comma-separated list of drug names")
    parser.add_argument("--all", action="store_true", help="Process all bundles")
    parser.add_argument("--missing-only", action="store_true", help="Only process bundles without reports")
    parser.add_argument("--offset", type=int, default=0, help="Start offset (for parallel processing)")
    parser.add_argument("--limit", type=int, help="Max number to process")
    parser.add_argument("--prompt-version", default="v5", choices=["v4", "v5"], help="Prompt version")
    parser.add_argument("--output", type=str, help="Output JSON file for results")
    parser.add_argument("--no-skip", action="store_true", help="Don't skip existing reports")
    parser.add_argument("--predictions-only", action="store_true", help="Only process bundles with predicted_indications")
    parser.add_argument("--model", type=str, default="sonnet", help="Claude model (default: sonnet)")

    args = parser.parse_args()

    # Get drug list
    if args.drugs:
        drug_dirs = [Path(f"data/bundles/{d.strip()}") for d in args.drugs.split(",")]
    elif args.missing_only:
        drug_dirs = get_missing_reports(predictions_only=args.predictions_only)
    elif args.all:
        drug_dirs = get_all_bundles()
    else:
        print("Please specify --drugs, --all, or --missing-only")
        sys.exit(1)

    # Apply offset and limit
    if args.offset:
        drug_dirs = drug_dirs[args.offset:]
    if args.limit:
        drug_dirs = drug_dirs[:args.limit]

    print(f"Processing {len(drug_dirs)} drugs (model={args.model}, offset={args.offset}, limit={args.limit or 'all'})...")
    print("-" * 60)

    results = []
    success_count = 0
    skip_count = 0
    error_count = 0

    for i, drug_dir in enumerate(drug_dirs, 1):
        drug_name = drug_dir.name
        print(f"[{i}/{len(drug_dirs)}] {drug_name}...", end=" ", flush=True)

        result = generate_report_for_drug(
            drug_name=drug_name,
            prompt_version=args.prompt_version,
            skip_existing=not args.no_skip,
            model=args.model,
        )
        results.append(result)

        if result["status"] == "success":
            success_count += 1
            print(f"✓ ({result['duration_seconds']}s)")
        elif result["status"] == "skipped":
            skip_count += 1
            print("⊘ (已存在)")
        else:
            error_count += 1
            print(f"✗ {result['error'][:50]}")

    # Summary
    print("-" * 60)
    print(f"完成: {success_count} 成功, {skip_count} 跳過, {error_count} 錯誤")

    # Save results
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"結果已儲存: {output_path}")

    return results


if __name__ == "__main__":
    main()
