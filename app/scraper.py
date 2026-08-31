"""Public (no-login) LinkedIn scraper logic copied from the standalone utility.

Provides `scrape(username, session=None)` -> (profile_dict|None, diagnostics)
"""
import json
import re
import time
from urllib.parse import urlparse
from typing import Optional

import requests

from .config import USER_AGENT, REQUEST_TIMEOUT

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def find_person(html: str) -> Optional[dict]:
    best, best_score = None, -1
    for block in LD_RE.findall(html):
        try:
            doc = json.loads(block)
        except json.JSONDecodeError:
            continue
        nodes = doc.get("@graph") if isinstance(doc, dict) else None
        for node in (nodes or [doc]):
            if not isinstance(node, dict):
                continue
            types = node.get("@type")
            types = types if isinstance(types, list) else [types]
            if "Person" not in types or not node.get("name"):
                continue
            score = sum(bool(node.get(k)) for k in ("jobTitle", "description", "image", "address", "worksFor", "alumniOf"))
            if score > best_score:
                best, best_score = node, score
    return best


def _first(value):
    if isinstance(value, list):
        return value[0] if value else None
    return value


def _org_name(node):
    if isinstance(node, str):
        return node.strip() or None
    if isinstance(node, dict):
        name = node.get("name")
        return name.strip() if isinstance(name, str) and name.strip() else None
    return None


def _location(person: dict) -> Optional[str]:
    address = person.get("address")
    if isinstance(address, str):
        return address.strip() or None
    if not isinstance(address, dict):
        return None
    parts = []
    for key in ("addressLocality", "addressRegion", "addressCountry"):
        val = address.get(key)
        if isinstance(val, dict):
            val = val.get("name") or val.get("identifier")
        if not isinstance(val, str) or not val.strip():
            continue
        val = val.strip()
        if re.fullmatch(r"[A-Z]{2}", val) and parts:
            continue
        if any(p.lower() == val.lower() for p in parts):
            continue
        parts.append(val)
    return ", ".join(parts) or None


def _followers(person: dict) -> Optional[int]:
    stat = person.get("interactionStatistic")
    for entry in (stat if isinstance(stat, list) else [stat]):
        if isinstance(entry, dict) and "Follow" in str(entry.get("interactionType", "")):
            count = entry.get("userInteractionCount")
            if isinstance(count, (int, float)):
                return int(count)
    return None


def _image(person: dict) -> Optional[str]:
    img = _first(person.get("image"))
    if isinstance(img, str):
        return img
    if isinstance(img, dict):
        return img.get("contentUrl") or img.get("url")
    return None


def to_profile(person: dict, username: str) -> dict:
    works_for = person.get("worksFor")
    works_for = works_for if isinstance(works_for, list) else ([works_for] if works_for else [])
    alumni = person.get("alumniOf")
    alumni = alumni if isinstance(alumni, list) else ([alumni] if alumni else [])
    companies = [n for n in (_org_name(o) for o in works_for) if n]
    schools = [n for n in (_org_name(o) for o in alumni) if n]
    url = person.get("url")
    return {
        "id": username,
        "name": person.get("name"),
        "headline": _first(person.get("jobTitle")),
        "location": _location(person),
        "about": person.get("description"),
        "url": url.split("?")[0] if isinstance(url, str) else None,
        "image": _image(person),
        "current_company": companies[0] if companies else None,
        "followers": _followers(person),
        "companies": companies,
        "schools": schools,
    }


def scrape(username: str, session: Optional[requests.Session] = None):
    get = (session or requests).get
    url = f"https://www.linkedin.com/in/{username}"
    started = time.time()
    response = get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    elapsed = round(time.time() - started, 2)
    html = response.text
    diag = {"username": username, "status": response.status_code, "chars": len(html), "elapsed_s": elapsed}

    person = find_person(html)
    if person:
        return to_profile(person, username), diag

    head = html[:4000].lower()
    if response.status_code == 999 or (response.status_code == 200 and len(html) < 5000):
        diag["outcome"] = "refused"
        diag["detail"] = (f"HTTP {response.status_code}, {len(html)} chars, no Person block. LinkedIn returns this shell both when it is throttling the caller and when the vanity name does not exist.")
    elif "authwall" in head or "join linkedin" in head:
        diag["outcome"] = "authwall"
        diag["detail"] = "Login wall served instead of the public preview."
    else:
        diag["outcome"] = "no_person_block"
        diag["detail"] = (f"HTTP {response.status_code}, {len(html)} chars. Page rendered but carried no schema.org Person block; the markup may have changed.")
    return None, diag
