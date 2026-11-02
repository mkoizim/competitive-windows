"""Discrete-time hazard of window exit (Post 1) from window_top6 spells.

Builds data/processed/hazard_pp.csv (one row per spell per season n, 2014-2025) and, from it,
three samples per docs/decisions.md ("Left-censored spells", 2026-10-26):

- F (primary)  left-censored spells (open in 2014) dropped; duration = duration_obs
- L            all spells; left-censored spells enter in 2014 at duration 1
- H            all spells; left-censored spells enter in 2014 at the top bin (4+) and stay there.
               At exact durations they enter at 4 and count up (duration_obs + 3).

Reports life tables at exact durations, life tables by entry strength (F only), discrete-time
logits M1 (bins 1, 2, 3, 4+), M2 (ln duration capped at 4 + era12 + strength + od_log2_rel) and
M2b (M2 with a duration-1 indicator in place of ln duration), the bins vs. log likelihood-ratio
test, persistent contenders, exit by deadline status, and closing by current-season strength
band (F only). M2/M2b standard errors are clustered by team_id (statsmodels' default small-sample
correction, normal reference distribution).

build_pp, strength_table and m1 also serve hazard_robustness.py (other thresholds, the grace
rule, zero-closing bins); their defaults give the baseline.

Only the "hazard" key of results.json is written; other keys are kept. Nothing is written if
any check fails.

Needs numpy, pandas, statsmodels and matplotlib (the repo's .venv). Run from the repo root:
.venv/bin/python src/analysis/hazard.py
"""

import csv
import json
import math
import sys
import warnings
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402
from scipy import stats  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spells import SEASONS, find_spells  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
WINDOWS = ROOT / "data" / "processed" / "windows.csv"
ODDS = ROOT / "data" / "processed" / "odds.csv"
PAYROLL = ROOT / "data" / "processed" / "payroll.csv"
PP_OUT = ROOT / "data" / "processed" / "hazard_pp.csv"
OUT = ROOT / "results" / "results.json"
FIG_DIR = ROOT / "results" / "figures"

COLUMN = "window_top6"
FIRST, LAST_PP = 2014, 2025  # 2026 rows excluded: 2027 not observed
ERA12_FROM = 2022            # deciding Opening Day n+1 >= 2022
K = 6
REF_RANK = 7
CAP = 4
BINS = ["1", "2", "3", "4+"]
SMALL_AT_RISK = 10
SAMPLES = ["F", "L", "H"]

PP_COLUMNS = ["team_id", "team", "league", "spell_id", "spell_start", "season", "left_censored",
              "duration_obs", "event", "era12", "strength", "od_log2_rel", "pd_above"]

# Checks fixed in the task brief
EXPECT_ROWS_EVENTS = {"F": (102, 30), "L": (144, 41), "H": (144, 41)}
EXPECT_F_BINS = {"1": (38, 13), "2": (21, 5), "3": (14, 5), "4+": (29, 7)}
EXPECT_DEADLINE_L = {"above_no_exit": 82, "above_exit": 16, "below_no_exit": 21, "below_exit": 25}
EXPECT_F_STRENGTH_BANDS = {"le_2": (39, 19), "gt_2_le_5": (25, 7), "gt_5_le_8": (15, 3),
                           "gt_8": (23, 1)}
DEADLINE_PATTERNS = {"above_no_exit": "Held, carried forward",
                     "above_exit": "Held, not carried forward",
                     "below_no_exit": "Gap year",
                     "below_exit": "Fizzled"}

# Reference categorical palette, slots 1-3 (dataviz skill), light surface
COLORS = {"F": "#2a78d6", "L": "#eb6834", "H": "#1baf7a"}
SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"


def bin_of(d):
    return str(d) if d < CAP else f"{CAP}+"


# ---------------------------------------------------------------- person-period file

def load():
    windows = pd.read_csv(WINDOWS)
    odds = pd.read_csv(ODDS)
    odds = odds[odds["snapshot"] == "opening_day"].copy()
    payroll = pd.read_csv(PAYROLL)
    return windows, odds, payroll


def at_season(x, season):
    """x is an int or a {season: int} mapping (the berth-relative threshold varies by season)."""
    return x[season] if isinstance(x, dict) else x


