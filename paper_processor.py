"""Paper processing pipeline: deduplication, sorting, and capping."""

from models import Paper


def deduplicate(papers: list[Paper]) -> list[Paper]:
    """
    Remove duplicate papers by arXiv ID, retaining the first occurrence.
    Returns a new list with unique papers.
    """
    seen: set[str] = set()
    unique: list[Paper] = []
    for paper in papers:
        if paper.arxiv_id not in seen:
            seen.add(paper.arxiv_id)
            unique.append(paper)
    return unique


def sort_by_date(papers: list[Paper]) -> list[Paper]:
    """
    Sort papers by publication date in descending order (most recent first).
    Uses a stable sort so papers with the same date maintain their relative order.
    """
    return sorted(papers, key=lambda p: p.published, reverse=True)


def cap_results(papers: list[Paper], max_count: int = 20) -> list[Paper]:
    """
    Return at most max_count papers from the list.
    """
    return papers[:max_count]


def process_papers(papers: list[Paper], max_count: int = 20) -> list[Paper]:
    """
    Pipeline: deduplicate → sort → cap. Convenience function combining all steps.
    """
    papers = deduplicate(papers)
    papers = sort_by_date(papers)
    papers = cap_results(papers, max_count)
    return papers
