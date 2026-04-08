"""Process-based implementation of the word-counting experiment."""

from __future__ import annotations

from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from utils import count_file, list_books, merge_counts


def _count_file_worker(path_str: str) -> Counter[str]:
    return count_file(Path(path_str))


def run_processes(
    corpus_dir: str | Path,
    limit: int | None = None,
    workers: int = 4,
) -> Counter[str]:
    files = [str(path) for path in list_books(corpus_dir, limit=limit)]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        partial_counts = list(executor.map(_count_file_worker, files))
    return merge_counts(partial_counts)