def strength_table(windows, odds, ref_rank=REF_RANK):
    """{(season, team_id): wins per 162 above the league's od_rank-ref_rank club}."""
    od = odds.set_index(["season", "team_id"])
    wpct = od["proj_w"] / (od["proj_w"] + od["proj_l"])
    out = {}
    for (season, league), g in windows.groupby(["season", "league"]):
        ref = g.loc[g["od_rank"] == at_season(ref_rank, season), "team_id"]
        if len(ref) != 1:
            continue  # reported by check 6
        ref_wpct = wpct[(season, int(ref.iloc[0]))]
        for t in g["team_id"]:
            out[(season, t)] = (wpct[(season, t)] - ref_wpct) * 162
    return out


def build_pp(windows, odds, payroll, column=COLUMN, k=K, grace=False):
    """k is an int or a {season: int} mapping; strength is measured against the (k+1)th club.

    Strict (grace=False): a window closes at the first Opening Day out. Grace: it closes after
    two straight Opening Days out. Dip seasons are not rows but count toward duration_obs, the
    event is recorded in the last in-window season, rows run to the last season whose outcome
    is observed (LAST_PP strict, one earlier under grace), and spells starting within the gap
    of 2014 are left-censored (2014 strict; 2014-2015 grace).
    """
    gap = 2 if grace else 1
    last_pp = LAST_PP - (gap - 1)
    ref_rank = {s: kk + 1 for s, kk in k.items()} if isinstance(k, dict) else k + 1
    current = windows[windows["season"] == SEASONS[-1]].set_index("team_id")["team"]
    w = windows.set_index(["season", "team_id"])
    strength = strength_table(windows, odds, ref_rank)
    pay = payroll.set_index(["season", "team_id"])["od_log2_rel"]
    rows = []
    for team_id, g in windows.groupby("team_id"):
        flags = dict(zip(g["season"], g[column]))
        team = current[team_id]
        for first, last in find_spells(flags, grace=grace):
            for n in range(first, min(last, last_pp) + 1):
                if not flags[n]:
                    continue  # dip season (grace only)
                r = w.loc[(n, team_id)]
                rows.append({
                    "team_id": team_id,
                    "team": team,
                    "league": r["league"],
                    "spell_id": f"{team}-{first}",
                    "spell_start": first,
                    "season": n,
                    "left_censored": int(first < FIRST + gap),
                    "duration_obs": n - first + 1,
                    "event": int(n == last and n + gap <= SEASONS[-1]),
                    "era12": int(n + 1 >= ERA12_FROM),
                    "strength": strength.get((n, team_id), np.nan),
                    "od_log2_rel": pay.get((n, team_id), np.nan),
                    "pd_above": int(r["pd_rank"] <= at_season(k, n)),
                })
    return pd.DataFrame(rows, columns=PP_COLUMNS).sort_values(["team", "season"],
                                                               ignore_index=True)


def samples(pp):
    lc = pp["left_censored"] == 1
    f = pp[~lc].copy()
    f["duration"] = f["duration_obs"]
    f["top_bin_entry"] = 0
    l_ = pp.copy()
    l_["duration"] = l_["duration_obs"]
    l_["top_bin_entry"] = 0
    h = pp.copy()
    h["duration"] = np.where(lc, h["duration_obs"] + CAP - 1, h["duration_obs"])
    h["top_bin_entry"] = lc.astype(int)
    out = {}
    for name, d in zip(SAMPLES, (f, l_, h)):
        d = d.reset_index(drop=True)
        d["bin"] = d["duration"].map(bin_of)
        d["ln_dur"] = np.log(np.minimum(d["duration"], CAP))
        d["dur1"] = (d["duration"] == 1).astype(int)
        out[name] = d
    return out


# ---------------------------------------------------------------- checks

