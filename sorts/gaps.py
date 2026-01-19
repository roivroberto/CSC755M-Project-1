from __future__ import annotations

from math import ceil
from typing import Callable, List


def shell_gaps(n: int) -> List[int]:
    gaps = []
    gap = n // 2
    while gap > 0:
        gaps.append(gap)
        gap //= 2
    return gaps


def knuth_gaps(n: int) -> List[int]:
    gaps = []
    gap = 1
    while gap < n:
        gaps.append(gap)
        gap = gap * 3 + 1
    return list(reversed(gaps))


def hibbard_gaps(n: int) -> List[int]:
    gaps = []
    k = 1
    gap = 1
    while gap < n:
        gaps.append(gap)
        k += 1
        gap = (1 << k) - 1
    return list(reversed(gaps))


def tokuda_gaps(n: int) -> List[int]:
    gaps = []
    k = 1
    while True:
        gap = ceil((9 * (9 / 4) ** (k - 1) - 4) / 5)
        if gap >= n:
            break
        gaps.append(int(gap))
        k += 1
    return list(reversed(gaps))


GAP_VARIANTS: dict[str, Callable[[int], List[int]]] = {
    "shell": shell_gaps,
    "knuth": knuth_gaps,
    "hibbard": hibbard_gaps,
    "tokuda": tokuda_gaps,
}


def get_gaps(variant: str, n: int) -> List[int]:
    key = variant.lower()
    if key not in GAP_VARIANTS:
        raise ValueError(f"Unknown gap variant: {variant}")
    return GAP_VARIANTS[key](n)


def available_variants() -> List[str]:
    return sorted(GAP_VARIANTS.keys())
