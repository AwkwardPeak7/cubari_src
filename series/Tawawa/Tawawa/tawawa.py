#!/usr/bin/env python3

import json

import requests

url = "https://www.reddit.com/r/tawawa/search.json?q=flair%3A%22Twitter+Webcomic%22+is_self%3A0+NOT+site%3A(mangadex.org%20OR%20twitter.com)"

entries = []

after = None
while True:
    params = {
        "raw_json": 1,
        "limit": 100,
        "after": after,
    }
    headers = { "User-Agent": "catgirl-v:cubari:v.0.0.69 (by the cg-v gang)" }
    response = requests.get(url, params=params, headers=headers).json()

    entries.extend(response["data"]["children"])

    if (after := response["data"].get("after")) is None:
        break

entries = (e["data"] for e in reversed(entries) if not e["data"]["is_self"])
chapters = {}
for n, e in enumerate(entries, start=1):
    url = e["url"]
    if (secure_media := e.get("secure_media")) is not None:
        if (reddit_video := secure_media.get("reddit_video")) is not None:
            if reddit_video["is_gif"]:
                url = reddit_video["fallback_url"]

    chapters[str(n)] = {
        "title": e["title"],
        "groups": {
            "Tawawa": [
                url,
            ],
        },
        "last_updated": int(e["created"]),
    }

cubari = {
    "$schema": "../../../schema/cubari/gistSource.schema.json",
    "title": "Getsuyoubi no Tawawa! - Weekly Edition",
    "description": "Getsuyoubi no Tawawa, also known as Tawawa on Monday. A blue-tinted series about the daily lives of beautiful, well-endowed girls. The branches bent low [were heavy] with fruit. Tags: Suggestive, Romance, Office Workers, School Life, Slice of Life",
    "artist": "Himura Kiseki",
    "author": "Himura Kiseki",
    "cover": "https://mangadex.org/covers/7a781b6f-6d4f-4169-99f1-34d22cdc00d5/4f64dbc9-e142-40e5-b300-cc5eb8283789.jpg",
    "chapters": chapters,
}

with open("series/Tawawa/Tawawa/cubari.json", "w") as f:
    json.dump(cubari, f, indent=4)
