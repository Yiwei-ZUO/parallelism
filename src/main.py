"""Run one implementation and display timing and top-word results."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from benchmark import benchmark, summarize_timings
from parallel_processes import run_processes
from parallel_threads import run_threads
from sequential import run_sequential


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Word counting lab skeleton")
    parser.add_argument("--corpus", default="books", help="Directory containing text files")
    parser.add_argument("--limit", type=int, default=None, help="Only use the first N files")
    parser.add_argument("--repeats", type=int, default=3, help="Benchmark repetitions")
    parser.add_argument("--workers", type=int, default=4, help="Parallel worker count")
    parser.add_argument(
        "--mode",
        choices=["sequential", "threads", "processes", "all"],
        default="all",
        help="Implementation to run",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=20,
        help="Number of most frequent words to display",
    )
    return parser.parse_args()


def print_summary(label: str, timings: list[float]) -> None:
    summary = summarize_timings(timings)
    print(
        f"{label}: min={summary['min']:.4f}s "
        f"mean={summary['mean']:.4f}s max={summary['max']:.4f}s"
    )


def print_top_words(counts: Counter[str], top_n: int) -> None:
    print(f"top {top_n} words:")
    for word, count in counts.most_common(top_n):
        print(f"{word}: {count}")


def main() -> None:
    args = parse_args()
    corpus_dir = Path(args.corpus)

    if not corpus_dir.exists():
        raise SystemExit(f"Corpus directory not found: {corpus_dir}")

    sequential_result = None

    if args.mode in {"sequential", "all"}:
        sequential_result, timings = benchmark(
            run_sequential,
            corpus_dir,
            limit=args.limit,
            repeats=args.repeats,
        )
        print_summary("sequential", timings)
        print_top_words(sequential_result, args.top_n)

    if args.mode in {"threads", "all"}:
        thread_result, timings = benchmark(
            run_threads,
            corpus_dir,
            limit=args.limit,
            workers=args.workers,
            repeats=args.repeats,
        )
        print_summary("threads", timings)
        if sequential_result is not None:
            print(f"threads matches sequential: {thread_result == sequential_result}")
        if args.mode == "threads":
            print_top_words(thread_result, args.top_n)

    if args.mode in {"processes", "all"}:
        process_result, timings = benchmark(
            run_processes,
            corpus_dir,
            limit=args.limit,
            workers=args.workers,
            repeats=args.repeats,
        )
        print_summary("processes", timings)
        if sequential_result is not None:
            print(f"processes matches sequential: {process_result == sequential_result}")
        if args.mode == "processes":
            print_top_words(process_result, args.top_n)


if __name__ == "__main__":
    main()
