"""arXiv API client for fetching AI security research papers."""

import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

from models import ArxivFetchError, Paper

ARXIV_API_URL = "http://export.arxiv.org/api/query"
DEFAULT_DAYS = 7

SEARCH_TERMS: list[str] = [
    "LLM security",
    "LLM safety",
    "prompt injection",
    "AI agent vulnerabilities",
    "adversarial attacks on language models",
    "red teaming AI agents",
]

# Atom XML namespace used by arXiv API responses
_ATOM_NS = "http://www.w3.org/2005/Atom"


def fetch_papers(
    search_terms: list[str] | None = None,
    days: int = DEFAULT_DAYS,
    max_results_per_query: int = 20,
) -> list[Paper]:
    """Query arXiv for each search term, restricted to papers from the last `days` days.

    Returns a flat list of Paper objects (may contain duplicates across terms).
    Raises ArxivFetchError if the API is unreachable or returns an error.
    """
    if search_terms is None:
        search_terms = SEARCH_TERMS

    today = datetime.now(timezone.utc).date()
    date_from = (today - timedelta(days=days)).strftime("%Y%m%d")
    date_to = today.strftime("%Y%m%d")

    papers: list[Paper] = []
    for term in search_terms:
        results = _query_arxiv(term, date_from, date_to, max_results_per_query)
        papers.extend(results)

    return papers


def _query_arxiv(
    search_term: str, date_from: str, date_to: str, max_results: int
) -> list[Paper]:
    """Execute a single arXiv API query and parse the Atom XML response."""
    search_query = f"all:{search_term} AND submittedDate:[{date_from} TO {date_to}]"

    params = urllib.parse.urlencode(
        {
            "search_query": search_query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "start": 0,
            "max_results": max_results,
        }
    )

    url = f"{ARXIV_API_URL}?{params}"

    try:
        with urllib.request.urlopen(url) as response:
            xml_text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise ArxivFetchError(
            f"arXiv API returned HTTP {exc.code} for query '{search_term}': {exc.reason}"
        ) from exc
    except urllib.error.URLError as exc:
        raise ArxivFetchError(
            f"Failed to reach arXiv API for query '{search_term}': {exc.reason}"
        ) from exc
    except Exception as exc:
        raise ArxivFetchError(
            f"Unexpected error fetching from arXiv for query '{search_term}': {exc}"
        ) from exc

    return _parse_atom_response(xml_text)


def _parse_atom_response(xml_text: str) -> list[Paper]:
    """Parse arXiv Atom XML into a list of Paper objects.

    Extracts arxiv_id, title, authors, abstract, published date, and URL.
    Raises ArxivFetchError on malformed XML.
    """
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise ArxivFetchError(f"Failed to parse arXiv XML response: {exc}") from exc

    papers: list[Paper] = []

    for entry in root.findall(f"{{{_ATOM_NS}}}entry"):
        # Extract the arXiv ID from the <id> tag (e.g., "http://arxiv.org/abs/2407.12345v1")
        id_elem = entry.find(f"{{{_ATOM_NS}}}id")
        if id_elem is None or id_elem.text is None:
            continue
        raw_id = id_elem.text.strip()
        # Extract the ID portion after the last slash, strip version suffix
        arxiv_id = raw_id.rsplit("/", 1)[-1]
        # Remove version suffix like "v1", "v2" etc.
        if arxiv_id and arxiv_id[-1].isdigit() and "v" in arxiv_id:
            version_idx = arxiv_id.rfind("v")
            if version_idx > 0 and arxiv_id[version_idx + 1 :].isdigit():
                arxiv_id = arxiv_id[:version_idx]

        # Extract title, normalize whitespace
        title_elem = entry.find(f"{{{_ATOM_NS}}}title")
        title = ""
        if title_elem is not None and title_elem.text:
            title = " ".join(title_elem.text.split())

        # Extract authors
        authors: list[str] = []
        for author_elem in entry.findall(f"{{{_ATOM_NS}}}author"):
            name_elem = author_elem.find(f"{{{_ATOM_NS}}}name")
            if name_elem is not None and name_elem.text:
                authors.append(name_elem.text.strip())

        # Extract abstract from <summary>
        summary_elem = entry.find(f"{{{_ATOM_NS}}}summary")
        abstract = ""
        if summary_elem is not None and summary_elem.text:
            abstract = " ".join(summary_elem.text.split())

        # Extract published date
        published_elem = entry.find(f"{{{_ATOM_NS}}}published")
        if published_elem is None or published_elem.text is None:
            continue
        try:
            published = datetime.fromisoformat(
                published_elem.text.strip().replace("Z", "+00:00")
            )
        except ValueError:
            continue

        # Construct the URL
        url = f"https://arxiv.org/abs/{arxiv_id}"

        papers.append(
            Paper(
                arxiv_id=arxiv_id,
                title=title,
                authors=authors,
                abstract=abstract,
                published=published,
                url=url,
            )
        )

    return papers
