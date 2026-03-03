"""JPRN (Japan Primary Registries Network) collector.

Collects clinical trial data from Japanese registries:
- UMIN-CTR (University hospital Medical Information Network)
- JapicCTI (Japan Pharmaceutical Information Center)
- JMACCT (Japan Medical Association Center for Clinical Trials)
"""

import re
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from .base import BaseCollector, CollectorResult


class JPRNCollector(BaseCollector):
    """Collector for Japan Primary Registries Network (JPRN).

    Searches Japanese clinical trial registries for drug-disease studies.
    """

    source_name = "jprn"

    # UMIN-CTR search URL
    UMIN_SEARCH_URL = "https://center6.umin.ac.jp/cgi-open-bin/ctr/ctr.cgi"
    UMIN_BASE_URL = "https://center6.umin.ac.jp"

    # JapicCTI search URL
    JAPIC_SEARCH_URL = "https://www.clinicaltrials.jp/cti-user/search/Search"
    JAPIC_BASE_URL = "https://www.clinicaltrials.jp"

    # Rate limiting
    REQUEST_DELAY = 1.0  # seconds between requests

    def __init__(self, max_results: int = 50):
        """Initialize the collector.

        Args:
            max_results: Maximum number of results to return per query
        """
        self.max_results = max_results
        self._last_request_time = 0

    def _rate_limit(self):
        """Ensure rate limiting between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.REQUEST_DELAY:
            time.sleep(self.REQUEST_DELAY - elapsed)
        self._last_request_time = time.time()

    def _fetch_url(self, url: str, method: str = "GET", data: bytes | None = None) -> str:
        """Fetch URL content with rate limiting.

        Args:
            url: URL to fetch
            method: HTTP method (GET or POST)
            data: POST data if applicable

        Returns:
            Response content as string
        """
        self._rate_limit()

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; JpTxGNN/1.0; +https://jptxgnn.yao.care)",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "ja,en;q=0.9",
        }

        if method == "POST":
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        request = Request(url, headers=headers, data=data, method=method)

        try:
            with urlopen(request, timeout=30) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset, errors="replace")
        except (HTTPError, URLError) as e:
            raise RuntimeError(f"Failed to fetch {url}: {e}")

    def search(self, drug: str, disease: str | None = None) -> CollectorResult:
        """Search JPRN registries for trials involving a drug and/or disease.

        Args:
            drug: Drug name (Japanese or English)
            disease: Disease/indication name (optional)

        Returns:
            CollectorResult with trial data
        """
        query = {"drug": drug, "disease": disease}

        try:
            all_trials = []

            # Search UMIN-CTR
            try:
                umin_trials = self._search_umin(drug, disease)
                all_trials.extend(umin_trials)
            except Exception as e:
                print(f"UMIN search error: {e}")

            # Search JapicCTI
            try:
                japic_trials = self._search_japic(drug, disease)
                all_trials.extend(japic_trials)
            except Exception as e:
                print(f"JapicCTI search error: {e}")

            # Remove duplicates based on trial ID
            unique_trials = self._deduplicate_trials(all_trials)

            return self._make_result(
                query=query,
                data={
                    "trials": unique_trials[:self.max_results],
                    "total": len(unique_trials),
                    "sources": ["UMIN-CTR", "JapicCTI"],
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

    def _search_umin(self, drug: str, disease: str | None = None) -> list[dict]:
        """Search UMIN-CTR registry.

        Args:
            drug: Drug name
            disease: Disease name (optional)

        Returns:
            List of trial dictionaries
        """
        # UMIN search parameters
        search_terms = drug
        if disease:
            search_terms = f"{drug} {disease}"

        params = {
            "function": "brows",
            "action": "brows",
            "type": "summary",
            "recptno": "",
            "language": "J",
            "_page_action": "search",
            "_page_recptno": "",
            "_page_language": "J",
            "terms": search_terms,
        }

        url = f"{self.UMIN_SEARCH_URL}?{urlencode(params)}"

        try:
            html = self._fetch_url(url)
            return self._parse_umin_results(html)
        except Exception:
            return []

    def _parse_umin_results(self, html: str) -> list[dict]:
        """Parse UMIN-CTR search results.

        Args:
            html: HTML response from UMIN search

        Returns:
            List of trial dictionaries
        """
        trials = []
        soup = BeautifulSoup(html, "html.parser")

        # Find trial rows in the result table
        # UMIN uses table-based layout for results
        rows = soup.find_all("tr", class_=re.compile(r"(odd|even|result)", re.I))

        for row in rows[:self.max_results]:
            try:
                cells = row.find_all("td")
                if len(cells) >= 4:
                    # Extract trial ID from link
                    link = row.find("a", href=re.compile(r"recptno="))
                    trial_id = ""
                    trial_url = ""
                    if link:
                        href = link.get("href", "")
                        match = re.search(r"recptno=([A-Z0-9]+)", href)
                        if match:
                            trial_id = match.group(1)
                            trial_url = f"{self.UMIN_BASE_URL}{href}"

                    trial = {
                        "registry": "UMIN-CTR",
                        "id": trial_id or cells[0].get_text(strip=True),
                        "title": cells[1].get_text(strip=True) if len(cells) > 1 else "",
                        "status": cells[2].get_text(strip=True) if len(cells) > 2 else "",
                        "phase": cells[3].get_text(strip=True) if len(cells) > 3 else "",
                        "sponsor": cells[4].get_text(strip=True) if len(cells) > 4 else "",
                        "url": trial_url,
                    }

                    if trial["id"] or trial["title"]:
                        trials.append(trial)

            except (IndexError, AttributeError):
                continue

        return trials

    def _search_japic(self, drug: str, disease: str | None = None) -> list[dict]:
        """Search JapicCTI registry.

        Args:
            drug: Drug name
            disease: Disease name (optional)

        Returns:
            List of trial dictionaries
        """
        # JapicCTI search uses POST with form data
        search_terms = drug
        if disease:
            search_terms = f"{drug} {disease}"

        # JapicCTI search form parameters
        form_data = {
            "txtKeyword": search_terms,
            "selRecState": "",  # All states
            "selPhase": "",     # All phases
            "sortOrder": "2",   # Sort by date
        }

        try:
            data = urlencode(form_data).encode("utf-8")
            html = self._fetch_url(self.JAPIC_SEARCH_URL, method="POST", data=data)
            return self._parse_japic_results(html)
        except Exception:
            return []

    def _parse_japic_results(self, html: str) -> list[dict]:
        """Parse JapicCTI search results.

        Args:
            html: HTML response from JapicCTI search

        Returns:
            List of trial dictionaries
        """
        trials = []
        soup = BeautifulSoup(html, "html.parser")

        # Find trial entries in the result list
        entries = soup.find_all("div", class_=re.compile(r"(result|entry|item)", re.I))

        for entry in entries[:self.max_results]:
            try:
                # Extract trial information
                title_elem = entry.find(["h3", "h4", "a", "span"], class_=re.compile(r"title", re.I))
                id_elem = entry.find(["span", "td"], class_=re.compile(r"(id|no|number)", re.I))

                link = entry.find("a", href=True)
                trial_url = ""
                trial_id = ""

                if link:
                    href = link.get("href", "")
                    if href.startswith("/"):
                        trial_url = f"{self.JAPIC_BASE_URL}{href}"
                    elif href.startswith("http"):
                        trial_url = href

                    # Extract JapicCTI ID from URL
                    match = re.search(r"(Japic[A-Z]*-\d+|CTI-\d+)", href, re.I)
                    if match:
                        trial_id = match.group(1)

                trial = {
                    "registry": "JapicCTI",
                    "id": trial_id or (id_elem.get_text(strip=True) if id_elem else ""),
                    "title": title_elem.get_text(strip=True) if title_elem else "",
                    "status": "",
                    "phase": "",
                    "sponsor": "",
                    "url": trial_url,
                }

                if trial["id"] or trial["title"]:
                    trials.append(trial)

            except (IndexError, AttributeError):
                continue

        return trials

    def _deduplicate_trials(self, trials: list[dict]) -> list[dict]:
        """Remove duplicate trials based on ID.

        Args:
            trials: List of trial dictionaries

        Returns:
            Deduplicated list of trials
        """
        seen_ids = set()
        unique = []

        for trial in trials:
            trial_id = trial.get("id", "")
            if trial_id and trial_id not in seen_ids:
                seen_ids.add(trial_id)
                unique.append(trial)
            elif not trial_id:
                # Keep trials without ID (based on title uniqueness)
                title = trial.get("title", "")
                if title and title not in seen_ids:
                    seen_ids.add(title)
                    unique.append(trial)

        return unique

    def search_umin_only(self, drug: str, disease: str | None = None) -> CollectorResult:
        """Search only UMIN-CTR registry.

        Args:
            drug: Drug name
            disease: Disease name (optional)

        Returns:
            CollectorResult with UMIN trial data
        """
        query = {"drug": drug, "disease": disease, "registry": "UMIN-CTR"}

        try:
            trials = self._search_umin(drug, disease)
            return self._make_result(
                query=query,
                data={
                    "trials": trials[:self.max_results],
                    "total": len(trials),
                    "source": "UMIN-CTR",
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

    def search_japic_only(self, drug: str, disease: str | None = None) -> CollectorResult:
        """Search only JapicCTI registry.

        Args:
            drug: Drug name
            disease: Disease name (optional)

        Returns:
            CollectorResult with JapicCTI trial data
        """
        query = {"drug": drug, "disease": disease, "registry": "JapicCTI"}

        try:
            trials = self._search_japic(drug, disease)
            return self._make_result(
                query=query,
                data={
                    "trials": trials[:self.max_results],
                    "total": len(trials),
                    "source": "JapicCTI",
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
