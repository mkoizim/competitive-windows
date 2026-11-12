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
 
## 2026-09-20 — Strategy classified at the window level  **[SUPERSEDED — by "P3 and P4 use different classification windows" (2026-09-20), then by "P3 conversion measured as a time-varying exposure" (2026-09-28)]**
 
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
 
## 2026-09-20 — The ~2003 futures panel is dropped  **[Study period and censoring figures SUPERSEDED — see "Study period extended to 2014–2026" (2026-09-21)]**
 
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
 
## 2026-09-20 — P4 replaced: under-conversion against a reachable frontier  **[Objective and falsifier SUPERSEDED 2026-09-28 — see "P4 re-specified against an optimal multi-season objective"]**
 
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
 
## 2026-09-21 — Berth-count shift handled as a robustness variant  **[2020 value extended 2026-09-27 — see "2020 postseason odds reconstructed"]**
 
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
 
## 2026-09-21 — 2020 retained for rank-based analysis, excluded from level-based  **[SUPERSEDED 2026-09-27, conditionally — see "2020 postseason odds reconstructed"]**
 
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
 
## 2026-09-21 — Collection by hand, not by script  **[SUPERSEDED same day — see "Collection by browser session"]**
 
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
 
## 2026-09-21 — Threshold stays Make Playoffs; R4 added as a fourth rival diagnosis  **[Win WS flatness claim CORRECTED 2026-09-28 — it was an assertion, not an observation; see "Data-examination wording corrected"]**
 
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
 
## 2026-09-21 — Collection by browser session, not by script  **[Email not sent — see "FanGraphs email not sent" (2026-10-18)]**
 
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
 
## 2026-09-22 — Three snapshots per season; Opening Day is an outcome, not a signal  **[Partly SUPERSEDED — the odds-delta claim by "No odds-space measure of offseason effect" (2026-09-22); the offseason signal by "Offseason signal set to prior-close standings" (2026-09-27)]**
 
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
 
## 2026-09-22 — [OPEN] §4b outcome variable  **[RESOLVED 2026-09-28 — see "P2 test specification"]**
 
**Question:** For the Mincer–Zarnowitz test, is the outcome realized qualification (binary), final
win percentage (continuous), or both?
**Leaning:** final W% as primary — binary qualification discards most of the information and makes
the residual test weak. Realized qualification reported alongside, since it is what the threshold
is defined on.
**Status:** not decided. Decide before running §4b.
 
## 2026-09-22 — No odds-space measure of offseason effect
 
**Question:** v0.10 claimed a prior-close-to-Opening-Day odds delta measures what a club's
offseason achieved. Does it?
**Chose:** No. The claim is withdrawn.
**Why:** End-of-season odds are degenerate — every club is at 0 or 1 for postseason access — so
there is nothing to take a delta from. The only available year-over-year comparison is Opening
Day to Opening Day, which spans a full year of development, aging, injury and rival activity in
addition to the club's own winter. Reading it as offseason effect would attribute a year of
league-wide movement to one club's transactions.
**Retained as:** a plain descriptive covariate — change in ex-ante position, year over year —
explicitly not interpreted as offseason effect. Conversion magnitude is measured by the horizon
score alone.
**Clarifies the snapshot roles:** Opening Day and pre-deadline establish *position* (is the club
in a window, and what was visible when it could act). End of regular season establishes *outcome*
(realized qualification, final record). Different questions; not substitutes.
**Revisit if:** a pre-Opening-Day forward-looking projection series covering the panel is found.
 
## 2026-09-22 — Lit review split into a duplication check and a full review
 
**Question:** When does the lit review happen, given the risk that prior work already answers
these questions?
**Options:** Full review now | Full review at write-up | Split
**Chose:** Split. A bounded **duplication check** runs in week 1; the full review runs alongside
drafting.
**Why:** The two serve different purposes. The duplication check is a go/no-go on the framing and
is cheap and narrow — does published work already estimate an MLB contention hazard, test
forecast efficiency on playoff odds, or measure conversion against a feasible frontier? The full
review is positioning and citation work, and it is more useful once data constraints and actual
results are known. Doing the full review first expands to fill available time and produces notes
against a spec that may still move.
**Known prior work to position against:** Jordan (SABR BRJ, Spring 2018) on typical window length;
Gennaro on postseason NPV; RotoWire's window model on core age, contracts and farm depth. None
estimates a hazard, tests forecast efficiency, or measures under-conversion.
**Revisit if:** the duplication check finds work that directly answers P1 or P4, in which case the
contribution is re-scoped here before any further data work.
 
## 2026-09-27 — Net horizon shift restated in years; dollar-years composite rejected  **[SUPERSEDED 2026-09-28 — see "Conversion classified from per-season net surplus"]**
 
**Question:** The net horizon shift was defined as Σ(acquired value × YTC) − Σ(surrendered value
× YTC), in dollar-years. Does it measure direction in time?
**Problem found:** No. Multiplying value by horizon lets the larger side of a trade dominate the
sign. Acquiring a $50M controllable star (horizon 2.0) for a $5M lottery ticket (horizon 4.5)
scores +77.5 — "building" — even though what came in arrives two and a half years sooner than
what went out.
**Options:** Keep the composite | Normalize by total value moved | Separate direction from magnitude
**Chose:** Separate them. Three measures per club per decision point:
- **Net horizon shift (ΔH)**, in years = value-weighted horizon of everything acquired minus
  value-weighted horizon of everything surrendered. Direction only.
- **Total value moved**, in dollars. Magnitude.
- **Net surplus value**, in dollars. Price.
**Sign convention unchanged:** negative = converting. `predictions.md` uses the term "net horizon
shift" and the negative-means-converting convention; both are preserved, so the registration is
unaffected. This is a correction to how the quantity is computed, made before any data was
collected.
**Revisit if:** ΔH proves unstable for periods with very small value on one side, which would
argue for a minimum-value rule on each side.
## 2026-09-27 — Years to contribution renamed "value horizon," weighted by production value  **[SUPERSEDED 2026-09-28 — see "Conversion classified from per-season net surplus"]**
 
**Question:** Two problems with YTC. (1) The name implies "when does the player start
contributing," which is zero for every major leaguer — a natural misreading. (2) It was
weighted by surplus value, which can be negative in any season (arbitration raises, underwater
tails), and a weighted average with negative weights does not produce a date.
**Chose:** Rename to **value horizon (H)**: the production-value-weighted average season in which
an asset's value arrives, t = 0 for the current season. Weight by **production value** (projected
WAR × $/WAR), which is non-negative, not surplus. Surplus is kept as its own measure, for price.
**Why:** Separates the two questions cleanly — production value answers *when*, surplus answers
*how good a deal*. Undiscounted, so the horizon does not depend on the discount rate.
**Revisit if:** never as a matter of definition.
 
## 2026-09-27 — Two units of time: season and decision point
 
**Question:** What is a "period"? Should the deadline be dropped as a unit, leaving one period
per season?
**Chose:** Two units. **Season** is the unit for windows. **Decision point** (offseason,
deadline) is the unit for behavior, signal, and the lag.
**Why:** The deadline is the only mid-season opportunity to add outside talent and the one place
where the signal cleanly precedes the behavior. Dropping it would leave one observation per year
and a P1 test built only on the weaker offseason signal.
**Revisit if:** never.
 
## 2026-09-27 — Offseason signal set to prior-close standings  **[Instrument SUPERSEDED 2026-09-28 — see "Offseason signal on Pythagorean standings"]**
 
**Question:** v0.10–v0.11 defined the offseason signal as the prior season's Opening Day rank plus
its final record. `predictions.md` registers the offseason signal as "prior season's close."
Which is it?
**Chose:** The club's within-league rank in the **final standings at the prior season's close**.
This matches `predictions.md`. The deadline signal remains Make Playoffs rank at the
pre-deadline snapshot.
**Why:** It is the freshest public information available before the winter. The prior Opening Day
rank is a full year stale. End-of-season *odds* are uninformative (every club at 0% or 100%), so
standings are used instead of odds at that one point.
**Limitation stated:** the offseason signal is a realized record, not a forecast. P1's deadline
test remains the clean one.
**Revisit if:** a forward-looking pre-Opening-Day projection series covering the panel is found.
 
## 2026-09-27 — 2020 postseason odds reconstructed  **[Condition met — confirmed by the author 2026-10-18]**
 
**Question:** On 2020 pages, Make Playoffs prices the old 10-team field. Can the correct 2020
postseason probability be recovered?
**Evidence:** The 2020 page and its documentation show the expanded field is priced in other
columns. Postseason probability = **Win Div + Win Div 2nd place + Clinch Wild Card**. The field
labelled Clinch Bye holds the second-place probability in 2020.
**Chose:** Use the reconstructed column for 2020 in both rank-based and level-based analysis,
**conditional on it summing to 8 per league** at each 2020 snapshot. Berth-relative robustness
variant uses rank 8 for 2020 (inside the registered test range). Supersedes the earlier
rank-only treatment of 2020 if the condition holds.
**If the sums fail:** revert to the earlier rule — 2020 used for rank only.
**Revisit if:** the sums fail at any 2020 snapshot.
 
## 2026-09-27 — P4 reported in two currencies
 
**Question:** Should P4's frontier be measured in playoff probability instead of World Series
probability?
**Chose:** Both. **Win WS primary**, as registered; **Make Playoffs secondary**.
**Why:** Make Playoffs saturates near 100% for strong clubs, so the best-resourced clubs would show
near-zero frontier gaps by construction — an artifact of the ceiling. Win WS does not saturate and
is convex in team strength, which is what makes "push when you're already good" the thesis. The
difference between the two gaps is itself informative: a large access gap with a small title gap
means a club could buy its way into October but not into favoritism — R4, quantified.
`predictions.md` registers P4 in title probability; the secondary currency is additional and does
not alter the registration.
 
## 2026-09-27 — Spec states the design; this log states the history
 
**Question:** The research plan had accumulated retired parameters, superseded contingencies and
withdrawn claims alongside the live design. A reader could not tell which parts were current.
**Chose:** The plan states the study as it currently is. This file holds what was considered,
rejected, and changed. The plan keeps a one-line-per-version history only.
**Removed from the plan in v0.12:** the parameter *D* discussion; the retired cohort contingency;
the account of what P4 no longer does; the dropped futures panel; the withdrawn odds-delta claim.
All remain recorded in this file.
 
## 2026-09-27 — [OPEN] Free-agency channel
 
**Question:** ΔH requires an acquired and a surrendered side. A free-agent signing surrenders
money and sometimes a draft pick, not assets, so it has no surrendered horizon. Free agency is one
of the two main conversion channels, concentrated in the offseason. How is it measured?
**Options:** Trade channel only, stated as a scope limit | A parallel free-agent measure (e.g.
current-season projected value added via free agency) | Treat the draft pick surrendered under
qualifying-offer rules as the surrendered side
**Status:** not decided. Must be resolved before Post 3. The deadline test is unaffected.
 
## 2026-09-27 — [OPEN] Active periods and the k-run  **[Expanded 2026-09-28 — see "Conversion classified from per-season net surplus"]**
 
**Question:** A decision point with only trivial moves should not define a mode. What minimum
total value moved makes a period count, and does an inactive period break a *k*-run or get
skipped?
**Status:** not decided. Must be resolved before Post 3, and before any transaction data is
examined.
 
## 2026-09-28 — Blind-spot review: disposition
 
**Question:** A separate review (2026-09-27) raised 25 items against plan v0.12. Which are adopted?
**Chose:** Adopted: A1, A2, A3, A4, A5, B1, B2, B3, B4, B5, B8, B9, B10, B11, C1–C4. Adopted with
modification: A6 (registration decision left open, downgrade recommended), A7 (normative benchmark
secondary, conditional on P4 machinery), B6 (clustering adopted; "effective N ≈ 13" rejected),
B8 (hindsight risk located in player-specific inputs, not generic tables). Moot: B7 (editorial
series cut). Added beyond the review: August waiver trades 2014–2018 assigned to the deadline.
Each change has its own entry below.
 
