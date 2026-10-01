"""Send a daily AI security paper digest via email."""

import os
import smtplib
import sys
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from arxiv_client import fetch_papers, SEARCH_TERMS
from paper_processor import process_papers
from models import ArxivFetchError

# Required env vars: FROM_ADDR, TO_ADDR
# Optional env vars: SMTP_HOST (default: localhost), SMTP_PORT (default: 25)
SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "25"))
FROM_ADDR = os.environ.get("FROM_ADDR", "")
TO_ADDR = os.environ.get("TO_ADDR", "")


def build_html(papers, error_message=None) -> str:
    today = date.today().strftime("%B %d, %Y")
    rows = ""

    if error_message:
        rows = f'<p style="color:#c0392b">Error fetching papers: {error_message}</p>'
    elif not papers:
        rows = '<p style="color:#666">No papers found for the last 7 days.</p>'
    else:
        for p in papers:
            authors = ", ".join(p.authors[:3])
            if len(p.authors) > 3:
                authors += f" +{len(p.authors) - 3} more"
            pub_date = p.published.strftime("%b %d, %Y")
            rows += f"""
<div style="border:1px solid #ddd;border-radius:6px;padding:14px 18px;margin-bottom:12px;background:#fafafa">
  <a href="{p.url}" style="color:#1a73e8;font-size:1rem;font-weight:600;text-decoration:none">{p.title}</a>
  <div style="margin-top:6px;font-size:0.85rem;color:#555">{authors}</div>
  <div style="font-size:0.8rem;color:#888;margin-bottom:8px">{pub_date}</div>
  <div style="font-size:0.875rem;color:#333;line-height:1.6">{p.abstract[:400]}{"…" if len(p.abstract) > 400 else ""}</div>
</div>"""

    count = len(papers) if papers else 0
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;max-width:760px;margin:0 auto;padding:24px;color:#222">
  <h1 style="font-size:1.4rem;font-weight:600;border-bottom:2px solid #eee;padding-bottom:10px;margin-bottom:4px">
    AI Security Papers — {today}
  </h1>
  <p style="color:#888;font-size:0.875rem;margin-bottom:20px">{count} paper{"s" if count != 1 else ""} from the last 7 days</p>
  {rows}
  <p style="margin-top:24px;font-size:0.75rem;color:#aaa;border-top:1px solid #eee;padding-top:12px">
    Source: <a href="https://arxiv.org" style="color:#1a73e8">arXiv</a> — AI Security Paper Tracker
  </p>
</body>
</html>"""


def send_report():
    if not FROM_ADDR or not TO_ADDR:
        raise ValueError("FROM_ADDR and TO_ADDR environment variables must be set.")

    papers = []
    error_message = None

    try:
        papers = fetch_papers(SEARCH_TERMS)
    except ArxivFetchError as e:
        error_message = str(e)

    if not error_message:
        papers = process_papers(papers)

    html = build_html(papers, error_message)
    today = date.today().strftime("%B %d, %Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"AI Security Papers — {today}"
    msg["From"] = FROM_ADDR
    msg["To"] = TO_ADDR
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.sendmail(FROM_ADDR, [TO_ADDR], msg.as_string())
        count = len(papers)
        print(f"Sent digest: {count} paper{'s' if count != 1 else ''}")
    except Exception as e:
        print(f"Failed to send email: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    send_report()
