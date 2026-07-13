#!/usr/bin/env python3
"""Batch collect drug bundles (without LLM calls).

This script collects drug bundles including DDI data for multiple drugs.
It does NOT require an API key since it only collects data, no LLM generation.

Usage:
    # Collect top 10 drugs by prediction count
    python scripts/batch_collect_bundles.py --limit 10

    # Collect specific drugs
    python scripts/batch_collect_bundles.py --drugs "Warfarin,Minoxidil,Aspirin"

    # Collect all drugs with high-confidence predictions
    python scripts/batch_collect_bundles.py --all --min-score 0.99

    # Parallel processing with offset (for running multiple instances)
    python scripts/batch_collect_bundles.py --all --offset 0 --limit 100 --skip-existing
    python scripts/batch_collect_bundles.py --all --offset 100 --limit 100 --skip-existing

    # Patch existing bundles that have no predicted_indications
    # (adds predictions + PubMed/ClinTrials evidence without re-collecting drug-level data)
    python scripts/batch_collect_bundles.py --patch-empty
"""

import argparse
import json
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
from jptxgnn.collectors import DrugBundleAggregator
from jptxgnn.paths import get_bundles_dir, slugify


def get_prediction_drugs(
    predictions_path: Path | None = None,
    min_score: float = 0.99,
    offset: int = 0,
    limit: int | None = None,
) -> list[dict]:
    """Get list of drugs with predictions, sorted by prediction count."""
    if predictions_path is None:
        predictions_path = Path("data/processed/txgnn_dl_predictions.csv.gz")

    df = pd.read_csv(predictions_path)

    # Filter by score
    df = df[df["txgnn_score"] >= min_score]

    # Group by drug and count predictions
    drug_stats = df.groupby("drug_name").agg({
        "txgnn_score": ["count", "max", "mean"]
    }).reset_index()
    drug_stats.columns = ["drug_name", "prediction_count", "max_score", "mean_score"]
    drug_stats = drug_stats.sort_values("prediction_count", ascending=False)

    # Apply offset
    if offset > 0:
        drug_stats = drug_stats.iloc[offset:]

    # Apply limit
    if limit:
        drug_stats = drug_stats.head(limit)

    return drug_stats.to_dict("records")


def get_mapping_drugs(
    mapping_path: Path | None = None,
    offset: int = 0,
    limit: int | None = None,
) -> list[dict]:
    """Get list of unique mapped drugs from drug_mapping.csv."""
    if mapping_path is None:
        mapping_path = Path("data/processed/drug_mapping.csv")

    df = pd.read_csv(mapping_path)

    # Find the success column (映射成功 or mapping_success)
    success_col = None
    for col in ["mapping_success", "映射成功"]:
        if col in df.columns:
            success_col = col
            break

    # Find the ingredient column
    ingredient_col = None
    for col in ["normalized_ingredient", "標準化成分", "drug_ingredient"]:
        if col in df.columns:
            ingredient_col = col
            break

    if success_col and ingredient_col:
        df = df[df[success_col] == True]
        drugs = df[ingredient_col].dropna().unique()
    else:
        # Fallback: use drugbank_id mapped rows
        df = df[df["drugbank_id"].notna()]
        for col in ["normalized_ingredient", "標準化成分", "drug_ingredient", "ingredient"]:
            if col in df.columns:
                drugs = df[col].dropna().unique()
                break
        else:
            drugs = []

    drug_list = [{"drug_name": d} for d in sorted(drugs)]

    if offset > 0:
        drug_list = drug_list[offset:]
    if limit:
        drug_list = drug_list[:limit]

    return drug_list


def preload_predictions(min_score: float = 0.99, top_n: int = 10) -> dict[str, list]:
    """Preload all DL predictions into a dict keyed by lowercase drug name.

    Returns:
        dict mapping drug_name (lowercase) -> list of PredictedIndication objects
    """
    from jptxgnn.collectors.drug_bundle import PredictedIndication
    from jptxgnn.collectors.known_relations import KnownRelationsChecker

    predictions_path = Path("data/processed/txgnn_dl_predictions.csv.gz")
    if not predictions_path.exists():
        print(f"警告: {predictions_path} 不存在，無法 patch")
        return {}

    df = pd.read_csv(predictions_path)
    df = df[df["txgnn_score"] >= min_score]

    checker = KnownRelationsChecker()
    drug_predictions: dict[str, list] = {}

    for drug_name, group in df.groupby("drug_name"):
        group = group.sort_values("txgnn_score", ascending=False)
        results = []
        for _, row in group.iterrows():
            disease = row["潛在新適應症"]
            if not checker.is_novel(drug_name, disease):
                continue
            results.append(
                PredictedIndication(
                    disease_name=disease,
                    txgnn_score=row["txgnn_score"],
                    txgnn_rank=row.get("rank"),
                )
            )
            if top_n > 0 and len(results) >= top_n:
                break
        if results:
            drug_predictions[drug_name.lower()] = results

    return drug_predictions


