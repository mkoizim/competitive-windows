# Competitive Windows in the Current MLB Postseason
## Research Plan v0.29

**Author:** Matt Koizim
**Started:** September 2026
**Soft target:** SABR Analytics Conference abstract, due **Wednesday, November 25, 2026, 11:59 pm MST** (1:59 am ET, Nov 26). Full Post 1 to follow on FanGraphs Community Research.
**Cadence:** 4–8 hrs/week, no hard deadline

**How this document works.** This plan states the study as it currently stands. It does not
record how the design got here. Every choice that has closed — what was considered, what was
rejected, and why — lives in `decisions.md`. Choices still genuinely open are marked
**[OPEN]** where they appear and listed together in §13.

**Version history** (one line each; detail in `decisions.md`)
- v0.29 — Post 1 hazard specified and fit: flow sample primary with L/H bounds; bins 1, 2, 3, 4+; M2 = log duration + era + Opening Day strength + payroll. Baseball-Reference backcast failed its gate. Cot's payroll collected. Deadline table added. 2027 forecasts timestamped (`3fdc139`). Descriptive count of Opening Day underdogs vs. realized qualification (three variants; not a test of P2).
- v0.28 — Window patterns fixed after the first run: next year = next Opening Day rank; gap year and fizzled separated; Out of contention added; patterns renamed by whether the next Opening Day carried them forward; thresholds 3–9. Persistent club-specific forecast error added to P2 (exploratory). Spell count done.
- v0.27 — Corrections from the data audit: 2020 second-place field, 2016 deadline (Aug 1), `data/processed/` never committed.
- v0.26 — Opening Day confirmed as the primary window definition; change between Opening Day and the deadline named as a write-up theme in §3.3b. Surprise patterns renamed. Post 1 reminder reworded.
- v0.25 — Signal switch labeled primary. Reminder to sort by underlying components when judging rationality. Spec reviewers named. FanGraphs data-use email not sent.
- v0.24 — SABR deadline set (Nov 25, 2026, 11:59 pm MST); phase plan replaced with a five-week timeline; FanGraphs added as the full-post venue.
- v0.23 — One-year switch filter set: Pythagorean rank to date inside the threshold at the pre-deadline snapshot.
- v0.22 — Surprise contenders broadened to six window patterns (E4), including the gap year. P1 adds a variant counting one-year signal switches backed by underlying performance.
- v0.21 — Surprise contenders named as a group (E4), with a secondary check on whether the surprise is backed by underlying performance. Behavioral switch now counts a single converting deadline above a size floor; two straight deadlines reported with equal prominence.
- v0.20 — Large off-grid moves listed by name. 2020 reconstruction confirmed. Post 1 reminder to state and defend the threshold rationale.
- v0.19 — Partly reverses v0.18: P3 reporting table withdrawn (left open); revenue-sharing status is a candidate R3 measure, unverified, not adopted. P4 margin stands.
- v0.18 — P4 margin set at 1.0 title-probability point, with the decision rule. P3 reporting table fixed in advance. R3 uses revenue-sharing status plus payroll/CBT position. Ghiroli citation confirmed. Bubble trap parked.
- v0.17 — Farm-rankings study moved to optional, after the luck ledger. Posts renumbered: 1 hazard, 2 putting the roof on, 3 leaving it on the table, 4 luck ledger. Luck ledger becomes the cheap fallback.
- v0.16 — Odds collected (Post 1 now exploratory). P3 downgraded to exploratory. P4 re-specified around the Doyle Number: club-specific willingness to pay vs. market price. R4 cutoff and P1's normative benchmark now use the Doyle Number. Ghiroli (2026) added as framing.
- v0.15 — §1.3 reworded with a worked example of the frames disagreeing. Post 3 commits to naming sustainability as a deliberate trade-off if the evidence supports it; Post 5 adds a long-modest vs. short-tall comparison of expected titles.
- v0.14 — §1.2 reframed: self-assessment failures are correctable process failures, not blameless; the study shows whether a lag exists, not its mechanism.
- v0.13 — Blind-spot review applied. Conversion classified from per-season net surplus (now vs. later), replacing average timing. Offseason signal on Pythagorean standings. P1's primary test moved to the deadline series, with a permutation null, censoring, and a transaction-assignment rule. P2 demoted to an instrument check; editorial series cut. P3 re-specified as a time-varying exposure with core age and control; registration status **[OPEN]**. P4 re-specified against an optimal multi-season objective with a materiality margin **[OPEN]**. Valuation inputs as-of the transaction date.
- v0.12 — History moved out of the spec; snapshot and comparison tables; 2020 reconstruction; P4 in two currencies.
- v0.11 — Withdrew the odds-space offseason delta; lit review split.
- v0.10 — Three snapshots per season; Opening Day treated as outcome; no methodology break assumed.
- v0.9 — Study period 2014–2026; ranking variable and mode fixed; R4 added; format regime handling.
- v0.8 — P4 replaced by under-conversion against a reachable frontier.
- v0.7 — P3 moved to in-window classification; persistent contenders named.
- v0.5–v0.6 — Parameters settled; predictions reconciled.
- v0.1–v0.4 — Initial framing through the mode-switch reframe.

---

## 1. Objective

Test whether MLB organizations switch from **building** competitive odds to **converting** them into championship probability later than public signal justifies — and whether that lag, or an equivalent failure to take the final step, costs them titles.

**Framing.** Writers and fans have long observed that contention windows don't cooperate with
the plans clubs make for them — see Brittany Ghiroli, "Competitive windows don't always
cooperate. MLB teams should act like it.", *The Athletic*, 2026-08-06
(https://www.nytimes.com/athletic/7494251/2026/08/06/mlb-competitive-window-trade-deadline/).
This project puts data behind that observation, and is prepared to find where it doesn't hold.
Several of her claims map onto tests here: secure contenders with improvable title odds who
didn't buy (P4, the Doyle zone); what a club could actually have acquired (R1); whether "just get
in and anything can happen" holds (Post 4).

### 1.1 Why "mode switch" and not "acting late"

Foundation work — development, controllable acquisitions, draft and international investment — is itself a leading decision that raises odds. A club whose odds rise because it developed players has, by construction, acted before the signal. Any prediction phrased as "behavior lags signal" is therefore trivially false.

The real question is when a club stops pouring concrete and puts a roof on. Two modes:

- **Odds-building** — surrender present value for future value. Raises the ceiling.
- **Odds-converting** — surrender future value for present value. Turns ceiling into title probability.

Both are rational. The hypothesis is that the transition between them happens late.

### 1.2 Why the framing targets process, not people

Clubs evaluate rivals from the outside and themselves from the inside, with sunk costs,
internal advocates for players they drafted, private information, and an owner in the room.
Good decision-makers are expected to correct for these, and most try. But knowing about a bias
doesn't remove it, which is why the fix is process (outside review, pre-committed switch
criteria), not individual vigilance. If this study finds a lag, it shows the lag exists, not
which of these mechanisms produced it.

**Tone rule.** Neutral diagnosis, sharp recommendation. Critique decisions and processes, never
named decision-makers. Diagnosis sections stay clinical; the aggressive view belongs in the
recommendation section, after the evidence is established.

### 1.3 The two frames, and how they shape windows

Reported separately. Never blended.

- **Frame A — Championship probability.** Rewards **peak height**. Titles are won at the top of the curve; a short tall window beats a long flat one.
- **Frame B — Owner economics.** Rewards **area under the curve, with diminishing returns**. Gennaro's NPV estimates — roughly $20M for a first berth, $13M for a second consecutive, $9M for a third — mean relevance pays repeatedly but pays less each time. Revenue responds to *reaching* October far more than to winning it.

