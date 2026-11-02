"""Jordan (2018) ex post contention windows beside the strict and grace windows (Post 1).

Per docs/decisions.md ("Week 3 robustness specification", 2026-11-01, item F, and "Week 3
prompts: left-censoring under gap-tolerant rules; Jordan reference", 2026-11-02). Description
only; no models.

Contending season (end_of_season snapshot in odds.csv, 2014-2025), any of:
- won its division (division order by W%; a tie for first is broken by the actual division title,
  TITLE_TIES below, and any other tie for first fails check 2; ties below first share the better
  rank);
- made the postseason as a non-division-winner (postseason_odds >= 0.999);
- 2nd or 3rd in its division and at most 5 games behind the division winner, games behind =
  ((leader W - W) + (L - leader L)) / 2;
- 87 or more wins.
2020: W% >= .537 in place of 87 wins, 1.85 games in place of 5. The 2018 records include the
game-163 tiebreakers.

Jordan windows: open with the first of two straight contending seasons; a single non-contending
season inside a window does not end it; a window closes after two straight non-contending seasons
and ends at the last contending season before them. Length is the full span, counting any
one-season gap, so no window is shorter than 2 seasons. Left-censored (dropped, listed) unless two
straight non-contending seasons occur between 2014 and the season before its first contending
season. Right-censored: last contending season 2024 or 2025.

Life tables follow the grace variant's construction: one row per contending season in a window,
duration = seasons since the window opened (gaps count toward it but are not rows, since a gap
season's outcome is settled by the row before it), the closing recorded in the window's last
contending season, and rows only through 2023, the last season whose outcome (two seasons on) is
observed for every club.

Compared with the strict ex ante windows (hazard_pp.csv, F) and the grace windows
(hazard_robustness_pp.csv, top6_grace, F). Writes results.json's "jordan_comparison" key (every
other key is confirmed unchanged byte for byte) and results/figures/survival_three_definitions.png.
Nothing is written if any check fails.

Needs the repo's .venv. Run from the repo root: .venv/bin/python src/analysis/jordan.py
"""

import json
import statistics
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hazard as hz  # noqa: E402
from hazard_robustness import survival_after  # noqa: E402

ROOT = hz.ROOT
OUT = hz.OUT
KEY = "jordan_comparison"
ROBUST_PP = ROOT / "data" / "processed" / "hazard_robustness_pp.csv"
FIG = hz.FIG_DIR / "survival_three_definitions.png"

FIRST, LAST = 2014, 2025
LAST_ROW = LAST - 2          # a closing at n is seen at n+1 and n+2
WINS, GB = 87, 5
WPCT_2020, GB_2020 = 0.537, 1.85
POSTSEASON = 0.999
YEARS = tuple(range(1, 7))

# Ties for first with no tiebreaker game: the records show a tie, the title went by head-to-head.
# (season, league, division): (title, tied with, source)
# Source: the actual division titles, tiebreaker as given in the 2026-11-02 Week 3 prompt.
TITLE_TIES = {
    (2022, "NL", "E"): ("ATL", "NYM", "ATL won the NL East title on head-to-head over NYM"),
    (2023, "AL", "W"): ("HOU", "TEX", "HOU won the AL West title on head-to-head over TEX"),
    (2025, "AL", "E"): ("TOR", "NYY", "TOR won the AL East title on head-to-head over NYY"),
}

EXPECT_CLUB_SEASONS = 360
EXPECT_BERTHS = {**{s: 5 for s in (2014, 2015, 2016, 2017, 2018, 2019, 2021)}, 2020: 8,
                 **{s: 6 for s in range(2022, 2026)}}
EXPECT_WINDOWS_CLOSINGS = {"strict": (38, 30), "grace": (20, 12)}
DEFS = ["jordan", "strict", "grace"]
LABELS = {"jordan": "Jordan (2018), ex post",
          "strict": "Strict ex ante, top 6 (F)",
          "grace": "Grace ex ante, top 6 (F)"}
