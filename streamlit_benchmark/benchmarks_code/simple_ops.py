#!/usr/bin/env python

import time

# do 100K simple operations

meta = {
    'description': 'Perform 100K simple operations',
    'num_operations': 100_000,
}

class Benchmark(object):
    def setup(self):
        pass
    
    def run_once(self) -> float:
        ''' Do 100K simple operations, return the elapsed time '''
        num_operations = meta['num_operations']
        
        a = 1
        t0 = time.time()
        for i in range(num_operations):
            a += i
        return time.time() - t0