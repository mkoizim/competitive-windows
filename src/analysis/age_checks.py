"""Age checks on ln duration in M2, both lines, sample F (Post 1).

Per docs/decisions.md, "Age checks on the berth-relative line: specification and decision rule"
(2026-11-11). Rows and design are realized_refit.py's (M2: const + ln(duration capped at 4) + era12 +
strength + od_log2_rel), with the original event (out of the window at n+1's Opening Day).

1. Firth penalized logit (log-likelihood + 1/2 log|X'WX|), fitted twice: Newton iteration on the
   modified score U* = X'(y - p + h(1/2 - p)), h = hat-matrix diagonal; and direct maximization
   with scipy.optimize (BFGS, analytic gradient U*). Penalized LR test for ln duration: 2 x (pl(M2)
   - pl(M2 without ln duration)), chi-square(1).
2. Two-way clustering by club and league-season (league x season n+1): statsmodels'
   cov_cluster_2groups (Cameron-Gelbach-Miller: V_club + V_ls - V_intersection, each with
   statsmodels' G/(G-1) x (N-1)/(N-K) correction). If not PSD, negative eigenvalues are set to 0.
   p-values and intervals against t with min(G_club, G_ls) - 1 df.
3. Wild score bootstrap for ln duration (Kline & Santos 2012), as inference.py does for strength:
   restricted model M2 without ln duration, Webb weights by club, SeedSequence(20261102), 9,999
   draws, no refitting. The stored strength result (hazard_inference.score_bootstrap) is first
   reproduced on the fixed line.
4. Leave-one-club-out refits of M2; t interval with G - 1 df, G = clubs remaining.
5. Functional form, copied from existing keys: M2b's first-year indicator, M1 bin hazards,
   bins-vs-log p (hazard_robustness.variants.top6 / .berth; fixed-line t interval for M2b from
   writeup_numbers).
6. M2 without strength.
7. M2 dropping rows with n = 2019, 2020, 2021.
8. M2 plus ln duration x era12.
Fits 4, 6, 7, 8 cluster by club (hazard.fit_logit), p_t and or_ci95_t with G - 1 df.

Decision rule, berth-relative line, (a)-(f) of the 2026-11-11 entry; age_rule_passes = all six.

Writes results.json's "age_checks" key; every other key is confirmed unchanged byte for byte and by
SHA-256. Nothing is written if any check fails. --dry-run prints only.

Needs the repo's .venv. Run from the repo root: .venv/bin/python src/analysis/age_checks.py
"""

import json
import math
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import optimize, stats
from statsmodels.stats.sandwich_covariance import cov_cluster_2groups

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hazard as hz  # noqa: E402
import inference as inf  # noqa: E402
from jordan import dump  # noqa: E402
from realized_refit import M2_COLS, lines, p_t, t_interval, write_key  # noqa: E402

ROOT = hz.ROOT
OUT = hz.OUT
KEY = "age_checks"
AGE = "ln_dur"
FIRTH_TOL = 1e-6
DROP_SEASONS = [2019, 2020, 2021]
SOURCES = {"fixed": "hazard_robustness.variants.top6", "berth": "hazard_robustness.variants.berth"}
STORED_M2 = {"fixed": "hazard.models.F.M2", "berth": "hazard_robustness.variants.berth.M2"}


def get(r, path):
    for p in path.split("."):
        r = r[p]
    return r


# ---------------------------------------------------------------- clustered fits with t

def fit_t(d, cols):
    """hazard.fit_logit, clustered by team_id; every term with OR, SE, p_normal, p_t, or_ci95_t."""
    dd = d.assign(const=1.0)
    res, notes = hz.fit_logit(dd, cols, cluster=True)
    g = int(d["team_id"].nunique())
    out = {"n_rows": len(d), "n_events": int(d["event"].sum()), "n_clusters": g, "t_df": g - 1,
           "notes": notes, "converged": False, "terms": {}}
    if res is None:
        return out
    out["converged"] = bool(res.mle_retvals.get("converged", False))
    out["loglik"] = float(res.llf)
    for c in cols:
        b, se = float(res.params[c]), float(res.bse[c])
        ci, tc = t_interval(b, se, g)
        out["terms"][c] = {"coef": b, "se_cluster": se, "z": b / se, "odds_ratio": math.exp(b),
                           "p_normal": float(res.pvalues[c]), "p_t": p_t(b / se, g),
                           "or_ci95_t": ci}
    return out