**Consequence, and the theoretical backbone of P3 and P4:** sustainability is a Frame B strategy defended in Frame A language. The frames give different verdicts on the same club: four wild-card berths and no title is a missed window under Frame A and a success under Frame B. Every result therefore states which frame it is in, and no window is called "missed" without naming the frame.

---

## 2. Pre-registered predictions

Registered in `predictions.md`, locked 2026-09-20 at commit `33dbb7d`, before any data was
collected. Changes to how a prediction is measured are logged in `decisions.md`, each stating
whether it alters the registered claim or only its operationalization.

**What has been seen.** All FanGraphs odds snapshots were collected by 2026-10-17. Analyses that
rest only on the odds — windows and the Post 1 hazard — are therefore **exploratory**: their
specifications were set before the data was collected, but changes made from here are made with
the data in view. Transactions and valuations have not been pulled, so P1's behavioral side and
P4 remain **confirmatory**. The author also lived through the period, as most readers did; the
safeguard is fixing analysis choices before the transaction data is seen, not ignorance of
baseball history.

By 2026-10-26, Baseball-Reference preseason odds and Cot's payrolls (both 2011–2026) had also been
collected, and the Post 1 hazard had been fit with its results seen. On 2026-10-31 to 11-01,
Opening Day Make Playoffs odds were set against realized qualification for a descriptive count of
Opening Day underdogs (three variants, logged in `decisions.md`). That pairing is P2's dataset. The
count is not a test of P2, but P2's data has now been looked at in this form, and readers should
know it. Transactions have still not been pulled.

### Registered

| # | Prediction | Operational test | Falsified if |
|---|---|---|---|
| **P1** | **(Spine)** Clubs switch from building to converting later than public signal justifies | Lag, in seasons, between the public-signal switch and the behavioral switch on the **deadline series** (§3.2), tested against a permutation null, with censoring (§4a). Full decision-grid version secondary | Behavioral switch leads or is contemporaneous with public signal |
| **P2** | **(Instrument check)** Preseason odds over-weight prior-season results | Does prior-season record predict the error in Opening Day Make Playoffs odds? (§4b) | Prior-season record has no predictive power over the error |
| **P4** | Clubs under-convert relative to their standing | At each deadline, the club's Doyle Number (what it should pay for current wins, given its odds) against the market price that deadline; shortfall measured in title probability (§4g) | Mean shortfall is below 1.0 title-probability point, or its 95% interval includes zero (§2.4) |

### Exploratory — no direction claimed

| # | Analysis |
|---|---|
| **E1** | Whether the lag is asymmetric between window openings and closings. Contingent on P1 surviving. |
| **E2** | Realized surplus value of retained top-100 prospects vs. their peak trade-market price. |
| **E3** | Predictive power of organizational farm rank for contention at 2, 3, and 4 years out. |
| **E4** | Window patterns (§3.3b): every club-season classified into seven patterns (surprise or held, each carried forward or not; gap year; fizzled; out of contention); what clubs did at the deadline in each; and whether each rise or dip was backed by underlying performance. |
| **P3 (exploratory)** | Does converting during an open window shorten it? Estimated as a time-varying exposure in a hazard model, with core age and control as controls, and reported with a confidence interval. No pass/fail claim (§3.4). Downgraded from registered 2026-10-17. |

### 2.1 Rival diagnoses — test, don't assume away

P1 attributes the gap to late recognition. Four alternatives can produce the same surface pattern:

| Rival | What it claims | Test |
|---|---|---|
| **R1 — Supply constraint** | Timing was right; no workable deal existed | Was an impact player acquired by *someone* that period, at a price this club could have paid? Per-club counterfactual, holding other clubs' behavior fixed (§4d) |
| **R2 — Final-step under-investment** | Timing was right; the club converted, but never enough | P4's shortfall (§4g) |
| **R3 — Payroll, not philosophy** | Clubs are "sustainable" because they're poor | Control for revenue position and payroll/CBT position; report with and without (§4d) |
| **R4 — Rational non-conversion** | Timing was right and supply existed, but the marginal title probability purchasable did not justify the price. *"We can qualify; we can't be a favorite."* | Non-conversion is explained by R4 when the club's Doyle Number was below the market price that deadline — buying wasn't worth it at the going rate (§4d) |

R4 and P4 both rest on the Doyle Number (Silver & Paine, FiveThirtyEight, 2015 on): optimal
buyers are secure playoff teams with improvable title odds, not bubble teams. Some measured lag
may be optimal behavior. R4 is the test of that.

A further candidate, **persistent club-specific forecast error**, can mimic a lag: if the public
signal is consistently wrong about a club and the club knows it, ignoring the signal is rational.
Tested in §4b (exploratory).

R2 may turn out to be the dominant failure mode. That would be a better finding than R1 and is
reported as such, not buried.

### 2.2 How windows are manufactured

Reported in Post 1: *window openings are preceded by net transaction-channel building in X%
of cases.* The measure sees trades only, not internal development — which is how most windows
open — so it describes the transaction channel, not window formation as a whole. Where the
value build allows, contrast it with growth in internally developed WAR.

### 2.3 Persistent contenders

**Result (2026-10-26):** one club, LAD, was in a window every season 2014–2026. Its spell was
open in 2014, so it is outside the primary (flow) sample and enters only the L and H bounds
(§3.3a). Persistent contenders contribute little to hazard estimation while having the most
conversion capacity in the sample.

They are reported as a named category with a count: *in thirteen seasons, N clubs never left
contention; the hazard describes the remainder.* The count is itself a finding.

### 2.4 Falsification and reporting

**P1.** If the behavioral switch tracks or leads the public-signal switch, there is no blind
spot. The series becomes a descriptive study of window duration — still publishable, headline
claim gone. Say so plainly.

**The threshold favors P1, and the paper says so.** A loose threshold fires the signal switch
earlier, which lengthens measured lag. So the rank-6 baseline biases P1 toward confirmation,
even though it biases Post 1's hazard the other way. P1 is therefore reported at ranks 3 and 4
with the same prominence as rank 6.

**So would requiring two converting deadlines.** A club with a one-year window that pushes its
chips in once could never show two straight converting deadlines, and would be recorded as never
converting — which counts as late. The primary rule therefore counts a single converting deadline
(*k* = 1, above a size floor); *k* = 2 is reported with equal prominence.

**P3.** Exploratory. The effect is estimated and reported with a confidence interval; the
study does not claim to confirm or reject it (§3.4). **[OPEN]:** whether to fix the wording of
each possible result in advance.

**P4.** Margin: **1.0 title-probability point** per club-deadline in which buying was favorable —
roughly the title odds one impact deadline acquisition adds (Ball; citation to verify). Anchored
there because it is a miss a GM would recognize: when its standing justified it, the club passed
up about one impact acquisition's worth of title odds.

- **Test:** P4 holds if the mean shortfall is at least 1.0 point **and** its 95% interval excludes
  zero.
- **Reported alongside:** whether the stricter version also holds — the entire 95% interval above
  1.0 point.
- **Falsified** if the mean shortfall is below 1.0 point, or its interval includes zero.

**Frame A.** The discount rate is not assumed. The study reports the **break-even rate** — the
rate at which converting and building have equal expected value — so the finding reads
"converting wins for any club whose required return exceeds X%." 8%, 10% and 12% are shown as
reference points; 10% is the reference rate wherever one rate is needed.

**Every robustness variant pre-specified in this plan is reported.** No variant is selected
after results are seen.

### 2.5 Author bias

Most predictions point the same direction. Prior employment with LAD, MIA, BAL — three obvious case studies. Two rules, stated in the published piece:

- Case selection by pre-registered rule, with outcomes unexamined at the time of selection.
- **No non-public knowledge from inside those organizations appears anywhere in the evidence.** Insider judgment is an asset in the recommendation section and a liability in the evidence section. Keep the wall visible to the reader.

### 2.6 2027 window forecasts

