# Referee packet: Post 1, the hazard of MLB contention windows

## A. Design (verbatim from the research plan)

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
know it. On 2026-11-02 the Week 3 robustness variants, small-cluster inference and Jordan comparison
were run, with their results seen (`decisions.md`, 2026-11-02). Transactions have still not been pulled.

#### Three snapshots per season

| Snapshot | Date rule | What it establishes | Confirmed by |
|---|---|---|---|
| **Opening Day (OD)** | First archived date of the season, from the page's own date list | Ex-ante position: is the club in a window this season? | 15 clubs per league; Make Playoffs sums to the season's berth count; any gap between first archived date and actual Opening Day logged |
| **Pre-deadline (PD)** | Archived date nearest to 7 days before the deadline | What was publicly visible when the club had to decide | Date falls before the deadline; Make Playoffs sums to berth count |
| **End of season (EOS)** | Last archived regular-season date | What actually happened: final record, realized qualification | Clubs at 100% Make Playoffs match the actual postseason field; final W-L matches Baseball-Reference |

**Deadline dates:** July 31 (2014–2015, 2017–2019, 2025); Aug 1 (2016 — July 31 was a Sunday); Aug 31 (2020);
July 30 (2021, 2024); Aug 1 (2023); Aug 1 or 2 (2022 — sources conflict by one day, immaterial); Aug 3 (2026).

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
   itself an output. With the line fixed at 6, the term asks whether a top-6 club's closing risk
   changed once 6th became a playoff spot (rank 6 moved from one spot outside the field to the last
   spot inside it). Under the berth-relative line it is not read as a format effect, because that
   line also moves at 2022.
2. **Berth-relative threshold** as a robustness variant — rank equal to berths per league:
   5 (2014–2019, 2021), 8 (2020), 6 (2022 on).
   In Post 1 it is reported with equal prominence alongside the fixed rank-6 baseline (decided
   2026-11-01, before its results were seen). It equals top 5 in 2014–2019 and 2021, top 8 in 2020
   and top 6 from 2022, so where it differs from the baseline, the difference comes mainly from the
   five-team era, not from the change at 2022.
3. **Era-stratified fitting** was listed as a secondary check where power allows. It is not run: F
   has 12 closings in the 10-team era and 18 in the 12-team era (`decisions.md`, 2026-11-02).

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
agreement against 85% required) and is not used. Under rules that tolerate a one-season gap, the
same principle drops more: grace-rule spells starting in 2015 (a club out on 2014 Opening Day may
have been in a dip from a window open in 2013), and Jordan windows unless two straight
non-contending seasons occur between 2014 and the window's first contending season.

**Optional descriptive context.** Realized postseason qualification going back decades is
available from Retrosheet or Baseball-Reference — an outcome, not ex-ante, so it cannot carry
the hazard model, but it can bound the question in a labeled section.

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
- **Robustness (fixed 2026-11-01; run 2026-11-02).** The eight variants (thresholds 3, 4, 5, 7, 8, 9;
  berth-relative; grace) run in F only. Strength in each is measured against the first club out at
  its threshold; bins stay at 1, 2, 3, 4+, and a zero-closing bin is reported as a raw count with an
  exact interval. Grace: a window closes after two straight Opening Days out; dip seasons count
  toward age but are not rows; rows run through 2024. Every clustered result also gets t(G − 1)
  p-values; strength in M2 (F) gets a wild score bootstrap (Kline & Santos, 2012; Webb weights;
  9,999 draws) with a size check.
- **Comparison with Jordan (2018).** His ex post rule (division winner, wild card, 2nd or 3rd within
  5 games of the division winner, or 87+ wins; opens after two contending seasons; closes after two
  non-contending) applied to the same 2014–2025 seasons from actual season-end records. 2020 scaled
  to 60 games (.537; 1.85 games). Ties for a division title since 2022 are broken by the actual
  title. Records stop at 2025, so no definition uses information from the 2026 season. Description
  only. Reinhart (2018) cited, not replicated.
