"""Realized-outcome refit of M2 (Post 1).

Per docs/decisions.md, "Realized-outcome refit (Post 1): specification" (2026-11-11). M2's rows and
covariates are unchanged; only the event changes, to an outcome realized on the field in season n+1.

Rows (sample F, left_censored = 0):
- fixed line:          data/processed/hazard_pp.csv
- berth-relative line: data/processed/hazard_robustness_pp.csv, variant berth
Design: hazard.samples(...)["F"], M2 = const + ln(duration capped at 4) + era12 + strength +
od_log2_rel, fitted by hazard.covariate_model (hazard.fit_logit, clustered by team_id).

Events for season n+1, from the end_of_season snapshot of data/processed/odds.csv:
- event_jordan = 1 if the club was not contending in n+1 by Jordan's rule, jordan.contending
  unchanged, with jordan.LAST set to 2026 here (jordan.py itself is not edited);
- event_post   = 1 if postseason_odds < 0.999 at n+1's end-of-season snapshot.

Four fits: fixed_jordan (primary, fixed line), berth_post (primary, berth-relative line),
fixed_post and berth_jordan. Every term carries the odds ratio, the clustered SE, p_normal, p_t
(t with G - 1 df, G = clubs) and or_ci95_t = exp(coef +/- t_{G-1, .975} x SE).
cushion_passes (primary fits) = strength OR < 1 and upper or_ci95_t < 1.

Writes results.json's "realized_outcome_refit" key; every other key is confirmed unchanged byte for
byte (and by SHA-256 per key). Nothing is written if any check fails. --dry-run prints only.

Needs the repo's .venv. Run from the repo root: .venv/bin/python src/analysis/realized_refit.py
"""

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hazard as hz  # noqa: E402
import jordan  # noqa: E402
from jordan import dump, merge_key  # noqa: E402

ROOT = hz.ROOT
OUT = hz.OUT
KEY = "realized_outcome_refit"
ROBUST_PP = ROOT / "data" / "processed" / "hazard_robustness_pp.csv"

jordan.LAST = 2026   # extend Jordan's contending seasons through 2026; logic unchanged

M2_COLS = ["const", "ln_dur", "era12", "strength", "od_log2_rel"]
POSTSEASON = 0.999
TOL = 1e-10
EXPECT_ROWS_CLUBS = {"fixed": (102, 22), "berth": (97, 23)}
EXPECT_BERTHS = {**{s: 5 for s in (2014, 2015, 2016, 2017, 2018, 2019, 2021)}, 2020: 8,
                 **{s: 6 for s in range(2022, 2027)}}
LINES = {"fixed": "Fixed top 6 (hazard_pp.csv, left_censored = 0)",
         "berth": "Berth-relative (hazard_robustness_pp.csv, variant berth, left_censored = 0)"}
OUTCOMES = {"jordan": "event_jordan", "post": "event_post"}
FITS = {"fixed_jordan": ("fixed", "jordan", "primary, fixed line"),
        "berth_post": ("berth", "post", "primary, berth-relative line"),
        "fixed_post": ("fixed", "post", "reported alongside"),
        "berth_jordan": ("berth", "jordan", "reported alongside")}
PRIMARY = ["fixed_jordan", "berth_post"]


# ---------------------------------------------------------------- shared helpers

def t_interval(coef, se, g):
    """95% odds-ratio interval with the t(G - 1) critical value."""
    tc = float(stats.t.ppf(0.975, g - 1))
    return [math.exp(coef - tc * se), math.exp(coef + tc * se)], tc


def p_t(z, g):
    return float(2 * stats.t.sf(abs(z), g - 1))