`docs/forecasts-2027.md`, locked at `3fdc139` (2026-10-26): the probability that each of the 12
windows open on 2026 Opening Day is closed on 2027 Opening Day, from M2 in the flow sample (§5).
Scored by Brier score against a constant 0.294, with log loss alongside; void if no 2027 regular
season starts by December 31, 2027. A single-season check, not a validation. The file is never
edited; scoring is logged in `decisions.md`.

---

## 3. Definitions

These are the study's fixed definitions. Each was chosen over defensible alternatives; the
alternatives and the reasons are in `decisions.md`. Choices still open are marked **[OPEN]**.

### 3.1 Value measures

#### Production value and surplus value

For every asset, project its **production value** by future season: projected WAR × $/WAR for
that season. **Surplus value** in a season is production value minus what the club pays for it.
Surplus can be negative in any season (arbitration raises, underwater contract years).

No published table supplies these per player, per season, across 2014–2026. They are
**built**, from components:

- **Major leaguers:** a projection available at the time of the transaction, extended to later
  seasons by a pre-specified aging curve.
- **Prospects:** contemporaneous prospect grades (Baseball America, owned) mapped to dollar
  values through one published grade-to-value table.
- **$/WAR:** one published series, by year, cited.
- **Salary:** contract and arbitration data from Cot's Contracts.

**As-of rule.** Every player-specific input — projections, grades, health, contract status — is
taken as it stood on the transaction date. Generic mapping tables (grade to dollars, $/WAR) are
fixed and cited. The aging curve is chosen and logged in `decisions.md` before any valuation is
computed. **[OPEN]:** projection source, aging curve, grade-to-value table, $/WAR series.

This is the largest single build in the project.

#### What each decision point is measured by

For each club at each decision point, sum surplus across everything acquired and everything
surrendered, season by season. Three numbers result:

| Measure | Definition | Question it answers |
|---|---|---|
| **ΔS_now** | Net surplus change in the current season (t = 0) | Did the club gain value this season? |
| **ΔS_later** | Net surplus change summed over later seasons (t ≥ 1), undiscounted | Did the club gain or give up future value? |
| **Total value moved** | Production value acquired + production value surrendered | How big was the activity? |

Net surplus value — the price question, "did they win the deal?" — is ΔS_now + ΔS_later.

#### Classifying a decision point

| | ΔS_later < 0 (gave up future) | ΔS_later > 0 (gained future) |
|---|---|---|
| **ΔS_now > 0** (gained now) | **Converting** | **Net acquisition** |
| **ΔS_now < 0** (gave up now) | **Net subtraction** | **Building** |

This matches the definition in §1.1 exactly: converting means surrendering future value for
present value.

**Link to the registered language.** `predictions.md` defines the behavioral switch as the
point where the "net horizon shift turns negative." A decision point classified **converting**
is what that phrase now means.

**Variants:** "now" as t ≤ 1 instead of t = 0; and a looser *present-oriented* classification in
which any period with ΔS_now > 0 counts.

**[OPEN] — Free agency.** A signing at market price adds roughly zero surplus by construction,
so this measure cannot see payroll-funded conversion, one of the two main conversion channels.
It needs its own measure — for example, current-season payroll added relative to the club's
prior level. Options: trade channel only, stated as a scope limit; a parallel payroll-channel
measure; or treat draft picks surrendered under qualifying-offer rules as the surrendered side.
Resolve before Post 2. The deadline test is largely unaffected, since free agency is effectively
closed then.

**[OPEN] — Non-classified periods.** A decision point with trivial activity should not define a
mode. Needs a minimum total value moved for a period to count, and a rule for how net
acquisition, net subtraction and inactive periods are treated in a *k*-run (break it, or skip).
Resolve before Post 2 and before any transaction data is examined.

### 3.2 Time, snapshots, and dating

#### Two units of time

| Unit | What it is | Used for |
|---|---|---|
| **Season** | One regular season | Windows. A window is a run of consecutive seasons above threshold |
| **Decision point** | The offseason, or the trade deadline — two per year | Behavior, signal, and the lag. The only times a club can add outside talent |

#### Three snapshots per season

| Snapshot | Date rule | What it establishes | Confirmed by |
|---|---|---|---|
| **Opening Day (OD)** | First archived date of the season, from the page's own date list | Ex-ante position: is the club in a window this season? | 15 clubs per league; Make Playoffs sums to the season's berth count; any gap between first archived date and actual Opening Day logged |
| **Pre-deadline (PD)** | Archived date nearest to 7 days before the deadline | What was publicly visible when the club had to decide | Date falls before the deadline; Make Playoffs sums to berth count |
| **End of season (EOS)** | Last archived regular-season date | What actually happened: final record, realized qualification | Clubs at 100% Make Playoffs match the actual postseason field; final W-L matches Baseball-Reference |

**Deadline dates:** July 31 (2014–2015, 2017–2019, 2025); Aug 1 (2016 — July 31 was a Sunday); Aug 31 (2020);
July 30 (2021, 2024); Aug 1 (2023); Aug 1 or 2 (2022 — sources conflict by one day, immaterial); Aug 3 (2026).

#### Which transactions belong to which decision point

| Decision point | Window | Notes |
|---|---|---|
| **Offseason** | Day after the World Series through the day before Opening Day | |
| **Deadline — primary** | PD snapshot date through the deadline, **plus** the August revocable-waiver trade period (Aug 1–31) in 2014–2018 | August waiver deals were part of the deadline market until 2019 |
| **Deadline — variant** | June 1 through the deadline (plus August 2014–2018) | Moves before PD are compared against a signal measured after them; flagged as signal-contaminated |
| **Off-grid** | Opening Day to the start of the deadline window; September onward | Excluded from classification. Share of total value moved off-grid is reported. **Large off-grid moves are listed by name** — any single move above a value threshold — so that significant conversions outside both windows (e.g. the June 2019 Kimbrel and Keuchel signings) are visible in the write-up even though they are not classified. **[OPEN]:** the threshold |

If more than a quarter of each season's deadline-market value moves before the PD snapshot,
the PD date is revisited and the change logged.

#### What gets compared to what

| Compare | Against | Question | Feeds |
|---|---|---|---|
| OD rank, season S | Threshold | Is the club in a window in S? | Windows, hazard (Post 1), P3 |
| OD Make Playoffs, S | Realized qualification, S | Did the preseason odds lean too hard on last season? | P2 (primary) |
| OD projected W%, S | Final W%, S | Same question, continuous version | P2 (secondary) |
| PD rank, S | Threshold | At the deadline, did public information say "contender"? | P1 — primary signal |
| Pythagorean standings rank, S−1 | Threshold | Going into the winter, did public information say "contender"? | P1 — secondary (offseason) signal |
| Signal switch | Behavioral switch | Did behavior lag the signal? | P1 |
| OD, S | PD, S | How far did the outlook move in-season, and was it luck or information? | §4c |
| Win WS at OD, PD, EOS | Each other | Does title equity separate once the field is set? | R4 probe |
| OD, S | OD, S−1 | Change in ex-ante position year over year | Descriptive covariate only — not a measure of what the offseason achieved |

**Opening Day does two jobs at different points in the chain.** As a level, it is the club's
ex-ante position entering the season. As the first snapshot after the winter, it already
contains the offseason's moves — which is why it can never be the signal the offseason decision
was made against.

#### The signal at each decision point

- **Deadline:** the club's within-league rank by **Make Playoffs at the pre-deadline snapshot**.
- **Offseason:** the club's within-league rank in **Pythagorean standings** (run differential)
  at the prior season's close. Raw-record rank and BaseRuns rank are reported as variants.
  Run differential is used because raw record carries more luck — the very thing P2 tests
  whether forecasters over-weight. End-of-season *odds* are uninformative (every club at 0% or
  100%), so standings are used at this one point.

#### Switch dating

