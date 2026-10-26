"""Classify club-seasons into contention patterns and add them to results/results.json.

Each club-season gets three readings at threshold k, where "above" means rank <= k:

- Opening Day   od_rank
- Deadline      pd_rank
- Next season   the same club's od_rank the following season (matched on team_id)

    Opening Day  Deadline  Next season  Label
    Below        Above     Below        Surprise, not carried forward
    Below        Above     Above        Surprise, carried forward
    Above        Above     Below        Held, not carried forward
    Above        Above     Above        Held, carried forward
    Above        Below     Above        Gap year
    Above        Below     Below        Fizzled
    Below        Below     either       Out of contention

2026 has no next season, so its rows get partial labels (Surprise / Held / Fell out, each
"(next unknown)", or Out of contention) and stay out of the 2014-2025 counts.

Part 1 runs every k from 3 to 9 (6 is the baseline). Part 2, at the baseline only, builds a
club x season label grid (results/label_grid.csv) and counts clubs with Surprise labels, or
with Held, not carried forward / Fizzled labels, in two or more consecutive seasons, against a null that
shuffles labels across clubs within each season. Consecutive runs use 2014-2025 only; the
2026 partial labels are in the grid but not in the counts.

Other keys in results.json are left as they are; this script writes only "patterns".
Nothing is written if any check fails.

Run from the repo root: python3 src/analysis/patterns.py
"""

import csv
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IN = ROOT / "data" / "processed" / "windows.csv"
OUT = ROOT / "results" / "results.json"
GRID_OUT = ROOT / "results" / "label_grid.csv"

FIRST, LAST = 2014, 2026
SEASONS = list(range(FIRST, LAST + 1))
FULL_SEASONS = SEASONS[:-1]  # 2014-2025: next season is known
THRESHOLDS = range(3, 10)
BASELINE = 6
N_CLUBS = 30
N_SHUFFLES = 10_000
SEED = 20261024

SURPRISE_NC = "Surprise, not carried forward"
SURPRISE_CF = "Surprise, carried forward"
HELD_NC = "Held, not carried forward"
HELD_CF = "Held, carried forward"
GAP = "Gap year"
FIZZLED = "Fizzled"
OUT_OF = "Out of contention"
FULL_LABELS = [SURPRISE_NC, SURPRISE_CF, HELD_NC, HELD_CF, GAP, FIZZLED, OUT_OF]
PARTIAL_LABELS = ["Surprise (next unknown)", "Held (next unknown)",
                  "Fell out (next unknown)", OUT_OF]

# (od above, pd above, next above) -> label
FULL_TABLE = {
    (False, True, False): SURPRISE_NC,
    (False, True, True): SURPRISE_CF,
    (True, True, False): HELD_NC,
    (True, True, True): HELD_CF,
    (True, False, True): GAP,
    (True, False, False): FIZZLED,
    (False, False, False): OUT_OF,
    (False, False, True): OUT_OF,
}
# (od above, pd above) -> label
PARTIAL_TABLE = {
    (False, True): PARTIAL_LABELS[0],
    (True, True): PARTIAL_LABELS[1],
    (True, False): PARTIAL_LABELS[2],
    (False, False): PARTIAL_LABELS[3],
}

SURPRISE_SET = {SURPRISE_NC, SURPRISE_CF}
HELD_NC_SET = {HELD_NC, FIZZLED}
LISTED = [SURPRISE_NC, SURPRISE_CF, GAP, FIZZLED]


def label_all(rows, k, failures):
    """Return {(season, team_id): label} at threshold k."""
    labels = {}
    for (season, team_id), r in rows.items():
        od, pd = r["od_rank"] <= k, r["pd_rank"] <= k
        if season == LAST:
            labels[(season, team_id)] = PARTIAL_TABLE[(od, pd)]
            continue
        nxt = rows.get((season + 1, team_id))
        if nxt is None:
            failures.append(f"k={k}: {season} {r['team']} has no {season + 1} row")
            continue
        labels[(season, team_id)] = FULL_TABLE[(od, pd, nxt["od_rank"] <= k)]
    return labels