def excludes_1(ci):
    return bool(ci[0] > 1 or ci[1] < 1)


def age_summary(fit):
    t = fit["terms"][AGE]
    return {"odds_ratio": t["odds_ratio"], "or_ci95_t": t["or_ci95_t"], "p_t": t["p_t"]}


# ---------------------------------------------------------------- 1. Firth

def _parts(X, y, b):
    eta = X @ b
    p = 1 / (1 + np.exp(-eta))
    w = p * (1 - p)
    info = (X * w[:, None]).T @ X
    sign, logdet = np.linalg.slogdet(info)
    ll = float(np.sum(y * eta - np.logaddexp(0, eta)))
    pl = ll + 0.5 * logdet
    info_inv = np.linalg.inv(info)
    h = w * np.einsum("ij,jk,ik->i", X, info_inv, X)
    score = X.T @ (y - p + h * (0.5 - p))
    return pl, score, info_inv, ll


def firth_newton(X, y, tol=1e-12, maxiter=200):
    b = np.zeros(X.shape[1])
    pl, score, info_inv, _ = _parts(X, y, b)
    for it in range(1, maxiter + 1):
        step = info_inv @ score
        t = 1.0
        while True:   # step-halving if the penalized log-likelihood falls
            nb = b + t * step
            npl, nscore, ninv, _ = _parts(X, y, nb)
            if npl >= pl - 1e-12 or t < 1e-8:
                break
            t /= 2
        b, pl, score, info_inv = nb, npl, nscore, ninv
        if np.max(np.abs(t * step)) < tol and np.max(np.abs(score)) < 1e-9:
            return b, pl, it, True
    return b, pl, maxiter, False


def firth_scipy(X, y):
    def f(b):
        pl, score, _, _ = _parts(X, y, b)
        return -pl, -score
    r = optimize.minimize(f, np.zeros(X.shape[1]), jac=True, method="BFGS",
                          options={"gtol": 1e-11, "maxiter": 10_000})
    return r.x, -float(r.fun), int(r.nit), bool(r.success), str(r.message)


def firth(d):
    y = d["event"].to_numpy(float)
    out, fails = {}, []
    for name, cols in (("M2", M2_COLS), ("M2_without_ln_dur", [c for c in M2_COLS if c != AGE])):
        X = d.assign(const=1.0)[cols].to_numpy(float)
        bn, pln, itn, okn = firth_newton(X, y)
        bs, pls, its, oks, msg = firth_scipy(X, y)
        diff = float(np.max(np.abs(bn - bs)))
        if not okn:
            fails.append(f"Firth Newton {name} did not converge")
        if diff >= FIRTH_TOL:
            fails.append(f"(8) Firth {name}: Newton and scipy differ by {diff:.3g}")
        out[name] = {"terms": {c: {"coef": float(b), "odds_ratio": math.exp(b),
                                   "coef_scipy": float(s)} for c, b, s in zip(cols, bn, bs)},
                     "penalized_loglik": pln, "penalized_loglik_scipy": pls,
                     "newton_iterations": itn, "newton_converged": okn,
                     "scipy_iterations": its, "scipy_success": oks, "scipy_message": msg,
                     "max_abs_coef_diff_newton_scipy": diff}
    lr = 2 * (out["M2"]["penalized_loglik"] - out["M2_without_ln_dur"]["penalized_loglik"])
    out["penalized_lr_ln_dur"] = {"stat": lr, "df": 1, "p": float(stats.chi2.sf(lr, 1))}
    out["ln_dur"] = {"odds_ratio": out["M2"]["terms"][AGE]["odds_ratio"],
                     "p_penalized_lr": out["penalized_lr_ln_dur"]["p"]}
    return out, fails


# ---------------------------------------------------------------- 2. two-way clustering

