"""Entry point for the AI Security Paper Tracker."""

import argparse
import socket
import webbrowser

from arxiv_client import fetch_papers
from paper_processor import process_papers
from app import create_app
from models import ArxivFetchError


def find_available_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Security Paper Tracker")
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to look back (default: 7)",
    )
    parser.add_argument(
        "--terms",
        nargs="+",
        metavar="TERM",
        help='Custom search terms, e.g. --terms "LLM security" "prompt injection"',
    )
    parser.add_argument(
        "--port",
        type=int,
        default=0,
        help="Port for the local web server (default: random available port)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    papers = []
    error_message = None

    try:
        papers = fetch_papers(search_terms=args.terms, days=args.days)
    except ArxivFetchError as e:
        error_message = str(e)

    if not error_message:
        papers = process_papers(papers)

    app = create_app(papers, error_message)

    port = args.port if args.port else find_available_port()
    url = f"http://localhost:{port}"

    try:
        webbrowser.open(url)
    except Exception:
        print(f"Could not open browser automatically. Visit: {url}")

    print(f"Starting AI Security Paper Tracker at {url}")
    app.run(host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
