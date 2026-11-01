"""Opening Day underdogs: expected vs. actual postseason qualifiers, 2014-2026.

Descriptive count only; it does not test P2 (docs/decisions.md, 2026-10-31 and 2026-11-01). Three
ways of picking each season's underdogs on Opening Day:

- below50         OD Make Playoffs < 50%
- outside_berths  outside the top N in the league by OD Make Playoffs, N = berths per league
                  (window_berth == 0 in data/processed/windows.csv: 5, 8 in 2020, 6 from 2022)
- outside_berths_plus2
                  OD rank in the league worse than berths per league + 2. Run per league; the
                  season figures are the AL and NL counts summed, and the summed range comes
                  from adding the two leagues' simulated counts.

For each, per season:

- actual    underdogs that made the postseason (end-of-season postseason_odds == 1, odds.csv)
- expected  sum of their OD odds
- p05, p95  5th and 95th percentiles of the count in 10,000 simulated seasons, each club an
            independent Bernoulli at its OD odds (inverted-CDF quantiles, so integers)

2020 is included with its 16-team field; its odds are the rebuilt Win Div 1st + Win Div 2nd +
Clinch Wild Card (odds.csv, §3.3a).

Only per-season aggregates are written: the "od_underdogs" key of results/results.json (other
keys are kept) and results/figures/od_underdogs_{variant}.{png,svg}. No team-level odds leave
data/. Nothing is written if any check fails.

Needs numpy and matplotlib (the repo's .venv). Run from the repo root:
.venv/bin/python src/analysis/od_underdogs.py
"""

import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ODDS = ROOT / "data" / "processed" / "odds.csv"
WINDOWS = ROOT / "data" / "processed" / "windows.csv"
OUT = ROOT / "results" / "results.json"
FIG_DIR = ROOT / "results" / "figures"

SEASONS = list(range(2014, 2027))
FIELD16 = 2020
ERA12_FROM = 2022
N_SIMS = 10_000
SEED = 20261031
CLUBS = 30

LEAGUES = ("AL", "NL")

# variant -> (definition, pick, run per league)
VARIANTS = {
    "below50": ("OD Make Playoffs below 50%",
                lambda c: c["od"] < 0.5, False),
    "outside_berths": ("outside the top N in the league on Opening Day (N = berths per league)",
                       lambda c: not c["favored"], False),
    "outside_berths_plus2": ("outside the top N + 2 in the league on Opening Day "
                             "(N = berths per league)",
                             lambda c: c["rank"] > c["berths"] + 2, True),
}
YLABEL = {
    "below50": "Clubs below 50% on Opening Day\nthat made the postseason",
    "outside_berths": "Clubs not favored on Opening Day\nthat made the postseason",
    "outside_berths_plus2": "Clubs outside the top berths + 2 on Opening Day\n"
                            "that made the postseason (AL + NL)",
}

SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
RANGE, DOT = "#d3d2cc", "#8a8984"
TITLE = "How many long shots got in? Opening Day odds vs. the final postseason field"


def berths_per_league(season):
    return 8 if season == FIELD16 else 6 if season >= ERA12_FROM else 5


def load():
    """One dict per club-season: season, league, od, favored, rank, made."""
    snaps = {}
    with open(ODDS) as f:
        for r in csv.DictReader(f):
            if r["snapshot"] in ("opening_day", "end_of_season"):
                snaps.setdefault((int(r["season"]), r["team_id"]), {})[r["snapshot"]] = r
    clubs = []
    with open(WINDOWS) as f:
        for w in csv.DictReader(f):
            key = (int(w["season"]), w["team_id"])
            s = snaps.get(key, {})
            clubs.append({
                "season": key[0],
                "league": w["league"],
                "berths": int(w["berths"]),
                "rank": int(w["od_rank"]),
                "favored": w["window_berth"] == "1",
                "od": float(s["opening_day"]["postseason_odds"]) if "opening_day" in s else None,
                "od_windows": float(w["od_postseason_odds"]),
                "made": (float(s["end_of_season"]["postseason_odds"])
                         if "end_of_season" in s else None),
            })
    return clubs


