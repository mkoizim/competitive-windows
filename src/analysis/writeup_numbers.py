"""Numbers the Post 1 abstract will quote (docs/decisions.md, "Numbers the abstract quotes; t-based
intervals in prose", 2026-11-11). Arithmetic on stored values; no new model.

1. t_intervals: or_ci95_t = exp(coef +/- t_{G-1, .975} x se_cluster) for every term of M2 and M2b
   in hazard.models.{F,L,H} and of M2 in every hazard_robustness.variants.*, with G = the stored
   n_clusters. Stored under t_intervals.<source>.<model>.<term>, where <source> is the JSON path
   of the stored model's parent ("hazard.models.F", "hazard_robustness.variants.berth", ...).
2. counts_nine_definitions: across hazard_robustness.order, from M2 (p_t as stored there).
3. long_windows: spells of length >= 4, their club-seasons and share of in-window club-seasons.
   Fixed line from variants.top6; berth-relative spells computed from windows.csv window_berth
   with spells.find_spells (strict consecutive, 2014-2026).
4. contention_rates_2014_2025: window_top6, window_berth (windows.csv) and Jordan-contending
   (jordan_comparison.club_seasons.contending) over 360 club-seasons.

Reads results/results.json and data/processed/windows.csv. Writes results.json's
"writeup_numbers" key; every other key is confirmed unchanged byte for byte and by SHA-256.
Nothing is written if any check fails. --dry-run prints only.

Needs the repo's .venv. Run from the repo root: .venv/bin/python src/analysis/writeup_numbers.py
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hazard as hz  # noqa: E402
from realized_refit import p_t, t_interval, write_key  # noqa: E402
from spells import SEASONS, find_spells  # noqa: E402

ROOT = hz.ROOT
OUT = hz.OUT
KEY = "writeup_numbers"
LONG = 4
FIRST, LAST = 2014, 2025
EXPECT_FIXED_LONG = (13, 90, 156)
P_TOL = 1e-12


def t_entry(t, g):
    ci, tc = t_interval(t["coef"], t["se_cluster"], g)
    return {"coef": t["coef"], "se_cluster": t["se_cluster"], "odds_ratio": t["odds_ratio"],
            "n_clusters": g, "t_df": g - 1, "t_crit": tc, "p_t": p_t(t["z"], g),
            "or_ci95_t": ci}


def t_intervals(r):
    out = {}
    for s in hz.SAMPLES:
        src = f"hazard.models.{s}"
        out[src] = {}
        for m in ("M2", "M2b"):
            model = r["hazard"]["models"][s][m]
            out[src][m] = {c: t_entry(t, model["n_clusters"]) for c, t in model["terms"].items()}
    for v in r["hazard_robustness"]["order"]:
        model = r["hazard_robustness"]["variants"][v]["M2"]
        out[f"hazard_robustness.variants.{v}"] = {
            "M2": {c: t_entry(t, model["n_clusters"]) for c, t in model["terms"].items()}}
    return out


def counts(r, ti):
    order = r["hazard_robustness"]["order"]
    m2 = {v: r["hazard_robustness"]["variants"][v]["M2"]["terms"] for v in order}
    tci = {v: ti[f"hazard_robustness.variants.{v}"]["M2"] for v in order}

    def lst(cond):
        return {"n": sum(cond(v) for v in order), "definitions": [v for v in order if cond(v)]}

    excl = lambda v, c: tci[v][c]["or_ci95_t"][0] > 1 or tci[v][c]["or_ci95_t"][1] < 1  # noqa
    return {
        "definitions": order,
        "p_t_source": "hazard_robustness.variants.<definition>.M2.terms.<term>.p_t",
        "strength": {
            "or_lt_1": lst(lambda v: m2[v]["strength"]["odds_ratio"] < 1),
            "p_t_lt_05": lst(lambda v: m2[v]["strength"]["p_t"] < 0.05),
            "t_interval_excludes_1": lst(lambda v: excl(v, "strength")),
        },
        "ln_dur": {
            "or_gt_1": lst(lambda v: m2[v]["ln_dur"]["odds_ratio"] > 1),
            "p_t_lt_05_and_or_gt_1": lst(lambda v: m2[v]["ln_dur"]["p_t"] < 0.05
                                         and m2[v]["ln_dur"]["odds_ratio"] > 1),
            "p_t_lt_05_and_or_lt_1": lst(lambda v: m2[v]["ln_dur"]["p_t"] < 0.05
                                         and m2[v]["ln_dur"]["odds_ratio"] < 1),
        },
    }


def berth_spells(windows):
    current = windows[windows["season"] == SEASONS[-1]].set_index("team_id")["team"]
    out = []
    for team_id, g in windows.groupby("team_id"):
        flags = dict(zip(g["season"], g["window_berth"]))
        for first, last in find_spells(flags, grace=False):
            out.append({"team": current[team_id], "first": first, "last": last,
                        "length": last - first + 1})
    return out


def long_summary(lengths, in_window):
    long_ = [n for n in lengths if n >= LONG]
    return {"spells_ge_4": len(long_), "club_seasons_ge_4": sum(long_),
            "in_window_club_seasons": in_window, "share": sum(long_) / in_window}


def main():
    dry_run = "--dry-run" in sys.argv
    r = json.loads(OUT.read_text())
    windows = pd.read_csv(hz.WINDOWS)
    fails = []

    ti = t_intervals(r)
    # p_t recomputed here must equal the stored p_t wherever one is stored
    max_p = 0.0
    for v in r["hazard_robustness"]["order"]:
        for c, t in r["hazard_robustness"]["variants"][v]["M2"]["terms"].items():
            max_p = max(max_p, abs(ti[f"hazard_robustness.variants.{v}"]["M2"][c]["p_t"]
                                   - t["p_t"]))
    for s in hz.SAMPLES:
        for m in ("M2", "M2b"):
            for c, t in r["hazard_inference"]["t_correction"][s][m]["terms"].items():
                max_p = max(max_p, abs(ti[f"hazard.models.{s}"][m][c]["p_t"] - t["p_t"]))
    if max_p > P_TOL:
        fails.append(f"(p_t) recomputed p_t differs from stored by {max_p:.3g}")

    # check 6: baseline fixed-line strength, t interval wider than the stored normal one
    for src in ("hazard.models.F", "hazard_robustness.variants.top6"):
        stored = (r["hazard"]["models"]["F"]["M2"] if src.startswith("hazard.models")
                  else r["hazard_robustness"]["variants"]["top6"]["M2"])["terms"]["strength"]
        tci = ti[src]["M2"]["strength"]["or_ci95_t"]
        if not (tci[0] < stored["or_ci95"][0] and tci[1] > stored["or_ci95"][1]):
            fails.append(f"(6) {src} strength: t interval {tci} not wider than {stored['or_ci95']}")

    cn = counts(r, ti)

    # long windows
    top6 = r["variants"]["top6"]
    fixed_long = long_summary([sp["length"] for sp in top6["spells"]],
                              top6["in_window_club_seasons"])
    if (fixed_long["spells_ge_4"], fixed_long["club_seasons_ge_4"],
            fixed_long["in_window_club_seasons"]) != EXPECT_FIXED_LONG:
        fails.append(f"(7) fixed long windows {fixed_long}, expected {EXPECT_FIXED_LONG}")
    dist = top6["length_distribution"]
    from_dist = (sum(v for k, v in dist.items() if int(k) >= LONG),
                 sum(int(k) * v for k, v in dist.items() if int(k) >= LONG))
    if from_dist != (fixed_long["spells_ge_4"], fixed_long["club_seasons_ge_4"]):
        fails.append(f"(7) fixed long windows from length_distribution {from_dist}")
    bsp = berth_spells(windows)
    b_in = int(windows.loc[windows["season"].between(SEASONS[0], SEASONS[-1]),
                           "window_berth"].sum())
    if sum(sp["length"] for sp in bsp) != b_in:
        fails.append(f"(7) berth spell lengths sum to {sum(sp['length'] for sp in bsp)}, "
                     f"in-window {b_in}")
    berth_long = long_summary([sp["length"] for sp in bsp], b_in)
    berth_long["n_spells"] = len(bsp)
    berth_long["spell_lengths_sum"] = sum(sp["length"] for sp in bsp)
    fixed_long["n_spells"] = top6["n_spells"]

    # contention rates
    w = windows[windows["season"].between(FIRST, LAST)]
    jc = r["jordan_comparison"]["club_seasons"]
    if len(w) != 360 or jc["total"] != 360:
        fails.append(f"(rates) {len(w)} windows.csv club-seasons, {jc['total']} Jordan, "
                     "expected 360")
    rates = {"seasons": [FIRST, LAST], "club_seasons": len(w),
             "fixed_top6": {"n": int(w["window_top6"].sum()),
                            "rate": float(w["window_top6"].mean())},
             "berth_relative": {"n": int(w["window_berth"].sum()),
                                "rate": float(w["window_berth"].mean())},
             "jordan_contending": {"n": jc["contending"], "rate": jc["contending"] / jc["total"],
                                   "source": "jordan_comparison.club_seasons.contending"}}

    if fails:
        print(f"{len(fails)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in fails:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    res = {
        "definition": (
            "Arithmetic on stored values. t_intervals.<source>.<model>.<term>: or_ci95_t = "
            "exp(coef +/- t_{G-1,0.975} x se_cluster), G = stored n_clusters; p_t = 2 x t_{G-1} "
            "tail at the stored z. <source> is the JSON path of the stored models. "
            "counts_nine_definitions: M2 across hazard_robustness.order, p_t as stored. "
            "long_windows: spells of length >= 4, their club-seasons (sum of lengths) and share "
            "of in-window club-seasons, 2014-2026; fixed from variants.top6, berth-relative from "
            "windows.csv window_berth (strict consecutive spells, spells.find_spells). "
            "contention_rates_2014_2025: share of the 360 club-seasons."),
        "t_intervals": ti,
        "counts_nine_definitions": cn,
        "long_windows": {"min_length": LONG, "fixed_top6": fixed_long,
                         "berth_relative": berth_long},
        "contention_rates_2014_2025": rates,
        "checks": {"passed": True, "max_abs_p_t_diff_vs_stored": max_p},
    }

    print("All checks passed.")
    print(f"  max |p_t - stored p_t| = {max_p:.3g}")
    print("\n== t intervals, M2 strength and ln_dur")
    for src, models in ti.items():
        for m, terms in models.items():
            print(f"  {src} {m}: " + "; ".join(
                f"{c} OR {terms[c]['odds_ratio']:.3f} [{terms[c]['or_ci95_t'][0]:.3f}, "
                f"{terms[c]['or_ci95_t'][1]:.3f}] p_t {terms[c]['p_t']:.4f}"
                for c in ("strength", "ln_dur", "dur1") if c in terms))
    print("\n== Counts across nine definitions")
    for term in ("strength", "ln_dur"):
        for k, v in cn[term].items():
            print(f"  {term} {k}: {v['n']} {v['definitions']}")
    print("\n== Long windows:", json.dumps(res["long_windows"]))
    print("\n== Contention rates:", json.dumps(rates))
    write_key(KEY, res, dry_run)


if __name__ == "__main__":
    main()
