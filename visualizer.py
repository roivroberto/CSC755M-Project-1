from __future__ import annotations

from typing import Iterable, List

from instrumentation import Event


def visualize(
    initial: List[int],
    events: Iterable[Event],
    speed: float = 1.0,
    title: str | None = None,
) -> None:
    try:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
    except ImportError as exc:
        raise SystemExit(
            "matplotlib is required for visualization. Install it with 'pip install matplotlib'."
        ) from exc

    data = list(initial)
    event_list = list(events)

    base_color = "#4C78A8"
    compare_color = "#F58518"
    swap_color = "#E45756"
    write_color = "#54A24B"
    mark_color = "#9D755D"

    fig, ax = plt.subplots()
    ax.set_title(title or "Sorting Visualization")
    bars = ax.bar(range(len(data)), data, color=base_color)
    ax.set_xlim(-0.5, max(len(data) - 0.5, 0.5))
    ymax = max(data) * 1.1 if data else 1
    ax.set_ylim(0, ymax)
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    def update(frame: int):
        event = event_list[frame]
        for bar in bars:
            bar.set_color(base_color)

        if event.kind == "compare":
            for idx in event.indices:
                bars[idx].set_color(compare_color)
        elif event.kind == "swap":
            i, j = event.indices
            data[i], data[j] = data[j], data[i]
            bars[i].set_height(data[i])
            bars[j].set_height(data[j])
            bars[i].set_color(swap_color)
            bars[j].set_color(swap_color)
        elif event.kind == "write":
            idx = event.indices[0]
            data[idx] = event.value
            bars[idx].set_height(data[idx])
            bars[idx].set_color(write_color)
        elif event.kind == "mark":
            idx = event.indices[0]
            bars[idx].set_color(mark_color)

        text.set_text(
            f"comparisons: {event.comparisons}  swaps: {event.swaps}  writes: {event.writes}"
        )
        return (*bars, text)

    if not event_list:
        text.set_text("No events to visualize")
        plt.show()
        return

    interval = max(1, int(60 / max(speed, 0.1)))
    anim = FuncAnimation(
        fig, update, frames=len(event_list), interval=interval, repeat=False
    )
    # Keep a reference so the animation isn't garbage collected before show().
    _ = anim
    plt.show()
