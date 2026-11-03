#!/usr/bin/env python3
"""
GitHub API utilities for TwTxGNN evidence checking scripts.
Provides deduplication and issue management functions.
"""

import os
import re
import requests
from typing import Optional, List

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY", "yao-care/JpTxGNN")

# 證據監測 issue 標題的藥名擷取：「🔬 新臨床試驗：DrugName (N 筆) → …」。
# 半形與全形冒號都接受；以「(數字」收尾，藥名本身帶括號（例：Insulin (human)）也擷取得到。
ISSUE_DRUG_RE = re.compile(r'[:：]\s*(.+?)\s*\(\d+')


def get_headers() -> dict:
    """Get GitHub API headers（沒有 token 時不送 Authorization，供唯讀查詢用）。"""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def list_issues(params: dict, max_pages: int = 200) -> List[dict]:
    """列出 repo 的 issue，依 Link header 分頁取全部（排除 pull request）。

    舊版只取第一頁 100 筆，issue 多的站（數千筆）去重與關舊 issue 都會漏看。
    出錯時拋出 requests.RequestException，由呼叫端決定怎麼處理。
    """
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    params = dict(params)
    params.setdefault("per_page", 100)
    issues = []
    for _ in range(max_pages):
        response = requests.get(url, headers=get_headers(), params=params, timeout=30)
        response.raise_for_status()
        issues.extend(i for i in response.json() if "pull_request" not in i)
        next_url = response.links.get("next", {}).get("url")
        if not next_url:
            break
        url, params = next_url, None  # next 連結已帶齊查詢參數
    return issues


def list_issue_comments(issue_number: int) -> List[dict]:
    """列出單一 issue 的全部留言（分頁）。"""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues/{issue_number}/comments"
    params = {"per_page": 100}
    comments = []
    for _ in range(50):
        response = requests.get(url, headers=get_headers(), params=params, timeout=30)
        response.raise_for_status()
        comments.extend(response.json())
        next_url = response.links.get("next", {}).get("url")
        if not next_url:
            break
        url, params = next_url, None
    return comments


_ISSUE_TITLE_CACHE = {}


def issue_exists(title: str, state: str = "all") -> bool:
    """
    Check if an issue with the given title already exists.

    Args:
        title: The exact issue title to search for
        state: "open", "closed", or "all" (default: "all")

    Returns:
        True if an issue with this title exists, False otherwise
    """
    if not GITHUB_TOKEN:
        print(f"[DRY RUN] Would check for existing issue: {title}")
        return False

    # GitHub API doesn't support exact title search, so we fetch and filter.
    # 分頁取全部；同一次執行內只抓一次，之後新開的 issue 由 create_issue 補進快取
    try:
        if state not in _ISSUE_TITLE_CACHE:
            _ISSUE_TITLE_CACHE[state] = {
                i.get("title"): i["number"]
                for i in list_issues({"state": state, "labels": "auto-detected"})
            }
        number = _ISSUE_TITLE_CACHE[state].get(title)
        if number is not None:
            print(f"  → Issue already exists: #{number} - {title}")
            return True

        return False

    except requests.RequestException as e:
        print(f"Warning: Could not check for existing issues: {e}")
        # If we can't check, assume it doesn't exist to avoid blocking
        return False


def find_existing_tfda_issues(drug_name: str, state: str = "open") -> List[dict]:
    """
    Find existing TFDA issues for a specific drug.

    Args:
        drug_name: The drug name to search for
        state: "open", "closed", or "all" (default: "open")

    Returns:
        List of matching issues (sorted by number, newest first)
    """
    if not GITHUB_TOKEN:
        print(f"[DRY RUN] Would search for TFDA issues: {drug_name}")
        return []

    try:
        issues = list_issues({"state": state, "labels": "tfda"})

        # Filter issues matching the drug name pattern
        # Title format: 🏥 TFDA 許可證變更：DrugName (N 筆)
        matching = []
        drug_name_lower = drug_name.lower()
        for issue in issues:
            title = issue.get("title", "")
            match = re.search(r'：(.+?)\s*\(', title)
            if match:
                issue_drug = match.group(1).strip().lower()
                if issue_drug == drug_name_lower:
                    matching.append({
                        "number": issue["number"],
                        "title": issue["title"],
                        "url": issue["html_url"]
                    })

        # Sort by issue number (newest first)
        matching.sort(key=lambda x: x["number"], reverse=True)
        return matching

    except requests.RequestException as e:
        print(f"Warning: Could not search for existing issues: {e}")
        return []


