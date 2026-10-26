"""Fetch Baseball-Reference playoff-odds pages into data/raw/bref_odds/.

One page per club-season: /teams/{TEAM}/{SEASON}-playoff-odds.shtml. Each season's
team codes come from that season's league page (/leagues/majors/{SEASON}.shtml), which
is cached alongside as league.html.

Rate rules (Sports-Reference locks out clients that break them):
  - one request at a time, at least 6 seconds apart;
  - every page is saved before it is parsed, and a cached page is never re-fetched;
  - any non-200 response (redirects included) stops the run. Nothing is retried.

Run from the repo root: python3 src/scrape/bref_odds.py 2011 2013
(both seasons inclusive). Add --limit N to fetch at most N pages.
"""

import argparse
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "raw" / "bref_odds"
BASE = "https://www.baseball-reference.com"
MIN_GAP = 6.5  # seconds between requests; the rule is 6, plus margin
HEADERS = {"User-Agent": "competitive-windows research scraper (personal, non-commercial)"}

_last_request = 0.0
_fetched = 0


class Stop(Exception):
    pass


def fetch(url, path, limit):
    """Return the page at url, from path if cached, else fetched and saved to path."""
    global _last_request, _fetched
    if path.exists():
        return path.read_text(encoding="utf-8")
    if limit is not None and _fetched >= limit:
        raise Stop(f"fetch limit {limit} reached")
    wait = _last_request + MIN_GAP - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    _last_request = time.monotonic()
    resp = requests.get(url, headers=HEADERS, timeout=60, allow_redirects=False)
    _fetched += 1
    if resp.status_code != 200:
        raise Stop(f"HTTP {resp.status_code} for {url}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(resp.text, encoding="utf-8")
    print(f"fetched {url}", flush=True)
    return resp.text


def team_codes(league_html, season):
    """Team codes linked as /teams/XXX/{season}.shtml, including links inside comments."""
    return sorted(set(re.findall(rf'href="/teams/([A-Z]{{3}})/{season}\.shtml"', league_html)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("first", type=int)
    ap.add_argument("last", type=int)
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    try:
        for season in range(args.first, args.last + 1):
            league = fetch(f"{BASE}/leagues/majors/{season}.shtml",
                           CACHE / str(season) / "league.html", args.limit)
            codes = team_codes(league, season)
            if len(codes) != 30:
                raise Stop(f"{season}: league page lists {len(codes)} teams: {codes}")
            for code in codes:
                fetch(f"{BASE}/teams/{code}/{season}-playoff-odds.shtml",
                      CACHE / str(season) / f"{code}.html", args.limit)
            print(f"{season}: 30 pages cached", flush=True)
    except Stop as e:
        print(f"STOPPED: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"done; {_fetched} requests made")


if __name__ == "__main__":
    main()
