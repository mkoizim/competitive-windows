# Competitive Windows in the Current MLB Postseason
## Research Plan v0.8

**Author:** Matt Koizim
**Started:** September 2026
**Soft target:** SABR Analytics Conference abstract (2025 deadline was Nov 21; 2024 was Nov 20 — confirm the 2027 call)
**Cadence:** 4–8 hrs/week, no hard deadline

**Version history**
- v0.1 — window survival + exchange rate
- v0.2 — reframed around self-observation asymmetry
- v0.3 — **mode-switch reframe.** The claim is no longer that clubs act late; it is that they switch from building odds to converting odds late. Adds the net horizon score, forecast-efficiency testing, revision decomposition, and rival diagnoses. Corrects the horizon-score sign convention.
- v0.3.1 — sign convention corrected to acquired − surrendered (converting is negative); YTC restated as duration.
- v0.4 — FanGraphs confirmed daily back to Opening Day 2016. Added a two-period design, day-level public-signal dating, and daily-series upgrades to §4c.
- v0.8 — **P4 replaced.** Was "prior building caps the peak" (cohort-based, near-certain to be untestable); now "clubs under-convert," measured against a reachable frontier built from players who actually moved at prices actually paid (§4g). R2 promoted from rival diagnosis to P4's own test. §2.2 cohort contingency retired.
- v0.7 — P3 moved to in-window classification (tests the sustainability orthodoxy directly). P4 made conditional on cohort balance (§2.2). Persistent contenders named as a reported category (§2.3).
- v0.6 — Predictions table in §2 reconciled with `predictions.md` (four registered, three exploratory). §3.4 rewritten to separate in-window from prior-behavior classification.
- v0.5 — **Parameters settled with the author.** Threshold moved to within-league top 6 of 15. Both switches dated at start-of-run, on a two-decision-point grid; parameter *D* retired. Strict consecutive windows with the grace rule demoted to robustness. Strategy classified at the window level. Break-even discount rate replaces an assumed rate. The ~2003 futures panel is dropped.

---

## 1. Objective

Test whether MLB organizations switch from **building** competitive odds to **converting** them into championship probability later than public signal justifies — and whether that lag, or an equivalent failure to take the final step, costs them titles.

### 1.1 Why "mode switch" and not "acting late"

Foundation work — development, controllable acquisitions, draft and international investment — is itself a leading decision that raises odds. A club whose odds rise because it developed players has, by construction, acted before the signal. Any prediction phrased as "behavior lags signal" is therefore trivially false.

The real question is when a club stops pouring concrete and puts a roof on. Two modes:

- **Odds-building** — surrender present value for future value. Raises the ceiling.
- **Odds-converting** — surrender future value for present value. Turns ceiling into title probability.

Both are rational. The hypothesis is that the transition between them happens late.

### 1.2 Why the non-adversarial framing

Clubs evaluate other organizations dispassionately and their own with sunk costs, internal advocates for players they drafted, private medicals, and an owner in the room. Self-assessment lag requires no one to be bad at their job. It is also the version a baseball-ops leader can forward internally without it reading as an accusation.

**Tone rule.** Neutral diagnosis, sharp recommendation. Critique decisions made under uncertainty, never decision-makers. Diagnosis sections stay clinical; the aggressive view belongs in the recommendation section, after the evidence is established.

### 1.3 The two frames, and how they shape windows

Reported separately. Never blended.

- **Frame A — Championship probability.** Rewards **peak height**. Titles are won at the top of the curve; a short tall window beats a long flat one.
- **Frame B — Owner economics.** Rewards **area under the curve, with diminishing returns**. Gennaro's NPV estimates — roughly $20M for a first berth, $13M for a second consecutive, $9M for a third — mean relevance pays repeatedly but pays less each time. Revenue responds to *reaching* October far more than to winning it.

**Consequence, and the theoretical backbone of P4:** sustainability is a Frame B strategy defended in Frame A language. The frames disagree about what "missing a window" means, so they must be fixed before any window is called missed.

---

## 2. Pre-registered predictions

Commit with real numbers before building anything. Publish in the appendix of Post 1.

**Four registered, three exploratory.** Seven predictions all pointing one way invites the
obvious read that something will be found regardless. The registered set is deliberately
small; the rest are run and reported without a directional claim.

