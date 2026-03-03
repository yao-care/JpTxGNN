"""WHO ICTRP collector - fetches international clinical trial data."""

import requests
from typing import Any

from .base import BaseCollector, CollectorResult


class ICTRPCollector(BaseCollector):
    """Collector for WHO International Clinical Trials Registry Platform (ICTRP).

    Uses the ICTRP search portal to find trials from multiple registries worldwide.
    Note: ICTRP doesn't have a public API, so this uses web scraping-like approach
    with their search interface.
    """

    source_name = "ictrp"
    # ICTRP search URL (returns XML/JSON when available)
    SEARCH_URL = "https://trialsearch.who.int/Trial2.aspx"
    # Alternative API endpoint (if available)
    API_URL = "https://apps.who.int/trialsearch/api/v1/search"

    def __init__(self, max_results: int = 50):
        """Initialize the collector.

        Args:
            max_results: Maximum number of results to return per query
        """
        self.max_results = max_results

    def search(self, drug: str, disease: str | None = None) -> CollectorResult:
        """Search ICTRP for trials involving a drug and/or disease.

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
        search_query = " AND ".join(search_terms)

        try:
            # Try the API first
            trials = self._search_api(search_query)

            # If API fails or returns empty, try alternative approach
            if not trials:
                trials = self._search_alternative(search_query)

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

    def _search_api(self, query: str) -> list[dict]:
        """Try to search using API endpoint.

        Args:
            query: Search query string

        Returns:
            List of trial dictionaries
        """
        # Note: WHO ICTRP API access may require registration
        # This is a placeholder implementation
        params = {
            "query": query,
            "limit": self.max_results,
        }

        try:
            response = requests.get(
                self.API_URL,
                params=params,
                timeout=30,
                headers={"Accept": "application/json"},
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_api_response(data)
        except Exception:
            pass

        return []

    def _parse_api_response(self, data: dict) -> list[dict]:
        """Parse API response.

        Args:
            data: API response data

        Returns:
            List of parsed trial dictionaries
        """
        trials = []

        # The actual structure depends on the API response format
        items = data.get("results", data.get("trials", []))

        for item in items[:self.max_results]:
            trial = {
                "registry": item.get("register", "ICTRP"),
                "id": item.get("trialId", item.get("id", "")),
                "title": item.get("title", item.get("publicTitle", "")),
                "phase": item.get("phase", "N/A"),
                "status": item.get("recruitmentStatus", item.get("status", "")),
                "country": item.get("countries", item.get("country", "")),
                "enrollment": item.get("targetSize", "N/A"),
                "intervention": item.get("intervention", ""),
                "condition": item.get("condition", item.get("healthCondition", "")),
                "sponsor": item.get("primarySponsor", ""),
                "url": item.get("url", item.get("webAddress", "")),
            }
            trials.append(trial)

        return trials

    def _search_alternative(self, query: str) -> list[dict]:
        """Alternative search approach using web interface.

        Args:
            query: Search query string

        Returns:
            List of trial dictionaries (may be limited)
        """
        # This is a fallback - ICTRP web interface may require different handling
        # For now, return empty list with a note about limited access

        # In a production environment, you might:
        # 1. Use Selenium/Playwright for web scraping
        # 2. Use a proxy service
        # 3. Apply for official API access

        return []

    def search_by_registry(
        self, drug: str, registry: str = "ChiCTR"
    ) -> CollectorResult:
        """Search a specific registry through ICTRP.

        Supported registries include:
        - ChiCTR (Chinese Clinical Trial Registry)
        - CTRI (Clinical Trials Registry India)
        - DRKS (German Clinical Trials Register)
        - IRCT (Iranian Registry of Clinical Trials)
        - JPRN (Japan Primary Registries Network)
        - ANZCTR (Australian New Zealand Clinical Trials Registry)
        - And others...

        Args:
            drug: Drug name
            registry: Registry code

        Returns:
            CollectorResult with trial data from specific registry
        """
        query = {"drug": drug, "registry": registry}

        try:
            # Build registry-specific query
            search_query = f"{drug} AND register:{registry}"
            trials = self._search_api(search_query)

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
