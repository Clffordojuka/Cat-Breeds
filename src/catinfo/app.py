"""FastAPI deployment wrapper for catinfo."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from src.catinfo.api import get_breeds_info
from src.catinfo.utils import find_breed_info, breed_summary

app = FastAPI(title="Cat Info API", version="1.0")

# Allow from anywhere for demo/visualization use. Lock this down in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/breed")
def get_breed(name: str = Query(..., description="Name of the cat breed")):
    """Return summary + raw data for a requested breed name."""
    try:
        breeds = get_breeds_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    breed = find_breed_info(name, breeds)
    if not breed:
        raise HTTPException(status_code=404, detail="Breed not found")

    return {"breed": breed.get("name"), "summary": breed_summary(breed), "raw": breed}


@app.get("/")
def root():
    return {"message": "Welcome to Cat Info API! Use /breed?name=Siamese"}
