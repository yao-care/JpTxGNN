"""PubMed collector - fetches literature data via NCBI E-utilities API."""

import requests
import time
from typing import Any
from xml.etree import ElementTree

from .base import BaseCollector, CollectorResult


class PubMedCollector(BaseCollector):
    """Collector for PubMed literature data.

    Uses NCBI E-utilities API to search PubMed.
    API docs: https://www.ncbi.nlm.nih.gov/books/NBK25500/
    """

    source_name = "pubmed"
    ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def __init__(self, max_results: int = 20, api_key: str | None = None):
        """Initialize the collector.

        Args:
            max_results: Maximum number of results to return per query
            api_key: Optional NCBI API key for higher rate limits
        """
        self.max_results = max_results
        self.api_key = api_key

    def search(self, drug: str, disease: str | None = None) -> CollectorResult:
        """Search PubMed for articles about a drug and/or disease.

        Args:
            drug: Drug name
            disease: Disease/indication name (optional)

        Returns:
            CollectorResult with publication data
        """
        # Build search query
        search_terms = [drug]
        if disease:
            search_terms.append(disease)
        query_string = " AND ".join(search_terms)

        query = {"drug": drug, "disease": disease, "query_string": query_string}

        try:
            # Step 1: Search for PMIDs
            pmids = self._search_pmids(query_string)

            if not pmids:
                return self._make_result(
                    query=query,
                    data={"query": query_string, "results": []},
                    success=True,
                )

            # Step 2: Fetch article details
            articles = self._fetch_articles(pmids)

            return self._make_result(
                query=query,
                data={"query": query_string, "results": articles},
                success=True,
            )

        except requests.RequestException as e:
            return self._make_result(
                query=query,
                data={"query": query_string, "results": []},
                success=False,
                error_message=str(e),
            )

    def _search_pmids(self, query: str) -> list[str]:
        """Search PubMed and return list of PMIDs.

        Args:
            query: Search query string

        Returns:
            List of PMID strings
        """
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": self.max_results,
            "retmode": "json",
            "sort": "relevance",
        }

        if self.api_key:
            params["api_key"] = self.api_key

        response = requests.get(self.ESEARCH_URL, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])

    def _fetch_articles(self, pmids: list[str]) -> list[dict]:
        """Fetch article details for a list of PMIDs.

        Args:
            pmids: List of PMID strings

        Returns:
            List of article dictionaries
        """
        if not pmids:
            return []

        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
        }

        if self.api_key:
            params["api_key"] = self.api_key

        # Rate limiting - NCBI allows 3 requests/second without API key
        time.sleep(0.4)

        response = requests.get(self.EFETCH_URL, params=params, timeout=60)
        response.raise_for_status()

        return self._parse_xml(response.text)

    def _parse_xml(self, xml_text: str) -> list[dict]:
        """Parse PubMed XML response.

        Args:
            xml_text: XML response text

        Returns:
            List of parsed article dictionaries
        """
        articles = []

        try:
            root = ElementTree.fromstring(xml_text)
        except ElementTree.ParseError:
            return articles

        for article_elem in root.findall(".//PubmedArticle"):
            try:
                article = self._parse_article(article_elem)
                if article:
                    articles.append(article)
            except Exception:
                continue

        return articles

    def _parse_article(self, elem: ElementTree.Element) -> dict | None:
        """Parse a single PubmedArticle element.

        Args:
            elem: PubmedArticle XML element

        Returns:
            Parsed article dictionary or None
        """
        medline = elem.find(".//MedlineCitation")
        if medline is None:
            return None

        pmid_elem = medline.find(".//PMID")
        pmid = pmid_elem.text if pmid_elem is not None else ""

        article_elem = medline.find(".//Article")
        if article_elem is None:
            return None

        # Title
        title_elem = article_elem.find(".//ArticleTitle")
        title = self._get_text(title_elem)

        # Abstract
        abstract_elem = article_elem.find(".//Abstract/AbstractText")
        abstract = self._get_text(abstract_elem)[:1000] if abstract_elem is not None else ""

        # Journal
        journal_elem = article_elem.find(".//Journal/Title")
        journal = self._get_text(journal_elem)

        # Year
        year_elem = article_elem.find(".//Journal/JournalIssue/PubDate/Year")
        if year_elem is None:
            year_elem = article_elem.find(".//Journal/JournalIssue/PubDate/MedlineDate")
        year = self._get_text(year_elem)[:4] if year_elem is not None else ""

        # Authors
        authors = []
        for author in article_elem.findall(".//AuthorList/Author")[:5]:
            lastname = self._get_text(author.find("LastName"))
            forename = self._get_text(author.find("ForeName"))
            if lastname:
                authors.append(f"{lastname} {forename}".strip())

        # Publication types
        pub_types = []
        for pt in article_elem.findall(".//PublicationTypeList/PublicationType"):
            if pt.text:
                pub_types.append(pt.text)

        # MeSH terms
        mesh_terms = []
        for mesh in medline.findall(".//MeshHeadingList/MeshHeading/DescriptorName"):
            if mesh.text:
                mesh_terms.append(mesh.text)

        return {
            "pmid": pmid,
            "title": title,
            "abstract": abstract,
            "journal": journal,
            "year": year,
            "authors": authors,
            "pub_types": pub_types,
            "mesh_terms": mesh_terms[:10],  # Limit MeSH terms
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        }

    def _get_text(self, elem: ElementTree.Element | None) -> str:
        """Safely get text content from an XML element."""
        if elem is None:
            return ""
        # Handle elements with mixed content (text + children)
        return "".join(elem.itertext()).strip()
