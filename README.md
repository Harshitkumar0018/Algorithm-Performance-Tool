# Algorithm Performance Measurement and Benchmarking Tool

A Streamlit app that runs algorithms and code snippets, measures execution time and peak memory,
benchmarks them over varying input sizes, plots the trends and compares theoretical vs observed complexity.

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
streamlit run app.py
```

## Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI (single run, search analysis, code benchmark, automated benchmark + charts + complexity table) |
| `search_analysis.py` | Dataset generator, Linear Search, Binary Search (with comparison counts) |
| `code_benchmark.py` | Single loop, nested loop, recursive and iterative factorial |
| `benchmark_engine.py` | Time/memory measurement, automated benchmarks, charts, complexity analysis |
| `project_notebook.ipynb` | Notebook with tables, graphs and conclusions |
| `generate_reports.py` | Saves CSV tables to `reports/` and graphs to `graphs/` |
| `make_report.py` | Builds `Final_Report.docx` |
| `check_app.py` | Headless smoke test of the app |
| `Final_Report.docx` | Final report |

## How measurement works
- **Time:** `time.perf_counter`, averaged over several runs.
- **Memory:** peak allocation via `tracemalloc` (measured in a separate run so it does not slow the timing).
- **Operations:** comparisons for searches, iterations/multiplications for the snippets.

## Input sizes
Search 100 / 1,000 / 10,000 / 50,000; factorial n = 100 / 500 / 1000; single loop 100 to 50,000.
The nested loop does n x n work, so it is tested at 100 to 5,000 iterations (25 million operations) only.

## Result summary
Binary search is far faster than linear search at large sizes; iterative factorial uses much less memory than
recursive; a single loop scales linearly while a nested loop scales quadratically. See `Final_Report.docx`.
