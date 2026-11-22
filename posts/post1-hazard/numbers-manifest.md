# Post 1 abstract: numbers manifest (author's revision after the cold read, 2026-11-22)

Every number and statistical claim in `abstract.md`, with its path in `results/results.json`.
`check_numbers.py` asserts each row. `W` = `writeup_numbers/t_intervals`; `HR` =
`hazard_robustness/variants`. "Fixed thresholds" = top 3 to top 9 under the strict rule; "robustness
variations" = those six other than top 6. Significance = t-based p < 0.05 in M2.

| # | In the abstract | Stored | Path |
|---|---|---|---|
| N1 | 2014–2026 | [2014, 2026] | `seasons` |
| N2 | top 6 of 15; top 3 to top 9 | strict thresholds 3–9 | `HR/*/threshold` |
| N3 | 36 windows, 28 closings (berth-relative) | 36; 28 | `HR/berth/F/{windows,closings}` |
| N4 | 56% after two seasons; 19% after four (berth-relative) | 0.5581; 0.1860 | `HR/berth/survival_after/{2,4}` |
| N5 | Cushion OR 0.67; 95% CI 0.53–0.84; p=0.0017 (berth-relative) | 0.6667 [0.5267, 0.8439]; 0.00172 | `W/…berth/M2/strength` |
| N6 | Age OR 2.60 per doubling of window age; 95% CI 1.21–5.58; p=0.016 (berth-relative) | 2.6018 [1.2131, 5.5803]; 0.0164 | `abstract_derived/age_per_doubling_berth` (= `W/…berth/M2/ln_dur` 3.973 [1.321, 11.946] raised to ln 2) |
| N7 | Without cushion, age not significant (p=0.65) (berth-relative) | p_t 0.6496 | `age_checks/lines/berth/M2_without_strength/terms/ln_dur` |
| N8 | Cushion OR 0.72; 95% CI 0.59–0.89; p=0.0033 (top 6) | 0.7225 [0.5892, 0.8861]; 0.00331 | `W/…top6/M2/strength` |
| N9 | Cushion significant in five of the six robustness variations | significant at 3, 5, 7, 8, 9; not 4 (p 0.129) | `W/…top{3,4,5,7,8,9}/M2/strength/p_t` |
| N10 | Age significant only at top 5 and top 8 (fixed thresholds; top 6 p 0.2995) | {5, 8} | `W/…top{3..9}/M2/ln_dur/p_t` |
| N11 | Payroll not significant in any model | lowest p_t 0.356 (top 7) | `W/…{all nine}/M2/od_log2_rel/p_t` |
| N12 | Postseason format not significant in any model | lowest p_t 0.113 (top 9) | `W/…{all nine}/M2/era12/p_t` |
| N13 | Cushion predicted actually missing the next postseason: OR 0.83; 95% CI 0.73–0.94; p=0.0047 (berth-relative) | 0.827 [0.729, 0.937]; 0.0047 | `realized_outcome_refit/fits/berth_post/terms/strength` |

**Not quoted, available:** fixed-line sample sizes (38, 30, 22 clubs); the grace variant; the age
estimation checks; the fixed-line realized-outcome refit; the Jordan comparison.
