"""Helper utilities: searching, formatting, and small adapters."""

from typing import Optional, Dict, Any, List


def find_breed_info(breed_name: str, breeds_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Case-insensitive search for a breed by its name.
    Returns the full breed dict or None if not found.
    """
    if not breed_name:
        return None
    desired = breed_name.strip().lower()
    # Try exact-name match first, then fallback to substring matches
    for breed in breeds_data:
        if breed.get("name", "").lower() == desired:
            return breed

    # fallback: substring
    for breed in breeds_data:
        if desired in breed.get("name", "").lower():
            return breed

    return None


def breed_summary(breed: Dict[str, Any]) -> str:
    """
    Return a compact multi-line textual summary for the breed.
    Useful for CLI or returning strings to agents.
    """
    if not breed:
        return "No breed data provided."

    lines = []
    name = breed.get("name", "Unknown")
    header = f"{name}"
    lines.append(header)
    origin = breed.get("origin", "Unknown")
    temperament = breed.get("temperament", "Unknown")
    life_span = breed.get("life_span", "Unknown")
    weight = breed.get("weight", {}).get("imperial", "Unknown")
    description = breed.get("description", "")

    lines.append(f"Origin: {origin}")
    lines.append(f"Temperament: {temperament}")
    lines.append(f"Life span: {life_span} years")
    lines.append(f"Weight (imperial): {weight} lbs")
    if description:
        lines.append("")
        lines.append("Description:")
        lines.append(description.strip())

    if breed.get("wikipedia_url"):
        lines.append("")
        lines.append(f"Learn more: {breed['wikipedia_url']}")

    return "\n".join(lines)


def print_breed_profile(breed: Dict[str, Any]) -> None:
    """Pretty-print the breed profile to stdout."""
    print(breed_summary(breed))
