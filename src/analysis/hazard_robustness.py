"""Post 1 hazard under the eight pre-specified window variants, flow sample (F) only.

Per docs/decisions.md ("Week 3 robustness specification", 2026-11-01, and "Week 3 prompts:
left-censoring under gap-tolerant rules", 2026-11-02):

- top3 ... top9  strict rule at thresholds 3-9 (top6 is the baseline, reproduced, not a variant)
- berth          strict rule, berth-relative threshold (window_berth: 5 in 2014-2019 and 2021,
                 8 in 2020, 6 from 2022)
- top6_grace     threshold 6, a window closes after two straight Opening Days out. Dip seasons
                 are not rows but count toward duration (span), the closing is recorded in the
                 last in-window season, rows run through 2024, and spells starting in 2014 or
                 2015 are left-censored.

Strength is measured against the first club out at each variant's threshold (the (k+1)th club by
od_rank; berths + 1 for berth-relative; the 7th club under grace). Era, payroll and the duration cap
are as at baseline. Bins are fixed at 1, 2, 3, 4+; a bin with zero closings is not fitted (see
hazard.m1). M1, M2, M2b and the bins-vs-log test are hazard.py's. M2/M2b p-values are reported
against the normal and against t with G - 1 degrees of freedom (G = clubs).

Writes results.json's "hazard_robustness" key (every other key is confirmed unchanged byte for
byte), data/processed/hazard_robustness_pp.csv and results/figures/robustness_or.png. Nothing is
written if any check fails or any fit fails to converge or shows separation.

Needs the repo's .venv. Run from the repo root: .venv/bin/python src/analysis/hazard_robustness.py
"""

import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hazard as hz  # noqa: E402
from spells import FIRST, SEASONS, find_spells  # noqa: E402

ROOT = hz.ROOT
OUT = hz.OUT
PP_OUT = ROOT / "data" / "processed" / "hazard_robustness_pp.csv"
FIG = hz.FIG_DIR / "robustness_or.png"

EXPECT_BERTHS = {**{s: 5 for s in (2014, 2015, 2016, 2017, 2018, 2019, 2021)}, 2020: 8,
                 **{s: 6 for s in range(2022, 2027)}}
EXPECT_BASELINE_F = (102, 30)
EXPECT_GRACE_LC = {2014: 12, 2015: 5}
EXPECT_GRACE_2015 = ["CHC", "CLE", "SDP", "SEA", "TOR"]
COVARIATES = ["duration", "ln_dur", "dur1", "era12", "strength", "od_log2_rel"]
TOL = 1e-9

# (key, label, column, k, grace); baseline first, berth-relative beside it
VARIANTS = [("top6", "Baseline: top 6, strict", "window_top6", 6, False),
            ("berth", "Berth-relative, strict", "window_berth", "berths", False),
            *[(f"top{k}", f"Top {k}, strict", f"window_top{k}", k, False) for k in (3, 4, 5)],
            *[(f"top{k}", f"Top {k}, strict", f"window_top{k}", k, False) for k in (7, 8, 9)],
            ("top6_grace", "Top 6, grace", "window_top6", 6, True)]
STRICT_COMPARE = ["top3", "top4", "top5", "top6", "top7", "top8", "top9"]

C_BASE, C_BERTH = "#2a78d6", "#eb6834"   # reference categorical slots 1-2, as in hazard.py


# ---------------------------------------------------------------- per variant

def term_table(model):
    """Add t(G - 1) p-values; 'p' from hazard.covariate_model is the normal reference."""
    g = model["n_clusters"]
    model["t_df"] = g - 1
    for t in model["terms"].values():
        t["p_normal"] = t.pop("p")
        t["p_t"] = float(2 * stats.t.sf(abs(t["z"]), g - 1))
    return model


def survival_after(lt, years=(1, 2, 3, 4)):
    """S(j) = product of (1 - hazard) over durations <= j with anyone at risk."""
    out, s = {}, 1.0
    for r in lt:
        if r["hazard"] is not None:
            s *= 1 - r["hazard"]
        if r["duration"] in years:
            out[str(r["duration"])] = s
    return {str(j): out.get(str(j)) for j in years}


