import os
import streamlit as st
import polars as pl
from matplotlib import pyplot as plt
from utils import project_root, run_benchmark, read_benchmark_results, agg_benchmark_results
import seaborn as sns


def main():
    st.set_page_config('Streamlit Benchmark Demo', layout='centered')
    st.title("Streamlit Benchmark Demo")

    benchmarks = sorted([
        os.path.splitext(filename)[0] for filename in os.listdir(
            os.path.join(project_root, 'benchmarks_code'))
        if filename not in ('__pycache__', '.ipynb_checkpoints')
    ])
    st.write('Benchmarks:')
    columns = st.columns([2, 1])
    with columns[0]:
        benchmark = st.selectbox('Benchmark',
                                 benchmarks,
                                 label_visibility='collapsed')

    with columns[1]:
        if st.button('Run Benchmark'):
            # read_and_agg_benchmark_results.clear()
            run_benchmark(benchmark)

    try:
        meta, df, agg_df = read_and_agg_benchmark_results(benchmark)
    except:
        st.warning('No benchmark results available')
        return
    st.write('Description:', meta['description'],
             f"({meta['num_operations']} ops per trial)")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    plot = sns.kdeplot(x='elapsed_ms', data=df, ax=axes[0])
    plot.set_title('Kernel Density Estimation')

    plot = sns.lineplot(x='trial',
                        y='elapsed_ms',
                        data=df.with_row_index().with_columns(
                            pl.col('index').alias('trial')),
                        ax=axes[1])
    plot.set_title(f'{benchmark} - Elapsed')
    st.pyplot(fig)
    st.write(agg_df)


# @st.cache_data
def read_and_agg_benchmark_results(benchmark):
    meta, df = read_benchmark_results(benchmark)
    return meta, df, agg_benchmark_results(meta, df)


main()