**Primary test — the deadline series.** Both signal and behavior are read at deadlines only, so
each is measured on one instrument throughout.

- **Behavioral switch:** the first deadline classified converting, provided the move clears a
  minimum size (*k* = 1). A club that converts is changing behavior whatever it does at the next
  deadline. **[OPEN]:** the size floor. *k* = 2 (two straight converting deadlines) is reported
  with equal prominence; *k* = 3 as a variant.
- **Public-signal switch (primary):** the first deadline at which PD rank crosses the threshold and stays
  crossed at the next deadline. Dated at the first crossing.
- **Variant — one-year switches.** Also counts a crossing that does not hold at the next deadline,
  provided underlying performance supports the club's rank at that deadline. This brings one-season
  windows (§3.3b) into P1: a club whose window lasted one season and never converted is recorded as
  not having acted before the window closed. The filter keeps out hot-streak flukes, for which not
  buying may have been correct. **Filter:** the club's within-league rank by Pythagorean
  (run-differential) record to date at the pre-deadline snapshot is also inside the threshold —
  the same threshold used for the signal, so it moves with the threshold variants. Reported
  alongside the primary test.
- **Lag:** in seasons. Less than one season is contemporaneous.

**Secondary test — the full decision grid.** Offseason and deadline together, with each
crossing confirmed **within its own instrument**: an offseason crossing by the next offseason,
a deadline crossing by the next deadline. The switch is the earliest confirmed crossing.

Both switches are dated at the **start of the run that later confirms them**. Confirmation
rules decide whether a switch was real; they never decide when it happened.

**Robustness:** a changepoint model on the classification series as a second dating method.
Disagreement is a finding about transition noise.

### 3.3 Windows

- **Window (observed):** a season in which the club ranks in the **top 6 of 15 within its
  league** by Opening Day Make Playoffs odds. Tested at 3, 4, 5, 7, 8, 9.
- **Why within league.** The postseason field is set inside each league. Ranking across all
  30 would import inter-league parity differences into a measure that has nothing to do
  with them.
- **Why a loose baseline, and what it costs.** A club just outside the top tercile is within
  striking distance and could reasonably convert its way into contention. For Post 1, a looser
  threshold produces longer windows and a flatter hazard, which works *against* the thesis.
  For P1 it does the opposite — it fires the signal earlier and lengthens measured lag — so P1
  is reported at ranks 3 and 4 with equal prominence (§2.4).
- **Ranking variable:** Make Playoffs, League view, `fg` projection mode. Ties broken by
  projected wins, then run differential.
- **Why Make Playoffs and not Win WS.** Make Playoffs is the entry condition; Win WS is the
  outcome P4 measures. Defining windows by title probability would exclude clubs that reached
  October without becoming favorites — hiding the failure the study is about.
- **Division path is priced in.** Simulated playoff odds already account for division strength.
- **Two measures, two jobs.** Contention is within-league (postseason access). Title
  probability is cross-league. Post 1 uses access; Frame A and P4 use title probability.
- **Covariates captured alongside:** Win WS; Clinch Bye from 2022; the gap between Make
  Playoffs rank and Win WS rank (R4).
- **Window length:** strictly consecutive qualifying seasons. A one-year window is a window of
  length 1. A one-season-dip grace rule runs as a robustness variant.
- **Short windows** get a descriptive section, not a category.
- **Hazard:** *given a club has been a contender for n consecutive seasons, the probability it
  stops being one in season n+1.*
- **Contention** is ex-ante position, not "made the playoffs." Berths are outcomes.

### 3.3a Study period and playoff formats

**2014–2026.** The FanGraphs playoff-odds archive begins 2014-03-29. Schema is identical across
the period, 30 clubs every year, no membership required.

**Four playoff formats sit inside the sample:** 10 berths 2014–2019, 16 in 2020, 10 in 2021,
12 from 2022. Handled three ways:

1. **Format regime as a covariate** in the hazard model. Whether the hazard shifted in 2022 is
   itself an output.
2. **Berth-relative threshold** as a robustness variant — rank equal to berths per league:
   5 (2014–2019, 2021), 8 (2020), 6 (2022 on).
   In Post 1 it is reported with equal prominence alongside the fixed rank-6 baseline (decided
   2026-11-01, before its results were seen).
3. **Era-stratified fitting** as a secondary check where power allows.

**2020.** The Make Playoffs column on 2020 pages prices the old 10-team field. The correct 2020
postseason probability is reconstructed as **Win Div + Win Div 2nd place + Clinch Wild Card**
(second place comes from its own field, `win_div_2nd`; the Clinch Bye field is blank in 2020). Used for 2020 in both
rank-based and level-based analysis, **provided it sums to 8 per league** at each 2020
snapshot. The author confirmed the 2020 data on 2026-10-18. 2020 stays flagged throughout for the 60-game season.

**Censoring.** Thirteen seasons cannot estimate the hazard for windows longer than roughly seven
years. The paper states the limit rather than extrapolating past it.

**Left censoring.** The 12 spells open in 2014 have unknown start years. The primary (flow) sample
drops them. Two bounds include them, entering at duration 1 (L) or at the top bin (H). A backcast
of their start years from Baseball-Reference preseason odds failed its validation gate (77%
agreement against 85% required) and is not used.

**Optional descriptive context.** Realized postseason qualification going back decades is
available from Retrosheet or Baseball-Reference — an outcome, not ex-ante, so it cannot carry
the hazard model, but it can bound the question in a labeled section.

### 3.3b Window patterns

**Why.** Windows are defined on Opening Day, and P1's primary signal requires a crossing to hold
at the next deadline. Short and irregular windows — the stars-align case, a contender's down year
— can fall through both rules. Windows stay defined on Opening Day (the cleaner measure of a
club's starting position); this section is where the study shows **how contention changes
between Opening Day and the deadline** — a planned theme of the write-up. It classifies every
club-season so none are lost, and
asks what clubs did in each pattern.

**Classification.** Each club-season is placed by three readings against threshold *k*: Opening
Day rank, pre-deadline rank, and the **next season's Opening Day rank** (consistent with windows
being defined on Opening Day). Baseline *k* = 6; reported at every *k* from 3 to 9.

| Pattern | Opening Day | Deadline | Next Opening Day | Plain description |
|---|---|---|---|---|
| **Surprise, not carried forward** | Below | Above | Below | Contention arrived unexpectedly; the next projection didn't believe it |
| **Surprise, carried forward** | Below | Above | Above | Contention arrived unexpectedly; the next projection kept the club above the line |
| **Held, not carried forward** | Above | Above | Below | An expected contender held through the deadline but started next season below the line |
| **Held, carried forward** | Above | Above | Above | The ordinary multi-year window |
| **Gap year** | Above | Below | Above | An expected contender fell out by the deadline and was back above the line next season |
| **Fizzled** | Above | Below | Below | An expected contender fell out by the deadline and stayed below |
| **Out of contention** | Below | Below | either | Below the line at both readings |

Labels describe a **club-season**, not a club: the names refer to what the next Opening Day
projection did, not to the club's whole history. A club's history is its sequence of labels. For
2026, next season is unknown, and club-seasons get partial labels from Opening Day and the deadline
only, reported separately.

The two surprise patterns together are the **surprise contenders**: below the line on Opening Day,
above it at the deadline.

**First run (2026-10-24, 2014–2025, k = 6).** About a third of contention changes hands between
Opening Day and the deadline: 46 of 144 Opening Day contenders fell below the line by the deadline,
and 46 clubs rose to replace them (the two counts are equal by construction; the size is the
finding). About half of each group was carried forward by the next Opening Day projection (24 of
46 surprises; 21 of 46 fallers, the gap years). This turnover is the motivating fact for the
Opening Day-to-deadline theme. Counts are stable between *k* = 6 and 7.

