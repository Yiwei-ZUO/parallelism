"""Sequential baseline for the word-counting experiment."""

from __future__ import annotations
from collections import Counter
from pathlib import Path
from utils import count_file, list_books, merge_counts

# Run the sequential word counting
def run_sequential(corpus_dir: str | Path, limit: int | None = None) -> Counter[str]:
    partial_counts = [count_file(path) for path in list_books(corpus_dir, limit=limit)]
    return merge_counts(partial_counts)