- **Week 3 results (2026-11-02; detail in `decisions.md`).**
  - Strength: odds ratio below 1 in all nine definitions (0.59–0.84 per projected win of cushion),
    interval excluding 1 in eight (not top 4). Holds under small-cluster inference: p = 0.0033 on
    t(21); wild score bootstrap 0.0003.
  - Duration: changes sign across definitions; no definition shows a detectable protective effect of
    age.
  - Era and payroll: not detected in any definition.
  - Jordan: ex post windows run longer (survival after 4 years 0.56 vs. 0.21 strict), and about a
    third of each definition's contenders are not contenders under the other.
- **Write-up framing (2026-11-02).**
  - The two lines, for readers: berth-relative is "projected to make the playoffs on Opening Day";
    fixed 6 is "projected in the field or the first club out" before 2022, and exactly the field
    from 2022. Fixed 6 stays primary because it was registered and its yardstick does not move
    across formats; equal prominence stands.
  - Headline: cushion, not age, predicts whether a window survives. No duration-dependence claim in
    either direction. Cushion tables are reported for both lines.
  - Prose quotes the most conservative p-value (t with G − 1 df); the others appear in the table.
  - The Jordan comparison is presented as what the ex ante definition changes.
  - The published survival figure stops at year 6; full life tables stay in `results.json`.
- This is the SABR abstract. It needs only the odds snapshots.
- **Reminder for the write-up:** state clearly why the threshold is what it is, and defend it.
  Frame the deadline difference between favorites and bubble clubs as **the same goal (titles)
  producing different returns**, not different goals. A favorite's playoff odds are already near
  the ceiling, so any gain shows up in title odds; a bubble club gains a lot of playoff odds and
  little title odds. Note that a bubble club buying its way into October may be making an
  owner-economics decision (Frame B), and that after 2022 favorites also buy for the first-round
  bye, which is about seeding.

## B. Decision log, Post 1 entries (verbatim, in date order)

Entries about later posts (trades, valuations, P1–P4) are omitted. 'Chose (write-up)' lines are the claims the abstract intends to make.

### 2026-09-20 — Window threshold: within-league, not across all 30
 
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

### 2026-09-20 — Strict consecutive windows; grace rule demoted
 
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

### 2026-09-20 — Persistent contenders reported as a named category
 
**Question:** How to handle clubs that never fall below threshold in the sample.
**Options:** Exclude them | Force them into the hazard model silently | Name them as a category
**Chose:** Retain as right-censored spells in the model, and report them separately with a count.
**Why:** Right-censoring is the statistically correct handling, but these clubs contribute little
to hazard estimation while having the most conversion capacity in the sample. Stating "N clubs
never left contention; the hazard describes the remainder" is more honest than a curve that
quietly excludes the most interesting cases, and the count is a finding in its own right.
**Revisit if:** the persistent-contender count is large enough that the hazard describes only a
minority of clubs, which would require rethinking the threshold.

### 2026-09-21 — Ranking variable, view, and projection mode fixed
 
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

### 2026-09-21 — Study period extended to 2014–2026
 
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

### 2026-09-21 — Berth-count shift handled as a robustness variant  **[2020 value extended 2026-09-27 — see "2020 postseason odds reconstructed"]**
 
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

### 2026-09-21 — Format change handled three ways, not defined away
 
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

### 2026-09-22 — No FanGraphs methodology break assumed; breaks tested empirically instead
 
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

### 2026-09-22 — Projection mode fixed at `fg`
 
**Question:** Which of the six projection modes (fg, ATC, THE BAT X, OOPSY, season-to-date, coin
flip) is the instrument?
**Chose:** `fg`, the site default, for the full panel.
**Why:** It is a consistent ZiPS/Steamer blend across the study period, it is what a front office
or journalist would actually have seen, and it is what a reader reproduces without extra steps.
The construct being measured is *publicly visible signal*, not best-available forecast — so the
default is correct on grounds of construct validity, not convenience. Fixed now, before any
mode's results have been seen; six modes are six different answers.
**Revisit if:** never, absent evidence `fg` is unavailable for some season in the panel.

### 2026-09-27 — 2020 postseason odds reconstructed  **[Condition met — confirmed by the author 2026-10-18]**
 
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

### 2026-09-28 — Data-examination wording corrected
 