### Registered

| # | Prediction | Operational test | Falsified if |
|---|---|---|---|
| **P1** | **(Spine)** Clubs switch from building to converting later than public signal justifies | Lag between behavioral switch date and public-signal switch date (§4a), both dated at start-of-run on the decision grid | Behavioral switch leads or is contemporaneous with public signal |
| **P2** | Preseason forecasts over-weight prior-season results | Forecast-efficiency test (§4b): prior-season record predicts forecast error | Prior-season record has no predictive power over the error |
| **P3** | Converting during an open window does not shorten it | Window length and hazard, by **in-window** net horizon score, matched on payroll tier and ex-ante strength | Converter windows are materially shorter under matching |
| **P4** | Clubs under-convert: title probability reached falls short of what was reachable | Reached vs. reachable title probability per open window, where reachable is built from players who actually changed hands that period at the prices actually paid, capped by the club's own tradeable surplus and payroll capacity (§4g) | Clubs reach or exceed the reachable frontier on average |

### Exploratory — no direction claimed

| # | Analysis |
|---|---|
| **E1** | Whether the lag is asymmetric between window openings and closings. Contingent on P1 surviving. |
| **E2** | Realized surplus value of retained top-100 prospects vs. their peak trade-market price. |
| **E3** | Predictive power of organizational farm rank for contention at 2, 3, and 4 years out. |

### 2.1 Rival diagnoses — test, don't assume away

P1 attributes the gap to late recognition. Three alternatives produce the same surface pattern and must be tested in the same post:

| Rival | What it claims | Test |
|---|---|---|
| **R1 — Supply constraint** | Timing was right; no workable deal existed | Was an impact player acquired by *someone* that period, at a price this club could have paid? If yes, supply wasn't binding for them (§4d) |
| **R2 — Final-step under-investment** | Timing was right; the club converted, but never enough | The reached-vs-reachable frontier gap (§4g). This is now P4's own test — R2 is promoted from a rival explanation to a registered prediction |
| **R3 — Payroll, not philosophy** | Clubs are "sustainable" because they're poor | Match on payroll tier and revenue; report matched and unmatched |

R2 may turn out to be the dominant failure mode. That would be a better finding than R1 and should be reported as such, not buried.

### 2.2 How windows are manufactured — a reported result, not a gate

Earlier drafts made P4 conditional on finding enough window-openings preceded by
*converting* rather than building. P4 no longer needs that cohort split, so the contingency
is retired.

The count is still reported in Post 1: *windows are preceded by net building in X% of
cases.* It is expected to be lopsided toward building, and if it is, that is a clean
empirical statement about how contention gets manufactured — build, then a window opens,
then the conversion decision arrives. It sets up Post 3 rather than gating it.

### 2.3 Persistent contenders

Some clubs — likely the Dodgers and Yankees — never fall below threshold across 2016–2026.
They enter the survival model as right-censored spells, which is the statistically correct
handling, but they contribute little to hazard estimation while having the most conversion
capacity in the sample.

**Report them as a named category**, with a count: *in eleven seasons, N clubs never left
contention; the hazard describes the remainder.* That is more honest than a hazard curve
that quietly excludes the most interesting clubs, and the count is itself a finding.

### 2.4 Falsification

**Primary (P1):** if the behavioral switch tracks or leads the public-signal switch, there is no blind spot. The series becomes a descriptive study of window duration — still publishable, headline claim gone. Say so plainly.

**Secondary (Frame A):** if title probability purchased per $1 of surplus value spent is lower than the discounted title probability that surplus generates when retained, aggressive pursuit is the inferior strategy. Discount rate set up front: propose 8–12% annually, test across the range.

### 2.3 Author bias

Most predictions point the same direction. Prior employment with LAD, MIA, BAL — three obvious case studies. Two rules, stated in the published piece:

- Case selection by pre-registered rule, with outcomes unexamined at the time of selection.
- **No non-public knowledge from inside those organizations appears anywhere in the evidence.** Insider judgment is an asset in the recommendation section and a liability in the evidence section. Keep the wall visible to the reader.

---

## 3. Definitions

Fix in the spec, before data. Each is a defensible choice; the point is to choose once, in public.

