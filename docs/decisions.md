# Decisions Log

Every methodological question that closes gets an entry here, dated. `predictions.md` is
never edited after its first commit; changes of position are recorded here instead.

Entries are append-only. A decision that is later reversed is marked **[SUPERSEDED]** with a
pointer to the entry that replaced it. Nothing is deleted — the record of what was considered
and rejected is part of the method.

Format:

```
## YYYY-MM-DD — Short title
Question:
Options:
Chose:
Why:
Revisit if:
```

---

## 2026-09-20 — Window threshold: within-league, not across all 30

**Question:** How to define whether a club is "in a window" in a given season.
**Options:** Top N of 30 overall | Top N of 15 within league | Absolute title-probability floor
**Chose:** Top 6 of 15 within league, tested at 3, 4, 5, 7, 8, 9.
**Why:** The postseason field is set inside each league — three division winners and three
wild cards per side. Ranking across 30 would import inter-league parity differences into a
measure that has nothing to do with them. Baseline set loose at 6 because a club just
outside the tercile is within striking distance and could reasonably convert to get there;
a loose threshold also lengthens measured windows and flattens the hazard, working against
the thesis rather than for it.
**Revisit if:** FanGraphs does not publish within-league odds and they cannot be reliably
ranked within league from what it does publish.

## 2026-09-20 — Signal measured at decision points, not daily

**Question:** At what frequency to measure the public signal.
**Options:** Daily series with a persistence filter | Two decision points per year
**Chose:** Two per year — prior season's close (for the offseason decision) and ~1 week
before the deadline (for the deadline decision).
**Why:** Clubs can only materially change the roster in two windows. A hot May cannot be
acted on until late July, so daily resolution measures something the club could not use.
Sampling at decision points also removes the noise that parameter *D* existed to filter, so
*D* is retired. Opening Day odds are deliberately not the offseason signal: they already
contain the offseason's moves, so using them would compare behavior against its own
consequence.
**Revisit if:** the deadline-week snapshot proves unavailable for some seasons.

## 2026-09-20 — Both switches dated at start-of-run

**Question:** Whether a switch is dated when it begins or when it is confirmed.
**Options:** At confirmation | At the start of the run that later confirms it
**Chose:** Start of run, for both behavioral and signal switches.
**Why:** *k* requires two decision points (~12 months) while a signal confirmation requires
one. Dating at confirmation would bake a lag of up to a year into the measurement before
any data was examined, making P1 half-true by construction. Confirmation rules decide
whether a switch was real; they must not decide when it happened.
**Revisit if:** never — this is a correctness requirement, not a preference.

## 2026-09-20 — Strict consecutive windows; grace rule demoted

**Question:** How to treat a single season below threshold inside an otherwise open window.
**Options:** One-season grace as default | Strict consecutive as default
**Chose:** Strict consecutive. The grace variant runs as a robustness check.
**Why:** A hazard model exists to handle short spells. Smoothing one-year windows away
deletes the left tail of exactly the distribution Post 1 estimates. A one-year window is a
window of length 1 and needs no special category. Whether such a window was "real" or a
fluke depends on whether it was knowable — which is the thing being measured, so building
it into the definition would be circular.
**Revisit if:** the strict rule fragments windows so severely that spell counts become
unusable.

## 2026-09-20 — Strategy classified at the window level

**Question:** Whether to label a club or a window as builder/converter.
**Options:** Club-level across the sample | Window-level
**Chose:** Window-level — the trailing 3-year mean horizon score as of that window.
**Why:** P1 asserts that clubs switch modes. Labeling a club once for a decade averages
away the exact behavior P1 is about. A club can be a converter in one window and a builder
in the next; that is two observations, not a contradiction.
**Revisit if:** window counts per club prove too small to support the split.

## 2026-09-20 — Break-even discount rate instead of an assumed one