def close_issue(issue_number: int, comment: str = None, state_reason: str = None) -> bool:
    """
    Close a GitHub issue with an optional comment.

    Args:
        issue_number: The issue number to close
        comment: Optional comment to add before closing
        state_reason: Optional "completed" or "not_planned"

    Returns:
        True if successful, False otherwise
    """
    if not GITHUB_TOKEN:
        print(f"[DRY RUN] Would close issue #{issue_number}")
        return True

    try:
        # Add comment if provided
        if comment:
            comment_url = f"https://api.github.com/repos/{GITHUB_REPO}/issues/{issue_number}/comments"
            requests.post(comment_url, headers=get_headers(), json={"body": comment}, timeout=30)

        # Close the issue
        url = f"https://api.github.com/repos/{GITHUB_REPO}/issues/{issue_number}"
        payload = {"state": "closed"}
        if state_reason:
            payload["state_reason"] = state_reason
        response = requests.patch(url, headers=get_headers(), json=payload, timeout=30)
        response.raise_for_status()
        print(f"  → Closed issue #{issue_number}")
        return True

    except requests.RequestException as e:
        print(f"Error closing issue #{issue_number}: {e}")
        return False


def close_older_tfda_issues(drug_name: str) -> int:
    """
    Close older TFDA issues for a drug, keeping only the latest.

    Args:
        drug_name: The drug name to process

    Returns:
        Number of issues closed
    """
    existing = find_existing_tfda_issues(drug_name, state="open")

    if len(existing) <= 1:
        return 0

    # Keep the first (newest), close the rest
    closed_count = 0
    for issue in existing[1:]:
        comment = f"🤖 自動關閉：已有更新的 issue #{existing[0]['number']} 追蹤此藥物的許可證變更。"
        if close_issue(issue["number"], comment):
            closed_count += 1

    return closed_count


def find_existing_issues_by_label(drug_name: str, label: str, state: str = "open") -> List[dict]:
    """
    Find existing issues for a specific drug with a given label.

    Args:
        drug_name: The drug name to search for
        label: The label to filter by (e.g., "pubmed", "clinicaltrials")
        state: "open", "closed", or "all" (default: "open")

    Returns:
        List of matching issues (sorted by number, newest first)
    """
    if not GITHUB_TOKEN:
        print(f"[DRY RUN] Would search for {label} issues: {drug_name}")
        return []

    try:
        issues = list_issues({"state": state, "labels": label})

        # Filter issues matching the drug name pattern
        # Title formats:
        # - 📚 新文獻：DrugName (N 篇) → …
        # - 🔬 新臨床試驗：DrugName (N 筆) → …
        matching = []
        drug_name_lower = drug_name.lower()
        for issue in issues:
            title = issue.get("title", "")
            match = ISSUE_DRUG_RE.search(title)
            if match:
                issue_drug = match.group(1).strip().lower()
                if issue_drug == drug_name_lower:
                    matching.append({
                        "number": issue["number"],
                        "title": issue["title"],
                        "url": issue["html_url"]
                    })

        # Sort by issue number (newest first)
        matching.sort(key=lambda x: x["number"], reverse=True)
        return matching

    except requests.RequestException as e:
        print(f"Warning: Could not search for existing issues: {e}")
        return []


def close_older_issues_by_label(drug_name: str, label: str, issue_type: str) -> int:
    """
    Close older issues for a drug with a specific label, keeping only the latest.

    Args:
        drug_name: The drug name to process
        label: The label to filter by (e.g., "pubmed", "clinicaltrials")
        issue_type: Human-readable description for the comment (e.g., "文獻", "臨床試驗")

    Returns:
        Number of issues closed
    """
    existing = find_existing_issues_by_label(drug_name, label, state="open")

    if len(existing) <= 1:
        return 0

    # Keep the first (newest), close the rest
    closed_count = 0
    for issue in existing[1:]:
        comment = f"🤖 自動關閉：已有更新的 issue #{existing[0]['number']} 追蹤此藥物的{issue_type}。"
        if close_issue(issue["number"], comment):
            closed_count += 1

    return closed_count


def close_older_pubmed_issues(drug_name: str) -> int:
    """Close older PubMed issues for a drug."""
    return close_older_issues_by_label(drug_name, "pubmed", "新文獻")


def close_older_clinicaltrials_issues(drug_name: str) -> int:
    """Close older ClinicalTrials issues for a drug."""
    return close_older_issues_by_label(drug_name, "clinicaltrials", "新臨床試驗")


def create_issue(title: str, body: str, labels: list) -> Optional[str]:
    """
    Create a GitHub issue with deduplication check.

    Args:
        title: Issue title
        body: Issue body (markdown)
        labels: List of label names

    Returns:
        Issue URL if created, None if skipped or failed
    """
    if not GITHUB_TOKEN:
        print(f"[DRY RUN] Would create issue: {title}")
        return None

    # Check if issue already exists
    if issue_exists(title):
        print(f"  → Skipping duplicate issue: {title}")
        return None

    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    payload = {
        "title": title,
        "body": body,
        "labels": labels
    }

    try:
        response = requests.post(url, headers=get_headers(), json=payload, timeout=30)
        response.raise_for_status()
        created = response.json()
        issue_url = created.get("html_url")
        for titles in _ISSUE_TITLE_CACHE.values():
            titles[title] = created.get("number")
        print(f"  → Created issue: {issue_url}")
        return issue_url

    except requests.RequestException as e:
        print(f"Error creating issue: {e}")
        return None
