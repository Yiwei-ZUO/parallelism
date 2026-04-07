# LAB4 Word Counting Project

This project contains a small Python codebase for the lab on profiling and parallel
word counting.

## Corpus

The corpus is stored in `books/` and currently contains 50 Project Gutenberg text
files.

## Project Structure

- `src/utils.py`: shared preprocessing helpers for file listing, text reading, cleaning,
  tokenisation, and merging partial counts.
- `src/sequential.py`: sequential baseline.
- `src/parallel_threads.py`: thread-based implementation.
- `src/parallel_processes.py`: process-based implementation.
- `src/main.py`: run one implementation and display timing plus top words.
- `src/benchmark.py`: timing utilities.
- `src/experiment_table.py`: generate runtime comparison tables and optionally append
  profiling results.
- `src/profile_run.py`: run profiling separately for the sequential version.

## Main Commands

Run a single implementation:

```bash
python3 src/main.py \
  --mode sequential \
  --limit 10 \
  --repeats 3
```

The value of `--mode` can be changed to `threads` or `processes`. The values of
`--limit`, `--workers`, and `--repeats` can also be adjusted depending on the
experiment.

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

This command runs the three implementations on three corpus sizes, repeats each
runtime experiment three times, appends profiling results for the sequential version on
the largest input size, and saves the outputs in both text and Markdown formats.

Optional separate profiling command:

```bash
python3 src/profile_run.py \
  --limit 50 \
  --top 15 \
  --output results/profile_limit50.txt
```

## Output Files

The full experiment command writes:

- `results/experiment_table.txt`: aligned plain-text runtime table with profiling output.
- `results/experiment_table.md`: Markdown version of the same results.

The optional profiling command writes:

- `results/profile_limit50.txt`: profiling output for the sequential version.

## Notes

- Project Gutenberg headers and footers are removed before tokenisation.
- Tokenisation is based on a regular expression and keeps letter-, digit-, and
  apostrophe-based tokens while ignoring punctuation as separate tokens.
- The code uses only the Python standard library.
