"""
main.py
--------
This is the FastAPI backend for the URL Shortener project.
It exposes three main endpoints:

1. GET /health       → For Kubernetes liveness/readiness checks
2. POST /shorten     → Accepts a URL and returns a short code
3. GET /{short_code} → Redirects to the original URL

The actual storage logic (in‑memory for now, Redis later)
lives in storage.py so this file stays clean and modular.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

# Import storage functions (in‑memory for now, Redis later)
from backend.app.storage import save_url, get_url


# ---------------------------------------------------------
# FastAPI application metadata (shows up in /docs)
# ---------------------------------------------------------
app = FastAPI(
    title="URL Shortener Service",
    description="Lightweight URL shortener backend for Kubernetes demo",
    version="1.0.0"
)


# ---------------------------------------------------------
# Request model for POST /shorten
# ---------------------------------------------------------
class URLRequest(BaseModel):
    url: HttpUrl   # Validates that the input is a proper URL


# ---------------------------------------------------------
# Health check endpoint
# Used by Kubernetes for liveness/readiness probes
# ---------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------------------------------------------------------
# POST /shorten
# Accepts a URL and returns:
#   - short_code
#   - short_url (full redirect link)
# ---------------------------------------------------------
@app.post("/shorten")
def shorten_url(request: URLRequest):
    # Save the URL using storage layer
    short_code = save_url(request.url)

    # Return both the code and a ready-to-use short URL
    return {
        "short_code": short_code,
        "short_url": f"http://localhost:8000/{short_code}"
    }


# ---------------------------------------------------------
# GET /{short_code}
# Redirects the user to the original URL
# ---------------------------------------------------------
@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    # Look up the original URL
    original_url = get_url(short_code)

    # If not found, return 404
    if not original_url:
        raise HTTPException(status_code=404, detail="Short code not found")

    # Redirect to the stored URL
    return RedirectResponse(url=original_url)