### 3.1 Core measure

Two separate quantities. Never combine them.

**(1) Net surplus value** — dollars. Acquired minus surrendered. Did the club win the trade? Not what this study is about, but needed as a control.

**(2) Years to contribution (YTC)** — years. This is **Macaulay duration applied to surplus value**. For any asset, project surplus value by future season, then take the value-weighted average of the arrival years:

> YTC = Σ(t × value in year t) ÷ Σ(value in all years)

The denominator divides out the dollars entirely. What remains is a date, not an amount. A prospect does not become more valuable by being further away; its value simply arrives later. Index t from 0 for the current season.

Reference points: deadline rental ≈ 0.2; 27-year-old with four years of control ≈ 1.8; Double-A arm ≈ 4.0; recent draft pick ≈ 5.

**(3) Net horizon shift** — dollar-years. Per club, per transaction period, using standard accounting order:

> Net horizon shift = Σ(acquired value × YTC) − Σ(surrendered value × YTC)

This is the change in the duration of the club's asset base. **Negative = converting** — value pulled toward the present, duration shortened. **Positive = building** — value pushed into the future, duration lengthened.

Also report it divided by total value moved, which converts dollar-years into plain years: how much earlier or later the value ended up. Two transaction periods per year: offseason and deadline.

*Caution:* published surplus-value tables already encode proximity partially. Check for double-counting against YTC.

### 3.2 Dates and lag

Both switch dates are measured on the same two-point-per-year grid, because that is when
clubs can actually act. Daily odds exist, but a club with a hot May cannot add outside
talent until late July.

**The decision grid.** Two decision points per year:

| Decision point | Behavior observed | Signal available at the time |
|---|---|---|
| Offseason | Net horizon shift across the winter | Odds at the close of the prior season |
| Deadline | Net horizon shift across the deadline | Odds ~1 week before the deadline |

The signal snapshot always precedes the behavior it is compared against. Opening Day odds
are *not* the offseason decision signal — they already contain the offseason moves, so
using them would compare behavior against its own consequence.

**Start-of-run dating.** Both switches are dated at the **start of the run that later
confirms them**, never at the moment of confirmation.

- **Behavioral switch:** the first period where the net horizon shift turns negative
  (converting) and stays negative for *k* consecutive periods. The date is that first
  period, not the *k*-th.
- **Public-signal switch:** the first decision point where the club's odds cross the
  window threshold and stay crossed at the following decision point. The date is the first
  crossing.

Confirmation rules decide whether a switch was *real*. They must not decide *when* it
happened. Dating at confirmation would bake a lag of up to a year into the measurement
before any data was examined, and P1 would be half-proven by construction.

**Parameter *D* is retired.** It existed to filter noise out of a daily series. Sampling at
decision points removes the noise instead, so there is nothing left for *D* to do.

- **Lag:** decision points between the signal switch and the behavioral switch. Minimum
  meaningful lag is one full period; anything less is contemporaneous.
- **Daily series, secondary use.** The daily odds remain useful descriptively — *by the day
  of the trade, the club had been below threshold for N straight days* — but they are
  reported as color, not as the parameter that dates anything.
- **Robustness:** a changepoint model on the horizon-score series (PELT or binary
  segmentation on the mean) as a second dating method. Report both. Disagreement is a
  finding about transition noise and belongs in the paper.

### 3.3 Windows

**Threshold is within-league.** The postseason field is set inside each league — three
division winners and three wild cards per side. Ranking across all 30 clubs would import
parity differences between leagues into a measure that has nothing to do with them.

- **Window (observed):** a season where the club ranks in the **top 6 of 15 within its
  league** by ex-ante postseason odds. Tested at 3, 4, 5, 7, 8, and 9 (equivalently 6
  through 18 across both leagues).
- **Why a loose baseline.** Top-6-per-league is deliberately generous. A club just outside
  the tercile is within striking distance and could reasonably conclude that converting
  would lift it into contention. A looser threshold also produces longer measured windows
  and a flatter hazard, which works *against* the thesis. Say so in the paper.
- **Division path comes free.** Simulation-based playoff odds already price in division
  strength, so ranking those odds handles the stacked-division problem without a separate
  control.