def patch_single_drug(
    bundle_path: Path,
    drug_predictions: dict[str, list],
) -> dict:
    """Patch an existing bundle that has no predicted_indications.

    Uses preloaded predictions (fast in-memory lookup) instead of
    reading the predictions CSV per drug.

    Returns:
        dict with status, drug, indication_count, error, duration_seconds
    """
    from jptxgnn.collectors.drug_bundle import DrugBundle

    result = {
        "drug": "",
        "status": "pending",
        "indication_count": 0,
        "error": None,
        "duration_seconds": 0,
    }

    start_time = time.time()

    try:
        bundle = DrugBundle.load(bundle_path)
        drug_name = bundle.drug.inn
        result["drug"] = drug_name

        # Fast in-memory lookup
        predicted = drug_predictions.get(drug_name.lower())

        if not predicted:
            result["status"] = "no_predictions"
            result["duration_seconds"] = round(time.time() - start_time, 2)
            return result

        # Deep copy so we don't mutate the shared list
        from copy import deepcopy
        predicted = deepcopy(predicted)

        # Collect per-indication evidence
        aggregator = DrugBundleAggregator(save_collected=True)
        for indication in predicted:
            aggregator.collect_indication_data(drug_name, indication)

        # Update bundle in-place
        bundle.drug.predicted_indications = predicted
        bundle.drug.is_novel_check_done = True
        bundle.collection_log.extend(aggregator._collection_log)
        bundle.metadata["patched_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        bundle.metadata["indications_found"] = len(predicted)
        bundle.save(bundle_path.parent)

        result["status"] = "success"
        result["indication_count"] = len(predicted)

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    result["duration_seconds"] = round(time.time() - start_time, 2)
    return result


def collect_single_drug(drug_name: str, top_n: int = 10, min_score: float = 0.99) -> dict:
    """Collect bundle for a single drug.

    Returns:
        dict with status, bundle_path, ddi_count, indication_count, error
    """
    result = {
        "drug": drug_name,
        "status": "pending",
        "bundle_path": None,
        "ddi_count": 0,
        "indication_count": 0,
        "error": None,
        "duration_seconds": 0,
    }

    start_time = time.time()

    try:
        aggregator = DrugBundleAggregator(save_collected=True)
        bundle = aggregator.collect(
            drug_name=drug_name,
            top_n=top_n,
            min_score=min_score,
        )

        # Save bundle
        bundle_path = bundle.save()

        # Get stats
        ddi_count = len(bundle.safety.get("ddi", []))
        indication_count = len(bundle.drug.predicted_indications)

        result.update({
            "status": "success",
            "bundle_path": str(bundle_path),
            "ddi_count": ddi_count,
            "indication_count": indication_count,
        })

    except Exception as e:
        result.update({
            "status": "error",
            "error": str(e),
        })

    result["duration_seconds"] = round(time.time() - start_time, 2)
    return result


def main():
    parser = argparse.ArgumentParser(description="Batch collect drug bundles")
    parser.add_argument("--drugs", type=str, help="Comma-separated list of drug names")
    parser.add_argument("--limit", type=int, help="Limit number of drugs to process")
    parser.add_argument("--offset", type=int, default=0, help="Start offset (for parallel processing)")
    parser.add_argument("--all", action="store_true", help="Process all drugs with predictions")
    parser.add_argument("--min-score", type=float, default=0.99, help="Minimum TxGNN score")
    parser.add_argument("--top-n", type=int, default=10, help="Top N predictions per drug")
    parser.add_argument("--output", type=str, help="Output JSON file for results")
    parser.add_argument("--skip-existing", action="store_true", help="Skip drugs with existing bundles")
    parser.add_argument("--from-mapping", action="store_true", help="Get drugs from drug_mapping.csv instead of DL predictions")
    parser.add_argument("--patch-empty", action="store_true", help="Patch existing bundles that have no predicted_indications (adds predictions + evidence without re-collecting drug-level data)")

    args = parser.parse_args()

    # --patch-empty mode: find and patch bundles missing predictions
    if args.patch_empty:
        bundles_dir = get_bundles_dir()
        if not bundles_dir.exists():
            print("data/bundles/ 不存在")
            sys.exit(1)

        # Find bundles with no predicted_indications
        empty_bundles = []
        for drug_dir in sorted(bundles_dir.iterdir()):
            bf = drug_dir / "drug_bundle.json"
            if not bf.is_file():
                continue
            try:
                with open(bf) as f:
                    data = json.load(f)
                pis = data.get("drug", {}).get("predicted_indications", [])
                if not pis:
                    empty_bundles.append(bf)
            except Exception:
                empty_bundles.append(bf)

        if not empty_bundles:
            print("所有 bundles 都已有 predicted_indications，無需 patch")
            return []

        print(f"找到 {len(empty_bundles)} 個需要 patch 的 bundles")

        # Preload predictions once (avoids re-reading CSV per bundle)
        print("載入 DL 預測資料...", end=" ", flush=True)
        drug_predictions = preload_predictions(
            min_score=args.min_score, top_n=args.top_n,
        )
        print(f"完成 ({len(drug_predictions)} 個藥物有預測)")
        print("-" * 60)

        results = []
        for i, bf in enumerate(empty_bundles, 1):
            drug_slug = bf.parent.name
            print(f"[{i}/{len(empty_bundles)}] {drug_slug}...", end=" ", flush=True)

            result = patch_single_drug(
                bundle_path=bf,
                drug_predictions=drug_predictions,
            )
            results.append(result)

            if result["status"] == "success":
                print(f"✓ Ind:{result['indication_count']} ({result['duration_seconds']}s)")
            elif result["status"] == "no_predictions":
                print(f"- no predictions found ({result['duration_seconds']}s)")
            else:
                print(f"✗ {result['error']}")

        # Summary
        print("-" * 60)
        success = sum(1 for r in results if r["status"] == "success")
        no_pred = sum(1 for r in results if r["status"] == "no_predictions")
        errors = sum(1 for r in results if r["status"] == "error")
        total_ind = sum(r["indication_count"] for r in results)
        print(f"完成: {success} patched, {no_pred} no predictions, {errors} errors")
        print(f"總計新增適應症: {total_ind}")

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
            print(f"結果已儲存: {output_path}")

        return results

    # Get drug list
    if args.drugs:
        drugs = [{"drug_name": d.strip()} for d in args.drugs.split(",")]
    elif args.from_mapping:
        drugs = get_mapping_drugs(offset=args.offset, limit=args.limit)
    elif args.all or args.limit:
        drugs = get_prediction_drugs(min_score=args.min_score, offset=args.offset, limit=args.limit)
    else:
        print("Please specify --drugs, --limit, or --all")
        sys.exit(1)

    # Filter out existing bundles if requested
    if args.skip_existing:
        bundles_dir = get_bundles_dir()
        original_count = len(drugs)
        drugs = [
            d for d in drugs
            if not (bundles_dir / slugify(d["drug_name"]) / "drug_bundle.json").exists()
        ]
        skipped = original_count - len(drugs)
        if skipped > 0:
            print(f"跳過 {skipped} 個已存在的 bundles")

    print(f"Processing {len(drugs)} drugs (offset={args.offset})...")
    print("-" * 60)

    results = []
    for i, drug_info in enumerate(drugs, 1):
        drug_name = drug_info["drug_name"]
        print(f"[{i}/{len(drugs)}] {drug_name}...", end=" ", flush=True)

        result = collect_single_drug(
            drug_name=drug_name,
            top_n=args.top_n,
            min_score=args.min_score,
        )
        results.append(result)

        if result["status"] == "success":
            print(f"✓ DDI:{result['ddi_count']} Ind:{result['indication_count']} ({result['duration_seconds']}s)")
        else:
            print(f"✗ {result['error']}")

    # Summary
    print("-" * 60)
    success = sum(1 for r in results if r["status"] == "success")
    total_ddi = sum(r["ddi_count"] for r in results)
    total_ind = sum(r["indication_count"] for r in results)
    print(f"完成: {success}/{len(drugs)} 成功")
    print(f"總計 DDI: {total_ddi}, 總計適應症: {total_ind}")

    # Save results
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"結果已儲存: {output_path}")

    return results


if __name__ == "__main__":
    main()