def run_checks(pp, smp, windows, results_json):
    failures = []
    # (1) rows and events
    for name, (n_rows, n_ev) in EXPECT_ROWS_EVENTS.items():
        d = smp[name]
        if (len(d), int(d["event"].sum())) != (n_rows, n_ev):
            failures.append(f"(1) {name}: {len(d)} rows / {int(d['event'].sum())} events, "
                            f"expected {n_rows} / {n_ev}")
    # (2) F binned rows/events
    f = smp["F"]
    for b, (n_rows, n_ev) in EXPECT_F_BINS.items():
        g = f[f["bin"] == b]
        if (len(g), int(g["event"].sum())) != (n_rows, n_ev):
            failures.append(f"(2) F bin {b}: {len(g)} rows / {int(g['event'].sum())} events, "
                            f"expected {n_rows} / {n_ev}")
    # (3) LAD
    for name in ("L", "H"):
        g = smp[name][smp[name]["team"] == "LAD"]
        if len(g) != 12 or g["event"].sum() != 0:
            failures.append(f"(3) {name}: LAD has {len(g)} rows, {int(g['event'].sum())} events")
    if (smp["F"]["team"] == "LAD").any():
        failures.append("(3) F: LAD present")
    # (4) no missing covariates
    for c in ("strength", "od_log2_rel", "pd_above"):
        n_missing = int(pp[c].isna().sum())
        if n_missing:
            failures.append(f"(4) {n_missing} rows missing {c}")
    # (5) consecutive seasons, at most one event, in the last row
    for sid, g in pp.groupby("spell_id"):
        s = g.sort_values("season")
        if list(s["season"]) != list(range(s["season"].min(), s["season"].max() + 1)):
            failures.append(f"(5) {sid}: seasons not consecutive")
        if s["event"].sum() > 1 or (s["event"].sum() == 1 and s["event"].iloc[-1] != 1):
            failures.append(f"(5) {sid}: event not confined to the last row")
        if list(s["duration_obs"]) != list(range(1, len(s) + 1)):
            failures.append(f"(5) {sid}: duration_obs not 1..{len(s)}")
    # (6) the 7th-ranked club has strength 0, every league-season
    strength = strength_table(windows, pd.read_csv(ODDS).query("snapshot == 'opening_day'"))
    for (season, league), g in windows.groupby(["season", "league"]):
        ref = g.loc[g["od_rank"] == REF_RANK, "team_id"]
        if len(ref) != 1:
            failures.append(f"(6) {season} {league}: {len(ref)} clubs with od_rank {REF_RANK}")
        elif abs(strength[(season, int(ref.iloc[0]))]) > 1e-12:
            failures.append(f"(6) {season} {league}: 7th-ranked club strength "
                            f"{strength[(season, int(ref.iloc[0]))]}")
    # (7) deadline x event in L matches the window patterns
    cells = deadline_cells(smp["L"])
    patterns = results_json["patterns"]["by_threshold"]["top6"]["counts_2014_2025"]
    for cell, expected in EXPECT_DEADLINE_L.items():
        if cells[cell] != expected:
            failures.append(f"(7) L {cell}: {cells[cell]}, expected {expected}")
        if patterns[DEADLINE_PATTERNS[cell]] != cells[cell]:
            failures.append(f"(7) L {cell}: {cells[cell]}, results.json "
                            f"'{DEADLINE_PATTERNS[cell]}' = {patterns[DEADLINE_PATTERNS[cell]]}")
    # (8) F closing by current-season strength band
    for band, (n_rows, n_ev) in EXPECT_F_STRENGTH_BANDS.items():
        g = f[strength_band(f["strength"]) == band]
        if (len(g), int(g["event"].sum())) != (n_rows, n_ev):
            failures.append(f"(8) F band {band}: {len(g)} rows / {int(g['event'].sum())} events, "
                            f"expected {n_rows} / {n_ev}")
    return failures


# ---------------------------------------------------------------- life tables

def life_table(d):
    """Exact durations: at risk, entered (delayed entry), exits, censored, hazard, survival."""
    last = d.sort_values("season").groupby("spell_id").tail(1)
    first = d.sort_values("season").groupby("spell_id").head(1)
    rows, surv = [], 1.0
    for dur in range(1, int(d["duration"].max()) + 1):
        at_risk = int((d["duration"] == dur).sum())
        exits = int(d.loc[d["duration"] == dur, "event"].sum())
        censored = int(((last["duration"] == dur) & (last["event"] == 0)).sum())
        entered = int(((first["duration"] == dur) & (dur > 1)).sum())
        h = exits / at_risk if at_risk else None
        if h is not None:
            surv *= 1 - h
        rows.append({"duration": dur, "at_risk": at_risk, "entered": entered, "exits": exits,
                     "censored": censored, "hazard": h, "survival": surv if at_risk else None,
                     "small": at_risk < SMALL_AT_RISK})
    return rows


