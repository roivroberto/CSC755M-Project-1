from __future__ import annotations

import pytest

from datasets import available_datasets, generate
from instrumentation import Instrumentation
from sorts import ALGORITHMS
from sorts.gaps import available_variants


def _run_algorithm(algo: str, data: list[int], gap_variant: str = "shell") -> list[int]:
    inst = Instrumentation()
    arr = list(data)
    ALGORITHMS[algo](arr, inst, gap_variant=gap_variant)
    return arr


@pytest.mark.parametrize(
    "data",
    [
        [],
        [1],
        [2, 1, 2],
        list(range(10)),
        list(range(9, -1, -1)),
    ],
)
@pytest.mark.parametrize("algo", sorted(ALGORITHMS.keys()))
def test_sort_correctness(algo: str, data: list[int]) -> None:
    if algo == "shell":
        for variant in available_variants():
            result = _run_algorithm(algo, data, gap_variant=variant)
            assert result == sorted(data)
    else:
        result = _run_algorithm(algo, data)
        assert result == sorted(data)


@pytest.mark.parametrize("dataset", available_datasets())
def test_dataset_determinism(dataset: str) -> None:
    first = generate(dataset, 50, 123)
    second = generate(dataset, 50, 123)
    assert first == second


@pytest.mark.parametrize("algo", sorted(ALGORITHMS.keys()))
def test_trace_matches_benchmark(algo: str) -> None:
    data = generate("random", 30, 99)

    base = list(data)
    inst_bench = Instrumentation()
    ALGORITHMS[algo](base, inst_bench, gap_variant="shell")

    events = []
    inst_trace = Instrumentation(event_sink=events.append)
    traced = list(data)
    ALGORITHMS[algo](traced, inst_trace, gap_variant="shell")

    assert base == traced