**Question:** Several entries say choices were made "before any data was examined." Instrument
structure was examined: FanGraphs berth sums, the strength-of-schedule column, 2020 page structure,
and the archive's date range.
**Chose:** Read every such phrase as **"before any outcome or transaction data was examined."** No
outcome variable, window, spell count or transaction was observed before any decision in this log.
**Correction:** the 2026-09-21 entry states Win WS is "nearly flat across ranks 6–12 (inside model
noise)." That was an assertion from general knowledge, not an observation, and was not measured. The
R4 probe will measure it. The threshold decision does not rest on it; the P4-tautology argument in
the same entry stands on its own.

### 2026-10-17 — Odds collected; what has been seen
 
**Record:** All FanGraphs playoff-odds snapshots planned for the project were collected by
2026-10-17. Transactions and valuations have not been pulled.
**Consequence:** Analyses resting only on the odds — window definitions and the Post 1 hazard — are
exploratory from here: their specifications were set before collection, but any change made now is
made with the data in view, and is logged with its date. P1's behavioral side and P4 depend on
transaction data not yet seen and remain confirmatory.
**Context, stated plainly:** the author lived through 2014–2026, inside a front office through 2016
and as an industry observer since. No researcher of this period is a blank slate. The safeguard is
fixing analysis choices before the transaction data is seen, not ignorance of history.

### 2026-10-18 — 2020 reconstruction confirmed
 
**Record:** The author confirmed the 2020 data is correct, closing the condition attached to "2020
postseason odds reconstructed." 2020 is used in both rank-based and level-based analysis.

### 2026-10-18 — Windows stay defined on Opening Day
 
**Question:** Should windows be defined at the trade deadline, when more information is available?
**Options:** Opening Day primary | Deadline primary | Both
**Chose:** Opening Day stays primary. How contention changes between Opening Day and the deadline is
written about directly through the window patterns (§3.3b).
**Why:** Deadline rank includes roughly 100 games of results, partly luck, so it mixes what was
expected with what happened. P1's signal already uses deadline rank; defining windows the same way
would collapse "in a window" into "the signal." And the patterns depend on the Opening Day vs.
deadline contrast.

### 2026-10-18 — Corrections from the odds audit
 
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

### 2026-10-20 — Spell count (go/no-go): proceed
 
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

### 2026-10-26 — Left-censored spells: flow sample primary, bounds and backcast reported
 
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

### 2026-10-26 — Baseball-Reference Opening Day odds as backcast source
 
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

### 2026-10-26 — Hazard model specification (Post 1)

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

### 2026-10-26 — Backcast validation failed; sample B not used

**Record:** Baseball-Reference preseason odds collected for 2011–2026 (480 club-seasons). All parsing
checks passed. Top-6 agreement with FanGraphs' Opening Day top 6, 2014–2026: 302 of 390 (77.4%),
below the 85% gate fixed before collection. By season: 67%–93%. Among the 12 clubs whose spells were
open in 2014: 9 of 12 in 2014.
**Consequence:** Sample B is not used. Left-censored spells are handled by the flow sample (primary)
with L and H as bounds, as decided earlier today. Backcast entry durations remain on disk, unused.
**Retained:** 2014–2026 B-Ref ranks, for the parked P2 benchmark and windows robustness check.

### 2026-10-26 — Payroll covariate for the Post 1 hazard

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

### 2026-10-26 — Payroll data: collection notes and 2020

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

### 2026-10-26 — Deadline status in the Post 1 hazard: description only

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

### 2026-10-26 — Hazard run: implementation choices

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

### 2026-11-01 — Plan v0.29; division strength and market size in Post 1

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

### 2026-11-01 — Week 3 robustness specification (Post 1)

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

### 2026-11-01 — Berth-relative threshold reported with equal prominence in Post 1

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

### 2026-11-02 — Week 3 prompts: left-censoring under gap-tolerant rules; Jordan reference

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

### 2026-11-02 — Robustness variants run (Post 1)

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

### 2026-11-02 — Small-cluster inference run (Post 1)

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

### 2026-11-02 — Jordan comparison: ties for a division title

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

### 2026-11-02 — Jordan comparison and berth-relative cushion table run (Post 1)

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

### 2026-11-02 — Era-stratified fitting not run (Post 1)

