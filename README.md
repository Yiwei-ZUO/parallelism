# Parallel Word Counting in Python

This project counts word frequencies in a corpus of text files and compares three
approaches: a sequential version, a thread-based version, and a process-based version.
Its purpose is to measure runtime, identify bottlenecks, and see when parallel execution
is actually beneficial. The project also includes a small task-granularity experiment to
examine how the size of the work units affects process-based performance.

## Corpus

The corpus is stored in `books/` and currently contains 50 plain-text Project Gutenberg
files.

## Structure

- `src/utils.py`: shared preprocessing utilities for file listing, text reading, cleaning,
  tokenisation, and merging partial counts.
- `src/sequential.py`: sequential baseline.
- `src/parallel_threads.py`: thread-based implementation.
- `src/parallel_processes.py`: process-based implementation.
- `src/main.py`: run one implementation and display timing plus top words.
- `src/benchmark.py`: timing utilities.
- `src/experiment_table.py`: generate runtime comparison tables and optional profiling
  output.
- `src/profile_run.py`: run profiling separately for the sequential version.
- `src/granularity_experiment.py`: compare different chunk sizes for the process-based
  implementation.

## Quick Start

Run a single implementation:

```bash
python3 src/main.py \
  --mode sequential \
  --limit 10 \
  --repeats 3
```

`--mode` can be changed to `threads` or `processes`. `--limit`, `--workers`, and
`--repeats` can also be adjusted depending on the experiment.

Run the full experiment:

```bash
python3 src/experiment_table.py \
  --limits 10 30 50 \
  --workers 4 \
  --repeats 3 \
  --implementations sequential threads processes \
  --include-profile \
  --profile-top 15 \
  --output results/experiment_table
```

This command compares all three implementations on three corpus sizes, repeats each
runtime measurement three times, appends profiling results for the sequential version on
the largest input size, and saves the outputs in both text and Markdown formats.

In the main implementation, each file is treated as one independent task.

Run the additional granularity experiment:

```bash
python3 src/granularity_experiment.py \
  --limit 50 \
  --workers 4 \
  --repeats 3 \
  --chunk-sizes 1 2 5 10 25 \
  --output results/granularity_experiment
```

This command tests the process-based version on 50 files with different chunk sizes,
where chunk size is measured in files per task.

Optional separate profiling command:

```bash
python3 src/profile_run.py \
  --limit 50 \
  --top 15 \
  --output results/profile_limit50.txt
```

## Outputs

The full experiment command writes:

- `results/experiment_table.txt`: aligned plain-text runtime table with profiling output
- `results/experiment_table.md`: Markdown version of the same results

The optional profiling command writes:

- `results/profile_limit50.txt`: profiling output for the sequential version

The granularity experiment writes:

- `results/granularity_experiment.txt`: aligned plain-text chunk-size comparison table
- `results/granularity_experiment.md`: Markdown version of the same results

## Granularity Result

In the supplementary granularity experiment on 50 files with 4 workers, the best result
was obtained with chunk size 5, with a mean runtime of 0.8353 s. Chunk sizes 1 and 2
were very close (0.8704 s and 0.8708 s), while larger chunk sizes were clearly slower:
1.0718 s for chunk size 10 and 1.3737 s for chunk size 25. This suggests that a medium
task size provides the best compromise between worker utilisation and management
overhead.

## Notes

- Project Gutenberg headers and footers are removed before tokenisation.
- Tokenisation is based on a regular expression and keeps letter-, digit-, and
  apostrophe-based tokens while ignoring punctuation as separate tokens.
- The project uses only the Python standard library.
