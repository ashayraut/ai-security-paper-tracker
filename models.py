"""Data models for the AI Security Paper Tracker."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Paper:
    """A single arXiv research paper."""

    arxiv_id: str  # e.g., "2407.12345"
    title: str  # Paper title, whitespace-normalized
    authors: list[str]  # List of author names
    abstract: str  # Full abstract text
    published: datetime  # Publication date (UTC)
    url: str  # Link to arXiv page: https://arxiv.org/abs/{arxiv_id}


class ArxivFetchError(Exception):
    """Raised when the arXiv API cannot be reached or returns an error."""

    pass