def run_checks(clubs):
    failures = []
    for season in SEASONS:
        cs = [c for c in clubs if c["season"] == season]
        berths = berths_per_league(season)
        if len(cs) != CLUBS:
            failures.append(f"{season}: {len(cs)} clubs, expected {CLUBS}")
        if any(c["od"] is None or c["made"] is None for c in cs):
            failures.append(f"{season}: club missing an odds.csv snapshot")
            continue
        if any(c["made"] not in (0.0, 1.0) for c in cs):
            failures.append(f"{season}: end-of-season odds not all 0/1")
        if sum(c["made"] for c in cs) != 2 * berths:
            failures.append(f"{season}: {sum(c['made'] for c in cs):.0f} qualifiers, "
                            f"expected {2 * berths}")
        if any(c["berths"] != berths for c in cs):
            failures.append(f"{season}: windows.csv berths != {berths}")
        if any(abs(c["od"] - c["od_windows"]) > 1e-9 for c in cs):
            failures.append(f"{season}: OD odds differ between odds.csv and windows.csv")
        if any(c["favored"] != (c["rank"] <= berths) for c in cs):
            failures.append(f"{season}: window_berth != (od_rank <= berths)")
        for league in LEAGUES:
            ranks = sorted(c["rank"] for c in cs if c["league"] == league)
            if ranks != list(range(1, CLUBS // 2 + 1)):
                failures.append(f"{season} {league}: OD ranks are not 1-{CLUBS // 2}")
            n_fav = sum(c["favored"] for c in cs if c["league"] == league)
            if n_fav != berths:
                failures.append(f"{season} {league}: {n_fav} favored, expected {berths}")
    return failures


def count(cs, rng):
    """Aggregates for one group of clubs, plus its simulated counts."""
    od = np.array([c["od"] for c in cs])
    sims = (rng.random((N_SIMS, len(od))) < od).sum(axis=1)
    return {
        "n_clubs": len(cs),
        "actual": int(sum(c["made"] for c in cs)),
        "expected": float(od.sum()),
    }, sims


def summarize(agg, sims):
    p05, p95 = np.quantile(sims, [0.05, 0.95], method="inverted_cdf")
    return {**agg, "expected": round(agg["expected"], 3), "p05": int(p05), "p95": int(p95)}


def season_result(clubs, season, pick, seed, by_league):
    """Seeded per (variant, season[, league]) so a range doesn't depend on which others run."""
    cs = [c for c in clubs if c["season"] == season and pick(c)]
    out = {"season": season, "berths_per_league": berths_per_league(season)}
    if not by_league:
        return {**out, **summarize(*count(cs, np.random.default_rng([*seed, season])))}
    leagues, total, total_sims = {}, {"n_clubs": 0, "actual": 0, "expected": 0.0}, 0
    for j, league in enumerate(LEAGUES):
        agg, sims = count([c for c in cs if c["league"] == league],
                          np.random.default_rng([*seed, season, j]))
        leagues[league] = summarize(agg, sims)
        total = {k: total[k] + agg[k] for k in total}
        total_sims = total_sims + sims
    return {**out, **summarize(total, total_sims), "by_league": leagues}


def print_table(variant, results):
    print(f"\n{variant}: {VARIANTS[variant][0]}")
    print(f"{'season':>6} {'field':>5} {'n':>4} {'actual':>6} {'expected':>8} "
          f"{'p05–p95':>8}  position")
    for r in results:
        pos = ("below" if r["actual"] < r["p05"] else
               "above" if r["actual"] > r["p95"] else "inside")
        print(f"{r['season']:>6} {2 * r['berths_per_league']:>5} {r['n_clubs']:>4} "
              f"{r['actual']:>6} {r['expected']:>8.2f} {r['p05']:>4}–{r['p95']:<3}  {pos}"
              + "".join(f"   {lg} {x['n_clubs']:>2} {x['actual']} {x['expected']:>5.2f} "
                        f"{x['p05']}–{x['p95']}" for lg, x in r.get("by_league", {}).items()))


def plot(variant, results, ymax):
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=9, length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)

    for r in results:
        x = r["season"]
        ax.plot([x, x], [r["p05"], r["p95"]], color=RANGE, linewidth=9,
                solid_capstyle="butt", zorder=1)
        ax.plot([x - 0.22, x + 0.22], [r["expected"]] * 2, color=INK_2, linewidth=1.6, zorder=2)
        ax.scatter([x], [r["actual"]], s=46, color=DOT, edgecolor=SURFACE, linewidth=1.6,
                   zorder=3)

    top = ymax + 1.8
    ax.set_ylim(-0.4, top)
    ax.set_xlim(SEASONS[0] - 0.6, SEASONS[-1] + 0.6)
    ax.set_xticks(SEASONS)

    # Field-size eras: 2020 shaded, 10 | 12 break dashed, labels along the top
    ax.axvspan(FIELD16 - 0.45, FIELD16 + 0.45, color=GRID, alpha=0.45, linewidth=0, zorder=0)
    ax.axvline(ERA12_FROM - 0.5, color=INK_2, linewidth=0.9, linestyle=(0, (3, 3)), zorder=0)
    for x, label in [(2016.5, "10-team field"), (FIELD16, "16-team"), (2021, "10-team"),
                     (2024, "12-team field")]:
        ax.text(x, top - 0.25, label, ha="center", va="top", fontsize=8, color=INK_2)

    ax.set_ylabel(YLABEL[variant], color=INK_2, fontsize=9)
    ax.set_title(TITLE, loc="left", fontsize=11, color=INK)

    handles = [
        plt.Line2D([], [], color=RANGE, linewidth=7, label="5th–95th pct, 10,000 sims"),
        plt.Line2D([], [], color=INK_2, linewidth=1.6, label="Expected (sum of OD odds)"),
        plt.Line2D([], [], marker="o", linestyle="", color=DOT, markersize=6.5, label="Actual"),
    ]
    ax.legend(handles=handles, frameon=False, fontsize=8.5, loc="upper center", labelcolor=INK,
              ncol=4, bbox_to_anchor=(0.5, -0.07), handlelength=1.6)
    fig.text(0.01, 0.01, "Source: FanGraphs playoff odds (Opening Day and final regular-season "
             "snapshots). Each club an independent Bernoulli at its OD Make Playoffs odds.\n"
             "2020 odds are Win Div 1st + Win Div 2nd + Clinch Wild Card (16-team field).",
             fontsize=7, color=INK_2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "svg"):
        fig.savefig(FIG_DIR / f"od_underdogs_{variant}.{ext}", dpi=200, facecolor=SURFACE)
    plt.close(fig)


def main():
    clubs = load()
    failures = run_checks(clubs)
    if failures:
        print(f"{len(failures)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in failures:
            print(f"  {msg}", file=sys.stderr)
        sys.exit(1)

    results = {v: [season_result(clubs, s, pick, [SEED, i], by_league) for s in SEASONS]
               for i, (v, (_, pick, by_league)) in enumerate(VARIANTS.items())}
    for v, rs in results.items():
        print_table(v, rs)

    existing = json.loads(OUT.read_text())
    existing["od_underdogs"] = {
        "description": "Opening Day underdogs: realized qualifiers vs. sum of OD odds, with a "
                       "5th-95th percentile range from independent-Bernoulli simulation. "
                       "Descriptive; does not test P2.",
        "decision": "docs/decisions.md, 2026-10-31 (two entries) and 2026-11-01",
        "n_sims": N_SIMS,
        "seed": SEED,
        "seeding": "numpy default_rng([seed, variant index, season(, league index)])",
        "quantile_method": "inverted_cdf",
        "note_2020": "16-team field; OD odds are Win Div 1st + Win Div 2nd + Clinch Wild Card",
        "variants": {v: {"definition": VARIANTS[v][0], "by_season": rs}
                     for v, rs in results.items()},
    }
    with open(OUT, "w") as f:
        json.dump(existing, f, indent=2)
        f.write("\n")

    # One y scale for both figures so they compare directly
    ymax = max(max(r["p95"], r["actual"]) for rs in results.values() for r in rs)
    for v, rs in results.items():
        plot(v, rs, ymax)
    print(f"\nWrote {OUT.relative_to(ROOT)} (od_underdogs), "
          f"results/figures/od_underdogs_{{{','.join(VARIANTS)}}}.{{png,svg}}")


if __name__ == "__main__":
    main()
