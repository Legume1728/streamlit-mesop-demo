import importlib
import json
import os
import random
import string
import polars as pl

project_root = os.path.dirname(os.path.abspath(__file__))


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def run_benchmark(benchmark):
    module = importlib.import_module(f'benchmarks_code.{benchmark}')

    benchmark_obj = module.Benchmark()
    meta = module.meta

    elapsed = []
    benchmark_obj.setup()
    for i in range(100):
        elapsed.append(benchmark_obj.run_once())

    with open(f'{project_root}/benchmarks_results/{benchmark}.json', 'w') as f:
        json.dump({'elapsed': elapsed, **meta}, f, indent=2)


def read_benchmark_results(benchmark):
    with open(f'benchmarks_results/{benchmark}.json') as f:
        results = json.loads(f.read())
    df = pl.DataFrame({
        'elapsed': results['elapsed']
    }).with_columns((pl.col('elapsed') * 1000).alias('elapsed_ms'))
    del results['elapsed']
    return results, df


def agg_benchmark_results(meta, df):
    num_operations = meta['num_operations']
    return df.select(
        pl.col('elapsed_ms').median().alias('median (ms)'),
        pl.col('elapsed_ms').quantile(0.95).alias('q95 (ms)'),
    ).with_columns(
        pl.lit(num_operations).alias('num_ops'),
        (pl.col('median (ms)') / num_operations).alias('median_ms_per_op'),
        (pl.col('q95 (ms)') / num_operations).alias('q95_ms_per_op'),
    )