- **Two different measures, two different jobs.** Contention is within-league
  (postseason access). Title probability is cross-league (the World Series is
  inter-league). Post 1's hazard uses the access measure; Frame A's exchange rate uses
  title probability. Do not substitute one for the other.
- **Window length:** strictly consecutive qualifying seasons. A one-year window is a window
  of length 1 and enters the hazard model as such.
- **Grace rule is the robustness variant, not the default.** Smoothing one-year windows
  away would delete the left tail of exactly the distribution Post 1 is estimating. Run the
  one-season-dip variant as a check and report both.
- **Short windows get a descriptive section, not a category.** The 2013 Red Sox — last
  place either side of a title — are interesting *because* the window was short. Did anyone
  see it coming? Did they convert? That is a P1 case study. Building "real vs. fluke" into
  the definition would be circular, since whether it was knowable is the thing being
  measured.
- **Hazard:** *given a club has been a contender for n consecutive seasons, the probability
  it stops being one in season n+1.*
- **Contention:** deliberately not "made the playoffs." Berths are outcomes; this study is
  about ex-ante position.

### 3.3a Study period

**2016–2026, single period.** FanGraphs posts playoff odds daily back to Opening Day 2016.

*v0.4 proposed a second panel back to ~2003 built on de-vigged World Series futures. That
is dropped.* Futures are cross-league title odds and cannot express a within-league
postseason-access threshold, so the two panels would have measured different constructs.
Adding vig removal, patchy archive coverage, and a second manual pipeline to buy a
mismatched variable is a bad trade.

**Consequence, stated plainly.** Eleven seasons means windows longer than roughly six years
are right-censored and their hazard is not estimable. Survival methods handle censoring
correctly, but the paper must say what the data cannot support rather than extrapolating.
2020 (60 games) and the 2022 format change both sit inside the sample and need flagging.

**Optional descriptive context.** Realized postseason qualification going back decades is
free and complete from Retrosheet or Baseball Reference. It is an *outcome* measure, not
ex-ante, so it cannot carry the hazard model — but it can bound the question descriptively
in a clearly labeled section. Cheap, and worth including if Post 1's spell count looks thin.

### 3.4 Strategy classification

**Three measurements from one horizon series. They must not be confused.**

| | Measures | Window used | Feeds |
|---|---|---|---|
| **Switch dating** | When the club changed mode | Unsmoothed, across the open window | P1 |
| **In-window profile** | What the club did *once the window was open* | Mean net horizon score during the open window | P3 |
| **Prior profile** | How the club arrived at the window | Trailing 3-year mean, ending at window open | Descriptive only (§2.2) — no registered prediction depends on it |

**P3 uses in-window behavior.** The question is whether converting during an open window
shortens it. This is not circular: converting does not mechanically extend or shorten a
window, and the industry's own belief is that it *shortens* one by depleting the farm. P3
therefore tests the sustainability orthodoxy directly.

**P4 uses neither.** P4 no longer compares cohorts at all. It compares each club against its
own feasible frontier (§4g), which removes the need for a builder/converter split and the
cohort-balance problem that came with it. The prior profile survives as a descriptive
statistic: how often windows are preceded by building.

**Window level, not club level.** A club can be a prior-builder entering its 2017 window and
a prior-converter entering its 2023 window. Two observations, not a contradiction — and P1
asserts clubs switch modes, so labeling a club once for a decade would average away the
behavior being studied.

**Hard rule:** no classification uses outcomes. Window length and peak title probability
never enter any cohort definition.

**Cohorts:** terciles of the relevant mean where a narrative needs them, matched within
ex-ante strength band and payroll tier. Report continuous and cohort versions; if they
disagree, trust the continuous one.

**Sample caution:** eleven seasons yields roughly one to two windows per club, minus the
persistent contenders who yield one censored spell each. Window-level N will be small —
check spell counts before committing to any cohort split.

### 3.5 Structural aggression

Accepting knowingly underwater contract tail years to buy present CBT relief. Applies only to clubs near the threshold — stratify by payroll tier. Tracked alongside the horizon score, not inside it.

### 3.6 Explicitly rejected

