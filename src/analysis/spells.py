"""Count window spells from data/processed/windows.csv and write results/results.json.

A spell is a run of consecutive seasons in which a club is in a window. Clubs are keyed by
team_id, so OAK and ATH are one club. Four variants, per §3.3 of the research plan:

- top6        strict consecutive, threshold 6 (the baseline)
- top5, top8  strict consecutive, thresholds 5 and 8
- top6_grace  threshold 6, one-season-dip grace rule: a single out-of-window season between
              two in-window seasons does not end the spell. A grace spell's length is its
              span, first season to last inclusive, so the dip season counts toward it;
              in_window_seasons gives the count without dips.

For each variant: the number of spells, the distribution of spell lengths, persistent
contenders (clubs with one spell covering all 13 seasons), and spells open in 2014
(left-censored) or 2026 (right-censored).

Nothing is written if any check fails.

Run from the repo root: python3 src/analysis/spells.py
"""

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IN = ROOT / "data" / "processed" / "windows.csv"
OUT = ROOT / "results" / "results.json"

FIRST, LAST = 2014, 2026
SEASONS = list(range(FIRST, LAST + 1))
BASELINE_IN_WINDOW = 156  # 6 clubs x 2 leagues x 13 seasons

VARIANTS = {
    "top6": ("window_top6", False),
    "top5": ("window_top5", False),
    "top8": ("window_top8", False),
    "top6_grace": ("window_top6", True),
}


def find_spells(in_window, grace):
    """Return [(first, last)] for one club, given {season: 0/1}."""
    seasons = [s for s in SEASONS if in_window[s]]
    spells = []
    for s in seasons:
        gap = s - spells[-1][1] if spells else None
        if gap == 1 or (grace and gap == 2):
            spells[-1][1] = s
        else:
            spells.append([s, s])
    return [tuple(sp) for sp in spells]


def summarize(clubs, column, grace):
    spells = []
    for team_id, info in sorted(clubs.items(), key=lambda kv: kv[1]["team"]):
        flags = {s: info["rows"][s][column] for s in SEASONS}
        for first, last in find_spells(flags, grace):
            spells.append({
                "team_id": team_id,
                "team": info["team"],
                "first": first,
                "last": last,
                "length": last - first + 1,
                "in_window_seasons": sum(flags[s] for s in range(first, last + 1)),
            })
    lengths = Counter(sp["length"] for sp in spells)
    full = [sp for sp in spells if sp["length"] == len(SEASONS)]
    return {
        "column": column,
        "grace": grace,
        "in_window_club_seasons": sum(
            info["rows"][s][column] for info in clubs.values() for s in SEASONS),
        "n_spells": len(spells),
        "length_distribution": {str(k): lengths[k] for k in sorted(lengths)},
        "persistent_contenders": {
            "count": len(full),
            "clubs": [sp["team"] for sp in full],
        },
        "left_censored": {
            "count": sum(sp["first"] == FIRST for sp in spells),
            "spells": [sp for sp in spells if sp["first"] == FIRST],
        },
        "right_censored": {
            "count": sum(sp["last"] == LAST for sp in spells),
            "spells": [sp for sp in spells if sp["last"] == LAST],
        },
        "spells": spells,
    }


def main():
    with open(IN, newline="") as f:
        rows = list(csv.DictReader(f))

    failures = []
    clubs = defaultdict(lambda: {"team": None, "rows": {}})
    for r in rows:
        season = int(r["season"])
        club = clubs[r["team_id"]]
        if season in club["rows"]:
            failures.append(f"{season} team {r['team_id']}: duplicate row")
        club["rows"][season] = {c: int(r[c]) for c in ("window_top5", "window_top6", "window_top8")}
        if season == LAST:
            club["team"] = r["team"]  # current abbreviation, e.g. ATH not OAK
    for team_id, club in clubs.items():
        missing = [s for s in SEASONS if s not in club["rows"]]
        if missing:
            failures.append(f"team {team_id}: no rows for {missing}")
    if failures:
        print(f"{len(failures)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in failures:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    results = {name: summarize(clubs, col, grace) for name, (col, grace) in VARIANTS.items()}
    results["top6_grace"]["length_note"] = (
        "Grace spell length is the full span, first season to last inclusive, so a one-season "
        "dip inside the spell counts toward its length (and toward length_distribution, "
        "persistent_contenders and the 13-season cap). in_window_seasons on each spell counts "
        "only the seasons actually in the window; those sum to in_window_club_seasons.")

    # (1) baseline in-window count
    n = results["top6"]["in_window_club_seasons"]
    if n != BASELINE_IN_WINDOW:
        failures.append(f"top6: {n} in-window club-seasons, expected {BASELINE_IN_WINDOW}")
    for name, res in results.items():
        spells = res["spells"]
        # (2) strict spell lengths add up to the in-window count; grace spells add up when
        # dip seasons are left out
        total = sum(sp["in_window_seasons" if res["grace"] else "length"] for sp in spells)
        if total != res["in_window_club_seasons"]:
            failures.append(f"{name}: spell lengths sum to {total}, "
                            f"expected {res['in_window_club_seasons']}")
        # (3) no spell longer than the panel
        for sp in spells:
            if sp["length"] > len(SEASONS):
                failures.append(f"{name}: {sp['team']} spell {sp['first']}-{sp['last']} "
                                f"is {sp['length']} seasons")
        # (4) every full-length strict spell is a club in a window every season
        if not res["grace"]:
            for sp in spells:
                if sp["length"] == len(SEASONS) and not all(
                        clubs[sp["team_id"]]["rows"][s][res["column"]] for s in SEASONS):
                    failures.append(f"{name}: {sp['team']} has a 13-season spell but is "
                                    f"out of the window in some season")
    if failures:
        print(f"{len(failures)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in failures:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"seasons": [FIRST, LAST], "variants": results}, f, indent=2)
        f.write("\n")

    print("All checks passed.")
    for name, res in results.items():
        print(f"\n{name}: {res['in_window_club_seasons']} in-window club-seasons, "
              f"{res['n_spells']} spells")
        print("  lengths:", ", ".join(f"{k}:{v}" for k, v in res["length_distribution"].items()))
        pc = res["persistent_contenders"]
        print(f"  persistent contenders: {pc['count']} {pc['clubs']}")
        for side in ("left_censored", "right_censored"):
            c = res[side]
            print(f"  {side}: {c['count']} "
                  + ", ".join(f"{sp['team']} {sp['first']}-{sp['last']}" for sp in c["spells"]))
    print(f"\nWrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