def fit_problems(name, res):
    """Convergence and separation notes for every fit; any note stops the run."""
    conv = {}
    problems = []
    m1 = res["M1"]
    conv["M1"] = (all("ci95_cluster" in b for b in m1["bins"].values() if not b.get("zero_closings"))
                  and not any("converge" in n for n in m1["notes"]))
    for m in ("M2", "M2b"):
        conv[m] = bool(res[m].get("converged")) and not any("converge" in n
                                                             for n in res[m]["notes"])
    conv["lr_log_model"] = not any("converge" in n for n in res["lr_bins_vs_log"]["notes"])
    for m, notes in (("M1", m1["notes"]), ("M2", res["M2"]["notes"]),
                     ("M2b", res["M2b"]["notes"]), ("lr_log_model", res["lr_bins_vs_log"]["notes"])):
        problems += [f"{name} {m}: {n}" for n in notes]
    problems += [f"{name} {m}: did not converge" for m, ok in conv.items() if not ok]
    return conv, problems


def run_variant(key, label, column, k, grace, windows, odds, payroll):
    pp = hz.build_pp(windows, odds, payroll, column=column, k=k, grace=grace)
    f = hz.samples(pp)["F"]
    m1 = hz.m1(f)
    res = {"M1": m1,
           "M2": term_table(hz.covariate_model(f, "ln_dur")),
           "M2b": term_table(hz.covariate_model(f, "dur1")),
           "lr_bins_vs_log": hz.lr_bins_vs_log(f, m1["loglik"])}
    flags = []
    if m1.get("zero_closing_bins"):
        res["lr_bins_vs_log"]["zero_closing_bins"] = m1["zero_closing_bins"]
        res["lr_bins_vs_log"]["zero_closing_note"] = (
            "Zero-closing bin(s) enter the bins model's log-likelihood at the limit (hazard 0, "
            "contribution 0); df unchanged at 2.")
        flags.append(f"zero-closing bin(s): {', '.join(m1['zero_closing_bins'])}")
    conv, problems = fit_problems(key, res)

    lc = pp[pp["left_censored"] == 1].drop_duplicates("spell_id")
    by_year = {str(y): sorted(g["team"]) for y, g in lc.groupby("spell_start")}
    lt = hz.life_table(f)
    gap = 2 if grace else 1
    entry = {
        "label": label,
        "column": column,
        "grace": grace,
        "threshold": k,
        "reference_rank": ({str(s): kk + 1 for s, kk in k.items()} if isinstance(k, dict)
                           else k + 1),
        "last_row_season": hz.LAST_PP - (gap - 1),
        "F": {"windows": int(f["spell_id"].nunique()), "rows": len(f),
              "closings": int(f["event"].sum()), "clubs": int(f["team_id"].nunique())},
        "left_censored_dropped": {"count": len(lc), "by_start_year": by_year},
        "binned": hz.binned_table(f),
        "life_table": lt,
        "survival_after": survival_after(lt),
        **res,
        "converged": conv,
        "flags": flags,
    }
    if grace:
        entry["era12_note"] = (
            "era12 = 1 if n+1 >= 2022, as at baseline. Under grace a closing at n is decided by "
            "the Opening Days of n+1 and n+2; rows with n = 2020 have era12 = 0 and n+2 = 2022.")
        entry["era12_rows_n2020"] = int((f["season"] == 2020).sum())
    return pp, f, entry, problems


# ---------------------------------------------------------------- checks

def spells_of(windows, column, grace):
    current = windows[windows["season"] == SEASONS[-1]].set_index("team_id")["team"]
    out = []
    for team_id, g in windows.groupby("team_id"):
        flags = dict(zip(g["season"], g[column]))
        for first, last in find_spells(flags, grace):
            out.append({"team": current[team_id], "first": first, "last": last,
                        "length": last - first + 1,
                        "in_window_seasons": sum(flags[s] for s in range(first, last + 1))})
    return out


def check_baseline(f, entry, existing):
    fails = []
    if (len(f), int(f["event"].sum())) != EXPECT_BASELINE_F:
        fails.append(f"(1) baseline F: {len(f)} rows / {int(f['event'].sum())} closings, "
                     f"expected {EXPECT_BASELINE_F}")
    old = existing["hazard"]["models"]["F"]["M2"]["terms"]
    new = entry["M2"]["terms"]
    if set(old) != set(new):
        fails.append(f"(1) baseline M2 terms {sorted(new)} vs {sorted(old)}")
    max_diff = 0.0
    for t in old:
        for a, b in (("coef", "coef"), ("se_cluster", "se_cluster")):
            d = abs(old[t][a] - new.get(t, {}).get(b, np.inf))
            max_diff = max(max_diff, d)
            if not d <= TOL:
                fails.append(f"(1) baseline M2 {t} {a}: {new.get(t, {}).get(b)} vs {old[t][a]}")
    return fails, max_diff