## 2026-09-28 — P2 demoted to an instrument check; editorial series cut
 
**Question:** P2's behavioral claim is established in adjacent work (Woodland 2016, MLB win totals;
Bennett 2019, college football). Does P2 still earn a place?
**Options:** Keep as a headline prediction | Drop | Keep as an instrument check
**Chose:** Keep as an instrument check, reported in Post 3's appendix. Cut the editorial-tiers series.
**Why:** It is nearly free — the Opening Day and end-of-season snapshots are its whole dataset. It
also checks the ruler P1 measures against: if the odds over-persist, the public signal is itself slow
to register a closing window, and P1 would understate the lag at closings. The editorial series was
the expensive part (hand-coding thirteen years of previews), ordinal rather than probabilistic, and
likely unavailable for 2014–2015.
**Registration:** the claim and falsifier are unchanged. Only its role in the write-up changes.
 
## 2026-09-28 — P2 test specification
 
**Question:** Resolves the open outcome-variable question. The earlier leaning (final W% outcome)
did not match the forecast (a probability); Mincer–Zarnowitz needs both in the same units.
**Chose:** **Primary:** realized qualification on Opening Day Make Playoffs, plus prior-season record,
using Franses's logit-based bias test for binary outcomes (*Applied Economics Letters* 28(15), 2021).
**Secondary:** final W% on Opening Day projected W%, plus prior-season record, standard MZ.
**Inference:** standard errors clustered by season, wild-cluster bootstrap (thirteen clusters).
**Why:** The primary tests the registered object — preseason odds — and the odds are what P1 uses.
The standard MZ Wald test is oversized for binary outcomes. Outcomes are dependent within a season
(fixed berths, shared shocks), so clustering is required. The review's claim that effective N is
about 13 is rejected: prior record varies within seasons, so identification does not come from
season-level variation alone. Effective N sits between 13 and ~390.
**Registration:** operationalization only.
 
## 2026-09-28 — Conversion classified from per-season net surplus
 
**Question:** The value horizon measured when, on average, acquired and surrendered value arrives.
Does that match the definition of converting — surrendering future value for present value?
**Problem:** No. It measures the composition of a trade. Trading a $5M prospect for a $50M
controllable star gains value in every season, yet average timing labels it converting. Weighting by
production value (adopted 2026-09-27 to fix negative weights) quietly changed the question from "did
the club give up future value?" to "did the average timing of production move earlier?"
**Options:** Keep the value horizon | Net surplus change by season, classified
**Chose:** For each club-decision point, compute ΔS_now (net surplus change, current season) and
ΔS_later (net surplus change, later seasons, undiscounted). Classify: converting (now +, later −);
building (now −, later +); net acquisition (both +); net subtraction (both −). Variants: "now" as
t ≤ 1; a looser present-oriented classification (any ΔS_now > 0).
**Why:** Matches the definition exactly, and a two-by-two is easy to explain. Negative surplus in
individual seasons is harmless here, because nothing is averaged. In near-fair trades the old and new
measures mostly agree; they diverge in lopsided trades and multi-move periods, which is where
correctness matters.
**Registration:** `predictions.md` defines the behavioral switch as the point where "net horizon shift
turns negative." A decision point classified converting is what that phrase now means. The registered
claim and falsifier are unchanged; this is operationalization, made before any transaction data
was examined. The value horizon is dropped from the spec.
**Expands the open active-period question:** it must now also say how net acquisition, net
subtraction and inactive periods enter a *k*-run.
 
## 2026-09-28 — Offseason signal on Pythagorean standings
 
**Question:** The offseason signal was raw-record standings rank at the prior season's close. Raw
record contains luck — the quantity P2 predicts forecasters over-weight. A club that correctly
discounts a lucky season would be scored as lagging the signal.
**Chose:** Within-league rank in Pythagorean (run-differential) standings at the prior season's
close. Raw-record rank and BaseRuns rank as variants.
**Why:** Public at season's close, less noisy than record, and fully reproducible from runs scored
and allowed. Still "prior season's close" as registered.
**Registration:** operationalization only.
 
## 2026-09-28 — P1's primary test on the deadline series
 
**Question:** The switch-confirmation rule mixed two instruments — odds rank at the deadline and
standings rank in the offseason. A club could "un-cross" purely because the instrument changed.
**Chose:** **Primary:** deadline series only — signal is PD Make Playoffs rank, behavior is
deadline classification, each confirmed at the next deadline, lag in seasons. **Secondary:** the full
grid, with each crossing confirmed within its own instrument.
**Why:** One instrument throughout, and the deadline is where the signal cleanly precedes behavior.
Cost accepted: resolution is one season on the primary test.
**Registration:** operationalization. The registered P1 text describes the signal as the club's
"odds" crossing the threshold, which the primary test now matches exactly.
 
## 2026-09-28 — Transaction assignment rule
 
**Question:** Which transactions belong to which decision point? July trades before the PD snapshot
would be compared against a signal measured after them; May–June trades belonged nowhere.
**Chose:** Offseason: day after the World Series through the day before Opening Day. Deadline
(primary): PD snapshot date through the deadline, plus the Aug 1–31 revocable-waiver period in
2014–2018. Deadline (variant): June 1 through the deadline, flagged as signal-contaminated.
Off-grid moves excluded from classification; their share of value moved reported.
**Why:** The primary window keeps signal strictly before behavior. August waiver deals (e.g.
Verlander to Houston, Aug 31, 2017) were part of the deadline market until 2019 and cannot be
omitted. Added beyond the review.
**Revisit if:** more than a quarter of each season's deadline-market value moves before the PD
snapshot, in which case the PD date is reconsidered and the change logged here.
 
## 2026-09-28 — P1 inference: permutation null and censoring
 
**Question:** The stated test (lag ≥ 1 outnumbers lag ≤ 0 "by more than chance") implied a 50/50
null, and dropped windows where the club never converted.
**Chose:** Lag treated as time-to-event. Windows that never convert are right-censored, not dropped.
Windows open at the start of 2014 are left-censored and reported separately. The null distribution
is built by permutation — shuffling behavioral series across clubs within era.
**Why:** Under independence the lag distribution depends on conversion and crossing frequencies,
not a coin. Never-converting windows are the strongest evidence for P1; dropping them biases toward
the null.
**Registration:** operationalization only.
 
## 2026-09-28 — P1 threshold bias acknowledged; normative benchmark added
 
**Question:** Two problems. (1) The plan said a loose threshold works against the thesis. That is
true for Post 1's hazard but backwards for P1: a looser threshold fires the signal switch earlier and
lengthens measured lag. (2) A threshold crossing is not the optimal moment to convert — the Doyle
Number work argues optimal buyers are secure contenders, not bubble teams.
**Chose:** State the bias. Report P1 at ranks 3 and 4 with the same prominence as the registered
rank 6. State that the threshold is a proxy, not an optimum. Where P4's machinery exists, also
report P1 against a normative benchmark: the first decision point at which the club's marginal
title return per dollar exceeded the exchange rate.
**Modified from the review:** the review proposed making the marginal-return benchmark primary.
Rejected as primary because it depends on the P4 machinery, which may not be built; kept secondary.
**Registration:** the baseline remains rank 6; ranks 3 and 4 are already in the registered test range.
 
## 2026-09-28 — P4 re-specified against an optimal multi-season objective  **[SUPERSEDED 2026-10-17 — see "P4 re-specified around the Doyle Number"]**
 
**Question:** As registered, P4 could not be falsified. "Reachable" was a maximum over a feasible set
that includes the club's own actual choice, so reachable ≥ reached for every club by construction.
It also maximized current-season title probability with no charge for the future title odds that
spent surplus would have bought — an infinite discount rate, under which every club under-converts.
**Options:** Keep as registered | Downgrade to exploratory | Re-specify
**Chose:** Re-specify. Objective = current-season title probability + discounted future title
probability of retained surplus, at the 10% reference rate; break-even reported. Gap = objective at
the optimum − objective at the club's actual choice, in expected titles. The gap can be negative
(over-conversion). Falsified if the mean gap is below a pre-registered materiality margin
**[OPEN — margin; proposed 1.0 title-probability point per open-window season]**.
Each club's optimum holds other clubs' behavior fixed; "under-convert on average" is the mean of
per-club gaps, not a league-wide claim. Premium bands are robustness checks, not a price-response
model.
**Why:** A falsification condition that can never occur is not a test. Prior evidence suggests true
gaps may be small (Paine 2025: net deadline WAR not significant for World Series odds once
pre-deadline strength is controlled; Ball: best single acquisitions add ~1–2 points), so the size
that counts must be fixed before seeing results.
**Registration:** this **alters the registered falsification condition**, which was defective. The
registered claim — clubs under-convert — is unchanged. Made before any data was examined.
**Revisit if:** the future-title mapping proves too model-dependent to defend, in which case P4
downgrades to the documented exchange-rate fallback, logged here.
 
## 2026-09-28 — P3 conversion measured as a time-varying exposure
 
**Question:** Classifying a window by its average conversion uses behavior across the whole window to
predict that window's length (immortal-time bias). Longer windows contribute more periods; short
windows over-weight a final-season sell-off, which reads as building. Separately, clubs convert
*because* they see the core aging and control running out — P3's main confound, untouched by payroll
and strength matching.
**Chose:** Discrete-time hazard of window exit at n+1, with conversion exposure through season n —
cumulative future surplus surrendered in converting periods since the window opened — as a
time-varying exposure. Variants: one-season-lagged exposure; count of converting decision points.
Controls: age and remaining team control of the top 10 contributors by projected WAR at Opening Day;
payroll tier; ex-ante strength.
**Also withdrawn:** the claim that "converting does not mechanically lengthen or shorten a window."
Converting mechanically trades later odds for current odds; P3 is a question of magnitude.
**Registration:** operationalization change (the registered text specified in-window mean
classification with matching). The registered claim is unchanged. Registration status is decided in
the next entry.
 
## 2026-09-28 — [OPEN] P3 registration status  **[RESOLVED 2026-10-17 — downgraded to exploratory]**
 
**Question:** P3 predicts no effect. With roughly 40–70 spells minus persistent contenders, a real
shortening effect would usually go undetected, so P3 would "survive" by default. "Materially shorter"
was never defined.
**Options:** (a) Downgrade to exploratory — estimate the effect with a confidence interval, no
directional claim. (b) Keep, with a pre-specified equivalence margin (e.g. hazard ratio within
0.67–1.5) and a TOST procedure.
**Recommended:** (a). At any margin narrow enough to mean something, TOST would almost certainly be
inconclusive with this sample, and the confounding in the previous entry makes a causal reading weak
in any case. Downgrading before data is legitimate and visible.
**Status:** awaiting the author's decision.
 
## 2026-09-28 — Valuation inputs as-of the transaction date
 
**Question:** Historical multi-year player projections are scarce, and current valuation tables
applied to 2014 trades would inject hindsight.
**Chose:** Every player-specific input — projections, prospect grades, health, contract status — is
taken as it stood on the transaction date. Generic mapping tables (grade to dollars, $/WAR) are fixed
and cited. The aging curve used to extend one-year projections is chosen and logged here before any
valuation is computed.
**Modified from the review:** hindsight enters through player-specific information, not through a
generic grade-to-dollar mapping. A table published after 2014 is acceptable if it is applied to
grades that were contemporaneous.
 
## 2026-09-28 — Labels and cutoffs: transaction-channel building; R4 cutoff  **[R4 cutoff SUPERSEDED 2026-10-17 — see "P4 re-specified around the Doyle Number"]**
 
**Question:** (1) "Windows preceded by net building in X%" would overstate building, since the
measure sees trades only, not internal development. (2) R4 had no threshold, so it could explain any
non-conversion after the fact.
**Chose:** (1) Label X as *transaction-channel* building; contrast with growth in internally developed
WAR where possible. (2) Non-conversion is explained by R4 when the club's marginal title probability
per dollar of available surplus fell below the exchange rate at the 10% reference rate. The rate's
value is computed before any non-converting club is examined.
 
## 2026-09-28 — Registration record
 
