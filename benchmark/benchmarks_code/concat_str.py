#!/usr/bin/env python

import random
import string
import time
import tempfile

# read 1 MB of random data from a file

meta = {
    'description': 'Concatenates a few strings',
    'num_operations': 100_000,
}


class Benchmark(object):
    def setup(self):
        pass

    def run_once(self) -> float:
        ''' Perform 100K dictionary reads, return the elapsed time '''

        t0 = time.time()
        b = ''
        for i in range(meta['num_operations']):
            b += 'hello'
        return time.time() - t0
        
            