**Question:** §3.3a lists era-stratified fitting as a secondary check "where power allows." Does it?
**Chose:** No; not run. The pooled era term remains the format test.
**Why:** In F, 12 closings come from 10-team-era rows (47 rows) and 18 from 12-team-era rows (55).
M2 fit within an era estimates four numbers (era drops out), about 3 closings per number in the
earlier era, below the 5–10 used when M2 was specified (2026-10-26). Decided on these counts alone,
with no stratified model fit.

### 2026-11-03 — Review steps before the abstract

**Question:** The plan had one referee pass, in Week 5 after reviewers read a draft, and no check of
the processed data against the raw files. Is that enough before the abstract?
**Chose:** Three steps before drafting: an independent rebuild of the processed files from
`data/raw/`; a hand spot check of five raw values against the FanGraphs pages; a referee pass on the
analysis in a fresh chat. A second referee pass runs on the draft in Week 5. A human technical
reviewer reads the model after the abstract and before the full Post 1.
**Why:** Every Week 1–3 check rebuilt results from the processed files, so an error in cleaning
would have passed all of them. A referee pass after reviewers have read a draft finds a fatal
objection too late to answer it cheaply.

### 2026-11-03 — Processed data rebuilt from raw; Opening Day snapshot gaps

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

### 2026-11-03 — Five raw values spot-checked against FanGraphs

**Record:** Checked by hand against the archived FanGraphs playoff-odds pages, all matching: 2014
Opening Day TBR and CLE; 2025 Opening Day HOU and BAL; 2020 Opening Day CHW (the three components of
the rebuilt postseason probability); 2023 pre-deadline MIA; 2019 end of season MIL. This closes the
column-labeling gap noted under "Not covered" in the entry above.

### 2026-11-03 — Correction: strict survival after four years

**Record:** Strict (fixed top 6, sample F) survival after four years is 0.21:
`hazard_robustness/variants/top6/survival_after/4` = 0.2148, matching
`jordan_comparison/definitions/strict/survival_after/4`. "Jordan comparison and berth-relative cushion
table run (Post 1)" (2026-11-02) and plan §5 in v0.30–v0.31 gave 0.22. Found while building the
abstract's numbers manifest. No result changes; the plan is corrected in v0.32 and the 2026-11-02 entry
stands as written.

### 2026-11-03 — SABR call checked

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

## C. Results (generated from results.json; numbers rounded for display)

