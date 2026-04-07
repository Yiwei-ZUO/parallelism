"""Generate runtime comparison tables and optional profiling output."""

from __future__ import annotations

import argparse
import cProfile
import io
from pathlib import Path
import pstats

from benchmark import benchmark, summarize_timings
from parallel_processes import run_processes
from parallel_threads import run_threads
from sequential import run_sequential


IMPLEMENTATIONS = {
    "sequential": run_sequential,
    "threads": run_threads,
    "processes": run_processes,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate benchmark tables for the lab")
    parser.add_argument("--corpus", default="books")
    parser.add_argument(
        "--limits",
        type=int,
        nargs="+",
        default=[10],
        help="Corpus sizes to benchmark, e.g. --limits 10 20 30",
    )
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument(
        "--implementations",
        nargs="+",
        choices=["sequential", "threads", "processes"],
        default=["sequential", "threads", "processes"],
        help="Implementations to include in the table",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional base output path; writes both .txt and .md versions",
    )
    parser.add_argument(
        "--include-profile",
        action="store_true",
        help="Append profiling results for the sequential version",
    )
    parser.add_argument(
        "--profile-limit",
        type=int,
        default=None,
        help="Corpus size to use for profiling; defaults to the largest limit",
    )
    parser.add_argument(
        "--profile-top",
        type=int,
        default=15,
        help="Number of profiling entries to display",
    )
    return parser.parse_args()


def format_timings(timings: list[float] | str) -> str:
    if isinstance(timings, str):
        return timings
    return " / ".join(f"{value:.4f}" for value in timings)


def build_profile_output(corpus_dir: Path, limit: int | None, top: int) -> str:
    profiler = cProfile.Profile()
    profiler.enable()
    run_sequential(corpus_dir, limit=limit)
    profiler.disable()

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative").print_stats(top)
    return stream.getvalue().rstrip()


def append_markdown(lines: list[str], message: str) -> None:
    lines.append(message)


def append_text(lines: list[str], message: str) -> None:
    lines.append(message)


def print_console_header() -> None:
    print(format_text_header())
    print("-" * 100)


def format_text_header() -> str:
    return (
        f"{'Files':>5}  {'Version':<10}  {'Runs (s)':<40}  "
        f"{'Mean (s)':>8}  {'Min (s)':>8}  {'Max (s)':>8}  {'Matches':>8}"
    )


def print_console_row(
    limit: int,
    name: str,
    timings: list[float],
    mean_value: float,
    min_value: float,
    max_value: float,
    matches_baseline: str,
) -> None:
    print(format_text_row(limit, name, timings, mean_value, min_value, max_value, matches_baseline))


def format_text_row(
    limit: int,
    name: str,
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
        f"{limit:>5}  {name:<10}  {runs:<40}  "
        f"{mean_display}  {min_display}  {max_display}  {matches_baseline:>8}"
    )


def main() -> None:
    args = parse_args()
    corpus_dir = Path(args.corpus)
    output_lines: list[str] = []
    text_lines: list[str] = []

    if not corpus_dir.exists():
        raise SystemExit(f"Corpus directory not found: {corpus_dir}")

    print_console_header()
    append_text(text_lines, format_text_header())
    append_text(text_lines, "-" * 100)
    append_markdown(
        output_lines,
        "| Files | Version | Runs (s) | Mean (s) | Min (s) | Max (s) | Matches Baseline |",
    )
    append_markdown(output_lines, "| --- | --- | --- | ---: | ---: | ---: | ---: |")

    for limit in args.limits:
        baseline_result = None

        for name in args.implementations:
            fn = IMPLEMENTATIONS[name]
            kwargs = {"limit": limit}
            if name != "sequential":
                kwargs["workers"] = args.workers

            try:
                result, timings = benchmark(
                    fn,
                    corpus_dir,
                    repeats=args.repeats,
                    **kwargs,
                )
            except Exception as exc:
                error_row = format_text_row(limit, name, "ERROR", "-", "-", "-", "ERROR")
                print(error_row)
                append_text(text_lines, error_row)
                append_markdown(output_lines, f"| {limit} | {name} | ERROR | - | - | - | ERROR |")
                append_markdown(output_lines, f"error for {name} at limit={limit}: {exc}")
                continue
            summary = summarize_timings(timings)
            matches_baseline = "-"
            if name == "sequential":
                baseline_result = result
            elif baseline_result is not None:
                matches_baseline = "True" if result == baseline_result else "False"

            row = format_text_row(
                limit,
                name,
                timings,
                summary["mean"],
                summary["min"],
                summary["max"],
                matches_baseline,
                )
            print(row)
            append_text(text_lines, row)
            append_markdown(
                output_lines,
                f"| {limit} | {name} | {format_timings(timings)} | "
                f"{summary['mean']:.4f} | {summary['min']:.4f} | {summary['max']:.4f} | {matches_baseline} |",
            )

    if args.include_profile:
        profile_limit = args.profile_limit if args.profile_limit is not None else max(args.limits)
        profile_output = build_profile_output(corpus_dir, profile_limit, args.profile_top)

        print()
        print(f"Profiling results for sequential mode (limit={profile_limit})")
        print("-" * 100)
        print(profile_output)

        append_text(text_lines, "")
        append_text(text_lines, f"Profiling results for sequential mode (limit={profile_limit})")
        append_text(text_lines, "-" * 100)
        for line in profile_output.splitlines():
            append_text(text_lines, line)

        append_markdown(output_lines, "")
        append_markdown(output_lines, f"## Profiling Results (sequential, limit={profile_limit})")
        append_markdown(output_lines, "```text")
        for line in profile_output.splitlines():
            append_markdown(output_lines, line)
        append_markdown(output_lines, "```")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        stem_path = output_path.with_suffix("")
        text_path = stem_path.with_suffix(".txt")
        markdown_path = stem_path.with_suffix(".md")
        text_path.write_text("\n".join(text_lines) + "\n", encoding="utf-8")
        markdown_path.write_text("\n".join(output_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
