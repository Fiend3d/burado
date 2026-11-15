#!/usr/bin/env python3
"""Diff static/chars against the wiki's playable character roster.

Usage:
    python scripts/missing_chars.py
    python scripts/missing_chars.py --show-all
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import wiki  # noqa: E402

PLAYABLE_CATEGORY = "Playable Characters"


def key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--show-all", action="store_true", help="Also print the matched roster")
    args = parser.parse_args()

    chars_dir = wiki.find_chars_dir()
    local = sorted(p.stem for p in chars_dir.iterdir() if p.suffix.lower() == ".png")
    local_keys = {key(n) for n in local}

    wiki_names = sorted(set(wiki.category_members(PLAYABLE_CATEGORY, namespace=0)))
    wiki_keys = {key(n) for n in wiki_names}

    has_aether = any(n.startswith("Aether_") for n in local)
    has_lumine = any(n.startswith("Lumine_") for n in local)

    def covered(name: str) -> bool:
        k = key(name)
        if k in local_keys:
            return True
        # Traveler (Pyro) <-> Aether_Pyro
        alt = k.replace("traveler", "aether")
        if alt != k and alt in local_keys:
            return True
        # Bare Traveler / Aether pages are covered by any element variant
        if k in {"traveler", "aether", "travelerunaligned"} and has_aether:
            return True
        if k == "lumine" and has_lumine:
            return True
        return False

    missing = [n for n in wiki_names if not covered(n)]
    local_only = [
        n
        for n in local
        if key(n) not in wiki_keys and key(n.replace("Aether", "Traveler")) not in wiki_keys
    ]

    print(f"Wiki playable characters: {len(wiki_names)}")
    print(f"Local icons in {chars_dir}: {len(local)}")

    print("\nMissing locally:")
    for n in missing:
        print(f"  {n}")
    if not missing:
        print("  (none)")

    print("\nLocal-only (not in the wiki playable category - possible duplicates):")
    for n in local_only:
        print(f"  {n}")
    if not local_only:
        print("  (none)")

    if args.show_all:
        print("\nMatched:")
        for n in wiki_names:
            if covered(n):
                print(f"  {n}")

    print("\nTo download the missing ones:")
    print("  python .agents/skills/add-genshin-characters/scripts/fetch_icons.py \"Name\" ...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
