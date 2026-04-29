"""Flask application factory for the AI Security Paper Tracker."""

from flask import Flask, render_template

from models import Paper


def create_app(papers: list[Paper], error_message: str | None = None) -> Flask:
    """Create and configure the Flask application.

    Args:
        papers: List of papers to display.
        error_message: Optional error message to display instead of papers.

    Returns:
        Configured Flask app instance.
    """
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template(
            "index.html",
            papers=papers,
            error_message=error_message,
        )

    return app