**Question:** `predictions.md` reads "Locked: [TODAY'S DATE]"; the placeholder was never filled, and
the file cannot be edited. The re-lock entry (2026-09-20) does not name the new commit.
**Record:** `predictions.md` was locked on **2026-09-20** at commit
**`33dbb7dff581a9d0cb12c62e34fdc1ff171b64b5`** (`33dbb7d`), superseding `2ddb3ac`. A timestamp record
of that hash was emailed to the author the same day. This entry is the authoritative lock date.
 
## 2026-09-28 — Data-examination wording corrected
 
**Question:** Several entries say choices were made "before any data was examined." Instrument
structure was examined: FanGraphs berth sums, the strength-of-schedule column, 2020 page structure,
and the archive's date range.
**Chose:** Read every such phrase as **"before any outcome or transaction data was examined."** No
outcome variable, window, spell count or transaction was observed before any decision in this log.
**Correction:** the 2026-09-21 entry states Win WS is "nearly flat across ranks 6–12 (inside model
noise)." That was an assertion from general knowledge, not an observation, and was not measured. The
R4 probe will measure it. The threshold decision does not rest on it; the P4-tautology argument in
the same entry stands on its own.
 
## 2026-10-17 — §1.2 framing: process failure, not blameless lag
 
**Question:** §1.2 said self-assessment lag "requires no one to be bad at their job." Is that right?
**Problem:** Sunk costs and advocate bias are textbook traps that front offices are paid to
recognize. Calling them blameless gives clubs a pass they wouldn't give themselves. The sentence
also read as a finding, when the study cannot identify which mechanism produced any lag.
**Options:** Keep "no one is at fault" | Frame as individual failure | Frame as correctable process failure
**Chose:** Correctable process failure. All four mechanisms (sunk costs, internal advocates,
private information, owner influence) sit on a spectrum between structural and skill-based.
Knowing about a bias doesn't remove it, so the remedy is process — outside review, pre-committed
switch criteria — not individual vigilance. The plan now states that the study shows whether a lag
exists, not which mechanism produced it.
**Tone rule revised:** critique decisions and processes, never named decision-makers.
**Why:** More accurate, and a stronger calling card: "your organization has a predictable blind
spot, and here's how to build a correction" is an offer; "it's nobody's fault" is reassurance.
**Registration:** none. Framing only.
 
## 2026-10-17 — Sustainability framed as a deliberate trade-off; reporting commitment
 
**Question:** If sustainability turns out to buy many postseason chances but no gain in title
probability, how is that reported?
**Chose:** Post 3 names it directly as a legitimate but deliberate choice: Frame B pays for it,
and it trades a real shot at a title for many modest chances. Clubs and owners making that trade
should do so knowingly, not defend it as a championship strategy. If the evidence shows the
opposite, that is reported with equal prominence. Post 5 adds the test that underlies the claim:
cumulative expected titles for long, modest windows vs. short, tall ones.
**Why:** It is the author's core interest, and stating it plainly is more useful to ops readers
than a hedge. Committing now to report the opposite outcome with equal prominence keeps the
framing from becoming a conclusion written in advance. The tone rule still applies: it describes
a strategy's trade-off, not a verdict on the people choosing it.
**Registration:** none. Reporting commitment only; no prediction altered.
 
## 2026-10-17 — Odds collected; what has been seen
 
**Record:** All FanGraphs playoff-odds snapshots planned for the project were collected by
2026-10-17. Transactions and valuations have not been pulled.
**Consequence:** Analyses resting only on the odds — window definitions and the Post 1 hazard — are
exploratory from here: their specifications were set before collection, but any change made now is
made with the data in view, and is logged with its date. P1's behavioral side and P4 depend on
transaction data not yet seen and remain confirmatory.
**Context, stated plainly:** the author lived through 2014–2026, inside a front office through 2016
and as an industry observer since. No researcher of this period is a blank slate. The safeguard is
fixing analysis choices before the transaction data is seen, not ignorance of history.
 
## 2026-10-17 — P3 downgraded to exploratory
 
**Question:** Resolves the open registration status.
**Chose:** Exploratory. Estimated in full as a time-varying exposure with core age and control as
controls, reported with a confidence interval, no pass/fail claim. Its themes remain central to
Post 3.
**Why:** P3 predicts no effect, and with roughly 40–70 spells a real effect would usually go
undetected, so a registered version would pass by default. Downgraded before any transaction data
was seen.
**Registration:** alters registration status — P3 is no longer a registered prediction.
 
## 2026-10-17 — P4 re-specified around the Doyle Number
 
**Question:** The 2026-09-28 specification required a full optimization over a feasible set, with
dollar valuations and a model of future title probability — expensive and hard to defend. Is there
a better benchmark for "under-converting relative to standing"?
**Options:** Keep the full optimization | Exchange-rate fallback | Doyle Number vs. market price
**Chose:** Doyle Number. Per club-deadline: D = future WAR the club should give up per current WAR,
given its odds (Silver & Paine method, rebuilt on FanGraphs odds, 10% reference rate, break-even
reported). M = market price — future WAR actually given up per current WAR acquired in that
deadline's trades. Where D > M, buying was favorable; shortfall = title probability the club would
have added buying up to D = M (capped by tradeable future WAR and payroll/CBT capacity) minus what
it added. Where D ≤ M, not buying is rational (R4); buying anyway is over-conversion. Falsified if
the mean shortfall is below the margin **[RESOLVED 2026-10-17 — 1.0 point; see "P4 margin and decision rule"]**.
**Why:** Normative, cheaper, and in WAR terms so $/WAR drops out of P4. It makes R4's cutoff concrete
(D below M) and gives P1 a normative benchmark (first deadline with D above M). M carries the supply
check: if no comparable player moved, M is undefined and the club-deadline is reported under R1.
Conceptually the Doyle Number was already P4's ancestor; this uses it directly.
**Registration:** substantial change to how P4 is measured; the registered claim — clubs
under-convert — is unchanged. Made before any transaction data was seen. D uses the odds, which
have been collected, but P4's outcome (what clubs actually did) depends on transactions not yet
seen.
**Also supersedes:** the R4 cutoff in "Labels and cutoffs" (2026-09-28), which used an exchange rate
per dollar of surplus.
 
## 2026-10-17 — Framing reference added  **[Headline confirmed — see "Ghiroli citation confirmed"]**
 
**Record:** Ghiroli, *The Athletic*, 2026-08-06,
https://www.nytimes.com/athletic/7494251/2026/08/06/mlb-competitive-window-trade-deadline/ — argues
competitive windows don't cooperate with clubs' plans. The project is framed as putting data behind
that observation. Headline not yet confirmed (page could not be fetched).
 
## 2026-10-17 — Farm-rankings study made optional; posts renumbered
 
**Question:** Where does the farm-rankings study (E3, formerly Post 2) belong?
**Chose:** Optional, after the luck ledger, if at all. Posts renumbered:
 
| New | Old | Post |
|---|---|---|
| Post 1 | Post 1 | The hazard of contention |
| Post 2 | Post 3 | Putting the roof on (P1, P3, rivals; P2 in appendix) |
| Post 3 | Post 4 | Leaving it on the table (P4) |
| Post 4 | Post 5 | The luck ledger |
| Optional | Post 2 | Farm rankings as a leading indicator (E3) |
 
**Why:** It doesn't answer either of the project's two core questions. Its role as the cheap fallback
if Post 1 stalls passes to the luck ledger, which uses only data already collected.
**Note for readers of this log:** entries dated before 2026-10-17 use the old numbering.
**Registration:** none. E3 remains exploratory.
 
## 2026-10-17 — P4 margin and decision rule
 
**Question:** How large must the mean shortfall be for P4 to hold, and how is uncertainty handled?
**Options considered:** 0.5 point (near the model's own noise) | 1.0 point | 2.0 points (would fail
even if under-conversion is real but modest).
**Chose:** **1.0 title-probability point** per club-deadline in which buying was favorable.
**Test:** P4 holds if the mean shortfall is at least 1.0 point and its 95% interval excludes zero.
Reported alongside: whether the entire 95% interval sits above 1.0 point. Falsified otherwise.
**Why:** Anchored on the title odds one impact deadline acquisition adds (Ball, roughly 1–2 points;
full citation to verify). A 1.0-point shortfall means that when its standing justified buying, a
club passed up about one impact acquisition's worth of title odds — a miss a GM would recognize.
For a contender with 8–15% title odds, one point is a 7–12% relative increase. Set before any
transaction data was seen.
**Registration:** completes P4's falsification condition. P4 stays registered.
**Revisit if:** Ball's figure cannot be verified, in which case the anchor is re-justified here
before any trade data is examined — the number itself does not move after data is seen.
 
## 2026-10-17 — P3 reporting rules fixed in advance  **[WITHDRAWN same day — see "v0.18 partly reversed"]**
 
**Question:** P3 is exploratory, and the author wants a particular answer. How is the write-up
protected from that?
**Chose:** The description of each possible result is fixed now (plan §2.4): interval near zero →
"does not meaningfully shorten windows"; interval spanning zero and large effects → "no evidence
either way; a meaningful effect cannot be ruled out"; interval on the shortening side → "converting
shortens windows, by about X"; interval on the lengthening side → reported as an association, not
causally. **[OPEN — before analysis]:** the range treated as negligible.
**Why:** Registration would not strengthen P3, since the sample cannot confirm a null. Committing
the wording in advance gives the same protection against motivated interpretation without
pretending to a test.
 
## 2026-10-17 — R3 revenue measure  **[Downgraded same day to an unverified candidate — see "v0.18 partly reversed"]**
 
**Question:** Revenue figures are outside estimates. What measures a club's revenue position?
**Chose:** Revenue-sharing payor/payee status as determined by the league under the CBA, with
Competitive Balance Round eligibility as a public cross-check, plus payroll and CBT position at each
deadline for capacity.
**Why:** League-determined status is more defensible than estimates. Capacity at the deadline is a
separate constraint: a rich club at the tax line can be more limited in July than a poor club with
room.
**Revisit if:** payor/payee status proves not to be publicly available by year.
 
## 2026-10-17 — Bubble trap parked
 
**Record:** Idea raised by the author and parked until after working with the data. Bubble clubs
may stay on the bubble because each single-deadline calculation correctly says not to buy, while
the leap to secure status — mostly an offseason move — is never attempted. Listed in the plan's
open items with possible tests. Not a prediction; nothing registered.
 
## 2026-10-17 — Ghiroli citation confirmed
 
**Record:** Brittany Ghiroli, "Competitive windows don't always cooperate. MLB teams should act like
it.", *The Athletic*, 2026-08-06. Read in full from a PDF the author supplied. Supersedes the
unconfirmed-headline note in "Framing reference added."
 
## 2026-10-17 — v0.18 partly reversed
 
**Record:** Three changes in v0.18 were committed without the author first confirming the full list.
On review, the author kept one and reversed two.
- **Kept:** P4 margin of 1.0 title-probability point and its decision rule.
- **Withdrawn:** the P3 reporting table. Whether to fix P3's wording in advance is open; the author
  wants more time to think about it.
- **Downgraded:** revenue-sharing payor/payee status is a candidate R3 revenue measure only,
  unverified. The author will confirm whether it is publicly available by year before it is adopted.
**Process note:** proposed edits are listed for the author's approval before they are applied.
## 2026-10-18 — Large off-grid moves listed by name
 
**Question:** Moves outside both decision-point windows are excluded from classification. Some are
real conversions — e.g. the June 2019 in-season free-agent signings of Craig Kimbrel (Cubs) and
Dallas Keuchel (Braves).
**Chose:** Keep them out of classification, but list every off-grid move above a value threshold by
name in the write-up. **[OPEN]:** the threshold.
**Why:** Off-grid moves have no signal snapshot taken just before them, so they can't enter the lag
test cleanly. Listing the large ones keeps significant conversions visible instead of silently
dropped.
 
## 2026-10-18 — 2020 reconstruction confirmed
 
**Record:** The author confirmed the 2020 data is correct, closing the condition attached to "2020
postseason odds reconstructed." 2020 is used in both rank-based and level-based analysis.
 