COLORS = {"jordan": "#2a78d6", "strict": "#eb6834", "grace": "#1baf7a"}  # slots 1-3, as hazard.py


# ---------------------------------------------------------------- contending seasons

def contending(odds):
    """One row per club-season, 2014-2025, with each Jordan criterion and the union, and the
    ties for first found: [(season, league, division, tied clubs, resolution or None)]."""
    e = odds[(odds["snapshot"] == "end_of_season") & odds["season"].between(FIRST, LAST)].copy()
    e["wpct"] = e["w"] / (e["w"] + e["l"])
    e["div_rank"] = (e.groupby(["season", "league", "division"])["wpct"]
                     .rank(method="min", ascending=False).astype(int))
    ties = []
    for (season, league, division), g in e[e["div_rank"] == 1].groupby(
            ["season", "league", "division"]):
        if len(g) == 1:
            continue
        tied = sorted(g["team"])
        title = TITLE_TIES.get((season, league, division))
        if title is None or sorted(title[:2]) != tied:
            ties.append((season, league, division, tied, None))
            continue  # left at shared rank 1: check 2 fails
        e.loc[g.index[g["team"] == title[1]], "div_rank"] = 2
        ties.append((season, league, division, tied, title))
    leader = (e[e["div_rank"] == 1].groupby(["season", "league", "division"])[["w", "l"]].first()
              .rename(columns={"w": "lead_w", "l": "lead_l"}))
    e = e.join(leader, on=["season", "league", "division"])
    e["gb"] = ((e["lead_w"] - e["w"]) + (e["l"] - e["lead_l"])) / 2
    is2020 = e["season"] == 2020
    e["c_division"] = e["div_rank"] == 1
    e["c_postseason"] = ~e["c_division"] & (e["postseason_odds"] >= POSTSEASON)
    e["c_close"] = e["div_rank"].isin([2, 3]) & (e["gb"] <= e["season"].map(
        lambda s: GB_2020 if s == 2020 else GB))
    e["c_wins"] = (is2020 & (e["wpct"] >= WPCT_2020)) | (~is2020 & (e["w"] >= WINS))
    e["contending"] = e[["c_division", "c_postseason", "c_close", "c_wins"]].any(axis=1)
    return e.sort_values(["season", "league", "division", "div_rank"], ignore_index=True), ties


# ---------------------------------------------------------------- Jordan windows

def jordan_windows(flags):
    """[(first, last)] for one club, given {season: bool} for 2014-2025. A window still open at
    2025 ends at its last contending season so far."""
    out, s = [], FIRST
    while s < LAST:
        if not (flags[s] and flags[s + 1]):
            s += 1
            continue
        first = last = s
        t = s + 1
        while t <= LAST:
            if flags[t]:
                last = t
            elif t - last == 2:   # two straight non-contending seasons
                break
            t += 1
        out.append((first, last))
        s = last + 3 if last + 2 <= LAST else LAST + 1
    return out


def double_gap_before(flags, first):
    """Seasons y (2014 <= y, y + 1 <= first - 1) with y and y + 1 both non-contending."""
    return [y for y in range(FIRST, first - 1) if not flags[y] and not flags[y + 1]]


def build_jordan(e):
    current = e[e["season"] == LAST].set_index("team_id")["team"]
    windows, dropped, rows = [], [], []
    for team_id, g in e.groupby("team_id"):
        flags = dict(zip(g["season"], g["contending"]))
        team = current[team_id]
        for first, last in jordan_windows(flags):
            seq = "".join("C" if flags[y] else "-" for y in range(FIRST, first))
            gaps = double_gap_before(flags, first)
            w = {"team": team, "first": first, "last": last, "length": last - first + 1,
                 "gap_seasons": [y for y in range(first, last + 1) if not flags[y]]}
            if not gaps:
                reason = ("first contending season 2014 or 2015: no room for two non-contending "
                          "seasons after 2014" if first <= FIRST + 1 else
                          "no two straight non-contending seasons in 2014-"
                          f"{first - 1} (seasons before: {seq})")
                dropped.append({**w, "reason": reason})
                continue
            closed = last + 2 <= LAST
            w["status"] = "closed" if closed else "right_censored"
            windows.append(w)
            for n in range(first, min(last, LAST_ROW) + 1):
                if not flags[n]:
                    continue  # gap season: counts toward duration, not a row
                rows.append({"team_id": team_id, "team": team, "spell_id": f"{team}-{first}",
                             "season": n, "duration": n - first + 1,
                             "event": int(closed and n == last)})
    pp = pd.DataFrame(rows).sort_values(["team", "season"], ignore_index=True)
    return windows, dropped, pp


