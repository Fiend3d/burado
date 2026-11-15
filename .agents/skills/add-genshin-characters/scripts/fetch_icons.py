#!/usr/bin/env python3
"""Download character card icons from the Genshin Impact wiki into static/chars.

Usage:
    python scripts/fetch_icons.py "Varka" "Mitya" "Valeriy"
    python scripts/fetch_icons.py --dry-run "Kujou Sara"
    python scripts/fetch_icons.py --search manekin
    python scripts/fetch_icons.py --force Nefer

Names are wiki display names (spaces allowed); files are saved with underscores,
e.g. `Kujou Sara` -> `static/chars/Kujou_Sara.png`.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import wiki  # noqa: E402

ITEM_CATEGORY = "Character_Item_Icons"


def safe_filename(name: str) -> str:
    """`Kujou Sara` -> `Kujou_Sara`, `Traveler (Anemo)` -> `Traveler_Anemo`."""
    name = re.sub(r"[^\w\s-]", "", name).strip()
    return re.sub(r"\s+", "_", name)


def item_icon_title(name: str) -> str:
    return f"{name} Item.png"


def candidates(name: str) -> list[str]:
    files = wiki.category_members(ITEM_CATEGORY, namespace=6)
    needle = name.lower()
    return [f.replace("File:", "") for f in files if needle in f.lower()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*", help="Character names, e.g. 'Kujou Sara'")
    parser.add_argument("--dry-run", action="store_true", help="Resolve only, write nothing")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--out", type=Path, default=None, help="Output directory (default static/chars)")
    parser.add_argument("--search", metavar="QUERY", help="List item-icon files matching QUERY and exit")
    args = parser.parse_args()

    out_dir = args.out if args.out else wiki.find_chars_dir()

    if args.search:
        matches = candidates(args.search)
        if not matches:
            print(f"No item icons match {args.search!r} in Category:{ITEM_CATEGORY}")
            return 1
        for m in sorted(matches):
            print(f"  {m}")
        return 0

    if not args.names:
        parser.error("no character names given (or use --search QUERY)")

    out_dir.mkdir(parents=True, exist_ok=True)
    failures = 0

    for name in args.names:
        title = item_icon_title(name)
        info = wiki.image_info(title)

        if info is None:
            print(f"[skip] {name}: no File:{title} on the wiki")
            matches = candidates(name)
            if matches:
                print(f"       candidates in Category:{ITEM_CATEGORY}:")
                for m in sorted(matches):
                    print(f"         - {m}")
            failures += 1
            continue

        target = out_dir / f"{safe_filename(name)}.png"
        if target.exists() and not args.force:
            print(f"[skip] {target.name} already exists (use --force to re-download)")
            continue

        if args.dry_run:
            print(
                f"[dry-run] {name} -> {target} "
                f"({info['width']}x{info['height']}, {info['mime']}, {info['url']})"
            )
            continue

        data = wiki.download(info["url"])
        target.write_bytes(data)
        print(
            f"[ok] {name} -> {target} "
            f"{info['width']}x{info['height']} {len(data)} bytes "
            f"(wiki mime {info['mime']})"
        )

    if not args.dry_run:
        print(f"\n{out_dir} now has "
              f"{len([p for p in out_dir.iterdir() if p.suffix.lower() == '.png'])} png files.")
        print("Next: cd static && python make_chars.py  (regenerates chars.json)")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
