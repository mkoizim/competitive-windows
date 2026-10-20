"""Build data/processed/windows.csv from data/processed/odds.csv.

One row per club-season, 2014-2026. Clubs are ranked within their league by postseason
odds at the Opening Day and pre-deadline snapshots, ties broken by projected wins
(higher first). A club-season is in a window at threshold N when its Opening Day rank
is N or better. See docs/competitive-windows-research-plan.md §3.3-3.3a.

Thresholds: 3-9 (6 is the baseline), plus the berth-relative variant, where N is the
season's berths per league: 5 (2014-2019, 2021), 8 (2020), 6 (2022 on).

The plan's second tie-break, run differential, is not in odds.csv. The checks below
stop the script if projected wins ever fail to break a tie, so it is never needed
silently. Nothing is written if any check fails.

Run from the repo root: python3 src/analysis/windows.py
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IN = ROOT / "data" / "processed" / "odds.csv"
OUT = ROOT / "data" / "processed" / "windows.csv"

RANKED_SNAPSHOTS = {"opening_day": "od", "pre_deadline": "pd"}
THRESHOLDS = range(3, 10)
CLUBS_PER_LEAGUE = 15

COLUMNS = (
    ["season", "team_id", "team", "league", "division", "berths",
     "od_postseason_odds", "od_proj_w", "od_rank",
     "pd_postseason_odds", "pd_proj_w", "pd_rank"]
    + [f"window_top{n}" for n in THRESHOLDS]
    + ["window_berth"]
)


def berths_per_league(season):
    # Same rule as src/clean/odds.py.
    if season == 2020:
        return 8
    if season >= 2022:
        return 6
    return 5


def rank_league(rows, tag, failures):
    """Return {team_id: rank} for one league at one snapshot; 1 is best."""
    key = lambda r: (float(r["postseason_odds"]), float(r["proj_w"]))
    ordered = sorted(rows, key=key, reverse=True)
    for a, b in zip(ordered, ordered[1:]):
        if key(a) == key(b):
            failures.append(f"{tag}: {a['team']} and {b['team']} tied on odds and "
                            f"projected wins; run differential needed")
    return {r["team_id"]: i for i, r in enumerate(ordered, start=1)}


def main():
    with open(IN, newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["snapshot"] in RANKED_SNAPSHOTS]

    groups = defaultdict(list)
    for r in rows:
        groups[(int(r["season"]), r["league"], r["snapshot"])].append(r)

    failures = []
    ranks = {}  # (season, snapshot, team_id) -> rank
    for (season, league, snapshot), rs in sorted(groups.items()):
        tag = f"{snapshot} {season} {league}"
        if len({r["team_id"] for r in rs}) != CLUBS_PER_LEAGUE or len(rs) != CLUBS_PER_LEAGUE:
            failures.append(f"{tag}: {len(rs)} rows, expected {CLUBS_PER_LEAGUE} distinct clubs")
        for team_id, rank in rank_league(rs, tag, failures).items():
            ranks[(season, snapshot, team_id)] = rank

    by_club = defaultdict(dict)  # (season, team_id) -> {snapshot: row}
    for r in rows:
        by_club[(int(r["season"]), r["team_id"])][r["snapshot"]] = r

    out_rows = []
    for (season, team_id), snaps in by_club.items():
        missing = [s for s in RANKED_SNAPSHOTS if s not in snaps]
        if missing:
            failures.append(f"{season} team {team_id}: no {', '.join(missing)} row")
            continue
        od, pd = snaps["opening_day"], snaps["pre_deadline"]
        if (od["league"], od["division"]) != (pd["league"], pd["division"]):
            failures.append(f"{season} {od['team']}: league/division differs between snapshots")
        od_rank = ranks[(season, "opening_day", team_id)]
        berths = berths_per_league(season)
        row = {
            "season": season,
            "team_id": team_id,
            "team": od["team"],
            "league": od["league"],
            "division": od["division"],
            "berths": berths,
            "od_postseason_odds": od["postseason_odds"],
            "od_proj_w": od["proj_w"],
            "od_rank": od_rank,
            "pd_postseason_odds": pd["postseason_odds"],
            "pd_proj_w": pd["proj_w"],
            "pd_rank": ranks[(season, "pre_deadline", team_id)],
        }
        for n in THRESHOLDS:
            row[f"window_top{n}"] = int(od_rank <= n)
        row["window_berth"] = int(od_rank <= berths)
        out_rows.append(row)

    if failures:
        print(f"{len(failures)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in failures:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    out_rows.sort(key=lambda r: (r["season"], r["league"], r["od_rank"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(out_rows)
    print(f"All checks passed. Wrote {len(out_rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