## 2026-10-18 — Surprise contenders named as a group  **[Broadened same day — see "Window patterns"]**
 
**Question:** Windows are defined on Opening Day, so a club that becomes a contender in-season —
the stars-align case — is invisible to the window-based analyses. What should such a club do, and
what do clubs actually do?
**Chose:** Name them. A surprise contender is below the window threshold on Opening Day and above it
at the pre-deadline snapshot. Exploratory analysis E4 compares their deadline behavior with expected
contenders, applies P4's Doyle comparison unchanged, and — as a secondary question — uses the §4c
split to ask whether each surprise is backed by underlying performance or by luck in the record.
**Why:** It is the cleanest read on how clubs respond to a signal they didn't plan for, and an
accessible question for readers. The Doyle Number doesn't depend on whether a window was planned.
**Not adopted:** using underlying performance to confirm the P1 signal in place of the next
deadline. The author chose to keep it as a secondary exploration only.
**Status:** exploratory — the odds have been seen; trades have not.
 
## 2026-10-18 — Single converting deadline counts as a behavioral switch
 
**Question:** The behavioral switch required two straight converting deadlines (*k* = 2). Is that
right?
**Chose:** *k* = 1 primary — the first converting deadline above a size floor counts — with *k* = 2
reported with equal prominence and *k* = 3 as a variant. **[OPEN]:** the size floor.
**Why:** A club that converts is changing behavior regardless of what it does at the next deadline.
Requiring two straight converting deadlines meant a club with a one-year window that pushed its chips
in once would be recorded as never converting — counted as late — biasing P1 toward confirmation,
the same problem as the loose threshold. The size floor guards against one small opportunistic deal
being read as a change of strategy.
**Registration:** `predictions.md` registers *k* = 2, tested at 1 and 3. This changes which value is
primary; 1 is already in the registered test range. Made before any transaction data was seen.
 
## 2026-10-18 — Window patterns
 
**Question:** Surprise contenders (where a club started) and one-year windows (whether it lasted)
overlap but are not the same, and a contender's down year between contending seasons is a third
irregular case. How are short and irregular windows handled?
**Chose:** Classify every club-season by Opening Day rank, pre-deadline rank and next season's
status into six patterns: stars aligned once, arrived early, faded fast, gap year, fizzled,
sustained. Surprise contenders are the first two. E4 asks what clubs did at the deadline in each
pattern, applies the Doyle comparison, and uses the §4c split to ask whether each rise or dip was
backed by underlying performance. Gap years are described alongside both the strict and grace
window rules.
**Why:** Covers every short or irregular window in one place, so none fall through P1's
confirmation rule or the strict window definition, and each pattern poses a distinct behavioral
question readers will recognize.
**Status:** exploratory — classification uses the odds, which have been seen.
 
## 2026-10-18 — One-year signal switches as a P1 variant
 
**Question:** P1's signal switch requires the crossing to hold at the next deadline, while the
behavioral switch now needs only one converting deadline. Should one-year signal switches count?
**Options:** Leave as is | Allow as a variant | Allow in the primary test
**Chose:** Variant. Primary keeps the two-deadline rule. The variant also counts a one-year crossing
when underlying performance supports the club's rank at that deadline. Filter resolved 2026-10-18 — see "One-year switch filter set."
**Why:** Brings one-season windows — the stars-align case — into P1, where a club that never
converted before its window closed is the strongest form of the thesis. The filter guards against
counting hot-streak flukes as "late," when not buying may have been right. Keeping it as a variant
avoids staking the headline on an untried filter.
**Registration:** operationalization; primary rule unchanged. Made before any transaction data was
seen.
 
## 2026-10-18 — One-year switch filter set
 
**Chose:** A one-year signal crossing counts in the P1 variant only if the club's within-league rank by
Pythagorean (run-differential) record to date, at the pre-deadline snapshot, is also inside the
threshold. The filter uses the same threshold as the signal and moves with the threshold variants.
**Why:** Simple, public, reproducible, and it separates rank earned by underlying performance from
rank earned by a lucky record. Requires runs scored and allowed as of each pre-deadline date, which
Baseball-Reference standings by date provide.
**Registration:** completes the variant's specification. Set before any transaction data was seen.
 
## 2026-10-18 — SABR deadline and five-week timeline
 
**Record:** SABR Analytics Conference abstracts are due Wednesday, November 25, 2026, 11:59 pm MST.
**Chose:** Replace the ten-week phase plan with a five-week timeline targeting submission by
November 22. Post 1 only, using the odds already collected. Trades, the value build, the Doyle Number,
the re-lock of `predictions.md`, and covariates that need the value build are deferred until after
the abstract. The full Post 1 is published on FanGraphs Community Research afterward.
**Open:** whether the SABR call accepts previously published work, which decides the FanGraphs timing.
**Why:** The hazard model needs only the odds; everything else would put the deadline at risk.
 
## 2026-10-18 — FanGraphs email not sent
 
**Record:** The author did not send, and will not send, the data-use email to FanGraphs. Collection
was completed through an ordinary browser session at reading pace, about 40 pages. The project
publishes derived measures only, never the raw odds tables.
 
## 2026-10-18 — Spec reviewers
 
**Record:** Former colleagues [reviewer] and [reviewer], possibly others, will review the spec's
definitions.
 
## 2026-10-18 — Reminder: judge rationality by underlying components
 
**Record (author's note, for later):** When evaluating whether the public signal was supported and
whether a club's restraint was rational, club-deadlines are grouped by underlying performance, not
only by playoff odds. A club with high odds but poor underlying numbers may be rationally holding
back. Applies to P1, R4, P4 and the window patterns. Method to be set before analysis.
 
## 2026-10-18 — Windows stay defined on Opening Day
 
**Question:** Should windows be defined at the trade deadline, when more information is available?
**Options:** Opening Day primary | Deadline primary | Both
**Chose:** Opening Day stays primary. How contention changes between Opening Day and the deadline is
written about directly through the window patterns (§3.3b).
**Why:** Deadline rank includes roughly 100 games of results, partly luck, so it mixes what was
expected with what happened. P1's signal already uses deadline rank; defining windows the same way
would collapse "in a window" into "the signal." And the patterns depend on the Opening Day vs.
deadline contrast.
 
## 2026-10-18 — Surprise patterns renamed
 
**Question:** "Arrived early" implied a plan, which is not observable.
**Chose:** "Stars aligned once" → **Surprise, one season**; "Arrived early" → **Surprise, sustained**
(below the line on Opening Day, above it at the deadline, still above the next year). Labels now
describe only what happened.
 
## 2026-10-18 — Post 1 threshold reminder reworded
 
**Chose:** Frame the favorite vs. bubble difference at the deadline as the same goal (titles) with
different returns, not different goals; note the Frame B reading of bubble clubs buying a berth and
the post-2022 first-round bye.
**Why:** The goals framing invites the reply that bubble clubs should still aim for titles; the
returns framing follows from the odds and is harder to dispute.
 
## 2026-10-18 — Corrections from the odds audit
 
**Record:** The cleaning script's checks all passed (13 seasons × 3 snapshots × 30 clubs; berth sums
correct every snapshot; 2020 reconstruction sums to 8 per league at all three snapshots). Three plan
corrections followed:
- **2020:** second place comes from its own field (`win_div_2nd`), not Clinch Bye, which is blank in
  2020. The reconstruction itself was always computed correctly.
- **2016 deadline:** August 1, not July 31 (July 31 was a Sunday). The pre-deadline snapshot (July 25)
  was already correct.
- **`data/processed/`** is never committed, alongside `data/raw/`, because processed files are close
  copies of the FanGraphs tables.
**Also noted:** end-of-season projected records differ from actual for a few clubs (unplayed games,
a 2023 FanGraphs glitch, 2018 tiebreakers). Final records use actual W-L; end-of-season projections
are not used. The Baseball-Reference cross-check of final records is deferred.
## 2026-10-20 — Spell count (go/no-go): proceed
 
**Record:** Baseline (top 6, strictly consecutive seasons): 53 spells — 21 of 1 season, 12 of 2,
7 of 3, 13 of 4 or more. Top 5: 42. Top 8: 54. Top 6 with the grace rule: 43. All four consistency
checks passed (156 in-window club-seasons at top 6; spell lengths sum to the in-window total at every
threshold; no spell over 13 seasons; the only 13-season spell is LAD's, in a window every season).
**Chose:** Proceed at the baseline (above the 40-spell cutoff).
**Also noted:** 12 spells were already open in 2014 and 12 are still open in 2026 (always 2k at
threshold k, by construction). Under the grace rule, 10 of 41 completed spells return after a
one-season dip.
**Convention:** A grace-rule spell's length is its full span, including the dip season; the
in-window count (`in_window_seasons`) is reported alongside.
**Open for Week 2:** treatment of spells already open in 2014 (left-censored, and they include most
long spells); pooling the hazard at lengths 4 and up.
 
## 2026-10-24 — Window patterns (E4, exploratory)
 
**Record:** Every club-season 2014–2025 classified at k = 3–9 (baseline 6) from Opening Day rank,
deadline rank and next season's Opening Day rank. All checks passed at every k. Baseline counts:
Surprise one season 22, Surprise sustained 24, Faded fast 16, Sustained 82, Gap year 21, Fizzled 25,
Out of contention 170. About 32% of Opening Day contenders fall below the line by the deadline (equal
to the number who rise, by construction).
**Chose:** Keep the seven labels; definitions fixed before the run (next season = next Opening Day
rank; gap year and fizzled separate; Out of contention added). Labels reviewed after seeing counts
against triggers set in advance; no changes.
**Dropped:** The label-sequence chance comparison. Adjacent labels share next season's Opening Day
rank, so the within-season shuffle null is invalid (two consecutive fades are impossible by
definition). Persistent club-specific forecast error moves to P2 as a signed-error test (projected
minus actual wins), exploratory.
**Also:** spells.py extended to k = 3–9 and now merges into results.json instead of overwriting it.
 
## 2026-10-25 — Window pattern definitions and renames (plan v0.28)
 
**Chose:**
- "Next year" in §3.3b means next season's Opening Day rank (consistent with windows defined on
  Opening Day), not next season's deadline rank.
- Gap year and fizzled are separate: an expected contender that falls out by the deadline is a gap
  year if back above the line next Opening Day, fizzled if not. The v0.22 table let them overlap.
- Seventh pattern, Out of contention (below at both readings), so every club-season has one label.
- Patterns reported at every *k* from 3 to 9; baseline 6.
- Renamed by what the next Opening Day projection did: Surprise, one season → **Surprise, not
  carried forward**; Surprise, sustained → **Surprise, carried forward**; Faded fast → **Held, not
  carried forward**; Sustained → **Held, carried forward**. Gap year and Fizzled unchanged.
- Labels describe a club-season; a club's history is its sequence of labels.
- Persistent club-specific forecast error added to P2 (§4b) and as a rival to P1 (§2.1),
  exploratory: signed error in wins, tested for a persistent club average and season-to-season
  carryover against permutation nulls.
**Why:** The old names implied a club-level history the labels don't measure. A club the public
signal consistently misjudges can rationally ignore it, which P1 would score as a lag.
**Note:** The label names in `patterns.py`, `results.json` and `label_grid.csv` still use the old
names; mapping above. **[RESOLVED 2026-10-25]** Code and outputs renamed to the new names, with
counts verified unchanged against the previous output (every k, by season, 2026 partials, club
lists, sequence results; label grid cell for cell). Printed short codes: S-NC, S-CF, H-NC, H-CF.
The sequence key in `results.json` is now `held_not_carried_forward_or_fizzled`.
## 2026-10-26 — Left-censored spells: flow sample primary, bounds and backcast reported
 
**Question:** 12 spells were already open in 2014, and the year each opened is unknown. How do they
enter the hazard?
**Options:** Start the clock in 2014 | Drop them (flow sample) | Recover the start year from a
pre-2014 ex ante source (backcast)
**Chose:** Flow sample (F) primary: 30 exits, 1 spell (LAD) open throughout. Reported with equal
prominence:
- **L:** every left-censored spell enters in 2014 at duration 1.
- **H:** every left-censored spell enters at the top bin.
- **B:** entry duration backcast from Baseball-Reference Opening Day playoff odds for 2011–2013. Used
  only if it passes the validation gate in the next entry.
