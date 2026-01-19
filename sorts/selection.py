from __future__ import annotations

from instrumentation import Instrumentation


def sort(arr: list[int], inst: Instrumentation, **_: object) -> list[int]:
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if inst.compare(arr[j], arr[min_idx], j, min_idx, op="lt"):
                min_idx = j
        if min_idx != i:
            inst.swap(arr, i, min_idx)
    return arr
