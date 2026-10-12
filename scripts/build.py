"""Build the Doubo public channel directory from iptv-org data.

Domain model
------------
Channel   a TV channel from iptv-org/database (id, country, categories, website).
Feed      a variant of a channel (SD/HD/regional) carrying its languages.
Stream    a URL submitted to iptv-org/iptv, pointing at one channel feed.
Policy    decides whether a stream may be listed. Only streams served by the
          channel's own website domain or by an allowlisted broadcast CDN /
          official FAST platform pass; everything else is left out.
Playlist  a named selection of listed streams (all, per country, per category,
          per language), written as M3U plus a JSON index for the website.

Usage: python scripts/build.py --data DATA_DIR --streams STREAMS_DIR --out OUT_DIR [--probe]
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import ipaddress
import json
import re
import urllib.request
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import tldextract

ROOT = Path(__file__).resolve().parent.parent
_extract = tldextract.TLDExtract(suffix_list_urls=())  # bundled public suffix list, no network


# ---------------------------------------------------------------- domain

@dataclass(frozen=True)
class Channel:
    id: str
    name: str
    country: str
    categories: tuple[str, ...]
    website: str
    is_nsfw: bool
    closed: bool


@dataclass(frozen=True)
class Feed:
    channel_id: str
    id: str
    is_main: bool
    languages: tuple[str, ...]


@dataclass
class Stream:
    channel_id: str
    feed_id: str
    title: str
    url: str
    options: list[str] = field(default_factory=list)  # #EXTVLCOPT lines (referrer, user agent)

    @property
    def geo_blocked(self) -> bool:
        return "[Geo-blocked]" in self.title


def registrable_domain(url: str) -> str | None:
    host = urlsplit(url).hostname or ""
    try:
        ipaddress.ip_address(host)
        return None  # bare IPs are never a broadcaster's official endpoint
    except ValueError:
        pass
    return _extract(host).top_domain_under_public_suffix or None


class Policy:
    def __init__(self, allowed_hosts: set[str], blocked_channels: set[str], takedowns: set[str]):
        self.allowed_hosts = allowed_hosts
        self.blocked_channels = blocked_channels
        self.takedowns = takedowns

    def admits(self, stream: Stream, channel: Channel | None) -> bool:
        if channel is None or channel.is_nsfw or channel.closed or "xxx" in channel.categories:
            return False
        if channel.id in self.blocked_channels or channel.id in self.takedowns or stream.url in self.takedowns:
            return False
        if urlsplit(stream.url).scheme not in ("http", "https"):
            return False
        domain = registrable_domain(stream.url)
        if domain is None:
            return False
        if channel.website and registrable_domain(channel.website) == domain:
            return True
        return domain in self.allowed_hosts


# ---------------------------------------------------------------- loading

def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def split(value: str) -> tuple[str, ...]:
    return tuple(v for v in value.split(";") if v)


def load_channels(data: Path) -> dict[str, Channel]:
    return {
        r["id"]: Channel(
            id=r["id"], name=r["name"], country=r["country"], categories=split(r["categories"]),
            website=r["website"], is_nsfw=r["is_nsfw"] == "TRUE", closed=bool(r["closed"]),
        )
        for r in read_csv(data / "channels.csv")
    }


def load_feeds(data: Path) -> dict[tuple[str, str], Feed]:
    feeds = {}
    for r in read_csv(data / "feeds.csv"):
        feed = Feed(r["channel"], r["id"], r["is_main"] == "TRUE", split(r["languages"]))
        feeds[(feed.channel_id, feed.id)] = feed
    return feeds


def load_logos(data: Path) -> dict[tuple[str, str], str]:
    logos: dict[tuple[str, str], str] = {}
    for r in read_csv(data / "logos.csv"):
        logos.setdefault((r["channel"], r["feed"]), r["url"])
    return logos


def load_lines(path: Path) -> set[str]:
    return {l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}


def parse_streams(streams_dir: Path) -> list[Stream]:
    streams = []
    for path in sorted(streams_dir.glob("*.m3u")):
        pending: Stream | None = None
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line.startswith("#EXTINF"):
                tvg_id = re.search(r'tvg-id="([^"]*)"', line)
                channel_id, _, feed_id = (tvg_id.group(1) if tvg_id else "").partition("@")
                pending = Stream(channel_id, feed_id, line.rsplit(",", 1)[-1].strip(), "")
            elif line.startswith("#EXTVLCOPT") and pending:
                pending.options.append(line)
            elif line and not line.startswith("#") and pending:
                pending.url = line
                streams.append(pending)
                pending = None
    return streams


# ---------------------------------------------------------------- probing

def probe(stream: Stream, timeout: float = 10) -> bool:
    headers = {"User-Agent": "Mozilla/5.0 (Doubo directory check)"}
    for opt in stream.options:
        key, _, value = opt.removeprefix("#EXTVLCOPT:").partition("=")
        headers[{"http-referrer": "Referer", "http-user-agent": "User-Agent"}.get(key, key)] = value
    request = urllib.request.Request(stream.url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status < 400 and bool(response.read(512))
    except Exception:
        return False


def keep_reachable(streams: list[Stream], workers: int = 64) -> list[Stream]:
    # Geo-blocked streams cannot be checked from a CI runner, so they are kept as listed.
    to_check = [s for s in streams if not s.geo_blocked]
    with concurrent.futures.ThreadPoolExecutor(workers) as pool:
        reachable = {id(s) for s, ok in zip(to_check, pool.map(probe, to_check)) if ok}
    return [s for s in streams if s.geo_blocked or id(s) in reachable]


# ---------------------------------------------------------------- output

@dataclass
class Entry:
    stream: Stream
    channel: Channel
    languages: tuple[str, ...]
    logo: str

    def m3u(self) -> str:
        attrs = {
            "tvg-id": f"{self.channel.id}@{self.stream.feed_id}" if self.stream.feed_id else self.channel.id,
            "tvg-logo": self.logo,
            "tvg-country": self.channel.country,
            "tvg-language": ";".join(self.languages),
            "group-title": ";".join(c.capitalize() for c in self.channel.categories) or "Undefined",
        }
        head = " ".join(f'{k}="{v}"' for k, v in attrs.items() if v)
        return "\n".join([f"#EXTINF:-1 {head},{self.stream.title}", *self.stream.options, self.stream.url])


def write_playlist(path: Path, entries: list[Entry]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(entries, key=lambda e: (e.stream.title.lower(), e.stream.url))
    path.write_text("#EXTM3U\n" + "".join(e.m3u() + "\n" for e in ordered), encoding="utf-8")


def build(data: Path, streams_dir: Path, out: Path, check: bool) -> dict:
    channels, feeds, logos = load_channels(data), load_feeds(data), load_logos(data)
    language_names = {r["code"]: r["name"] for r in read_csv(data / "languages.csv")}
    policy = Policy(
        allowed_hosts=load_lines(ROOT / "policy" / "allowed-hosts.txt"),
        blocked_channels={r["channel"] for r in read_csv(data / "blocklist.csv")},
        takedowns={r["target"] for r in read_csv(ROOT / "policy" / "takedown.csv")},
    )
    listed = [s for s in parse_streams(streams_dir) if policy.admits(s, channels.get(s.channel_id))]
    if check:
        listed = keep_reachable(listed)

    entries = []
    seen_urls = set()
    for s in listed:
        if s.url in seen_urls:
            continue
        seen_urls.add(s.url)
        channel = channels[s.channel_id]
        feed = feeds.get((s.channel_id, s.feed_id))
        logo = logos.get((s.channel_id, s.feed_id)) or logos.get((s.channel_id, ""), "")
        entries.append(Entry(s, channel, feed.languages if feed else (), logo))

    by_country, by_category, by_language = defaultdict(list), defaultdict(list), defaultdict(list)
    for e in entries:
        by_country[e.channel.country.lower()].append(e)
        for c in e.channel.categories:
            by_category[c].append(e)
        for lang in e.languages:
            by_language[lang].append(e)

    write_playlist(out / "index.m3u", entries)
    for group, folder in ((by_country, "countries"), (by_category, "categories"), (by_language, "languages")):
        for key, items in group.items():
            write_playlist(out / folder / f"{key}.m3u", items)

    def channel_names(items: list[Entry]) -> list[dict]:
        unique = {}
        for e in items:
            unique.setdefault(e.channel.id, {"name": e.channel.name, "categories": list(e.channel.categories)})
        return sorted(unique.values(), key=lambda c: c["name"].lower())

    index = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "streams": len(entries),
        "channels": len({e.channel.id for e in entries}),
        "countries": sorted(
            ({"code": k, "streams": len(v), "channels": channel_names(v)} for k, v in by_country.items()),
            key=lambda c: c["code"],
        ),
        "categories": sorted(
            ({"id": k, "streams": len(v), "channels": len({e.channel.id for e in v})} for k, v in by_category.items()),
            key=lambda c: c["id"],
        ),
        "languages": sorted(
            (
                {"code": k, "name": language_names.get(k, k), "streams": len(v), "channels": len({e.channel.id for e in v})}
                for k, v in by_language.items()
            ),
            key=lambda c: -c["channels"],
        ),
    }
    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", type=Path, required=True, help="iptv-org/database data/ directory")
    parser.add_argument("--streams", type=Path, required=True, help="iptv-org/iptv streams/ directory")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--probe", action="store_true", help="drop streams that do not respond")
    args = parser.parse_args()
    index = build(args.data, args.streams, args.out, args.probe)
    print(f"{index['channels']} channels, {index['streams']} streams, {len(index['countries'])} countries")


if __name__ == "__main__":
    main()
