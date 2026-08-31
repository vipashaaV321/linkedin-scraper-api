from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .scraper import scrape
from .models import Profile

app = FastAPI(title="LinkedIn Scraper API (public)")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/scrape/{username}")
def scrape_username(username: str):
    profile, diag = scrape(username)
    if profile:
        return JSONResponse(content=Profile(**profile).dict())
    raise HTTPException(status_code=502, detail=diag)
