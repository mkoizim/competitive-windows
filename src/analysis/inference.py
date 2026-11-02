"""Small-cluster inference for the Post 1 hazard (docs/decisions.md, "Week 3 robustness
specification", 2026-11-01, item E; size-check band from "Week 3 prompts", 2026-11-02).

1. t(G - 1) p-values for every term of M2 and M2b in F, L and H, from the clustered z-statistics
   already in results.json["hazard"] (G = clubs: 22 in F, 26 in L and H).
2. Wild score bootstrap (Kline & Santos, 2012) for strength in M2, sample F. Restricted fit: M2
   without strength. Effective score per row e_i = u_i (x_i,strength - H_bt H_tt^-1 x_i,theta),
   with u_i = y_i - p~_i and H = sum p~(1 - p~) x x' at the restricted estimates; club sums S_g;
   T = sum S_g / sqrt(sum S_g^2). Each draw: T* = sum w_g S_g / sqrt(sum w_g^2 S_g^2), one Webb
   weight per club, no refitting, H fixed. p = share of draws with |T*| >= |T|; also the normal
   p-value for T. No small-sample scaling of either.
3. Size check: 500 datasets with outcomes drawn as Bernoulli(p~) on the real rows; on each the
   restricted model is refitted and the test run with 999 draws. Dataset k is seeded by child k
   of SeedSequence(MASTER_SEED).spawn(500), which drives both its outcomes and its weights. The
   main bootstrap uses SeedSequence(MASTER_SEED) itself, a stream distinct from every child.

Reads data/processed/hazard_pp.csv (built by hazard.py). Only the "hazard_inference" key of
results.json is written; every other key is confirmed unchanged. Nothing is written if any check
fails.

Needs numpy, pandas, scipy and statsmodels (the repo's .venv). Run from the repo root:
.venv/bin/python src/analysis/inference.py
"""

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hazard as hz  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PP = ROOT / "data" / "processed" / "hazard_pp.csv"
OUT = ROOT / "results" / "results.json"
KEY = "hazard_inference"

MASTER_SEED = 20261102
DRAWS = 9_999
SIM_DATASETS, SIM_DRAWS = 500, 999
WEBB = np.array([-math.sqrt(1.5), -1.0, -math.sqrt(0.5), math.sqrt(0.5), 1.0, math.sqrt(1.5)])
M2_COLS = ["const", "ln_dur", "era12", "strength", "od_log2_rel"]
TEST = "strength"

# Checks fixed in the task brief
EXPECT_G = {"F": 22, "L": 26, "H": 26}
EXPECT_P_T_F = {"M2": {"strength": 0.0033, "ln_dur": 0.30, "era12": 0.67, "od_log2_rel": 0.89},
                "M2b": {"strength": 0.0034, "dur1": 0.25}}
EXPECT_F = (102, 30)
SIZE_BAND = (0.03, 0.07)
ROBUSTNESS_TOL = 1e-9      # relative, F p_t vs hazard_robustness top6
SCORE_TOL = 1e-8           # restricted score on theta at the restricted MLE


def sig2(x):
    return float(f"{x:.2g}")


# ---------------------------------------------------------------- 1. t(G - 1)

def t_pvalues(hazard):
    out = {}
    for s in hz.SAMPLES:
        out[s] = {}
        for m in ("M2", "M2b"):
            model = hazard["models"][s][m]
            g = model["n_clusters"]
            out[s][m] = {"n_clusters": g, "t_df": g - 1, "terms": {
                c: {"z": t["z"], "p_normal": t["p"],
                    "p_t": float(2 * stats.t.sf(abs(t["z"]), g - 1))}
                for c, t in model["terms"].items()}}
    return out


def check_t(tp, robustness):
    failures = []
    for s, g in EXPECT_G.items():
        for m in ("M2", "M2b"):
            if tp[s][m]["n_clusters"] != g:
                failures.append(f"(1) {s} {m}: G = {tp[s][m]['n_clusters']}, expected {g}")
    for m, terms in EXPECT_P_T_F.items():
        for c, expected in terms.items():
            p = tp["F"][m]["terms"][c]["p_t"]
            if sig2(p) != expected:
                failures.append(f"(2) F {m} {c}: p_t {p:.6g}, expected {expected}")
    max_rel = 0.0
    for m in ("M2", "M2b"):
        rob = robustness["variants"]["top6"][m]["terms"]
        if set(rob) != set(tp["F"][m]["terms"]):
            failures.append(f"(3) F {m}: terms differ from hazard_robustness top6")
            continue
        for c, t in tp["F"][m]["terms"].items():
            rel = abs(t["p_t"] - rob[c]["p_t"]) / rob[c]["p_t"]
            max_rel = max(max_rel, rel)
            if rel > ROBUSTNESS_TOL:
                failures.append(f"(3) F {m} {c}: p_t {t['p_t']:.10g}, hazard_robustness top6 "
                                f"{rob[c]['p_t']:.10g}")
    return failures, max_rel


