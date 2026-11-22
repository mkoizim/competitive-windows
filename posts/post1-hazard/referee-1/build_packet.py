"""Build the referee packet for the Post 1 analysis from the repo files. Stdlib only.
Run from the repo root: python3 posts/post1-hazard/referee-1/build_packet.py
Plan and decisions text is copied verbatim; every number in Part C is read from results.json."""
import json, re
from pathlib import Path

OUT = Path("posts/post1-hazard/referee-1/packet.md")
plan = Path("docs/competitive-windows-research-plan.md").read_text()
dec = Path("docs/decisions.md").read_text()
d = json.load(open("results/results.json"))

def between(text, start, end):
    i = text.index(start); j = text.index(end, i + len(start))
    return text[i:j].rstrip()

# ---------- Part A: design (plan, verbatim) ----------
A = [
    "## A. Design (verbatim from the research plan)",
    between(plan, "**What has been seen.**", "### Registered"),
    between(plan, "#### Three snapshots per season", "#### Which transactions belong"),
    between(plan, "### 3.3 Windows", "### 3.3b Window patterns"),
    between(plan, "**Post 1 — The hazard of contention.**", "**Post 2 — Putting the roof on.**"),
]

# ---------- Part B: decisions (verbatim) ----------
entries = re.split(r"(?m)^(?=## \d{4}-\d{2}-\d{2} — )", dec)
entries = [e for e in entries if re.match(r"## \d{4}", e)]
keep = [
    ("2026-09-20", "Window threshold"), ("2026-09-20", "Strict consecutive windows"),
    ("2026-09-20", "Persistent contenders"),
    ("2026-09-21", "Ranking variable"), ("2026-09-21", "Study period extended"),
    ("2026-09-21", "Berth-count shift"), ("2026-09-21", "Format change handled"),
    ("2026-09-22", "No FanGraphs methodology break"), ("2026-09-22", "Projection mode fixed"),
    ("2026-09-27", "2020 postseason odds reconstructed"),
    ("2026-09-28", "Data-examination wording corrected"),
    ("2026-10-17", "Odds collected"),
    ("2026-10-18", "2020 reconstruction confirmed"), ("2026-10-18", "Windows stay defined on Opening Day"),
    ("2026-10-18", "Corrections from the odds audit"),
    ("2026-10-20", "Spell count"),
    ("2026-10-26", "Left-censored spells"), ("2026-10-26", "Baseball-Reference Opening Day odds"),
    ("2026-10-26", "Hazard model specification"), ("2026-10-26", "Backcast validation failed"),
    ("2026-10-26", "Payroll covariate"), ("2026-10-26", "Payroll data"),
    ("2026-10-26", "Deadline status"), ("2026-10-26", "Hazard run"),
    ("2026-11-01", "Plan v0.29"), ("2026-11-01", "Week 3 robustness specification"),
    ("2026-11-01", "Berth-relative threshold reported"),
    ("2026-11-02", ""), ("2026-11-03", ""),
]
picked = []
for e in entries:
    head = e.splitlines()[0]
    for date, pre in keep:
        if head.startswith(f"## {date} — {pre}"):
            picked.append(e.rstrip()); break
missing = [k for k in keep if k[1] and not any(p.startswith(f"## {k[0]} — {k[1]}") for p in picked)]
assert not missing, missing
B = ["## B. Decision log, Post 1 entries (verbatim, in date order)",
     "Entries about later posts (trades, valuations, P1–P4) are omitted. 'Chose (write-up)' lines are the claims the abstract intends to make."] \
    + [p.replace("\n## ", "\n### ").replace("## 20", "### 20", 1) for p in picked]

# ---------- Part C: results (generated from results.json) ----------
f2 = lambda x: "—" if x is None else f"{x:.2f}"
f3 = lambda x: f"{x:.3f}"
fp = lambda p: f"{p:.4f}" if p >= 0.0001 else f"{p:.1e}"
def lt_table(rows, maxd=None):
    out = ["| Age (seasons) | At risk | Closed | Censored | Hazard | Still open |", "|---|---|---|---|---|---|"]
    for r in rows:
        if maxd and r["duration"] > maxd: break
        out.append(f"| {r['duration']} | {r['at_risk']} | {r['exits']} | {r['censored']} | {f2(r['hazard'])} | {f2(r['survival'])} |")
    return "\n".join(out)
