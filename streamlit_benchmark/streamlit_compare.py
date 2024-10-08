import os
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils import project_root, run_benchmark, read_benchmark_results, agg_benchmark_results

benchmarks = sorted([
    os.path.splitext(filename)[0]
    for filename in os.listdir(os.path.join(project_root, 'benchmarks_code'))
    if filename not in ('__pycache__', '.ipynb_checkpoints')
])


def main():
    st.set_page_config('Streamlit Benchmark Demo', layout='wide')
    st.title('Compare Two Benchmarks')
    columns = st.columns(2)
    with columns[0]:
        st.write('Left Benchmark')
        show_one('left')

    with columns[1]:
        st.write('Right Benchmark')
        show_one('right')


@st.fragment
def show_one(key):
    columns = st.columns([2, 1])
    with columns[0]:
        benchmark = st.selectbox('Benchmark',
                                 benchmarks,
                                 label_visibility='collapsed',
                                 key=f'benchmark_selector_{key}')

    with columns[1]:
        if st.button('Run Benchmark', key=f'run_benchmark_btn_{key}'):
            # read_and_agg_benchmark_results.clear()
            run_benchmark(benchmark)

    try:
        meta, df, agg_df = read_and_agg_benchmark_results(benchmark)
    except:
        st.warning('No benchmark results available')
        return
    st.write('Description:', meta['description'],
             f"({meta['num_operations']} ops per trial)")
    fig = plt.figure()
    plot = sns.kdeplot(x='elapsed_ms', data=df)
    plot.set_title(f'{benchmark} - Kernel Density Estimation')
    st.pyplot(fig)
    st.write(agg_df)


# @st.cache_data
def read_and_agg_benchmark_results(benchmark):
    meta, df = read_benchmark_results(benchmark)
    return meta, df, agg_benchmark_results(meta, df)


main()
