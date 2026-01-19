# Repository Guidelines

## Project Overview
This repository currently contains the project specification (`README.md`) for a sorting‑algorithm implementation with visualization and benchmarking. The codebase is expected to be Python‑based and to expose a small CLI for running benchmarks and visualizations.

## Project Structure & Module Organization
Use the structure suggested in the spec so components stay decoupled:
- `sorts/` — algorithm implementations (`bubble.py`, `insertion.py`, `selection.py`, `shell.py`) and gap sequences (`gaps.py`).
- `instrumentation.py` — counters and timing helpers.
- `visualizer.py` — event consumer and animation logic.
- `benchmark.py` — benchmark runner and CSV/JSON export.
- `datasets.py` — deterministic dataset generators.
- `main.py` — CLI entry point.
- `results/` — generated CSV/JSON output and plots (do not commit large binaries).

## Build, Test, and Development Commands
No build system is committed yet. When the CLI is implemented, these are the expected entry points (from the spec):
- `python main.py viz --algo bubble --n 50 --seed 123` — run visualization mode.
- `python main.py viz --algo shell --gap knuth --n 60 --speed 2` — visualize a specific gap sequence.
- `python main.py bench --algo all --sizes 100 500 1000 --trials 10 --out results.csv` — benchmark mode.
- `python -m pytest` — run the test suite.

## Coding Style & Naming Conventions
- Python: 4‑space indentation, PEP 8 naming (`snake_case` for functions/vars, `PascalCase` for classes).
- Keep sorting logic free of visualization code; emit events instead.
- Module names should be short, single‑purpose, and lowercase (`datasets.py`, `benchmark.py`).

## Testing Guidelines
Use pytest. Follow `test_*.py` naming, keep tests near the modules they cover or in a top‑level `tests/` folder. The spec requires correctness across edge cases (empty, size‑1, duplicates, sorted, reverse). Ensure trace mode yields the same final array as benchmark mode.

## Commit & Pull Request Guidelines
There is no commit history yet, so no established convention. Use short, imperative subjects (e.g., “Add shell sort gaps”). PRs should include: a brief description, the algorithms touched, and (if applicable) a screenshot/GIF of the visualization and a sample benchmark CSV.

## Configuration Tips
Keep dataset generation deterministic by requiring a `seed` parameter in generators and in benchmark trials. Store large outputs under `results/` and ignore them in version control if they’re regenerated artifacts.
