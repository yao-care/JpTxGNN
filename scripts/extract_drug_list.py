#!/usr/bin/env python3
"""
Extract drug list from docs/_drugs/*.md files.
Creates a JSON file with drug names, evidence levels, and indication counts.
"""

import json
import re
from pathlib import Path


def parse_front_matter(content: str) -> dict:
    """Parse YAML front matter from markdown content."""
    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    front_matter = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            front_matter[key] = value

    return front_matter


def extract_predicted_indication(content: str) -> str:
    """Extract predicted indication from the drug report."""
    # Look for the pattern in the quick overview table
    match = re.search(r'\|\s*預測新適應症\s*\|\s*([^|]+)\s*\|', content)
    if match:
        return match.group(1).strip()
    return ""


def main():
    drugs_dir = Path(__file__).parent.parent / "docs" / "_drugs"
    output_file = Path(__file__).parent / "drug_list.json"

    drugs = []

    for md_file in sorted(drugs_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        front_matter = parse_front_matter(content)

        drug_name = front_matter.get("title", md_file.stem)
        evidence_level = front_matter.get("evidence_level", "")
        indication_count = front_matter.get("indication_count", "0")

        # Extract predicted indication for search queries
        predicted_indication = extract_predicted_indication(content)

        drugs.append({
            "name": drug_name,
            "file": md_file.name,
            "evidence_level": evidence_level,
            "indication_count": int(indication_count) if indication_count.isdigit() else 0,
            "predicted_indication": predicted_indication
        })

    # Save to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "total": len(drugs),
            "generated_at": __import__("datetime").datetime.now().isoformat(),
            "drugs": drugs
        }, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(drugs)} drugs to {output_file}")

    # Print summary
    level_counts = {}
    for drug in drugs:
        level = drug["evidence_level"] or "Unknown"
        level_counts[level] = level_counts.get(level, 0) + 1

    print("\nEvidence level distribution:")
    for level in sorted(level_counts.keys()):
        print(f"  {level}: {level_counts[level]}")


if __name__ == "__main__":
    main()
