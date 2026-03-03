"""PMDA (Pharmaceuticals and Medical Devices Agency) collector.

Collects drug approval information and safety alerts from PMDA Japan.

PMDA Website: https://www.pmda.go.jp/
"""

import re
import time
from typing import Any
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup

from .base import BaseCollector, CollectorResult


class PMDACollector(BaseCollector):
    """Collector for PMDA drug information."""

    source_name = "pmda"

    BASE_URL = "https://www.pmda.go.jp"
    SEARCH_URL = "https://www.pmda.go.jp/PmdaSearch/iyakuSearch/"

    # Rate limiting
    REQUEST_DELAY = 1.0  # seconds between requests

    def __init__(self):
        self._last_request_time = 0

    def _rate_limit(self):
        """Ensure rate limiting between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.REQUEST_DELAY:
            time.sleep(self.REQUEST_DELAY - elapsed)
        self._last_request_time = time.time()

    def _fetch_url(self, url: str) -> str:
        """Fetch URL content with rate limiting."""
        self._rate_limit()

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; JpTxGNN/1.0; +https://jptxgnn.yao.care)",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "ja,en;q=0.9",
        }

        request = Request(url, headers=headers)

        try:
            with urlopen(request, timeout=30) as response:
                return response.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError) as e:
            raise RuntimeError(f"Failed to fetch {url}: {e}")

    def search(self, drug: str, disease: str | None = None) -> CollectorResult:
        """Search for drug information on PMDA.

        Args:
            drug: Drug name (Japanese or English)
            disease: Disease name (optional, used for filtering)

        Returns:
            CollectorResult with PMDA search results
        """
        query = {"drug": drug, "disease": disease}

        try:
            results = self._search_drug(drug)

            # Filter by disease if provided
            if disease and results:
                results = [
                    r for r in results
                    if disease.lower() in r.get("indication", "").lower()
                    or disease in r.get("indication", "")
                ]

            return self._make_result(
                query=query,
                data={
                    "results": results,
                    "total": len(results),
                },
                success=True,
            )

        except Exception as e:
            return self._make_result(
                query=query,
                data=None,
                success=False,
                error_message=str(e),
            )

    def _search_drug(self, drug_name: str) -> list[dict]:
        """Search for a drug on PMDA website."""
        # PMDA search uses a form-based interface
        # We'll scrape the search results
        search_url = f"{self.SEARCH_URL}?srhKey={quote(drug_name)}"

        try:
            html = self._fetch_url(search_url)
            return self._parse_search_results(html)
        except Exception:
            # If search fails, return empty results
            return []

    def _parse_search_results(self, html: str) -> list[dict]:
        """Parse PMDA search results HTML."""
        results = []
        soup = BeautifulSoup(html, "html.parser")

        # Find result rows (PMDA uses table-based layout)
        # This is a simplified parser - actual structure may vary
        rows = soup.find_all("tr", class_=re.compile(r"result|row"))

        for row in rows[:20]:  # Limit to first 20 results
            try:
                cells = row.find_all("td")
                if len(cells) >= 3:
                    result = {
                        "approval_number": cells[0].get_text(strip=True),
                        "brand_name": cells[1].get_text(strip=True),
                        "generic_name": cells[2].get_text(strip=True) if len(cells) > 2 else "",
                        "manufacturer": cells[3].get_text(strip=True) if len(cells) > 3 else "",
                        "indication": cells[4].get_text(strip=True) if len(cells) > 4 else "",
                    }
                    if result["brand_name"]:
                        results.append(result)
            except (IndexError, AttributeError):
                continue

        return results

    def get_drug_details(self, approval_number: str) -> dict | None:
        """Get detailed information for a specific drug by approval number."""
        # PMDA detail page URL pattern
        detail_url = f"{self.BASE_URL}/PmdaSearch/iyakuDetail/{approval_number}"

        try:
            html = self._fetch_url(detail_url)
            return self._parse_drug_details(html)
        except Exception:
            return None

    def _parse_drug_details(self, html: str) -> dict:
        """Parse drug detail page."""
        soup = BeautifulSoup(html, "html.parser")
        details = {}

        # Extract key fields (simplified)
        for key, label in [
            ("brand_name", "販売名"),
            ("generic_name", "一般名"),
            ("indication", "効能・効果"),
            ("dosage", "用法・用量"),
            ("warnings", "警告"),
            ("manufacturer", "製造販売業者"),
            ("approval_date", "承認日"),
        ]:
            element = soup.find(string=re.compile(label))
            if element:
                parent = element.find_parent("tr") or element.find_parent("div")
                if parent:
                    value = parent.get_text(strip=True)
                    value = value.replace(label, "").strip()
                    details[key] = value

        return details

    def get_safety_alerts(self, drug_name: str) -> list[dict]:
        """Get safety alerts for a drug."""
        # PMDA safety information page
        alerts = []

        # This would require scraping the safety information section
        # Simplified implementation

        return alerts
