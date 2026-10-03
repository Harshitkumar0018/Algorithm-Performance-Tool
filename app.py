"""Streamlit app: streamlit run app.py"""
import pandas as pd
import streamlit as st

import benchmark_engine as be
import code_benchmark as cb
import search_analysis as sa

st.set_page_config(page_title="Algorithm Performance Tool", layout="wide")
st.title("Algorithm Performance Measurement and Benchmarking Tool")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Run Single", "Search Analysis", "Code Benchmark", "Automated Benchmark"])

with tab1:
    st.subheader("Run any algorithm or snippet")
    options = {**sa.ALGORITHMS, **cb.SNIPPETS}
    name = st.selectbox("Algorithm / snippet", list(options))
    n = st.number_input("Input size", 1, 3000, 1000, key="single_n")
    if st.button("Execute", key="single_run"):
        if name in sa.ALGORITHMS:
            data = sa.generate_dataset(int(n))
            args = (data, data[-1])
        else:
            args = (int(n),)
        res, t, mem = be.measure(options[name], *args)
        c1, c2, c3 = st.columns(3)
        c1.metric("Time (ms)", f"{t * 1000:.4f}")
        c2.metric("Peak memory (KB)", f"{mem:.2f}")
        c3.metric("Operations", res[1])
    st.caption("Max 3000 to keep nested loop and recursion fast.")

with tab2:
    st.subheader("Linear vs Binary Search")
    size = st.number_input("Dataset size", 1, 1000000, 10000, key="search_n")
    data = sa.generate_dataset(int(size))
    key = st.number_input("Search key", value=int(data[len(data) // 2]))
    st.caption(f"Dataset: sorted, {len(data)} unique integers "
               f"(min {data[0]}, max {data[-1]})")
    if st.button("Search", key="search_run"):
        rows = []
        for name, func in sa.ALGORITHMS.items():
            res, t, mem = be.measure(func, data, int(key))
            rows.append({"Algorithm": name,
                         "Result": f"Found at index {res[0]}" if res[0] >= 0 else "Not found",
                         "Comparisons": res[1], "Time (ms)": round(t * 1000, 5),
                         "Memory (KB)": round(mem, 2)})
        st.table(pd.DataFrame(rows))

with tab3:
    st.subheader("Compare code snippets")
    chosen = st.multiselect("Snippets", list(cb.SNIPPETS),
                            default=["Single Loop", "Nested Loop"])
    n = st.number_input("Input size", 1, 3000, 1000, key="code_n")
    if st.button("Run selected", key="code_run") and chosen:
        rows = []
        for name in chosen:
            res, t, mem = be.measure(cb.SNIPPETS[name], int(n), repeats=3)
            rows.append({"Snippet": name, "Time (ms)": round(t * 1000, 5),
                         "Memory (KB)": round(mem, 2), "Operations": res[1]})
        df = pd.DataFrame(rows)
        st.table(df)
        st.bar_chart(df.set_index("Snippet")["Time (ms)"])

with tab4:
    st.subheader("Automated benchmark over varying input sizes")
    if st.button("Run full benchmark", key="auto_run"):
        with st.spinner("Running (nested loop takes a few seconds)..."):
            st.session_state["results"] = be.run_all()
    results = st.session_state.get("results")
    if results:
        for cat, df in results.items():
            st.markdown(f"### {cat}")
            left, right = st.columns(2)
            left.dataframe(df.round(4), width="stretch")
            right.pyplot(be.plot_comparison(df, *be.CHARTS[cat]))
            for line in be.summarize(df):
                st.write("- " + line)
        st.markdown("### Complexity analysis: theory vs observed")
        st.dataframe(be.complexity_table(results), width="stretch")
