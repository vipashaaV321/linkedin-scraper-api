**LinkedIn Scraper API**

This package is a self-contained public (no-login) LinkedIn profile scraper packaged as a small FastAPI service.

- a lightweight public (no-login) scraper for many public profiles (fast, reliable when available), located at [free_linkedin_scraper/main.py](../free_linkedin_scraper/main.py);
- a small packaged wrapper and data model under this folder that can reuse the free scraper or be extended to include authenticated scraping and parsing logic: see [linkedin_scraper_api/scripts/main.py](scripts/main.py) and [linkedin_scraper_api/app/models.py](app/models.py).

What this package contains
- `app/` — FastAPI app and scraping logic (entry: [app/main.py](app/main.py)).
- `app/scraper.py` — public LD+JSON scraper that extracts top-card fields.
- `app/models.py` — `Profile` Pydantic model for output shape.
- `scripts/main.py` — demo CLI wrapper that calls the scraper.

Key points
- The scraper reads the LinkedIn public profile HTML and extracts the schema.org `Person` LD+JSON block when available.
- The service exposes two endpoints: `/health` and `/scrape/{username}`.

Quick local run
1. Create and activate a virtual environment inside the `linkedin_scraper_api` folder:

```bash
cd linkedin_scraper_api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the demo CLI (prints JSON for a vanity name):

```bash
PYTHONPATH=. python3 linkedin_scraper_api/scripts/main.py williamhgates
```

3. Run the web service locally:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
# health: curl http://127.0.0.1:8000/health
# scrape: curl http://127.0.0.1:8000/scrape/williamhgates
```

API Endpoints
- `GET /health` — returns `{ "status": "ok" }`.
- `GET /scrape/{username}` — returns the `Profile` JSON when available, otherwise returns a diagnostic error.

**Capturing Experience / SDUI network payloads**
To implement full Experience/Education parsing you will often need the SDUI/XHR payload the LinkedIn client fetches when the Experience section loads. The easiest way to gather this is via DevTools → Network → XHR/Fetch. Copy the request as cURL and the response JSON; paste them here and the parser can be updated to decode the real payload.



