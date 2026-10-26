"""Build data/processed/bref_od.csv from the Baseball-Reference pages in data/raw/bref_odds/.

One row per club-season: the earliest-dated row of the club's playoff-odds table (the
preseason simulation, with a blank current W-L). Clubs are ranked within league by
`post`, ties broken by `avg_w` (higher first); bref_top6 is rank 6 or better.

League comes from the season's league page (the WAA-by-position table's "Rank: n in
ALx/NLx" tip), so Houston is NL through 2012. team_id is matched on the club code
against windows.csv (OAK and ATH both map to the Athletics); it is left blank when a
2011-2013 code has no match there (FLA).

Odds are read from the 0.1%-rounded display; "<0.1%" is stored as 0.0005 and ">99.9%"
as 0.9995.

The checks below run before anything is written. If any fails, the script stops and
lists the failures; nothing is written.

Run from the repo root: python3 src/clean/bref_odds.py 2011 2013
(both seasons inclusive).
"""

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "bref_odds"
WINDOWS = ROOT / "data" / "processed" / "windows.csv"
OUT = ROOT / "data" / "processed" / "bref_od.csv"

SUM_TOL = 0.05
PARTS_TOL = 0.002
TOP_N = 6

COLUMNS = [
    "season", "bref_team", "team_id", "league", "date", "srs", "avg_w", "avg_l",
    "post", "div", "wc", "win_ws", "bref_rank", "bref_top6",
]


def berths_per_league(season):
    if season == 2011:
        return 4
    if season == 2020:
        return None  # reported, not checked
    if season >= 2022:
        return 6
    return 5


def league_sizes(season):
    return {"NL": 16, "AL": 14} if season <= 2012 else {"NL": 15, "AL": 15}


def pct(text):
    text = text.strip()
    if text == "<0.1%":
        return 0.0005
    if text == ">99.9%":
        return 0.9995
    return float(text.rstrip("%")) / 100


def leagues(league_html):
    """Club code -> AL/NL from the league page's WAA table tips."""
    found = re.findall(
        r'poptip ([A-Z]{3}) fixed_width" data-stat="Total" data-tip="WL: [0-9-]+, Rank: \d+ in (AL|NL)',
        league_html)
    return dict(found)


def earliest_row(html):
    """Cells of the earliest-dated data row in the playoff_prob table, comments included."""
    start = html.index('id="playoff_prob"')
    table = html[start:html.index("</table>", start)]
    best = None
    for tr in re.findall(r"<tr[^>]*>.*?</tr>", table, re.S):
        cells = dict(re.findall(r'data-stat="([a-z_]+)"[^>]*>(.*?)</t[dh]>', tr, re.S))
        m = re.search(r">(\d{4}-\d{2}-\d{2})<", cells.get("date_sim", ""))
        if m and (best is None or m.group(1) < best[0]):
            best = (m.group(1), cells)
    return best


def team_ids():
    """Club code -> windows.csv team_id, and the (season, team_id) pairs in windows.csv."""
    by_code, pairs = {}, set()
    with open(WINDOWS, newline="") as f:
        for r in csv.DictReader(f):
            by_code[r["team"]] = r["team_id"]
            pairs.add((int(r["season"]), r["team_id"]))
    return by_code, pairs


