"""2027 window forecasts: P(window closed on 2027 Opening Day) for the 12 window_top6 windows open
on 2026 Opening Day, from M2 in sample F (docs/decisions.md, "2027 window forecasts timestamped",
2026-10-26).

M2 is refit with hazard.py's code; the run stops if any coefficient or clustered standard error
differs from results.json's hazard.models.F.M2 by more than 1e-6. Inputs for season 2026 are built
as in hazard.py: duration = 2026 - spell start + 1 capped at 4 (spells open since 2014 use 4),
era12 = 1, strength from the 2026 Opening Day snapshot, od_log2_rel from payroll.csv. Intervals
are 95% Wald intervals on the logit scale, x'b +/- 1.96 x sqrt(x' V x) with V the club-clustered
covariance of the refit, with both ends transformed to probabilities.

Writes the "forecasts_2027" key of results.json (replacing only that key) and prints the table
and expected number of closed windows for docs/forecasts-2027.md. Nothing is written if any check fails.

Run from the repo root: .venv/bin/python src/analysis/forecasts_2027.py
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hazard import (CAP, COLUMN, FIRST, OUT, REF_RANK, build_pp, fit_logit, load,  # noqa: E402
                    samples, strength_table)
from spells import find_spells  # noqa: E402

SEASON = 2026
N_WINDOWS = 12
TOL = 1e-6
COLS = ["const", "ln_dur", "era12", "strength", "od_log2_rel"]
KEY = "forecasts_2027"


def main():
    windows, odds, payroll = load()
    existing = json.loads(OUT.read_text())
    stored = existing["hazard"]["models"]["F"]["M2"]["terms"]
    failures = []

    # refit M2 in F
    f = samples(build_pp(windows, odds, payroll))["F"]
    res, notes = fit_logit(f.assign(const=1.0), COLS, cluster=True)
    if res is None or notes:
        sys.exit(f"refit failed: {notes}")
    beta = res.params[COLS].to_numpy()
    V = res.cov_params().loc[COLS, COLS].to_numpy()
    for c in COLS:
        for name, new, old in (("coef", res.params[c], stored[c]["coef"]),
                               ("se_cluster", res.bse[c], stored[c]["se_cluster"])):
            if abs(new - old) > TOL:
                failures.append(f"refit {c} {name}: {new} vs results.json {old}")

    # 2026 windows and inputs
    strength = strength_table(windows, odds)
    pay = payroll.set_index(["season", "team_id"])["od_log2_rel"]
    w26 = windows[(windows["season"] == SEASON) & (windows[COLUMN] == 1)]
    if len(w26) != N_WINDOWS:
        sys.exit(f"{len(w26)} windows open in {SEASON}, expected {N_WINDOWS}")
    for league, g in windows[windows["season"] == SEASON].groupby("league"):
        ref = g.loc[g["od_rank"] == REF_RANK, "team_id"]
        if len(ref) != 1 or abs(strength[(SEASON, int(ref.iloc[0]))]) > 1e-12:
            failures.append(f"{SEASON} {league}: 7th-ranked club strength not 0")

    rows = []
    for r in w26.itertuples():
        g = windows[windows["team_id"] == r.team_id]
        spell = [sp for sp in find_spells(dict(zip(g["season"], g[COLUMN])), grace=False)
                 if sp[1] == SEASON]
        start = spell[0][0]
        dur = CAP if start == FIRST else min(SEASON - start + 1, CAP)
        x = np.array([1.0, math.log(dur), 1.0, strength[(SEASON, r.team_id)],
                      pay[(SEASON, r.team_id)]])
        if np.isnan(x).any():
            failures.append(f"{r.team}: missing input")
        eta = x @ beta
        se = math.sqrt(x @ V @ x)
        p, lo, hi = (1 / (1 + math.exp(-v)) for v in (eta, eta - 1.96 * se, eta + 1.96 * se))
        rows.append({"team": r.team, "team_id": int(r.team_id), "league": r.league,
                     "spell_start": int(start), "duration_capped": int(dur),
                     "strength": float(x[3]), "od_log2_rel": float(x[4]),
                     "p_closed": p, "logit": eta, "se_logit_cluster": se,
                     "ci95": [lo, hi]})
    rows.sort(key=lambda d: -d["p_closed"])

    if len(rows) != N_WINDOWS:
        failures.append(f"{len(rows)} rows")
    for d in rows:
        if not 0 < d["p_closed"] < 1:
            failures.append(f"{d['team']}: p = {d['p_closed']}")
    if failures:
        print(f"{len(failures)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in failures:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    existing[KEY] = {
        "definition": ("P(window_top6 window open on 2026 Opening Day is closed on 2027 Opening "
                       "Day), M2 in sample F as estimated (hazard.models.F.M2), 2026 Opening Day "
                       "inputs, era12 = 1. ci95: Wald interval on the logit scale with the "
                       "club-clustered covariance, both ends transformed. Text: docs/forecasts-2027.md."),
        "covariance_cluster": {"terms": COLS, "matrix": V.tolist()},
        "expected_closed": sum(d["p_closed"] for d in rows),
        "clubs": rows,
    }
    with open(OUT, "w") as fh:
        json.dump(existing, fh, indent=2, default=lambda o: o.item() if hasattr(o, "item") else o)
        fh.write("\n")

    print("All checks passed.\n")
    print("| Club | League | Spell start | Duration (capped) | Strength | od_log2_rel | "
          "P(closed) | 95% interval |")
    print("|---|---|---:|---:|---:|---:|---:|---|")
    for d in rows:
        lo, hi = d["ci95"]
        print(f"| {d['team']} | {d['league']} | {d['spell_start']} | {d['duration_capped']} | "
              f"{d['strength']:+.1f} | {d['od_log2_rel']:+.3f} | {d['p_closed']:.2f} | "
              f"{lo:.2f}–{hi:.2f} |")
    print(f"\nExpected number of closed windows: {existing[KEY]['expected_closed']:.1f}")


if __name__ == "__main__":
    main()
