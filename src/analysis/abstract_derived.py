"""Derived numbers quoted in the Post 1 abstract. Stdlib only.
Adds the top-level key `abstract_derived` to results/results.json; every other key is left unchanged
(checked before writing).
Run from the repo root: python3 src/analysis/abstract_derived.py"""
import json, math
from pathlib import Path
P = Path("results/results.json")
d = json.loads(P.read_text())
before = {k: json.dumps(v, sort_keys=True) for k, v in d.items() if k != "abstract_derived"}
src = "writeup_numbers.t_intervals.hazard_robustness.variants.berth.M2.ln_dur"
x = d["writeup_numbers"]["t_intervals"]["hazard_robustness.variants.berth"]["M2"]["ln_dur"]
k = math.log(2)
d["abstract_derived"] = {
    "age_per_doubling_berth": {
        "source": src,
        "note": "ln_dur is the natural log of window age (1 in a window's first season), capped at 4. "
                "The odds ratio per doubling of age is OR**ln(2); the same transform applies to the "
                "t-based interval. p-value unchanged.",
        "odds_ratio": x["odds_ratio"] ** k,
        "or_ci95_t": [v ** k for v in x["or_ci95_t"]],
        "p_t": x["p_t"],
    }
}
after = {kk: json.dumps(v, sort_keys=True) for kk, v in d.items() if kk != "abstract_derived"}
assert before == after, "another key changed"
P.write_text(json.dumps(d, indent=2) + "\n")
print(json.dumps(d["abstract_derived"], indent=1))
