#!/usr/bin/env python

import random
import string
import time
import tempfile

# read 1 MB of random data from a file

meta = {
    'description': 'Perform 100K dictionary reads',
    'num_operations': 100_000,
}

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

class Benchmark(object):
    def setup(self):
        self.adict = {}
        self.keys = [generate_random_string() for _ in range(meta['num_operations'])]
        for key in self.keys:
            self.adict[key] = random.choice(string.ascii_lowercase)

    def run_once(self) -> float:
        ''' Perform 100K dictionary reads, return the elapsed time '''

        t0 = time.time()
        for key in self.keys:
            content = self.adict[key]
        return time.time() - t0
        
            