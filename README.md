# Competitive Windows

Do MLB organizations switch from building competitive odds to converting them into championship
probability later than public signal justifies, and does that lag cost them titles? This repo holds
the research plan, the pre-registered predictions, a dated log of every methodological decision,
and the code behind each result.

## Start here

| If you want | Read |
|---|---|
| The first result, in 500 words | [`posts/post1-hazard/abstract.md`](posts/post1-hazard/abstract.md), submitted to the 2027 SABR Analytics Conference |
| How every choice was made, and why | [`docs/decisions.md`](docs/decisions.md), a dated, append-only log of options considered, choices made and corrections |
| The full design | [`docs/competitive-windows-research-plan.md`](docs/competitive-windows-research-plan.md) |
| What was predicted before any data was collected | [`docs/predictions.md`](docs/predictions.md) and [`docs/forecasts-2027.md`](docs/forecasts-2027.md) |

## Status (November 2026)

- **Post 1, how long windows last:** done. A discrete-time hazard model of window closing, using
  2014–2026 Opening Day FanGraphs playoff odds. Exploratory: specifications were set before the data
  was collected, and later changes, made with results in view, are logged.
- **Registered predictions (P1, P2, P4):** not yet tested. The transaction data they depend on has
  not been pulled.
- **2027 window forecasts:** locked October 2026; scored on 2027 Opening Day.

## Pre-registration, and how to check it

- `docs/predictions.md` was locked on 2026-09-20 at commit `5468778` (first version `1663b96`),
  before any data was collected. It is never edited; changes of position go in the decisions log.
- `docs/forecasts-2027.md` was locked on 2026-10-26 at commit `1e95d3f`.
- This repo was published on 2026-11-22 as a copy of a private original, with personal details
  removed from its history. That changed every commit hash, but not the contents of any locked file.
  To check a lock: `git rev-parse 5468778:docs/predictions.md` returns `5a79be7…`, the hash recorded
  in the decisions log. Hashes cited inside the docs before 2026-11-22 refer to the original; the log
  maps them to this repo.
- Commit dates are set by the author's machine, so the public record of the locks starts with
  publication.

## Layout

| Path | Contents |
|---|---|
| `docs/` | Plan, predictions, forecasts, decisions log |
| `src/scrape/`, `src/clean/` | Collection and cleaning scripts (`data/raw/` → `data/processed/`) |
| `src/analysis/` | Analysis scripts; each writes its numbers to `results/results.json` |
| `results/` | `results.json` (every number that appears in writing) and figures |
| `posts/post1-hazard/` | The abstract, a manifest tying each of its numbers to `results.json`, a script that checks them, and the review packets |
| `CLAUDE.md` | Standing rules for AI coding sessions in this repo |

## Data and reproduction

The data is not included. Under FanGraphs' terms of service its tables are not republished, so
`data/` is never committed. Sources: FanGraphs playoff odds (Opening Day and in-season snapshots),
Baseball-Reference standings and preseason odds, and Cot's Contracts payrolls. How each was
collected is recorded in the decisions log.

With the data in place: Python 3.9, `pip install -r requirements.txt`, then the `src/clean/` and
`src/analysis/` scripts. `python3 posts/post1-hazard/check_numbers.py` confirms every number in the
abstract against `results.json`.

## How this was built

The code was written by an AI agent (Claude Code) under my direction. Planning, and independent
re-computation of each result with separate code, happened in a separate Claude session. Draft
results went to referee passes in fresh sessions with no prior context. The decisions log records
what was decided, by whom and why.

## Author

Matt Koizim ([mkoizim.github.io](https://mkoizim.github.io)). I worked in the front offices of the
Dodgers, Marlins and Orioles through 2016. No non-public information from those organizations is
used anywhere in the evidence (plan §2.5).
