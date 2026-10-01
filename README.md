# AI Security Paper Tracker

Fetches the latest AI security research papers from arXiv and displays them in a dark-mode web UI. Run one command, get a browser page with this week's papers. Works on macOS, Linux, and Windows.

## What it does

Queries arXiv for papers published in the last 7 days across six topics: LLM security, LLM safety, prompt injection, AI agent vulnerabilities, adversarial attacks on language models, and red teaming AI agents. Results are deduplicated and shown up to 20 papers, most recent first. Each title links to the original arXiv page with an expandable abstract.

## Prerequisites

- Python 3.10 or later
- Internet connection (to query arXiv)

## Quick start

```bash
git clone https://github.com/YOUR_USERNAME/ai-security-paper-tracker.git
cd ai-security-paper-tracker
./run.sh
```

The script creates a virtual environment, installs Flask, fetches papers, and opens your browser.

## Manual setup

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Configuration

### CLI flags

| Flag | Default | Description |
|---|---|---|
| `--days N` | 7 | How many days back to search |
| `--terms "t1" "t2" ...` | built-in list | Custom search terms |
| `--port N` | random | Port for the local web server |

Examples:

```bash
# Look back 14 days
python main.py --days 14

# Custom search terms
python main.py --terms "jailbreak" "model extraction" "backdoor attack"

# Fixed port
python main.py --port 8080
```

### Email digest

`email_report.py` sends an HTML digest email. Configure it with environment variables:

| Variable | Required | Default | Description |
|---|---|---|---|
| `FROM_ADDR` | yes | — | Sender email address |
| `TO_ADDR` | yes | — | Recipient email address |
| `SMTP_HOST` | no | `localhost` | SMTP relay hostname |
| `SMTP_PORT` | no | `25` | SMTP relay port |

```bash
FROM_ADDR=you@example.com TO_ADDR=you@example.com python email_report.py
```

**Gmail users:** Gmail blocks regular passwords for SMTP. You need an App Password instead: Google Account → Security → 2-Step Verification → App passwords. Generate one and use it as your SMTP credential. Set `SMTP_HOST=smtp.gmail.com` and `SMTP_PORT=587`.

## Project structure

```
ai-security-paper-tracker/
├── main.py              # Entry point — fetch, serve, open browser
├── models.py            # Paper dataclass and ArxivFetchError
├── arxiv_client.py      # arXiv API client
├── paper_processor.py   # Deduplication, sorting, capping
├── app.py               # Flask app factory
├── email_report.py      # Optional email digest sender
├── templates/
│   └── index.html       # Dark-mode Jinja2 template
├── requirements.txt     # Runtime dependencies (Flask)
├── requirements-dev.txt # Dev dependencies (pytest, hypothesis)
└── run.sh               # One-command launcher
```

## License

MIT