- **Buy/sell binary.** Selling is buying for the future. Allocation is continuous, not categorical.
- **Contract length as a duration signal.** Long deals are frequently AAV instruments for CBT purposes with tail years known to be underwater. Length reveals payroll structure, not contention horizon.
- **Cost-side-only measurement (v0.2).** Surrendering a near-MLB arm for a rental is a present bet; surrendering the same arm for another controllable 23-year-old is lateral. Cost alone doesn't disambiguate direction. Both sides, netted.

---

## 4. Measurement

### 4a. Behavioral switch — the net horizon score

Compute the score (§3.1) for every club-period. Date the switch by the *k*-period sign rule, with changepoint detection as robustness (§3.2). Include offseason activity, not just the deadline.

Separately, record the **magnitude** of the largest present-oriented move during each open window. This is the R2 test and is independent of timing.

### 4b. Forecast efficiency — is persistence actually excessive?

Persistence must be *proven* excessive, not assumed. Three regressions:

| # | Regression | Yields |
|---|---|---|
| 1 | Preseason odds at *t* on prior-season results, with roster-change and aging controls | **Assumed** persistence |
| 2 | Actual outcome at *t* on the same prior-season results, same controls | **Realized** persistence |
| 3 | Difference | The gap |

Equivalently and preferably, run the direct form: regress outcome on forecast and test whether prior-season record still predicts the residual. If it does, the forecast leaned on last season too hard. This is Mincer–Zarnowitz — citable, and recognizable to a referee.

*This replaces v0.2's approach of implying optimal persistence from the hazard model, which invited a circularity complaint.*

**Run two series separately:**
- **FanGraphs playoff odds** — built from player projections, closer to a model baseline.
- **Editorial tiers** (The Athletic previews and similar) — closer to belief actually circulating, since editorial coverage is partly club-sourced.

The gap between them is the sentiment layer on top of the math. Because editorial coverage is partly club-sourced, editorial over-persistence is evidence of *shared industry* over-persistence, not simply media bias.

### 4c. Midseason revisions — decompose before interpreting

A midseason odds jump may be information, or may be a good first half that was mostly luck. As a raw series it cannot distinguish them. Decompose each revision into:

- The part explained by **record to date** — largely noise.
- The part explained by **underlying components** — run differential, peripherals, health, playing-time changes.

Only the component-driven part counts as evidence the signal existed. For the lag test, what matters is whether the information was *knowable then*, not whether the outcome later validated it. Judging by outcomes is hindsight and a referee will say so.

**What the daily series adds.** With odds posted every day since 2016, this stops being a three-point chain and becomes a continuous trajectory. Three things become available that a preseason/midseason snapshot could not support:

- **Odds on the day of each transaction.** Every acquisition and non-acquisition can be scored against the club's title probability at that exact moment, rather than against a season-level average.
- **Persistence before the decision.** How many consecutive days the club had already been below (or above) threshold when it acted. This is the core knowability measure.
- **Slope, not just level.** A club at 20% and falling is in a different position than a club at 20% and rising. Include the trailing 30-day slope as a covariate in the lag model.

**Caveat:** FanGraphs has revised its odds model over the years. Confirm which seasons are methodologically comparable before running anything across the full 2016–2026 span, and report any break.

### 4d. Rival diagnoses

- **R1 (supply):** per transaction period, count impact players actually moved and their acquisition price. If a club near the threshold didn't move while comparable talent changed hands at a payable price, supply wasn't binding for them.
- **R2 (final step):** measured by the reached-vs-reachable frontier in §4g, which is P4's own test. Reported as the magnitude of under-conversion, in title-probability points left on the table.
- **R3 (payroll):** all cohort comparisons matched on payroll tier and revenue proxy; unmatched results reported alongside.

### 4g. The reachable frontier (P4)

For each open window, compute the title probability the club **reached** and the title
probability it could have **reached** with the talent that was actually available to it.

**Constructing the feasible set.** Reachable is built only from what really happened that
period:

- **Players who actually changed hands.** If a player moved, he was gettable — another club
  got him. Players who stayed put are excluded; there is no evidence they were available at
  any price.
- **At the prices actually paid.** The acquiring club's outgoing package defines the price.
  Do not substitute your own valuation of the player — that turns the finding into an
  argument about your model rather than about club behavior. Test a premium band (paying
  10% and 25% over observed price) as robustness, since outbidding costs more than matching.
