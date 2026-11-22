"""Build the referee packet for the Post 1 abstract draft. Stdlib only.
Run from the repo root: python3 posts/post1-hazard/referee-2/build_packet.py
The abstract is copied verbatim; every number in the results section is read from results.json."""
import json
from pathlib import Path
OUT = Path("posts/post1-hazard/referee-2/packet.md")
abstract = Path("posts/post1-hazard/abstract.md").read_text().strip()
d = json.load(open("results/results.json"))
hr = d["hazard_robustness"]["variants"]; W = d["writeup_numbers"]["t_intervals"]
f2 = lambda x: "—" if x is None else f"{x:.2f}"
fp = lambda p: f"{p:.4f}" if p >= 0.0001 else f"{p:.1e}"
def orci(x): return f"{f2(x['odds_ratio'])} ({f2(x['or_ci95_t'][0])}–{f2(x['or_ci95_t'][1])})"

S = ["# Referee packet: SABR abstract draft, Post 1 (competitive windows)", "",
     "## A. The abstract (verbatim, 487 words with title; SABR limit 500 including the title)", "", abstract, ""]

S += ["## B. Context the abstract does not state", "",
"- **Definitions.** A window is a run of consecutive seasons in which a club ranks inside a line in its league (15 clubs) by FanGraphs' Opening Day projected playoff odds (`fg` mode). Berth-relative line = top N, N = playoff berths per league (5 in 2014–2019 and 2021, 8 in 2020, 6 from 2022). Fixed line = top 6 in every season. A window closes when the club starts the next season below the line. Cushion = Opening Day projected wins per 162 above the first club below the line.",
"- **Sample.** Windows already open on 2014 Opening Day are dropped (age unknown). Model rows run 2015–2025 (closing judged at the next Opening Day, through 2026).",
"- **Model.** Discrete-time logit; terms: ln(window age, capped at 4), 12-team-format era (n+1 ≥ 2022), cushion, Opening Day payroll (log2 relative to the MLB mean). Standard errors clustered by club; p-values and 95% intervals against t with (clubs − 1) degrees of freedom.",
"- **Registration and status.** The fixed top-6 line was pre-registered (commit 33dbb7d, 2026-09-20, before the odds data were cleaned or analyzed). The berth-relative line was pre-specified as a robustness variant (2026-09-21) and given equal prominence on 2026-11-01, before its results were seen. Presenting it as the primary model in this abstract was decided after both lines' results were seen; the author's reason is that it is the more intuitive definition (“projected to make the playoffs”). All Post 1 analyses are exploratory: specifications were set before data collection, but several choices were made with results in view, and the decision log records them. The age finding was examined in depth after the main results were seen, with a decision rule fixed before the robustness checks were run.",
"- **On the berth-relative line, the era term is not a test of the 2022 format change**, because the line itself changes size in 2022; the format statement in the abstract comes from the fixed line.",
"- **Results deliberately left out of the abstract** (author's choice, for focus): the realized-outcome refit, the comparison with Jordan's (2018) results-based windows, sample sizes, and the age robustness checks. They are in section C.",
"- **Previous work.** The author's search found no hazard model or ex ante (projection-based) study of MLB window length.", ""]

C = ["## C. Results (generated from results.json; t-based intervals)", ""]
C += ["### C1. Samples and survival", "", "| | Berth-relative | Fixed top 6 |", "|---|---|---|"]
for lab, k in [("Windows", "windows"), ("Club-season rows", "rows"), ("Closings", "closings"), ("Clubs", "clubs")]:
    C.append(f"| {lab} | {hr['berth']['F'][k]} | {hr['top6']['F'][k]} |")
C.append(f"| Windows open in 2014, dropped | {hr['berth']['left_censored_dropped']['count']} | {hr['top6']['left_censored_dropped']['count']} |")
for j in "1234":
    C.append(f"| Still open after {j} season(s) | {f2(hr['berth']['survival_after'][j])} | {f2(hr['top6']['survival_after'][j])} |")
lw = d["writeup_numbers"]["long_windows"]
C.append(f"| In-window club-seasons inside windows of 4+ seasons (all spells) | {lw['berth_relative']['club_seasons_ge_4']} of {lw['berth_relative']['in_window_club_seasons']} | {lw['fixed_top6']['club_seasons_ge_4']} of {lw['fixed_top6']['in_window_club_seasons']} |")
C += ["", "### C2. Main model (M2), both lines", "", "| Term | Berth-relative OR (95% CI), p | Fixed top 6 OR (95% CI), p |", "|---|---|---|"]
for term, lab in [("strength", "Cushion (per projected win)"), ("ln_dur", "ln(window age)"), ("era12", "12-team era"), ("od_log2_rel", "Payroll (log2 relative)")]:
    b = W["hazard_robustness.variants.berth"]["M2"][term]; f = W["hazard_robustness.variants.top6"]["M2"][term]
    C.append(f"| {lab} | {orci(b)}, {fp(b['p_t'])} | {orci(f)}, {fp(f['p_t'])} |")