def check_strict_counts(windows, existing, variants_info):
    fails, rows = [], {}
    for key in STRICT_COMPARE:
        sp = spells_of(windows, f"window_top{key[3:]}", grace=False)
        ref = existing["variants"][key]
        pp = variants_info[key]["pp"]
        n_lc = int(pp.loc[pp["left_censored"] == 1, "spell_id"].nunique())
        pp_set = {tuple(x) for x in pp[["team", "spell_start"]].drop_duplicates().to_numpy()}
        ref_set = {(s["team"], s["first"]) for s in ref["spells"] if s["first"] <= hz.LAST_PP}
        rows[key] = {"spells": len(sp), "spells_results_json": ref["n_spells"],
                     "left_censored": n_lc,
                     "left_censored_results_json": ref["left_censored"]["count"],
                     "pp_spells_match": pp_set == ref_set}
        if len(sp) != ref["n_spells"]:
            fails.append(f"(2) {key}: {len(sp)} spells, results.json {ref['n_spells']}")
        if n_lc != ref["left_censored"]["count"]:
            fails.append(f"(2) {key}: {n_lc} left-censored, results.json "
                         f"{ref['left_censored']['count']}")
        if pp_set != ref_set:
            fails.append(f"(2) {key}: person-period spells differ from results.json spells "
                         f"starting by {hz.LAST_PP}")
    return fails, rows


def check_reference_zero(windows, odds, variants_info):
    fails = []
    for key, v in variants_info.items():
        rr = v["entry"]["reference_rank"]
        rr = {int(s): r for s, r in rr.items()} if isinstance(rr, dict) else rr
        table = hz.strength_table(windows, odds, rr)
        for (season, league), g in windows.groupby(["season", "league"]):
            ref = g.loc[g["od_rank"] == hz.at_season(rr, season), "team_id"]
            if len(ref) != 1:
                fails.append(f"(3) {key} {season} {league}: {len(ref)} reference clubs")
            elif abs(table[(season, int(ref.iloc[0]))]) > 1e-12:
                fails.append(f"(3) {key} {season} {league}: reference club strength "
                             f"{table[(season, int(ref.iloc[0]))]}")
    return fails


def check_strict_spells(key, pp):
    fails = []
    for sid, g in pp.groupby("spell_id"):
        s = g.sort_values("season")
        if list(s["season"]) != list(range(s["season"].min(), s["season"].max() + 1)):
            fails.append(f"(4) {key} {sid}: seasons not consecutive")
        if s["event"].sum() > 1 or (s["event"].sum() == 1 and s["event"].iloc[-1] != 1):
            fails.append(f"(4) {key} {sid}: closing not confined to the last row")
        if list(s["duration_obs"]) != list(range(1, len(s) + 1)):
            fails.append(f"(4) {key} {sid}: duration_obs not 1..{len(s)}")
    return fails