def binned_table(d):
    return {b: {"rows": int((d["bin"] == b).sum()),
                "events": int(d.loc[d["bin"] == b, "event"].sum()),
                "hazard": float(d.loc[d["bin"] == b, "event"].mean())} for b in BINS}


def entry_strength_groups(f):
    first = f.sort_values("season").groupby("spell_id").head(1)
    median = float(first["strength"].median())
    above = set(first.loc[first["strength"] >= median, "spell_id"])
    groups = {"at_or_above_median": f[f["spell_id"].isin(above)],
              "below_median": f[~f["spell_id"].isin(above)]}
    return median, first, groups


# ---------------------------------------------------------------- models

def fit_logit(d, cols, cluster):
    """Logit of event on cols. Returns (result, notes) with convergence/separation notes."""
    X = d[cols].astype(float)
    notes = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            kw = {"cov_type": "cluster", "cov_kwds": {"groups": d["team_id"].to_numpy()}} \
                if cluster else {}
            res = sm.Logit(d["event"].astype(float), X).fit(disp=0, maxiter=200, **kw)
        except Exception as e:  # perfect separation raises in statsmodels
            return None, [f"{type(e).__name__}: {e}"]
    notes += [str(w.message) for w in caught]
    if not res.mle_retvals.get("converged", False):
        notes.append("did not converge")
    p = res.predict(X)
    if (p < 1e-8).any() or (p > 1 - 1e-8).any():
        notes.append("fitted probabilities at 0 or 1 (possible separation)")
    # quasi-separation screen: a binary regressor whose level has no events or no non-events
    for c in cols:
        vals = set(d[c].unique())
        if vals <= {0, 1} and len(vals) == 2:
            for v in (0, 1):
                ev = d.loc[d[c] == v, "event"]
                if ev.sum() in (0, len(ev)):
                    notes.append(f"{c}={v}: {int(ev.sum())} events in {len(ev)} rows "
                                 f"(separation)")
    return res, notes


def clopper_pearson(k, n, level=0.95):
    a = (1 - level) / 2
    lo = 0.0 if k == 0 else float(stats.beta.ppf(a, k, n - k + 1))
    hi = 1.0 if k == n else float(stats.beta.ppf(1 - a, k + 1, n - k))
    return [lo, hi]


def m1(d):
    """A bin with zero closings is not fitted (its ML hazard is 0, on the boundary): it is
    reported as a raw count with an exact interval and flagged. Its rows leave the fit, which
    matches the full-data log-likelihood at that limit (each contributes 0)."""
    zero = [b for b in BINS if d.loc[d["bin"] == b, "event"].sum() == 0]
    fitted = [b for b in BINS if b not in zero]
    X = pd.get_dummies(d["bin"]).reindex(columns=BINS, fill_value=0).astype(float)
    dd = d.assign(**{f"bin_{b}": X[b] for b in BINS})
    dd = dd[dd["bin"].isin(fitted)]
    cols = [f"bin_{b}" for b in fitted]
    out = {"n_rows": len(d), "n_events": int(d["event"].sum()),
           "n_clusters": int(d["team_id"].nunique()), "bins": {}}
    if zero:
        out["zero_closing_bins"] = zero
        out["n_rows_fitted"] = len(dd)
        out["n_clusters_fitted"] = int(dd["team_id"].nunique())
    fits = {}
    for label, cluster in (("model", False), ("cluster", True)):
        res, notes = fit_logit(dd, cols, cluster)
        fits[label] = (res, notes)
    res_m, notes_m = fits["model"]
    res_c, notes_c = fits["cluster"]
    for b in BINS:
        g = d[d["bin"] == b]
        entry = {"rows": len(g), "events": int(g["event"].sum())}
        if b in zero:
            entry["zero_closings"] = True
            entry["hazard_raw"] = 0.0 if len(g) else None
            entry["ci95_exact"] = clopper_pearson(0, len(g)) if len(g) else None
            out["bins"][b] = entry
            continue
        c = f"bin_{b}"
        for label, res in (("model", res_m), ("cluster", res_c)):
            if res is None:
                continue
            beta, se = res.params[c], res.bse[c]
            entry["hazard"] = float(1 / (1 + math.exp(-beta)))
            entry[f"ci95_{label}"] = [float(1 / (1 + math.exp(-(beta - 1.96 * se)))),
                                      float(1 / (1 + math.exp(-(beta + 1.96 * se))))]
        out["bins"][b] = entry
    out["loglik"] = float(res_m.llf) if res_m is not None else None
    out["notes"] = sorted(set(notes_m + notes_c))
    out["ci_note"] = ("Hazard = logistic(bin coefficient), no intercept. ci95_model uses the "
                      "ordinary ML standard error; ci95_cluster clusters by team_id. Both are "
                      "Wald intervals on the logit scale, transformed.")
    if zero:
        out["zero_closing_note"] = (
            f"Bin(s) {', '.join(zero)} had zero closings and were not fitted: hazard_raw = 0 "
            "with an exact (Clopper-Pearson) 95% interval. Their rows were left out of the fit; "
            "loglik equals the full-data log-likelihood at the limit (hazard 0, contribution 0). "
            "Clustered SEs use n_clusters_fitted clubs.")
    return out


