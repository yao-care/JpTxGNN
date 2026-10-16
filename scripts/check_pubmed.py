#!/usr/bin/env python3
"""
Check PubMed for new publications related to our drug list.
Creates GitHub Issues when new papers are found.

NOTE: Filters out known/approved indications to focus on repurposing evidence.
"""

import json
import os
import re
import time
from datetime import datetime
from pathlib import Path

import requests

from github_utils import create_issue, close_older_pubmed_issues


def is_known_indication(approved_indication: str, predicted_indication: str) -> bool:
    """Check if predicted indication overlaps with approved indication.

    Uses keyword matching to detect if the predicted indication is likely
    already approved for the drug.
    """
    if not approved_indication or not predicted_indication:
        return False

    approved_lower = approved_indication.lower()
    predicted_lower = predicted_indication.lower()

    # Extract meaningful keywords from predicted indication
    cleaned = re.sub(r'\s*\(disease\)\s*', ' ', predicted_lower)
    cleaned = re.sub(r'\s*\(disorder\)\s*', ' ', cleaned)
    cleaned = re.sub(r'[^\w\s]', ' ', cleaned)

    words = cleaned.split()

    # Generic medical terms that are too broad for matching
    generic_terms = {
        'disease', 'disorder', 'syndrome', 'type', 'of', 'the', 'and', 'or',
        'with', 'due', 'to', 'in', 'by', 'for', 'as', 'is', 'a', 'an',
        'primary', 'secondary', 'chronic', 'acute', 'severe', 'mild',
        'familial', 'hereditary', 'congenital', 'acquired', 'idiopathic',
        'cancer', 'tumor', 'carcinoma', 'neoplasm', 'infection', 'infectious',
        'deficiency', 'failure', 'insufficiency', 'inflammation',
        'cell', 'cells', 'blood', 'bone', 'muscle', 'nerve', 'skin',
    }

    # Keep important acronyms even if short
    important_acronyms = {
        'hiv', 'aids', 'copd', 'adhd', 'als', 'ms', 'ibd', 'ibs',
        'hcv', 'hbv', 'tb', 'ra', 'sle', 'ckd', 'chf', 'cad',
    }

    # Expanded forms for acronyms
    expanded_terms = {
        'hiv': 'immunodeficiency virus',
        'aids': 'acquired immunodeficiency',
        'copd': 'chronic obstructive pulmonary',
        'adhd': 'attention deficit',
        'als': 'amyotrophic lateral sclerosis',
    }

    keywords = []
    for w in words:
        w_lower = w.lower()
        if w_lower in important_acronyms:
            keywords.append(w_lower)
        elif w_lower not in generic_terms and len(w) > 4:
            keywords.append(w_lower)

    if not keywords:
        return False

    # Check if specific keywords appear in approved indication
    matches = 0
    for kw in keywords:
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, approved_lower):
            matches += 1
        elif kw in expanded_terms:
            if expanded_terms[kw] in approved_lower:
                matches += 1

    # Need majority of specific keywords to match
    if len(keywords) >= 2 and matches >= len(keywords) * 0.6:
        return True

    # Single very specific keyword match
    for kw in keywords:
        if len(kw) > 8:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, approved_lower):
                return True
        elif kw in expanded_terms and expanded_terms[kw] in approved_lower:
            return True

    return False

# Configuration
ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
CACHE_FILE = Path(__file__).parent.parent / "data" / "cache" / "pubmed_cache.json"
DRUG_LIST_FILE = Path(__file__).parent / "drug_list.json"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY", "yao-care/EuTxGNN")
NCBI_API_KEY = os.environ.get("NCBI_API_KEY")  # Optional, for higher rate limits
RATE_LIMIT_DELAY = 0.4 if NCBI_API_KEY else 1.0  # seconds between API calls


def load_cache() -> dict:
    """Load the cache of previously seen PMIDs."""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_check": None, "seen_pmids": {}}


