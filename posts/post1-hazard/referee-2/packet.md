# Referee packet: SABR abstract draft, Post 1 (competitive windows)

## A. The abstract (verbatim, 487 words with title; SABR limit 500 including the title)

Anticipating Competitive Window Length: A Hazard Model Analysis of FanGraphs Opening Day Playoff Odds

Front office strategy is heavily influenced by expectations of “competitive windows,” during which the Major League team will be positioned to contend for a postseason berth. Prior research on competitive window length is based on observed results (Jordan, Baseball Research Journal, 2018; Reinhart, The Hardball Times, 2018). However, no known research exists into MLB window length based on predicted outcomes. Because organizations make player personnel decisions based on predictions, assessing the probability of a window being or remaining open is of critical strategic importance.

The methodology is an exploratory hazard model analysis of window length using 2014–2026 Opening Day FanGraphs Playoff Odds, a public proxy for organizations’ internal projections. The primary model is berth-relative: it deems a team to be in a window if its Opening Day FanGraphs Playoff Odds project it to secure one of its league’s berths, adapting for multiple postseason formats. An alternative model defining a window as being open when a team is projected in the top 6 out of the 15 in its league by playoff odds is also explored and reported, as are variations setting the fixed-rank threshold from top 3 to top 9 as robustness checks. Windows are defined to be closed once the team is projected below the threshold on the next Opening Day. Windows open in 2014 are excluded, as their true age is not available in the data. All models are discrete-time logistic hazard regressions of team-seasons on current window age, Opening Day payroll, postseason format, and “cushion” (wins per 162 above the first team below the window threshold, as projected on Opening Day).

Results from the berth-relative definition indicate 56% of windows remained open after two seasons; 19% remained open after four. The hazard model showed each projected win in a team’s cushion lowered the odds of its window closing (odds ratio per projected win 0.67; 95% CI 0.53–0.84; p=0.0017). Among windows with the same Opening Day cushion, older windows were more likely to close (odds ratio 3.97 per log-season; 95% CI 1.32–11.9; p=0.016). Older windows did not close more often overall because surviving windows tended to carry more cushion.

At the fixed line (top 6 teams), cushion lowered the odds of its window closing similarly (odds ratio 0.72; 95% CI 0.59–0.89; p=0.0033), but window age was not statistically significant (odds ratio 1.72; 95% CI 0.60–4.98; p=0.30).

Opening Day payroll was not statistically significant once cushion was held fixed, nor was postseason format significant on the fixed line.

This research contributes the first known hazard model of competitive windows, providing a method for evaluating organizational strategy using the lens through which front offices must approach decisions: predicted outcomes. It will also provide a foundation for future analyses into organizational decisions to build for future seasons versus capitalizing on an open window, and how such decisions may impact the length of a window.

## B. Context the abstract does not state

