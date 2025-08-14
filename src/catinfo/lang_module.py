"""
LangChain tool wrapper.

Install langchain in your environment to use this tool decorator.
This file exposes a `tool` that LangChain agents can call.
"""
from typing import Optional, Dict, Any
try:
    # If user has LangChain installed, decorate with @tool
    from langchain.tools import tool  # type: ignore
except Exception:
    # If LangChain is not installed, provide a no-op decorator for import safety.
    def tool(name: str):
        def _decorator(fn):
            return fn
        return _decorator

from rpcats.rpcats.api import get_breeds_info
from rpcats.rpcats.utils import find_breed_info, breed_summary


@tool("get-cat-breed-info")
def get_cat_breed_info_tool(breed_name: str) -> Optional[str]:
    """
    LangChain tool that returns a human-readable summary for the requested breed.

    Returns:
        A string summary (good for LLM consumption) or None if breed not found.
    """
    breeds = get_breeds_info()
    breed = find_breed_info(breed_name, breeds)
    if not breed:
        return None
    return breed_summary(breed)