**Question:** What discount rate to apply to future surplus value.
**Options:** Assume 10%, test 8–12% | Report the break-even rate
**Chose:** Report the break-even rate; show 8%, 10%, 12% as reference points.
**Why:** Neither author nor advisor has a principled basis for picking a rate, and the
choice tilts the answer. Inverting the question — "converting wins for any club whose
required return exceeds X%" — produces a number a front office can test against its own
cost of capital rather than an assumption it must accept.
**Revisit if:** break-even proves unstable across threshold specifications.

## 2026-09-20 — The ~2003 futures panel is dropped

**Question:** Whether to extend the study period using de-vigged World Series futures.
**Options:** Two-panel design (futures 2003+, FanGraphs 2016+) | Single panel 2016–2026
**Chose:** Single panel, 2016–2026.
**Why:** Once the threshold moved to within-league postseason access, futures no longer
measure the same construct — they are cross-league title odds. Buying a mismatched variable
at the cost of vig removal, patchy archive coverage, and a second manual pipeline is a bad
trade. Consequence accepted: windows longer than ~6 years are right-censored and their
hazard is not estimable. That limit gets stated, not extrapolated past. Realized
qualification history remains available as clearly labeled descriptive context.
**Revisit if:** spell counts prove too thin and a longer ex-ante series can be found that
expresses within-league postseason access.

## 2026-09-20 — P3 and P4 use different classification windows  **[P4 portion SUPERSEDED same day — P4 no longer uses cohort classification]**

**Question:** Whether builder/converter classification is measured before the window or during it.
**Options:** Prior behavior for both | In-window for both | Split by prediction
**Chose:** P3 in-window, P4 prior.
**Why:** For P4, in-window classification is near-circular — converting during a window *is*
the act of raising title probability, which is P4's outcome. Prior classification keeps cause
and outcome in non-overlapping periods. For P3, the reverse holds: prior classification would
be tested against a cohort that is likely almost all builders, and in-window classification is
not circular because converting does not mechanically lengthen or shorten a window. In-window
also tests the sustainability orthodoxy directly — the industry's stated belief is that
converting shortens windows by depleting the farm.
**Revisit if:** in-window horizon scores prove too sparse inside short windows to classify.

## 2026-09-20 — P4 made conditional on cohort balance  **[SUPERSEDED same day — see "P4 replaced" below]**

**Question:** What to do if window openings are almost all preceded by building, leaving P4
without a comparison group.
**Options:** Register P4 unconditionally | Drop P4 | Register with a pre-specified contingency
**Chose:** Contingency. Count the split first; P4 runs if 70/30 or better, withdraws if worse.
**Why:** The concern is real — windows plausibly follow building most of the time, which would
leave no prior-converter cohort. Discovering that in week 6 would mean either abandoning a
registered prediction or quietly redefining it. Pre-registering a conditional analysis plan is
standard practice; registering a prediction that later proves untestable is not. The split is
reported either way, since how contention gets manufactured is itself a Post 1 result.
**Revisit if:** the 70/30 line proves arbitrary once actual counts are known — but the line is
fixed now precisely so it cannot be moved after seeing them.

## 2026-09-20 — Persistent contenders reported as a named category

**Question:** How to handle clubs that never fall below threshold in the sample.
**Options:** Exclude them | Force them into the hazard model silently | Name them as a category
**Chose:** Retain as right-censored spells in the model, and report them separately with a count.
**Why:** Right-censoring is the statistically correct handling, but these clubs contribute little
to hazard estimation while having the most conversion capacity in the sample. Stating "N clubs
never left contention; the hazard describes the remainder" is more honest than a curve that
quietly excludes the most interesting cases, and the count is a finding in its own right.
**Revisit if:** the persistent-contender count is large enough that the hazard describes only a
minority of clubs, which would require rethinking the threshold.

## 2026-09-20 — P4 replaced: under-conversion against a reachable frontier