- **Capped by the club's own tradeable surplus** at that moment, and by payroll and CBT
  capacity. A club cannot spend what it does not have.
- **Converted to title probability** through the same win-curve and bracket simulation used
  for the exchange rate (Post 4).

**The measure:** frontier gap = reachable title probability − reached title probability, in
probability points, per open window.

**What kills this analysis, stated in advance:**
- If tradeable surplus cannot be estimated reliably from public data, the cap is
  unenforceable and the frontier becomes fantasy. Go/no-go before Post 4 begins.
- If too few impact players move in a given period, the feasible set is empty and that
  period is evidence for R1 (supply constraint), not for P4. Report those periods
  separately — they are the honest answer to "there was nothing to do."

**Documented fallback.** If the frontier proves infeasible, P4 downgrades to the exchange
rate alone: does converting buy more title probability per dollar than retaining that
surplus generates in discounted future title probability? Weaker, because it compares
converting against holding rather than against converting *more*. Log the downgrade in
`decisions.md` if it happens.

### 4e. Front-office vs. public convergence

Clubs run better versions of the same machinery — proprietary projections, medicals, internal development data. For single-season assessment, public odds are a defensible proxy for front-office belief. Two caveats:

- Divergence is systematic, not random. Clubs are consistently more optimistic about their own players, and that optimism concentrates exactly where the thesis lives: teams on the margin.
- Single-season convergence implies nothing about multi-year agreement. Nobody consults a public four-year team forecast; clubs maintain internal multi-year depth charts.

**Fallback thesis.** If beliefs converge, the claim becomes "teams apply a different decision rule to the same odds," not "teams miscalculate." Two clubs at identical 25% title probability behave completely differently. That version requires proving no one's math was wrong — only that the decision rule is miscalibrated against the value function. More defensible, and the fallback if P1 weakens.

### 4f. Speculative

**ZiPS multi-year team outlooks.** If consistent archived team-level multi-year forecasts exist, that is a directly contemporaneous duration instrument. Existence unverified — allocate 30 minutes, no more.

---

## 5. Series structure

Modular. Each post stands alone. Ordered so cheap wins precede expensive work.

**Post 1 — The hazard of contention.** How long windows last and what governs length.
- Report the **hazard**, not an average. Length is likely bimodal — a few perennials, a long tail of short bursts — and an average pools two populations and describes neither. The hazard is also the question a decision-maker actually faces.
- **Model the full distribution, then illustrate with outliers.** Studying only long windows to learn what makes windows long selects on the dependent variable.
- Covariates: core age, committed payroll, farm rank, division strength, market size.
- This is the SABR abstract.

**Post 2 — Farm rankings as a leading indicator.** Runs E3. Cheap, self-contained, uses Baseball America data already in hand. Publish first if Post 1 bogs down in cleaning.

**Post 3 — Putting the roof on.** The spine. Mode-switch lag (§4a), forecast efficiency (§4b), revision decomposition (§4c), and all three rival diagnoses (§4d). P1, P2, and E1 live here.

**Post 4 — Leaving it on the table.** Tests P4. Builds the exchange rate (title probability purchased per unit of surplus surrendered, with the break-even discount rate), then the reachable frontier on top of it (§4g). Requires simulating the 12-team bracket on historical strengths, since 2022–25 gives only four postseasons.

**Post 5 — The luck ledger.** Expected titles (sum of ex-ante title odds) vs. actual, by organization. Answers "who did the right things and got unlucky." Likely the most shareable output; cheap once Post 1's data exists.

**Optional — Owner economics.** Frame B. Weak data: Forbes estimates, attendance, and Atlanta Braves Holdings filings — the only publicly traded club and therefore the only real revenue series for calibration. Directional only. Do not let this consume the project.

**Deliverables per post:** essay, technical appendix, public repo. Once Post 3 or 4 lands, add a 2-page decision memo with one chart — the artifact that actually gets forwarded inside a front office.

---

## 6. Rules fixed before analysis

