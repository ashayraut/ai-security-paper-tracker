"""Entry point for the AI Security Paper Tracker."""

import socket
import webbrowser

from arxiv_client import fetch_papers, SEARCH_TERMS
from paper_processor import process_papers
from app import create_app
from models import ArxivFetchError


def find_available_port() -> int:
    """Bind to port 0 and return the OS-assigned available port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def main():
    """Fetch papers, process them, and serve via Flask with browser auto-open."""
    papers = []
    error_message = None

    # 1. Fetch papers from arXiv
    try:
        papers = fetch_papers(SEARCH_TERMS)
    except ArxivFetchError as e:
        error_message = str(e)

    # 2. Process papers if fetch succeeded
    if not error_message:
        papers = process_papers(papers)

    # 3. Create Flask app
    app = create_app(papers, error_message)

    # 4. Find an available port
    port = find_available_port()

    url = f"http://localhost:{port}"

    # 5. Open browser (with fallback to printing URL)
    try:
        webbrowser.open(url)
    except Exception:
        print(f"Could not open browser automatically. Visit: {url}")

    # Print startup message
    print(f"Starting AI Security Paper Tracker at {url}")

    # 6. Start Flask server
    app.run(host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