**Question:** P4 previously claimed prior building caps the peak, split by builder/converter
cohorts. If windows almost always follow building, that cohort split is nearly empty and the
prediction is untestable. What replaces it?
**Options:** Keep with the 70/30 contingency | Drop P4 | Exchange rate (converting vs. holding)
| Reachable frontier (converting vs. converting more)
**Chose:** Reachable frontier. The exchange rate becomes the intermediate result reported on
the way there.
**Why:** The natural sequence is build, window opens, then the conversion decision arrives — so
the interesting question is not whether builders differ from converters, but whether clubs
convert *enough* once the window is open. The frontier compares each club against its own
feasible set rather than against a cohort, which removes the cohort-balance problem entirely.
It also promotes R2 (final-step under-investment) from a rival diagnosis to a registered
prediction, which is where it belongs given it may be the dominant failure mode.
**Feasible set fixed now:** players who actually changed hands that period, at the prices
actually paid by the acquiring club, capped by the subject club's tradeable surplus and payroll
capacity. Premium bands of +10% and +25% tested as robustness. The author's own valuations are
never substituted for observed prices.
**Revisit if:** tradeable surplus proves unestimable from public data — documented fallback is
the exchange rate alone, logged here if triggered.

## 2026-09-20 — §2.2 cohort contingency retired

**Question:** Does the building-vs-converting split among window openings still gate anything?
**Chose:** No. It becomes a reported descriptive result in Post 1.
**Why:** It existed only to protect the old cohort-based P4. With P4 now measured against a
per-club frontier, no registered prediction depends on cohort balance. The count is still worth
reporting — *windows are preceded by net building in X% of cases* is a clean statement about how
contention gets manufactured, and it sets up Post 3.

## 2026-09-20 — predictions.md re-locked at v0.8

**Question:** `predictions.md` was committed at v0.5 (`2ddb3ac`), then P3 and P4 were revised.
Is re-committing it a violation of pre-registration?
**Options:** Leave the v0.5 version as the registered one | Add v0.8 as a separate file |
Re-commit with an explicit supersession note
**Chose:** Re-commit, with the supersession, the reason, and the superseded hash written into
the file header.
**Why:** Pre-registration requires that predictions precede data, not that a first draft is
never revised. No data had been collected at any point between the two commits, so nothing in
the repository could have influenced the revisions. Git preserves `2ddb3ac` permanently, so the
change is auditable by anyone who wants to diff it — which is a stronger artifact than a
registered document with no visible drafting history. What would compromise the registration is
revising after seeing results, or revising silently. Neither applies.
**Revisit if:** never. From this commit forward the file is fixed; positions change only here.

## 2026-09-21 — Ranking variable, view, and projection mode fixed

**Question:** Which FanGraphs field defines the window threshold, and from which page view
and projection mode.
**Options:** Make Playoffs | Win Division | Win WS | composite — across six projection modes
(fg, ATC, THE BAT X, OOPSY, season-to-date, coin flip) and four views.
**Chose:** **Make Playoffs**, from the **League view**, at the **`fg` default mode**. Ties
broken by projected wins, then by run differential.
**Why:** Make Playoffs is the within-league postseason-access measure §3.3 calls for. Win WS
is cross-league title probability and is reserved for Frame A and P4, per §3.3's
two-measures rule. The League view already groups 15 clubs per league and each record
carries an explicit `league` field, so no manual team-to-league mapping is required. The
mode is fixed now, before any mode's results have been seen, because six modes are six
different answers and leaving the choice open is an undeclared researcher degree of freedom.
**Revisit if:** the `fg` mode proves to have a methodology break that the alternatives do
not — in which case the switch is logged here with the break date, not made silently.

## 2026-09-21 — Study period extended to 2014–2026

**Question:** `predictions.md` fixes the study period at 2016–2026 on the belief that the
FanGraphs archive began at Opening Day 2016. The archive actually begins 2014-03-29.
**Options:** Hold 2016–2026 as registered | Extend to 2014–2026
**Chose:** Extend to 2014–2026. Thirteen seasons.
**Why:** The registered period rested on a factual error about data availability, not on a
methodological judgment. Schema is identical across 2014, 2016, 2020, 2023 and 2026, and
30 clubs appear in every year. Spell count is the binding constraint on Post 1, so two
additional seasons are material. This is a correction made before any data was examined,
not a revision after seeing results. `predictions.md` remains unedited.
**Consequence accepted:** a larger share of the panel now sits in the 10-berth era. See the
berth-count entry below.
**Revisit if:** the 2014–2015 pages prove to differ from later years on inspection.