def covariate_model(d, dur_col):
    cols = ["const", dur_col, "era12", "strength", "od_log2_rel"]
    dd = d.assign(const=1.0)
    res, notes = fit_logit(dd, cols, cluster=True)
    out = {"n_rows": len(d), "n_events": int(d["event"].sum()),
           "n_clusters": int(d["team_id"].nunique()), "notes": notes, "terms": {}}
    if res is None:
        return out
    for c in cols:
        beta, se = float(res.params[c]), float(res.bse[c])
        out["terms"][c] = {"coef": beta, "se_cluster": se, "z": beta / se,
                           "p": float(res.pvalues[c]),
                           "odds_ratio": math.exp(beta),
                           "or_ci95": [math.exp(beta - 1.96 * se), math.exp(beta + 1.96 * se)]}
    out["loglik"] = float(res.llf)
    out["converged"] = bool(res.mle_retvals.get("converged", False))
    return out


def lr_bins_vs_log(d, m1_loglik):
    res, notes = fit_logit(d.assign(const=1.0), ["const", "ln_dur"], cluster=False)
    stat = 2 * (m1_loglik - res.llf)
    return {"loglik_bins": m1_loglik, "loglik_log": float(res.llf), "lr_stat": float(stat),
            "df": 2, "p": float(stats.chi2.sf(stat, 2)), "notes": notes}


# ---------------------------------------------------------------- descriptions

def deadline_cells(d):
    return {"above_no_exit": int(((d["pd_above"] == 1) & (d["event"] == 0)).sum()),
            "above_exit": int(((d["pd_above"] == 1) & (d["event"] == 1)).sum()),
            "below_no_exit": int(((d["pd_above"] == 0) & (d["event"] == 0)).sum()),
            "below_exit": int(((d["pd_above"] == 0) & (d["event"] == 1)).sum())}


def deadline(d):
    c = deadline_cells(d)
    above, below = c["above_no_exit"] + c["above_exit"], c["below_no_exit"] + c["below_exit"]
    return {"cells": c,
            "share_closing": {"above": c["above_exit"] / above if above else None,
                              "below": c["below_exit"] / below if below else None},
            "share_of_exits_below": (c["below_exit"] / (c["above_exit"] + c["below_exit"])
                                     if c["above_exit"] + c["below_exit"] else None)}


STRENGTH_BANDS = [("le_2", "<= 2"), ("gt_2_le_5", "> 2 to 5"), ("gt_5_le_8", "> 5 to 8"),
                  ("gt_8", "> 8")]


def strength_band(s):
    return pd.cut(s, [-np.inf, 2, 5, 8, np.inf], right=True,
                  labels=[b for b, _ in STRENGTH_BANDS]).astype(str)


def closing_by_strength_band(d):
    band = strength_band(d["strength"])
    out = {}
    for b, label in STRENGTH_BANDS:
        g = d[band == b]
        out[b] = {"label": label, "club_seasons": len(g), "closings": int(g["event"].sum()),
                  "share": float(g["event"].mean()) if len(g) else None}
    return out


