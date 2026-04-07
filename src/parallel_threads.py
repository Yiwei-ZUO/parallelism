"""Thread-based implementation of the word-counting experiment."""

from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from text_processing import count_file, list_books, merge_counts


def run_threads(
    corpus_dir: str | Path,
    limit: int | None = None,
    workers: int = 4,
) -> Counter[str]:
    files = list_books(corpus_dir, limit=limit)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        partial_counts = list(executor.map(count_file, files))
    return merge_counts(partial_counts)