### C1. Definitions used in the files
- **hazard**: window_top6, strict consecutive spells. One row per spell per season n, 2014-2025 (2026 excluded: 2027 not observed). event = 1 if out of the window at season n+1's Opening Day. era12 = 1 if n+1 >= 2022. strength = 162 x (Opening Day proj_w/(proj_w+proj_l) minus that of the league's od_rank-7 club), season n. od_log2_rel from payroll.csv, season n. pd_above = pd_rank <= 6 in season n.
- **samples F / L / H**: F: Left-censored spells dropped; duration = duration_obs. Primary. | L: All spells; left-censored spells enter in 2014 at duration 1. | H: All spells; left-censored spells enter in 2014 at the top bin (4+) and stay there: bin 4+, ln(duration capped at 4) = ln 4, duration-1 indicator 0. In the exact-duration life table they enter at duration 4 and count up (duration_obs + 3); 'entered' counts these delayed entries.
- **models**: Discrete-time logit. M2/M2b: standard errors clustered by team_id (statsmodels cluster, default small-sample correction G/(G-1) x (N-1)/(N-K)); intervals are Wald, normal reference. LR test uses the ordinary likelihood: M1 (4 bin parameters) vs. intercept + ln(duration capped at 4), df 2.
- **robustness**: Post 1 hazard (hazard.py's M1, M2, M2b and bins-vs-log test) under the pre-specified window variants, flow sample F only. Strength = wins per 162 above the first club out at the variant's threshold (reference_rank). Era, payroll and the duration cap (4) as at baseline. Bins fixed at 1, 2, 3, 4+. M2/M2b standard errors clustered by team_id (statsmodels default small-sample correction); intervals Wald, normal reference; p_normal against the normal, p_t against t with G - 1 df (G = clubs in F). Grace: closes after two straight Opening Days out; dip seasons are not rows but count toward duration; closing recorded in the last in-window season; rows through 2024; spells starting 2014-2015 left-censored.
- **small-cluster inference**: Small-cluster inference per docs/decisions.md 2026-11-01 item E. t_correction: p_t = 2 x t_{G-1} tail at the clustered z in hazard.models (G = clubs); p_normal is hazard's normal-reference p. score_bootstrap: Kline & Santos (2012) wild score bootstrap for strength in M2, sample F, restricted fit M2 without strength, Webb weights by club, no refitting, H fixed at the restricted estimates; p_bootstrap = share of draws with |T*| >= |T|; p_normal = 2 x normal tail at T; no small-sample scaling. size_check: the same test on datasets simulated under the restricted model.

### C2. Windows at the baseline (fixed top 6, strict), 2014–2026
- Window spells: 53; club-seasons in a window: 156; open in 2014 (left-censored): 12; still open in 2026: 12; in a window every season (persistent): 1
- Spell length distribution (length: count): 1: 21, 2: 12, 3: 7, 4: 3, 6: 4, 7: 2, 8: 1, 9: 1, 10: 1, 13: 1
- Model rows (club-seasons at risk), closings, windows, clubs: F 102 rows, 30 closings, 38 windows, 22 clubs; L 144 rows, 41 closings, 50 windows, 26 clubs; H 144 rows, 41 closings, 50 windows, 26 clubs

### C3. Life table, baseline, sample F
| Age (seasons) | At risk | Closed | Censored | Hazard | Still open |
|---|---|---|---|---|---|
| 1 | 38 | 13 | 4 | 0.34 | 0.66 |
| 2 | 21 | 5 | 2 | 0.24 | 0.50 |
| 3 | 14 | 5 | 0 | 0.36 | 0.32 |
| 4 | 9 | 3 | 0 | 0.33 | 0.21 |
| 5 | 6 | 0 | 0 | 0.00 | 0.21 |
| 6 | 6 | 2 | 1 | 0.33 | 0.14 |
| 7 | 3 | 0 | 0 | 0.00 | 0.14 |
| 8 | 3 | 1 | 1 | 0.33 | 0.10 |
| 9 | 1 | 0 | 0 | 0.00 | 0.10 |
| 10 | 1 | 1 | 0 | 1.00 | 0.00 |

### C4. M1 (age bins only), sample F
| Bin | Rows | Closings | Hazard | 95% interval (clustered) |
|---|---|---|---|---|
| 1 | 38 | 13 | 0.34 | 0.20–0.52 |
| 2 | 21 | 5 | 0.24 | 0.10–0.48 |
| 3 | 14 | 5 | 0.36 | 0.18–0.59 |
| 4+ | 29 | 7 | 0.24 | 0.12–0.42 |

Bins vs. ln(age) likelihood-ratio test (F): LR = 0.86, df = 2, p = 0.6498

### C5. M2, sample F (clubs = 22)
| Term | Odds ratio | 95% interval | p (normal) | p (t, G−1) |
|---|---|---|---|---|
| ln_dur | 1.722 | 0.633–4.689 | 0.2874 | 0.2995 |
| era12 | 1.212 | 0.509–2.885 | 0.6640 | 0.6684 |
| strength | 0.723 | 0.596–0.876 | 0.0009 | 0.0033 |
| od_log2_rel | 0.946 | 0.436–2.051 | 0.8886 | 0.8900 |

### C5. M2b, sample F (clubs = 22)
| Term | Odds ratio | 95% interval | p (normal) | p (t, G−1) |
|---|---|---|---|---|
| dur1 | 0.547 | 0.201–1.487 | 0.2370 | 0.2502 |
| era12 | 1.205 | 0.514–2.824 | 0.6687 | 0.6730 |
| strength | 0.722 | 0.594–0.876 | 0.0010 | 0.0034 |
| od_log2_rel | 1.052 | 0.486–2.275 | 0.8979 | 0.8991 |

### C5. M2, sample L (clubs = 26)
| Term | Odds ratio | 95% interval | p (normal) | p (t, G−1) |
|---|---|---|---|---|
| ln_dur | 1.522 | 0.729–3.175 | 0.2634 | 0.2740 |
| era12 | 0.809 | 0.383–1.710 | 0.5795 | 0.5844 |
| strength | 0.713 | 0.605–0.841 | 5.7e-05 | 0.0005 |
| od_log2_rel | 0.893 | 0.432–1.846 | 0.7603 | 0.7628 |

### C5. M2b, sample L (clubs = 26)
| Term | Odds ratio | 95% interval | p (normal) | p (t, G−1) |
|---|---|---|---|---|
| dur1 | 0.594 | 0.281–1.258 | 0.1738 | 0.1859 |
| era12 | 0.809 | 0.384–1.705 | 0.5771 | 0.5821 |
| strength | 0.710 | 0.596–0.846 | 0.0001 | 0.0008 |
| od_log2_rel | 0.955 | 0.460–1.983 | 0.9022 | 0.9032 |

### C5. M2, sample H (clubs = 26)
| Term | Odds ratio | 95% interval | p (normal) | p (t, G−1) |
|---|---|---|---|---|
| ln_dur | 2.049 | 0.836–5.019 | 0.1166 | 0.1292 |
| era12 | 1.002 | 0.442–2.276 | 0.9953 | 0.9953 |
| strength | 0.694 | 0.580–0.831 | 6.8e-05 | 0.0005 |
| od_log2_rel | 0.852 | 0.398–1.823 | 0.6795 | 0.6830 |

### C5. M2b, sample H (clubs = 26)
| Term | Odds ratio | 95% interval | p (normal) | p (t, G−1) |
|---|---|---|---|---|
| dur1 | 0.442 | 0.164–1.191 | 0.1066 | 0.1191 |
| era12 | 0.923 | 0.430–1.981 | 0.8370 | 0.8386 |
| strength | 0.696 | 0.580–0.835 | 9.9e-05 | 0.0007 |
| od_log2_rel | 0.967 | 0.461–2.028 | 0.9284 | 0.9292 |

### C6. Wild score bootstrap, strength in M2, sample F
- T = -3.276; bootstrap p = 0.0003 (3 of 9999 draws); normal p = 0.0011; clusters = 22
- Size check (500 null datasets, 999 draws each): rejection 0.068 at 5%, 0.106 at 10%; pass band [0.03, 0.07]

### C7. M2 under all nine definitions, sample F
| Definition | Windows | Rows | Closings | Clubs | Cushion OR (95%) | p_t | ln(age) OR (95%) | p_t | Era OR | p_t | Payroll p_t | Open after 1 / 2 / 3 / 4 | Bins-vs-log p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Baseline: top 6, strict | 38 | 102 | 30 | 22 | 0.723 (0.596–0.876) | 0.0033 | 1.72 (0.63–4.69) | 0.2995 | 1.21 (0.51–2.88) | 0.6684 | 0.8900 | 0.66 / 0.50 / 0.32 / 0.21 | 0.6498 |
| Berth-relative, strict | 36 | 97 | 28 | 23 | 0.667 (0.534–0.833) | 0.0017 | 3.97 (1.40–11.24) | 0.0164 | 0.60 (0.31–1.19) | 0.1581 | 0.5492 | 0.72 / 0.56 / 0.30 / 0.19 | 0.2642 |
| Top 3, strict | 22 | 53 | 18 | 17 | 0.589 (0.365–0.949) | 0.0450 | 0.47 (0.11–1.89) | 0.3008 | 1.41 (0.31–6.35) | 0.6594 | 0.7695 | 0.50 / 0.35 / 0.35 / 0.17 | 0.1475 |
| Top 4, strict | 29 | 65 | 23 | 20 | 0.838 (0.674–1.043) | 0.1294 | 0.49 (0.13–1.84) | 0.3014 | 0.78 (0.26–2.36) | 0.6637 | 0.6060 | 0.45 / 0.37 / 0.26 / 0.26 | 0.5336 |
| Top 5, strict | 29 | 84 | 23 | 20 | 0.615 (0.507–0.745) | 8.7e-05 | 7.38 (2.22–24.57) | 0.0042 | 0.63 (0.24–1.65) | 0.3615 | 0.3831 | 0.83 / 0.53 / 0.26 / 0.22 | 0.0704 |
| Top 7, strict | 37 | 110 | 29 | 22 | 0.708 (0.589–0.851) | 0.0014 | 2.91 (1.04–8.18) | 0.0549 | 1.29 (0.44–3.77) | 0.6490 | 0.3556 | 0.76 / 0.54 / 0.37 / 0.20 | 0.8634 |
| Top 8, strict | 35 | 122 | 23 | 25 | 0.735 (0.582–0.927) | 0.0159 | 4.13 (1.54–11.07) | 0.0094 | 0.63 (0.19–2.08) | 0.4512 | 0.8514 | 0.86 / 0.79 / 0.51 / 0.39 | 0.1142 |
| Top 9, strict | 34 | 125 | 19 | 24 | 0.733 (0.608–0.884) | 0.0036 | 1.66 (0.70–3.95) | 0.2631 | 0.36 (0.11–1.22) | 0.1134 | 0.9662 | 0.82 / 0.69 / 0.58 / 0.54 | 0.9410 |
| Top 6, grace | 20 | 65 | 12 | 18 | 0.775 (0.620–0.969) | 0.0387 | 0.83 (0.23–2.95) | 0.7748 | 2.28 (0.48–10.73) | 0.3129 | 0.4997 | 0.75 / 0.58 / 0.42 / 0.36 | 0.4148 |

Flags:
- Top 3, strict: zero-closing bin(s): 3

Threshold by season for the berth-relative line: 2014: 5, 2015: 5, 2016: 5, 2017: 5, 2018: 5, 2019: 5, 2020: 8, 2021: 5, 2022: 6, 2023: 6, 2024: 6, 2025: 6, 2026: 6

### C8. Life table, berth-relative line, sample F
| Age (seasons) | At risk | Closed | Censored | Hazard | Still open |
|---|---|---|---|---|---|
| 1 | 36 | 10 | 4 | 0.28 | 0.72 |
| 2 | 22 | 5 | 2 | 0.23 | 0.56 |
| 3 | 15 | 7 | 0 | 0.47 | 0.30 |
| 4 | 8 | 3 | 0 | 0.38 | 0.19 |
| 5 | 5 | 0 | 0 | 0.00 | 0.19 |
| 6 | 5 | 2 | 1 | 0.40 | 0.11 |
| 7 | 2 | 0 | 0 | 0.00 | 0.11 |
| 8 | 2 | 0 | 1 | 0.00 | 0.11 |
| 9 | 1 | 0 | 0 | 0.00 | 0.11 |
| 10 | 1 | 1 | 0 | 1.00 | 0.00 |

### C9. Closing rate by Opening Day cushion (projected wins per 162 above the first club below the line), sample F
Fixed top 6:

| Cushion | Club-seasons | Closed by next Opening Day | Share |
|---|---|---|---|
| <= 2 | 39 | 19 | 0.49 |
| > 2 to 5 | 25 | 7 | 0.28 |
| > 5 to 8 | 15 | 3 | 0.20 |
| > 8 | 23 | 1 | 0.04 |

Berth-relative:

| Cushion | Club-seasons | Closed by next Opening Day | Share |
|---|---|---|---|
| <= 2 | 30 | 15 | 0.50 |
| > 2 to 5 | 29 | 9 | 0.31 |
| > 5 to 8 | 16 | 3 | 0.19 |
| > 8 | 22 | 1 | 0.05 |

### C10. Life tables by cushion in a window's first season (split at the median, 1.69 wins), sample F
at or above median (19 windows):

| Age (seasons) | At risk | Closed | Censored | Hazard | Still open |
|---|---|---|---|---|---|
| 1 | 19 | 4 | 2 | 0.21 | 0.79 |
| 2 | 13 | 2 | 2 | 0.15 | 0.67 |
| 3 | 9 | 3 | 0 | 0.33 | 0.45 |
| 4 | 6 | 0 | 0 | 0.00 | 0.45 |
| 5 | 6 | 0 | 0 | 0.00 | 0.45 |
| 6 | 6 | 2 | 1 | 0.33 | 0.30 |
| 7 | 3 | 0 | 0 | 0.00 | 0.30 |
| 8 | 3 | 1 | 1 | 0.33 | 0.20 |
| 9 | 1 | 0 | 0 | 0.00 | 0.20 |
| 10 | 1 | 1 | 0 | 1.00 | 0.00 |

below median (19 windows):

| Age (seasons) | At risk | Closed | Censored | Hazard | Still open |
|---|---|---|---|---|---|
| 1 | 19 | 9 | 2 | 0.47 | 0.53 |
| 2 | 8 | 3 | 0 | 0.38 | 0.33 |
| 3 | 5 | 2 | 0 | 0.40 | 0.20 |
| 4 | 3 | 3 | 0 | 1.00 | 0.00 |

### C11. Deadline status in season n vs. closing at n+1's Opening Day (description only; not in the model)
| Sample | Above the line at the deadline: closed | Below the line at the deadline: closed |
|---|---|---|
| F | 9 of 64 | 21 of 38 |
| L | 16 of 98 | 25 of 46 |
| H | 16 of 98 | 25 of 46 |

### C12. Comparison with Jordan (2018), ex post, 2014–2025
- Definition: Jordan (2018) contending season, end_of_season snapshot, 2014-2025: division winner (division order by W%; ties for first broken by the actual division title, see ties_for_first; ties below first share the better rank); postseason as a non-division-winner (postseason_odds >= 0.999); 2nd or 3rd in the division with games behind the division winner <= 5 (games behind = ((leader W - W) + (L - leader L)) / 2); or W >= 87. 2020: W% >= .537 and <= 1.85 games. Window opens with the first of two straight contending seasons, survives one non-contending season, closes after two straight non-contending seasons and ends at the last contending season before them; length = full span. Left-censored unless two straight non-contending seasons occur in 2014 to the season before the window's first contending season. Right-censored: last contending season 2024 or 2025.
- Notes: Jordan life table built as the grace variant's: one row per contending season in a window, duration = seasons since the window opened (gap seasons count toward it but are not rows), closing recorded in the last contending season, rows through 2023 (the last season whose outcome, two seasons on, is observed). windows_with_rows excludes windows opening after 2023. Strict and grace life tables are hazard.py's life_table on their person-period rows. survival_after j = product of (1 - hazard) over durations <= j; null where the table ends before j. Strict and grace windows are measured in Opening Day seasons, Jordan windows in end-of-season records. Jordan windows cannot be shorter than 2 seasons.
- Club-seasons: 360; contending by Jordan's rule: 147
- Jordan contending × fixed top 6 on Opening Day: both 92; Jordan only 55; top 6 only 52; neither 161; agreement 0.70

| Definition | Windows | Closings | Left-censored dropped | Completed: mean / median length | Open after 1 / 2 / 3 / 4 / 5 / 6 |
|---|---|---|---|---|---|
| Jordan (2018), ex post | 16 | 7 | 13 | 3.29 / 3 | 1.00 / 0.75 / 0.56 / 0.56 / 0.38 / 0.25 |
| Strict ex ante, top 6 (F) | 38 | 30 | 12 | 2.67 / 2.0 | 0.66 / 0.50 / 0.32 / 0.21 / 0.21 / 0.14 |
| Grace ex ante, top 6 (F) | 20 | 12 | 17 | 2.25 / 2.0 | 0.75 / 0.58 / 0.42 / 0.36 / 0.29 / 0.29 |

Jordan life table:

| Age (seasons) | At risk | Closed | Censored | Hazard | Still open |
|---|---|---|---|---|---|
| 1 | 14 | 0 | 2 | 0.00 | 1.00 |
| 2 | 12 | 3 | 1 | 0.25 | 0.75 |
| 3 | 8 | 2 | 1 | 0.25 | 0.56 |
| 4 | 5 | 0 | 1 | 0.00 | 0.56 |
| 5 | 3 | 1 | 0 | 0.33 | 0.38 |
| 6 | 3 | 1 | 2 | 0.33 | 0.25 |

Grace life table (fixed top 6, closes after two straight seasons out):

| Age (seasons) | At risk | Closed | Censored | Hazard | Still open |
|---|---|---|---|---|---|
| 1 | 20 | 5 | 2 | 0.25 | 0.75 |
| 2 | 9 | 2 | 0 | 0.22 | 0.58 |
| 3 | 11 | 3 | 1 | 0.27 | 0.42 |
| 4 | 7 | 1 | 0 | 0.14 | 0.36 |
| 5 | 5 | 1 | 1 | 0.20 | 0.29 |
| 6 | 4 | 0 | 0 | 0.00 | 0.29 |
| 7 | 4 | 0 | 1 | 0.00 | 0.29 |
| 8 | 3 | 0 | 1 | 0.00 | 0.29 |
| 9 | 2 | 0 | 2 | 0.00 | 0.29 |