# ---------------------------------------------------------------- 2. wild score bootstrap

def restricted_fit(d):
    return hz.fit_logit(d.assign(const=1.0), [c for c in M2_COLS if c != TEST], cluster=False)


def club_scores(d, p):
    """Effective scores for TEST at restricted fitted probabilities p, summed by team_id.
    Returns (clubs, S_g, projection H_tt^-1 H_tb, max |sum u x_theta|)."""
    X = d.assign(const=1.0)[M2_COLS].to_numpy(float)
    j = M2_COLS.index(TEST)
    th = [i for i in range(len(M2_COLS)) if i != j]
    u = d["event"].to_numpy(float) - p
    H = (X * (p * (1 - p))[:, None]).T @ X
    proj = np.linalg.solve(H[np.ix_(th, th)], H[th, j])   # H symmetric: H_bt H_tt^-1 = proj'
    e = u * (X[:, j] - X[:, th] @ proj)
    clubs, idx = np.unique(d["team_id"].to_numpy(), return_inverse=True)
    S = np.bincount(idx, weights=e)
    return clubs, S, proj, float(np.abs(X[:, th].T @ u).max())


def wild_score(S, draws, rng):
    T = S.sum() / math.sqrt((S ** 2).sum())
    W = rng.choice(WEBB, size=(draws, len(S)))
    T_star = (W @ S) / np.sqrt((W ** 2) @ (S ** 2))
    n_extreme = int((np.abs(T_star) >= abs(T)).sum())
    return {"T": float(T), "n_extreme": n_extreme, "p_bootstrap": n_extreme / draws,
            "p_normal": float(2 * stats.norm.sf(abs(T)))}


def converged(res):
    return res is not None and bool(res.mle_retvals.get("converged", False))


def score_bootstrap(f):
    failures = []
    if (len(f), int(f["event"].sum())) != EXPECT_F or f["team_id"].nunique() != EXPECT_G["F"]:
        failures.append(f"(4) F: {len(f)} rows / {int(f['event'].sum())} events / "
                        f"{f['team_id'].nunique()} clubs, expected {EXPECT_F} / {EXPECT_G['F']}")
    res, notes = restricted_fit(f)
    if not converged(res):
        failures.append(f"(4) restricted fit did not converge: {notes}")
        return None, failures
    p = np.asarray(res.predict())
    clubs, S, proj, score_theta = club_scores(f, p)
    if score_theta > SCORE_TOL:
        failures.append(f"(4) restricted score on theta not 0: max |sum u x| = {score_theta:.3g}")
    test = wild_score(S, DRAWS, np.random.default_rng(np.random.SeedSequence(MASTER_SEED)))
    team = f.drop_duplicates("team_id").set_index("team_id")["team"]
    theta = [c for c in M2_COLS if c != TEST]
    out = {
        "sample": "F", "model": "M2", "term": TEST,
        "n_rows": len(f), "n_events": int(f["event"].sum()), "n_clusters": len(clubs),
        "master_seed": MASTER_SEED, "draws": DRAWS,
        "weights": "Webb six-point: +/-sqrt(3/2), +/-1, +/-sqrt(1/2), each 1/6; one per club "
                   "per draw",
        "rng": "numpy default_rng(SeedSequence(master_seed)); weights drawn as one "
               "(draws x clubs) array, clubs in ascending team_id order",
        **test,
        "restricted": {"terms": theta,
                       "coef": {c: float(res.params[c]) for c in theta},
                       "loglik": float(res.llf), "converged": True, "notes": notes},
        "projection_H_tt_inv_H_tb": {c: float(v) for c, v in zip(theta, proj)},
        "restricted_score_max_abs": score_theta,
        "S_g": [{"team_id": int(c), "team": team[c], "S_g": float(s)} for c, s in zip(clubs, S)],
        "sum_S_g": float(S.sum()), "sum_S_g_sq": float((S ** 2).sum()),
    }
    return (out, p), failures


# ---------------------------------------------------------------- 3. size check

