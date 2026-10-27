# 2027 window forecasts

**Written:** 2026-10-26
**Model:** M2 (ln duration capped at 4, era12, strength, od_log2_rel; discrete-time logit), flow sample
(F), as estimated in `results/results.json` (`hazard.models.F.M2`). Inputs from 2026 Opening Day;
era12 = 1. 95% intervals on the logit scale, clustered by club.
**This file is never edited after its first commit.**

## Forecasts

Probability that each window open on 2026 Opening Day (`window_top6` = 1) is closed on 2027 Opening
Day. Strength is wins per 162 above the league's 7th-ranked club in the 2026 Opening Day projections.
Intervals are computed on the linear predictor with the club-clustered covariance, and both ends are
transformed to probabilities.

| Club | League | Spell start | Duration (capped) | Strength | od_log2_rel | P(closed) | 95% interval |
|---|---|---:|---:|---:|---:|---:|---|
| TEX | AL | 2025 | 2 | +0.7 | +0.092 | 0.56 | 0.41–0.70 |
| PIT | NL | 2026 | 1 | +0.6 | −0.731 | 0.49 | 0.30–0.67 |
| CHC | NL | 2025 | 2 | +1.9 | +0.350 | 0.46 | 0.33–0.60 |
| TOR | AL | 2026 | 1 | +1.9 | +0.671 | 0.37 | 0.18–0.60 |
| BOS | AL | 2025 | 2 | +3.3 | +0.132 | 0.36 | 0.26–0.47 |
| DET | AL | 2026 | 1 | +2.3 | +0.233 | 0.35 | 0.19–0.54 |
| PHI | NL | 2024 | 3 | +4.6 | +0.699 | 0.30 | 0.16–0.49 |
| NYY | AL | 2018 | 4 | +5.6 | +0.769 | 0.27 | 0.12–0.50 |
| ATL | NL | 2020 | 4 | +6.6 | +0.516 | 0.21 | 0.09–0.43 |
| SEA | AL | 2024 | 3 | +6.7 | −0.104 | 0.19 | 0.08–0.38 |
| NYM | NL | 2025 | 2 | +6.9 | +1.028 | 0.14 | 0.05–0.33 |
| LAD | NL | 2014 | 4 | +14.9 | +0.867 | 0.02 | 0.00–0.14 |

Expected number of closed windows (sum of the 12 probabilities): 3.7.

LAD's spell has been open since 2014 (left-censored), so its duration is set to 4.

## Outcome

**Outcome:** closed = below 6th in its league by FanGraphs Make Playoffs on the first archived 2027
date (same rules as `windows.csv`).

## Scoring

**Scoring, fixed in advance:** Brier score against a constant forecast of 30/102 = 0.294; log loss
reported alongside. With 12 forecasts, the result is reported as a single-season check, not a
validation.

## Labor contingency

**Contingency:** the CBA expires December 1, 2026. If 2027 Opening Day odds are archived, score against
them regardless of playoff format. If no 2027 regular season starts by December 31, 2027, the
forecasts are void.

## Limit

Forecasts use 2026 Opening Day information only. Nothing from the 2026 season, deadline or offseason
is in them.