**Not used:** comparing label sequences against a within-season shuffle. Adjacent labels share next
season's Opening Day rank, so some sequences are impossible by definition and that null is
invalid. Club-level persistence is tested on signed forecast error instead (§4b).

**What is asked of each pattern (E4, exploratory):**
- **Behavior at the deadline:** Did surprise contenders push their chips in, or
  wait for proof? Did fizzled clubs sell? Did gap-year clubs sell off in the down year, or hold?
  Compared with sustained contenders at similar pre-deadline odds.
- **Against standing:** P4's Doyle comparison applies unchanged. The Doyle Number does not depend
  on whether a window was planned.
- **Was it luck?** Using the §4c split, how much of each rise or dip is explained by record to date
  (largely luck) vs. underlying performance (run differential, peripherals). Do clubs respond
  differently to changes the underlying numbers support?
- **Gap years and the window definition:** the strict rule splits a gap year into two windows; the
  grace rule merges them. Describing the pattern directly shows what actually happened in those
  seasons, alongside both rules.

**Status.** Classification uses only the odds, so it is exploratory. Labels were reviewed after
the first run against triggers set beforehand, and kept. The behavior side needs trades,
which have not been seen. Reported in Post 2, with the Doyle comparison in Post 3.

### 3.4 Conversion as an exposure

**Three uses of the classification series. They must not be confused.**

| | Measures | Built from | Feeds |
|---|---|---|---|
| **Switch dating** | When the club changed mode | Classification at each decision point | P1 |
| **Conversion exposure** | How much the club has converted since its window opened | Cumulative future surplus surrendered in converting periods (−ΔS_later), from window open through the deadline of season n | P3 |
| **Prior profile** | How the club arrived at the window | Classifications over the three years before it opened | Descriptive only (§2.2) |

**P3 is a time-varying exposure, not a window-level label.** Conversion exposure through season
n predicts window exit at n+1 in a discrete-time hazard model. A one-season-lagged exposure and
a count of converting decision points run as variants. This uses only behavior that happened
before the outcome it predicts. Labeling a whole window by its average behavior would not:
longer windows contribute more periods, and short windows over-weight a final-season sell-off,
which reads as building.

**Converting does mechanically trade later odds for current odds.** That is what converting
means. P3 is therefore a question of magnitude: does converting shorten windows by enough to
matter?

**Controls:**
- **Core age and remaining team control** — the age and control years of the top 10
  contributors by projected WAR, as of Opening Day. This is P3's main confound: clubs convert
  *because* they can see the core aging and control running out, so converter windows would be
  shorter even if converting had no effect. The inputs come from the value build.
- **Payroll tier, a revenue measure and ex-ante strength** (R3).

**Why P3 is exploratory.** P3 predicts *no* effect. With roughly 40–70 spells, minus persistent
contenders, a real shortening effect would usually go undetected, so a pass/fail version would
"pass" by default. It is estimated in full and written up — its themes are central to Post 2 —
but reported as an estimate with a confidence interval, not a verdict.

**Window level, not club level.** A club can arrive at its 2017 window by building and its 2023
window by converting. Two observations, not a contradiction.

**Hard rule:** no classification or exposure uses outcomes. Window length and peak title
probability never enter any classification.

### 3.5 Structural aggression

Accepting knowingly underwater contract tail years to buy present CBT relief. Applies only to
clubs near the threshold — stratified by payroll tier. Tracked alongside the conversion
measures, not inside them.

### 3.6 Explicitly rejected

- **Buy/sell binary.** Selling is buying for the future. Allocation is continuous.
- **Contract length as a duration signal.** Long deals are often AAV instruments for CBT
  purposes with tail years known to be underwater.
- **Cost-side-only measurement.** Both sides of a move are needed.
- **A single dollar-years composite.** Multiplying value by timing lets the bigger side of a
  trade dominate the sign.
- **Average timing of value moved as the conversion classifier.** Comparing when, on average,
  acquired and surrendered value arrives measures the *composition* of a trade, not whether the
  club gave up future value. A club that trades a small prospect for a large controllable star
  gains value in every season, yet average timing would label it converting.

---

## 4. Measurement

### 4a. P1 — the mode-switch lag

**Inputs:**

| Input | Source | Status |
|---|---|---|
| Deadline signal | Pre-deadline snapshots | Collecting |
| Offseason signal | Runs scored and allowed, Baseball-Reference (Pythagorean) | Not started — trivial |
| Trades, both sides, by decision point | Retrosheet / Baseball-Reference transactions | Not started |
| Surplus by season, per asset, as-of | The value build (§3.1) | Not started — largest task in the project |
| Free-agent signings | Cot's / Baseball-Reference | Not started; treatment **[OPEN]** |
| Payroll and CBT position at each decision point | Cot's | Not started — also needed for P4 |

**Procedure.** Classify every club-decision point (§3.1). Date signal and behavioral switches on
the deadline series (primary) and the full grid (secondary) (§3.2).

**Lag as time-to-event.** For each window opening, the lag is the time from signal switch to
behavioral switch. A club that opens a window and never converts before the window closes or
the panel ends is **right-censored** — not dropped. These are the strongest evidence for P1,
and dropping them would bias the test toward the null. Windows already open at the start of
2014 are **left-censored** and reported separately.

**Null distribution by permutation.** Under the null of no relationship, the lag distribution
depends on how often clubs convert and how often they cross the threshold — not on a 50/50
coin. The null is built by shuffling behavioral series across clubs within era and recomputing
lags. The observed lag distribution is compared against it.

**Resolution limit, stated in advance.** Lag on the deadline series is measured in whole
seasons. A true lag shorter than one season is undetectable by design. If P1 comes back null,
the paper distinguishes "no lag" from "lag below resolution."

**Collect for P4 at the same time.** When transactions are pulled, capture both sides of every
deal and the club's payroll position. Same pull, and exactly what P4 needs.

### 4b. P2 — instrument check

**Purpose.** P1 measures behavior against FanGraphs odds. If those odds lean too hard on last
season, the public signal is itself slow to register a closing window, and P1 would understate
the lag at closings. P2 checks whether the ruler is biased.

**Prior work.** The behavioral finding is established: Woodland (2016) for MLB win-total
betting markets, and Bennett (2019) and the preseason-poll literature in other sports. P2 is
not presented as new. Its contribution is narrower: whether *model-based published playoff
odds* show the same bias. Reported in Post 2's appendix.

**Primary test.** Realized qualification on Opening Day Make Playoffs odds, with prior-season
record added, using Franses's logit-based bias test for binary outcomes (*Applied Economics
Letters* 28(15), 2021). The standard Mincer–Zarnowitz Wald test is oversized for binary
outcomes. This tests the registered object — preseason odds — directly.

**Secondary test.** Final W% on Opening Day projected W%, with prior-season record added, in the
standard Mincer–Zarnowitz form. Same units on both sides; more statistical power.

**Inference.** Outcomes within a season are dependent: berths are fixed, and league-wide shocks
are shared. Standard errors are clustered by season, with a wild-cluster bootstrap given only
thirteen clusters.

**Model changes are tested, not enumerated.** The persistence coefficient is estimated year by
year and inspected for a discontinuity. If a jump appears, the test splits at it, the hazard
model carries a regime indicator as a time-varying covariate, and no seasons are dropped.

**Editorial tiers are not used.** The second belief series is cut.

**Persistent club-specific forecast error (exploratory).** A forecast can be unbiased across the
league and still be biased for particular clubs. For each club-season, take the signed error:
Opening Day projected wins minus actual wins. Test (a) whether clubs have a
persistent average error and (b) whether one season's error predicts the next, each against a
permutation null. Why it matters: a club the projections consistently underrate, that knows it,
is rational to ignore the public signal; P1 would score it as lagging when it isn't. It is
therefore also a rival to P1 (§2.1). Same data as the secondary test; no direction claimed.

