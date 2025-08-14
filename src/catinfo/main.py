"""CLI entry point for catinfo."""

import argparse
import sys
from typing import Optional

from rpcats.rpcats.api import get_breeds_info
from rpcats.rpcats.utils import find_breed_info, print_breed_profile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Get information about cat breeds (TheCatAPI)")
    parser.add_argument("breed", help="Name of cat breed (e.g., 'Siamese'). Partial names allowed.")
    parser.add_argument("--raw", action="store_true", help="Print raw JSON for the breed.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        breeds = get_breeds_info()
    except Exception as exc:
        print(f"Failed to fetch breed list: {exc}", file=sys.stderr)
        return 1

    breed = find_breed_info(args.breed, breeds)
    if not breed:
        print(f"Breed not found for '{args.breed}'. Try a different name or check spelling.", file=sys.stderr)
        return 0

    if args.raw:
        # Print raw JSON-like dict
        import json
        print(json.dumps(breed, indent=2))
    else:
        print_breed_profile(breed)

    return 0


if __name__ == "__main__":
    sys.exit(main())