- **Definitions.** A window is a run of consecutive seasons in which a club ranks inside a line in its league (15 clubs) by FanGraphs' Opening Day projected playoff odds (`fg` mode). Berth-relative line = top N, N = playoff berths per league (5 in 2014–2019 and 2021, 8 in 2020, 6 from 2022). Fixed line = top 6 in every season. A window closes when the club starts the next season below the line. Cushion = Opening Day projected wins per 162 above the first club below the line.
- **Sample.** Windows already open on 2014 Opening Day are dropped (age unknown). Model rows run 2015–2025 (closing judged at the next Opening Day, through 2026).
- **Model.** Discrete-time logit; terms: ln(window age, capped at 4), 12-team-format era (n+1 ≥ 2022), cushion, Opening Day payroll (log2 relative to the MLB mean). Standard errors clustered by club; p-values and 95% intervals against t with (clubs − 1) degrees of freedom.
- **Registration and status.** The fixed top-6 line was pre-registered (commit 33dbb7d, 2026-09-20, before the odds data were cleaned or analyzed). The berth-relative line was pre-specified as a robustness variant (2026-09-21) and given equal prominence on 2026-11-01, before its results were seen. Presenting it as the primary model in this abstract was decided after both lines' results were seen; the author's reason is that it is the more intuitive definition (“projected to make the playoffs”). All Post 1 analyses are exploratory: specifications were set before data collection, but several choices were made with results in view, and the decision log records them. The age finding was examined in depth after the main results were seen, with a decision rule fixed before the robustness checks were run.
- **On the berth-relative line, the era term is not a test of the 2022 format change**, because the line itself changes size in 2022; the format statement in the abstract comes from the fixed line.
- **Results deliberately left out of the abstract** (author's choice, for focus): the realized-outcome refit, the comparison with Jordan's (2018) results-based windows, sample sizes, and the age robustness checks. They are in section C.
- **Previous work.** The author's search found no hazard model or ex ante (projection-based) study of MLB window length.

## C. Results (generated from results.json; t-based intervals)

### C1. Samples and survival

| | Berth-relative | Fixed top 6 |
|---|---|---|
| Windows | 36 | 38 |
| Club-season rows | 97 | 102 |
| Closings | 28 | 30 |
| Clubs | 23 | 22 |
| Windows open in 2014, dropped | 10 | 12 |
| Still open after 1 season(s) | 0.72 | 0.66 |
| Still open after 2 season(s) | 0.56 | 0.50 |
| Still open after 3 season(s) | 0.30 | 0.32 |
| Still open after 4 season(s) | 0.19 | 0.21 |
| In-window club-seasons inside windows of 4+ seasons (all spells) | 77 of 146 | 90 of 156 |

### C2. Main model (M2), both lines

| Term | Berth-relative OR (95% CI), p | Fixed top 6 OR (95% CI), p |
|---|---|---|
| Cushion (per projected win) | 0.67 (0.53–0.84), 0.0017 | 0.72 (0.59–0.89), 0.0033 |
| ln(window age) | 3.97 (1.32–11.95), 0.0164 | 1.72 (0.60–4.98), 0.2995 |
| 12-team era | 0.60 (0.29–1.24), 0.1581 | 1.21 (0.48–3.04), 0.6684 |
| Payroll (log2 relative) | 0.71 (0.22–2.27), 0.5492 | 0.95 (0.42–2.15), 0.8900 |

### C3. Across all nine definitions (M2)

| Definition | Cushion OR (95% CI), p | ln(age) OR (95% CI), p |
|---|---|---|
| Baseline: top 6, strict | 0.72 (0.59–0.89), 0.0033 | 1.72 (0.60–4.98), 0.2995 |
| Berth-relative, strict | 0.67 (0.53–0.84), 0.0017 | 3.97 (1.32–11.95), 0.0164 |
| Top 3, strict | 0.59 (0.35–0.99), 0.0450 | 0.47 (0.10–2.12), 0.3008 |
| Top 4, strict | 0.84 (0.66–1.06), 0.1294 | 0.49 (0.12–2.02), 0.3014 |
| Top 5, strict | 0.61 (0.50–0.76), 8.7e-05 | 7.38 (2.04–26.66), 0.0042 |
| Top 7, strict | 0.71 (0.58–0.86), 0.0014 | 2.91 (0.98–8.71), 0.0549 |
| Top 8, strict | 0.73 (0.58–0.94), 0.0159 | 4.13 (1.46–11.67), 0.0094 |
| Top 9, strict | 0.73 (0.60–0.89), 0.0036 | 1.66 (0.67–4.14), 0.2631 |
| Top 6, grace | 0.77 (0.61–0.99), 0.0387 | 0.83 (0.21–3.25), 0.7748 |

### C4. Closing rate by Opening Day cushion (next Opening Day)

| Cushion (wins) | Berth-relative: closed | Fixed top 6: closed |
|---|---|---|
| <= 2 | 15 of 30 | 19 of 39 |
| > 2 to 5 | 9 of 29 | 7 of 25 |
| > 5 to 8 | 3 of 16 | 3 of 15 |
| > 8 | 1 of 22 | 1 of 23 |

### C5. Age robustness checks (ln age)

| Check | Berth-relative | Fixed top 6 |
|---|---|---|
| Firth | OR 3.56, penalized LR p 0.0046 | OR 1.65, penalized LR p 0.0835 |
| Two-way clustering | 3.97 (1.36–11.60), p 0.0141 | 1.72 (0.59–5.07), p 0.3069 |
| Wild score bootstrap | p 0.0170 | p 0.2523 |
| Without cushion in the model | 1.26 (0.44–3.64), p 0.6496 | 0.81 (0.30–2.17), p 0.6548 |
| Dropping rows n = 2019–2021 | 5.67 (1.15–28.02), p 0.0347 | 2.22 (0.66–7.44), p 0.1840 |
| Leave one club out: OR range | 3.40–4.95 | 1.45–2.32 |
| Decision rule for an age claim (all six conditions, berth-relative) | True | — |

### C6. Cushion against the next season's actual results (not in the abstract)

Same rows and covariates; event = berth-relative: missed the postseason in n+1; fixed: not contending in n+1 by Jordan's (2018) rule.

| | Berth-relative (missed postseason) | Fixed top 6 (not contending) |
|---|---|---|
| Cushion OR (95% CI), p | 0.83 (0.73–0.94), 0.0047 | 0.84 (0.75–0.94), 0.0043 |
| Cushion <= 2: failed | 20 of 30 | 22 of 39 |
| Cushion > 2 to 5: failed | 17 of 29 | 15 of 25 |
| Cushion > 5 to 8: failed | 6 of 16 | 5 of 15 |
| Cushion > 8: failed | 4 of 22 | 4 of 23 |

### C7. Projected vs. results-based contention, 2014–2025 (not in the abstract)

- Contention rates of 360 club-seasons: berth-relative 134, fixed top 6 144, Jordan's rule 147.
- Fixed top 6 vs. Jordan: both 92; projected but not contending 52; contending but not projected 55; neither 161.