### 4c. In-season revisions — decompose before interpreting

The move from Opening Day to pre-deadline odds may be information, or a lucky first half.
Decompose each revision into:

- The part explained by **record to date** — largely noise.
- The part explained by **underlying components** — run differential, peripherals, health,
  playing time.

Only the component-driven part counts as evidence the signal existed. What matters is whether
the information was *knowable then*, not whether the outcome later validated it.

### 4d. Rival diagnoses

- **R1 (supply):** per decision point, count impact players actually moved and their price. If
  a club near the threshold didn't move while comparable talent changed hands at a price it
  could have paid, supply wasn't binding for it. Framed per club, holding others' behavior
  fixed. **[OPEN]:** definition of "impact player."
- **R2 (final step):** P4's shortfall (§4g).
- **R3 (payroll):** controlled throughout, with results reported with and without. Two parts:
  **revenue position** and **capacity at the deadline** (payroll and CBT position). A rich club at
  the tax line can be more constrained in July than a poor club with room, so both are needed.
  **[OPEN]:** the revenue measure. Candidate: revenue-sharing payor/payee status as determined by
  the league under the CBA — unverified; the author needs to confirm whether it is publicly
  available by year before it is adopted.
- **R4 (rational non-conversion):** non-conversion at a deadline is explained by R4 when the
  club's Doyle Number was below the market price that deadline (§4g). A club that wasn't
  supposed to buy at the going rate, and didn't, was being rational, not timid.
- **Reminder — sort by underlying components when judging rationality.** When asking whether the
  public signal was supported and whether a club's restraint was rational, group club-deadlines by
  underlying performance (run differential, peripherals), not only by playoff odds. A club with
  high odds but poor underlying numbers may be rationally holding back. Applies to P1, R4, P4 and
  the window patterns (§3.3b). How exactly to build the grouping is to be worked out before
  analysis.

### 4e. Front-office convergence and the fallback thesis

Clubs run better versions of the same machinery. For single-season assessment, public odds are
a defensible proxy for front-office belief, with two caveats: clubs are systematically more
optimistic about their own players, concentrated at the margin; and single-season agreement
implies nothing about multi-year agreement.

**The threshold is a proxy, not an optimum.** "Later than public signal justifies" uses a
threshold crossing as the benchmark. It does not claim the crossing is the optimal moment to
convert. P1 is also reported against a normative benchmark: the first deadline at which the
club's Doyle Number exceeded the market price (§4g).

**Fallback thesis.** If beliefs converge, the claim becomes "teams apply a different decision
rule to the same odds," not "teams miscalculate." Given P1's resolution limit (§4a), this
framing may end up carrying more weight than P1 itself.

### 4f. Speculative

**ZiPS multi-year team outlooks.** If consistent archived team-level multi-year forecasts
exist, they are a directly contemporaneous duration instrument. Unverified — 30 minutes, no
more.

### 4g. P4 — conversion relative to standing (the Doyle Number)

**The idea.** A club's standing determines how much a win this season is worth to it. A secure
contender with improvable title odds gains a lot from one more win; a long shot or a bubble team
gains little. So each club, at each deadline, has its own price it should be willing to pay for
current wins. Under-conversion is a club whose standing said "buy" at a time when the market was
selling below that price, and that didn't buy enough.

**Three quantities per club-deadline:**