def terms_table(terms, ptkey):
    out = ["| Term | Odds ratio | 95% interval | p (normal) | p (t, G−1) |", "|---|---|---|---|---|"]
    for k, t in terms.items():
        if k == "const": continue
        out.append(f"| {k} | {f3(t['odds_ratio'])} | {f3(t['or_ci95'][0])}–{f3(t['or_ci95'][1])} | {fp(t.get('p', t.get('p_normal')))} | {fp(ptkey[k]['p_t'])} |")
    return "\n".join(out)

h = d["hazard"]; hr = d["hazard_robustness"]; hi = d["hazard_inference"]; j = d["jordan_comparison"]
C = ["## C. Results (generated from results.json; numbers rounded for display)"]
C.append("### C1. Definitions used in the files\n" + "\n".join(f"- **{k}**: {v}" for k, v in
         [("hazard", h["definition"]), ("samples F / L / H", " | ".join(f"{s}: {h['samples'][s]}" for s in 'FLH')),
          ("models", h["model_notes"]), ("robustness", hr["definition"]), ("small-cluster inference", hi["definition"])]))
v6 = d["variants"]["top6"]
C.append("### C2. Windows at the baseline (fixed top 6, strict), 2014–2026\n"
         f"- Window spells: {v6['n_spells']}; club-seasons in a window: {v6['in_window_club_seasons']}; "
         f"open in 2014 (left-censored): {v6['left_censored']['count']}; still open in 2026: {v6['right_censored']['count']}; "
         f"in a window every season (persistent): {h['persistent_contenders']['count']}\n"
         "- Spell length distribution (length: count): " + ", ".join(f"{k}: {n}" for k, n in v6["length_distribution"].items()) + "\n"
         "- Model rows (club-seasons at risk), closings, windows, clubs: " +
         "; ".join(f"{s} {h['rows_events'][s]['rows']} rows, {h['rows_events'][s]['events']} closings, {h['rows_events'][s]['spells']} windows, {h['rows_events'][s]['clubs']} clubs" for s in "FLH"))
C.append("### C3. Life table, baseline, sample F\n" + lt_table(h["life_tables"]["F"]))
m1 = h["models"]["F"]["M1"]["bins"]
C.append("### C4. M1 (age bins only), sample F\n| Bin | Rows | Closings | Hazard | 95% interval (clustered) |\n|---|---|---|---|---|\n" +
         "\n".join(f"| {b} | {x['rows']} | {x['events']} | {f2(x['hazard'])} | {f2(x['ci95_cluster'][0])}–{f2(x['ci95_cluster'][1])} |" for b, x in m1.items()) +
         f"\n\nBins vs. ln(age) likelihood-ratio test (F): LR = {h['models']['F']['lr_bins_vs_log']['lr_stat']:.2f}, df = 2, p = {fp(h['models']['F']['lr_bins_vs_log']['p'])}")
for s in "FLH":
    for m in ("M2", "M2b"):
        C.append(f"### C5. {m}, sample {s} (clubs = {hi['t_correction'][s][m]['n_clusters']})\n" +
                 terms_table(h["models"][s][m]["terms"], hi["t_correction"][s][m]["terms"]))
sb = hi["score_bootstrap"]; sc = hi["size_check"]
C.append("### C6. Wild score bootstrap, strength in M2, sample F\n"
         f"- T = {sb['T']:.3f}; bootstrap p = {fp(sb['p_bootstrap'])} ({sb['n_extreme']} of {sb['draws']} draws); normal p = {fp(sb['p_normal'])}; clusters = {sb['n_clusters']}\n"
         f"- Size check ({sc['n_datasets']} null datasets, {sc['draws_per_dataset']} draws each): rejection {sc['rejection_rate_all']['5']:.3f} at 5%, {sc['rejection_rate_all']['10']:.3f} at 10%; pass band {sc['band_5pct']}")
