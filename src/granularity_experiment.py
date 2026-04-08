"""Benchmark different process-task chunk sizes for the word-counting experiment."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from benchmark import benchmark, summarize_timings
from sequential import run_sequential
from utils import count_file, list_books, merge_counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare different chunk sizes for the process-based implementation"
    )
    parser.add_argument("--corpus", default="books")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument(
        "--chunk-sizes",
        type=int,
        nargs="+",
        default=[1, 2, 5, 10, 25],
        help="Number of files grouped into one process task",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional base output path; writes both .txt and .md versions",
    )
    return parser.parse_args()


def chunk_paths(paths: list[Path], chunk_size: int) -> list[list[str]]:
    as_strings = [str(path) for path in paths]
    return [as_strings[index : index + chunk_size] for index in range(0, len(as_strings), chunk_size)]


def _count_chunk_worker(path_strings: list[str]) -> Counter[str]:
    return merge_counts(count_file(Path(path_str)) for path_str in path_strings)


def run_processes_chunked(
    corpus_dir: str | Path,
    limit: int | None = None,
    workers: int = 4,
    chunk_size: int = 1,
) -> Counter[str]:
    files = list_books(corpus_dir, limit=limit)
    chunks = chunk_paths(files, chunk_size)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        partial_counts = list(executor.map(_count_chunk_worker, chunks))
    return merge_counts(partial_counts)


def format_timings(timings: list[float] | str) -> str:
    if isinstance(timings, str):
        return timings
    return " / ".join(f"{value:.4f}" for value in timings)


def format_text_header() -> str:
    return (
        f"{'Chunk':>5}  {'Tasks':>5}  {'Runs (s)':<30}  "
        f"{'Mean (s)':>8}  {'Min (s)':>8}  {'Max (s)':>8}  {'Matches':>8}"
    )


def format_text_row(
    chunk_size: int,
    tasks: int,
    timings: list[float] | str,
    mean_value: float | str,
    min_value: float | str,
    max_value: float | str,
    matches_baseline: str,
) -> str:
    runs = format_timings(timings)
    mean_display = f"{mean_value:>8.4f}" if isinstance(mean_value, float) else f"{mean_value:>8}"
    min_display = f"{min_value:>8.4f}" if isinstance(min_value, float) else f"{min_value:>8}"
    max_display = f"{max_value:>8.4f}" if isinstance(max_value, float) else f"{max_value:>8}"
    return (
        f"{chunk_size:>5}  {tasks:>5}  {runs:<30}  "
        f"{mean_display}  {min_display}  {max_display}  {matches_baseline:>8}"
    )


def main() -> None:
    args = parse_args()
    corpus_dir = Path(args.corpus)
    if not corpus_dir.exists():
        raise SystemExit(f"Corpus directory not found: {corpus_dir}")

    baseline = run_sequential(corpus_dir, limit=args.limit)
    files = list_books(corpus_dir, limit=args.limit)

    text_lines: list[str] = []
    markdown_lines: list[str] = []

    header = format_text_header()
    separator = "-" * 86
    print(header)
    print(separator)
    text_lines.extend([header, separator])
    markdown_lines.append(
        "| Chunk Size | Number of Tasks | Runs (s) | Mean (s) | Min (s) | Max (s) | Matches Baseline |"
    )
    markdown_lines.append("| ---: | ---: | --- | ---: | ---: | ---: | ---: |")

    for chunk_size in args.chunk_sizes:
        if chunk_size <= 0:
            error_row = format_text_row(chunk_size, 0, "ERROR", "-", "-", "-", "ERROR")
            print(error_row)
            text_lines.append(error_row)
            markdown_lines.append(f"| {chunk_size} | 0 | ERROR | - | - | - | ERROR |")
            continue

        tasks = len(chunk_paths(files, chunk_size))

        try:
            result, timings = benchmark(
                run_processes_chunked,
                corpus_dir,
                limit=args.limit,
                workers=args.workers,
                chunk_size=chunk_size,
                repeats=args.repeats,
            )
        except Exception as exc:
            error_row = format_text_row(chunk_size, tasks, "ERROR", "-", "-", "-", "ERROR")
            print(error_row)
            text_lines.append(error_row)
            markdown_lines.append(f"| {chunk_size} | {tasks} | ERROR | - | - | - | ERROR |")
            markdown_lines.append(f"error for chunk size {chunk_size}: {exc}")
            continue

        summary = summarize_timings(timings)
        matches_baseline = "True" if result == baseline else "False"
        row = format_text_row(
            chunk_size,
            tasks,
            timings,
            summary["mean"],
            summary["min"],
            summary["max"],
            matches_baseline,
        )
        print(row)
        text_lines.append(row)
        markdown_lines.append(
            f"| {chunk_size} | {tasks} | {format_timings(timings)} | "
            f"{summary['mean']:.4f} | {summary['min']:.4f} | {summary['max']:.4f} | {matches_baseline} |"
        )

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        stem_path = output_path.with_suffix("")
        text_path = stem_path.with_suffix(".txt")
        markdown_path = stem_path.with_suffix(".md")
        text_path.write_text("\n".join(text_lines) + "\n", encoding="utf-8")
        markdown_path.write_text("\n".join(markdown_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
