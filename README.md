**LinkedIn Scraper API**

This small standalone package provides two usable scrapers for LinkedIn profiles:

- a lightweight public (no-login) scraper for many public profiles (fast, reliable when available), located at [free_linkedin_scraper/main.py](../free_linkedin_scraper/main.py);
- a small packaged wrapper and data model under this folder that can reuse the free scraper or be extended to include authenticated scraping and parsing logic: see [linkedin_scraper_api/scripts/main.py](scripts/main.py) and [linkedin_scraper_api/app/models.py](app/models.py).

Use this folder as a clean, self-contained submission of the public-profile scraping functionality. The instructions below explain how to set it up and run demos locally.

**Contents**
- **App config & models:** [linkedin_scraper_api/app/config.py](app/config.py), [linkedin_scraper_api/app/models.py](app/models.py)
- **Entry script:** [linkedin_scraper_api/scripts/main.py](scripts/main.py)
- **Standalone public scraper (original):** [free_linkedin_scraper/main.py](../free_linkedin_scraper/main.py)
- **Helpful project scripts (root):** [scripts/run_scrape_profile.py](../../scripts/run_scrape_profile.py), [scripts/linkedin_profile_free_scraper.py](../../scripts/linkedin_profile_free_scraper.py), [scripts/scrape_topcard.py](../../scripts/scrape_topcard.py)

**Prerequisites**
- Python 3.8 or newer installed locally.
- A virtual environment for isolation (recommended).

**Quick Setup (standalone folder)**
1. From the repository root create and activate a virtualenv and install the package requirements:

```bash
cd linkedin_scraper_api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the packaged demo (uses the existing free scraper if present in the repository):

```bash
PYTHONPATH=. python3 linkedin_scraper_api/scripts/main.py williamhgates
```

This prints JSON following the `Profile` model when the public schema.org `Person` block is available for the requested vanity name.

**Running the original free scraper**
If you prefer the original script that was used for quick public demos, you can run:

```bash
cd ..
python3 free_linkedin_scraper/main.py williamhgates
```

**Authenticated scraping (rich results)**
The repo includes scripts that attempt authenticated scraping (these require a valid LinkedIn session/cookies or account credentials). Two supported approaches:

- Programmatic login (may hit LinkedIn security checkpoints; the project will abort on CAPTCHA/checkpoint): supply `LINKEDIN_EMAIL` and `LINKEDIN_PASSWORD` in a `.env` file and run the project runner:

```bash
# from repo root
source .venv/bin/activate
PYTHONPATH=. python3 scripts/run_scrape_profile.py "https://www.linkedin.com/in/<your-vanity>"
```

- Manual cookie fallback (recommended when programmatic login hits checkpoints): copy cookies from your browser DevTools into `.env`:

```
LINKEDIN_LI_AT=<li_at value>
LINKEDIN_JSESSIONID="ajax:<token>"   # keep the surrounding quotes
```

Then re-run the same `scripts/run_scrape_profile.py` command above; the app prefers cookies from `.env` over programmatic login.

**Headful/browser rendering (Playwright)**
For pages that only render data client-side, a headful browser is the most reliable approach. A Playwright-based scraper exists at [scripts/scrape_topcard_browser.py](../../scripts/scrape_topcard_browser.py).

Install Playwright and browsers (only if you plan to use the browser scraper):

```bash
pip install playwright
python -m playwright install --with-deps
```

Run the browser scraper (it reads `.env` for cookies if present):

```bash
python3 scripts/scrape_topcard_browser.py "https://www.linkedin.com/in/<vanity>"
```

**Capturing Experience / SDUI network payloads**
To implement full Experience/Education parsing you will often need the SDUI/XHR payload the LinkedIn client fetches when the Experience section loads. The easiest way to gather this is via DevTools → Network → XHR/Fetch. Copy the request as cURL and the response JSON; paste them here and the parser can be updated to decode the real payload.

**Troubleshooting**
- Module import errors when running scripts directly? Use `PYTHONPATH=.` or run from the repo root so `app` can be imported.
- HTTP 302 / 410 / 999 responses mean LinkedIn redirected or served a minimal shell (login wall or anti-bot). If you see these, either supply valid `.env` cookies (manual cookie method above) or open the same account in a browser and clear any security checkpoint.
- `urllib3 NotOpenSSLWarning` about LibreSSL is informational and does not prevent requests from working.
- Playwright download errors: network issues can interrupt browser downloads; re-run `python -m playwright install --with-deps` to retry.

**Security & Ethics**
- Use a dedicated LinkedIn account for scraping — do not use your primary/personal account for automated requests.
- Respect LinkedIn's Terms of Service and robots policies. This code is for educational and limited personal use; do not run high-volume scraping.

**Extending the scraper**
- The parser lives in `app` in the main project (`app/scraper.py`) — add new extraction rules there once you have a sample raw response (see SDUI capture above).
- The `app/models.py` file in this package provides a `Profile` Pydantic model you can use for downstream APIs or tests.

If you want, I can:
- Copy the free scraper logic into this package so `linkedin_scraper_api` is fully self-contained, and add a small `setup.sh` to set up the venv and run a demo,
- Or create a zip/tarball of this folder ready for submission.

If you'd like one of those, tell me which and I will add it.