rows = ["| Definition | Windows | Rows | Closings | Clubs | Cushion OR (95%) | p_t | ln(age) OR (95%) | p_t | Era OR | p_t | Payroll p_t | Open after 1 / 2 / 3 / 4 | Bins-vs-log p |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for k in hr["order"]:
    v = hr["variants"][k]; t = v["M2"]["terms"]; F = v["F"]; sa = v["survival_after"]
    rows.append(f"| {v['label']} | {F['windows']} | {F['rows']} | {F['closings']} | {F['clubs']} | "
                f"{f3(t['strength']['odds_ratio'])} ({f3(t['strength']['or_ci95'][0])}–{f3(t['strength']['or_ci95'][1])}) | {fp(t['strength']['p_t'])} | "
                f"{f2(t['ln_dur']['odds_ratio'])} ({f2(t['ln_dur']['or_ci95'][0])}–{f2(t['ln_dur']['or_ci95'][1])}) | {fp(t['ln_dur']['p_t'])} | "
                f"{f2(t['era12']['odds_ratio'])} ({f2(t['era12']['or_ci95'][0])}–{f2(t['era12']['or_ci95'][1])}) | {fp(t['era12']['p_t'])} | {fp(t['od_log2_rel']['p_t'])} | "
                f"{' / '.join(f2(sa.get(str(i))) for i in range(1,5))} | {fp(v['lr_bins_vs_log']['p'])} |")
flags = [f"- {hr['variants'][k]['label']}: {', '.join(hr['variants'][k]['flags'])}" for k in hr["order"] if hr["variants"][k]["flags"]]
C.append("### C7. M2 under all nine definitions, sample F\n" + "\n".join(rows) + ("\n\nFlags:\n" + "\n".join(flags) if flags else "")
         + "\n\nThreshold by season for the berth-relative line: " + ", ".join(f"{y}: {n}" for y, n in hr["variants"]["berth"]["threshold"].items()))
C.append("### C8. Life table, berth-relative line, sample F\n" + lt_table(hr["variants"]["berth"]["life_table"]))
def cush(b): return "\n".join(f"| {x['label']} | {x['club_seasons']} | {x['closings']} | {f2(x['share'])} |" for x in b.values())
C.append("### C9. Closing rate by Opening Day cushion (projected wins per 162 above the first club below the line), sample F\n"
         "Fixed top 6:\n\n| Cushion | Club-seasons | Closed by next Opening Day | Share |\n|---|---|---|---|\n" + cush(h["closing_by_strength_band"]["bands"]) +
         "\n\nBerth-relative:\n\n| Cushion | Club-seasons | Closed by next Opening Day | Share |\n|---|---|---|---|\n" + cush(d["cushion_berth"]["bands"]))
es = h["entry_strength"]
C.append(f"### C10. Life tables by cushion in a window's first season (split at the median, {es['median_first_season_strength']:.2f} wins), sample F\n" +
         "\n\n".join(f"{g.replace('_',' ')} ({es['n_spells'][g]} windows):\n\n" + lt_table(es["life_tables"][g]) for g in es["life_tables"]))
dl = []
for s in "FLH":
    c = h["deadline"][s]["cells"]
    dl.append(f"| {s} | {c['above_exit']} of {c['above_exit']+c['above_no_exit']} | {c['below_exit']} of {c['below_exit']+c['below_no_exit']} |")
C.append("### C11. Deadline status in season n vs. closing at n+1's Opening Day (description only; not in the model)\n"
         "| Sample | Above the line at the deadline: closed | Below the line at the deadline: closed |\n|---|---|---|\n" + "\n".join(dl))
tb = j["two_by_two"]["cells"]
jl = ["| Definition | Windows | Closings | Left-censored dropped | Completed: mean / median length | Open after 1 / 2 / 3 / 4 / 5 / 6 |", "|---|---|---|---|---|---|"]
for k in ("jordan", "strict", "grace"):
    x = j["definitions"][k]; cl = x["completed_length"]; sa = x["survival_after"]
    jl.append(f"| {x['label']} | {x['windows']} | {x['closings']} | {x['left_censored_dropped']} | {f2(cl['mean'])} / {cl['median']} | {' / '.join(f2(sa.get(str(i))) for i in range(1,7))} |")
C.append("### C12. Comparison with Jordan (2018), ex post, 2014–2025\n"
         f"- Definition: {j['definition']}\n- Notes: {j['life_table_note']} {j['min_length_note']}\n"
         f"- Club-seasons: {j['club_seasons']['total']}; contending by Jordan's rule: {j['club_seasons']['contending']}\n"
         f"- Jordan contending × fixed top 6 on Opening Day: both {tb['contending__window']}; Jordan only {tb['contending__no_window']}; "
         f"top 6 only {tb['not_contending__window']}; neither {tb['not_contending__no_window']}; agreement {j['two_by_two']['agreement']:.2f}\n\n" + "\n".join(jl)
         + "\n\nJordan life table:\n\n" + lt_table(j["definitions"]["jordan"]["life_table"])
         + "\n\nGrace life table (fixed top 6, closes after two straight seasons out):\n\n" + lt_table(j["definitions"]["grace"]["life_table"]))

text = "# Referee packet: Post 1, the hazard of MLB contention windows\n\n" + \
       "\n\n".join(A) + "\n\n" + "\n\n".join(B) + "\n\n" + "\n\n".join(C) + "\n"
OUT.write_text(text)
print(OUT, len(text.split()), "words;", len(picked), "decision entries")