| Quantity | What it is | Built from |
|---|---|---|
| **Doyle Number (D)** | Future WAR the club should give up for one WAR this season, given its standing | Marginal title probability of one added win now (from the club's odds and a simulated bracket), divided by the title probability one future WAR buys on average, discounted at the 10% reference rate |
| **Market price (M)** | Future WAR clubs actually gave up per current-season WAR acquired, that deadline | Trades that actually happened, both sides, valued in WAR as of the trade date |
| **Actual conversion** | Current-season WAR the club acquired, net | The club's own deadline trades |

**Classifying each club-deadline:**
- **D > M — buying was favorable.** The club should have acquired current WAR until its
  marginal D fell to M, subject to its tradeable future WAR and payroll and CBT capacity.
- **D ≤ M — buying was not favorable.** Not buying is rational (R4).

**The measure.** For favorable club-deadlines: shortfall = title probability the club would have
added by buying up to that point − title probability it actually added. For unfavorable ones, a
club that bought anyway has a negative shortfall (over-conversion). Both directions are reported.

**Why this replaces the full feasible-set optimization.** It is normative — it says what a club
should have done given its odds — and much cheaper. It needs WAR projections and control years,
not dollar valuations, so $/WAR drops out of P4 entirely. It also makes R4 concrete and gives P1 a
normative benchmark. Its limit is that D measures willingness to pay, not supply; the market price
M carries the supply check (R1): if no comparable player moved, M is undefined and that
club-deadline is reported under R1.

**Per-club counterfactual.** Each club's shortfall holds other clubs' behavior fixed. Clubs cannot
all buy more at once without moving prices. "Clubs under-convert" is the average of per-club
shortfalls, not a league-wide claim.

**Replication, not borrowing.** The Silver & Paine method is rebuilt from its published
description on FanGraphs odds for 2014–2026, and the replication is checked against their published
numbers for overlapping seasons where possible.

**What prior evidence says about magnitude.** Paine (2025) found net deadline WAR adds no
significant World Series probability once pre-deadline strength is controlled. Ball estimates the
best single acquisitions add roughly one to two points. True shortfalls may be small, which is why
the margin is fixed in advance (§2.4).

**What kills this analysis, stated in advance:** if the mapping from future WAR to future title
probability proves too model-dependent to defend, D is unstable. Report it across the 8–12% range
and the break-even rate; if conclusions flip within that range, say so.

**Two currencies.** Win WS primary; Make Playoffs secondary. The difference shows clubs that could
buy access but not favoritism.

---

## 5. Series structure

Modular. Each post stands alone. Ordered so cheap wins precede expensive work.

**Post 1 — The hazard of contention.** How long windows last and what governs length.
- **Samples (glossary).** All three use the same windows and differ only in the 12 windows already
  open on 2014 Opening Day, whose true age is unknown. **F (flow, primary):** those 12 are left
  out, so every window's age is known. **L (low-age bound):** the 12 are included as if they opened
  in 2014. **H (high-age bound):** the 12 are included as already in their 4th year or later. A
  result that holds in all three doesn't depend on the 2014 assumption.
- Report the **hazard**, not an average. Length is likely bimodal, and an average pools two
  populations and describes neither.
- **Model the full distribution, then illustrate with outliers.**
- **Models (fixed 2026-10-26):** M1 = duration bins 1, 2, 3, 4+. **M2 (primary)** = ln(duration,
  capped at 4) + 12-team era + Opening Day strength (projected wins above the league's 7th-ranked
  club) + Opening Day payroll (log₂ relative to the MLB mean). M2b = M2 with a first-year indicator
  in place of ln duration. Logit, standard errors clustered by club, bins-vs-log likelihood-ratio
  test. **Descriptive:** exact-duration life tables (F, L, H), life tables by entry strength, and
  deadline status vs. closing.
- **Not in the model:** core age and control, committed payroll and farm rank need the value build
  (§7). **Division strength** is left out for the exit budget (it would be a sixth estimated number
  from 30 exits). Window membership already prices the division path, but strength (projected win
  percentage) does not, so a club in a weak division can hold a window with little strength; this
  is stated as a limitation. **Market size** is deferred until after the abstract: it is a capacity
  measure clubs don't choose, to be considered alongside R3's revenue measure (§4d).
- **Write-up notes:** strength is in the model because surviving windows are disproportionately
  strong, so duration is read with strength held fixed. Gap years include temporary setbacks such
  as injuries; a weak first half does not determine the next projection.
- Report an ex-post comparison with Jordan (2018) and Reinhart (2018) to show what the ex-ante
  definition changes.
- This is the SABR abstract. It needs only the odds snapshots.
- **Reminder for the write-up:** state clearly why the threshold is what it is, and defend it.
  Frame the deadline difference between favorites and bubble clubs as **the same goal (titles)
  producing different returns**, not different goals. A favorite's playoff odds are already near
  the ceiling, so any gain shows up in title odds; a bubble club gains a lot of playoff odds and
  little title odds. Note that a bubble club buying its way into October may be making an
  owner-economics decision (Frame B), and that after 2022 favorites also buy for the first-round
  bye, which is about seeding.

**Post 2 — Putting the roof on.** The spine: P1 (§4a), in-season revisions (§4c), rivals R1, R3
and R4 (§4d), P3 (§3.4), and E1. P2 in the appendix. Requires the value build.
- **Sustainability as a deliberate choice.** If the evidence shows sustainability buys many
  postseason chances but no measurable gain in title probability, the post says so directly:
  it is a legitimate choice — Frame B pays for it — but it is a choice to accept many modest
  chances in place of a real shot, and that trade-off should be made knowingly, not defended as
  a championship strategy. If the evidence shows the opposite, that is reported with equal
  prominence.

**Post 3 — Leaving it on the table.** P4 (§4g). Rebuilds the Doyle Number for 2014–2026 on
FanGraphs odds, measures each deadline's market price from actual trades, and compares. Requires
simulating the bracket on historical strengths.

**Post 4 — The luck ledger.** Expected titles (sum of ex-ante title odds) vs. actual, by
organization. Likely the most shareable output; uses only data already collected, so it can be published early if Post 1 stalls.
- **Do many chances add up?** Compare cumulative expected titles (summed Win WS) for long,
  modest windows against short, tall ones. Convexity of title odds predicts the tall windows
  win, but it is an empirical question, and the answer bears directly on the sustainability
  claim in Post 2.

**Optional — Farm rankings as a leading indicator.** Runs E3. Self-contained, uses Baseball
America data already in hand. Scheduled after the luck ledger, if at all.

**Optional — Owner economics.** Frame B. Weak data: Forbes estimates, attendance, and Atlanta
Braves Holdings filings. Directional only.

**Deliverables per post:** essay, technical appendix, public repo. Once Post 2 or 3 lands, a
2-page decision memo with one chart.

---

## 6. Rules fixed before analysis

- **Case selection by rule**, not by interest. If LAD, MIA, or BAL appear, the rule selected them.
- **The bias wall** (§2.5): no non-public knowledge in the evidence sections.
- **No number in any write-up is typed by hand.** Every figure comes from `results.json`.
- **Every pre-specified robustness variant is reported.** None is chosen after results are seen.
- **As-of valuation.** No player-specific information from after a transaction date enters its
  valuation.
- **Endogeneity.** Clubs convert when they believe they're good and when they see the core
  aging. Every conversion comparison controls ex-ante strength, payroll tier, and core age and
  control.
- **No selecting on the dependent variable.**
- **Era caution.** The CBA expires after 2026. Keep conclusions structural.

---

## 7. Phase plan to the SABR abstract

**Deadline:** Wednesday, November 25, 2026, 11:59 pm MST (1:59 am ET, November 26). About five
and a half weeks from October 18, at 4–8 hours a week — roughly 25–45 hours. Post 1 only; it
needs only the odds, which are collected.

| Week | Dates | Goal |
|---|---|---|
| 1 | Oct 19–25 | Clean the odds; build the window table; count spells (go/no-go); classify window patterns |
| 2 | Oct 26–Nov 1 | Done 2026-10-26: hazard model (F/L/H), format era, payroll from Cot's, persistent contenders; 2027 forecasts timestamped |
| 3 | Nov 2–8 | Robustness (thresholds 3–9, grace rule, berth-relative); wild-cluster bootstrap intervals for M2; comparison with Jordan and Reinhart |
| 4 | Nov 9–15 | Draft the abstract; send to one or two reviewers |
| 5 | Nov 16–22 | Revise; referee pass in a fresh chat |
| Buffer | Nov 23–25 | Target submission by November 22; don't rely on Thanksgiving week |

**Deferred until after the abstract:** trades, the value build, the Doyle Number, the re-lock of
`predictions.md`, and Post 1 covariates that need the value build (core age and control, farm rank).
The abstract needs a clean hazard result and an honest description of what follows, not the series.

**FanGraphs.** The full Post 1 goes to FanGraphs Community Research after the abstract.
**[OPEN]:** check whether the SABR call accepts work already published elsewhere; if not, hold the
FanGraphs piece until after the conference or publish a narrower piece first.

Posts 2–4: 25–40 hours each; Post 2 more, because of the value build. Total project:
150–250 hours. **Fallback if November slips:** SABR national convention abstracts run in
February.

---

## 8. Data inventory

| Source | Use | Cost | Notes |
|---|---|---|---|
| FanGraphs playoff odds | Windows (Make Playoffs), Frame A (Win WS), deadline signal, P2 | Free | Archive from 2014-03-29. Collected through a browser session at reading pace, ~40 pages. Raw tables not republished (ToS) |
| Baseball-Reference standings | Final W-L, runs scored and allowed (Pythagorean) at season's end and as of each pre-deadline date, realized postseason field | Free | Offseason signal; one-year switch filter; end-of-season cross-check. Same Sports-Reference terms as the playoff-odds row |
| Retrosheet / Baseball-Reference transactions | Trades by decision point, both sides, including August waiver trades 2014–2018 | Free | Cache once |
| Cot's Contracts | Salary, arbitration, payroll, CBT position | Free | Collected 2011–2026 from club pages. Opening Day payroll used; year-end and CBT kept for R3 and P4. Cot's publishes no Opening Day CBT. 2020 is prorated (see `decisions.md`) |
| Baseball-Reference playoff odds | Preseason odds 2011–2026 | Free | Backcast failed its gate; retained for the P2 benchmark and a robustness check. Collected at under 20 requests/min; raw pages not committed. Sports-Reference's terms bar using content to prompt AI models; the author proceeded knowingly |
| Player projections, as-of | Surplus by season, major leaguers | TBD | Multi-year archives scarce; likely one-year projection plus a pre-specified aging curve |
| Grade-to-value table | Surplus, prospects | Free | One published table, cited |
| $/WAR series by year | Converts WAR to dollars | Free | One series, cited |
| Baseball America Top 100 + org rankings | Contemporaneous prospect grades; farm covariate | Owned | Methodology changes across years |
| Lahman database | Rosters, ages, service proxies | Free | — |
| Preseason World Series futures | Post 4 luck ledger only | Free | Vig removal required |
| Forbes valuations / Braves Holdings filings | Frame B only | Free | Estimates, except Braves |

**Standing rule:** pull once, cache locally, version the cache. `data/raw/` and `data/processed/` are never committed — processed files are close copies of the FanGraphs tables.

---

## 9. Repository layout

```
competitive-windows/
  CLAUDE.md
  docs/
    competitive-windows-research-plan.md   # this file
    predictions.md                         # locked; never edited
    forecasts-2027.md                      # locked at 3fdc139; never edited
    decisions.md                           # dated, append-only log
    data-dictionary.md                     # planned
    lit-notes.md                           # planned
  data/raw/          # cached pulls, never edited, never committed
  data/interim/
  data/processed/    # derived from raw; never committed
  src/scrape/  src/clean/  src/analysis/
  results/figures/  results/tables/
  results/results.json   # every number that appears in prose
  posts/post1-hazard/
  requirements.txt   # pinned packages for hazard.py
  .venv/             # local environment; never committed
```

Two conventions matter more than the structure:

1. **`results.json` is the only source of numbers in writing.**
2. **`decisions.md` gets an entry whenever a methodological question closes**, in the format
   shown at the top of that file.

---

## 10. Claude usage map (Pro plan)

Usage limits are the binding constraint; Code and chat draw from the same pool.

| Phase | Surface | Notes |
|---|---|---|
| Spec, definitions, identification strategy | Project chat, extended thinking on | For any choice between defensible options |
| Drafting prose, quick lookups | Project chat, thinking off | Don't spend usage on work that doesn't need it |
| Lit review | Deep research | Scoped runs only. Verify every citation by hand |
| Odds collection | Claude Code with browser tools | Reading pace, no parallel requests |
| Cleaning, analysis, plotting | Claude Code, local | Reusable scripts, not analysis in conversation |
| Referee pass | Fresh Incognito chat, no project, no memory | Referee report plus a steelman of the opposite conclusion |

**Project:** "MLB Competitive Windows." Knowledge: the plan, `predictions.md`, `decisions.md`,
data dictionary — re-upload when they change.

---

## 11. Review and distribution

1. **Spec review** — former colleagues [reviewer] and [reviewer], possibly others, on definitions.
2. **Referee pass** — fresh Incognito chat.
3. **Human technical review** — someone who will check the model, not just the prose.
4. **Publish:** personal site as permanent home; FanGraphs Community Research; SABR.

---

## 12. Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| Value build (§3.1) is larger than planned; no historical per-asset table exists | **High** | Scope it before Post 2. Start with deadline trades only, where the free-agency gap barely applies |
| Look-ahead bias in valuations | **High** | As-of rule (§3.1); aging curve logged before any valuation is computed |
| Free agency invisible to the surplus measures | **High** | Resolve before Post 2 (§3.1) |
| Lag measured in whole seasons on the primary test | **High** | Stated in advance (§4a); fallback thesis (§4e) survives without dating |
| Loose threshold biases P1 toward confirmation | **High** | P1 reported at ranks 3 and 4 with equal prominence (§2.4) |
| Requiring two converting deadlines biases P1 against short windows | **High** | Single converting deadline (*k* = 1) is primary; *k* = 2 reported with equal prominence (§3.2) |
| Short and irregular windows invisible to window-based analyses | Medium | Window patterns classify every club-season (§3.3b); one-year signal switches enter P1 as a variant (§3.2) |
| P3 underpowered and confounded | **High** | Downgraded to exploratory; time-varying exposure with core age and control |
| Thirteen seasons cannot estimate hazards for windows beyond ~7 years | **High** | State the censoring limit; do not extrapolate |
| Too few window spells | Resolved | 53 spells at baseline (2026-10-20) |
| Few clusters (22 clubs in the primary sample) make clustered standard errors unreliable | Medium | Wild-cluster bootstrap (Week 3) |
| Strength result partly reflects projections agreeing with themselves | Medium | State it in the write-up; the parked Baseball-Reference windows check offers a second instrument |
| Sports-Reference terms (AI clause) | Low | Logged; only derived ranks published; Retrosheet as a fallback |
| Doyle Number unstable because the future-WAR-to-title mapping is model-dependent | **High** | Report across 8–12% and the break-even rate; state if conclusions flip (§4g) |
| Post 1 analyzed with the odds already in view | Medium | Labeled exploratory; any specification change from here logged with date |
| Confirmation bias | **High** | Pre-registration; rule-based selection; all variants reported; adversarial referee pass |
| True P4 shortfalls are small (Paine 2025; Ball) | Medium | Materiality margin fixed in advance; a small shortfall is a valid, reportable result |
| Undetected FanGraphs model change | Medium | Year-by-year persistence coefficient (§4b) |
| 2020 reconstruction fails to sum to 8 per league | Medium | Fall back to rank-only use of 2020 |
| Empty feasible set in thin markets | Medium | Report those periods separately as evidence for R1 |
| Tone reads as adversarial to ops readers | Medium | §1.2: critique process, not named people; a reviewer reads specifically for tone |
| Four postseasons under the current format | Medium | Simulate the 12-team bracket |
| Scope creep across five posts | Medium | Each ships independently |
| Project death during data work | Medium | The luck ledger (Post 4) uses only data already collected — publish it early if Post 1 stalls |
| Frame B data too weak | Low | Label directional; cap time spent |

---

## 13. Open items

**Decide now (registration)**
- [x] P4 margin: 1.0 title-probability point (2026-10-17)
- [ ] Re-lock `predictions.md` before any transaction data is pulled
- [ ] P3: decide whether to fix the wording of each possible result in advance

**Before Post 1**
- [x] Collect the three snapshots per season, 2014–2026 (done by 2026-10-17)
- [x] 2020 reconstruction confirmed by the author (2026-10-18)
- [x] Count window spells under the baseline threshold — Post 1 go/no-go: 53 spells, proceed (2026-10-20)
- [x] Spell counts and window patterns at every threshold *k* = 3–9 (2026-10-24)
- [ ] Probe: Win WS dispersion at OD, PD and EOS (two seasons)
- [x] Spec reviewers identified: [reviewer], [reviewer] (possibly others)
- [x] SABR Analytics abstract deadline: Nov 25, 2026, 11:59 pm MST
- [ ] Check whether the SABR call accepts work published elsewhere first (affects FanGraphs timing)
- [x] Hazard model fit (2026-10-26)
- [x] 2027 forecasts timestamped (`3fdc139`, 2026-10-26)
- [x] Add the closing-rate-by-cushion table to `hazard.py` and `results.json` (2026-11-02)
- [x] Fresh-install test of `requirements.txt`: passed, results reproduced byte for byte (2026-11-02)
- [ ] Wild-cluster bootstrap for M2 (Week 3)
- [ ] Heads-up to [reviewer] and [reviewer] that a draft is coming

**After the abstract**
- [ ] Score the 2027 forecasts on 2027 Opening Day
- [ ] Install a current Python (3.12 or 3.13, from python.org), rebuild `.venv`, and rerun the fresh-install test
- [ ] Second source for the Brewers' 2024 year-end payroll before R3 or P4 use it

**Before Post 2**
- [ ] Value build: projection source, aging curve, grade-to-value table, $/WAR series — logged before any valuation is computed
- [ ] Free-agency treatment (§3.1)
- [ ] Non-classified periods: activity floor, and how net acquisition, net subtraction and inactive periods enter a *k*-run (§3.1)
- [ ] Size floor for a single converting deadline to count as a behavioral switch (§3.2)
- [ ] Define "impact player" for R1
- [ ] Locate the Silver & Paine Doyle Number methodology and their published values for replication checks
- [ ] Verify Ball's "1–2 points per best acquisition" figure and get a full citation (anchors the P4 margin)
- [ ] Confirm public availability of revenue-sharing payor/payee status by year (R3 candidate; not adopted until confirmed)
- [ ] Fix payroll tiers and structural-aggression thresholds
- [ ] 30-minute check: archived ZiPS multi-year team outlooks (§4f)

**Parked ideas — revisit after working with the data**
- [ ] Baseball-Reference preseason ranks (2014–2026) as a P2 benchmark and a windows robustness check.
- [ ] A long-panel version of the windows from Retrosheet game logs, to see longer windows and compare directly with Jordan (2018).
- [ ] Cushion measured in playoff odds rather than projected wins (odds minus the first club out's odds), at baseline, as a response to the division-strength limitation. Odds compress near 100% for strong clubs, which makes it harder to read.
- [ ] **The bubble trap.** At each deadline the Doyle Number correctly tells a bubble team not to buy, so it stays on the bubble and gets the same answer next year: every decision rational, no championship. The way off is a leap big enough to reach secure status in one move, mostly an offseason move, which a one-deadline calculation can't see. Possible tests: bubble persistence from tier-to-tier transitions in the odds (exploratory), and whether bubble clubs that made a big offseason conversion reached secure status more often (needs trades). May also be where offseason under-conversion lives.
