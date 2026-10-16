"""Pull public r/LinusTechTips comments from the Arctic Shift Reddit archive.

    python collect.py pool.csv                          # 2026-07-01 .. 2026-10-15, the main pool
    python collect.py pool2.csv 2026-03-01 2026-07-01   # an earlier window, for the stretch extras

Writes a candidate pool (text, permalink) to label from. Not labels.csv itself.
"""
import csv
import html
import json
import sys
import time
import urllib.request
from collections import Counter

API = "https://arctic-shift.photon-reddit.com/api/comments/search"
AFTER, BEFORE = "2026-07-01", "2026-10-15"
PAGES = 60          # 100 comments per page
PER_THREAD = 4      # cap so one hot thread can't dominate the pool


def fetch(before, after):
    url = f"{API}?subreddit=LinusTechTips&limit=100&after={after}&before={before}&sort=desc"
    req = urllib.request.Request(url, headers={"User-Agent": "ai201-takemeter-coursework/1.0"})
    for attempt in range(4):    # the archive throws the odd 422/5xx under load
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)["data"]
        except urllib.error.HTTPError as e:
            print(f"  {e.code} at before={before}, retrying")
            time.sleep(5 * (attempt + 1))
    return []


def keep(c):
    body = c["body"]
    return (
        c["author"] not in ("AutoModerator", "[deleted]")
        and body not in ("[deleted]", "[removed]")
        and 60 <= len(body) <= 1200
        and not body.startswith(("&gt;", ">"))      # mostly a quote of someone else
        and "removed by a" not in body               # mod boilerplate
    )


def main(out, after=AFTER, before=BEFORE):
    rows, seen, per_thread = [], set(), Counter()
    for _ in range(PAGES):
        page = fetch(before, after)
        if not page:
            break
        for c in page:
            text = " ".join(html.unescape(c["body"]).replace("�", "").split())
            if keep(c) and text not in seen and per_thread[c["link_id"]] < PER_THREAD:
                seen.add(text)
                per_thread[c["link_id"]] += 1
                rows.append({"text": text, "permalink": f"https://reddit.com{c.get('permalink', '')}"})
        before = page[-1]["created_utc"]
        time.sleep(1)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["text", "permalink"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} comments from {len(per_thread)} threads -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