## 2026-09-21 — Berth-count shift handled as a robustness variant

**Question:** Make Playoffs sums to 10 berths through 2021 and 12 from 2022. "Top 6 of 15"
is therefore one spot outside the field in the early era and exactly the field in the later
one — the same rank meaning two different competitive positions.
**Options:** Keep rank 6 fixed | Move the baseline to berth-relative | Run both
**Chose:** Baseline stays at **rank 6**, as registered. A **berth-relative variant** runs as
a robustness check: top 5 of 15 through 2021, top 6 from 2022.
**Why:** `predictions.md` is locked and registers 6. Both 5 and 6 already sit inside the
pre-registered test range (3, 4, 5, 7, 8, 9), so the variant requires no change to the
registration. The stated rationale for choosing 6 — a club within striking distance that
could reasonably convert its way in — describes the early-era meaning of rank 6, which is
precisely why the variant is worth running rather than assuming away.
**Reported either way:** if baseline and variant disagree, that disagreement is a finding
about how the 2022 format change moved the contention line, and it belongs in Post 1.
**Revisit if:** never as a matter of registration; the baseline is fixed.

## 2026-09-21 — 2020 retained for rank-based analysis, excluded from level-based

**Question:** The 2020 Opening Day odds page (2020-07-23) sums to 10 berths, not 16. The
expanded field was agreed the same day the season opened, so the model had not taken it up.
**Options:** Drop 2020 entirely | Retain fully | Split by how the field is used
**Chose:** Split. 2020 is **retained for rank-based analysis** (window definition, threshold
crossing, hazard) and **excluded from level-based analysis** (title probability for Frame A
and the P4 reachable frontier).
**Why:** The threshold is a within-league rank, and mispriced probability levels do not
change the ordering, so window classification survives. Any use of the probability *level*
does not. 2020 is already flagged throughout for the 60-game season; this adds a second,
independent reason and a sharper rule for when it applies.
**Revisit if:** dates later in the 2020 season show the model corrected to 16 berths, which
would make the mid-season snapshots usable at level. Only 2020-07-23 was checked.

## 2026-09-21 — Collection by hand, not by script

**Question:** How to collect the odds snapshots given FanGraphs' terms of service.
**Options:** Scripted bulk pull | Manual collection through the site interface | Request
permission first
**Chose:** Manual collection, and email FanGraphs regardless.
**Why:** §17 of the terms commits users not to access the service by means other than the
provided interface, which a scripted pull arguably violates. The spec needs roughly 33 page
loads — one preseason snapshot per season for the threshold, plus two decision-point
snapshots per club-season for the signal series — which is an afternoon of manual work and
entirely within the interface. Scripting would buy very little and risk the relationship
with a publication venue the project intends to use. The email is sent anyway: a documented
yes matters if the daily series is ever needed for descriptive work.
**Revisit if:** FanGraphs grants explicit permission for automated access, logged here.

## 2026-09-21 — Threshold stays Make Playoffs; R4 added as a fourth rival diagnosis

**Question:** Should the window threshold rank on Win WS rather than Make Playoffs? A club
may rationally judge that it can reach October but cannot become a favorite, and therefore
not convert — which Make Playoffs cannot see.
**Options:** Make Playoffs | Win WS | composite
**Chose:** **Make Playoffs** stays the threshold. The concern becomes **R4 — rational
non-conversion**, a fourth rival diagnosis.
**Why:** Make Playoffs is the entry condition; Win WS is the outcome P4 measures. Defining
the window by title probability would mean clubs that reached October without becoming
favorites never enter a window — making the exact failure the study is about invisible, and
collapsing P4 into a tautology. Win WS is also skewed and nearly flat across ranks 6–12
(inside model noise), and it is convex in team strength, so it is more contaminated by the
conversion behavior being studied. But the underlying objection is legitimate and needed a
home: R4 says timing was right and supply existed, and converting still wasn't worth it at
the margin. Tested by computing Win WS and marginal Win WS per dollar of available surplus
at each decision point. R4 is a sharper, quantitative version of §4e's decision-rule
fallback — it requires no one's math to be wrong.
**Covariates added:** Win WS, Clinch Bye (post-2022 — the first-round bye is a large title
lever), and the Make Playoffs-to-Win WS rank gap.
**Revisit if:** the rank gap proves to have no variance, which would make R4 untestable.

