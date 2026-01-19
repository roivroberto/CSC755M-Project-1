from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from datasets import available_datasets, generate
from instrumentation import Event, Instrumentation
from sorts import ALGORITHMS
from sorts.gaps import available_variants

BASE_COLOR = "#4C78A8"
COMPARE_COLOR = "#F58518"
SWAP_COLOR = "#E45756"
WRITE_COLOR = "#54A24B"
MARK_COLOR = "#9D755D"


def collect_events(
    algo: str,
    n: int,
    dataset: str,
    seed: int,
    gap_variant: str | None = None,
) -> Tuple[List[int], List[Event]]:
    data = generate(dataset, n, seed)
    initial = list(data)
    events: List[Event] = []
    inst = Instrumentation(event_sink=events.append)
    sort_fn = ALGORITHMS[algo]
    sort_fn(data, inst, gap_variant=gap_variant or "shell")
    return initial, events


def downsample(events: List[Event], max_frames: int = 600) -> List[Event]:
    if len(events) <= max_frames:
        return events
    stride = max(1, math.ceil(len(events) / max_frames))
    sampled = events[::stride]
    if sampled[-1] is not events[-1]:
        sampled.append(events[-1])
    return sampled


def apply_event(data: List[int], event: Event) -> None:
    if event.kind == "swap":
        i, j = event.indices
        data[i], data[j] = data[j], data[i]
    elif event.kind == "write":
        idx = event.indices[0]
        data[idx] = event.value


def save_gif(
    initial: List[int],
    events: Iterable[Event],
    path: Path,
    title: str,
    fps: int = 30,
) -> None:
    events_list = list(events)
    data = list(initial)

    fig, ax = plt.subplots()
    ax.set_title(title)
    bars = ax.bar(range(len(data)), data, color=BASE_COLOR)
    ax.set_xlim(-0.5, max(len(data) - 0.5, 0.5))
    ymax = max(data) * 1.1 if data else 1
    ax.set_ylim(0, ymax)
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    def update(frame: int):
        event = events_list[frame]
        for bar in bars:
            bar.set_color(BASE_COLOR)

        if event.kind == "compare":
            for idx in event.indices:
                bars[idx].set_color(COMPARE_COLOR)
        elif event.kind == "swap":
            i, j = event.indices
            data[i], data[j] = data[j], data[i]
            bars[i].set_height(data[i])
            bars[j].set_height(data[j])
            bars[i].set_color(SWAP_COLOR)
            bars[j].set_color(SWAP_COLOR)
        elif event.kind == "write":
            idx = event.indices[0]
            data[idx] = event.value
            bars[idx].set_height(data[idx])
            bars[idx].set_color(WRITE_COLOR)
        elif event.kind == "mark":
            idx = event.indices[0]
            bars[idx].set_color(MARK_COLOR)

        text.set_text(
            f"comparisons: {event.comparisons}  swaps: {event.swaps}  writes: {event.writes}"
        )
        return (*bars, text)

    anim = FuncAnimation(fig, update, frames=len(events_list), interval=1000 / fps, repeat=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    anim.save(path, writer=PillowWriter(fps=fps))
    plt.close(fig)


def save_snapshot(
    initial: List[int],
    events: Iterable[Event],
    path: Path,
    title: str,
    steps: int = 200,
) -> None:
    data = list(initial)
    events_list = list(events)
    for event in events_list[:steps]:
        apply_event(data, event)

    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.bar(range(len(data)), data, color=BASE_COLOR)
    ax.set_xlim(-0.5, max(len(data) - 0.5, 0.5))
    ymax = max(data) * 1.1 if data else 1
    ax.set_ylim(0, ymax)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    out_dir = Path("results/visuals")
    highlights_dir = out_dir / "highlights"
    all_dir = out_dir / "all"
    all_dir.mkdir(parents=True, exist_ok=True)
    highlights_dir.mkdir(parents=True, exist_ok=True)

    n = 50
    seed = 123
    fps = 24
    max_frames = 350

    datasets = available_datasets()
    gap_variants = available_variants()

    for algo in sorted(ALGORITHMS.keys()):
        algo_dir = all_dir / algo
        algo_dir.mkdir(parents=True, exist_ok=True)
        if algo == "shell":
            for dataset in datasets:
                for gap in gap_variants:
                    initial, events = collect_events(
                        algo=algo, n=n, dataset=dataset, seed=seed, gap_variant=gap
                    )
                    events = downsample(events, max_frames=max_frames)
                    filename = f"shell_{dataset}_n{n}_seed{seed}_gap-{gap}.gif"
                    save_gif(
                        initial,
                        events,
                        algo_dir / filename,
                        title=f"Shell Sort ({gap} gaps, {dataset}, n={n})",
                        fps=fps,
                    )
        else:
            for dataset in datasets:
                initial, events = collect_events(
                    algo=algo, n=n, dataset=dataset, seed=seed
                )
                events = downsample(events, max_frames=max_frames)
                filename = f"{algo}_{dataset}_n{n}_seed{seed}.gif"
                save_gif(
                    initial,
                    events,
                    algo_dir / filename,
                    title=f"{algo.title()} Sort ({dataset}, n={n})",
                    fps=fps,
                )

    # Highlight assets for quick reference in the README.
    bubble_initial, bubble_events = collect_events(
        algo="bubble", n=n, dataset="random", seed=seed
    )
    bubble_events = downsample(bubble_events, max_frames=max_frames)
    save_gif(
        bubble_initial,
        bubble_events,
        highlights_dir / "bubble_random_n50.gif",
        title="Bubble Sort (random, n=50)",
        fps=fps,
    )

    shell_initial, shell_events = collect_events(
        algo="shell", n=60, dataset="random", seed=seed, gap_variant="knuth"
    )
    shell_events = downsample(shell_events, max_frames=max_frames)
    save_snapshot(
        shell_initial,
        shell_events,
        highlights_dir / "shell_knuth_snapshot.png",
        title="Shell Sort (Knuth gaps, random, n=60)",
        steps=200,
    )
