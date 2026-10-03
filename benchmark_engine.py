"""Core engine: measures time/memory, runs automated benchmarks, builds charts."""
import sys
import time
import tracemalloc

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import code_benchmark as cb
import search_analysis as sa

sys.setrecursionlimit(5000)

SEARCH_SIZES = [100, 1000, 10000, 50000]
FACT_SIZES = [100, 500, 1000]
SINGLE_LOOP_SIZES = [100, 1000, 5000, 10000, 50000]
NESTED_LOOP_SIZES = [100, 500, 1000, 2000, 5000]  # n*n work, so kept smaller


def measure(func, *args, repeats=5):
    """Run func(*args). Returns (result, avg_time_seconds, peak_memory_kb)."""
    start = time.perf_counter()
    for _ in range(repeats):
        result = func(*args)
    avg_time = (time.perf_counter() - start) / repeats

    # memory is measured in a separate run because tracemalloc slows code down
    tracemalloc.start()
    func(*args)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return result, avg_time, peak / 1024


def _row(name, n, res, t, mem):
    return dict(Algorithm=name, Size=n, Time_ms=t * 1000,
                Memory_KB=mem, Operations=res[1])


def run_search_benchmarks():
    rows = []
    for n in SEARCH_SIZES:
        data = sa.generate_dataset(n)
        key = data[-1]  # worst case for linear search
        for name, func in sa.ALGORITHMS.items():
            res, t, mem = measure(func, data, key)
            rows.append(_row(name, n, res, t, mem))
    return pd.DataFrame(rows)


def run_factorial_benchmarks():
    rows = []
    for n in FACT_SIZES:
        for name, func in cb.FACTORIAL.items():
            res, t, mem = measure(func, n)
            rows.append(_row(name, n, res, t, mem))
    return pd.DataFrame(rows)


def run_loop_benchmarks():
    rows = []
    sizes = {"Single Loop": SINGLE_LOOP_SIZES, "Nested Loop": NESTED_LOOP_SIZES}
    for name, func in cb.LOOPS.items():
        for n in sizes[name]:
            res, t, mem = measure(func, n, repeats=3)
            rows.append(_row(name, n, res, t, mem))
    return pd.DataFrame(rows)


def run_all():
    """Automated benchmarking: returns dict of DataFrames per category."""
    return {"Search": run_search_benchmarks(),
            "Factorial": run_factorial_benchmarks(),
            "Loops": run_loop_benchmarks()}


CHARTS = {
    "Search": ("Search: Dataset Size vs Execution Time", "Dataset size"),
    "Factorial": ("Factorial: Input Size vs Execution Time", "n"),
    "Loops": ("Loops: Iterations vs Execution Time", "Iterations"),
}


def plot_comparison(df, title, xlabel, path=None):
    """Line chart of size vs time for each algorithm in df."""
    fig, ax = plt.subplots(figsize=(6, 4))
    for name, g in df.groupby("Algorithm", sort=False):
        ax.plot(g["Size"], g["Time_ms"], marker="o", label=name)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Execution time (ms)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=120)
    return fig


THEORY = {
    "Linear Search": "O(n)",
    "Binary Search": "O(log n)",
    "Recursive Factorial": "O(n)",
    "Iterative Factorial": "O(n)",
    "Single Loop": "O(n)",
    "Nested Loop": "O(n^2)",
}


def growth_slope(g):
    """Slope of log(time) vs log(size): ~0 constant/log, ~1 linear, ~2 quadratic."""
    if len(g) < 2:
        return float("nan")
    return float(np.polyfit(np.log(g["Size"]), np.log(g["Time_ms"]), 1)[0])


def describe_growth(slope):
    if slope < 0.4:
        return "Almost flat (constant / logarithmic)"
    if slope < 1.3:
        return "Roughly linear"
    if slope < 1.8:
        return "Between linear and quadratic"
    return "Roughly quadratic or worse"


def complexity_table(results):
    """Theoretical vs observed table using the largest size of each algorithm."""
    rows = []
    for df in results.values():
        for name, g in df.groupby("Algorithm", sort=False):
            g = g.sort_values("Size")
            last = g.iloc[-1]
            slope = growth_slope(g)
            rows.append({
                "Algorithm": name,
                "Theoretical": THEORY[name],
                "Largest Size": int(last["Size"]),
                "Time (ms)": round(last["Time_ms"], 4),
                "Memory (KB)": round(last["Memory_KB"], 2),
                "Log-log slope": round(slope, 2),
                "Observed growth": describe_growth(slope),
            })
    return pd.DataFrame(rows)


def summarize(df):
    """Plain-text trend summary for one category."""
    lines = []
    for name, g in df.groupby("Algorithm", sort=False):
        g = g.sort_values("Size")
        lines.append(f"{name}: {g['Time_ms'].iloc[0]:.4f} ms at n={g['Size'].iloc[0]} -> "
                     f"{g['Time_ms'].iloc[-1]:.4f} ms at n={g['Size'].iloc[-1]} "
                     f"({describe_growth(growth_slope(g)).lower()}).")
    # compare all algorithms at the largest size they have in common
    common = df.groupby("Algorithm")["Size"].max().min()
    at = df[df["Size"] == common]
    best = at.loc[at["Time_ms"].idxmin()]
    lines.append(f"Fastest at n={common}: {best['Algorithm']}.")
    return lines