# ---------------------------------------------------------------- strict and grace

def ex_ante(pp):
    """Flow-sample windows from a hazard person-period frame (left_censored == 0)."""
    f = pp[pp["left_censored"] == 0].copy()
    f["duration"] = f["duration_obs"]
    last = f.sort_values("season").groupby("spell_id").tail(1)
    windows = [{"team": r.team, "first": int(r.spell_start), "last": int(r.season),
                "length": int(r.duration_obs),
                "status": "closed" if r.event else "right_censored"}
               for r in last.itertuples()]
    lc = pp[pp["left_censored"] == 1].drop_duplicates("spell_id")
    dropped = [{"team": r.team, "first": int(r.spell_start)} for r in lc.itertuples()]
    return windows, dropped, f


def summary(windows, dropped, f, name):
    done = [w["length"] for w in windows if w["status"] == "closed"]
    lt = hz.life_table(f)
    return {
        "label": LABELS[name],
        "windows": len(windows),
        "windows_with_rows": int(f["spell_id"].nunique()),
        "closings": len(done),
        "right_censored": len(windows) - len(done),
        "left_censored_dropped": len(dropped),
        "rows": len(f),
        "completed_length": {"n": len(done),
                             "mean": statistics.mean(done) if done else None,
                             "median": statistics.median(done) if done else None,
                             "distribution": {str(k): done.count(k) for k in sorted(set(done))}},
        "life_table": lt,
        "survival_after": survival_after(lt, YEARS),
    }


def two_by_two(e, windows_csv):
    w = windows_csv[windows_csv["season"].between(FIRST, LAST)].set_index(["season", "team_id"])
    d = e.join(w["window_top6"], on=["season", "team_id"])
    cells = {}
    for jc in (True, False):
        for wt in (1, 0):
            cells[f"{'contending' if jc else 'not_contending'}__"
                  f"{'window' if wt else 'no_window'}"] = int(((d["contending"] == jc) &
                                                               (d["window_top6"] == wt)).sum())
    return d, cells


# ---------------------------------------------------------------- checks

