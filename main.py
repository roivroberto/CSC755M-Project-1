from __future__ import annotations

import argparse
from typing import List

import benchmark
from datasets import available_datasets, generate
from instrumentation import Instrumentation
from sorts import ALGORITHMS
from sorts.gaps import available_variants
from visualizer import visualize


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sorting algorithms visualization and benchmarking")
    subparsers = parser.add_subparsers(dest="command", required=True)

    viz = subparsers.add_parser("viz", help="Visualize a sorting algorithm")
    viz.add_argument("--algo", choices=sorted(ALGORITHMS.keys()), required=True)
    viz.add_argument("--n", type=int, default=50)
    viz.add_argument("--seed", type=int, default=0)
    viz.add_argument("--dataset", choices=available_datasets(), default="random")
    viz.add_argument("--gap", choices=available_variants(), default="shell")
    viz.add_argument("--speed", type=float, default=1.0)

    bench = subparsers.add_parser("bench", help="Run algorithm benchmarks")
    bench.add_argument(
        "--algo",
        choices=sorted(list(ALGORITHMS.keys()) + ["all"]),
        default="all",
    )
    bench.add_argument("--sizes", nargs="+", type=int, default=None)
    bench.add_argument("--datasets", nargs="+", choices=available_datasets(), default=None)
    bench.add_argument("--trials", type=int, default=5)
    bench.add_argument("--seed", type=int, default=0)
    bench.add_argument("--gaps", nargs="+", choices=available_variants(), default=None)
    bench.add_argument("--out", required=True)

    return parser.parse_args()


def _run_viz(args: argparse.Namespace) -> None:
    data = generate(args.dataset, args.n, args.seed)
    initial = list(data)
    events = []
    inst = Instrumentation(event_sink=events.append)
    sort_fn = ALGORITHMS[args.algo]
    sort_fn(data, inst, gap_variant=args.gap)

    title = f"{args.algo.title()} Sort ({args.dataset}, n={args.n})"
    if args.algo == "shell":
        title += f" - {args.gap} gaps"
    visualize(initial, events, speed=args.speed, title=title)


def _run_bench(args: argparse.Namespace) -> None:
    algorithms: List[str]
    if args.algo == "all":
        algorithms = list(sorted(ALGORITHMS.keys()))
    else:
        algorithms = [args.algo]

    sizes = args.sizes if args.sizes is not None else benchmark.default_sizes()
    datasets = args.datasets if args.datasets is not None else benchmark.default_datasets()

    results = benchmark.run_benchmarks(
        algorithms=algorithms,
        sizes=sizes,
        datasets=datasets,
        trials=args.trials,
        base_seed=args.seed,
        gap_variants=args.gaps,
    )
    benchmark.write_results(args.out, results)
    print(f"Wrote {len(results)} rows to {args.out}")


def main() -> None:
    args = _parse_args()
    if args.command == "viz":
        _run_viz(args)
    elif args.command == "bench":
        _run_bench(args)


if __name__ == "__main__":
    main()
