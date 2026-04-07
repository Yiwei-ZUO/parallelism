"""Small benchmarking helpers for repeated runtime measurements."""

from __future__ import annotations

import statistics
import time
from typing import Any, Callable


def benchmark(
    fn: Callable[..., Any],
    *args: Any,
    repeats: int = 3,
    **kwargs: Any,
) -> tuple[Any, list[float]]:
    result: Any = None
    timings: list[float] = []

    for _ in range(repeats):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        end = time.perf_counter()
        timings.append(end - start)

    return result, timings


def summarize_timings(timings: list[float]) -> dict[str, float]:
    return {
        "min": min(timings),
        "mean": statistics.mean(timings),
        "max": max(timings),
    }
