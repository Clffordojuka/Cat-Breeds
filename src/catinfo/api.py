"""API utilities — fetch real-time data from TheCatAPI with error handling."""

from typing import List, Dict, Any
import requests

from .config import BREEDS_ENDPOINT, REQUEST_TIMEOUT


def get_breeds_info() -> List[Dict[str, Any]]:
    """
    Fetch all cat breeds from TheCatAPI in real-time.

    Raises:
        RuntimeError: if the network request fails.
    """
    try:
        resp = requests.get(BREEDS_ENDPOINT, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            raise RuntimeError("Unexpected API response format")
        return data
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch breeds: {exc}") from exc