def run_checks(e, ties, d, cells, windows_csv, jw, dropped, summaries):
    fails = []
    if len(e) != EXPECT_CLUB_SEASONS:
        fails.append(f"(1) {len(e)} club-seasons, expected {EXPECT_CLUB_SEASONS}")
    for season, league, division, tied, title in ties:
        if title is None:
            fails.append(f"(2) {season} {league} {division}: tie for first not in TITLE_TIES "
                         f"({', '.join(tied)})")
    found = {(s, lg, dv) for s, lg, dv, _, title in ties if title is not None}
    for k in TITLE_TIES:
        if k not in found:
            fails.append(f"(2) {k}: listed in TITLE_TIES but no such tie for first in the records")
    for (season, league), g in e.groupby(["season", "league"]):
        n_div = int(g["c_division"].sum())
        if n_div != 3 or g.groupby("division")["c_division"].sum().ne(1).any():
            fails.append(f"(2) {season} {league}: {n_div} division winners")
        post = int((g["c_division"] | (g["postseason_odds"] >= POSTSEASON)).sum())
        n_odds = int((g["postseason_odds"] >= POSTSEASON).sum())
        if post != EXPECT_BERTHS[season] or n_odds != EXPECT_BERTHS[season]:
            fails.append(f"(3) {season} {league}: {post} postseason clubs ({n_odds} with "
                         f"postseason_odds >= {POSTSEASON}), expected {EXPECT_BERTHS[season]}")
    g20 = e[e["season"] == 2020]
    bad = g20[~(g20["w"] + g20["l"]).between(58, 60)]
    if len(bad):
        fails.append(f"(4) 2020 W + L outside 58-60: {', '.join(bad['team'])}")
    n_window = int(windows_csv[windows_csv["season"].between(FIRST, LAST)]["window_top6"].sum())
    if sum(cells.values()) != EXPECT_CLUB_SEASONS:
        fails.append(f"(5) 2x2 sums to {sum(cells.values())}")
    if cells["contending__window"] + cells["not_contending__window"] != n_window:
        fails.append(f"(5) window margin {cells['contending__window'] + cells['not_contending__window']}"
                     f", window_top6 club-seasons {n_window}")
    for w in dropped:
        if not w.get("first") or not w.get("reason"):
            fails.append(f"(6) left-censored window not listed in full: {w}")
    n_lc_found = sum(1 for t, g in e.groupby("team_id")
                     for first, _ in jordan_windows(dict(zip(g["season"], g["contending"])))
                     if not double_gap_before(dict(zip(g["season"], g["contending"])), first))
    if n_lc_found != len(dropped):
        fails.append(f"(6) {n_lc_found} left-censored windows found, {len(dropped)} listed")
    for name, (n_w, n_c) in EXPECT_WINDOWS_CLOSINGS.items():
        s = summaries[name]
        if (s["windows"], s["closings"]) != (n_w, n_c):
            fails.append(f"(7) {name}: {s['windows']} windows / {s['closings']} closings, "
                         f"expected {n_w} / {n_c}")
    s1 = summaries["jordan"]["survival_after"]["1"]
    if s1 != 1:
        fails.append(f"(8) Jordan survival after year 1 = {s1}")
    return fails


# ---------------------------------------------------------------- figure

