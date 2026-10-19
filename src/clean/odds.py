"""Build data/processed/odds.csv from the FanGraphs playoff-odds snapshots in data/raw/.

One row per club per snapshot (Opening Day, pre-deadline, end of season), 2014-2026.
See docs/competitive-windows-research-plan.md §3.2-3.3a.

postseason_odds is FanGraphs' Make Playoffs, except in 2020, where it is rebuilt as
Win Div 1st + Win Div 2nd + Clinch Wild Card to price the 16-team field (§3.3a).

The checks below are run before anything is written. If any fails, the script stops
and lists the failures; it never alters the raw data.

Run from the repo root: python3 src/clean/odds.py
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed" / "odds.csv"

# Raw file -> snapshot label used in the processed table, in chronological order.
SNAPSHOTS = {
    "opening_day": "fg_playoff_odds_lg_first.csv",
    "pre_deadline": "fg_playoff_odds_lg_midseason.csv",
    "end_of_season": "fg_playoff_odds_lg_last_regular_season.csv",
}
SEASONS = range(2014, 2027)
CLUBS_PER_LEAGUE = 15
SUM_TOL = 1e-3  # raw odds carry 6 decimals; per-league sums drift by ~1e-6

COLUMNS = [
    "season", "snapshot", "date", "team_id", "team", "league", "division",
    "postseason_odds", "win_ws", "clinch_bye", "proj_w", "proj_l", "w", "l",
]


def berths_per_league(season):
    if season == 2020:
        return 8
    if season >= 2022:
        return 6
    return 5


def postseason_odds(row):
    if int(row["season"]) == 2020:
        parts = [row["win_div_1st"], row["win_div_2nd"], row["clinch_wild_card"]]
        return f"{sum(float(p) for p in parts):.6f}"
    return row["make_playoffs"]


def check(snapshot, rows, failures):
    by_league = defaultdict(list)
    for r in rows:
        by_league[(int(r["season"]), r["league"])].append(r)

    seasons = {s for s, _ in by_league}
    for s in SEASONS:
        if s not in seasons:
            failures.append(f"{snapshot} {s}: season missing")

    for (season, league), rs in sorted(by_league.items()):
        tag = f"{snapshot} {season} {league}"
        dates = {r["date"] for r in rs}
        if len(dates) != 1:
            failures.append(f"{tag}: {len(dates)} dates {sorted(dates)}")
        teams = {r["team_id"] for r in rs}
        if len(rs) != CLUBS_PER_LEAGUE or len(teams) != CLUBS_PER_LEAGUE:
            failures.append(f"{tag}: {len(rs)} rows, {len(teams)} distinct clubs")

        total = sum(float(r["postseason"]) for r in rs)
        if abs(total - berths_per_league(season)) > SUM_TOL:
            failures.append(
                f"{tag}: postseason odds sum to {total:.4f}, "
                f"expected {berths_per_league(season)}"
            )

        if season == 2020:
            # The rebuilt value should agree with the access_odds column collected with it.
            for r in rs:
                diff = abs(float(r["postseason"]) - float(r["access_odds"]))
                if diff > 1e-6:
                    failures.append(f"{tag} {r['team_abbr']}: rebuilt 2020 odds differ "
                                    f"from access_odds by {diff:.2e}")


def main():
    out_rows, failures = [], []
    for snapshot, filename in SNAPSHOTS.items():
        with open(RAW / filename, newline="") as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            r["postseason"] = postseason_odds(r)
        check(snapshot, rows, failures)
        for r in rows:
            out_rows.append({
                "season": r["season"],
                "snapshot": snapshot,
                "date": r["date"],
                "team_id": r["team_id"],
                "team": r["team_abbr"],
                "league": r["league"],
                "division": r["division"],
                "postseason_odds": r["postseason"],
                "win_ws": r["win_ws"],
                "clinch_bye": r["clinch_bye"],
                "proj_w": r["proj_w"],
                "proj_l": r["proj_l"],
                "w": r["w"],
                "l": r["l"],
            })

    if failures:
        print(f"{len(failures)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in failures:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    order = {name: i for i, name in enumerate(SNAPSHOTS)}
    out_rows.sort(key=lambda r: (int(r["season"]), order[r["snapshot"]],
                                 r["league"], r["division"], r["team"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(out_rows)
    print(f"All checks passed. Wrote {len(out_rows)} rows to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
