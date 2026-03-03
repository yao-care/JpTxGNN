"""ClinicalTrials.gov collector - fetches clinical trial data via API."""

import requests
from typing import Any

from .base import BaseCollector, CollectorResult


class ClinicalTrialsCollector(BaseCollector):
    """Collector for ClinicalTrials.gov clinical trial data.

    Uses the ClinicalTrials.gov API v2 to search for trials.
    API docs: https://clinicaltrials.gov/data-api/api
    """

    source_name = "clinicaltrials"
    BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

    def __init__(self, max_results: int = 50):
        """Initialize the collector.

        Args:
            max_results: Maximum number of results to return per query
        """
        self.max_results = max_results

    def search(self, drug: str, disease: str | None = None) -> CollectorResult:
        """Search for clinical trials involving a drug and/or disease.

        Args:
            drug: Drug name
            disease: Disease/indication name (optional)

        Returns:
            CollectorResult with trial data
        """
        query = {"drug": drug, "disease": disease}

        # Build search query
        search_terms = [drug]
        if disease:
            search_terms.append(disease)

        params = {
            "query.term": " AND ".join(search_terms),
            "pageSize": self.max_results,
            "format": "json",
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            # Parse the results
            trials = self._parse_trials(data)

            return self._make_result(
                query=query,
                data=trials,
                success=True,
            )

        except requests.RequestException as e:
            return self._make_result(
                query=query,
                data=[],
                success=False,
                error_message=str(e),
            )

    def _parse_trials(self, data: dict) -> list[dict]:
        """Parse the API response into a list of trial summaries.

        Args:
            data: Raw API response

        Returns:
            List of parsed trial dictionaries
        """
        trials = []
        studies = data.get("studies", [])

        for study in studies:
            protocol = study.get("protocolSection", {})
            identification = protocol.get("identificationModule", {})
            status = protocol.get("statusModule", {})
            design = protocol.get("designModule", {})
            description = protocol.get("descriptionModule", {})
            eligibility = protocol.get("eligibilityModule", {})
            outcomes = protocol.get("outcomesModule", {})
            contacts = protocol.get("contactsLocationsModule", {})

            # Extract locations/countries
            locations = contacts.get("locations", [])
            countries = list(set(loc.get("country", "") for loc in locations if loc.get("country")))

            # Extract primary outcomes
            primary_outcomes = outcomes.get("primaryOutcomes", [])
            endpoints = [po.get("measure", "") for po in primary_outcomes[:3]]

            trial = {
                "registry": "ClinicalTrials.gov",
                "id": identification.get("nctId", ""),
                "title": identification.get("officialTitle") or identification.get("briefTitle", ""),
                "phase": ", ".join(design.get("phases", [])) or "N/A",
                "status": status.get("overallStatus", ""),
                "start_date": status.get("startDateStruct", {}).get("date", ""),
                "completion_date": status.get("completionDateStruct", {}).get("date", ""),
                "country": ", ".join(countries) if countries else "N/A",
                "enrollment": design.get("enrollmentInfo", {}).get("count", "N/A"),
                "brief_summary": description.get("briefSummary", "")[:500],
                "eligibility_criteria": eligibility.get("eligibilityCriteria", "")[:300],
                "endpoints": endpoints,
                "sponsor": identification.get("organization", {}).get("fullName", ""),
                "url": f"https://clinicaltrials.gov/study/{identification.get('nctId', '')}",
            }
            trials.append(trial)

        return trials

    def get_trial_details(self, nct_id: str) -> dict | None:
        """Get detailed information for a specific trial.

        Args:
            nct_id: NCT identifier (e.g., "NCT01234567")

        Returns:
            Trial details or None if not found
        """
        url = f"{self.BASE_URL}/{nct_id}"

        try:
            response = requests.get(url, params={"format": "json"}, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None
