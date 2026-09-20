# Pre-Registered Predictions
## Competitive Windows in the Current MLB Postseason

**Author:** Matt Koizim
**Locked:** September 20, 2026
**Spec version at time of locking:** research-plan.md v0.8

This file is committed before any data is collected or examined. It is never edited after
its first commit. Any change of position is recorded in `decisions.md` with a date and a
reason, leaving this file intact.

Four predictions are registered with a directional commitment. Three further analyses are
listed as exploratory: they will be run and reported, but no direction is claimed in
advance, and no result from them counts as confirmation of the registered predictions.

---

## Fixed parameters

| Parameter | Baseline | Tested at | What it does |
|---|---|---|---|
| Window threshold | Top 6 of 15 **within league** | 3, 4, 5, 7, 8, 9 | Defines whether a club is "in a window" in a given season |
| Decision grid | 2 points per year: offseason, deadline | — | The only times a club can materially change its roster |
| Signal snapshot | Prior season's close (for offseason); ~1 week pre-deadline (for deadline) | — | Always precedes the behavior it is compared against |
| *k* — behavioral switch persistence | 2 consecutive decision points | 1 and 3 | Whether a mode switch was real |
| Switch dating | Start of the confirming run | — | Confirmation rules decide *whether*, never *when* |
| Minimum meaningful lag | 1 full decision point | — | Below this, treat as contemporaneous |
| Discount rate | Break-even rate reported | 8%, 10%, 12% shown as reference | Rate at which converting and building break even |
| Window length | Strictly consecutive seasons | One-season-dip grace variant | A one-year window is a window of length 1 |
| Classification — P3 | **In-window** mean net horizon score | Terciles where cohorts are needed | What the club did once the window was open |
| Feasible set — P4 | Players who actually changed hands that period, at the prices actually paid | +10% and +25% premium bands | Defines what was reachable; excludes players who never moved |
| Capacity cap — P4 | Club's own tradeable surplus, payroll and CBT capacity at that moment | — | A club cannot spend what it does not have |
| Persistent contenders | Clubs never below threshold in 2016–2026 | — | Right-censored in the model; reported as a named category with a count |
| Matching variables | Payroll tier and ex-ante strength | Unmatched reported alongside | Controls for R3 |
| Study period | 2016–2026 | — | Bounded by the FanGraphs daily odds archive |

**On the baseline threshold.** Top 6 of 15 per league is deliberately generous. A club just
outside the tercile is within striking distance and could reasonably conclude that
converting would lift it into contention. A looser threshold also produces longer measured
windows and a flatter hazard, which works against the thesis rather than for it.

**On persistent contenders.** Clubs that never fall below threshold across 2016–2026 enter
the survival model as right-censored spells and are reported separately, with a count.

**On censoring.** Eleven seasons cannot estimate the hazard for windows longer than roughly
six years. That limit is stated in the results, not extrapolated past.

---

## Registered predictions

### P1 — The mode-switch lag (spine)

Clubs switch from building competitive odds to converting them into championship
probability later than public signal justifies. The behavioral switch — the first decision
point where the net horizon shift turns negative and stays negative for *k* points — lags
the public-signal switch, the first decision point where the club's odds cross the window
threshold and stay crossed at the next one. Both are dated at the start of the confirming
run.

**Falsified if:** the behavioral switch is contemporaneous with or leads the public signal.

**Rival diagnoses tested alongside, not assumed away:**
- **R1 — Supply constraint.** Timing was right; no workable deal existed.
- **R2 — Final-step under-investment.** Timing was right; the club converted, but never enough.
- **R3 — Payroll, not philosophy.** Apparent strategy differences are budget differences.

If R2 proves dominant, that is reported as the finding. It is a different diagnosis with a
different remedy, not a lesser result.

### P2 — Forecast over-persistence

Preseason forecasts over-weight prior-season results. Prior-season record will predict the
error in preseason odds, in a forecast-efficiency test of the Mincer–Zarnowitz form.

**Falsified if:** prior-season record has no predictive power over the forecast error.

This is the only registered prediction testing *why* a lag would exist rather than whether
it does, and it is testable independently of P1.

### P3 — Converting does not shorten the window

A club that converts during an open window — surrendering future value for present value —
does not hold contention for fewer seasons than a club that keeps building through its
window, once matched on payroll tier and ex-ante strength.

This tests the sustainability orthodoxy head-on. The industry's stated belief is that
converting shortens a window by depleting the farm system. Converting does not mechanically
lengthen or shorten a window, so classifying this way is not circular.

**Falsified if:** converter windows are materially shorter under matching.

**Noted in advance:** if the effect is present unmatched and disappears under payroll
matching, the finding is that sustainability is a budget rather than a philosophy. That is
a different conclusion and will be reported as such, not framed as support for this
prediction.

### P4 — Clubs under-convert

During an open window, the title probability a club actually reaches falls short of the
title probability that was reachable to it. Clubs leave achievable championship odds on the
table.

**Reachable** is built only from what actually happened that period:

- Players who **actually changed hands**. If a player moved, he was gettable — someone got
  him. Players who never moved are excluded; there is no evidence they were available.
- At the **prices actually paid**, defined by the acquiring club's outgoing package. Not by
  the author's own valuation of the player — that would turn the finding into an argument
  about the model rather than about club behavior. A premium band of +10% and +25% is tested
  as robustness, since outbidding costs more than matching.
- **Capped** by the club's own tradeable surplus and its payroll and CBT capacity at that
  moment.
- Converted to title probability through the same win curve and bracket simulation used for
  the exchange rate.

**The measure:** frontier gap = reachable − reached, in title-probability points, per open
window.

**Falsified if:** clubs reach or exceed the reachable frontier on average.

**Stated in advance:** periods in which too few impact players moved produce an empty
feasible set. Those are evidence for R1 (supply constraint), not failures of P4, and are
reported separately. This is the honest answer to "there was nothing to do."

**Documented fallback:** if tradeable surplus cannot be estimated reliably from public data,
the frontier is unenforceable and P4 downgrades to the exchange rate alone — does converting
buy more title probability per dollar than retaining that surplus generates in discounted
future title probability? Weaker, because it compares converting against holding rather than
against converting more. Any downgrade is logged in `decisions.md`.

---

## Exploratory analyses — no direction claimed

**E1 — Asymmetry of the lag.** Whether the mode-switch lag differs between window openings
and closings. Contingent on P1 surviving.

**E2 — Realized value of retained prospects.** Surplus value actually realized by retained
top-100 prospects, compared with their trade-market price at peak.

**E3 — Farm rankings as a leading indicator.** Predictive power of organizational farm rank
for contention at 2, 3, and 4 years out.

---

## Author bias disclosure

The author worked in the front offices of the Dodgers, Marlins, and Orioles through 2016.
Two rules govern this exposure:

1. Case selection is by pre-registered rule, with outcomes unexamined at the time of
   selection.
2. No non-public knowledge from inside those organizations appears anywhere in the evidence
   sections. Insider judgment appears only in clearly labeled recommendation sections.
