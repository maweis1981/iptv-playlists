"""Find public M3U playlists on GitHub and harvest the streams that are official.

Weekly job. It searches GitHub for playlist files, reads each candidate, and looks at
every entry that names a known channel (tvg-id in iptv-org/database):

- served from the channel's own website domain, and not yet listed: added to
  discovered/official.m3u, which the daily build merges like any other source (so it
  still has to pass POLICY.md and the playback check);
- served from an allowlisted CDN only: counted in discovered/REPORT.md for a person to
  review, never added automatically (relays of paid channels often sit on such CDNs);
- anything else: ignored.

Searches for the focus in sources.yml (countries and categories) run first, so playlists
for those areas are not crowded out by the general searches, and the report counts focus
streams per playlist so they can be reviewed first.

Usage: python scripts/discover.py --data DATABASE_DATA_DIR --listed DIST_INDEX_M3U
Needs GITHUB_TOKEN for the code search API. Rate-limited searches are retried with backoff;
if no playlist files are found at all the script exits non-zero and writes no report.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter
import urllib.error
import urllib.parse
import urllib.request

import yaml
from datetime import datetime, timezone
from pathlib import Path

from build import ROOT, Channel, Policy, load_channels, load_lines, parse_playlist, read_csv, registrable_domain

QUERIES = [
    '"#EXTINF" "tvg-id" extension:m3u',
    '"#EXTINF" "tvg-id" extension:m3u8',
]
MAX_FILES = 200
MAX_BYTES = 5 * 1024 * 1024
OFFICIAL = ROOT / "discovered" / "official.m3u"
REPORT = ROOT / "discovered" / "REPORT.md"
RETRIES = 4
MAX_WAIT = 120  # seconds; keeps the job well inside its 30-minute timeout


def github(url: str, token: str) -> dict:
    """GET a GitHub API URL. Rate-limit responses (429, or 403 with a retry hint) are retried
    with backoff, honouring Retry-After / X-RateLimit-Reset when GitHub sends them."""
    request = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "User-Agent": "doubo-discover",
    })
    for attempt in range(RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            limited = error.code == 429 or (error.code == 403 and (
                error.headers.get("Retry-After") or error.headers.get("X-RateLimit-Remaining") == "0"))
            if not limited or attempt == RETRIES:
                raise
            if error.headers.get("Retry-After"):
                wait = int(error.headers["Retry-After"])
            elif error.headers.get("X-RateLimit-Reset"):
                wait = int(error.headers["X-RateLimit-Reset"]) - int(time.time()) + 1
            else:
                wait = 15 * 2 ** attempt
            wait = min(max(wait, 5), MAX_WAIT)
            print(f"rate limited ({error.code}), retrying in {wait}s")
            time.sleep(wait)
    raise AssertionError("unreachable")


class Focus:
    """The countries and categories discovery looks for first (sources.yml: discovery.focus)."""

    def __init__(self, registry: Path, data: Path):
        focus = (yaml.safe_load(registry.read_text(encoding="utf-8")).get("discovery") or {}).get("focus") or {}
        self.countries = {c.upper() for c in focus.get("countries", [])}
        self.categories = set(focus.get("categories", []))
        country_names = {r["code"]: r["name"] for r in read_csv(data / "countries.csv")}
        category_names = {r["id"]: r["name"] for r in read_csv(data / "categories.csv")}
        self.terms = [country_names[c] for c in sorted(self.countries) if c in country_names]
        self.terms += [category_names[c] for c in sorted(self.categories) if c in category_names]

    def queries(self) -> list[tuple[str, int]]:
        """(query, pages): one page per focus term, then two pages per general query."""
        return [(f'"#EXTINF" "tvg-id" "{t}" extension:m3u', 1) for t in self.terms] + [(q, 2) for q in QUERIES]

    def labels(self, channel: Channel) -> list[str]:
        labels = [channel.country.lower()] if channel.country in self.countries else []
        return labels + [c for c in channel.categories if c in self.categories]


def candidate_files(token: str, focus: Focus) -> list[str]:
    """Raw URLs of playlist files found by code search, focus searches first."""
    raw: list[str] = []
    for query, pages in focus.queries():
        for page in range(1, pages + 1):
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
    parser.add_argument("--sources", type=Path, default=ROOT / "sources.yml", help="sources.yml with the discovery focus")
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

    focus = Focus(args.sources, args.data)
    print(f"focus searches: {', '.join(focus.terms) or 'none'}")
    files = candidate_files(token, focus)
    if not files:
        # Every search failed or came back empty: fail the job instead of committing an empty report.
        sys.exit("code search returned no playlist files; nothing to report")

    rows, added = [], []
    for url in files:
        text = fetch(url)
        if not text or "#EXTINF" not in text:
            continue
        streams = parse_playlist(text, "discovered")
        identified = official = review = 0
        focused: Counter[str] = Counter()
        for s in streams:
            channel = channels.get(s.channel_id)
            if channel is None:
                continue
            identified += 1
            if s.url in known or not policy.admits(s, channel):
                continue
            focused.update(focus.labels(channel))
            if channel.website and registrable_domain(channel.website) == registrable_domain(s.url):
                official += 1
                added.append(s)
                known.add(s.url)
            else:
                review += 1
        if identified:
            rows.append((url, len(streams), identified, official, review, focused))

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
        f"Focus ({', '.join(focus.terms)}): playlists with new streams for these come first; "
        "the Focus column counts their new streams (added or for review).", "",
        "| Playlist | Entries | Known channels | Added (official) | For review (CDN) | Focus |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for url, total, identified, official, review, focused in sorted(
        rows, key=lambda r: (-sum(r[5].values()), -r[3], -r[4])
    ):
        tags = ", ".join(f"{k} {v}" for k, v in focused.most_common())
        lines.append(f"| {url} | {total} | {identified} | {official} | {review} | {tags} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} playlists with known channels, {len(added)} official streams added")


if __name__ == "__main__":
    main()