def with_t(model):
    """hazard.covariate_model output -> terms with p_normal, p_t, or_ci95_t (G = n_clusters)."""
    g = model["n_clusters"]
    out = {k: v for k, v in model.items() if k != "terms"}
    out["t_df"] = g - 1
    out["terms"] = {}
    for c, t in model["terms"].items():
        ci, tc = t_interval(t["coef"], t["se_cluster"], g)
        out["terms"][c] = {"coef": t["coef"], "se_cluster": t["se_cluster"], "z": t["z"],
                           "odds_ratio": t["odds_ratio"], "p_normal": t["p"],
                           "p_t": p_t(t["z"], g), "or_ci95": t["or_ci95"],
                           "or_ci95_t": ci, "t_crit": tc}
    return out


def key_hashes(obj):
    return {k: hashlib.sha256(dump(v).encode()).hexdigest() for k, v in obj.items()}


def write_key(key, value, dry_run):
    """merge_key (jordan.py) plus a SHA-256 comparison of every other top-level key."""
    before = json.loads(OUT.read_text())
    h0 = key_hashes(before)
    text = merge_key(key, value)
    after = json.loads(text)
    h1 = key_hashes({k: v for k, v in after.items() if k != key})
    if h0 != h1 or set(after) != set(before) | {key}:
        sys.exit("SHA-256 of an existing key would change; nothing written")
    if dry_run:
        print(f"\n(dry run: {OUT.relative_to(ROOT)} not written)")
        return
    OUT.write_text(text)
    h2 = key_hashes({k: v for k, v in json.loads(OUT.read_text()).items() if k != key})
    if h2 != h0:
        sys.exit("WARNING: existing keys changed after write")
    print(f"\nWrote {OUT.relative_to(ROOT)} ({key}); SHA-256 of all {len(h0)} other keys "
          "unchanged.")


def lines():
    """{'fixed': F rows, 'berth': F rows} with hazard.samples' derived columns."""
    fixed = hz.samples(pd.read_csv(hz.PP_OUT))["F"]
    rob = pd.read_csv(ROBUST_PP)
    berth = hz.samples(rob[rob["variant"] == "berth"].drop(columns="variant")
                       .reset_index(drop=True))["F"]
    return {"fixed": fixed, "berth": berth}


def m2(d, event=None):
    dd = d if event is None else d.assign(event=d[event])
    return hz.covariate_model(dd, "ln_dur")


# ---------------------------------------------------------------- outcomes

def outcomes(odds):
    """(club-season frame 2014-2026 with contending and made_post, ties for first)."""
    e, ties = jordan.contending(odds)
    e["made_post"] = e["postseason_odds"] >= POSTSEASON
    return e, ties


def attach(d, e):
    o = e.set_index(["season", "team_id"])[["contending", "made_post"]]
    nxt = d.assign(season_next=d["season"] + 1).join(o, on=["season_next", "team_id"])
    d = d.copy()
    d["missing_next"] = nxt["contending"].isna().to_numpy()
    d["event_jordan"] = (~nxt["contending"].astype("boolean")).astype("Int64").to_numpy()
    d["event_post"] = (~nxt["made_post"].astype("boolean")).astype("Int64").to_numpy()
    return d


def bands(d, event):
    band = hz.strength_band(d["strength"])
    out = {}
    for b, label in hz.STRENGTH_BANDS:
        g = d.loc[band == b, event]
        out[b] = {"label": label, "club_seasons": len(g), "events": int(g.sum()),
                  "share": float(g.mean()) if len(g) else None}
    return out


def crosstab(d, event):
    cells = {}
    for o in (1, 0):
        for n in (1, 0):
            cells[f"original_{o}__new_{n}"] = int(((d["event"] == o) & (d[event] == n)).sum())
    return cells


# ---------------------------------------------------------------- checks