def check(labels, rows, k, failures):
    full = {key: lab for key, lab in labels.items() if key[0] != LAST}
    if len(full) != len(FULL_SEASONS) * N_CLUBS:
        failures.append(f"k={k}: {len(full)} labeled 2014-2025 club-seasons, "
                        f"expected {len(FULL_SEASONS) * N_CLUBS}")
    if set(full.values()) - set(FULL_LABELS):
        failures.append(f"k={k}: unexpected 2014-2025 labels {set(full.values()) - set(FULL_LABELS)}")
    missing = [key for key in rows if key[0] != LAST and key not in labels]
    if missing:
        failures.append(f"k={k}: {len(missing)} 2014-2025 club-seasons without a label")
    for season in FULL_SEASONS:
        c = Counter(lab for (s, _), lab in full.items() if s == season)
        od_side = c[HELD_CF] + c[HELD_NC] + c[GAP] + c[FIZZLED]
        pd_side = c[HELD_CF] + c[HELD_NC] + c[SURPRISE_NC] + c[SURPRISE_CF]
        if od_side != 2 * k:
            failures.append(f"k={k} {season}: Held+Gap+Fizzled = {od_side}, expected {2 * k}")
        if pd_side != 2 * k:
            failures.append(f"k={k} {season}: Held+Surprises = {pd_side}, expected {2 * k}")
    last = [lab for (s, _), lab in labels.items() if s == LAST]
    if len(last) != N_CLUBS or set(last) - set(PARTIAL_LABELS):
        failures.append(f"k={k}: {len(last)} 2026 rows with labels {sorted(set(last))}; "
                        f"expected {N_CLUBS}, all partial")


def summarize(labels, rows, k):
    full = {key: lab for key, lab in labels.items() if key[0] != LAST}
    overall = Counter(full.values())
    by_season = {}
    for season in FULL_SEASONS:
        c = Counter(lab for (s, _), lab in full.items() if s == season)
        by_season[str(season)] = {lab: c[lab] for lab in FULL_LABELS}
    partial = Counter(lab for (s, _), lab in labels.items() if s == LAST)
    out = {
        "k": k,
        "counts_2014_2025": {lab: overall[lab] for lab in FULL_LABELS},
        "counts_by_season": by_season,
        "partial_2026": {lab: partial[lab] for lab in PARTIAL_LABELS},
    }
    if k == BASELINE:
        out["listed"] = {
            lab: [{"season": s, "team_id": t, "team": rows[(s, t)]["team"],
                   "od_rank": rows[(s, t)]["od_rank"], "pd_rank": rows[(s, t)]["pd_rank"],
                   "next_od_rank": rows[(s + 1, t)]["od_rank"]}
                  for (s, t), l in sorted(full.items()) if l == lab]
            for lab in LISTED
        }
    return out


def clubs_with_runs(grid, label_set):
    """Number of clubs with labels in label_set in two or more consecutive seasons."""
    n = 0
    for seq in grid.values():
        if any(a in label_set and b in label_set for a, b in zip(seq, seq[1:])):
            n += 1
    return n