def check_grace(windows, existing, pp, f):
    fails = []
    flags = windows.set_index(["season", "team_id"])["window_top6"]
    dips = [r for r in pp.itertuples() if flags[(r.season, r.team_id)] != 1]
    if dips:
        fails.append(f"(5) grace: {len(dips)} dip-season rows")
    if pp["season"].max() > 2024:
        fails.append(f"(5) grace: rows after 2024 (max {pp['season'].max()})")
    sp = spells_of(windows, "window_top6", grace=True)
    ref = existing["variants"]["top6_grace"]["spells"]
    late = sorted((s["team"], s["first"], s["last"], s["length"], s["in_window_seasons"])
                  for s in sp if s["first"] >= 2016)
    late_ref = sorted((s["team"], s["first"], s["last"], s["length"], s["in_window_seasons"])
                      for s in ref if s["first"] >= 2016)
    if late != late_ref:
        fails.append("(5) grace: spells starting 2016+ differ from variants.top6_grace.spells")
    # the person-period rows of those spells: in-window seasons through 2024, closing in the
    # last in-window season iff the spell ended by 2024
    by_id = {f"{s['team']}-{s['first']}": s for s in sp}
    for sid, g in f.groupby("spell_id"):
        s = by_id[sid]
        want = [n for n in range(s["first"], min(s["last"], 2024) + 1)
                if flags[(n, int(g["team_id"].iloc[0]))] == 1]
        if list(g.sort_values("season")["season"]) != want:
            fails.append(f"(5) grace {sid}: rows {list(g['season'])}, expected {want}")
        ev = g.sort_values("season")["event"].tolist()
        want_ev = [0] * (len(want) - 1) + [int(s["last"] <= 2024)]
        if ev != want_ev:
            fails.append(f"(5) grace {sid}: events {ev}, expected {want_ev}")
    f_ids = set(f["spell_id"])
    want_f = {f"{s['team']}-{s['first']}" for s in sp if 2016 <= s["first"] <= 2024}
    if f_ids != want_f:
        fails.append(f"(5) grace: F spells {sorted(f_ids ^ want_f)} differ from 2016-2024 starts")
    lc = {}
    for year, n in EXPECT_GRACE_LC.items():
        starters = sorted(s["team"] for s in sp if s["first"] == year)
        lc[year] = starters
        if len(starters) != n:
            fails.append(f"(5) grace: {len(starters)} spells start in {year}, expected {n}")
        if (f["spell_start"] == year).any():
            fails.append(f"(5) grace: spells starting {year} have rows in F")
    if lc[2015] != EXPECT_GRACE_2015:
        fails.append(f"(5) grace: 2015 starters {lc[2015]}, expected {EXPECT_GRACE_2015}")
    return fails, lc


def check_covariates(key, pp, f):
    fails = []
    for c in ["era12", "strength", "od_log2_rel"]:
        if pp[c].isna().any():
            fails.append(f"(6) {key}: {int(pp[c].isna().sum())} person-period rows missing {c}")
    for c in COVARIATES:
        if f[c].isna().any():
            fails.append(f"(6) {key}: {int(f[c].isna().sum())} F rows missing {c}")
    return fails


def check_inputs(windows):
    fails = []
    berths = windows.groupby("season")["berths"].unique()
    for s, b in berths.items():
        if list(b) != [EXPECT_BERTHS[s]]:
            fails.append(f"(input) {s}: berths {list(b)}, expected {EXPECT_BERTHS[s]}")
    if not (windows["window_berth"] == (windows["od_rank"] <= windows["berths"])).all():
        fails.append("(input) window_berth != od_rank <= berths")
    for k in range(3, 10):
        if not (windows[f"window_top{k}"] == (windows["od_rank"] <= k)).all():
            fails.append(f"(input) window_top{k} != od_rank <= {k}")
    return fails


# ---------------------------------------------------------------- figure

def figure(entries):
    keys = [v[0] for v in VARIANTS]
    y = np.arange(len(keys))[::-1]
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 5.2), sharey=True, facecolor=hz.SURFACE)
    panels = [("strength", "Strength (per win per 162 above the first club out)",
               [0.4, 0.6, 0.8, 1, 1.2]),
              ("ln_dur", "Duration (per unit of ln duration, capped at 4)",
               [0.1, 0.3, 1, 3, 10, 30])]
    for ax, (term, title, ticks) in zip(axes, panels):
        hz.style(ax)
        ax.grid(axis="y", visible=False)
        ax.grid(axis="x", color=hz.GRID, linewidth=0.8)
        ax.axvline(1, color=hz.INK_2, linewidth=1, zorder=1)
        for yi, key in zip(y, keys):
            t = entries[key]["M2"]["terms"][term]
            color = C_BASE if key == "top6" else C_BERTH if key == "berth" else hz.INK_2
            ax.plot(t["or_ci95"], [yi, yi], color=color, linewidth=2, solid_capstyle="round",
                    zorder=2)
            ax.plot(t["odds_ratio"], yi, marker="o", markersize=8, color=color,
                    markeredgecolor=hz.SURFACE, markeredgewidth=2, zorder=3)
        ax.set_xscale("log")
        ax.set_xticks(ticks)
        ax.set_xticklabels([f"{t:g}" for t in ticks])
        ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax.set_title(title, loc="left", fontsize=9.5, color=hz.INK)
        ax.set_xlabel("Odds ratio of closing (log scale)", color=hz.INK_2, fontsize=9)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels([entries[k]["label"] for k in keys])
    for lab, key in zip(axes[0].get_yticklabels(), keys):
        lab.set_color(hz.INK)
        if key in ("top6", "berth"):
            lab.set_fontweight("bold")
            lab.set_color(C_BASE if key == "top6" else C_BERTH)
    for ax in axes:
        ax.axhspan(y[1] - 0.5, y[0] + 0.5, color=hz.GRID, alpha=0.35, zorder=0, linewidth=0)
    fig.suptitle("M2 odds ratios by window definition, flow sample (F)", x=0.01, ha="left",
                 fontsize=11, color=hz.INK)
    fig.text(0.01, 0.01, "Points: odds ratios. Lines: 95% intervals, clustered by club, normal "
             "reference. Shaded: baseline and berth-relative.", fontsize=8, color=hz.INK_2)
    fig.tight_layout(rect=(0, 0.03, 1, 0.97))
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=200, facecolor=hz.SURFACE)
    plt.close(fig)