def save_cache(cache: dict):
    """Save the cache."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    cache["last_check"] = datetime.now().isoformat()
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def load_drug_list() -> list:
    """Load the drug list."""
    with open(DRUG_LIST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["drugs"]


def search_pubmed(drug_name: str, indication: str = "", days_back: int = 7) -> list:
    """Search PubMed for recent publications."""
    # Build search query
    query_parts = [f'"{drug_name}"[Title/Abstract]']
    if indication:
        # Clean up indication text
        indication = indication.split("(")[0].strip()
        if indication and len(indication) > 3:
            query_parts.append(f'"{indication}"[Title/Abstract]')

    query = " AND ".join(query_parts)

    params = {
        "db": "pubmed",
        "term": query,
        "datetype": "edat",  # Entry date
        "reldate": days_back,  # Last N days
        "retmode": "json",
        "retmax": 50,
        "sort": "date"
    }

    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY

    try:
        response = requests.get(ESEARCH_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        id_list = data.get("esearchresult", {}).get("idlist", [])
        return id_list
    except requests.RequestException as e:
        print(f"Error searching PubMed for {drug_name}: {e}")
        return []


def _clean_indication(name: str) -> str:
    name = re.sub(r"\s*\((disease|disorder)\)\s*", " ", name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip().replace('"', "")


def search_pubmed_predicted(inn: str, indications: list, days_back: int = 7) -> list:
    """2026-10-16：查「INN AND (預測新適應症1 OR …)」，只抓和預測有關的新文獻。"""
    terms = [f'"{_clean_indication(i)}"[Title/Abstract]' for i in indications if len(_clean_indication(i)) > 3]
    if not terms:
        return []
    query = f'"{inn}"[Title/Abstract] AND (' + " OR ".join(terms) + ")"
    params = {
        "db": "pubmed",
        "term": query,
        "datetype": "edat",
        "reldate": days_back,
        "retmode": "json",
        "retmax": 50,
        "sort": "date",
    }
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    try:
        response = requests.get(ESEARCH_URL, params=params, timeout=30)
        response.raise_for_status()
        return response.json().get("esearchresult", {}).get("idlist", [])
    except requests.RequestException as e:
        print(f"Error searching PubMed for {inn}: {e}")
        return []


def matched_indications(papers: list, indications: list) -> list:
    """以論文標題比對命中哪些預測新適應症；比對不到就回傳空串列。"""
    titles = " ".join(p.get("title", "") for p in papers).lower()
    return [i for i in indications if _clean_indication(i).lower() in titles]


def get_paper_details(pmids: list) -> list:
    """Get details for a list of PMIDs."""
    if not pmids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json"
    }

    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY

    try:
        response = requests.get(ESUMMARY_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        result = data.get("result", {})
        papers = []

        for pmid in pmids:
            paper_data = result.get(pmid, {})
            if paper_data and "title" in paper_data:
                papers.append({
                    "pmid": pmid,
                    "title": paper_data.get("title", ""),
                    "source": paper_data.get("source", ""),
                    "pubdate": paper_data.get("pubdate", ""),
                    "authors": [a.get("name", "") for a in paper_data.get("authors", [])[:3]]
                })

        return papers
    except requests.RequestException as e:
        print(f"Error getting paper details: {e}")
        return []


def create_github_issue(drug_name: str, new_papers: list, indications: list = None):
    """Create a GitHub Issue for new papers found."""
    indications = indications or []
    ind_label = "; ".join(indications[:2]) + (" …" if len(indications) > 2 else "")
    title = f"📚 新文獻：{drug_name} ({len(new_papers)} 篇)"
    if ind_label:
        title += f" → {ind_label}"  # 接在數量後面，github_utils 以「：…(」擷取藥名才對得上

    if not GITHUB_TOKEN:
        print(f"[DRY RUN] Would create issue for {drug_name} with {len(new_papers)} new papers")
        for paper in new_papers[:3]:
            print(f"  - PMID {paper['pmid']}: {paper['title'][:60]}...")
        return

    # Close older issues for this drug before creating a new one
    closed_count = close_older_pubmed_issues(drug_name)
    if closed_count > 0:
        print(f"  → Closed {closed_count} older issue(s) for {drug_name}")

    # Format paper details
    paper_details = []
    for paper in new_papers:
        authors = ", ".join(paper["authors"]) + (" et al." if len(paper["authors"]) >= 3 else "")
        paper_details.append(
            f"### PMID: {paper['pmid']}\n"
            f"- **Title**: {paper['title']}\n"
            f"- **Journal**: {paper['source']}\n"
            f"- **Publication Date**: {paper['pubdate']}\n"
            f"- **Authors**: {authors}\n"
            f"- **Link**: https://pubmed.ncbi.nlm.nih.gov/{paper['pmid']}/\n"
        )

    body = f"""## 📚 New Publications Detected

