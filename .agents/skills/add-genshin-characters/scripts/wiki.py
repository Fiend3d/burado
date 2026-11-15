"""Shared Genshin Impact wiki helpers for the add-genshin-characters skill.

Only the Python standard library is used (no `requests` dependency).
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

API_URL = "https://genshin-impact.fandom.com/api.php"

# The MediaWiki API is open, but static.wikia.nocookie.net sits behind Cloudflare and
# answers 403 for library default user agents. A full browser header set works.
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "sec-ch-ua": '"Not.A/Brand";"8","Chromium";"126"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    "Referer": "https://www.google.com/",
}

API_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Burado thumbnail maker)",
    "Accept": "application/json",
}


def api(params: dict) -> dict:
    url = API_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=API_HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def category_members(category: str, namespace: int = 0) -> list[str]:
    """All page (or file) titles in a wiki category."""
    titles: list[str] = []
    token = None
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category}",
            "cmlimit": 500,
            "cmnamespace": namespace,
            "format": "json",
        }
        if token:
            params["cmcontinue"] = token
        data = api(params)
        titles += [m["title"] for m in data["query"]["categorymembers"]]
        if "continue" in data:
            token = data["continue"]["cmcontinue"]
        else:
            return titles


def image_info(file_title: str) -> dict | None:
    """imageinfo for `File:<...>` (pass the title without the `File:` prefix)."""
    data = api(
        {
            "action": "query",
            "titles": f"File:{file_title}",
            "prop": "imageinfo",
            "iiprop": "url|size|mime|timestamp",
            "format": "json",
        }
    )
    for _page_id, page in data["query"]["pages"].items():
        if "imageinfo" in page:
            return page["imageinfo"][0]
    return None


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers=BROWSER_HEADERS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def find_chars_dir(start: Path | None = None) -> Path:
    """Walk up from this script until the repo's static/chars directory is found."""
    path = (start or Path(__file__)).resolve()
    for candidate in [path] + list(path.parents):
        chars = candidate / "static" / "chars"
        if chars.is_dir():
            return chars
    raise SystemExit(
        "Could not find static/chars above this script. Run it from inside the Burado repo."
    )


def repo_root(chars_dir: Path) -> Path:
    return chars_dir.parents[1]
