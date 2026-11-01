# Competitive windows: rules for every session

Definitions and closed decisions live in `docs/decisions.md`; read the entries a task names before
building. The design is in `docs/competitive-windows-research-plan.md`.

**Never**
- Edit `docs/predictions.md` or `docs/forecasts-2027.md`.
- Edit anything in `docs/` unless the prompt says to. The plan and decisions log are edited in the
  planning chat.
- Overwrite existing keys in `results/results.json`. Merge under the key the prompt names, and
  confirm every other key is unchanged.
- Drop terms, change an estimator or loosen a check to make something run. Stop and report instead.

**Always**
- Run the prompt's checks before reporting. If any fail, stop and report.
- Report results without interpreting them. Interpretation happens in the planning chat.
- Put every number that could appear in prose into `results.json`.
- Use `.venv` for scripts that need numpy, pandas, statsmodels, scipy or matplotlib. Add any new
  package to `requirements.txt` with its exact version.

**Data**
- Collect new data only when the prompt asks. Before collecting from a site not used before, report
  the source, the number of page loads and anything its terms say about automated access, then wait
  for approval.
- Never change or delete existing files in `data/raw/`. New collections go in new files or folders
  under `data/raw/`, saved exactly as collected.
- Files in `data/processed/` are built from `data/raw/` by scripts in `src/clean/` or
  `src/analysis/`. Never edit them by hand.
- Never commit anything under `data/`. Before committing, check that `git status` lists no data
  files.

**Web collection**
- One request at a time, cache every raw page before parsing, never re-fetch a cached page.
- Sports-Reference: at least 6 seconds between requests. Stop on any non-200 response.
- If a site blocks the browser, stop and report. Don't try to get around it.

**Git**
- Don't commit unless the prompt says to. When committing, push too.
