# HDF5 Reading Performance Testing

A project to benchmark and compare different strategies for fast HDF5 file reading in Python.

## Features
- Multiple reading approaches comparison
- Performance benchmarking
- Memory usage tracking
- CSV output for results analysis

## Installation
```bash
pip install -r requirements.txt
```

## Usage
1. Generate test HDF5 files:
```python
python generate_test_data.py
```

2. Run benchmarks:
```python
python benchmark.py
```

3. View results in `results/` directory

## Tested Strategies
1. Basic h5py dataset reading
2. Chunked reading
3. Memory mapping
4. Parallel reading
5. Selective column reading

## Requirements
- Python 3.8+
- h5py
- numpy
- pandas
- tqdm (for progress bars)
