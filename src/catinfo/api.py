import httpx
import asyncio
from functools import lru_cache
from typing import List, Dict, Any

from .config import BREEDS_ENDPOINT, REQUEST_TIMEOUT


@lru_cache(maxsize=1)
def get_breeds_info_sync() -> List[Dict[str, Any]]:
    """Synchronous fetch with caching."""
    import requests
    try:
        resp = requests.get(BREEDS_ENDPOINT, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            raise RuntimeError("Unexpected API response format")
        return data
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch breeds: {exc}") from exc


async def get_breeds_info() -> List[Dict[str, Any]]:
    """Async wrapper for FastAPI."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_breeds_info_sync)