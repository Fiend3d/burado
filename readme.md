# Burado Thumbnail Maker 

[https://fiend3d.github.io/burado/](https://fiend3d.github.io/burado/)

I built this to create thumbnails for my [YouTube channel](https://www.youtube.com/@buradoplays), replacing a simpler Python script I used before.

[![Burado Thumbnail Maker](https://img.youtube.com/vi/waembn8Wqt4/0.jpg)](https://www.youtube.com/watch?v=waembn8Wqt4)

## How to add a character

Place the PNG file in the `static/chars` directory and push. The [workflow](.github/workflows/pages.yml) regenerates `static/chars.json` from whatever is in that directory and redeploys the site, so the character appears in the autocomplete on its own — there is nothing to run by hand.

`make_chars.py` still does the same job locally. Run it from inside `static/` if you want `chars.json` up to date before pushing, e.g. to try the new character on a local `python -m http.server`.

## Deployment

The same workflow publishes the site, so **Settings → Pages → Source** has to stay on "GitHub Actions" rather than "Deploy from a branch".