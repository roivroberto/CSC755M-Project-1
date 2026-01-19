# Results Directory

This folder contains submission artifacts.

## Layout
- `benchmarks/` — CSV/JSON benchmark outputs
- `plots/` — derived plots
  - `plots/time/` — time vs n
  - `plots/metrics/` — comparisons/swaps/writes vs n
  - `plots/shell/` — Shell gap comparison plots
- `visuals/` — visualization GIFs and snapshots
- `visuals/highlights/` — example visuals for quick review
  - `visuals/all/` — comprehensive GIFs organized by algorithm
    - `visuals/all/bubble/`
    - `visuals/all/insertion/`
    - `visuals/all/selection/`
    - `visuals/all/shell/`

## Benchmarks
- `benchmarks/results.csv` — full benchmark sweep (all algorithms)
- `benchmarks/shell.json` — shell gap comparison runs
- `benchmarks/insertion.csv` — insertion on nearly_sorted dataset

## Plots
Created with `scripts/generate_plots.py`.

## Visuals
Created with `scripts/generate_visuals.py`.