def percentile(values, q):
    # Linear interpolation between order statistics (numpy's default).
    xs = sorted(values)
    pos = (len(xs) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


def sequences(labels, team_ids):
    # grid restricted to 2014-2025, one list per club in season order
    grid = {t: [labels[(s, t)] for s in FULL_SEASONS] for t in team_ids}
    observed = {"surprise": clubs_with_runs(grid, SURPRISE_SET),
                "held_nc_or_fizzled": clubs_with_runs(grid, HELD_NC_SET)}
    rng = random.Random(SEED)
    null = {name: [] for name in observed}
    columns = [[grid[t][i] for t in team_ids] for i in range(len(FULL_SEASONS))]
    for _ in range(N_SHUFFLES):
        shuffled = []
        for col in columns:
            col = col[:]
            rng.shuffle(col)
            shuffled.append(col)
        sim = {t: [shuffled[i][j] for i in range(len(FULL_SEASONS))]
               for j, t in enumerate(team_ids)}
        null["surprise"].append(clubs_with_runs(sim, SURPRISE_SET))
        null["held_nc_or_fizzled"].append(clubs_with_runs(sim, HELD_NC_SET))
    return {
        name: {
            "observed": observed[name],
            "null_mean": round(sum(null[name]) / N_SHUFFLES, 3),
            "null_p95": percentile(null[name], 0.95),
            "share_null_at_least_observed": round(
                sum(v >= observed[name] for v in null[name]) / N_SHUFFLES, 4),
            "clubs": sorted(
                rows_team for t, rows_team in team_ids.items()
                if clubs_with_runs({t: grid[t]}, SURPRISE_SET if name == "surprise" else HELD_NC_SET)),
        }
        for name in observed
    }


def main():
    with open(IN, newline="") as f:
        raw = list(csv.DictReader(f))

    failures = []
    rows = {}
    team_ids = {}  # team_id -> current abbreviation
    for r in raw:
        key = (int(r["season"]), r["team_id"])
        if key in rows:
            failures.append(f"{key}: duplicate row")
        rows[key] = {"team": r["team"], "od_rank": int(r["od_rank"]),
                     "pd_rank": int(r["pd_rank"])}
        if key[0] == LAST:
            team_ids[r["team_id"]] = r["team"]
    if len(team_ids) != N_CLUBS:
        failures.append(f"{len(team_ids)} clubs in {LAST}, expected {N_CLUBS}")

    by_k = {}
    labels_by_k = {}
    for k in THRESHOLDS:
        labels = label_all(rows, k, failures)
        check(labels, rows, k, failures)
        labels_by_k[k] = labels
        by_k[f"top{k}"] = summarize(labels, rows, k)
    if failures:
        print(f"{len(failures)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in failures:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    base = labels_by_k[BASELINE]
    team_ids = dict(sorted(team_ids.items(), key=lambda kv: kv[1]))
    seq = sequences(base, team_ids)

    results = json.loads(OUT.read_text()) if OUT.exists() else {}
    results["patterns"] = {
        "definition": ("Readings at threshold k: Opening Day od_rank, deadline pd_rank, and the "
                       "same club's od_rank the following season; above means rank <= k. "
                       "2026 rows get partial labels and are excluded from 2014-2025 counts."),
        "baseline": f"top{BASELINE}",
        "by_threshold": by_k,
        "sequences": {
            "threshold": f"top{BASELINE}",
            "seasons": [FIRST, LAST - 1],
            "note": ("Clubs with labels from the set in two or more consecutive seasons, "
                     "2014-2025 (2026 partial labels excluded). Null: labels shuffled across "
                     f"clubs within each season, {N_SHUFFLES} times, seed {SEED}; p95 uses "
                     "linear interpolation."),
            "surprise_either_kind": seq["surprise"],
            "held_not_carried_forward_or_fizzled": seq["held_nc_or_fizzled"],
            "grid_file": str(GRID_OUT.relative_to(ROOT)),
        },
    }

    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
        f.write("\n")
    with open(GRID_OUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["team_id", "team"] + SEASONS)
        for t, team in team_ids.items():
            writer.writerow([t, team] + [base[(s, t)] for s in SEASONS])

    print("All checks passed at every k.")
    short = {SURPRISE_NC: "S-NC", SURPRISE_CF: "S-CF", HELD_NC: "H-NC", HELD_CF: "H-CF",
             GAP: "GY", FIZZLED: "Fz", OUT_OF: "Out"}
    for name, res in by_k.items():
        c = res["counts_2014_2025"]
        print(f"\n{name} 2014-2025: " + ", ".join(f"{short[l]} {c[l]}" for l in FULL_LABELS))
        print(f"  2026 partial: " + ", ".join(f"{l} {n}" for l, n in res["partial_2026"].items()))
    print(f"\nBaseline by season ({', '.join(f'{v}={k}' for k, v in short.items())}):")
    for season, c in by_k[f"top{BASELINE}"]["counts_by_season"].items():
        print(f"  {season}: " + " ".join(f"{short[l]}:{c[l]}" for l in FULL_LABELS))
    print("\nBaseline listed club-seasons:")
    for lab, items in by_k[f"top{BASELINE}"]["listed"].items():
        print(f"  {lab} ({len(items)}): "
              + ", ".join(f"{i['team']} {i['season']}" for i in items))
    print("\nSequences (baseline, 2014-2025):")
    for name in ("surprise", "held_nc_or_fizzled"):
        s = seq[name]
        print(f"  {name}: observed {s['observed']}, null mean {s['null_mean']}, "
              f"p95 {s['null_p95']}, P(null >= obs) {s['share_null_at_least_observed']}  "
              f"{s['clubs']}")
    print(f"\nWrote patterns to {OUT.relative_to(ROOT)} and {GRID_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
