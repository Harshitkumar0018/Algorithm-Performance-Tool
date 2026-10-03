"""Renders benchmark tables as PNG images for the report (screenshots/)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import search_analysis as sa
import code_benchmark as cb
import benchmark_engine as be


def table_image(df, title, path):
    fig, ax = plt.subplots(figsize=(min(2 + 1.7 * len(df.columns), 14), 0.6 + 0.4 * len(df)))
    ax.axis("off")
    ax.set_title(title, fontsize=11, fontweight="bold")
    t = ax.table(cellText=df.values, colLabels=df.columns, loc="center", cellLoc="center")
    t.auto_set_font_size(False)
    t.set_fontsize(8)
    t.scale(1, 1.3)
    fig.tight_layout()
    fig.savefig(path, dpi=130)


# Search analysis output (Task 2)
data = sa.generate_dataset(10000)
key = data[5000]
rows = []
for name, f in sa.ALGORITHMS.items():
    res, t, mem = be.measure(f, data, key)
    rows.append([name, f"Found at index {res[0]}", res[1], round(t * 1000, 5), round(mem, 2)])
table_image(pd.DataFrame(rows, columns=["Algorithm", "Result", "Comparisons", "Time (ms)", "Memory (KB)"]),
            f"Search Analysis output (n=10000, key={key})", "screenshots/search_output.png")

# Code benchmark output (Task 3)
rows = []
for name, f in cb.SNIPPETS.items():
    res, t, mem = be.measure(f, 1000, repeats=3)
    rows.append([name, round(t * 1000, 5), round(mem, 2), res[1]])
table_image(pd.DataFrame(rows, columns=["Snippet", "Time (ms)", "Memory (KB)", "Operations"]),
            "Code Benchmark comparison table (input size 1000)", "screenshots/code_output.png")

# Complexity table (Task 6)
table_image(pd.read_csv("reports/complexity_table.csv"),
            "Complexity analysis: theoretical vs observed", "screenshots/complexity_table.png")
