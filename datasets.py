from __future__ import annotations

import random
from typing import Callable, List


def random_dataset(n: int, seed: int) -> List[int]:
    rng = random.Random(seed)
    return [rng.randint(0, n * 10) for _ in range(n)]


def sorted_dataset(n: int, seed: int) -> List[int]:
    data = random_dataset(n, seed)
    return sorted(data)


def reversed_dataset(n: int, seed: int) -> List[int]:
    data = random_dataset(n, seed)
    return sorted(data, reverse=True)


def nearly_sorted_dataset(n: int, seed: int) -> List[int]:
    rng = random.Random(seed)
    data = sorted_dataset(n, seed)
    if n < 2:
        return data
    swaps = max(1, int(n * 0.03))
    for _ in range(swaps):
        i = rng.randrange(n)
        j = rng.randrange(n)
        data[i], data[j] = data[j], data[i]
    return data


def few_unique_dataset(n: int, seed: int) -> List[int]:
    rng = random.Random(seed)
    uniques = [rng.randint(0, n * 10) for _ in range(max(2, n // 10))]
    return [rng.choice(uniques) for _ in range(n)]


DATASETS: dict[str, Callable[[int, int], List[int]]] = {
    "random": random_dataset,
    "sorted": sorted_dataset,
    "reversed": reversed_dataset,
    "nearly_sorted": nearly_sorted_dataset,
    "few_unique": few_unique_dataset,
}


def generate(name: str, n: int, seed: int) -> List[int]:
    key = name.lower()
    if key not in DATASETS:
        raise ValueError(f"Unknown dataset: {name}")
    return DATASETS[key](n, seed)


def available_datasets() -> List[str]:
    return sorted(DATASETS.keys())