- **Case selection by rule**, not by interest. Write the rule down. If LAD, MIA, or BAL appear, they appear because the rule selected them.
- **The bias wall** (§2.3): no non-public knowledge in the evidence sections.
- **No number in any write-up is typed by hand.** Every figure is generated by code into `results.json` and read from there.
- **Robustness checks** on every headline result: alternative thresholds, eras, window definitions, both dating methods.
- **Endogeneity.** Teams convert when they believe they're good. Any builder-vs-converter comparison must be matched on ex-ante strength and payroll tier.
- **No selecting on the dependent variable.** Applies to outlier analysis in Post 1 and cohort construction throughout.
- **Era caution.** CBA expires after 2026 with a possible lockout. Keep conclusions structural — odds math, aging curves, supply — rather than tied to current rules.

---

## 7. Phase plan to the SABR abstract

~60 hours across 10 weeks at 6 hrs/week. Post 1 only.

| Weeks | Phase | Hours | Output |
|---|---|---|---|
| 1–2 | Spec + lit review | 12 | This document finalized; predictions committed; lit notes |
| 2 | **Network review of the spec** | 2 | Feedback on definitions from 1–2 baseball contacts, before data work |
| 3–4 | Data acquisition + audit | 12 | Cached local dataset, data dictionary, documented gaps |
| 5–7 | Post 1 analysis | 18 | Hazard model, covariates, robustness |
| 8–9 | Write-up + abstract | 12 | Post 1 draft; 500-word abstract |
| 10 | Referee pass + revise | 6 | Submitted abstract, near-final post |

Posts 2–5: 25–40 hours each. Total project: 150–250 hours.
**Fallback if November slips:** SABR national convention abstracts run in February (Feb 22 in 2026).

---

## 8. Data inventory

| Source | Use | Cost | Risk |
|---|---|---|---|
| FanGraphs playoff odds, daily | Model-baseline belief series; daily signal dating; ex-ante strength 2016+ | Membership | Confirmed daily back to Opening Day 2016. Model revisions over the span may break comparability — check. Respect site terms; cache once. |
| Preseason World Series futures (Sports Odds History) | Post 5 luck ledger only — expected vs. actual titles | Free | Vig removal required. No longer used as a window threshold. |
| The Athletic previews / editorial tiers | Industry-circulating belief series | Subscription | Tier framing inconsistent year to year; likely manual coding |
| Baseball America Top 100 + org rankings | Farm covariate; prospect valuation | Owned | Methodology changes across years |
| Retrosheet / Baseball Reference transactions | Horizon scores, switch dating | Free | Rate-limited; cache once |
| Cot's Contracts | Payroll, CBT position, contract structure | Free | Manual cleanup likely |
| Lahman database | Rosters, ages, service proxies | Free | — |
| Published surplus-value tables | YTC inputs, exchange-rate denominator | Free | Methodology varies; pick one, cite it, check proximity double-counting |
| Forbes valuations / Braves Holdings filings | Frame B only | Free | Estimates, not audited, except Braves |

**Standing rule:** pull once, cache locally, version the cache.

---

## 9. Repository layout

```
competitive-windows/
  CLAUDE.md
  docs/
    research-plan.md      # this file, versioned in-place
    predictions.md        # first commit; never edited after
    decisions.md          # dated log of every settled question
    data-dictionary.md
    lit-notes.md
  data/raw/               # cached pulls, never edited
  data/interim/
  data/processed/
  src/scrape/  src/clean/  src/analysis/
  results/figures/  results/tables/
  results/results.json    # every number that appears in prose
  posts/post1-hazard/
```

Two conventions matter more than the structure:

1. **`results.json` is the only source of numbers in writing.**
2. **`decisions.md` gets an entry whenever a methodological question closes:**

```
## 2026-09-19 — Behavioral switch dating
Question: how to date the mode switch objectively
Options: changepoint detection | k-period sign persistence | first positive period
Chose: k-period sign persistence, k=2; changepoint as robustness
Why: pre-registrable, symmetric with the public-signal rule
Revisit if: methods disagree by >1 period for >20% of clubs
```

---

## 10. Claude usage map (Pro plan)

Usage limits are the binding constraint; Code and chat draw from the same pool.

