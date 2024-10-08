import os
from matplotlib import pyplot as plt
import mesop as me
import seaborn as sns
import polars as pl

from mesop_common import sidebar, SIDEBAR_WIDTH
from utils import agg_benchmark_results, project_root, read_benchmark_results, run_benchmark


@me.page(path='/compare')
def compare_page():
    viewport_width = me.viewport_size().width
    content_width = viewport_width - SIDEBAR_WIDTH
    with me.box(style=me.Style(
            display='flex',
            flex_direction='row',
    )):
        sidebar()

        with me.box(style=me.Style(
                height='100%',
                width=content_width,
        )):
            main_content(content_width)


def main_content(content_width):
    me.text('Compare page',
            style=me.Style(font_size=20,
                           margin=me.Margin(top=20, bottom=20),
                           font_weight='bold'))
    with me.box(style=me.Style(
            display='flex',
            flex_direction='row',
    )):
        benchmarks = sorted([
            os.path.splitext(filename)[0] for filename in os.listdir(
                os.path.join(project_root, 'benchmarks_code'))
            if filename not in ('__pycache__', '.ipynb_checkpoints')
        ])
        with me.box(style=me.Style(width=int(content_width) // 2)):
            show_one(benchmarks, 'left', content_width // 2)
        with me.box(style=me.Style(width=int(content_width) // 2)):
            show_one(benchmarks, 'right', content_width // 2)


def show_one(benchmarks, key, content_width):
    selected_benchmark_key = f'selected_benchmark_{key}'
    with me.box(style=me.Style(display='flex', flex_direction='row')):
        me.select(label='Benchmarks:',
                  options=[
                      me.SelectOption(label=benchmark, value=benchmark)
                      for benchmark in benchmarks
                  ],
                  key=f'select_benchmark_{key}',
                  multiple=False,
                  on_selection_change=on_selection_change)
        with me.box(style=me.Style(
                padding=me.Padding.symmetric(vertical=10, horizontal=10))):
            me.button(
                'Run Benchmark',
                color='primary',
                type='raised',
                key=f'run_benchmark_btn_{key}',
                on_click=handle_run_benchmark_event,
                disabled=not getattr(me.state(State), selected_benchmark_key))

    benchmark = getattr(me.state(State), selected_benchmark_key)
    try:
        meta, df, agg_df = read_and_agg_benchmark_results(benchmark)
    except:
        me.text('No benchmark results available')
        return
    me.text(
        f"Description: {meta['description']} ({meta['num_operations']} ops per trial)"
    )
    graph_width = content_width // 99
    print(f'{graph_width=}')
    fig = plt.figure(figsize=(graph_width, 5))
    # fig.set_figwidth(content_width * 0.8)
    plot = sns.kdeplot(x='elapsed_ms', data=df)
    plot.set_title('Kernel Density Estimation')
    me.plot(fig)

    with me.box(style=me.Style(
            width=content_width,
            overflow='scroll',
    )):
        me.table(agg_df.to_pandas())


@me.stateclass
class State:
    selected_benchmark_left = ''
    selected_benchmark_right = ''


def read_and_agg_benchmark_results(benchmark):
    meta, df = read_benchmark_results(benchmark)
    return meta, df, agg_benchmark_results(meta, df)


def on_selection_change(event: me.SelectSelectionChangeEvent):
    s = me.state(State)
    if event.key.endswith('_left'):
        s.selected_benchmark_left = event.value
    else:
        s.selected_benchmark_right = event.value


# note: using separate functions for right benchmark because closure variables in event handlers
# cannot be distinguished in Mesop:
# https://google.github.io/mesop/guides/event-handlers/#avoid-using-closure-variables-in-event-handler
def handle_run_benchmark_event(event: me.ClickEvent):
    s = me.state(State)
    if event.key.endswith('_left'):
        selected_benchmark = s.selected_benchmark_left
    else:
        selected_benchmark = s.selected_benchmark_right
    run_benchmark(selected_benchmark)