**Why:** Starting the clock in 2014 records long-window exits as short ones. L and H barely differ
at duration 1 and at the top bin (4+: 0.21 vs 0.25). A backcast can move exits into the middle bins,
which neither extreme does, so B is reported rather than assumed away.
**Bins:** 1, 2, 3, 4+. The flow sample has 7 exits at 4+, above the 5-exit cutoff. Finer bins at
5–6 and 6+ were considered and rejected: they rest on 2–4 exits each, too few to tell apart from
duration 4. The life table shows exact durations. Thirteen seasons cannot estimate the hazard for
long windows (§3.3a); this is stated rather than extrapolated.
**Seen when deciding:** binned and exact-duration life tables for F, L and H.
**LAD:** excluded from F; named in the write-up as the only persistent contender.
## 2026-10-26 — Baseball-Reference Opening Day odds as backcast source
 
**Chose:** Baseball-Reference team playoff-odds pages, using the preseason row (the earliest date,
before any game).
- **Collection:** 2011–2013 first, then 2014–2026 for validation. Below 20 requests a minute, as
  Sports-Reference's bot policy requires. Raw pages cached and never committed.
- **Use:** within-league rank by Post odds, top 6, ranks only. Used only to date when the 12
  left-censored spells opened. Never defines an exit or adds a spell.
**Validation gate, fixed before collection:** top-6 membership must agree with FanGraphs' Opening
Day top 6 on at least 85% of the 390 club-seasons in 2014–2026 (chance is about 52%). Below that, B
is not used and that is reported.
**Known differences:** B-Ref rates teams on the last 100 games plus 50 games of .500 ball. It uses no
projections and sees no offseason moves. Its historical odds were generated after the fact. In
2011–2012 the leagues had 16 and 14 clubs; top 6 is used regardless.
**Terms:** Sports-Reference's data-use page bars using site content to prompt or instruct AI models.
The author reviewed this and chose to proceed. Not legal advice.
**Parked:** using the 2014–2026 B-Ref ranks as a P2 benchmark and as a windows robustness check
(Week 3 at earliest), and a long-panel version (after the abstract).

## 2026-10-26 — Hazard model specification (Post 1)

**Question:** How does the hazard model represent window duration, given 30 exits in the flow sample?
**Chose:**
- **M1 (description):** duration bins 1, 2, 3, 4+, no covariates.
- **M2 (primary):** log duration (capped at 4) + era + Opening Day strength + payroll. Five estimated
  numbers.
- **M2b (pre-specified variant):** M2 with a first-year indicator (duration 1 vs. 2+) in place of log
  duration.
- **Bins vs. log check:** likelihood-ratio test of M1's bins against log duration alone. If p < 0.05,
  the write-up says the smooth form misses structure. M2 is not changed after the fact.
- **Life tables by entry strength:** windows split at the median of Opening Day strength in their
  first season. Description only.
- **Link:** logit, with coefficients reported as odds ratios. Complementary log-log not run.
- **Definitions:** era = 1 when the deciding Opening Day is 2022 or later; 2020 is grouped with the
  10-berth seasons. Strength = Opening Day projected W% minus that of the 7th-ranked club in the
  league. Standard errors clustered by club.
**Why:** Bins plus covariates would need about 7 estimated numbers from 30 exits, above the usual
5–10 exits per number. M2b asks whether new windows are more fragile than established ones; the life
table does not obviously favor it, so it was not chosen to fit a seen pattern. Strength is included
because strong clubs survive into long durations, which would otherwise make windows look sturdier
with age.
**Rejected:** shrunken bins (hard to explain in an abstract; possible after it), a Cox model (sets
aside the duration question), club random effects (too few clubs and exits), and dropping payroll to
make room for bins.
**Seen when deciding:** the life tables in "Left-censored spells" (2026-10-26).
**Open:** the payroll measure, decided separately.

## 2026-10-26 — Backcast validation failed; sample B not used

**Record:** Baseball-Reference preseason odds collected for 2011–2026 (480 club-seasons). All parsing
checks passed. Top-6 agreement with FanGraphs' Opening Day top 6, 2014–2026: 302 of 390 (77.4%),
below the 85% gate fixed before collection. By season: 67%–93%. Among the 12 clubs whose spells were
open in 2014: 9 of 12 in 2014.
**Consequence:** Sample B is not used. Left-censored spells are handled by the flow sample (primary)
with L and H as bounds, as decided earlier today. Backcast entry durations remain on disk, unused.
**Retained:** 2014–2026 B-Ref ranks, for the parked P2 benchmark and windows robustness check.

## 2026-10-26 — Payroll covariate for the Post 1 hazard

**Chose:** Opening Day payroll from Cot's (active roster and injured list), for season n, predicting
exit at n+1. Scaled as log₂ of payroll relative to the MLB mean that season, so one unit is double the
league average.
**Collected but not used now:** year-end 40-man payroll and CBT payroll, 2011–2026, for R3, P4 and P3
later. Opening Day CBT figures too, where Cot's shows them.
**Rejected:**
- Year-end payroll: includes deadline acquisitions, the behavior Post 2 studies.
- CBT payroll as the primary measure: it handles deferrals better, but Cot's reports it at year-end,
  after transactions.
- Season n+1 payroll: clubs cut payroll after deciding to rebuild.
- Raw dollars (salary inflation) and rank (loses magnitude).
**Interpretation:** with Opening Day strength in the model, payroll's coefficient compares clubs with
the same projection. It measures capacity beyond the current roster, mixed with commitment to the
window. It is not described as market size or as ability to spend alone.
**Known limit:** Opening Day cash payroll understates clubs with heavily deferred contracts.
**Deferred:** committed future payroll, to the value build.

## 2026-10-26 — Payroll data: collection notes and 2020

**Record:** Cot's club pages collected for 2011–2026 (480 club-seasons). All checks passed for
2014–2026. Collection used the built-in browser, one page at a time, 31 page loads. No Opening Day CBT
figures exist on Cot's, so there is no CBT variant.
**2020:** Opening Day figures are prorated for all 30 clubs. Cot's gives no note, and the proration may
be uneven (2020 as a share of the 2019–2021 average ranges from 0.35 to 0.65). Kept as published: the
club-level correlation of relative payroll is 0.82 for 2019→2020 and 0.88 for 2020→2021, inside the
0.79–0.94 range for other adjacent seasons. Interpolating from 2021 was rejected because 2021 payroll
reflects decisions made after 2020.
**Cot's errors noted, not corrected:** Brewers 2020 listed twice (copy dropped). Brewers 2024 year-end
equals the Marlins' figure; it needs a second source before R3 or P4 use it. Reds 2021 year-end has a
missing comma (parsed correctly). Cot's printed MLB ranks disagree with its dollar figures 105 times;
dollar figures are used, ranks never.
**2026:** year-end and CBT figures are Cot's projections; Opening Day figures appear to be actuals.

## 2026-10-26 — Deadline status in the Post 1 hazard: description only

**Question:** Should falling below the line by the deadline enter the hazard model?
**Chose:** No. It is reported as a cross-tabulation of exit at n+1 against deadline status in season
n, for each sample. Across all 144 Opening Day contender club-seasons, 2014–2025 (sample L), the cells
are the window patterns: held, carried forward 82; held, not carried forward 16; gap year 21;
fizzled 25. Of the 41 exits, 25 had already fallen below the line by the deadline.
**Why:** Post 1 asks how long windows last as judged from Opening Day. Deadline status is information
from after that point, so adding it changes the question to one conditional on the first half. It
would also be a sixth estimated number from 30 exits.
**Corrected in discussion:** the first half does not determine the next Opening Day projection.
Projections are built player by player, and 21 of 46 deadline fallers were back above the line the
next Opening Day. Gap years include temporary setbacks such as injuries, and the write-up says so.
Whether a drop was backed by underlying performance is tested in the window-pattern analysis (§4c,
E4, Post 2), not here.

## 2026-10-26 — Hazard run: implementation choices

**Record:** All seven checks passed (F: 102 rows, 30 events, 22 clubs; L and H: 144 rows, 41 events).
Choices made in implementation, accepted on review:
- In H's exact-duration life table, left-censored spells enter at duration 4 and count up; in the
  models they stay in bin 4+.
- M1 intervals are reported both unclustered and clustered by club.
- Clustered standard errors use statsmodels' default small-sample correction, with Wald intervals.
- Analysis packages live in a local `.venv`, not committed; versions are pinned in `requirements.txt`
  (commit `1f152ea`).

**Independent check:** M2 in F and the bins-vs-log test were refit in the planning chat from
`hazard_pp.csv`, with identical results.
**Planned for Week 3:** wild-cluster bootstrap intervals for M2 (inference only; not a new variant).

## 2026-10-26 — 2027 window forecasts timestamped

**Chose:** Forecast the probability that each of the 12 windows open on 2026 Opening Day is closed on
2027 Opening Day. M2 in the flow sample, as estimated, with 2026 Opening Day inputs. Written to
`docs/forecasts-2027.md`, committed and pushed before the 2026–27 free-agent market opens, and never
edited afterward.
**Outcome:** closed = below 6th in its league by FanGraphs Make Playoffs on the first archived 2027
date (same rules as `windows.csv`).
**Scoring, fixed in advance:** Brier score against a constant forecast of 30/102 = 0.294; log loss
reported alongside. With 12 forecasts, the result is reported as a single-season check, not a
validation.
**Contingency:** the CBA expires December 1, 2026. If 2027 Opening Day odds are archived, score against
them regardless of playoff format. If no 2027 regular season starts by December 31, 2027, the
forecasts are void.
**Limit stated in the file:** forecasts use 2026 Opening Day information only. Nothing from the 2026
season, deadline or offseason is in them.

## 2026-10-26 — Forecast lock record

**Record:** `docs/forecasts-2027.md` was committed and pushed at
`3fdc13969042cc8709cc19c79df91002cb3fd253` (`3fdc139`), 2026-10-26 20:15:33 −0400. This entry is the
authoritative lock record.

## 2026-10-31 — OD Make Playoffs vs. realized qualification: descriptive count

**Record:** Opening Day Make Playoffs odds against realized qualification (P2's dataset) are being
examined for a descriptive count, before any analysis is run. For each season 2014–2026 except 2020:
clubs with OD Make Playoffs below 50%, how many qualified (actual), the sum of their OD odds
(expected), and a 5th–95th percentile range from 10,000 simulated seasons treating each club's OD odds
as an independent Bernoulli.
**Not a test of P2.** P2 is about whether prior-season record predicts the forecast error (a
Mincer–Zarnowitz-form efficiency test). This count conditions on nothing from the prior season and
does not test that claim; it does not count toward P2's result either way.
**Output:** a new key in `results/results.json` (per-season aggregates only; no team-level odds) and a
figure in `results/figures/`.

## 2026-10-31 — Descriptive count: 2020 included; berth-relative variant added

**Changes the entry above, before anything was committed from it.** Two changes, both still
descriptive and not a test of P2:
- **2020 is shown.** It uses the 16-team field: OD odds are the rebuilt Win Div 1st + Win Div 2nd +
  Clinch Wild Card (§3.3a), and 16 clubs qualify. It is marked as its own era in the figure.
- **Second variant: not favored on Opening Day.** A club is in the count if it was outside the top N
  in its league by OD Make Playoffs, where N is that season's berths per league (5 in 2014–2019 and
  2021, 8 in 2020, 6 from 2022). This is `window_berth` = 0 in `windows.csv`. The below-50% variant
  is kept alongside it.
**Why:** a fixed 50% cutoff means something different when the field size changes (in 2020 more
than half the league qualifies). The berth-relative cut uses the field size each season.

## 2026-11-01 — Descriptive count: third variant, outside berths + 2