This issue was automatically created by GitHub Actions.

### Drug Name
{drug_name}

### Predicted New Indication(s)
{chr(10).join("- " + x for x in indications) if indications else "-"}

### PMIDs
{", ".join(p["pmid"] for p in new_papers)}

### Data Source
PubMed

### Evidence Type
New Academic Publications

### Details
Found **{len(new_papers)}** new publications:

{"".join(paper_details)}

### Suggested Actions
- [ ] Review paper abstracts
- [ ] Evaluate publication type (RCT, observational, case report, etc.)
- [ ] Evaluate if drug report evidence level needs updating
- [ ] Add publication information to report

---
*Auto-detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""

    # Create the issue with deduplication check
    labels = ["auto-detected", "needs-review", "pubmed"]
    create_issue(title, body, labels)


def main():
    print("=" * 60)
    print("PubMed Evidence Checker")
    print("(Filtering out known/approved indications)")
    print(f"Started at: {datetime.now().isoformat()}")
    print(f"NCBI API Key: {'Configured' if NCBI_API_KEY else 'Not configured (slower rate limit)'}")
    print("=" * 60)

    # Load data
    cache = load_cache()
    drugs = load_drug_list()

    print(f"Loaded {len(drugs)} drugs from drug list")
    print(f"Last check: {cache.get('last_check', 'Never')}")

    # Check each drug
    new_findings = []
    seen_pmids = cache.get("seen_pmids", {})
    skipped_known = 0

    for i, drug in enumerate(drugs):
        drug_name = drug["name"]
        indication = drug.get("predicted_indication", "")
        approved_indication = drug.get("approved_indication", "")

        # Skip if predicted indication is a known/approved indication
        if indication and approved_indication:
            if is_known_indication(approved_indication, indication):
                skipped_known += 1
                continue

        print(f"\n[{i+1}/{len(drugs)}] Checking: {drug_name}")

        predicted = drug.get("predicted_indications") or []
        if not predicted or not drug.get("inn"):
            continue
        pmids = search_pubmed_predicted(drug["inn"], predicted, days_back=7)
        time.sleep(RATE_LIMIT_DELAY)

        if not pmids:
            continue

        # Filter to truly new papers
        drug_seen = seen_pmids.get(drug_name, [])
        is_initial_discovery = not drug_seen  # First time checking this drug
        new_pmids = [p for p in pmids if p not in drug_seen]

        if new_pmids:
            # Get paper details
            papers = get_paper_details(new_pmids)
            time.sleep(RATE_LIMIT_DELAY)

            if papers:
                # Skip issue creation for initial discovery
                if is_initial_discovery:
                    print(f"  Initial discovery: {len(papers)} papers (baseline established)")
                # Skip if only 1 paper - wait for more evidence
                elif len(papers) < 2:
                    print(f"  Only {len(papers)} paper found - below threshold")
                else:
                    print(f"  Found {len(papers)} new papers!")
                    new_findings.append({
                        "drug": drug_name,
                        "papers": papers,
                        "indications": matched_indications(papers, predicted) or predicted,
                    })

            # Update seen PMIDs
            drug_seen.extend(new_pmids)

        seen_pmids[drug_name] = drug_seen

    # Update cache
    cache["seen_pmids"] = seen_pmids
    save_cache(cache)

    # Create issues for new findings
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Skipped (known indications): {skipped_known}")

    if new_findings:
        print(f"New findings: {len(new_findings)}")
        print("\nCreating Issues...")
        for finding in new_findings:
            create_github_issue(finding["drug"], finding["papers"], finding["indications"])
    else:
        print("No new papers found.")

    print(f"\nCompleted at: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
