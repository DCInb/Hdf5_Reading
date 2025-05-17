import h5py
import numpy as np
from tqdm import tqdm

def create_small_dataset():
    """Create a small HDF5 file (~100MB)"""
    with h5py.File('test_small.h5', 'w') as f:
        data = np.random.rand(10000, 100)
        f.create_dataset('small_dataset', data=data)

def create_medium_dataset():
    """Create a medium HDF5 file (~1GB)"""
    with h5py.File('test_medium.h5', 'w') as f:
        data = np.random.rand(100000, 100)
        f.create_dataset('medium_dataset', data=data)

def create_large_dataset():
    """Create a large HDF5 file (~10GB)"""
    with h5py.File('test_large.h5', 'w') as f:
        # Create dataset in chunks to avoid memory issues
        dset = f.create_dataset('large_dataset', (1000000, 100), dtype='float64')
        for i in tqdm(range(0, 1000000, 10000)):
            dset[i:i+10000] = np.random.rand(10000, 100)

if __name__ == '__main__':
    print("Generating test HDF5 files...")
    print("Creating small dataset (100MB)...")
    create_small_dataset()
    print("Small dataset created successfully")
    
    print("Creating medium dataset (1GB)...")
    create_medium_dataset()
    print("Medium dataset created successfully")
    
    print("Creating large dataset (10GB)...")
    create_large_dataset()
    print("Large dataset created successfully")
    
    print("Verifying files exist...")
    import os
    for fname in ['test_small.h5', 'test_medium.h5', 'test_large.h5']:
        if os.path.exists(fname):
            print(f"✓ {fname} exists ({os.path.getsize(fname)/1024/1024:.2f} MB)")
        else:
            print(f"✗ {fname} not found!")
