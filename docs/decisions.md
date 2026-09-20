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
