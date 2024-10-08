#!/usr/bin/env python

import random
import string
import time
import tempfile

# read 1 MB of random data from a file

meta = {
    'description': 'Read 1 MB of random data from a file',
    'num_operations': 1,
}

class Benchmark(object):
    def setup(self):
        to_write = ''.join(
            [random.choice(string.ascii_lowercase) for i in range(1_000_000)])
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            print(f"Temporary file created at: {temp_file.name}")
            # Write to the temp file or use it as needed
            temp_file.write(to_write)
        self.temp_file = temp_file
    
    def run_once(self) -> float:
        ''' Read the contents of the file, return the elapsed time '''
        t0 = time.time()
        with open(self.temp_file.name) as f:
            contents = f.read()
        return time.time() - t0