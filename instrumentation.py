from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple


@dataclass(frozen=True)
class Event:
    kind: str
    indices: Tuple[int, ...]
    value: Optional[Any] = None
    label: Optional[str] = None
    comparisons: int = 0
    swaps: int = 0
    writes: int = 0


class Instrumentation:
    def __init__(self, event_sink: Optional[Callable[[Event], None]] = None) -> None:
        self.comparisons = 0
        self.swaps = 0
        self.writes = 0
        self._event_sink = event_sink

    def _emit(
        self,
        kind: str,
        indices: Tuple[int, ...] = (),
        value: Optional[Any] = None,
        label: Optional[str] = None,
    ) -> None:
        if not self._event_sink:
            return
        event = Event(
            kind=kind,
            indices=tuple(indices),
            value=value,
            label=label,
            comparisons=self.comparisons,
            swaps=self.swaps,
            writes=self.writes,
        )
        self._event_sink(event)

    def compare(
        self,
        a: Any,
        b: Any,
        i: Optional[int] = None,
        j: Optional[int] = None,
        op: str = "lt",
    ) -> bool:
        self.comparisons += 1
        if i is not None and j is not None:
            self._emit("compare", (i, j))
        if op == "lt":
            return a < b
        if op == "gt":
            return a > b
        if op == "le":
            return a <= b
        if op == "ge":
            return a >= b
        if op == "eq":
            return a == b
        if op == "ne":
            return a != b
        raise ValueError(f"Unsupported comparison op: {op}")

    def swap(self, arr: list[Any], i: int, j: int) -> None:
        if i == j:
            return
        arr[i], arr[j] = arr[j], arr[i]
        self.swaps += 1
        self.writes += 2
        self._emit("swap", (i, j))

    def write(self, arr: list[Any], i: int, value: Any) -> None:
        arr[i] = value
        self.writes += 1
        self._emit("write", (i,), value=value)

    def mark(self, i: int, label: str) -> None:
        self._emit("mark", (i,), label=label)
