from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Dict, List, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
BENCH_DIR = RESULTS_DIR / "benchmarks"
PLOTS_DIR = RESULTS_DIR / "plots"
TIME_DIR = PLOTS_DIR / "time"
METRICS_DIR = PLOTS_DIR / "metrics"
SHELL_DIR = PLOTS_DIR / "shell"
for path in (PLOTS_DIR, TIME_DIR, METRICS_DIR, SHELL_DIR):
    path.mkdir(parents=True, exist_ok=True)


def _load_results_csv(path: Path) -> List[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def _load_shell_json(path: Path) -> List[dict[str, object]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _filter_results(results: List[dict[str, str]], dataset: str) -> List[dict[str, str]]:
    return [
        row
        for row in results
        if row.get("dataset") == dataset
        and (row.get("algorithm") != "shell" or row.get("gap_variant") == "shell")
    ]


def plot_metric_by_dataset(
    results: List[dict[str, str]],
    dataset: str,
    metric: str,
    label: str,
) -> Path | None:
    filtered = _filter_results(results, dataset)
    if not filtered:
        return None

    values: Dict[Tuple[str, int], List[float]] = defaultdict(list)
    for row in filtered:
        algo = row["algorithm"]
        n = int(row["n"])
        values[(algo, n)].append(float(row[metric]))

    algos = sorted({row["algorithm"] for row in filtered})
    fig, ax = plt.subplots()
    for algo in algos:
        ns = sorted({n for (a, n) in values.keys() if a == algo})
        avg_vals = [mean(values[(algo, n)]) for n in ns]
        ax.plot(ns, avg_vals, marker="o", label=algo)

    ax.set_title(f"Average {label} vs N ({dataset} dataset)")
    ax.set_xlabel("n")
    ax.set_ylabel(label)
    ax.legend()
    ax.grid(True, alpha=0.3)

    out_dir = TIME_DIR if metric == "time_ms" else METRICS_DIR
    out = out_dir / f"{metric}_{dataset}_all_algos.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def plot_shell_gap_comparison(
    rows: List[dict[str, object]],
    dataset: str | None = None,
) -> Path | None:
    if not rows:
        return None

    datasets = sorted({row["dataset"] for row in rows if "dataset" in row})
    dataset = dataset or ("random" if "random" in datasets else (datasets[0] if datasets else ""))
    filtered = [row for row in rows if (not dataset or row.get("dataset") == dataset)]
    if not filtered:
        filtered = rows
        dataset = dataset or filtered[0].get("dataset", "")

    times: Dict[Tuple[str, int], List[float]] = defaultdict(list)
    for row in filtered:
        variant = str(row.get("gap_variant", ""))
        n = int(row.get("n", 0))
        times[(variant, n)].append(float(row.get("time_ms", 0.0)))

    variants = sorted({v for (v, _) in times.keys()})
    fig, ax = plt.subplots()
    for variant in variants:
        ns = sorted({n for (v, n) in times.keys() if v == variant})
        avg_times = [mean(times[(variant, n)]) for n in ns]
        label = variant or "(none)"
        ax.plot(ns, avg_times, marker="o", label=label)

    title = "Shell Sort Gap Comparison"
    if dataset:
        title += f" ({dataset} dataset)"
    ax.set_title(title)
    ax.set_xlabel("n")
    ax.set_ylabel("time_ms")
    ax.legend(title="gap_variant")
    ax.grid(True, alpha=0.3)

    suffix = f"_{dataset}" if dataset else ""
    out = SHELL_DIR / f"shell_gap_comparison{suffix}.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


if __name__ == "__main__":
    results_csv = _load_results_csv(BENCH_DIR / "results.csv")
    if not results_csv:
        results_csv = _load_results_csv(RESULTS_DIR / "results.csv")

    shell_json = _load_shell_json(BENCH_DIR / "shell.json")
    if not shell_json:
        shell_json = _load_shell_json(RESULTS_DIR / "shell.json")
    datasets = sorted({row["dataset"] for row in results_csv})

    for dataset in datasets:
        plot_metric_by_dataset(results_csv, dataset, "time_ms", "time_ms")
        plot_metric_by_dataset(results_csv, dataset, "comparisons", "comparisons")
        plot_metric_by_dataset(results_csv, dataset, "swaps", "swaps")
        plot_metric_by_dataset(results_csv, dataset, "writes", "writes")

    for dataset in sorted({row.get("dataset") for row in shell_json if "dataset" in row}):
        plot_shell_gap_comparison(shell_json, dataset=dataset)
