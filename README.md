# AI Security Paper Tracker

A local macOS app that fetches the latest AI security research papers from arXiv and displays them in a dark-mode web UI. Run one command, get a browser page with this week's papers.

## What it does

- Queries arXiv for papers published in the last 7 days across these topics:
  - LLM security / LLM safety
  - Prompt injection
  - AI agent vulnerabilities
  - Adversarial attacks on language models
  - Red teaming AI agents
- Deduplicates results and shows up to 20 papers, most recent first
- Each paper title links to the original arXiv page
- Click "Show abstract" to expand the full abstract inline
- Dark mode UI, no external dependencies beyond Flask

## Prerequisites

- Python 3.10 or later
- Internet connection (to query arXiv)

## Quick start

```bash
git clone <your-repo-url>
cd ai-security-paper-tracker
./run.sh
```

That's it. The script creates a virtual environment, installs Flask, fetches papers, and opens your browser.

## Manual setup

If you prefer to set things up yourself:

```bash
cd ai-security-paper-tracker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Customization

To change the search terms, edit the `SEARCH_TERMS` list in `arxiv_client.py`. To change the time window, pass a different `days` value to `fetch_papers()` in `main.py`.

## Project structure

```
ai-security-paper-tracker/
├── main.py              # Entry point — fetch, serve, open browser
├── models.py            # Paper dataclass and ArxivFetchError
├── arxiv_client.py      # arXiv API client
├── paper_processor.py   # Deduplication, sorting, capping
├── app.py               # Flask app factory
├── templates/
│   └── index.html       # Dark-mode Jinja2 template
├── requirements.txt     # Runtime dependencies (Flask)
├── requirements-dev.txt # Dev dependencies (pytest, hypothesis)
└── run.sh               # One-command launcher
```
