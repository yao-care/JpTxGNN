#!/usr/bin/env python3
"""
Generate individual drug pages for Jekyll.

Creates markdown pages for each drug with predicted indications.

Output: docs/drugs/{drug-slug}/index.md
"""

import json
from datetime import datetime
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
DRUGS_DIR = DOCS_DIR / "drugs"
DATA_DIR = DOCS_DIR / "data"


def load_search_index():
    """Load the search index."""
    search_index_path = DATA_DIR / "search-index.json"
    with open(search_index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_drugs_json():
    """Load the drugs.json."""
    drugs_path = DATA_DIR / "drugs.json"
    with open(drugs_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_drug_page(drug: dict, drugs_info: dict) -> str:
    """Generate markdown content for a drug page."""
    slug = drug.get("slug", "")
    name = drug.get("name", "")
    drugbank_id = drug.get("drugbank_id", "")
    indications = drug.get("indications", [])

    # Get additional info from drugs.json
    drug_info = drugs_info.get(slug, {})
    original_indication = drug_info.get("original_indication", "")
    brand_names = drug_info.get("brand_names", [])

    # Build markdown content
    content = f"""---
layout: page
title: {name}
parent: 医薬品検索
nav_exclude: true
---

# {name}

## 基本情報

| 項目 | 値 |
|------|-----|
| DrugBank ID | [{drugbank_id}](https://go.drugbank.com/drugs/{drugbank_id}) |
| エビデンスレベル | L5（計算予測のみ） |
| 予測適応症数 | {len(indications)} |
"""

    if brand_names:
        content += f"| 日本商品名（例） | {', '.join(brand_names[:3])} |\n"

    if original_indication:
        content += f"""
## 承認適応症（KEGG）

{original_indication}
"""

    content += f"""
## 予測適応症（TxGNN）

以下は TxGNN 知識グラフにより予測された潜在的新適応症です。

| # | 適応症 | ソース | レベル |
|---|--------|--------|--------|
"""

    for i, ind in enumerate(indications, 1):
        ind_name = ind.get("name", "")
        ind_source = ind.get("source", "TxGNN")
        ind_level = ind.get("level", "L5")
        content += f"| {i} | {ind_name} | {ind_source} | {ind_level} |\n"

    content += """
## 免責事項

これらの予測は研究目的のみであり、医療アドバイスを構成するものではありません。
臨床応用には必ず適切な検証が必要です。

---

[← 医薬品検索に戻る](/drugs/)
"""

    return content


def main():
    print("Loading data...")

    # Load data
    search_index = load_search_index()
    drugs_data = load_drugs_json()

    # Build drugs info lookup
    drugs_info = {}
    for drug in drugs_data.get("drugs", []):
        drugs_info[drug["slug"]] = drug

    print(f"  - Search index: {len(search_index.get('drugs', []))} drugs")
    print(f"  - Drugs info: {len(drugs_info)} drugs")

    # Create drugs directory
    DRUGS_DIR.mkdir(parents=True, exist_ok=True)

    # Group drugs by slug to avoid duplicates
    drugs_by_slug = {}
    for drug in search_index.get("drugs", []):
        slug = drug.get("slug", "")
        if slug:
            if slug not in drugs_by_slug:
                drugs_by_slug[slug] = drug
            else:
                # Merge indications
                existing = drugs_by_slug[slug]
                existing_ind_names = {i["name"] for i in existing.get("indications", [])}
                for ind in drug.get("indications", []):
                    if ind["name"] not in existing_ind_names:
                        existing["indications"].append(ind)
                        existing_ind_names.add(ind["name"])

    print(f"  - Unique drug slugs: {len(drugs_by_slug)}")

    # Generate pages
    pages_created = 0
    for slug, drug in drugs_by_slug.items():
        # Create drug directory
        drug_dir = DRUGS_DIR / slug
        drug_dir.mkdir(parents=True, exist_ok=True)

        # Generate page content
        content = generate_drug_page(drug, drugs_info)

        # Write index.md
        page_path = drug_dir / "index.md"
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(content)

        pages_created += 1

    print(f"\nOutput: {DRUGS_DIR}")
    print(f"  - Pages created: {pages_created}")


if __name__ == "__main__":
    main()