## 2026-09-21 — Format change handled three ways, not defined away

**Question:** Four playoff formats sit inside the sample — 10 berths 2014–2019, 16 in 2020,
10 in 2021, 12 from 2022. How should the threshold and model absorb this?
**Options:** Fixed rank | Berth-relative rank | Absolute probability floor | Era-stratified
fitting | Format as a model covariate
**Chose:** All three of: fixed rank 6 as the registered baseline; berth-relative rank (5
through 2021, 6 from 2022) as the pre-specified robustness variant; **format regime as a
covariate in the hazard model**.
**Why:** The covariate is the addition that matters — modeling the change asks whether the
hazard itself shifted in 2022, which is a more interesting output than a threshold that
quietly absorbs it. The berth-relative variant keeps the threshold's *meaning* constant
where the fixed rank keeps only its number, and both values already sit inside the
registered test range, so neither requires touching `predictions.md`. Era-stratified fitting
runs as a secondary check where power allows. **An absolute probability floor is rejected:**
it depends on probability levels, which are compromised by both 2020 and the model revision.
**Revisit if:** the regime indicator proves collinear with calendar time to the point of
being unidentifiable.

## 2026-09-21 — Collection by browser session, not by script

**Question:** Revises the earlier manual-collection decision. May a browser-automation tool
drive a real Chrome session instead of copy-paste?
**Chose:** Yes, with rate safeguards — reading pace, no parallel requests, ~35 pages total.
Email FanGraphs regardless.
**Why:** ToS §17 commits users not to access the service by means other than the provided
interface. A tool driving the user's own browser, rendering pages normally at human pace, is
a genuinely unsettled case under that clause; the terms do not distinguish between a person
clicking and an agent clicking in that person's browser. What draws objection in practice is
volume and rate, not mechanism, and ~35 page loads at reading pace is indistinguishable from
browsing. The email converts "probably fine" into "confirmed fine" for the cost of one
message, and opens a relationship with a publication venue the project intends to use.
**Not legal advice.**
**Revisit if:** FanGraphs responds with any restriction, which is logged here and obeyed.

## 2026-09-21 — [OPEN] Probe: does Win WS carry signal at the decision points?

**Question:** Do World Series odds separate meaningfully once the postseason field is
finalized, compared with the two decision points? If Win WS is nearly flat at the deadline,
R4's premise — *we can qualify but can't be a favorite* — is the rational read, and it also
confirms why Win WS is a poor threshold.
**Method:** two seasons, Win WS at (a) prior season's close, (b) ~1 week pre-deadline, (c)
the day after the final regular-season game. Compare dispersion.
**Measurement caution:** post-elimination clubs sit at zero, so raw spread widens
mechanically. Compare dispersion **among qualifying clubs only**, or coefficient of
variation across the top 8 per league.
**Cost:** ~4 page loads. Run it during collection.
**Status:** not yet run. Exploratory diagnostic on instrument choice — not a registered
prediction, and no result from it tests any hypothesis.

## 2026-09-22 — No FanGraphs methodology break assumed; breaks tested empirically instead

