#!/usr/bin/env python3
"""Sync notes from data/notes/ to docs/_drugs/ for Jekyll.

This script reads pharmacist notes and creates Jekyll-compatible drug pages
with proper front matter for the documentation site.

Usage:
    uv run python scripts/sync_notes_to_docs.py
"""

import json
import re
from pathlib import Path


def extract_evidence_level(content: str) -> str:
    """Extract evidence level from note content."""
    # Look for "| 證據等級 | L1 |" pattern
    match = re.search(r'\|\s*證據等級\s*\|\s*(L[1-5])\s*\|', content)
    if match:
        return match.group(1)
    return "L5"


def extract_indication_count(content: str, bundle_path: Path) -> int:
    """Extract indication count from bundle or content."""
    # Try to get from bundle first
    if bundle_path.exists():
        try:
            with open(bundle_path) as f:
                bundle = json.load(f)
                if "drug" in bundle and "predicted_indications" in bundle["drug"]:
                    return len(bundle["drug"]["predicted_indications"])
        except Exception:
            pass

    # Fallback: count from content (look for "預測新適應症" section)
    # Simple heuristic: if there's a predicted indication, count = 1
    match = re.search(r'\|\s*預測新適應症\s*\|\s*([^|]+)\s*\|', content)
    if match:
        indication = match.group(1).strip()
        if indication and indication != "無":
            return 1
    return 0


def get_parent_by_level(level: str) -> str:
    """Get parent page name by evidence level."""
    if level in ("L1", "L2"):
        return "高證據等級 (L1-L2)"
    elif level in ("L3", "L4"):
        return "中證據等級 (L3-L4)"
    else:
        return "僅模型預測 (L5)"


def sync_notes_to_docs():
    """Main sync function."""
    base_dir = Path(__file__).parent.parent
    notes_dir = base_dir / "data" / "notes"
    bundles_dir = base_dir / "data" / "bundles"
    docs_drugs_dir = base_dir / "docs" / "_drugs"

    # Create docs/_drugs if not exists
    docs_drugs_dir.mkdir(parents=True, exist_ok=True)

    # Get all drug directories with notes
    drug_dirs = sorted([d for d in notes_dir.iterdir() if d.is_dir()])

    print(f"Found {len(drug_dirs)} drug directories")

    synced = 0
    errors = []

    for i, drug_dir in enumerate(drug_dirs, 1):
        drug_name = drug_dir.name
        notes_path = drug_dir / "drug_pharmacist_notes.md"

        if not notes_path.exists():
            errors.append(f"{drug_name}: notes not found")
            continue

        # Read notes content
        content = notes_path.read_text(encoding="utf-8")

        # Extract metadata
        evidence_level = extract_evidence_level(content)
        bundle_path = bundles_dir / drug_name / "drug_bundle.json"
        indication_count = extract_indication_count(content, bundle_path)
        parent = get_parent_by_level(evidence_level)

        # Format title (capitalize first letter of each word)
        title = drug_name.replace("_", " ").title()

        # Create Jekyll front matter
        front_matter = f"""---
layout: default
title: {title}
parent: {parent}
nav_order: {i + 10}
evidence_level: {evidence_level}
indication_count: {indication_count}
---

# {title}
{{: .fs-9 }}

證據等級: **{evidence_level}** | 預測適應症: **{indication_count}** 個
{{: .fs-6 .fw-300 }}

---

## 目錄
{{: .no_toc .text-delta }}

1. TOC
{{:toc}}

---

<div id="pharmacist">

## 藥師評估報告

</div>

"""

        # Combine front matter with content
        full_content = front_matter + content + "\n---\n\n"

        # Write to docs/_drugs
        output_path = docs_drugs_dir / f"{drug_name}.md"
        output_path.write_text(full_content, encoding="utf-8")

        synced += 1
        print(f"[{i}/{len(drug_dirs)}] {drug_name}: {evidence_level}")

    print(f"\n{'='*60}")
    print(f"Synced: {synced} drugs")
    print(f"Errors: {len(errors)}")

    if errors:
        print("\nErrors:")
        for err in errors:
            print(f"  - {err}")

    # Print statistics
    print(f"\n{'='*60}")
    print("Evidence Level Distribution:")

    # Count by evidence level
    level_counts = {"L1": 0, "L2": 0, "L3": 0, "L4": 0, "L5": 0}
    for drug_file in docs_drugs_dir.glob("*.md"):
        content = drug_file.read_text()
        match = re.search(r'evidence_level:\s*(L[1-5])', content)
        if match:
            level_counts[match.group(1)] += 1

    for level, count in sorted(level_counts.items()):
        print(f"  {level}: {count}")


if __name__ == "__main__":
    sync_notes_to_docs()
