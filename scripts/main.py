#!/usr/bin/env python3
"""Entry point for linkedin_scraper_api (public, no-login scraper).

This script wraps the scraping logic and outputs JSON matching
the `app.models.Profile` schema.
"""
import json
import sys
from pathlib import Path

from app import config
from app.models import Profile

# Import scraper logic from the local package implementation.
try:
    from app.scraper import scrape as _scrape
except Exception:
    # Fallback: inline simple implementation returning a diagnostic
    def _scrape(username, session=None):
        return None, {"username": username, "outcome": "not_available", "detail": "scraper module missing"}


def main(argv):
    if len(argv) < 2:
        print("Usage: python main.py <vanity-name-or-url>")
        return 2
    username = argv[1]
    # normalize URL -> username
    if username.startswith("http"):
        from urllib.parse import urlparse

        username = urlparse(username).path.strip("/").split("/")[-1]

    profile, diag = _scrape(username)
    if profile:
        p = Profile(**profile)
        print(p.json(indent=2, ensure_ascii=False))
        return 0
    print(json.dumps(diag, indent=2))
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
