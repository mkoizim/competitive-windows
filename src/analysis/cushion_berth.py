"""Closing by Opening Day cushion, berth-relative windows (Post 1).

Rows: data/processed/hazard_robustness_pp.csv, variant berth, left_censored = 0 (flow sample F).
Strength there is wins per 162 above the first club out of the field (od_rank berths + 1), per
"Robustness variants run (Post 1)" (2026-11-02). Bands and definitions are hazard.py's
closing_by_strength_band: <= 2, > 2 to 5, > 5 to 8, > 8.

Writes results.json's "cushion_berth" key (every other key is confirmed unchanged byte for byte).
Nothing is written if any check fails.

Needs the repo's .venv. Run from the repo root: .venv/bin/python src/analysis/cushion_berth.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hazard as hz  # noqa: E402
from jordan import merge_key  # noqa: E402

ROOT = hz.ROOT
OUT = hz.OUT
KEY = "cushion_berth"
ROBUST_PP = ROOT / "data" / "processed" / "hazard_robustness_pp.csv"

EXPECT_ROWS_CLOSINGS = (97, 28)
EXPECT_BANDS = {"le_2": (30, 15), "gt_2_le_5": (29, 9), "gt_5_le_8": (16, 3), "gt_8": (22, 1)}


def main():
    rob = pd.read_csv(ROBUST_PP)
    f = rob[(rob["variant"] == "berth") & (rob["left_censored"] == 0)]
    bands = hz.closing_by_strength_band(f)

    fails = []
    if (len(f), int(f["event"].sum())) != EXPECT_ROWS_CLOSINGS:
        fails.append(f"{len(f)} rows / {int(f['event'].sum())} closings, expected "
                     f"{EXPECT_ROWS_CLOSINGS}")
    if f["strength"].isna().any():
        fails.append(f"{int(f['strength'].isna().sum())} rows missing strength")
    for b, (n, k) in EXPECT_BANDS.items():
        if (bands[b]["club_seasons"], bands[b]["closings"]) != (n, k):
            fails.append(f"band {b}: {bands[b]['closings']} of {bands[b]['club_seasons']}, "
                         f"expected {k} of {n}")
    if fails:
        print(f"{len(fails)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in fails:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    res = {
        "sample": "F",
        "rows": "data/processed/hazard_robustness_pp.csv, variant berth, left_censored = 0",
        "definition": ("Club-seasons by Opening Day strength in season n (wins per 162 above the "
                       "league's first club out of the field, od_rank berths + 1); closings = "
                       "event (out of the berth-relative window at n+1's Opening Day); share = "
                       "closings / club-seasons. Bands as hazard.closing_by_strength_band."),
        "club_seasons": len(f),
        "closings": int(f["event"].sum()),
        "bands": bands,
        "checks": {"passed": True},
    }
    text = merge_key(KEY, res)
    OUT.write_text(text)

    print("All checks passed.")
    print(f"\n== Closing by cushion, berth-relative, F: {len(f)} club-seasons, "
          f"{int(f['event'].sum())} closings")
    for v in bands.values():
        print(f"  {v['label']:>9}: {v['closings']:>2} of {v['club_seasons']:>2}  ({v['share']:.3f})")
    print(f"\nWrote {OUT.relative_to(ROOT)} ({KEY})")


if __name__ == "__main__":
    main()
