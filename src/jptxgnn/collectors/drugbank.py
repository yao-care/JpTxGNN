"""DrugBank collector - fetches drug information including MOA."""

import csv
import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

import httpx

from .base import BaseCollector, CollectorResult


class DrugBankCollector(BaseCollector):
    """Collector for DrugBank drug information.

    Provides:
    - DrugBank ID lookup
    - Mechanism of Action (MOA)
    - Drug description
    - Drug categories
    - Targets and enzymes

    Can work with:
    1. Local vocab file (for ID lookup)
    2. Web scraping from DrugBank (for detailed info)
    3. Local cache files (for offline use)
    """

    source_name = "drugbank"

    def __init__(
        self,
        vocab_path: str | Path | None = None,
        cache_dir: str | Path | None = None,
        use_web: bool = True,
    ):
        """Initialize the DrugBank collector.

        Args:
            vocab_path: Path to drugbank_vocab.csv file
            cache_dir: Directory for caching fetched data
            use_web: Whether to fetch from web if not in cache
        """
        base_dir = Path(__file__).parent.parent.parent.parent / "data"

        if vocab_path is None:
            self.vocab_path = base_dir / "external" / "drugbank_vocab.csv"
        else:
            self.vocab_path = Path(vocab_path)

        if cache_dir is None:
            self.cache_dir = base_dir / "external" / "drugbank_cache"
        else:
            self.cache_dir = Path(cache_dir)

        self.use_web = use_web
        self._vocab: dict[str, str] | None = None
        self._vocab_reverse: dict[str, str] | None = None

    def _load_vocab(self) -> tuple[dict[str, str], dict[str, str]]:
        """Load DrugBank vocabulary for name-to-ID mapping.

        Returns:
            Tuple of (name_to_id, id_to_name) dictionaries
        """
        if self._vocab is not None:
            return self._vocab, self._vocab_reverse

        self._vocab = {}
        self._vocab_reverse = {}

        if not self.vocab_path.exists():
            return self._vocab, self._vocab_reverse

        with open(self.vocab_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                db_id = row.get("drugbank_id", "")
                name = row.get("drug_name", "")
                name_upper = row.get("drug_name_upper", "")

                if db_id and name:
                    self._vocab[name.lower()] = db_id
                    self._vocab_reverse[db_id] = name
                if name_upper:
                    self._vocab[name_upper.lower()] = db_id

        return self._vocab, self._vocab_reverse

    def get_drugbank_id(self, drug_name: str) -> str | None:
        """Get DrugBank ID for a drug name.

        Args:
            drug_name: Drug name (case-insensitive)

        Returns:
            DrugBank ID (e.g., "DB00001") or None if not found
        """
        vocab, _ = self._load_vocab()
        return vocab.get(drug_name.lower())

    def _get_cache_path(self, drugbank_id: str) -> Path:
        """Get cache file path for a DrugBank ID."""
        return self.cache_dir / f"{drugbank_id}.json"

    def _load_from_cache(self, drugbank_id: str) -> dict | None:
        """Load drug data from cache."""
        cache_path = self._get_cache_path(drugbank_id)
        if cache_path.exists():
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def _save_to_cache(self, drugbank_id: str, data: dict) -> None:
        """Save drug data to cache."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = self._get_cache_path(drugbank_id)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _fetch_from_web(self, drugbank_id: str) -> dict | None:
        """Fetch drug data from DrugBank website.

        Args:
            drugbank_id: DrugBank ID (e.g., "DB00001")

        Returns:
            Dictionary with drug information or None if failed
        """
        url = f"https://go.drugbank.com/drugs/{drugbank_id}"

        try:
            with httpx.Client(timeout=30.0, follow_redirects=True) as client:
                response = client.get(url)
                if response.status_code != 200:
                    return None

                html = response.text

                # Parse key information from HTML
                data = {
                    "drugbank_id": drugbank_id,
                    "fetched_from_web": True,
                }

                # Extract drug name
                name_match = re.search(
                    r'<dt[^>]*id="name"[^>]*>.*?</dt>\s*<dd[^>]*>(.*?)</dd>',
                    html,
                    re.DOTALL,
                )
                if name_match:
                    data["name"] = self._clean_html(name_match.group(1))

                # Extract description
                desc_match = re.search(
                    r'<dt[^>]*id="description"[^>]*>.*?</dt>\s*<dd[^>]*>(.*?)</dd>',
                    html,
                    re.DOTALL,
                )
                if desc_match:
                    data["description"] = self._clean_html(desc_match.group(1))

                # Extract mechanism of action
                moa_match = re.search(
                    r'<dt[^>]*id="mechanism-of-action"[^>]*>.*?</dt>\s*<dd[^>]*>(.*?)</dd>',
                    html,
                    re.DOTALL,
                )
                if moa_match:
                    data["mechanism_of_action"] = self._clean_html(moa_match.group(1))

                # Extract pharmacodynamics
                pd_match = re.search(
                    r'<dt[^>]*id="pharmacodynamics"[^>]*>.*?</dt>\s*<dd[^>]*>(.*?)</dd>',
                    html,
                    re.DOTALL,
                )
                if pd_match:
                    data["pharmacodynamics"] = self._clean_html(pd_match.group(1))

                # Extract indication
                ind_match = re.search(
                    r'<dt[^>]*id="indication"[^>]*>.*?</dt>\s*<dd[^>]*>(.*?)</dd>',
                    html,
                    re.DOTALL,
                )
                if ind_match:
                    data["indication"] = self._clean_html(ind_match.group(1))

                # Extract drug categories
                cat_match = re.search(
                    r'<dt[^>]*id="categories"[^>]*>.*?</dt>\s*<dd[^>]*>(.*?)</dd>',
                    html,
                    re.DOTALL,
                )
                if cat_match:
                    categories_html = cat_match.group(1)
                    categories = re.findall(r'<a[^>]*>([^<]+)</a>', categories_html)
                    data["categories"] = categories

                # Extract half-life
                hl_match = re.search(
                    r'<dt[^>]*id="half-life"[^>]*>.*?</dt>\s*<dd[^>]*>(.*?)</dd>',
                    html,
                    re.DOTALL,
                )
                if hl_match:
                    data["half_life"] = self._clean_html(hl_match.group(1))

                # Extract protein binding
                pb_match = re.search(
                    r'<dt[^>]*id="protein-binding"[^>]*>.*?</dt>\s*<dd[^>]*>(.*?)</dd>',
                    html,
                    re.DOTALL,
                )
                if pb_match:
                    data["protein_binding"] = self._clean_html(pb_match.group(1))

                # Extract metabolism
                met_match = re.search(
                    r'<dt[^>]*id="metabolism"[^>]*>.*?</dt>\s*<dd[^>]*>(.*?)</dd>',
                    html,
                    re.DOTALL,
                )
                if met_match:
                    data["metabolism"] = self._clean_html(met_match.group(1))

                # Extract toxicity
                tox_match = re.search(
                    r'<dt[^>]*id="toxicity"[^>]*>.*?</dt>\s*<dd[^>]*>(.*?)</dd>',
                    html,
                    re.DOTALL,
                )
                if tox_match:
                    data["toxicity"] = self._clean_html(tox_match.group(1))

                return data

        except Exception as e:
            print(f"Error fetching DrugBank data for {drugbank_id}: {e}")
            return None

    def _clean_html(self, html: str) -> str:
        """Clean HTML tags and normalize whitespace."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        return text.strip()

    def search(self, drug: str, disease: str | None = None) -> CollectorResult:
        """Search for DrugBank data for a drug.

        Args:
            drug: Drug name (INN or brand name)
            disease: Ignored for DrugBank lookup

        Returns:
            CollectorResult with DrugBank data
        """
        query = {"drug": drug}

        # Try to find DrugBank ID
        drugbank_id = self.get_drugbank_id(drug)

        if not drugbank_id:
            return self._make_result(
                query=query,
                data={
                    "found": False,
                    "drugbank_id": None,
                    "message": f"Drug '{drug}' not found in DrugBank vocabulary",
                },
                success=True,
            )

        # Try to load from cache first
        data = self._load_from_cache(drugbank_id)

        if data is None and self.use_web:
            # Fetch from web
            data = self._fetch_from_web(drugbank_id)
            if data:
                self._save_to_cache(drugbank_id, data)
                # Rate limiting
                time.sleep(1)

        if data is None:
            # Return basic info from vocab
            _, id_to_name = self._load_vocab()
            data = {
                "found": True,
                "drugbank_id": drugbank_id,
                "name": id_to_name.get(drugbank_id, drug),
                "mechanism_of_action": None,
                "description": None,
                "source": "vocab_only",
            }
        else:
            data["found"] = True

        return self._make_result(
            query=query,
            data=data,
            success=True,
        )

    def get_moa(self, drug: str) -> str | None:
        """Get mechanism of action for a drug.

        Args:
            drug: Drug name

        Returns:
            MOA string or None if not found
        """
        result = self.search(drug)
        if result.success and result.data:
            return result.data.get("mechanism_of_action")
        return None

    def get_drug_info(self, drug: str) -> dict:
        """Get comprehensive drug information.

        Args:
            drug: Drug name

        Returns:
            Dictionary with drug information
        """
        result = self.search(drug)
        if result.success:
            return result.data
        return {"found": False, "error": result.error_message}