def persistent_contenders(windows):
    g = windows.groupby("team_id").agg(n=(COLUMN, "sum"), seasons=("season", "nunique"))
    ids = g.index[(g["n"] == len(SEASONS)) & (g["seasons"] == len(SEASONS))]
    current = windows[windows["season"] == SEASONS[-1]].set_index("team_id")["team"]
    return {"seasons": [SEASONS[0], SEASONS[-1]], "count": len(ids),
            "clubs": sorted(current[i] for i in ids)}


# ---------------------------------------------------------------- figures

def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=9, length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def plot_lines(ax, series, ykey):
    """series: [(label, color, life table rows)]. Hollow markers: fewer than 10 at risk.
    Survival curves start at 1 at duration 0 (no marker)."""
    for label, color, lt in series:
        pts = [r for r in lt if r[ykey] is not None]
        x = [r["duration"] for r in pts]
        y = [r[ykey] for r in pts]
        if ykey == "survival":
            x, y = [0] + x, [1.0] + y
        ax.plot(x, y, color=color, linewidth=2, zorder=2, label=label)
        for r in pts:
            ax.plot(r["duration"], r[ykey], marker="o", markersize=7, zorder=3,
                    markeredgewidth=1.6, markeredgecolor=color,
                    markerfacecolor=SURFACE if r["small"] else color)


