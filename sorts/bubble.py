from __future__ import annotations

from instrumentation import Instrumentation


def sort(arr: list[int], inst: Instrumentation, **_: object) -> list[int]:
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if inst.compare(arr[j], arr[j + 1], j, j + 1, op="gt"):
                inst.swap(arr, j, j + 1)
                swapped = True
        if not swapped:
            break
    return arr
