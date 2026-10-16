#!/usr/bin/env python3
"""
Check ClinicalTrials.gov for new clinical trials related to our drug list.
Creates GitHub Issues when new trials are found.

NOTE: Filters out known/approved indications to focus on repurposing evidence.
"""

import json
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests

from github_utils import create_issue, close_older_clinicaltrials_issues


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
API_BASE = "https://clinicaltrials.gov/api/v2/studies"
CACHE_FILE = Path(__file__).parent.parent / "data" / "cache" / "clinicaltrials_cache.json"
DRUG_LIST_FILE = Path(__file__).parent / "drug_list.json"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY", "yao-care/EuTxGNN")
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



# --- 試驗與藥物的關係必須是結構化的介入角色（JpTxGNN #26713）---
# query.term 全文搜尋會把只在描述中提到藥名的試驗（例：安慰劑用的生理食鹽水、AI 工具研究）
# 也當成該藥的新試驗。改用 query.intr，並要求藥名出現在介入措施名稱／別名、且不是安慰劑組。
_SALTS = {"hydrochloride", "hcl", "sodium", "potassium", "calcium", "sulfate", "sulphate", "maleate", "fumarate",
          "tartrate", "citrate", "acetate", "mesylate", "besylate", "succinate", "phosphate", "bromide", "chloride"}


def _norm_name(text) -> str:
    import unicodedata
    t = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode().lower()
    return " ".join("".join(c if c.isalnum() else " " for c in t).split())


def _role_bound(study: dict, drug_name: str) -> bool:
    full = _norm_name(drug_name)
    core = " ".join(w for w in full.split() if w not in _SALTS) or full
    ivs = (study.get("protocolSection", {}).get("armsInterventionsModule", {}) or {}).get("interventions", []) or []
    for iv in ivs:
        name = _norm_name(iv.get("name", ""))
        if "placebo" in name:
            continue
        text = " " + " ".join([name] + [_norm_name(n) for n in (iv.get("otherNames") or [])]) + " "
        if (full and f" {full} " in text) or (core and f" {core} " in text):
            return True
    return False

def _clean_condition(name: str) -> str:
    name = re.sub(r"\s*\((disease|disorder)\)\s*", " ", name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip().replace('"', "")


def search_trials(drug_name: str, days_back: int = 7, conditions: list = None) -> list:
    """Search for trials updated in the last N days.

    2026-10-16：conditions 給預測新適應症時，只抓「藥＋這些疾病」的試驗。
    """
    min_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    params = {
        "query.intr": drug_name,
        "filter.advanced": f"AREA[LastUpdatePostDate]RANGE[{min_date},MAX]",
        "pageSize": 50,
        "fields": "NCTId,BriefTitle,OverallStatus,Phase,EnrollmentCount,Condition,LastUpdatePostDate,InterventionName,InterventionType,InterventionOtherName"
    }
    # ClinicalTrials.gov 對過長片語回 400「Too complicated query」：略過超過 6 個字的疾病名
    conds = [f'"{_clean_condition(c)}"' for c in (conditions or [])
             if len(_clean_condition(c)) > 3 and len(_clean_condition(c).split()) <= 6]
    if conditions and not conds:
        return []
    if conds:
        params["query.cond"] = " OR ".join(conds)

    try:
        response = requests.get(API_BASE, params=params, timeout=30)
        if response.status_code == 400 and len(conds) > 3:
            params["query.cond"] = " OR ".join(conds[:3])
            response = requests.get(API_BASE, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return [s for s in data.get("studies", []) if _role_bound(s, drug_name)]
    except requests.RequestException as e:
        print(f"Error searching trials for {drug_name}: {e}")
        return []


def create_github_issue(drug_name: str, new_trials: list, indications: list = None):
    """Create a GitHub Issue for new trials found."""
    indications = indications or []
    ind_label = "; ".join(indications[:2]) + (" …" if len(indications) > 2 else "")
    title = f"🔬 新臨床試驗：{drug_name} ({len(new_trials)} 筆)"
    if ind_label:
        title += f" → {ind_label}"  # 接在數量後面，github_utils 以「：…(」擷取藥名才對得上

    if not GITHUB_TOKEN:
        print(f"[DRY RUN] Would create issue for {drug_name} with {len(new_trials)} new trials")
        for trial in new_trials[:3]:
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
            f"- **Title**: {brief_title}\n"
            f"- **Status**: {status}\n"
            f"- **Phase**: {phase}\n"
            f"- **Enrollment**: {enrollment}\n"
            f"- **Link**: https://clinicaltrials.gov/study/{nct_id}\n"
        )

    body = f"""## 🔬 New Clinical Trials Detected

This issue was automatically created by GitHub Actions.

### Drug Name
{drug_name}

### Predicted New Indication(s)
{chr(10).join("- " + x for x in indications) if indications else "-"}

### NCT IDs
{", ".join(t.get("protocolSection", {}).get("identificationModule", {}).get("nctId", "") for t in new_trials)}

### Data Source
ClinicalTrials.gov

### Evidence Type
New/Updated Clinical Trials

### Details
Found **{len(new_trials)}** new or updated clinical trials:

{"".join(trial_details)}

### Suggested Actions
- [ ] Review trial details
- [ ] Evaluate if drug report evidence level needs updating
- [ ] Add trial information to report

---
*Auto-detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""

    # Create the issue with deduplication check
    labels = ["auto-detected", "needs-review", "clinicaltrials"]
    create_issue(title, body, labels)


def main():
    print("=" * 60)
    print("ClinicalTrials.gov Evidence Checker")
    print("(Filtering out known/approved indications)")
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
    skipped_known = 0

    for i, drug in enumerate(drugs):
        drug_name = drug["name"]
        predicted_indication = drug.get("predicted_indication", "")
        approved_indication = drug.get("approved_indication", "")

        # Skip if predicted indication is a known/approved indication
        if predicted_indication and approved_indication:
            if is_known_indication(approved_indication, predicted_indication):
                skipped_known += 1
                continue

        print(f"\n[{i+1}/{len(drugs)}] Checking: {drug_name}")

        predicted = drug.get("predicted_indications") or []
        if not predicted or not drug.get("inn"):
            continue
        trials = search_trials(drug["inn"], days_back=7, conditions=predicted)
        time.sleep(RATE_LIMIT_DELAY)

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
            if is_initial_discovery:
                print(f"  Initial discovery: {len(new_trials)} trials (baseline established)")
            # Skip if only 1 trial - wait for more evidence
            elif len(new_trials) < 2:
                print(f"  Only {len(new_trials)} trial found - below threshold")
            else:
                print(f"  Found {len(new_trials)} new trials!")
                conds = " ".join(" ".join(t.get("protocolSection", {}).get("conditionsModule", {}).get("conditions", [])) for t in new_trials).lower()
                new_findings.append({
                    "drug": drug_name,
                    "trials": new_trials,
                    "indications": [x for x in predicted if _clean_condition(x).lower() in conds] or predicted,
                })

        # Update seen trials
        seen_trials[drug_name] = drug_seen

    # Update cache
    cache["seen_trials"] = seen_trials
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
            create_github_issue(finding["drug"], finding["trials"], finding["indications"])
    else:
        print("No new trials found.")

    print(f"\nCompleted at: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
