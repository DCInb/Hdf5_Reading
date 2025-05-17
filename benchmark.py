import time
import h5py
import numpy as np
import pandas as pd
from multiprocessing import Pool
import psutil
import os

def measure_memory():
    """Return current process memory usage in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def basic_read(filename, dataset_name):
    """Basic h5py dataset reading"""
    with h5py.File(filename, 'r') as f:
        return f[dataset_name][:]

def chunked_read(filename, dataset_name, chunk_size=10000):
    """Chunked reading of dataset"""
    data = []
    with h5py.File(filename, 'r') as f:
        dset = f[dataset_name]
        for i in range(0, len(dset), chunk_size):
            data.append(dset[i:i+chunk_size])
    return np.concatenate(data)

def memory_map_read(filename, dataset_name):
    """Memory mapping approach"""
    with h5py.File(filename, 'r') as f:
        return np.array(f[dataset_name])

def parallel_read_worker(args):
    """Worker function for parallel reading"""
    filename, dataset_name, start, end = args
    with h5py.File(filename, 'r') as f:
        return f[dataset_name][start:end]

def parallel_read(filename, dataset_name, workers=4):
    """Parallel reading using multiprocessing"""
    with h5py.File(filename, 'r') as f:
        size = len(f[dataset_name])
    chunk_size = size // workers
    ranges = [(filename, dataset_name, i, i+chunk_size) 
              for i in range(0, size, chunk_size)]
    
    with Pool(workers) as p:
        chunks = p.map(parallel_read_worker, ranges)
    return np.concatenate(chunks)

def selective_read(filename, dataset_name, columns=None):
    """Selective column reading"""
    with h5py.File(filename, 'r') as f:
        if columns:
            return f[dataset_name][:, columns]
        return f[dataset_name][:]

def run_benchmark(filename, dataset_name):
    """Run all reading strategies and measure performance"""
    methods = [
        ('Basic', basic_read),
        ('Chunked', chunked_read),
        ('Memory Map', memory_map_read),
        ('Parallel', parallel_read),
        ('Selective', selective_read)
    ]
    
    results = []
    for name, func in methods:
        start_time = time.time()
        start_mem = measure_memory()
        
        # Run the reading method
        data = func(filename, dataset_name)
        
        end_time = time.time()
        end_mem = measure_memory()
        
        results.append({
            'Method': name,
            'Time (s)': end_time - start_time,
            'Memory (MB)': end_mem - start_mem,
            'Data Shape': data.shape
        })
    
    return pd.DataFrame(results)

if __name__ == '__main__':
    # Benchmark all test files
    test_files = [
        ('test_small.h5', 'small_dataset'),
        ('test_medium.h5', 'medium_dataset'),
        ('test_large.h5', 'large_dataset')
    ]
    
    all_results = []
    for filename, dataset in test_files:
        print(f"\nBenchmarking {filename}...")
        df = run_benchmark(filename, dataset)
        df['File'] = filename
        all_results.append(df)
    
    # Save combined results
    results_df = pd.concat(all_results)
    results_df.to_csv('results/benchmark_results.csv', index=False)
    print("\nBenchmarking complete! Results saved to results/benchmark_results.csv")