**Adds to the two 2026-10-31 entries; still descriptive and not a test of P2.** Third variant: a club
is in the count if its Opening Day rank in its league by Make Playoffs is worse than berths per
league + 2 (outside the top 7 in 2014–2019 and 2021, top 10 in 2020, top 8 from 2022). Each league
is analyzed separately (actual, expected and a simulated range per league), and the figure shows
the two leagues summed; the summed range comes from adding the per-league simulated counts.
**Why:** this leaves out the clubs just outside the field, so it asks whether clubs priced as
clear long shots qualify at the rate their odds imply.

## 2026-11-01 — Plan v0.29; division strength and market size in Post 1

**Record:** The plan moves to v0.29, carrying in the decisions logged 2026-10-26 to 2026-11-01. Edits
that only carry logged decisions were applied without re-approval; the items below were new and
decided by the author.
**Chose:**
- **Division strength:** not in M2. The reason is the exit budget (a sixth estimated number from 30
  exits), not that it is already priced in: window membership prices the division path, but
  strength (projected win percentage) does not. Stated as a limitation in the write-up.
- **Market size:** deferred until after the abstract. It is a capacity measure clubs don't choose,
  to be considered alongside R3's revenue measure; it is not treated as a substitute for that
  measure.
- **Risk register:** two rows added, for the strength result partly reflecting projections agreeing
  with themselves (Medium) and for Sports-Reference's terms (Low).
- **Repository layout:** `docs/data-dictionary.md` and `docs/lit-notes.md` marked as planned.
  `CLAUDE.md` to be created before Week 3.

## 2026-11-01 — Week 3 robustness specification (Post 1)

**Question:** How are the pre-specified robustness variants, the small-cluster inference and the
Jordan comparison run? Fixed before any Week 3 result is seen.
**Chose:**
- **A. Samples:** the eight variants (thresholds 3, 4, 5, 7, 8, 9; berth-relative; grace rule) are
  run in the flow sample (F) only. L and H remain baseline bounds.
- **B. Strength in each variant:** measured against the first club out at that variant's threshold,
  the (k+1)th club (berths + 1 for the berth-relative variant). At k = 6, including the grace
  variant, this is the 7th club, as at baseline.
- **C. Bins:** fixed at 1, 2, 3, 4+ in every variant. A bin with zero closings is reported as a raw
  count with an exact binomial interval and flagged, not estimated by the model. The bins-vs-log test
  runs in each variant.
- **D. Grace variant:** a window closes after two straight Opening Days out. Dip seasons are not
  rows but count toward a window's age (span length, as logged 2026-10-20). A closing is recorded in
  the last in-window season before the two seasons out. Rows run through 2024 only, so every row's
  outcome is known.
- **E. Small-cluster inference:** every clustered result (M2 and M2b in F, L and H, and the variants)
  also gets p-values against a t-distribution with G − 1 degrees of freedom (G = clubs). Strength in
  M2, sample F, also gets a wild score bootstrap p-value (Kline & Santos, 2012; Webb weights; 9,999
  draws), with an implementation check: 500 simulated datasets with a true null effect should be
  rejected at about 5%. The planning chat rebuilds the bootstrap independently. This replaces the
  "wild-cluster bootstrap intervals" planned on 2026-10-26; the clustered intervals stand.
- **F. Jordan comparison:** Jordan's (2018) ex post rule applied to the same 2014–2025 seasons from
  the end-of-season records already collected (division winner, wild card, 2nd or 3rd within 5
  games, or 87+ wins; opens after two contending seasons; closes after two non-contending seasons).
  2020 thresholds scaled to 60 games (.537; 1.85 games). Windows open in 2014 dropped, as in F.
  Reported side by side with the strict and grace windows: club-season agreement, window counts,
  length distributions and life tables. Description only; no hazard models. Reinhart (2018) cited,
  not replicated.
**Why:** each choice keeps the variants comparable with the baseline, avoids outcome-dependent
censoring, or addresses the 22-cluster limitation without changing the model. The Jordan comparison
holds the seasons fixed, so any difference comes from the definition, not the period.

## 2026-11-01 — Berth-relative threshold reported with equal prominence in Post 1

**Question:** Should Post 1's baseline be the berth-relative threshold (top 5 in 2014–2019 and 2021,
top 8 in 2020, top 6 from 2022) instead of fixed rank 6?
**Options:** Keep fixed 6 primary, berth-relative one of eight variants | Keep fixed 6 primary,
berth-relative reported with equal prominence | Switch the primary to berth-relative
**Chose:** Fixed rank 6 stays primary. The berth-relative variant gets its own line in every Post 1
table and in the abstract, alongside the baseline.
**Why:** The berth-relative line keeps the meaning of a window constant (inside the projected
field), which is a real argument for it. But rank 6 is the registered baseline and is shared with
P1; switching after the fixed-6 hazard results were seen is the move pre-registration exists to rule
out; and with a fixed line the 12-team-era term measures the format change rather than a moving
threshold. Equal prominence, decided before the berth-relative results are seen, takes the argument
seriously without those costs. If the two disagree, the disagreement is a finding about the 2022
format (as anticipated in "Berth-count shift handled as a robustness variant," 2026-09-21).

## 2026-11-02 — Week 3 prompts: left-censoring under gap-tolerant rules; Jordan reference

**Question:** F drops windows whose age is unknown. Under rules that tolerate a one-season gap,
which windows does that cover?
**Chose:**
- **Grace variant:** spells starting in 2014 or 2015 are left-censored. A club out on 2014 Opening
  Day may have been in a one-season dip from a window open in 2013, which the archive does not
  cover. Five spells start in 2015: CHC, CLE, SDP, SEA, TOR.
- **Jordan windows:** a window is left-censored unless two straight non-contending seasons occur
  between 2014 and the season before its first contending season.
- **Jordan's games-behind rule:** "2nd or 3rd within 5 games" is measured against the division
  winner, as his article specifies.
- **Score bootstrap size check:** passes if the 5% rejection rate over 500 simulated datasets is
  within 3–7%.
**Why:** Applies F's existing rule (every window's age is known) to definitions in which one season
out does not close a window. Fixed before any Week 3 result was seen.

## 2026-11-02 — Robustness variants run (Post 1)

**Record:** The eight variants (thresholds 3, 4, 5, 7, 8, 9; berth-relative; grace) were run in F
as specified on 2026-11-01 and 2026-11-02. All six checks passed; every fit converged, with no
separation. The generalized `hazard.py` reproduces the baseline byte for byte, and every
pre-existing key in `results.json` is unchanged.

**Implementation choices, accepted on review:**
- Era under grace coded as at baseline (n+1 ≥ 2022). Eight rows with n = 2020 are coded 0
  although their closing also depends on 2022 Opening Day. Footnoted in the write-up.
- One zero-closing bin (top 3, duration 3: 0 of 6, exact 95% interval 0–0.459), reported as a raw
  count and entered at its limit in the bins-vs-log test.
- Grace life table: the number at risk can rise between durations. A dip season counts toward a
  window's age but is not a row, because its outcome is already settled by the previous row (a
  dip-season row could never record a closing). So a window that dips at age 3 is at risk at age 4
  but not at age 3.
- `data/processed/hazard_robustness_pp.csv` written for independent refits (not committed).
- In `hazard_robustness`, the normal p-value key is `p_normal`, beside `p_t`; the `hazard` key keeps
  `p`.

**Independent check:** All nine definitions were rebuilt in the planning chat from `windows.csv`,
`odds.csv` and `payroll.csv` with separate code. Person-period rows are identical in every
variant, and every reported count, odds ratio, p-value, bin hazard, survival figure and bins-vs-log
p-value reproduced. `window_berth` was confirmed to equal `window_top5` in 2014–2019 and 2021,
`window_top8` in 2020 and `window_top6` from 2022, with no mismatches.

**Results, for the record:**
- **Strength:** odds ratio below 1 in all nine definitions (0.59–0.84 per projected win above the
  first club out), with the 95% interval excluding 1 in eight (not top 4).
- **Duration:** the odds ratio changes sign across definitions (below 1 at top 3, top 4 and grace;
  above 1 elsewhere). Significant (t-p < 0.05) at top 5, top 8 and berth-relative. No definition
  shows a significant protective effect; top 3 and top 4 lean protective with wide intervals.
- **Berth-relative as a blend:** its estimates fall between top 5 and top 6 (duration 3.97 vs 7.38
  and 1.72; strength 0.667 vs 0.615 and 0.723), as expected from a line that is top 5 in seven of
  the twelve row seasons and top 6 in four.
- **Era and payroll:** not significant in any definition. Baseline era 1.21 (0.51–2.88).
- **Bins vs. log:** not rejected in any definition (lowest p = 0.07, top 5).
- **t-correction:** changes no conclusion.

**Chose (write-up):**
- **The two lines, described for readers.** Berth-relative: "projected to make the playoffs on
  Opening Day." Fixed top 6: "projected in the field or the first club out" before 2022, and exactly
  the field from 2022. Fixed 6 stays primary because it was registered and its yardstick does not move
  across formats, not because it matters more to readers. Equal prominence stands.
- **Duration.** No claim in either direction. Stated instead: no definition shows a detectable
  protective effect of age; under some definitions older windows are riskier, but that depends on
  where the line is drawn. What reliably predicts survival is cushion, not age.
- **Baseline vs. berth-relative on duration.** The difference comes mainly from 2014–2021, where
  the berth-relative line sits inside the five-team field (top 5) and the baseline one spot outside
  it (top 6); top 5 alone, which does not change at 2022, shows the same pattern. Windows carried
  over from 2021 can differ in age between the two definitions, so the line's change at 2022
  contributes a little, which is why "mainly" and not "entirely."
- **Format.** The baseline era term is the format test, with one stated limit: rank 6 moved from one
  spot outside the field to the last spot inside it, so the term asks whether a top-6 club's closing
  risk changed once 6th became a playoff spot. No change detected; four seasons, wide interval. The
  berth-relative era term (0.60) is not read as a format effect, because that line also loosens from
  5 to 6 at 2022. No further analysis of the format question is added now.
- **Cushion table for berth-relative.** Written to `results.json` under `hazard_robustness`, with
  cushion measured against the first club out of the field (berths + 1), before any figure from it
  appears in the write-up.

**Revises:** the expectation in "Berth-count shift handled as a robustness variant" (2026-09-21) that
a disagreement between the two lines would show how the 2022 format change moved the contention
line. The disagreement found (on age) comes mainly from where the line sits in the five-team era
(inside the field at 5th, or one spot outside at 6th), not from the change at 2022.

**Correction:** strength is in projected wins per 162 (162 × the difference in projected W%), as §5
states; the 2026-10-26 specification entry's "projected W%" wording is superseded.

## 2026-11-02 — Small-cluster inference run (Post 1)

**Record:** Run as specified in item E of "Week 3 robustness specification" (2026-11-01) and in
"Week 3 prompts" (2026-11-02). All checks passed.
- **t-correction:** p-values against t with G − 1 df for every term of M2 and M2b in F, L and H
  (G = 22 in F, 26 in L and H). F values match `hazard_robustness` (top 6) exactly.
- **Wild score bootstrap** (strength, M2, F): master seed 20261102, 9,999 draws, Webb weights.
  T = −3.276; bootstrap p = 0.0003 (3 of 9,999); normal-approximation p = 0.0011.
- **Size check:** 500 simulated null datasets, 999 draws each, no fit failures. Rejection 6.8% at
  the 5% level (inside the 3–7% band) and 10.6% at 10%.

**Independent check:** The bootstrap was rebuilt in the planning chat from the formula in the
prompt. Restricted coefficients, projection, all 22 club sums (largest difference 1.5e-14) and T are
identical, and Claude Code's seed scheme reproduces 3 of 9,999 exactly. Further checks, not
pre-specified and not used in the write-up: with 1,000,000 draws the bootstrap p is about 0.0001,
so 0.0003 is within draw-to-draw noise at 9,999 draws; a 2,000-dataset size check gave 5.3% at 5%
and 10.6% at 10%, so the 6.8% is consistent with noise; 17 of 22 clubs' score contributions share a
sign, and dropping the largest (HOU, 24% of the sum of squares) leaves T = −3.20.