def size_check(f, p_tilde):
    children = np.random.SeedSequence(MASTER_SEED).spawn(SIM_DATASETS)
    fails, noted, rej = [], 0, {"5": 0, "10": 0}
    for k, child in enumerate(children):
        rng = np.random.default_rng(child)
        dk = f.assign(event=rng.binomial(1, p_tilde))
        res, notes = restricted_fit(dk)
        if not converged(res):
            fails.append({"dataset": k, "notes": notes})
            continue
        noted += bool(notes)
        _, S, _, _ = club_scores(dk, np.asarray(res.predict()))
        pb = wild_score(S, SIM_DRAWS, rng)["p_bootstrap"]
        rej["5"] += pb <= 0.05
        rej["10"] += pb <= 0.10
    ok = SIM_DATASETS - len(fails)
    out = {
        "n_datasets": SIM_DATASETS, "draws_per_dataset": SIM_DRAWS,
        "dgp": ("event ~ Bernoulli(p~), p~ = restricted-model fitted probabilities on the real F "
                "rows; same rows, clubs and covariates"),
        "seeding": ("dataset k uses default_rng(SeedSequence(master_seed).spawn(500)[k]) for its "
                    "outcomes, then its 999 weight draws"),
        "rejection": "p_bootstrap <= level",
        "n_fit_failures": len(fails), "fit_failures": fails,
        "n_successful_fits": ok, "n_successful_fits_with_notes": noted,
        "rejections": rej,
        "rejection_rate_successful": {lv: (n / ok if ok else None) for lv, n in rej.items()},
        "rejection_rate_all": {lv: n / SIM_DATASETS for lv, n in rej.items()},
        "band_5pct": list(SIZE_BAND),
    }
    failures = []
    for base in ("successful", "all"):
        r = out[f"rejection_rate_{base}"]["5"]
        if r is None or not SIZE_BAND[0] <= r <= SIZE_BAND[1]:
            failures.append(f"(5) 5% rejection rate over {base} fits = {r}, outside "
                            f"{SIZE_BAND[0]:.0%}-{SIZE_BAND[1]:.0%}")
    return out, failures


# ---------------------------------------------------------------- main

def fail(failures):
    print(f"{len(failures)} check(s) failed; nothing written:", file=sys.stderr)
    for msg in failures:
        print("  " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    before_text = OUT.read_text()
    existing = json.loads(before_text)
    tp = t_pvalues(existing["hazard"])
    failures, max_rel = check_t(tp, existing["hazard_robustness"])

    f = hz.samples(pd.read_csv(PP))["F"]
    boot, f2 = score_bootstrap(f)
    failures += f2
    if boot is None:
        fail(failures)
    boot, p_tilde = boot
    size, f3 = size_check(f, p_tilde)
    failures += f3
    if failures:
        fail(failures)

    existing[KEY] = {
        "definition": ("Small-cluster inference per docs/decisions.md 2026-11-01 item E. "
                       "t_correction: p_t = 2 x t_{G-1} tail at the clustered z in "
                       "hazard.models (G = clubs); p_normal is hazard's normal-reference p. "
                       "score_bootstrap: Kline & Santos (2012) wild score bootstrap for strength "
                       "in M2, sample F, restricted fit M2 without strength, Webb weights by "
                       "club, no refitting, H fixed at the restricted estimates; p_bootstrap = "
                       "share of draws with |T*| >= |T|; p_normal = 2 x normal tail at T; no "
                       "small-sample scaling. size_check: the same test on datasets simulated "
                       "under the restricted model."),
        "t_correction": tp,
        "t_correction_F_max_rel_diff_vs_robustness_top6": max_rel,
        "score_bootstrap": boot,
        "size_check": size,
        "checks_passed": True,
    }

    old = json.loads(before_text)
    for k in old:
        if existing[k] != old[k]:
            fail([f"key '{k}' would change"])
    with open(OUT, "w") as fh:
        json.dump(existing, fh, indent=2, default=lambda o: o.item() if hasattr(o, "item") else o)
        fh.write("\n")
    after = json.loads(OUT.read_text())
    changed = [k for k in old if after[k] != old[k]]
    if changed or set(after) != set(old) | {KEY}:
        print(f"WARNING: keys changed after write: {changed}; key sets "
              f"{sorted(set(after) ^ (set(old) | {KEY}))}", file=sys.stderr)
        sys.exit(1)

    print("All checks passed.")
    print("\n== t(G - 1) p-values")
    for s in hz.SAMPLES:
        for m in ("M2", "M2b"):
            print(f"  {s} {m} (df {tp[s][m]['t_df']}): " + ", ".join(
                f"{c} {t['p_t']:.4g}" for c, t in tp[s][m]["terms"].items()))
    print(f"  F vs hazard_robustness top6: max relative difference {max_rel:.3g}")
    print(f"\n== Wild score bootstrap, strength in M2, F (seed {MASTER_SEED}, {DRAWS} draws)")
    print(f"  T = {boot['T']:.6f}, p_bootstrap = {boot['p_bootstrap']:.6f} "
          f"({boot['n_extreme']} / {DRAWS}), p_normal = {boot['p_normal']:.6f}")
    print("  restricted coef: " + ", ".join(f"{c} {v:.6f}"
                                            for c, v in boot["restricted"]["coef"].items()))
    print("  S_g: " + ", ".join(f"{r['team']} {r['S_g']:.5f}" for r in boot["S_g"]))
    print(f"\n== Size check ({SIM_DATASETS} datasets, {SIM_DRAWS} draws)")
    print(f"  fit failures: {size['n_fit_failures']}; fits with notes: "
          f"{size['n_successful_fits_with_notes']}")
    for base in ("successful", "all"):
        r = size[f"rejection_rate_{base}"]
        print(f"  rejection over {base}: 5% {r['5']:.3f}, 10% {r['10']:.3f}")
    print(f"\nWrote {OUT.relative_to(ROOT)} ({KEY}); other keys unchanged.")


if __name__ == "__main__":
    main()