def two_way(d):
    dd = d.assign(const=1.0)
    club = pd.factorize(d["team_id"])[0]
    ls = pd.factorize(d["league"].astype(str) + "-" + (d["season"] + 1).astype(str))[0]
    g_club, g_ls = int(len(set(club))), int(len(set(ls)))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        res = sm.Logit(dd["event"].astype(float), dd[M2_COLS].astype(float)).fit(
            disp=0, maxiter=200)
    notes = [str(w.message) for w in caught]
    V, V_club, V_ls = cov_cluster_2groups(res, np.column_stack([club, ls]))
    eig = np.linalg.eigvalsh(V)
    fixed = bool(eig.min() < 0)
    if fixed:
        val, vec = np.linalg.eigh(V)
        V = vec @ np.diag(np.clip(val, 0, None)) @ vec.T
    df = min(g_club, g_ls) - 1
    tc = float(stats.t.ppf(0.975, df))
    terms = {}
    for i, c in enumerate(M2_COLS):
        b, se = float(res.params[c]), float(math.sqrt(V[i, i]))
        terms[c] = {"coef": b, "se_two_way": se, "odds_ratio": math.exp(b),
                    "se_club_only": float(math.sqrt(V_club[i, i])),
                    "se_league_season_only": float(math.sqrt(V_ls[i, i])),
                    "p_t": float(2 * stats.t.sf(abs(b / se), df)),
                    "or_ci95_t": [math.exp(b - tc * se), math.exp(b + tc * se)]}
    return {"G_club": g_club, "G_league_season": g_ls, "t_df": df, "t_crit": tc,
            "converged": bool(res.mle_retvals.get("converged", False)), "notes": notes,
            "eigenvalues": [float(x) for x in eig], "psd": not fixed,
            "eigenvalue_fix_applied": fixed,
            "method": ("statsmodels cov_cluster_2groups: V_club + V_league_season - "
                       "V_intersection, each with G/(G-1) x (N-1)/(N-K)"),
            "terms": terms}


# ---------------------------------------------------------------- 3. wild score bootstrap

def club_scores(d, p, test):
    """inference.club_scores for an arbitrary tested term."""
    X = d.assign(const=1.0)[M2_COLS].to_numpy(float)
    j = M2_COLS.index(test)
    th = [i for i in range(len(M2_COLS)) if i != j]
    u = d["event"].to_numpy(float) - p
    H = (X * (p * (1 - p))[:, None]).T @ X
    proj = np.linalg.solve(H[np.ix_(th, th)], H[th, j])
    e = u * (X[:, j] - X[:, th] @ proj)
    clubs, idx = np.unique(d["team_id"].to_numpy(), return_inverse=True)
    S = np.bincount(idx, weights=e)
    return clubs, S, float(np.abs(X[:, th].T @ u).max())


def score_bootstrap(d, test):
    theta = [c for c in M2_COLS if c != test]
    res, notes = hz.fit_logit(d.assign(const=1.0), theta, cluster=False)
    if not inf.converged(res):
        return None, [f"restricted fit for {test} did not converge: {notes}"]
    clubs, S, score_theta = club_scores(d, np.asarray(res.predict()), test)
    out = inf.wild_score(S, inf.DRAWS,
                         np.random.default_rng(np.random.SeedSequence(inf.MASTER_SEED)))
    out.update({"term": test, "restricted_terms": theta, "n_clusters": len(clubs),
                "master_seed": inf.MASTER_SEED, "draws": inf.DRAWS,
                "restricted_score_max_abs": score_theta, "restricted_notes": notes})
    fails = []
    if score_theta > inf.SCORE_TOL:
        fails.append(f"restricted score for {test} not 0: {score_theta:.3g}")
    return out, fails


# ---------------------------------------------------------------- 4. leave one club out

def loco(d, full_ci):
    """A removal 'puts 1 in the interval' only if the full-sample t interval excludes 1; when it
    already includes 1 that list is null and only the raw include/exclude lists are given."""
    rows, fails = [], []
    team = d.drop_duplicates("team_id").set_index("team_id")["team"]
    for tid in sorted(d["team_id"].unique(), key=lambda t: team[t]):
        f = fit_t(d[d["team_id"] != tid], M2_COLS)
        ok = f["converged"] and AGE in f["terms"]
        row = {"dropped": team[tid], "team_id": int(tid), "n_rows": f["n_rows"],
               "n_events": f["n_events"], "n_clusters": f["n_clusters"], "converged": ok,
               "notes": f["notes"]}
        if ok:
            row.update(age_summary(f))
            row["interval_includes_1"] = not excludes_1(f["terms"][AGE]["or_ci95_t"])
        else:
            fails.append(f"(10) LOCO without {team[tid]} did not converge: {f['notes']}")
        rows.append(row)
    incl = [r["dropped"] for r in rows if r.get("interval_includes_1")]
    excl = [r["dropped"] for r in rows if r["converged"] and not r["interval_includes_1"]]
    full_excl = excludes_1(full_ci)
    return {"fits": rows, "full_sample_or_ci95_t": full_ci,
            "full_sample_interval_excludes_1": full_excl,
            "clubs_whose_removal_puts_1_in_interval": incl if full_excl else None,
            "clubs_with_interval_including_1": incl,
            "clubs_with_interval_excluding_1": excl,
            "n_fits": len(rows), "n_not_converged": sum(not r["converged"] for r in rows),
            "fits_with_notes": [r["dropped"] for r in rows if r["notes"]],
            "or_range": [min(r["odds_ratio"] for r in rows if r["converged"]),
                         max(r["odds_ratio"] for r in rows if r["converged"])]}, fails