# ---------------------------------------------------------------- report

def fmt(x, d=3):
    return "—" if x is None else f"{x:.{d}f}"


def print_report(hr):
    keys = hr["order"]
    v = hr["variants"]
    head = "| | " + " | ".join(keys) + " |\n|---|" + "---|" * len(keys)

    def row(name, fn):
        return f"| {name} | " + " | ".join(fn(v[k]) for k in keys) + " |"

    print("\n### Sample F\n" + head)
    for c in ("windows", "rows", "closings", "clubs"):
        print(row(c, lambda e, c=c: str(e["F"][c])))
    print(row("left-censored dropped", lambda e: str(e["left_censored_dropped"]["count"])))

    print("\n### Exact-duration life table (at risk / closings)\n" + head)
    max_d = max(r["duration"] for k in keys for r in v[k]["life_table"])
    for d in range(1, max_d + 1):
        def cell(e, d=d):
            r = next((r for r in e["life_table"] if r["duration"] == d), None)
            return "—" if r is None or r["at_risk"] == 0 else f"{r['at_risk']}/{r['exits']}"
        print(row(str(d), cell))

    print("\n### Survival after year j\n" + head)
    for j in ("1", "2", "3", "4"):
        print(row(j, lambda e, j=j: fmt(e["survival_after"][j])))

    print("\n### M1 bin hazards, clustered 95% CI (zero-closing bins: raw, exact CI, *)\n" + head)
    for b in hz.BINS:
        def cell(e, b=b):
            x = e["M1"]["bins"][b]
            if x.get("zero_closings"):
                ci = x["ci95_exact"]
                return f"0/{x['rows']} [0, {ci[1]:.3f}]*" if ci else "0/0*"
            return f"{x['hazard']:.3f} [{x['ci95_cluster'][0]:.3f}, {x['ci95_cluster'][1]:.3f}]"
        print(row(b, cell))
    print(row("rows/closings", lambda e: " ".join(
        f"{e['M1']['bins'][b]['rows']}/{e['M1']['bins'][b]['events']}" for b in hz.BINS)))

    for m in ("M2", "M2b"):
        print(f"\n### {m}: OR [clustered 95% CI]; p normal / p t(G-1)\n" + head)
        terms = list(v["top6"][m]["terms"])
        for t in terms:
            print(row(t, lambda e, t=t: (
                f"{e[m]['terms'][t]['odds_ratio']:.3f} [{e[m]['terms'][t]['or_ci95'][0]:.3f}, "
                f"{e[m]['terms'][t]['or_ci95'][1]:.3f}]")))
            print(row(f"  p {t}", lambda e, t=t: (
                f"{e[m]['terms'][t]['p_normal']:.4f} / {e[m]['terms'][t]['p_t']:.4f}")))
        print(row("G (t df)", lambda e: f"{e[m]['n_clusters']} ({e[m]['t_df']})"))

    print("\n### Bins vs. log LR test\n" + head)
    print(row("LR stat", lambda e: fmt(e["lr_bins_vs_log"]["lr_stat"])))
    print(row("p (df 2)", lambda e: fmt(e["lr_bins_vs_log"]["p"], 4)))

    print("\n### Convergence\n" + head)
    for m in ("M1", "M2", "M2b", "lr_log_model"):
        print(row(m, lambda e, m=m: str(e["converged"][m])))
    print(row("flags", lambda e: "; ".join(e["flags"]) or "—"))


# ---------------------------------------------------------------- main