def run_checks(L, existing, e, ties):
    fails, diffs = [], {}
    stored = {"fixed": existing["hazard"]["models"]["F"]["M2"],
              "berth": existing["hazard_robustness"]["variants"]["berth"]["M2"]}
    for line, d in L.items():
        # (1) original event reproduces stored M2
        new = m2(d)
        mx = 0.0
        for c in M2_COLS:
            for f in ("coef", "se_cluster"):
                diff = abs(new["terms"][c][f] - stored[line]["terms"][c][f])
                mx = max(mx, diff)
        diffs[line] = mx
        if not mx < TOL:
            fails.append(f"(1) {line}: max |coef/SE diff| vs stored M2 = {mx:.3g}")
        # (2) rows and clubs
        n, g = EXPECT_ROWS_CLUBS[line]
        if (len(d), d["team_id"].nunique()) != (n, g):
            fails.append(f"(2) {line}: {len(d)} rows / {d['team_id'].nunique()} clubs, "
                         f"expected {n} / {g}")
        # (5) new events defined for every row
        if d["missing_next"].any() or d[["event_jordan", "event_post"]].isna().any().any():
            fails.append(f"(5) {line}: {int(d['missing_next'].sum())} rows with no n+1 season")
    # tie rule: every tie for first must be listed; none in 2026
    for season, league, division, tied, title in ties:
        if title is None:
            fails.append(f"(tie) {season} {league} {division}: tie for first not in TITLE_TIES "
                         f"({', '.join(tied)})")
        if season == 2026:
            fails.append(f"(tie) 2026 {league} {division}: tie for first ({', '.join(tied)})")
    # (3) Jordan 2014-2025 reproduces jordan_comparison.club_seasons
    ref = existing["jordan_comparison"]["club_seasons"]
    sub = e[e["season"] <= 2025]
    crit = {"division_winner": "c_division", "postseason_non_division_winner": "c_postseason",
            "second_or_third_within_gb": "c_close", "wins_87_or_wpct_537_2020": "c_wins"}
    got = {"total": len(sub), "contending": int(sub["contending"].sum()),
           "by_criterion": {k: int(sub[c].sum()) for k, c in crit.items()}}
    if got != ref or got["contending"] != 147:
        fails.append(f"(3) Jordan 2014-2025: {got}, stored {ref}")
    # (3b) same with LAST = 2025 (the stored run's constant)
    jordan.LAST = 2025
    e25, _ = jordan.contending(pd.read_csv(hz.ODDS))
    jordan.LAST = 2026
    cols = ["season", "team_id", "contending", "c_division", "c_postseason", "c_close", "c_wins"]
    if not e25[cols].reset_index(drop=True).equals(sub[cols].reset_index(drop=True)):
        fails.append("(3) contending with LAST = 2025 differs from the 2014-2025 subset")
    # (4) made-postseason per league-season = berths
    post_counts = {}
    for (season, league), g in e.groupby(["season", "league"]):
        k = int(g["made_post"].sum())
        post_counts[f"{season} {league}"] = k
        if k != EXPECT_BERTHS[season]:
            fails.append(f"(4) {season} {league}: {k} made the postseason, expected "
                         f"{EXPECT_BERTHS[season]}")
    if sorted(e["season"].unique()) != list(range(2014, 2027)):
        fails.append(f"(4) seasons {sorted(e['season'].unique())}")
    return fails, diffs, got


# ---------------------------------------------------------------- main