# ---------------------------------------------------------------- 5. copies

def functional_form(r, line):
    src = SOURCES[line]
    v = get(r, src)
    dur1 = v["M2b"]["terms"]["dur1"]
    out = {"source": src,
           "M2b_dur1": {"odds_ratio": dur1["odds_ratio"], "or_ci95": dur1["or_ci95"],
                        "p_t": dur1["p_t"],
                        "source": f"{src}.M2b.terms.dur1 (or_ci95 normal reference)"},
           "M1_bins": v["M1"]["bins"],
           "M1_source": f"{src}.M1.bins",
           "bins_vs_log_p": v["lr_bins_vs_log"]["p"],
           "bins_vs_log_source": f"{src}.lr_bins_vs_log.p"}
    if line == "fixed":
        out["M2b_dur1"]["or_ci95_t"] = \
            r["writeup_numbers"]["t_intervals"]["hazard.models.F"]["M2b"]["dur1"]["or_ci95_t"]
        out["M2b_dur1"]["or_ci95_t_source"] = \
            "writeup_numbers.t_intervals.hazard.models.F.M2b.dur1.or_ci95_t"
    return out


def check_copies(r, ff, line):
    src = get(r, SOURCES[line])
    pairs = [(ff["M2b_dur1"]["odds_ratio"], src["M2b"]["terms"]["dur1"]["odds_ratio"]),
             (ff["M2b_dur1"]["or_ci95"], src["M2b"]["terms"]["dur1"]["or_ci95"]),
             (ff["M2b_dur1"]["p_t"], src["M2b"]["terms"]["dur1"]["p_t"]),
             (ff["M1_bins"], src["M1"]["bins"]),
             (ff["bins_vs_log_p"], src["lr_bins_vs_log"]["p"])]
    if line == "fixed":
        pairs.append((ff["M2b_dur1"]["or_ci95_t"], r["writeup_numbers"]["t_intervals"]
                      ["hazard.models.F"]["M2b"]["dur1"]["or_ci95_t"]))
    return [f"(11) {line}: copied value differs from source"
            for a, b in pairs if dump(a) != dump(b)]


# ---------------------------------------------------------------- main

def run_line(line, d, r):
    fails = []
    out = {"rows": len(d), "events": int(d["event"].sum()), "clubs": int(d["team_id"].nunique())}
    # check 1: original event reproduces stored M2
    m2 = fit_t(d, M2_COLS)
    stored = get(r, STORED_M2[line])["terms"]
    mx = max(abs(m2["terms"][c][k] - stored[c][k]) for c in M2_COLS for k in ("coef", "se_cluster"))
    if not mx < 1e-10:
        fails.append(f"(1) {line}: M2 differs from stored by {mx:.3g}")
    out["M2"] = m2
    out["M2_max_abs_diff_vs_stored"] = mx

    out["firth"], f1 = firth(d)
    fails += f1
    out["two_way_cluster"] = two_way(d)
    if not out["two_way_cluster"]["converged"]:
        fails.append(f"{line}: two-way base fit did not converge")
    out["wild_score_bootstrap_ln_dur"], f3 = score_bootstrap(d, AGE)
    fails += f3
    out["leave_one_club_out"], f4 = loco(d, m2["terms"][AGE]["or_ci95_t"])
    fails += f4
    out["functional_form"] = functional_form(r, line)
    fails += check_copies(r, out["functional_form"], line)
    out["M2_without_strength"] = fit_t(d, [c for c in M2_COLS if c != "strength"])
    dd = d[~d["season"].isin(DROP_SEASONS)]
    out["drop_line_change_rows"] = {"dropped_seasons_n": DROP_SEASONS,
                                    "rows": len(dd), "closings": int(dd["event"].sum()),
                                    "clubs": int(dd["team_id"].nunique()),
                                    "fit": fit_t(dd, M2_COLS)}
    out["age_x_era"] = fit_t(d.assign(ln_dur_x_era12=d[AGE] * d["era12"]),
                             M2_COLS + ["ln_dur_x_era12"])
    for name, f in (("M2_without_strength", out["M2_without_strength"]),
                    ("drop_line_change_rows", out["drop_line_change_rows"]["fit"]),
                    ("age_x_era", out["age_x_era"])):
        if not f["converged"]:
            fails.append(f"{line} {name} did not converge: {f['notes']}")
    return out, fails


