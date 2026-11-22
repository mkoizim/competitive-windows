"""Assert every number in numbers-manifest.md against results/results.json. Stdlib only.
Run from the repo root: python3 posts/post1-hazard/check_numbers.py"""
import json, sys
d = json.load(open("results/results.json"))
hr = d["hazard_robustness"]["variants"]; W = d["writeup_numbers"]["t_intervals"]; A = d["age_checks"]["lines"]
r2 = lambda x: round(x + 1e-12, 2)
def ci(x, hi1=False):
    lo, hi = x["or_ci95_t"]
    return (r2(lo), round(hi, 1) if hi1 else r2(hi))
def m(line, term): return W["hazard_robustness.variants." + line]["M2"][term]
FIX = [3, 4, 5, 6, 7, 8, 9]; ROB = [k for k in FIX if k != 6]
sig = lambda line, term: m(line, term)["p_t"] < 0.05
c = {}
c["N1"] = d["seasons"] == [2014, 2026]
c["N2"] = sorted(v["threshold"] for v in hr.values() if isinstance(v["threshold"], int) and not v["grace"]) == FIX
c["N3"] = (hr["berth"]["F"]["windows"], hr["berth"]["F"]["closings"]) == (36, 28)
c["N4"] = (round(hr["berth"]["survival_after"]["2"] * 100), round(hr["berth"]["survival_after"]["4"] * 100)) == (56, 19)
x = m("berth", "strength"); c["N5"] = (r2(x["odds_ratio"]), ci(x), round(x["p_t"], 4)) == (0.67, (0.53, 0.84), 0.0017)
x = d["abstract_derived"]["age_per_doubling_berth"]; c["N6"] = (r2(x["odds_ratio"]), ci(x), round(x["p_t"], 3)) == (2.60, (1.21, 5.58), 0.016)
x = d["realized_outcome_refit"]["fits"]["berth_post"]["terms"]["strength"]; c["N13"] = (r2(x["odds_ratio"]), ci(x), round(x["p_t"], 4)) == (0.83, (0.73, 0.94), 0.0047)
p = A["berth"]["M2_without_strength"]["terms"]["ln_dur"]["p_t"]; c["N7"] = r2(p) == 0.65
x = m("top6", "strength");  c["N8"] = (r2(x["odds_ratio"]), ci(x), round(x["p_t"], 4)) == (0.72, (0.59, 0.89), 0.0033)
c["N9"] = [k for k in ROB if sig(f"top{k}", "strength")] == [3, 5, 7, 8, 9]
c["N10"] = [k for k in FIX if sig(f"top{k}", "ln_dur")] == [5, 8]
ALL = [k for k in hr]
c["N11"] = not any(m(l, "od_log2_rel")["p_t"] < 0.05 for l in ALL)
c["N12"] = not any(m(l, "era12")["p_t"] < 0.05 for l in ALL)
for k, ok in c.items(): print(k, "ok" if ok else "FAIL")
sys.exit(0 if all(c.values()) else 1)