def build(seasons):
    by_code, pairs = team_ids()
    rows, failures, notes = [], [], []
    for season in seasons:
        sdir = RAW / str(season)
        lg = leagues((sdir / "league.html").read_text(encoding="utf-8"))
        for path in sorted(sdir.glob("*.html")):
            code = path.stem
            if code == "league":
                continue
            date, c = earliest_row(path.read_text(encoding="utf-8"))
            if c["ppr_cur_w"].strip() or c["ppr_cur_l"].strip():
                failures.append(f"{season} {code}: earliest row {date} has current W-L "
                                f"{c['ppr_cur_w']}-{c['ppr_cur_l']}")
            rows.append({
                "season": season, "bref_team": code, "team_id": by_code.get(code, ""),
                "league": lg.get(code, ""), "date": date, "srs": float(c["ppr_srs"]),
                "avg_w": float(c["ppr_avg_w"]), "avg_l": float(c["ppr_avg_l"]),
                "post": pct(c["ppr_postseason"]), "div": pct(c["ppr_division"]),
                "wc": pct(c["ppr_wildcard"]), "win_ws": pct(c["ppr_champs"]),
            })
    rank(rows, failures)
    check(rows, seasons, pairs, failures, notes)
    return rows, failures, notes


def rank(rows, failures):
    groups = defaultdict(list)
    for r in rows:
        groups[(r["season"], r["league"])].append(r)
    for (season, league), grp in groups.items():
        grp.sort(key=lambda r: (-r["post"], -r["avg_w"]))
        for i, r in enumerate(grp, 1):
            r["bref_rank"] = i
            r["bref_top6"] = int(i <= TOP_N)
        for a, b in zip(grp, grp[1:]):
            if (a["post"], a["avg_w"]) == (b["post"], b["avg_w"]):
                failures.append(f"{season} {league}: {a['bref_team']} and {b['bref_team']} "
                                f"tie on post and avg_w")


def check(rows, seasons, pairs, failures, notes):
    by_season = defaultdict(list)
    for r in rows:
        by_season[r["season"]].append(r)
    for season in seasons:
        srows = by_season[season]
        # 1. 30 clubs
        if len(srows) != 30:
            failures.append(f"{season}: {len(srows)} clubs, expected 30")
        # 2. league sizes
        sizes = defaultdict(int)
        for r in srows:
            sizes[r["league"]] += 1
        if dict(sizes) != league_sizes(season):
            failures.append(f"{season}: league sizes {dict(sizes)}, expected {league_sizes(season)}")
        # 3. shared earliest date
        dates = defaultdict(list)
        for r in srows:
            dates[r["date"]].append(r["bref_team"])
        if len(dates) > 1:
            modal = max(dates, key=lambda d: len(dates[d]))
            for d, teams in sorted(dates.items()):
                if d != modal:
                    failures.append(f"{season}: earliest date {d} for {', '.join(teams)} "
                                    f"(others {modal})")
        # 4. post sums to berths
        berths = berths_per_league(season)
        for league in ("AL", "NL"):
            total = sum(r["post"] for r in srows if r["league"] == league)
            notes.append(f"{season} {league}: post sums to {total:.3f}")
            if berths is not None and abs(total - berths) > SUM_TOL:
                failures.append(f"{season} {league}: post sums to {total:.3f}, expected {berths}")
        for r in srows:
            # 5. post = div + wc
            if abs(r["post"] - r["div"] - r["wc"]) > PARTS_TOL:
                failures.append(f"{season} {r['bref_team']}: post {r['post']:.4f} != div "
                                f"{r['div']:.4f} + wc {r['wc']:.4f}")
            # 6. every 2014+ row matches windows.csv
            if season >= 2014 and (season, r["team_id"]) not in pairs:
                failures.append(f"{season} {r['bref_team']}: no team_id match in windows.csv")
            if not r["league"]:
                failures.append(f"{season} {r['bref_team']}: no league on the league page")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("first", type=int)
    ap.add_argument("last", type=int)
    args = ap.parse_args()
    seasons = range(args.first, args.last + 1)

    rows, failures, notes = build(seasons)
    for n in notes:
        print(n)
    if failures:
        print(f"\n{len(failures)} check(s) failed; nothing written:", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        sys.exit(1)

    rows.sort(key=lambda r: (r["season"], r["league"], r["bref_rank"]))
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()})
    print(f"\nwrote {OUT.relative_to(ROOT)}: {len(rows)} rows")


if __name__ == "__main__":
    main()
