"""Validate Baseball-Reference preseason odds against windows.csv and backcast 2014 spell entries.

Reads data/processed/bref_od.csv (src/clean/bref_odds.py) and data/processed/windows.csv.

Validation, 2014-2026: agreement of bref_top6 with window_top6 over all 390 club-seasons
and by season; Spearman correlation of bref_rank with od_rank by season (both leagues
pooled, as asked; within-league figures are reported alongside); and agreement in 2014
for the clubs whose top-6 spells were open in 2014. The gate passes when overall
agreement is at least 85%.

Entry durations: for each top-6 spell open in 2014 (strict consecutive, as in spells.py),
entry_2014 = 1 + the number of consecutive seasons immediately before 2014 (2013, then
2012, then 2011) in which the club is bref_top6, capped at 4. A club with no bref row
for a season (no team_id match) counts as not top 6 there. Computed whether or not the
gate passes; gate_passed is recorded in each row.

Writes data/processed/backcast_entry.csv and the "backcast" key of results/results.json.
Other keys of results.json are left as they are.

Run from the repo root: python3 src/analysis/backcast.py
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spells import find_spells  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BREF = ROOT / "data" / "processed" / "bref_od.csv"
WINDOWS = ROOT / "data" / "processed" / "windows.csv"
ENTRY_OUT = ROOT / "data" / "processed" / "backcast_entry.csv"
RESULTS = ROOT / "results" / "results.json"

VALID_SEASONS = range(2014, 2027)
PRE_SEASONS = [2013, 2012, 2011]
ENTRY_CAP = 4
GATE = 0.85

ENTRY_COLUMNS = [
    "team_id", "spell_start", "spell_end", "bref_top6_2011", "bref_top6_2012",
    "bref_top6_2013", "entry_2014", "gate_passed",
]


def avg_ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def spearman(x, y):
    rx, ry = avg_ranks(x), avg_ranks(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = sum((a - mx) ** 2 for a in rx)
    vy = sum((b - my) ** 2 for b in ry)
    return cov / (vx * vy) ** 0.5


def load():
    with open(BREF, newline="") as f:
        bref = list(csv.DictReader(f))
    with open(WINDOWS, newline="") as f:
        windows = list(csv.DictReader(f))
    return bref, windows


def main():
    bref, windows = load()
    bref_by = {(int(r["season"]), r["team_id"]): r for r in bref if r["team_id"]}
    failures = []

    # Validation pairs, 2014-2026.
    pairs = []
    for w in windows:
        s = int(w["season"])
        b = bref_by.get((s, w["team_id"]))
        if b is None:
            failures.append(f"{s} team_id {w['team_id']} ({w['team']}): no bref row")
            continue
        if b["league"] != w["league"]:
            failures.append(f"{s} {w['team']}: league {w['league']} in windows, {b['league']} in bref")
        pairs.append((s, w, b))
    if len(pairs) != 390:
        failures.append(f"{len(pairs)} matched club-seasons, expected 390")

    # Spells open in 2014 (strict top 6), keyed by team_id.
    clubs = defaultdict(dict)
    teams = {}
    for w in windows:
        clubs[w["team_id"]][int(w["season"])] = int(w["window_top6"])
        teams[w["team_id"]] = w["team"]
    open_2014 = []
    for team_id, flags in clubs.items():
        for first, last in find_spells(flags, grace=False):
            if first == 2014:
                open_2014.append((team_id, first, last))
    open_2014.sort(key=lambda t: teams[t[0]])
    if len(open_2014) != 12:
        failures.append(f"{len(open_2014)} spells open in 2014, expected 12")

    if failures:
        print(f"{len(failures)} check(s) failed; nothing written:", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        sys.exit(1)

    def agree(ps):
        hits = sum(w["window_top6"] == b["bref_top6"] for _, w, b in ps)
        return {"agree": hits, "n": len(ps), "rate": round(hits / len(ps), 4)}

    overall = agree(pairs)
    by_season = {str(s): agree([p for p in pairs if p[0] == s]) for s in VALID_SEASONS}

    spearman_by_season = {}
    spearman_by_league = {}
    for s in VALID_SEASONS:
        ps = [p for p in pairs if p[0] == s]
        spearman_by_season[str(s)] = round(
            spearman([int(b["bref_rank"]) for _, _, b in ps], [int(w["od_rank"]) for _, w, _ in ps]), 4)
        for lg in ("AL", "NL"):
            lp = [p for p in ps if p[1]["league"] == lg]
            spearman_by_league[f"{s} {lg}"] = round(
                spearman([int(b["bref_rank"]) for _, _, b in lp], [int(w["od_rank"]) for _, w, _ in lp]), 4)

    open_ids = {t for t, _, _ in open_2014}
    open_pairs = [p for p in pairs if p[0] == 2014 and p[1]["team_id"] in open_ids]
    open_agree = agree(open_pairs)
    open_agree["clubs"] = {w["team"]: {"window_top6": int(w["window_top6"]), "bref_top6": int(b["bref_top6"]),
                                       "bref_rank": int(b["bref_rank"]), "od_rank": int(w["od_rank"])}
                           for _, w, b in open_pairs}

    gate_passed = overall["rate"] >= GATE

    # Entry durations.
    entries = []
    for team_id, first, last in open_2014:
        flags = {}
        for s in PRE_SEASONS:
            b = bref_by.get((s, team_id))
            flags[s] = int(b["bref_top6"]) if b else 0
        run = 0
        for s in PRE_SEASONS:
            if not flags[s]:
                break
            run += 1
        entries.append({
            "team_id": team_id, "team": teams[team_id], "spell_start": first, "spell_end": last,
            "bref_top6_2011": flags[2011], "bref_top6_2012": flags[2012], "bref_top6_2013": flags[2013],
            "entry_2014": min(1 + run, ENTRY_CAP), "gate_passed": int(gate_passed),
        })

    with open(ENTRY_OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ENTRY_COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(entries)

    # Per-season data facts from bref_od.csv.
    dates, post_sums = {}, {}
    for r in bref:
        dates[r["season"]] = r["date"]
        key = f"{r['season']} {r['league']}"
        post_sums[key] = post_sums.get(key, 0.0) + float(r["post"])

    results = json.loads(RESULTS.read_text())
    results["backcast"] = {
        "source": "Baseball-Reference preseason playoff odds (earliest row per club-season)",
        "seasons": [2011, 2026],
        "preseason_date": dict(sorted(dates.items())),
        "post_sum_by_league": {k: round(v, 3) for k, v in sorted(post_sums.items())},
        "unmatched_bref_clubs": [f"{r['season']} {r['bref_team']}" for r in bref if not r["team_id"]],
        "validation": {
            "seasons": [2014, 2026],
            "top6_agreement": overall,
            "top6_agreement_by_season": by_season,
            "spearman_bref_rank_od_rank_by_season": spearman_by_season,
            "spearman_bref_rank_od_rank_by_season_league": spearman_by_league,
            "open_2014_agreement": open_agree,
            "gate_threshold": GATE,
            "gate_passed": gate_passed,
        },
        "entry_2014": {
            "cap": ENTRY_CAP,
            "gate_passed": gate_passed,
            "spells": entries,
            "distribution": {str(k): sum(e["entry_2014"] == k for e in entries)
                             for k in range(1, ENTRY_CAP + 1)},
        },
    }
    RESULTS.write_text(json.dumps(results, indent=2) + "\n")

    print(f"top-6 agreement: {overall['agree']}/{overall['n']} = {overall['rate']:.1%}; "
          f"gate (>= {GATE:.0%}) {'passed' if gate_passed else 'failed'}")
    for s in VALID_SEASONS:
        a = by_season[str(s)]
        print(f"  {s}: agreement {a['agree']}/30 = {a['rate']:.1%}, spearman {spearman_by_season[str(s)]:.3f}")
    print(f"open-2014 clubs, 2014 agreement: {open_agree['agree']}/{open_agree['n']}")
    for e in entries:
        print(f"  {e['team']}: {e['spell_start']}-{e['spell_end']}  "
              f"2011-13 {e['bref_top6_2011']}{e['bref_top6_2012']}{e['bref_top6_2013']}  entry {e['entry_2014']}")
    print(f"wrote {ENTRY_OUT.relative_to(ROOT)} and the backcast key of {RESULTS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
