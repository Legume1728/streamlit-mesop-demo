import os
from matplotlib import pyplot as plt
import mesop as me
import seaborn as sns
from mesop_common import sidebar, sidebar_link
from utils import project_root, run_benchmark, read_benchmark_results, agg_benchmark_results
import polars as pl
from mesop_compare import compare_page


@me.stateclass
class State:
    selected_benchmark = ''


def load(e: me.LoadEvent):
    me.set_theme_mode("system")


@me.page(path='/', on_load=load)
def main():
    with me.box(style=me.Style(
            display='flex',
            flex_direction='row',
    )):
        sidebar()

        with me.box():
            main_content()


def main_content():
    benchmarks = sorted([
        os.path.splitext(filename)[0] for filename in os.listdir(
            os.path.join(project_root, 'benchmarks_code'))
        if filename not in ('__pycache__', '.ipynb_checkpoints')
    ])

    me.text('Mesop Benchmark Demo',
            style=me.Style(font_size=20,
                           margin=me.Margin(top=20, bottom=20),
                           font_weight='bold'))

    with me.box(style=me.Style(
            display='flex',
            flex_direction='row',
    )):
        me.select(label='Benchmarks:',
                  options=[
                      me.SelectOption(label=benchmark, value=benchmark)
                      for benchmark in benchmarks
                  ],
                  multiple=False,
                  on_selection_change=on_selection_change)
        with me.box(style=me.Style(
                padding=me.Padding.symmetric(vertical=10, horizontal=10))):
            me.button('Run Benchmark',
                      color='primary',
                      type='raised',
                      on_click=handle_run_benchmark_event,
                      disabled=not me.state(State).selected_benchmark)

    benchmark = me.state(State).selected_benchmark
    if not benchmark:
        me.text('No benchmark selected')
        return

    try:
        meta, df, agg_df = read_and_agg_benchmark_results(benchmark)
    except:
        me.text('No benchmark results available')
        return
    me.text(
        f"Description: {meta['description']} ({meta['num_operations']} ops per trial)"
    )
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    plot = sns.kdeplot(x='elapsed_ms', data=df, ax=axes[0])
    plot.set_title('Kernel Density Estimation')

    plot = sns.lineplot(x='trial',
                        y='elapsed_ms',
                        data=df.with_row_index().with_columns(
                            pl.col('index').alias('trial')),
                        ax=axes[1])
    plot.set_title(f'{benchmark} - Elapsed')
    me.plot(fig)

    me.table(agg_df.to_pandas())


def read_and_agg_benchmark_results(benchmark):
    meta, df = read_benchmark_results(benchmark)
    return meta, df, agg_benchmark_results(meta, df)


def on_selection_change(event: me.SelectSelectionChangeEvent):
    s = me.state(State)
    s.selected_benchmark = event.value


def handle_run_benchmark_event(event: me.ClickEvent):
    s = me.state(State)
    run_benchmark(s.selected_benchmark)
