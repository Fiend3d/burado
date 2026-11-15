---
name: add-genshin-characters
description: Add, refresh, or prune Genshin Impact character card icons in this repo's static/chars directory and regenerate static/chars.json. Use when asked to add missing characters, sync the character roster with the Genshin Impact wiki, check which characters are missing, or remove duplicate/renamed character icons.
---

# Add missing Genshin characters

Adds character card icons to `static/chars/` and regenerates `static/chars.json`.
Run the bundled scripts from the repo root; they locate `static/chars` themselves.

Read `references/wiki-notes.md` before downloading anything — it covers the Cloudflare
header trick, the naming convention, and which characters have no wiki icon.

## Workflow

1. **Find what is missing** (optional but recommended):

   ```bash
   python .agents/skills/add-genshin-characters/scripts/missing_chars.py
   ```

   Compares `static/chars/` against the wiki's `Category:Playable Characters` and prints
   missing entries plus local-only entries.

2. **Preview the download** (no files written):

   ```bash
   python .agents/skills/add-genshin-characters/scripts/fetch_icons.py --dry-run Varka Mitya Valeriy
   ```

   Names are wiki display names with spaces (`Kujou Sara`); the script saves them with
   underscores (`Kujou_Sara.png`). If a name has no `File:<Name> Item.png`, the script
   prints matching candidates from `Category:Character_Item_Icons` instead of guessing.

3. **Download**:

   ```bash
   python .agents/skills/add-genshin-characters/scripts/fetch_icons.py Varka Mitya Valeriy
   ```

   Add `--force` to re-download an icon that already exists.

4. **Verify visually**: `read` each new `static/chars/<Name>.png`. It must be the same
   fanned-card character frame as the existing icons, correct character, 256x256.
   WebP data with a `.png` extension is normal here — most wiki-sourced files in
   `static/chars/` are WebP and the browser renders them fine.

5. **Regenerate the roster** (the GitHub workflow also does this, but keep it local so a
   local `python -m http.server` preview works):

   ```bash
   cd static && python make_chars.py
   ```

6. **Report** added/removed files and the new `chars.json` count. Do not commit or push
   unless the user asks.

## Rules

- One file per character: `static/chars/<Name>.png`, underscores instead of spaces
  (`Kamisato_Ayaka.png`, `Kujou_Sara.png`). `static/js/script.js` maps the lowercased
  name to `static/chars/<name>.png`, so the filename is the autocomplete entry.
- No duplicates or near-duplicates. If both `Sara.png` and `Kujou_Sara.png` exist, keep
  the wiki name and delete the other only after the user confirms.
- Traveler variants are `Aether_<Element>.png` / `Lumine_<Element>.png`
  (`Aether_Pyro.png`, `Aether_Cryo.png`, ...). The wiki page is `Traveler (<Element>)`.
- Multi-part characters (e.g. `Wonderland Manekin`) may have no item icon at all; report
  them as needing a different source instead of substituting a fan image.
- Never hand-edit `static/chars.json`; it is generated from the directory listing.