def main():
    dry_run = "--dry-run" in sys.argv
    r = json.loads(OUT.read_text())
    L = lines()
    fails = []

    # check 9: reproduce the stored strength bootstrap on the fixed line
    stored = r["hazard_inference"]["score_bootstrap"]
    rep, f9 = score_bootstrap(L["fixed"], "strength")
    fails += f9
    if rep is None or abs(rep["T"] - stored["T"]) >= 1e-10 or rep["n_extreme"] != stored["n_extreme"]:
        fails.append(f"(9) strength bootstrap: T {rep and rep['T']} vs {stored['T']}, n_extreme "
                     f"{rep and rep['n_extreme']} vs {stored['n_extreme']}")
    if fails:
        print("Check 9 failed; nothing run or written:", file=sys.stderr)
        for msg in fails:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    res_lines = {}
    for line, d in L.items():
        res_lines[line], f = run_line(line, d, r)
        fails += f
    if fails:
        print(f"{len(fails)} check(s) failed; nothing written:", file=sys.stderr)
        for msg in fails:
            print("  " + msg, file=sys.stderr)
        sys.exit(1)

    b = res_lines["berth"]
    a_ci = r["writeup_numbers"]["t_intervals"]["hazard_robustness.variants.berth"]["M2"][AGE][
        "or_ci95_t"]
    rule = {
        "a_M2_t_interval_excludes_1": excludes_1(a_ci),
        "b_firth_or_gt_1_and_penalized_lr_p_lt_05": bool(
            b["firth"]["ln_dur"]["odds_ratio"] > 1 and b["firth"]["ln_dur"]["p_penalized_lr"] < 0.05),
        "c_two_way_t_interval_excludes_1": excludes_1(
            b["two_way_cluster"]["terms"][AGE]["or_ci95_t"]),
        "d_wild_score_bootstrap_p_lt_05": bool(
            b["wild_score_bootstrap_ln_dur"]["p_bootstrap"] < 0.05),
        "e_no_club_removal_puts_1_in_interval": bool(
            b["leave_one_club_out"]["full_sample_interval_excludes_1"]
            and not b["leave_one_club_out"]["clubs_with_interval_including_1"]),
        "f_or_gt_1_without_line_change_rows": bool(
            b["drop_line_change_rows"]["fit"]["terms"][AGE]["odds_ratio"] > 1),
    }
    rule["age_rule_passes"] = all(rule.values())
    rule["line"] = "berth"
    rule["a_source"] = ("writeup_numbers.t_intervals.hazard_robustness.variants.berth.M2.ln_dur."
                        "or_ci95_t")
    rule["a_interval"] = a_ci

    res = {
        "definition": (
            "Checks on ln(duration capped at 4) in M2, sample F, original event, per docs/"
            "decisions.md 2026-11-11 'Age checks on the berth-relative line'. Lines: fixed = "
            "hazard_pp.csv; berth = hazard_robustness_pp.csv variant berth. Club-clustered fits "
            "use hazard.fit_logit; p_t and or_ci95_t use t with G - 1 df (G = clubs in the fit). "
            "Firth: log-likelihood + 1/2 log|X'WX|, Newton on the modified score and scipy BFGS; "
            "coefficients reported are Newton's; penalized LR = 2 x (pl(M2) - pl(M2 without ln_dur"
            ")), chi2(1). Two-way: club and league x season n+1, statsmodels cov_cluster_2groups, "
            "t with min(G) - 1 df. Wild score bootstrap: inference.py's procedure with ln_dur as "
            "the tested term (restricted model M2 without ln_dur), Webb weights by club, "
            "SeedSequence(20261102), 9,999 draws. Functional form copied from existing keys. Drop "
            "rows: n in 2019, 2020, 2021. Interaction: ln_dur x era12 added to M2."),
        "strength_bootstrap_reproduction": {"T": rep["T"], "n_extreme": rep["n_extreme"],
                                            "stored_T": stored["T"],
                                            "stored_n_extreme": stored["n_extreme"],
                                            "abs_T_diff": abs(rep["T"] - stored["T"])},
        "lines": res_lines,
        "rule": rule,
        "checks": {"passed": True},
    }

    print("All checks passed.")
    print(f"  strength bootstrap reproduced: T {rep['T']!r} (stored {stored['T']!r}), n_extreme "
          f"{rep['n_extreme']} (stored {stored['n_extreme']})")
    for line, o in res_lines.items():
        print(f"\n== {line}: {o['rows']} rows, {o['events']} closings, {o['clubs']} clubs; "
              f"M2 max diff vs stored {o['M2_max_abs_diff_vs_stored']:.3g}")
        fm = o["firth"]
        print(f"  Firth: max |Newton - scipy| M2 {fm['M2']['max_abs_coef_diff_newton_scipy']:.3g},"
              f" restricted {fm['M2_without_ln_dur']['max_abs_coef_diff_newton_scipy']:.3g}; "
              f"ORs " + ", ".join(f"{c} {t['odds_ratio']:.3f}" for c, t in fm["M2"]["terms"].items())
              + f"; pen. LR {fm['penalized_lr_ln_dur']['stat']:.3f}, p "
              f"{fm['penalized_lr_ln_dur']['p']:.4f}")
        tw = o["two_way_cluster"]
        print(f"  Two-way: G_club {tw['G_club']}, G_ls {tw['G_league_season']}, df {tw['t_df']}, "
              f"PSD {tw['psd']}, min eig {min(tw['eigenvalues']):.3g}")
        for c, t in tw["terms"].items():
            print(f"    {c:12} OR {t['odds_ratio']:.3f} SE {t['se_two_way']:.3f} (club "
                  f"{t['se_club_only']:.3f}, ls {t['se_league_season_only']:.3f}) p_t "
                  f"{t['p_t']:.4f} [{t['or_ci95_t'][0]:.3f}, {t['or_ci95_t'][1]:.3f}]")
        wb = o["wild_score_bootstrap_ln_dur"]
        print(f"  Bootstrap ln_dur: T {wb['T']:.4f}, n_extreme {wb['n_extreme']}, p_boot "
              f"{wb['p_bootstrap']:.4f}, p_normal {wb['p_normal']:.4f}")
        lc = o["leave_one_club_out"]
        print(f"  LOCO: {lc['n_fits']} fits, {lc['n_not_converged']} not converged, notes "
              f"{lc['fits_with_notes']}; OR range {lc['or_range']}; flips "
              f"{lc['clubs_whose_removal_puts_1_in_interval']}; incl-1 {lc['clubs_with_interval_including_1']}")
        for row in lc["fits"]:
            print(f"    -{row['dropped']:4} G {row['n_clusters']} OR {row['odds_ratio']:.3f} "
                  f"[{row['or_ci95_t'][0]:.3f}, {row['or_ci95_t'][1]:.3f}] p_t {row['p_t']:.4f}")
        ff = o["functional_form"]
        print(f"  M2b dur1: {json.dumps(ff['M2b_dur1'])}")
        print(f"  M1 bins: " + "; ".join(f"{k} {v.get('hazard', v.get('hazard_raw'))}"
                                        for k, v in ff["M1_bins"].items())
              + f"; bins vs log p {ff['bins_vs_log_p']}")
        for name, f in (("M2", o["M2"]), ("M2 without strength", o["M2_without_strength"]),
                        ("drop n 2019-21", o["drop_line_change_rows"]["fit"])):
            s = age_summary(f)
            print(f"  {name}: rows {f['n_rows']}, events {f['n_events']}, G {f['n_clusters']}; "
                  f"ln_dur OR {s['odds_ratio']:.3f} [{s['or_ci95_t'][0]:.3f}, "
                  f"{s['or_ci95_t'][1]:.3f}] p_t {s['p_t']:.4f}; notes {f['notes']}")
        print(f"  Age x era (notes {o['age_x_era']['notes']}):")
        for c, t in o["age_x_era"]["terms"].items():
            print(f"    {c:15} OR {t['odds_ratio']:.3f} SE {t['se_cluster']:.3f} p_t {t['p_t']:.4f}"
                  f" [{t['or_ci95_t'][0]:.3f}, {t['or_ci95_t'][1]:.3f}]")
    print("\n== Rule (berth):", json.dumps(rule, indent=1))
    write_key(KEY, res, dry_run)


if __name__ == "__main__":
    main()
