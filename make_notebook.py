"""Builds and executes project_notebook.ipynb."""
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

nb = nbf.v4.new_notebook()
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
nb.cells = [
    md("# Algorithm Performance Measurement and Benchmarking\n"
       "Runs the same engine used by `app.py` and shows tables, graphs and analysis."),
    code("import benchmark_engine as be\nimport matplotlib.pyplot as plt\n"
         "%matplotlib inline\nresults = be.run_all()"),
    md("## 1. Search algorithms (Linear vs Binary)"),
    code("results['Search'].round(4)"),
    code("be.plot_comparison(results['Search'], *be.CHARTS['Search']); plt.show()\n"
         "print('\\n'.join(be.summarize(results['Search'])))"),
    md("## 2. Factorial (Recursive vs Iterative)"),
    code("results['Factorial'].round(4)"),
    code("be.plot_comparison(results['Factorial'], *be.CHARTS['Factorial']); plt.show()\n"
         "print('\\n'.join(be.summarize(results['Factorial'])))"),
    md("## 3. Loops (Single vs Nested)"),
    code("results['Loops'].round(4)"),
    code("be.plot_comparison(results['Loops'], *be.CHARTS['Loops']); plt.show()\n"
         "print('\\n'.join(be.summarize(results['Loops'])))"),
    md("## 4. Complexity: theory vs observed"),
    code("be.complexity_table(results)"),
    md("## 5. Conclusions\n"
       "- Binary search stays almost flat (O(log n)) while linear search grows linearly.\n"
       "- Iterative factorial uses far less memory than recursive (no call stack); "
       "both grow faster than linear because big-integer multiplication gets costlier.\n"
       "- Nested loop grows quadratically; a single loop grows linearly.\n"
       "- Time-space trade-off: binary search needs sorted data (sorting cost up front), "
       "recursion trades memory for simpler code."),
]
ExecutePreprocessor(timeout=600, kernel_name="python3").preprocess(nb, {"metadata": {"path": "."}})
nbf.write(nb, "project_notebook.ipynb")
