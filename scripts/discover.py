"""Find public M3U playlists on GitHub and harvest the streams that are official.

Weekly job. It searches GitHub for playlist files, reads each candidate, and looks at
every entry that names a known channel (tvg-id in iptv-org/database):

- served from the channel's own website domain, and not yet listed: added to
  discovered/official.m3u, which the daily build merges like any other source (so it
  still has to pass POLICY.md and the playback check);
- served from an allowlisted CDN only: counted in discovered/REPORT.md for a person to
  review, never added automatically (relays of paid channels often sit on such CDNs);
- anything else: ignored.

Usage: python scripts/discover.py --data DATABASE_DATA_DIR --listed DIST_INDEX_M3U
Needs GITHUB_TOKEN for the code search API.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from build import ROOT, Policy, load_channels, load_lines, parse_playlist, read_csv, registrable_domain

QUERIES = [
    '"#EXTINF" "tvg-id" extension:m3u',
    '"#EXTINF" "tvg-id" extension:m3u8',
]
MAX_FILES = 120
MAX_BYTES = 5 * 1024 * 1024
OFFICIAL = ROOT / "discovered" / "official.m3u"
REPORT = ROOT / "discovered" / "REPORT.md"


def github(url: str, token: str) -> dict:
    request = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "User-Agent": "doubo-discover",
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def candidate_files(token: str) -> list[str]:
    """Raw URLs of playlist files found by code search, most recently indexed first."""
    raw: list[str] = []
    for query in QUERIES:
        for page in (1, 2):
            q = urllib.parse.quote(query)
            try:
                result = github(f"https://api.github.com/search/code?q={q}&per_page=100&page={page}", token)
            except OSError as error:
                print(f"search failed: {error}")
                break
            for item in result.get("items", []):
                repo = item["repository"]["full_name"]
                raw.append(f"https://raw.githubusercontent.com/{repo}/HEAD/{urllib.parse.quote(item['path'])}")
            time.sleep(7)  # code search allows about 10 requests a minute
    return list(dict.fromkeys(raw))[:MAX_FILES]


def fetch(url: str) -> str | None:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "doubo-discover"}), timeout=30) as r:
            body = r.read(MAX_BYTES + 1)
        return None if len(body) > MAX_BYTES else body.decode("utf-8", errors="replace")
    except OSError:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--listed", type=Path, required=True, help="current dist/index.m3u")
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN", "")

    channels = load_channels(args.data)
    policy = Policy(
        allowed_hosts=load_lines(ROOT / "policy" / "allowed-hosts.txt"),
        blocked_channels={r["channel"] for r in read_csv(args.data / "blocklist.csv")},
        takedowns={r["target"] for r in read_csv(ROOT / "policy" / "takedown.csv")},
    )
    known = {s.url for s in parse_playlist(args.listed.read_text(encoding="utf-8", errors="replace"), "listed")}
    known |= {s.url for s in parse_playlist(OFFICIAL.read_text(encoding="utf-8"), "discovered")}

    rows, added = [], []
    for url in candidate_files(token):
        text = fetch(url)
        if not text or "#EXTINF" not in text:
            continue
        streams = parse_playlist(text, "discovered")
        identified = official = review = 0
        for s in streams:
            channel = channels.get(s.channel_id)
            if channel is None:
                continue
            identified += 1
            if s.url in known or not policy.admits(s, channel):
                continue
            if channel.website and registrable_domain(channel.website) == registrable_domain(s.url):
                official += 1
                added.append(s)
                known.add(s.url)
            else:
                review += 1
        if identified:
            rows.append((url, len(streams), identified, official, review))

    if added:
        with OFFICIAL.open("a", encoding="utf-8") as f:
            for s in added:
                f.write("\n".join([f'#EXTINF:-1 tvg-id="{s.channel_id}{"@" + s.feed_id if s.feed_id else ""}",{s.title}', *s.options, s.url]) + "\n")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        "# Discovery report", "",
        f"Last run: {stamp}. New official streams added this run: {len(added)}.", "",
        "Streams on a channel's own domain are added to `official.m3u` automatically. "
        "Streams on allowlisted CDNs are only counted here; to use a list, review it and add it to `sources.yml` in a pull request.", "",
        "| Playlist | Entries | Known channels | Added (official) | For review (CDN) |", "| --- | ---: | ---: | ---: | ---: |",
    ]
    for url, total, identified, official, review in sorted(rows, key=lambda r: (-r[3], -r[4])):
        lines.append(f"| {url} | {total} | {identified} | {official} | {review} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} playlists with known channels, {len(added)} official streams added")


if __name__ == "__main__":
    main()