def figure(summaries):
    fig, ax = plt.subplots(figsize=(8, 4.6), facecolor=hz.SURFACE)
    hz.style(ax)
    hz.plot_lines(ax, [(f"{LABELS[k]}: {summaries[k]['windows']} windows, "
                        f"{summaries[k]['closings']} closings", COLORS[k],
                        summaries[k]["life_table"]) for k in DEFS], "survival")
    ax.set_xlabel("Duration (seasons since the window opened)", color=hz.INK_2, fontsize=9)
    ax.set_ylabel("Share of windows still open", color=hz.INK_2, fontsize=9)
    ax.set_xticks(range(0, max(r["duration"] for k in DEFS
                               for r in summaries[k]["life_table"]) + 1))
    ax.set_ylim(0, 1.02)
    ax.legend(frameon=False, fontsize=9, loc="upper right", labelcolor=hz.INK)
    ax.set_title("Window survival under three definitions, 2014-2025 (flow samples)",
                 loc="left", fontsize=11, color=hz.INK)
    fig.text(0.01, 0.01, f"Hollow markers: fewer than {hz.SMALL_AT_RISK} at risk. Jordan windows "
             "cannot be shorter than 2 seasons.", fontsize=8, color=hz.INK_2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(FIG, dpi=200, facecolor=hz.SURFACE)
    plt.close(fig)


# ---------------------------------------------------------------- results.json

def dump(obj):
    return json.dumps(obj, indent=2, default=lambda o: o.item() if hasattr(o, "item") else o) + "\n"


def merge_key(key, value):
    """Add a new top-level key to results.json, leaving every existing key byte for byte.
    Returns the new text, or exits without writing."""
    raw = OUT.read_text()
    existing = json.loads(raw)
    if key in existing:
        sys.exit(f"results.json already has '{key}'; nothing written")
    if dump(existing) != raw:
        sys.exit("results.json does not round-trip; nothing written")
    text = dump({**existing, key: value})
    head = raw.rstrip()[:-1].rstrip()   # everything before the closing brace
    new = json.loads(text)
    if not text.startswith(head) or any(dump(new[k]) != dump(existing[k]) for k in existing) \
            or list(new)[:-1] != list(existing):
        sys.exit("existing keys would change; nothing written")
    return text


# ---------------------------------------------------------------- main

def report(res):
    print("\n== Ties for first (no tiebreaker game)")
    for t in res["ties_for_first"]:
        print(f"  {t['season']} {t['league']} {t['division']}: {' and '.join(t['tied'])} "
              f"{t['record'][0]}-{t['record'][1]}; {t['resolution']} "
              f"({t['division_winner']} rank 1, {t['rank_2']} rank 2)")
    print("\n== Club-seasons, 2014-2025")
    print("  Jordan contending:", res["club_seasons"]["contending"], "of",
          res["club_seasons"]["total"], "| by criterion:",
          json.dumps(res["club_seasons"]["by_criterion"]))
    c = res["two_by_two"]["cells"]
    print("  2x2 (Jordan x window_top6):")
    print(f"    {'':16}{'window':>8}{'no window':>11}")
    print(f"    {'contending':16}{c['contending__window']:>8}{c['contending__no_window']:>11}")
    print(f"    {'not contending':16}{c['not_contending__window']:>8}"
          f"{c['not_contending__no_window']:>11}")
    print("\n== Windows (flow samples)")
    print(f"  {'':28}{'windows':>8}{'closed':>8}{'right-c':>8}{'left-c dropped':>16}"
          f"{'mean len':>10}{'median':>8}")
    for k in DEFS:
        s = res["definitions"][k]
        cl = s["completed_length"]
        print(f"  {s['label']:28}{s['windows']:>8}{s['closings']:>8}{s['right_censored']:>8}"
              f"{s['left_censored_dropped']:>16}{cl['mean']:>10.2f}{cl['median']:>8}")
    print("\n  Survival after year j:")
    print(f"  {'':28}" + "".join(f"{j:>7}" for j in YEARS))
    for k in DEFS:
        sa = res["definitions"][k]["survival_after"]
        print(f"  {LABELS[k]:28}" + "".join(f"{sa[str(j)]:>7.3f}" if sa[str(j)] is not None
                                           else f"{'-':>7}" for j in YEARS))
    for k in DEFS:
        print(f"\n  Life table, {LABELS[k]}:")
        print("    dur  at_risk  exits  censored  hazard  survival")
        for r in res["definitions"][k]["life_table"]:
            h = "-" if r["hazard"] is None else f"{r['hazard']:.3f}"
            sv = "-" if r["survival"] is None else f"{r['survival']:.3f}"
            print(f"    {r['duration']:>3}  {r['at_risk']:>7}  {r['exits']:>5}  {r['censored']:>8}"
                  f"  {h:>6}  {sv:>8}")
    print("\n== Jordan left-censored windows (dropped)")
    for w in res["jordan_left_censored"]:
        print(f"  {w['team']} {w['first']}-{w['last']}: {w['reason']}")


def main():
    odds = pd.read_csv(hz.ODDS)
    windows_csv = pd.read_csv(hz.WINDOWS)
    e, ties = contending(odds)
    jw, dropped, jpp = build_jordan(e)
    d, cells = two_by_two(e, windows_csv)

    strict_w, strict_d, strict_f = ex_ante(pd.read_csv(hz.PP_OUT))
    rob = pd.read_csv(ROBUST_PP)
    grace_w, grace_d, grace_f = ex_ante(rob[rob["variant"] == "top6_grace"])
    summaries = {"jordan": summary(jw, dropped, jpp, "jordan"),
                 "strict": summary(strict_w, strict_d, strict_f, "strict"),
                 "grace": summary(grace_w, grace_d, grace_f, "grace")}

    fails = run_checks(e, ties, d, cells, windows_csv, jw, dropped, summaries)
    if fails:
        print(f"{len(fails)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in fails:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    crit = {c: int(e[c].sum()) for c in ("c_division", "c_postseason", "c_close", "c_wins")}
    res = {
        "definition": (
            "Jordan (2018) contending season, end_of_season snapshot, 2014-2025: division winner "
            "(division order by W%; ties for first broken by the actual division title, see "
            "ties_for_first; ties below first share the better rank); postseason as a non-division-"
            "winner (postseason_odds >= 0.999); 2nd or 3rd in the division with games behind the "
            "division winner <= 5 (games behind = ((leader W - W) + (L - leader L)) / 2); or W >= "
            "87. 2020: W% >= .537 and <= 1.85 games. Window opens with the first of two straight "
            "contending seasons, survives one non-contending season, closes after two straight "
            "non-contending seasons and ends at the last contending season before them; length = "
            "full span. Left-censored unless two straight non-contending seasons occur in 2014 to "
            "the season before the window's first contending season. Right-censored: last "
            "contending season 2024 or 2025."),
        "comparison_samples": {
            "strict": "data/processed/hazard_pp.csv, left_censored = 0 (window_top6, strict).",
            "grace": ("data/processed/hazard_robustness_pp.csv, variant top6_grace, left_censored "
                      "= 0 (spells starting 2014 or 2015 excluded)."),
        },
        "life_table_note": (
            "Jordan life table built as the grace variant's: one row per contending season in a "
            "window, duration = seasons since the window opened (gap seasons count toward it but "
            "are not rows), closing recorded in the last contending season, rows through 2023 "
            "(the last season whose outcome, two seasons on, is observed). windows_with_rows "
            "excludes windows opening after 2023. Strict and grace life tables are hazard.py's "
            "life_table on their person-period rows. survival_after j = product of (1 - hazard) "
            "over durations <= j; null where the table ends before j. Strict and grace windows "
            "are measured in Opening Day seasons, Jordan windows in end-of-season records."),
        "min_length_note": "Jordan windows cannot be shorter than 2 seasons.",
        "ties_for_first": [
            {"season": s, "league": lg, "division": dv, "tied": tied, "record": rec,
             "division_winner": title[0], "rank_2": title[1], "resolution": title[2]}
            for s, lg, dv, tied, title in ties
            for rec in [e.loc[(e["season"] == s) & (e["team"] == title[0]), ["w", "l"]]
                        .iloc[0].astype(int).tolist()]],
        "club_seasons": {"total": len(e), "contending": int(e["contending"].sum()),
                         "by_criterion": {"division_winner": crit["c_division"],
                                          "postseason_non_division_winner": crit["c_postseason"],
                                          "second_or_third_within_gb": crit["c_close"],
                                          "wins_87_or_wpct_537_2020": crit["c_wins"]}},
        "two_by_two": {
            "rows": "Jordan contending (yes/no)",
            "columns": "window_top6 (yes/no), Opening Day",
            "seasons": [FIRST, LAST],
            "cells": cells,
            "margins": {"contending": cells["contending__window"] + cells["contending__no_window"],
                        "not_contending": (cells["not_contending__window"]
                                           + cells["not_contending__no_window"]),
                        "window": cells["contending__window"] + cells["not_contending__window"],
                        "no_window": (cells["contending__no_window"]
                                      + cells["not_contending__no_window"])},
            "agreement": (cells["contending__window"] + cells["not_contending__no_window"]) / len(e),
        },
        "definitions": summaries,
        "jordan_windows": sorted(jw, key=lambda w: (w["team"], w["first"])),
        "jordan_left_censored": sorted(dropped, key=lambda w: (w["team"], w["first"])),
        "jordan_contending_by_club": {
            t: "".join("C" if c else "-" for c in g.sort_values("season")["contending"])
            for t, g in e.assign(team=e["team_id"].map(
                e[e["season"] == LAST].set_index("team_id")["team"])).groupby("team")},
        "checks": {"passed": True, "club_seasons": len(e),
                   "window_top6_club_seasons": (cells["contending__window"]
                                                + cells["not_contending__window"])},
        "figure": str(FIG.relative_to(ROOT)),
    }

    text = merge_key(KEY, res)
    figure(summaries)
    OUT.write_text(text)
    print("All checks passed.")
    report(res)
    print(f"\nWrote {OUT.relative_to(ROOT)} ({KEY}), {FIG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
