#!/usr/bin/env python

import subprocess
import time
from utils import project_root

# read 1 MB of random data from a file

meta = {
    'description': 'fork 10k subprocesses',
    'num_operations': 200,
}


class Benchmark(object):

    def setup(self):
        pass

    def run_once(self) -> float:
        ''' Read the contents of the file, return the elapsed time '''
        num_ops = meta['num_operations']
        t0 = time.time()
        for _ in range(num_ops):
            subprocess.call(['echo', ''])
        return time.time() - t0
