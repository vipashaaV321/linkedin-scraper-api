import os

# Configuration for the standalone linkedin scraper

USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
