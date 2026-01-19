from __future__ import annotations

import csv
import json
import os
import random
import time
from typing import Iterable, List

from datasets import available_datasets, generate
from instrumentation import Instrumentation
from sorts import ALGORITHMS
from sorts.gaps import available_variants


def _ensure_output_dir(path: str) -> None:
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def _build_seed_map(
    datasets: Iterable[str],
    sizes: Iterable[int],
    trials: int,
    base_seed: int,
) -> dict[tuple[str, int, int], int]:
    rng = random.Random(base_seed)
    seeds: dict[tuple[str, int, int], int] = {}
    for dataset in datasets:
        for n in sizes:
            for trial in range(1, trials + 1):
                seeds[(dataset, n, trial)] = rng.randint(0, 2**32 - 1)
    return seeds


def run_benchmarks(
    algorithms: Iterable[str],
    sizes: Iterable[int],
    datasets: Iterable[str],
    trials: int,
    base_seed: int,
    gap_variants: Iterable[str] | None = None,
) -> List[dict[str, object]]:
    results: List[dict[str, object]] = []
    gap_variants = list(gap_variants or available_variants())

    seed_map = _build_seed_map(datasets, sizes, trials, base_seed)

    for algo in algorithms:
        if algo not in ALGORITHMS:
            raise ValueError(f"Unknown algorithm: {algo}")
        algo_fn = ALGORITHMS[algo]
        variants = gap_variants if algo == "shell" else [""]

        for variant in variants:
            for dataset in datasets:
                for n in sizes:
                    for trial in range(1, trials + 1):
                        seed = seed_map[(dataset, n, trial)]
                        base_data = generate(dataset, n, seed)
                        data = list(base_data)
                        inst = Instrumentation()
                        start = time.perf_counter()
                        algo_fn(data, inst, gap_variant=variant)
                        elapsed_ms = (time.perf_counter() - start) * 1000

                        results.append(
                            {
                                "algorithm": algo,
                                "gap_variant": variant,
                                "n": n,
                                "dataset": dataset,
                                "trial": trial,
                                "seed": seed,
                                "time_ms": round(elapsed_ms, 4),
                                "comparisons": inst.comparisons,
                                "swaps": inst.swaps,
                                "writes": inst.writes,
                            }
                        )
    return results


def write_results(path: str, rows: List[dict[str, object]]) -> None:
    _ensure_output_dir(path)
    if path.lower().endswith(".json"):
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(rows, handle, indent=2)
        return

    fieldnames = [
        "algorithm",
        "gap_variant",
        "n",
        "dataset",
        "trial",
        "seed",
        "time_ms",
        "comparisons",
        "swaps",
        "writes",
    ]
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def default_sizes() -> List[int]:
    return [50, 100, 200, 500, 1000, 2000, 5000]


def default_datasets() -> List[str]:
    return available_datasets()
