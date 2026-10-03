"""Runs all benchmarks, saves CSV tables to reports/ and graphs to graphs/."""
import benchmark_engine as be

results = be.run_all()
for cat, df in results.items():
    df.round(4).to_csv(f"reports/{cat.lower()}_results.csv", index=False)
    be.plot_comparison(df, *be.CHARTS[cat], path=f"graphs/{cat.lower()}.png")
table = be.complexity_table(results)
table.to_csv("reports/complexity_table.csv", index=False)
for cat, df in results.items():
    print(cat)
    print(df.round(4).to_string(index=False))
    print("\n".join(be.summarize(df)), "\n")
print(table.to_string(index=False))