**Results, for the record:** Strength in M2, F: clustered normal p 0.0009; t(21) 0.0033; score
normal 0.0011; wild score bootstrap 0.0003. In L and H, strength's t-based p is below 0.001. No
other term in M2 or M2b reaches 0.05 in any sample.

**Chose (write-up):** Prose quotes the most conservative p-value, t with G − 1 df (0.0033 for
strength in F); the bootstrap and the other p-values appear in the table. The bootstrap p is
reported as computed (0.0003, 3 of 9,999), not replaced by the larger-draw figure. Strength's
significance does not depend on 22-cluster asymptotics, and the write-up says so in one sentence.

## 2026-11-02 — Jordan comparison: ties for a division title

**Question:** From 2022 MLB settles division ties by formula, without a tiebreaker game, so the
win-loss records show two clubs tied for first in three division-seasons (2022 NL East, 2023 AL
West, 2025 AL East). Jordan's "won its division" needs one winner.
**Chose:** Ties for first are broken by the actual division title (ATL 2022, HOU 2023, TOR 2025,
each on head-to-head record), listed in `jordan.py` with sources. Check 2 (three division winners
per league) unchanged. Ties below first share the better rank.
**Why:** "Won its division" means the title. `clinch_bye` marks the same clubs here but is not
defined as division winner. No contending flag changes: all six tied clubs made the postseason.
Fixed before any Jordan result was seen; the run stopped at the check.
**Correction:** the planning chat had said the season-end records needed no tie rule because they
include the 2018 game-163 tiebreakers. That holds only through 2021.

## 2026-11-02 — Jordan comparison and berth-relative cushion table run (Post 1)

**Record:** Run as specified in item F of "Week 3 robustness specification" (2026-11-01), "Week 3
prompts" (2026-11-02) and "Jordan comparison: ties for a division title" (2026-11-02). All checks
passed after the tie rule was set. Two new keys, `jordan_comparison` and `cushion_berth`; every
pre-existing key in `results.json` unchanged.
**Implementation choices, accepted on review:**
- Jordan life table built as the grace one: one row per contending season; gap seasons count toward
  age but are not rows; the closing is recorded in the last contending season. Rows run through 2023,
  since a closing needs two later seasons; 14 of 16 windows have rows.
- "Within 5 games" is inclusive, matching Jordan's "five or fewer" (decides CLE 2014, 5.0 back).
- The 2020 threshold (.537) is compared with unrounded W/(W+L).
**Independent check:** Rebuilt in the planning chat from `odds.csv` with separate code. Contending
count (147 of 360), division winners (72), the 2×2 table, the 16 Jordan windows (7 closed), the 13
left-censored windows and completed lengths (mean 3.29, median 3) all match; the Jordan life table
was recomputed by hand (year 5 depends on MIL 2022 as a gap year). Berth-relative cushion bands
match the expected counts.
**Results, for the record:**
- Survival after 4 years: Jordan 0.56; strict 0.22; grace 0.36. Mean completed length 3.29, 2.67,
  2.25. Jordan windows cannot be shorter than 2 seasons; among strict windows that survive their
  first year, 0.33 are open after year 4.
- 2×2 (Jordan contending × window_top6, 2014–2025): 92 both; 52 projected but not contending; 55
  contending but not projected; 161 neither. 70% agreement.
- Jordan: 16 windows in the flow sample after 13 were dropped as left-censored; 7 closed.
- Berth-relative cushion: ≤ 2 wins, 15 of 30 closed; 2–5, 9 of 29; 5–8, 3 of 16; > 8, 1 of 22.
**Chose (write-up):**
- The comparison is reported as what the ex ante definition changes: judged from Opening Day, as
  clubs plan, windows are shorter and less durable than a results-based count suggests, and about a
  third of each definition's contenders are not contenders under the other. Description only.
- Jordan uses season-end records through 2025, as specified, so no definition uses information from
  the 2026 season: the ex ante windows judge closings by 2026 Opening Day projections. 2026 records
  were available and not used.
- The published survival figure stops at year 6, matching the life tables and the stated limit on
  long windows; the year-6 point is labeled "still open after 6 seasons." Full life tables stay in
  `results.json`. The repo figure is regenerated when the write-up figures are built (Week 4).

## 2026-11-02 — Era-stratified fitting not run (Post 1)

**Question:** §3.3a lists era-stratified fitting as a secondary check "where power allows." Does it?
**Chose:** No; not run. The pooled era term remains the format test.
**Why:** In F, 12 closings come from 10-team-era rows (47 rows) and 18 from 12-team-era rows (55).
M2 fit within an era estimates four numbers (era drops out), about 3 closings per number in the
earlier era, below the 5–10 used when M2 was specified (2026-10-26). Decided on these counts alone,
with no stratified model fit.

## 2026-11-03 — Review steps before the abstract

**Question:** The plan had one referee pass, in Week 5 after reviewers read a draft, and no check of
the processed data against the raw files. Is that enough before the abstract?
**Chose:** Three steps before drafting: an independent rebuild of the processed files from
`data/raw/`; a hand spot check of five raw values against the FanGraphs pages; a referee pass on the
analysis in a fresh chat. A second referee pass runs on the draft in Week 5. A human technical
reviewer reads the model after the abstract and before the full Post 1.
**Why:** Every Week 1–3 check rebuilt results from the processed files, so an error in cleaning
would have passed all of them. A referee pass after reviewers have read a draft finds a fatal
objection too late to answer it cheaply.

## 2026-11-03 — Processed data rebuilt from raw; Opening Day snapshot gaps

**Record:** `odds.csv` (1,170 rows), `windows.csv` (390 rows) and `payroll.csv` (480 rows) were
rebuilt in the planning chat from `data/raw/` with separate code, from the plan's definitions only.
Every column matches; relative payroll matches to 5e-7 (rounding). All pre-deadline dates fall exactly
7 days before the deadline. Every Opening Day snapshot has all clubs at 0–0, and every
league-season's postseason odds sum to its berths.
**Gap logged (§3.2):** the first archived date falls before an international opening series in
2019 (Mar 19; Tokyo), 2024 (Mar 19; Seoul) and 2025 (Mar 17; Tokyo), about 9 days before most clubs'
openers. The snapshot rule (first archived date, all clubs 0–0) is followed; those projections
predate roughly a week of late-spring news. No change made.
**Not covered:** both builds read the same raw columns, so a column mislabeled at collection would
pass. The five-value spot check against FanGraphs addresses this.

## 2026-11-03 — Five raw values spot-checked against FanGraphs

**Record:** Checked by hand against the archived FanGraphs playoff-odds pages, all matching: 2014
Opening Day TBR and CLE; 2025 Opening Day HOU and BAL; 2020 Opening Day CHW (the three components of
the rebuilt postseason probability); 2023 pre-deadline MIA; 2019 end of season MIL. This closes the
column-labeling gap noted under "Not covered" in the entry above.

## 2026-11-03 — Correction: strict survival after four years

**Record:** Strict (fixed top 6, sample F) survival after four years is 0.21:
`hazard_robustness/variants/top6/survival_after/4` = 0.2148, matching
`jordan_comparison/definitions/strict/survival_after/4`. "Jordan comparison and berth-relative cushion
table run (Post 1)" (2026-11-02) and plan §5 in v0.30–v0.31 gave 0.22. Found while building the
abstract's numbers manifest. No result changes; the plan is corrected in v0.32 and the 2026-11-02 entry
stands as written.

## 2026-11-03 — SABR call checked

