"""API utilities — fetch data from TheCatAPI with simple caching and error handling."""
from functools import lru_cache
from typing import List, Dict, Any

import requests

from config import BREEDS_ENDPOINT, REQUEST_TIMEOUT


@lru_cache(maxsize=1)
def get_breeds_info() -> List[Dict[str, Any]]:
    """
    Fetch all cat breeds from TheCatAPI.

    Uses an in-process LRU cache so repeated calls during program lifetime
    won't re-download data unnecessarily. TTL not implemented — restart to refresh.

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
