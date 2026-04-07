from __future__ import annotations

import argparse
import cProfile
import io
import pstats
from pathlib import Path

from sequential import run_sequential


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile the sequential baseline")
    parser.add_argument("--corpus", default="books")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--sort", default="cumulative")
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--output", default=None, help="Optional output file for profiling results")
    args = parser.parse_args()

    profiler = cProfile.Profile()
    profiler.enable()
    run_sequential(args.corpus, limit=args.limit)
    profiler.disable()

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats(args.sort).print_stats(args.top)
    output_text = stream.getvalue()
    print(output_text, end="")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text, encoding="utf-8")


if __name__ == "__main__":
    main()
