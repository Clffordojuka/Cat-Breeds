"""FastAPI deployment wrapper for Cat Info API with real-time data from TheCatAPI."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import requests
from .config import BREEDS_ENDPOINT, REQUEST_TIMEOUT

app = FastAPI(title="Cat Info API", version="1.0")

# Allow from anywhere for demo/visualization use. Lock this down in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def get_breeds_info():
    """Fetch all cat breeds from TheCatAPI in real-time."""
    try:
        resp = requests.get(BREEDS_ENDPOINT, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            raise RuntimeError("Unexpected API response format")
        return data
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch breeds: {exc}") from exc


@app.get("/breed")
def get_breed(name: str = Query(..., description="Name of the cat breed")):
    """Return live summary + raw data for a requested breed name."""
    try:
        breeds = get_breeds_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # find the breed from the freshly fetched data
    breed = next((b for b in breeds if b.get("name").lower() == name.lower()), None)
    
    if not breed:
        raise HTTPException(status_code=404, detail="Breed not found")

    # dynamically create a summary from the breed object
    summary = {
        "temperament": breed.get("temperament"),
        "origin": breed.get("origin"),
        "life_span": breed.get("life_span"),
        "description": breed.get("description")
    }

    return {"breed": breed.get("name"), "summary": summary, "raw": breed}


@app.get("/")
def root():
    return {"message": "Welcome to Cat Info API! Use /breed?name=Siamese"}


@app.get("/health")
def healthcheck():
    """Healthcheck endpoint for uptime monitors."""
    return {"status": "ok"}