"""
Tiny LangGraph-friendly node wrapper.

LangGraph implementations differ between releases. This file provides a simple class
(`CatBreedNode`) with a .run(...) method that LangGraph node wrappers can adapt or wrap.
If your LangGraph environment expects a specific node signature, wrap CatBreedNode.run
into the required adapter.

Usage example (generic):
    node = CatBreedNode()
    result = node.run({"breed_name": "Siamese"})  # returns dict with summary + raw data
"""
from typing import Dict, Any, Optional

from .api import get_breeds_info
from .utils import find_breed_info, breed_summary


class CatBreedNode:
    """A small node-like class exposing run(inputs: dict) -> dict"""

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expect inputs to contain key "breed_name".
        Returns:
            {
                "found": bool,
                "breed_name": str,
                "summary": Optional[str],
                "raw": Optional[dict]
            }
        """
        breed_name = inputs.get("breed_name") or inputs.get("breed") or ""
        if not breed_name:
            return {"found": False, "breed_name": "", "summary": None, "raw": None, "error": "No breed_name provided"}

        breeds = get_breeds_info()
        breed = find_breed_info(breed_name, breeds)
        if not breed:
            return {"found": False, "breed_name": breed_name, "summary": None, "raw": None}

        return {"found": True, "breed_name": breed.get("name"), "summary": breed_summary(breed), "raw": breed}
