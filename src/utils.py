"""Shared utilities for text preprocessing and word-count merging."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
from typing import Iterable

# Regular expression to match words, including apostrophes, and ignore punctuation
WORD_RE = re.compile(r"\b[\w']+\b", re.UNICODE)
START_MARKERS = (
    "*** START OF THE PROJECT GUTENBERG EBOOK",
    "*** START OF THIS PROJECT GUTENBERG EBOOK",
)
END_MARKERS = (
    "*** END OF THE PROJECT GUTENBERG EBOOK",
    "*** END OF THIS PROJECT GUTENBERG EBOOK",
)

# List all text files in the corpus directory, optionally limiting the number of files returned
def list_books(corpus_dir: str | Path, limit: int | None = None) -> list[Path]:
    files = sorted(
        path
        for path in Path(corpus_dir).iterdir()
        if path.is_file() and not path.name.startswith(".")
    )
    if limit is not None:
        return files[:limit]
    return files


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

 # Strip the Project Gutenberg boilerplate from the text
def strip_gutenberg_boilerplate(text: str) -> str:
    for marker in START_MARKERS:
        start = text.find(marker)
        if start != -1:
            next_newline = text.find("\n", start)
            if next_newline != -1:
                text = text[next_newline + 1 :]
            break

    for marker in END_MARKERS:
        end = text.find(marker)
        if end != -1:
            text = text[:end]
            break

    return text.lstrip("\ufeff").strip()

# Tokenize the text into words, converting to lowercase and ignoring punctuation
def tokenize(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())

# Count the frequency of each word in the text
def count_text(text: str) -> Counter[str]:
    return Counter(tokenize(text))

# Count the frequency of each word in the file
def count_file(path: Path) -> Counter[str]:
    return count_text(strip_gutenberg_boilerplate(read_text(path)))

# Merge multiple word count dictionaries into a single dictionary with total counts
def merge_counts(counts: Iterable[Counter[str]]) -> Counter[str]:
    total: Counter[str] = Counter()
    for counter in counts:
        total.update(counter)
    return total
