# Wiki notes

## Endpoints

- MediaWiki API: `https://genshin-impact.fandom.com/api.php` (works with a plain UA)
- Image host: `https://static.wikia.nocookie.net/gensin-impact/images/...` (Cloudflare protected)

## Cloudflare gotcha

The API is open, but the image host returns **403 "Just a moment..."** for
`python-requests` default UA and for plain curl. A full browser header set works:

```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/126.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/*,*/*;q=0.8
Sec-Fetch-Dest: image
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: cross-site
sec-ch-ua: "Not.A/Brand";"8","Chromium";"126"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Referer: https://www.google.com/
```

`scripts/fetch_icons.py` already sends these. `items/download.py` (the original script)
does not, so it may fail with 403 until the same headers are added there.

Useful categories:

- `Category:Playable Characters` — the roster to diff against (namespace 0)
- `Category:Character_Item_Icons` — the card-frame icons, `File:<Name> Item.png` (namespace 6)

## Icon format

- 256x256, the fanned "character card" frame with the character portrait.
- The wiki serves WebP from the `.../revision/latest` URL even when `imageinfo` reports
  `mime: image/png`. Saved as `.png` anyway — matches the existing files
  (`Kujou_Sara.png`, `Hu_Tao.png` are WebP) and browsers ignore the extension.
- Do not convert or resize; the editor draws them at a fixed aspect.

## Known gaps (as of the last run)

- `Manekin`, `Manekina`, `Wonderland Manekin` — no `File:<Name> Item.png` in
  `Category:Character_Item_Icons`; need another source.
- `Lumine` — `File:Lumine Item.png` exists, but `items/rename.py` deliberately skips
  Aether/Lumine, so they never reach `static/chars/`.
- Traveler elements: only `Aether_Cryo/Dendro/Geo/Pyro` are present; Anemo/Electro/Hydro
  variants are not.

## Local wiring

- `static/js/script.js` loads `static/chars.json`, builds `chars_map` from
  `assets.chars.chars`, and sets `characters[name].src = static/chars/<name>.png`.
- `static/make_chars.py` regenerates `chars.json` from the directory listing (run from
  inside `static/`).
- `.github/workflows/pages.yml` regenerates `chars.json` from `static/chars` on push, so
  pushing a new PNG is enough for the deployed site.
