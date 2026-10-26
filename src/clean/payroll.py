"""Build data/processed/payroll.csv from data/raw/cots_payroll.csv (Cot's club payroll tables).

One row per club-season, 2011-2026. Payrolls are whole dollars parsed from Cot's cell text
(the MLB rank in parentheses is dropped). Clubs are matched to windows.csv team_id by the
Cot's page URL, so the Athletics (OAK/ATH), Cleveland and Miami need no name matching.
team is the windows.csv club code for that season (OAK through 2024, ATH from 2025; the
URL's code for 2011-2013, which windows.csv lacks). team_name is the club name from the
page URL, current name for every season (e.g. Cleveland Guardians before 2022).

od_cbt_payroll is blank throughout: no Cot's club page shows an Opening Day CB Tax figure.
od_rel is a club's Opening Day payroll divided by the 30-club mean that season;
od_log2_rel is its base-2 log. 2020 Opening Day figures are used as published.

Exact duplicate rows (the Brewers page lists 2020 twice) are dropped; conflicting
duplicates are a failure.

Checks, for each season 2014-2026:
  1. all 30 clubs have an Opening Day payroll;
  2. the team_id set matches windows.csv exactly;
  3. od_rel averages 1.000.
A failure in 2014-2025 stops the script and nothing is written; a 2026 failure is reported
and the build continues. Also reported, not checked: clubs whose Opening Day payroll changed
more than 60% year over year, and parsed values whose order disagrees with Cot's published
rank.

Run from the repo root: python3 src/clean/payroll.py
"""

import csv
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "cots_payroll.csv"
WINDOWS = ROOT / "data" / "processed" / "windows.csv"
OUT = ROOT / "data" / "processed" / "payroll.csv"

CHECK_SEASONS = range(2014, 2027)
SOFT_SEASONS = {2026}  # failures reported, build continues
YOY_LIMIT = 0.60
REL_TOL = 0.0005

COLUMNS = [
    "season", "team_id", "team", "team_name", "od_payroll", "ye_payroll", "cbt_payroll", "od_cbt_payroll",
    "od_rel", "od_log2_rel",
]

# Cot's page slug -> windows.csv club code
SLUGS = {
    "baltimore-orioles": "BAL", "boston-red-sox": "BOS", "new-york-yankees": "NYY",
    "tampa-bay-rays": "TBR", "toronto-blue-jays": "TOR", "chicago-white-sox": "CHW",
    "cleveland-guardians": "CLE", "detroit-tigers": "DET", "kansas-city-royals": "KCR",
    "minnesota-twins": "MIN", "athletics": "OAK", "houston-astros": "HOU",
    "los-angeles-angels": "LAA", "seattle-mariners": "SEA", "texas-rangers": "TEX",
    "atlanta-braves": "ATL", "miami-marlins": "MIA", "new-york-mets": "NYM",
    "philadelphia-phillies": "PHI", "washington-nationals": "WSN", "chicago-cubs": "CHC",
    "cincinnati-reds": "CIN", "milwaukee-brewers": "MIL", "pittsburgh-pirates": "PIT",
    "st-louis-cardinals": "STL", "arizona-diamondbacks": "ARI", "colorado-rockies": "COL",
    "los-angeles-dodgers": "LAD", "san-diego-padres": "SDP", "san-francisco-giants": "SFG",
}


def money(text):
    """'$ 92,970,900 (26)' -> (92970900, 26); blank -> (None, None)."""
    text = text.strip()
    if not text:
        return None, None
    m = re.fullmatch(r"\$([\d,\s]+)\(\s*(\d+)\)", text)
    if not m:
        raise ValueError(f"unparsed payroll cell {text!r}")
    return int(re.sub(r"\D", "", m.group(1))), int(m.group(2))


def windows_ids():
    """Club code -> team_id, season -> set of team_ids, and (season, team_id) -> club code,
    from windows.csv."""
    by_code, by_season, codes = {}, defaultdict(set), {}
    with open(WINDOWS, newline="") as f:
        for r in csv.DictReader(f):
            by_code[r["team"]] = r["team_id"]
            by_season[int(r["season"])].add(r["team_id"])
            codes[(int(r["season"]), r["team_id"])] = r["team"]
    return by_code, by_season, codes


def team_name(slug):
    """'st-louis-cardinals' -> 'St. Louis Cardinals'."""
    return slug.replace("-", " ").title().replace("St Louis", "St. Louis")


