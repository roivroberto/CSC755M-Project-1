from __future__ import annotations

from instrumentation import Instrumentation
from sorts.gaps import get_gaps


def sort(
    arr: list[int],
    inst: Instrumentation,
    gap_variant: str = "shell",
    **_: object,
) -> list[int]:
    n = len(arr)
    gaps = get_gaps(gap_variant, n)
    for gap in gaps:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and inst.compare(arr[j - gap], temp, j - gap, j, op="gt"):
                inst.write(arr, j, arr[j - gap])
                j -= gap
            inst.write(arr, j, temp)
    return arr