| Phase | Surface | Model | Notes |
|---|---|---|---|
| Spec, definitions, identification strategy | Project chat | Opus 5, **extended thinking on** | For any choice between defensible options |
| Drafting prose, quick lookups | Project chat | Opus 5, **thinking off** | Don't burn usage on work that doesn't need it |
| Lit review | Deep research | — | 3–4 scoped runs: window duration; deadline-acquisition outcomes; prospect surplus-value methods; forecast-efficiency tests in sports. Verify every citation by hand. |
| Scraping, cleaning, plotting | Claude Code, local | Sonnet 5 | Required — the chat sandbox has no network access to FanGraphs or Baseball Reference |
| Referee pass | Fresh Incognito chat, no project, no memory | Opus 5 | Journal-style referee report plus a steelman of the opposite conclusion |

**Project setup:** Claude Project "Competitive Windows." Knowledge: research-plan.md, predictions.md, data-dictionary.md — re-upload when they change. Instructions: §3 definitions verbatim, plus "flag every embedded assumption" and "when a methodological question closes, output a decisions.md entry in the standard format."

**Usage discipline:** one task per Code session; short CLAUDE.md; have Code write reusable scripts rather than iterating analysis in conversation. Consider Max for one or two months *only* if limits bind during Posts 3–4. Don't buy up front. Skip Cowork — it splits context without adding capability.

---

## 11. Review and distribution

1. **Spec review** (week 2) — 1–2 baseball contacts, on definitions.
2. **Referee pass** — fresh Incognito chat.
3. **Human technical review** — someone who will check the model, not just the prose.
4. **Publish:** personal site as permanent home; FanGraphs Community Research for industry readership; SABR abstract for the room where team staff are.

---

## 12. Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| Horizon-score dating too noisy → P1 untestable | **High** | Go/no-go end of week 4. Fallback: decision-rule framing (§4e), which survives without dating |
| Short panel — 11 seasons cannot estimate hazards for windows beyond ~6 years | **High** | State the censoring limit explicitly; do not extrapolate. Optional descriptive context from realized qualification history (§3.3a) |
| Tradeable surplus not reliably estimable from public data → the reachable frontier is unenforceable | **High** | Go/no-go before Post 4. Documented fallback to the exchange rate alone (§4g) |
| Too few impact players move in a period → empty feasible set | Medium | Report those periods separately as evidence for R1, not as P4 failures |
| Too few window spells for stable hazard estimation | High | Count spells in week 3. If thin, widen the threshold within the pre-registered test range rather than inventing a new one |
| FanGraphs odds methodology revised mid-sample | High | Identify break points; test robustness to excluding pre-break seasons |
| 2020 (60 games) and the 2022 format change sit inside the sample | Medium | Flag 2020 throughout; test with and without it. Keep conclusions structural |
| Circularity — belief and outcome from the same series | High | §4b tests forecast efficiency directly; §3.4 bars outcomes from cohort definitions |
| Payroll confound masquerading as philosophy (R3) | High | Match on payroll tier and revenue; report both |
| Confirmation bias | High | Pre-registration; rule-based selection; adversarial referee pass |
| Surplus-value tables double-count proximity | Medium | Audit before computing YTC |
| Tone reads as adversarial to ops readers | Medium | §1.2 tone rule; network reviewer reads specifically for tone |
| Four postseasons under the current format | Medium | Simulate the 12-team bracket; don't lean on observed outcomes |
| Scope creep across five posts | Medium | Each ships independently; no post starts before the prior is published |
| Project death during data cleaning | Medium | Post 2 is cheap — publish it first if Post 1 stalls |
| Frame B data too weak | Low | Label directional; cap time spent |

---

## 13. Open items

- [ ] Choose a single surplus-value methodology; audit it for proximity double-counting
- [ ] Confirm FanGraphs daily odds are scrapeable, and check site terms before any bulk pull
- [ ] Confirm FanGraphs publishes **within-league** postseason odds, or that team odds can be ranked within league
- [ ] Identify FanGraphs odds-model revision dates across 2016–2026
- [ ] Count window spells under the baseline threshold before committing to the hazard model
- [ ] Confirm 2027 SABR Analytics call and deadline
- [ ] 30-minute check: archived ZiPS multi-year team outlooks (§4f)
- [ ] Define "impact player" for the R1 supply test
- [ ] Fix structural-aggression thresholds and payroll tiers
- [ ] Identify the 1–2 spec reviewers
