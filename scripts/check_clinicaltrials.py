#!/usr/bin/env python3
"""
Check ClinicalTrials.gov for new clinical trials related to our drug list.
Creates GitHub Issues when new trials are found.
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests

from github_utils import create_issue, issue_exists, close_older_clinicaltrials_issues

# Configuration
API_BASE = "https://clinicaltrials.gov/api/v2/studies"
CACHE_FILE = Path(__file__).parent.parent / "data" / "cache" / "clinicaltrials_cache.json"
DRUG_LIST_FILE = Path(__file__).parent / "drug_list.json"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY", "yao-care/JpTxGNN")
RATE_LIMIT_DELAY = 0.5  # seconds between API calls


def load_cache() -> dict:
    """Load the cache of previously seen trial IDs."""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_check": None, "seen_trials": {}}


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


def search_trials(drug_name: str, days_back: int = 7) -> list:
    """Search for trials updated in the last N days."""
    min_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    params = {
        "query.term": drug_name,
        "filter.advanced": f"AREA[LastUpdatePostDate]RANGE[{min_date},MAX]",
        "pageSize": 50,
        "fields": "NCTId,BriefTitle,OverallStatus,Phase,EnrollmentCount,Condition,LastUpdatePostDate"
    }

    try:
        response = requests.get(API_BASE, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("studies", [])
    except requests.RequestException as e:
        print(f"Error searching trials for {drug_name}: {e}")
        return []


def create_github_issue(drug_name: str, new_trials: list):
    """Create a GitHub Issue for new trials found."""
    title = f"🔬 新臨床試驗：{drug_name} ({len(new_trials)} 筆)"

    if not GITHUB_TOKEN:
        print(f"[DRY RUN] Would create issue for {drug_name} with {len(new_trials)} new trials")
        for trial in new_trials[:3]:  # Show first 3
            nct_id = trial.get("protocolSection", {}).get("identificationModule", {}).get("nctId", "Unknown")
            brief_title = trial.get("protocolSection", {}).get("identificationModule", {}).get("briefTitle", "Unknown")
            print(f"  - {nct_id}: {brief_title[:60]}...")
        return

    # Close older issues for this drug before creating a new one
    closed_count = close_older_clinicaltrials_issues(drug_name)
    if closed_count > 0:
        print(f"  → Closed {closed_count} older issue(s) for {drug_name}")

    # Format trial details
    trial_details = []
    for trial in new_trials:
        protocol = trial.get("protocolSection", {})
        id_module = protocol.get("identificationModule", {})
        status_module = protocol.get("statusModule", {})
        design_module = protocol.get("designModule", {})

        nct_id = id_module.get("nctId", "Unknown")
        brief_title = id_module.get("briefTitle", "Unknown")
        status = status_module.get("overallStatus", "Unknown")
        phase = ", ".join(design_module.get("phases", ["Unknown"]))
        enrollment = design_module.get("enrollmentInfo", {}).get("count", "Unknown")

        trial_details.append(
            f"### {nct_id}\n"
            f"- **標題**: {brief_title}\n"
            f"- **狀態**: {status}\n"
            f"- **階段**: {phase}\n"
            f"- **人數**: {enrollment}\n"
            f"- **連結**: https://clinicaltrials.gov/study/{nct_id}\n"
        )

    body = f"""## 🔬 自動偵測到新臨床試驗

此 Issue 由 GitHub Actions 自動建立。

### 藥物名稱
{drug_name}

### 資料來源
ClinicalTrials.gov

### 證據類型
新臨床試驗

### 詳細資訊
發現 **{len(new_trials)}** 個新的或更新的臨床試驗：

{"".join(trial_details)}

### 建議行動
- [ ] 檢視臨床試驗內容
- [ ] 評估是否需要更新藥物報告證據等級
- [ ] 新增臨床試驗資訊到報告

---
*自動偵測時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""

    # Create the issue with deduplication check
    labels = ["auto-detected", "needs-review", "clinicaltrials"]
    create_issue(title, body, labels)


def main():
    print("=" * 60)
    print("ClinicalTrials.gov Evidence Checker")
    print(f"Started at: {datetime.now().isoformat()}")
    print("=" * 60)

    # Load data
    cache = load_cache()
    drugs = load_drug_list()

    print(f"Loaded {len(drugs)} drugs from drug list")
    print(f"Last check: {cache.get('last_check', 'Never')}")

    # Check each drug
    new_findings = []
    seen_trials = cache.get("seen_trials", {})

    for i, drug in enumerate(drugs):
        drug_name = drug["name"]
        print(f"\n[{i+1}/{len(drugs)}] Checking: {drug_name}")

        trials = search_trials(drug_name, days_back=7)
        time.sleep(RATE_LIMIT_DELAY)  # Rate limiting

        if not trials:
            continue

        # Filter to truly new trials
        drug_seen = seen_trials.get(drug_name, [])
        is_initial_discovery = not drug_seen  # First time checking this drug
        new_trials = []

        for trial in trials:
            nct_id = trial.get("protocolSection", {}).get("identificationModule", {}).get("nctId")
            if nct_id and nct_id not in drug_seen:
                new_trials.append(trial)
                drug_seen.append(nct_id)

        if new_trials:
            # Skip issue creation for initial discovery (first time seeing this drug)
            # Only create issues for truly new trials after baseline is established
            if is_initial_discovery:
                print(f"  Initial discovery: {len(new_trials)} trials (no issue created, baseline established)")
            # Skip if only 1 trial - too noisy, wait for more evidence
            elif len(new_trials) < 2:
                print(f"  Only {len(new_trials)} trial found - below threshold, skipping issue")
            else:
                print(f"  Found {len(new_trials)} new trials!")
                new_findings.append({
                    "drug": drug_name,
                    "trials": new_trials
                })

        # Update seen trials
        seen_trials[drug_name] = drug_seen

    # Update cache
    cache["seen_trials"] = seen_trials
    save_cache(cache)

    # Create issues for new findings
    print("\n" + "=" * 60)
    print("Creating Issues for New Findings")
    print("=" * 60)

    if new_findings:
        for finding in new_findings:
            create_github_issue(finding["drug"], finding["trials"])
    else:
        print("No new trials found.")

    print(f"\nCompleted at: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