**Question:** Is there a forecast-methodology break inside 2014–2026 that §4b must split on?
**Evidence checked:** Strength of schedule is absent through the last day of 2017 and present
from the first day of 2018. On inspection, SOS is interpretive display — projected
neutral-opponent win percentage across a club's remaining opponents — and does not feed the
forecast. Other known changes: playing-time inputs moved from hard-coded depth charts to daily
roster-management data somewhere between 2018 and 2021; playoff-format adjustments; simulation
count raised from 10,000 to 20,000.
**Chose:** **Assume no break.** The odds are a ZiPS/Steamer blend with a depth-chart playing-time
factor throughout, and none of the above is a documented change to that. The simulation-count
increase is variance reduction, not a change in expectation. **Supersedes** the earlier entry
bracketing a break at the 2017–2018 boundary, which rested on the SOS column and was wrong.
**Instead:** §4b estimates the persistence coefficient **year by year** and inspects it for a
discontinuity. A model change matters only if it moved the parameter being measured, so this
detects what matters directly rather than reconstructing FanGraphs' internals from outside.
**Why this rule, and not more archaeology:** enumerating possible upstream changes has no
natural stopping point — ZiPS and Steamer each revise continuously, and chasing them would
consume the project without bounding the risk. Testing the parameter bounds the risk exactly.
**If a jump appears:** the forecast-efficiency test splits at it; the hazard model carries a
regime indicator entered as a **time-varying covariate**, so spells spanning the break are not
assigned arbitrarily to the regime they started in; no seasons are dropped.
**Revisit if:** the year-by-year coefficient shows a discontinuity, in which case the date is
logged here and the split applied.

## 2026-09-22 — Projection mode fixed at `fg`

**Question:** Which of the six projection modes (fg, ATC, THE BAT X, OOPSY, season-to-date, coin
flip) is the instrument?
**Chose:** `fg`, the site default, for the full panel.
**Why:** It is a consistent ZiPS/Steamer blend across the study period, it is what a front office
or journalist would actually have seen, and it is what a reader reproduces without extra steps.
The construct being measured is *publicly visible signal*, not best-available forecast — so the
default is correct on grounds of construct validity, not convenience. Fixed now, before any
mode's results have been seen; six modes are six different answers.
**Revisit if:** never, absent evidence `fg` is unavailable for some season in the panel.

## 2026-09-22 — Three snapshots per season; Opening Day is an outcome, not a signal

**Question:** The spec used "odds at the close of the prior season" as the offseason decision
signal. End-of-season odds are degenerate — clubs are in or out — so they carry no forward-looking
information about the next season. What is the offseason signal, and what is Opening Day for?
**Options:** Keep prior-season-close odds | Use Opening Day as the signal | Reclassify Opening Day
as an outcome and use backward-looking evidence as the offseason signal
**Chose:** Three snapshots per season — **Opening Day**, **~1 week pre-deadline**, **end of regular
season** — with Opening Day reclassified as an outcome.

- **Opening Day** fixes whether the club is in a window that season (ex-ante position), and the
  **prior-close-to-Opening-Day delta** measures what the offseason achieved in odds space.
- **Pre-deadline** is the deadline decision signal; it cleanly precedes the behavior.
- **End of regular season** supplies final record and realized qualification — the outcome variable
  for §4b — plus Win WS on the day the field is set, for the R4 probe.

**Why:** Opening Day odds already contain the winter's moves, so they cannot be the signal the
offseason decision was made against. What a club actually knew entering the winter is its prior
Opening Day rank and its realized record, both backward-looking. The archive begins at Opening Day
each year, so no forward-looking offseason snapshot exists to collect.
**Consequence accepted, and stated in the paper:** **P1's lag test is cleanest at the deadline.**
The offseason result is reported alongside with the limitation named, rather than presented as
equivalent evidence.
**Bonus the delta buys:** a second, independent read on conversion magnitude — odds-space movement
to cross-check the dollar-years horizon score. *Caution:* odds also move on rival moves, injuries
and aging, so the delta measures change in competitive position, not purely club-caused change.
Cross-check, not substitute.
**Revisit if:** a forward-looking pre-Opening-Day projection series is found that covers the panel.

## 2026-09-22 — [OPEN] §4b outcome variable

**Question:** For the Mincer–Zarnowitz test, is the outcome realized qualification (binary), final
win percentage (continuous), or both?
**Leaning:** final W% as primary — binary qualification discards most of the information and makes
the residual test weak. Realized qualification reported alongside, since it is what the threshold
is defined on.
**Status:** not decided. Decide before running §4b.

