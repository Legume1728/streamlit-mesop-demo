#!/usr/bin/env python

import os
import random
import string
import tempfile
import time
import polars as pl


# write 1 MB of random data to a file

meta = {
    'description': 'Write 1 MB of random data from a file',
    'num_operations': 1,
}

class Benchmark(object):
    def setup(self):
        self.to_write = ''.join(
            [random.choice(string.ascii_lowercase) for i in range(1_000_000)])
    
    def run_once(self) -> float:
        ''' Write the contents of the file, return the elapsed time '''

        temp_context = tempfile.NamedTemporaryFile(delete=False, mode='w')
        t0 = time.time()
        with temp_context as f:
            # Write to the temp file or use it as needed
            f.write(self.to_write)
            f.flush()
            
        return time.time() - t0