C += ["", "### C3. Across all nine definitions (M2)", "", "| Definition | Cushion OR (95% CI), p | ln(age) OR (95% CI), p |", "|---|---|---|"]
for k in d["hazard_robustness"]["order"]:
    s = W["hazard_robustness.variants." + k]["M2"]["strength"]; a = W["hazard_robustness.variants." + k]["M2"]["ln_dur"]
    C.append(f"| {hr[k]['label']} | {orci(s)}, {fp(s['p_t'])} | {orci(a)}, {fp(a['p_t'])} |")
C += ["", "### C4. Closing rate by Opening Day cushion (next Opening Day)", "", "| Cushion (wins) | Berth-relative: closed | Fixed top 6: closed |", "|---|---|---|"]
for band in ("le_2", "gt_2_le_5", "gt_5_le_8", "gt_8"):
    b = d["cushion_berth"]["bands"][band]; f = d["hazard"]["closing_by_strength_band"]["bands"][band]
    C.append(f"| {b['label']} | {b['closings']} of {b['club_seasons']} | {f['closings']} of {f['club_seasons']} |")
A = d["age_checks"]["lines"]
C += ["", "### C5. Age robustness checks (ln age)", "", "| Check | Berth-relative | Fixed top 6 |", "|---|---|---|"]
def g(line, *path):
    x = A[line]
    for p in path: x = x[p]
    return x
rows = []
for line in ("berth", "fixed"):
    fi = A[line]["firth"]; tw = A[line]["two_way_cluster"]; bs = A[line]["wild_score_bootstrap_ln_dur"]
    rows.append((line, fi, tw, bs))
def firth_s(fi): return f"OR {f2(fi['M2']['terms']['ln_dur']['odds_ratio'])}, penalized LR p {fp(fi['penalized_lr_ln_dur']['p'])}"
def tw_s(tw): x = tw['terms']['ln_dur']; return f"{orci(x)}, p {fp(x['p_t'])}"
def bs_s(bs): return f"p {fp(bs['p_bootstrap'])}"
try:
    C.append(f"| Firth | {firth_s(A['berth']['firth'])} | {firth_s(A['fixed']['firth'])} |")
except Exception: pass
try:
    C.append(f"| Two-way clustering | {tw_s(A['berth']['two_way_cluster'])} | {tw_s(A['fixed']['two_way_cluster'])} |")
except Exception: pass
try:
    C.append(f"| Wild score bootstrap | {bs_s(A['berth']['wild_score_bootstrap_ln_dur'])} | {bs_s(A['fixed']['wild_score_bootstrap_ln_dur'])} |")
except Exception: pass
for lab, key in [("Without cushion in the model", "M2_without_strength"), ("Dropping rows n = 2019–2021", "drop_line_change_rows")]:
    try:
        gb = A["berth"][key]; gf = A["fixed"][key]
        gb = gb.get("fit", gb); gf = gf.get("fit", gf)
        xb = gb["terms"]["ln_dur"]; xf = gf["terms"]["ln_dur"]
        C.append(f"| {lab} | {orci(xb)}, p {fp(xb['p_t'])} | {orci(xf)}, p {fp(xf['p_t'])} |")
    except Exception: pass
lo = [A[l]["leave_one_club_out"]["or_range"] for l in ("berth", "fixed")]
C.append(f"| Leave one club out: OR range | {f2(lo[0][0])}–{f2(lo[0][1])} | {f2(lo[1][0])}–{f2(lo[1][1])} |")
C.append(f"| Decision rule for an age claim (all six conditions, berth-relative) | {d['age_checks']['rule']['age_rule_passes']} | — |")
R = d["realized_outcome_refit"]
C += ["", "### C6. Cushion against the next season's actual results (not in the abstract)", "",
      "Same rows and covariates; event = berth-relative: missed the postseason in n+1; fixed: not contending in n+1 by Jordan's (2018) rule.", "",
      "| | Berth-relative (missed postseason) | Fixed top 6 (not contending) |", "|---|---|---|"]
sb = R["fits"]["berth_post"]["terms"]["strength"]; sf = R["fits"]["fixed_jordan"]["terms"]["strength"]
C.append(f"| Cushion OR (95% CI), p | {orci(sb)}, {fp(sb['p_t'])} | {orci(sf)}, {fp(sf['p_t'])} |")
for band in ("le_2", "gt_2_le_5", "gt_5_le_8", "gt_8"):
    b = R["bands"]["berth_post"][band]; f = R["bands"]["fixed_jordan"][band]
    C.append(f"| Cushion {b['label']}: failed | {b['events']} of {b['club_seasons']} | {f['events']} of {f['club_seasons']} |")
j = d["jordan_comparison"]; cr = d["writeup_numbers"]["contention_rates_2014_2025"]
C += ["", "### C7. Projected vs. results-based contention, 2014–2025 (not in the abstract)", "",
      f"- Contention rates of {cr['club_seasons']} club-seasons: berth-relative {cr['berth_relative']['n']}, fixed top 6 {cr['fixed_top6']['n']}, Jordan's rule {cr['jordan_contending']['n']}.",
      f"- Fixed top 6 vs. Jordan: both {j['two_by_two']['cells']['contending__window']}; projected but not contending {j['two_by_two']['cells']['not_contending__window']}; contending but not projected {j['two_by_two']['cells']['contending__no_window']}; neither {j['two_by_two']['cells']['not_contending__no_window']}."]
OUT.write_text("\n".join(S + C) + "\n")
print(OUT, len(OUT.read_text().split()), "words")