def main():
    dry_run = "--dry-run" in sys.argv
    existing = json.loads(OUT.read_text())
    e, ties = outcomes(pd.read_csv(hz.ODDS))
    L = {line: attach(d, e) for line, d in lines().items()}

    fails, diffs, jordan_check = run_checks(L, existing, e, ties)
    if fails:
        print(f"{len(fails)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in fails:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    fits = {}
    for name, (line, outcome, role) in FITS.items():
        d = L[line].assign(**{OUTCOMES[outcome]: L[line][OUTCOMES[outcome]].astype(int)})
        res = with_t(m2(d, OUTCOMES[outcome]))
        res.update({"line": line, "outcome": OUTCOMES[outcome], "role": role})
        fits[name] = res
    passes = {}
    for name in PRIMARY:
        s = fits[name]["terms"]["strength"]
        passes[name] = {"strength_or": s["odds_ratio"], "or_ci95_t": s["or_ci95_t"],
                        "passes": bool(s["odds_ratio"] < 1 and s["or_ci95_t"][1] < 1)}

    res = {
        "definition": (
            "M2 (const + ln(duration capped at 4) + era12 + strength + od_log2_rel), sample F rows "
            "and covariates unchanged, refitted with outcomes realized in season n+1 "
            "(end_of_season snapshot, odds.csv). event_jordan = 1 if not contending in n+1 by "
            "Jordan's rule (jordan.contending, LAST set to 2026; ties for first broken by the "
            "listed titles, none in 2026); event_post = 1 if postseason_odds < 0.999 at n+1's "
            "end-of-season snapshot. Logit, SEs clustered by team_id (hazard.fit_logit). p_normal: "
            "normal reference; p_t and or_ci95_t: t with G - 1 df, G = clubs in the sample; "
            "or_ci95_t = exp(coef +/- t_{G-1,0.975} x SE). or_ci95 is the stored-style normal "
            "interval. cushion_passes = strength OR < 1 and upper or_ci95_t < 1. Rows with "
            "n + 1 = 2020 keep era12 = 0."),
        "lines": LINES,
        "fits": fits,
        "cushion_passes": passes,
        "bands": {
            "definition": ("Club-seasons by Opening Day strength in season n (hazard.strength_band:"
                           " <= 2, > 2 to 5, > 5 to 8, > 8 wins); events = the new event; share = "
                           "events / club-seasons."),
            **{name: bands(L[line], OUTCOMES[outcome])
               for name, (line, outcome, _) in FITS.items()}},
        "rows_next_season_2020": {line: int((d["season"] + 1 == 2020).sum())
                                  for line, d in L.items()},
        "crosstabs": {
            "definition": ("original = event in sample F (out of the window at n+1's Opening Day);"
                           " new = event_jordan or event_post. Cell original_a__new_b counts rows "
                           "with original = a and new = b."),
            **{line: {OUTCOMES[o]: crosstab(d, OUTCOMES[o]) for o in OUTCOMES}
               for line, d in L.items()}},
        "events_total": {line: {"original": int(d["event"].sum()),
                                "event_jordan": int(d["event_jordan"].sum()),
                                "event_post": int(d["event_post"].sum())}
                         for line, d in L.items()},
        "checks": {"passed": True,
                   "max_abs_diff_vs_stored_M2": diffs,
                   "jordan_2014_2025": jordan_check,
                   "ties_for_first_2014_2026": [[int(s), lg, dv, t] for s, lg, dv, t, _ in ties]},
    }

    print("All checks passed.")
    print(f"  max |coef/SE diff| vs stored M2: {diffs}")
    print(f"  ties for first: {res['checks']['ties_for_first_2014_2026']}")
    for name, f in fits.items():
        print(f"\n== {name} ({f['role']}): {f['n_rows']} rows, {f['n_events']} events, "
              f"G = {f['n_clusters']}, converged {f['converged']}, notes {f['notes']}")
        print(f"  {'term':12}{'OR':>8}{'SE':>8}{'p_norm':>9}{'p_t':>9}   or_ci95_t")
        for c, t in f["terms"].items():
            print(f"  {c:12}{t['odds_ratio']:>8.3f}{t['se_cluster']:>8.3f}{t['p_normal']:>9.4f}"
                  f"{t['p_t']:>9.4f}   [{t['or_ci95_t'][0]:.3f}, {t['or_ci95_t'][1]:.3f}]")
    print("\n== cushion_passes:", {k: v["passes"] for k, v in passes.items()})
    print("\n== Bands")
    for name in FITS:
        print(f"  {name}: " + "; ".join(f"{v['label']} {v['events']}/{v['club_seasons']} "
                                        f"({v['share']:.3f})" for v in res["bands"][name].values()
                                        if isinstance(v, dict)))
    print("\n== Rows with n+1 = 2020:", res["rows_next_season_2020"])
    print("\n== Cross-tabs")
    for line in L:
        for o in OUTCOMES.values():
            print(f"  {line} {o}: {res['crosstabs'][line][o]}")
    print("\n== Events:", res["events_total"])
    write_key(KEY, res, dry_run)


if __name__ == "__main__":
    main()