def read_raw(by_code, codes, failures):
    seen = {}
    with open(RAW, newline="") as f:
        for r in csv.DictReader(line for line in f if not line.startswith("#")):
            slug = r["page_url"].rstrip("/").rsplit("/", 1)[-1]
            key = (int(r["season"]), by_code[SLUGS[slug]])
            cells = (r["od_payroll_text"], r["ye_payroll_text"], r["cbt_payroll_text"])
            if key in seen and seen[key][0] != cells:
                failures.append(f"{key[0]} {SLUGS[slug]}: conflicting duplicate rows")
            seen.setdefault(key, (cells, slug))
    rows = []
    for (season, team_id), ((od, ye, cbt), slug) in seen.items():
        code = codes.get((season, team_id), SLUGS[slug])
        (od_v, od_rank), (ye_v, ye_rank), (cbt_v, cbt_rank) = money(od), money(ye), money(cbt)
        rows.append({
            "season": season, "team_id": team_id, "code": code,
            "team": code, "team_name": team_name(slug),
            "od_payroll": od_v, "ye_payroll": ye_v, "cbt_payroll": cbt_v, "od_cbt_payroll": None,
            "ranks": {"od_payroll": od_rank, "ye_payroll": ye_rank, "cbt_payroll": cbt_rank},
        })
    return rows


def relative(rows):
    by_season = defaultdict(list)
    for r in rows:
        by_season[r["season"]].append(r)
    for grp in by_season.values():
        ods = [r["od_payroll"] for r in grp if r["od_payroll"] is not None]
        mean = sum(ods) / len(ods)
        for r in grp:
            r["od_rel"] = r["od_payroll"] / mean if r["od_payroll"] is not None else None
            r["od_log2_rel"] = math.log2(r["od_rel"]) if r["od_rel"] else None
    return by_season


def check(by_season, windows_by_season, failures, soft, notes):
    for season in CHECK_SEASONS:
        grp = by_season.get(season, [])
        out = soft if season in SOFT_SEASONS else failures
        # 1. 30 clubs with an Opening Day payroll
        n_od = sum(r["od_payroll"] is not None for r in grp)
        if n_od != 30:
            out.append(f"{season}: {n_od} clubs with an Opening Day payroll, expected 30")
        # 2. team_id set matches windows.csv
        ids = {r["team_id"] for r in grp}
        if ids != windows_by_season[season]:
            out.append(f"{season}: team_ids missing {sorted(windows_by_season[season] - ids)}, "
                       f"extra {sorted(ids - windows_by_season[season])}")
        # 3. od_rel averages 1
        rels = [r["od_rel"] for r in grp if r["od_rel"] is not None]
        mean_rel = sum(rels) / len(rels)
        notes.append(f"{season}: mean od_rel {mean_rel:.3f} over {len(rels)} clubs")
        if abs(mean_rel - 1) > REL_TOL:
            out.append(f"{season}: mean od_rel {mean_rel:.4f}")


def yoy(by_season):
    prev = {r["team_id"]: r for r in by_season.get(min(CHECK_SEASONS) - 1, [])}
    flagged = []
    for season in CHECK_SEASONS:
        cur = {r["team_id"]: r for r in by_season.get(season, [])}
        for tid, r in sorted(cur.items(), key=lambda kv: kv[1]["code"]):
            p = prev.get(tid)
            if p and p["od_payroll"] and r["od_payroll"]:
                change = r["od_payroll"] / p["od_payroll"] - 1
                if abs(change) > YOY_LIMIT:
                    flagged.append(f"{season} {r['code']}: {p['od_payroll']:,} -> "
                                   f"{r['od_payroll']:,} ({change:+.0%})")
        prev = cur
    return flagged


def rank_mismatches(by_season):
    """Parsed values whose descending order disagrees with Cot's published rank."""
    out = []
    for season, grp in sorted(by_season.items()):
        for col in ("od_payroll", "ye_payroll", "cbt_payroll"):
            vals = [r for r in grp if r[col] is not None]
            for r in vals:
                implied = 1 + sum(o[col] > r[col] for o in vals)
                if implied != r["ranks"][col]:
                    out.append(f"{season} {r['code']} {col}: {r[col]:,} published rank "
                               f"{r['ranks'][col]}, implied {implied}")
    return out


def fmt(v):
    if v is None:
        return ""
    return f"{v:.6f}" if isinstance(v, float) else v


def main():
    by_code, windows_by_season, codes = windows_ids()
    failures, soft, notes = [], [], []
    rows = read_raw(by_code, codes, failures)
    by_season = relative(rows)
    check(by_season, windows_by_season, failures, soft, notes)

    for n in notes:
        print(n)
    flagged = yoy(by_season)
    print(f"\nOpening Day payroll changes over {YOY_LIMIT:.0%} year over year ({len(flagged)}):")
    for f in flagged:
        print(f"  {f}")
    mism = rank_mismatches(by_season)
    print(f"\nParsed values out of order with Cot's published rank ({len(mism)}):")
    for m in mism:
        print(f"  {m}")
    if soft:
        print("\n2026 check(s) failed (reported, build continues):")
        for s in soft:
            print(f"  {s}")
    if failures:
        print(f"\n{len(failures)} check(s) failed; nothing written:", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        sys.exit(1)

    rows.sort(key=lambda r: (r["season"], int(r["team_id"])))
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: fmt(r[k]) for k in COLUMNS})
    print(f"\nwrote {OUT.relative_to(ROOT)}: {len(rows)} rows")


if __name__ == "__main__":
    main()