**Record:** The 2027 SABR Analytics Conference call
(https://sabr.org/latest/submit-your-presentation-abstract-for-2027-sabr-analytics-conference/) sets
abstracts at no more than 500 words, with a title, a review of previous work, a summary of methodology,
preliminary or final results, and the expected contribution. Abstracts go by email to
analytics-presentations@sabr.org, marked general or student track, and should describe audio-visual
needs. General-track presenters submit a full research paper after review: requested December 18, due
January 22, 2027. Finalists are notified February 19; the conference is March 12–14, 2027, in Phoenix.
**Not addressed by the call:** whether figures or tables may be included, and whether work published
elsewhere is eligible. Both are put to SABR by email. Until it answers, the abstract is plain text and
the FanGraphs timing question in plan §7 stays open.

## 2026-11-11 — Realized-outcome refit (Post 1): specification

**Question:** Both referee passes (2026-11-04) objected that cushion and closing come from the same
FanGraphs projections a year apart. Does cushion also predict what happens on the field the next
season?
**Discussion:** The objection is narrower than the referees put it. The n+1 Opening Day projection
is not carried forward from n: it takes in season n's results and the winter's roster changes. What
remains is persistent club-specific forecast error (§4b) and the projections' shrinkage toward the
mean. The refit is run because realized contention is the outcome a front office cares about, and
because it answers the objection with a result rather than an argument. It is written up as cushion
against realized outcomes, not as a test of whether the result is an artifact.
**Chose:**
- **Rows and covariates:** the F rows of M2, unchanged. Fixed line from `hazard_pp.csv`;
  berth-relative from `hazard_robustness_pp.csv` (variant `berth`). Covariates as in M2: ln(duration,
  capped at 4), era12, strength (cushion), Opening Day payroll. Only the event changes.
- **Events, season n+1:** (i) not contending by Jordan's (2018) rule as implemented in `jordan.py`
  (2020 scaled; ties for first broken by the actual title), extended to 2026; (ii) did not make the
  postseason (end-of-season postseason odds below 0.999). Records and fields come from the FanGraphs
  end-of-season snapshot, which includes 2026, so rows with n = 2025 are kept.
- **Primary pairings, matched by meaning:** fixed line with Jordan-contending (fixed 6 is "in the
  field or the first club out" before 2022, closer to Jordan's broader contention); berth-relative
  with postseason ("projected to make the playoffs"). The other two pairings are reported alongside.
- **Model:** M2 only. Standard errors clustered by club; p-values against t with G − 1 df; t-based
  95% intervals. Also the realized-outcome rate by cushion band (≤ 2, > 2–5, > 5–8, > 8 wins), the
  bands of `closing_by_strength_band`, which were set 2026-11-02 after the baseline results were seen.
- **Decision rule:** the cushion result carries over to realized outcomes if cushion's odds ratio is
  below 1 with a t-based interval excluding 1 in both primary pairings. If one pairing passes, the
  write-up says which. If neither does, the headline becomes that windows, as defined, track the
  projections' own persistence.
- **2020:** rows with n + 1 = 2020 keep era12 = 0, as in M2; their count is reported, because a
  16-team field makes the postseason outcome easier that year.
**Seen when deciding:** M2's results in every definition and both referee reports. Fixed before the
refit is run.
**Also:** risk-register row "Strength result partly reflects projections agreeing with themselves"
(Medium) reworded to persistent club-specific forecast error (Low–Medium), mitigated by this refit.

## 2026-11-11 — Numbers the abstract quotes; t-based intervals in prose

**Question:** The abstract will quote figures not yet in `results.json`, and the stored intervals are
normal-reference while the prose quotes t(G − 1) p-values. At top 7 the normal interval for ln
duration excludes 1 while p_t = 0.055 (both referee passes, 2026-11-04).
**Chose:** Add a `writeup_numbers` key: t-based 95% intervals (t with G − 1 df) for M2 and M2b in F,
L and H and for M2 in every variant; counts across the nine definitions for strength and ln duration;
the share of in-window club-seasons inside windows of four or more seasons, for both lines; and
contention rates in 2014–2025 under fixed top 6, berth-relative and Jordan's rule. Intervals quoted
in prose are the t-based ones, matching the p-values. The normal intervals stay in `results.json` and
in tables.
**Why:** Arithmetic on stored values; no new model. Keeps the rule that no number in a write-up is
typed by hand.

## 2026-11-11 — Prose leads with berth-relative; fixed top 6 stays registered

**Question:** The author finds the berth-relative line ("projected to make the playoffs") more
intuitive and asked whether it should become primary.
**Options:** Keep fixed 6 primary, prose order unchanged | Lead the prose with berth-relative, fixed 6
still the registered line | Make berth-relative primary, with a disclosure
**Chose:** Lead the prose with berth-relative. Fixed top 6 remains the registered line and is reported
with equal prominence in every table and in the abstract; the primary designation is unchanged.
**Why:** Readability is a legitimate reason to change the order of presentation. Re-designating the
primary after results were seen is what "Berth-relative threshold reported with equal prominence in
Post 1" (2026-11-01) ruled out, and doing it while considering an age claim that only berth-relative
supports would choose the line by its result. Every result that holds on one line and not the other
is stated as such.

## 2026-11-11 — Age checks on the berth-relative line: specification and decision rule

**Question:** Age (ln duration, M2) is significant on the berth-relative line (OR 3.97, p_t = 0.016)
and not at fixed top 6 (1.72, p_t = 0.30). Both referee passes (2026-11-04) said the write-up cannot
say "no claim" on age. Can it say that older windows were more likely to close, relative to the size of
the playoff field?
**Chose:** Eight checks, run on both lines in sample F; the rule applies to berth-relative.
1. Firth-penalized logit (Firth 1993), with a penalized likelihood-ratio test for ln duration.
2. Two-way clustering by club and by league-season (league × season n+1), p-values and intervals
   against t with min(G) − 1 df.
3. Wild score bootstrap for ln duration (Kline & Santos 2012; Webb weights; 9,999 draws), as for
   strength on 2026-11-02.
4. Leave-one-club-out refits of M2.
5. Functional form: M2b (first-year indicator), M1 bins and the bins-vs-log test, from existing keys.
6. M2 without strength (age's total association, not net of cushion).
7. M2 dropping rows whose window line changes between n and n+1 (n = 2019, 2020, 2021 for
   berth-relative: 5 to 8, 8 to 5, 5 to 6).
8. M2 with an ln duration × era12 interaction.
**Decision rule (berth-relative):** the abstract states that older windows were more likely to close
only if all of these hold: (a) the t-based 95% interval for ln duration in M2 excludes 1; (b) under
Firth the odds ratio is above 1 with penalized LR p < 0.05; (c) under two-way clustering the t-based
interval excludes 1; (d) the wild score bootstrap p < 0.05; (e) no single club's removal makes the
t-based interval include 1; (f) the odds ratio stays above 1 when the line-change rows are dropped.
Checks 5, 6 and 8 are descriptive and inform the wording only. If the rule holds, the abstract also
says the effect does not appear at the registered top-6 line and that age was examined after results
were seen. If it fails, the abstract says age effects are imprecise and depend on where the line is
drawn, with no definition showing established windows to be more durable.
**Seen when deciding:** M2 in all nine definitions; both referee reports. Fixed before any check is
run.

## 2026-11-11 — Baseball-Reference replication of the age pattern: not run

**Question:** Should berth-relative windows be rebuilt from Baseball-Reference preseason odds
(2011–2026, already collected) to test the age pattern on a second instrument?
**Chose:** No.
**Why:** Baseball-Reference rates clubs on their last 100 games with regression to the mean, not on
player projections, so its "window" means recent performance rather than projected contention. It is
not the same construct, and a miss could not be told apart from that difference.

## 2026-11-11 — Write-up figures after the abstract

**Chose:** The reviewer draft carries the cushion table for both lines as text. The survival figure
(cut at year 6) and a cushion chart are built after the abstract, for the paper.
**Why:** The SABR abstract is plain text unless SABR says otherwise, and the table carries the same
information as the chart. The survival figure's open design choices (which lines; the year-6 label)
are settled when it is built.

## 2026-11-11 — Referee pass on the analysis: disposition

**Record:** The referee pass on the analysis (plan §11) was run twice, by accident, on 2026-11-04, in
fresh Incognito chats with the same prompt and packet (`posts/post1-hazard/referee-1/`). The two
reports agree on every major point.
**Adopted:**
- **Age.** "No claim in either direction" (2026-11-02, "Robustness variants run", write-up framing)
  is superseded. Age is reported as unresolved, or as the claim allowed by the rule in "Age checks on
  the berth-relative line" (2026-11-11). The berth-relative age estimate is reported with equal
  prominence.
- **"Windows are short."** Not used as a claim: survival is reported with its dependence on the
  line and without the word.
- **Jordan comparison.** The survival comparison (0.56 vs. 0.21) is not used in the abstract, because
  Jordan's rules (two seasons to open, two to close) build in length. The club-season disagreement
  is kept. A rule-swap decomposition is deferred to the paper.
- **Cushion vs. projection persistence.** Answered by the realized-outcome refit (2026-11-11).
- **Intervals.** t-based intervals in prose (2026-11-11).
- **Disclosure.** The abstract says the analysis is exploratory and that the emphasis on cushion was
  chosen after results were seen.
**Not adopted, with reasons:**
- **Persistence benchmark** (simulate windows from year-to-year cushion movement). Deferred to the
  paper; not needed once "short" is dropped as a claim.
- **The referees' framing of the persistence objection.** The n+1 projection updates on season n's
  results and roster changes, so "the forecast remembers" overstates it (2026-11-11).
**Deferred to the paper:** M2 without cushion and entry cushion beyond the age checks; hysteresis
variant; survival under L and H; size check with a club random intercept; refits dropping 2020 and
the early-snapshot seasons; an odds-gap version of cushion; Jordan against the berth-relative line.
**Forking paths, recorded:**
- The cushion bands (≤ 2, > 2–5, > 5–8, > 8 wins) were set 2026-11-02, after the baseline M2
  results (2026-10-26) were seen and before any variant was run.
- "Week 3 robustness specification" (2026-11-01) was written with the baseline M2 results known; it
  was fixed before any Week 3 result.
- `predictions.md` registers no prediction about duration dependence. Its note on the baseline
  threshold says a looser line gives "longer measured windows and a flatter hazard, which works
  against the thesis," which implies short windows were expected.
- **Seen when deciding** the 2026-11-02 write-up framing (in "Robustness variants run", "Small-cluster
  inference run" and "Jordan comparison and berth-relative cushion table run"): M2 in all nine
  definitions, the small-cluster inference and the Jordan comparison.
**Size check (2026-11-02):** an implementation check with independent outcomes, not a test of
within-club dependence; described that way in the write-up.

## 2026-11-11 — Corrections: snapshot dates and season-end records

**Record:**
- **2014 Opening Day.** LAD and ARI opened in Sydney on March 22–23, 2014, before the first archived
  date (March 29), yet both show 0–0 on it. The "all clubs 0–0" check (2026-11-03) does not show the
  snapshot predates every game. The gap is logged with the 2019, 2024 and 2025 gaps; no change made.
  LAD's 2014 window is left-censored and not in F.
- **2020 Opening Day** is 2020-07-22 in `odds.csv`. "2020 retained for rank-based analysis"
  (2026-09-21) gave 2020-07-23.
- **2022 deadline:** August 2. The pre-deadline snapshot (July 26) is exactly 7 days before, as the
  2026-11-03 rebuild found. Replaces "Aug 1 or 2" in plan §3.2.
- **Season-end records:** the W-L used for Jordan's rule are FanGraphs' actual records in the
  end-of-season snapshot, including 2026. The differences noted in "Corrections from the odds audit"
  (2026-10-18) were in projected records. The Baseball-Reference cross-check is optional.
- **Era labels:** "12 closings in the 10-team era" (2026-11-02) groups 2020's 16-team season with the
  10-team seasons, as M2's era term does.
- **L and H** are alternative assumptions about the age of windows open in 2014. They bound the age
  assigned, not the estimates.

## 2026-11-11 — No publication before the abstract

**Chose:** Nothing from the project is published before the SABR abstract is submitted. Afterward,
the author may share it privately.
**Open:** whether SABR accepts work published between submission and the March 2027 conference,
which decides the FanGraphs timing. Put to SABR by email.

## 2026-11-11 — Realized-outcome refit and age checks run (Post 1)

**Record:** Run as specified in "Realized-outcome refit (Post 1): specification", "Numbers the
abstract quotes; t-based intervals in prose" and "Age checks on the berth-relative line" (all
2026-11-11). Three new keys, `realized_outcome_refit`, `writeup_numbers` and `age_checks`; every
existing key byte-identical. All twelve checks passed. Refitting M2 with the original event reproduces
the stored M2 on both lines; Jordan's rule extended to 2026 reproduces the stored 2014–2025 counts;
the strength bootstrap reproduces exactly.
**Implementation choices, accepted on review:**
- Two-way covariance was not positive semi-definite on either line (smallest eigenvalue −0.031 fixed,
  −0.18 berth-relative); the Cameron–Gelbach–Miller eigenvalue fix was applied. Without it the
  berth-relative interval is narrower (1.49–10.59), so the fix is the conservative choice.
- Firth is reported as odds ratios and a penalized likelihood-ratio test, without an interval.
- Leave-one-club-out "flips" are defined only where the full-sample interval excludes 1.
**Independent check:** In the planning chat, with separate code from the processed files: Jordan's
rule rebuilt (147 contending, 2014–2025); all four realized-outcome fits, the band tables, M2 without
strength, the line-change refit, leave-one-club-out, Firth (by direct penalized maximization) and the
berth-relative long-window counts reproduced. The score statistic reproduced exactly; the bootstrap p
with a separate seed and 200,000 draws was 0.018 (berth-relative) and 0.26 (fixed).
**Results, for the record:**
- **Realized outcomes:** cushion's odds ratio per projected win is 0.84 (t interval 0.75–0.94) for
  fixed top 6 against Jordan-contending, and 0.83 (0.73–0.94) for berth-relative against making the
  postseason. `cushion_passes` is true for both primary pairings; the other two pairings also exclude 1.
  By band, the failure rate is similar at ≤ 2 and > 2–5 wins (0.56 and 0.60, fixed/Jordan) and falls
  above 5 wins (0.33; > 8 wins, 4 of 23).
- **Age, berth-relative:** all six conditions of the rule hold (`age_rule_passes` true): t interval
  1.32–11.9; Firth 3.56, penalized LR p 0.005; two-way interval 1.36–11.6; bootstrap p 0.017; no
  single club's removal puts 1 in the interval (odds ratios 3.40–4.95); 5.67 without the line-change
  rows.
- **Age, fixed top 6:** no check shows an effect (Firth p 0.08; bootstrap p 0.25; every
  leave-one-club-out interval includes 1).
- **Age without cushion:** odds ratio 1.26 (p_t 0.65) berth-relative and 0.81 (p_t 0.65) fixed. The age
  effect appears only with cushion held fixed: older windows do not close more often overall, because
  surviving windows tend to carry more cushion.
- **Writeup numbers:** windows of four or more seasons hold 90 of 156 in-window club-seasons (fixed)
  and 77 of 146 (berth-relative). Contention, 2014–2025: 144 fixed, 134 berth-relative, 147 Jordan, of
  360.

## 2026-11-11 — Age sentence for the abstract

**Chose:** "On the berth-relative line, among windows with the same Opening Day cushion, older windows
were more likely to close (odds ratio 3.97 per log-season; 95% interval 1.32–11.9), robust to
penalized estimation, two-way clustering, a cluster bootstrap and dropping any single club. Older
windows did not close more often overall, because the windows that survive tend to be the ones with
more cushion, and the effect does not appear at the registered top-6 line." Numbers from
`writeup_numbers` and `age_checks`; may be trimmed for length, keeping the conditional clause and the
top-6 clause.
**Basis for "surviving windows carry more cushion":** mean Opening Day cushion rises with window age
on both lines (fixed: 2.4 wins at age 1, 7.0 at 4+; berth-relative: 2.9 and 7.8; correlation with ln
age 0.43 and 0.45, sample F). Stated in words in the abstract; these figures are not in `results.json`.
Whether cushion grows inside surviving windows or only high-cushion windows survive is not separated.
**Revises** the disclosure in "Referee pass on the analysis: disposition" (2026-11-11): no
age-specific "examined after results" clause. The abstract's statement that the analysis is
exploratory, and that the age effect does not appear at the registered line, carry it; the detail
stays here and in the paper.