def figures(life, groups_lt, median):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    names = {"F": "F (flow, primary)", "L": "L (enter at 1)", "H": "H (enter at 4+)"}

    fig, ax = plt.subplots(figsize=(8, 4.6), facecolor=SURFACE)
    style(ax)
    plot_lines(ax, [(names[s], COLORS[s], life[s]) for s in SAMPLES], "hazard")
    ax.set_xlabel("Duration (seasons in window through season n)", color=INK_2, fontsize=9)
    ax.set_ylabel("Hazard of exit by next Opening Day", color=INK_2, fontsize=9)
    ax.set_xticks(range(1, max(r["duration"] for s in SAMPLES for r in life[s]) + 1))
    ax.set_ylim(0, 1.02)
    ax.legend(frameon=False, fontsize=9, loc="upper right", labelcolor=INK)
    ax.set_title("Window exit hazard by exact duration, window_top6, 2014-2025",
                 loc="left", fontsize=11, color=INK)
    fig.text(0.01, 0.01, f"Hollow markers: fewer than {SMALL_AT_RISK} at risk.",
             fontsize=8, color=INK_2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(FIG_DIR / "hazard_lifetable.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.6), facecolor=SURFACE)
    style(ax)
    plot_lines(ax, [(f"At or above median ({median:+.1f} W)", COLORS["F"],
                     groups_lt["at_or_above_median"]),
                    ("Below median", COLORS["L"], groups_lt["below_median"])], "survival")
    ax.set_xlabel("Duration (seasons in window)", color=INK_2, fontsize=9)
    ax.set_ylabel("Share of windows still open", color=INK_2, fontsize=9)
    ax.set_xticks(range(0, max(r["duration"] for lt in groups_lt.values() for r in lt) + 1))
    ax.set_ylim(0, 1.02)
    ax.legend(frameon=False, fontsize=9, loc="upper right", labelcolor=INK)
    ax.set_title("Survival by Opening Day strength in a window's first season (sample F)",
                 loc="left", fontsize=11, color=INK)
    fig.text(0.01, 0.01, f"Split at the median first-season strength, {median:+.2f} wins per 162 "
             f"vs. the 7th-ranked club. Hollow markers: fewer than {SMALL_AT_RISK} at risk.",
             fontsize=8, color=INK_2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(FIG_DIR / "survival_by_entry_strength.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)


# ---------------------------------------------------------------- main

def main():
    windows, odds, payroll = load()
    existing = json.loads(OUT.read_text())
    pp = build_pp(windows, odds, payroll)
    smp = samples(pp)

    failures = run_checks(pp, smp, windows, existing)
    if failures:
        print(f"{len(failures)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in failures:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    life = {s: life_table(smp[s]) for s in SAMPLES}
    median, first_rows, groups = entry_strength_groups(smp["F"])
    groups_lt = {g: life_table(d) for g, d in groups.items()}

    models = {}
    for s in SAMPLES:
        d = smp[s]
        r1 = m1(d)
        models[s] = {"M1": r1,
                     "M2": covariate_model(d, "ln_dur"),
                     "M2b": covariate_model(d, "dur1"),
                     "lr_bins_vs_log": lr_bins_vs_log(d, r1["loglik"])}

    hazard = {
        "definition": (
            "window_top6, strict consecutive spells. One row per spell per season n, 2014-2025 "
            "(2026 excluded: 2027 not observed). event = 1 if out of the window at season n+1's "
            "Opening Day. era12 = 1 if n+1 >= 2022. strength = 162 x (Opening Day proj_w/(proj_w"
            "+proj_l) minus that of the league's od_rank-7 club), season n. od_log2_rel from "
            "payroll.csv, season n. pd_above = pd_rank <= 6 in season n."),
        "samples": {
            "F": "Left-censored spells dropped; duration = duration_obs. Primary.",
            "L": "All spells; left-censored spells enter in 2014 at duration 1.",
            "H": ("All spells; left-censored spells enter in 2014 at the top bin (4+) and stay "
                  "there: bin 4+, ln(duration capped at 4) = ln 4, duration-1 indicator 0. In "
                  "the exact-duration life table they enter at duration 4 and count up "
                  "(duration_obs + 3); 'entered' counts these delayed entries."),
        },
        "pp_file": str(PP_OUT.relative_to(ROOT)),
        "rows_events": {s: {"rows": len(smp[s]), "events": int(smp[s]["event"].sum()),
                            "spells": int(smp[s]["spell_id"].nunique()),
                            "clubs": int(smp[s]["team_id"].nunique())} for s in SAMPLES},
        "binned": {s: binned_table(smp[s]) for s in SAMPLES},
        "life_tables": {"small_at_risk_threshold": SMALL_AT_RISK,
                        **{s: life[s] for s in SAMPLES}},
        "entry_strength": {
            "sample": "F",
            "median_first_season_strength": median,
            "n_spells": {"at_or_above_median": int(groups["at_or_above_median"]["spell_id"]
                                                   .nunique()),
                         "below_median": int(groups["below_median"]["spell_id"].nunique())},
            "life_tables": groups_lt,
            "spells": [{"spell_id": r.spell_id, "first_season_strength": float(r.strength),
                        "group": "at_or_above_median" if r.strength >= median else
                        "below_median"} for r in first_rows.itertuples()],
        },
        "models": models,
        "model_notes": ("Discrete-time logit. M2/M2b: standard errors clustered by team_id "
                        "(statsmodels cluster, default small-sample correction G/(G-1) x "
                        "(N-1)/(N-K)); intervals are Wald, normal reference. LR test uses the "
                        "ordinary likelihood: M1 (4 bin parameters) vs. intercept + ln(duration "
                        "capped at 4), df 2."),
        "persistent_contenders": persistent_contenders(windows),
        "deadline": {s: deadline(smp[s]) for s in SAMPLES},
        "closing_by_strength_band": {
            "sample": "F",
            "definition": ("Club-seasons by Opening Day strength in season n (wins per 162 above "
                           "the league's od_rank-7 club); closings = event (out of the window at "
                           "n+1's Opening Day); share = closings / club-seasons."),
            "bands": closing_by_strength_band(smp["F"]),
        },
        "figures": ["results/figures/hazard_lifetable.png",
                    "results/figures/survival_by_entry_strength.png"],
    }

    pp.to_csv(PP_OUT, index=False, quoting=csv.QUOTE_MINIMAL)
    figures(life, groups_lt, median)
    existing["hazard"] = hazard
    with open(OUT, "w") as f:
        json.dump(existing, f, indent=2, default=lambda o: o.item() if hasattr(o, "item") else o)
        f.write("\n")

    print("All checks passed.")
    for s in SAMPLES:
        re_ = hazard["rows_events"][s]
        print(f"\n== {s}: {re_['rows']} rows, {re_['events']} events, {re_['spells']} spells")
        print("  binned:", ", ".join(f"{b} {v['rows']}/{v['events']}"
                                     for b, v in hazard["binned"][s].items()))
    print(f"\nWrote {PP_OUT.relative_to(ROOT)}, {OUT.relative_to(ROOT)} (hazard), figures")


if __name__ == "__main__":
    main()
