from __future__ import annotations

from instrumentation import Instrumentation


def sort(arr: list[int], inst: Instrumentation, **_: object) -> list[int]:
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and inst.compare(arr[j], key, j, j + 1, op="gt"):
            inst.write(arr, j + 1, arr[j])
            j -= 1
        inst.write(arr, j + 1, key)
    return arr