def main():
    windows, odds, payroll = hz.load()
    raw_before = OUT.read_text()
    existing = json.loads(raw_before)

    failures = check_inputs(windows)
    info, problems = {}, []
    for key, label, column, k, grace in VARIANTS:
        kk = {int(s): int(b) for s, b in windows.groupby("season")["berths"].first().items()} \
            if k == "berths" else k
        pp, f, entry, probs = run_variant(key, label, column, kk, grace, windows, odds, payroll)
        info[key] = {"pp": pp, "f": f, "entry": entry}
        problems += probs

    f1, max_diff = check_baseline(info["top6"]["f"], info["top6"]["entry"], existing)
    failures += f1
    f2, strict_counts = check_strict_counts(windows, existing, info)
    failures += f2
    failures += check_reference_zero(windows, odds, info)
    for key, label, column, k, grace in VARIANTS:
        if not grace:
            failures += check_strict_spells(key, info[key]["pp"])
        failures += check_covariates(key, info[key]["pp"], info[key]["f"])
    f5, grace_lc = check_grace(windows, existing, info["top6_grace"]["pp"],
                               info["top6_grace"]["f"])
    failures += f5

    if failures or problems:
        print(f"{len(failures)} check failure(s), {len(problems)} fit problem(s); nothing written:",
              file=sys.stderr)
        for msg in failures + problems:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    entries = {k: v["entry"] for k, v in info.items()}
    hr = {
        "definition": (
            "Post 1 hazard (hazard.py's M1, M2, M2b and bins-vs-log test) under the pre-specified "
            "window variants, flow sample F only. Strength = wins per 162 above the first club "
            "out at the variant's threshold (reference_rank). Era, payroll and the duration cap "
            "(4) as at baseline. Bins fixed at 1, 2, 3, 4+. M2/M2b standard errors clustered by "
            "team_id (statsmodels default small-sample correction); intervals Wald, normal "
            "reference; p_normal against the normal, p_t against t with G - 1 df (G = clubs in "
            "F). Grace: closes after two straight Opening Days out; dip seasons are not rows but "
            "count toward duration; closing recorded in the last in-window season; rows through "
            "2024; spells starting 2014-2015 left-censored."),
        "sample": "F",
        "order": [v[0] for v in VARIANTS],
        "baseline": "top6",
        "variants": entries,
        "checks": {
            "passed": True,
            "baseline_F_rows_closings": [len(info["top6"]["f"]),
                                         int(info["top6"]["f"]["event"].sum())],
            "baseline_M2_max_abs_diff": max_diff,
            "strict_spell_counts": strict_counts,
            "grace_left_censored_starters": {str(y): t for y, t in grace_lc.items()},
            "hazard_key_unchanged": True,
            "other_keys_unchanged": True,
        },
        "pp_file": str(PP_OUT.relative_to(ROOT)),
        "figure": str(FIG.relative_to(ROOT)),
    }

    # every other key unchanged byte for byte: the original file must re-serialize to itself,
    # and the new file minus hazard_robustness must serialize as the original minus it
    def dump(obj):
        return json.dumps(obj, indent=2,
                          default=lambda o: o.item() if hasattr(o, "item") else o) + "\n"

    def others(obj):
        return dump({k: v for k, v in obj.items() if k != "hazard_robustness"})

    if dump(existing) != raw_before:
        print("results.json does not round-trip; nothing written", file=sys.stderr)
        sys.exit(1)
    new = {**existing, "hazard_robustness": hr}
    text = dump(new)
    if others(json.loads(text)) != others(existing):
        print("other keys would change; nothing written", file=sys.stderr)
        sys.exit(1)
    start = raw_before.index('\n  "hazard": ')
    end = raw_before.index('\n  "', start + 1)
    if raw_before[start:end] not in text:
        print("hazard key text would change; nothing written", file=sys.stderr)
        sys.exit(1)

    pd.concat([v["pp"].assign(variant=k) for k, v in info.items()], ignore_index=True)[
        ["variant"] + hz.PP_COLUMNS].to_csv(PP_OUT, index=False)
    figure(entries)
    OUT.write_text(text)

    print("All checks passed.")
    print(f"(1) baseline F {hr['checks']['baseline_F_rows_closings']}; "
          f"M2 max |diff| {max_diff:.2e}")
    print("(2) strict spell counts:", json.dumps(strict_counts))
    print("(5) grace left-censored starters:", json.dumps(grace_lc))
    print_report(hr)
    print(f"\nWrote {OUT.relative_to(ROOT)} (hazard_robustness), {PP_OUT.relative_to(ROOT)}, "
          f"{FIG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
