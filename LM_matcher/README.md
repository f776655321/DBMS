# Leverage LM model to do name entity matching

## To test overall performance:

### Usage
```
python ./test_performance/main.py --data_dir data_dir_path --benchmark benchmark
```
* data_dir_path is the path where the whole dataset is. Default is **./data**
* benchmark indicate which benchmark you want to test Default is **autojoin-Benchmark**
* main.py will calculate the average f1 in the whole benchmark and output the cases which f1 are lower than 0.85.
### If you want to test single case, you can type:
```
python ./test_performance/test.py --data_dir data_dir_path --benchmark benchmark --case case
```
* case is a specific directory in the benchmark. Default is **us cities**

### Current result
* Average F1: 0.93
* Cases whose F1 are < 0.85: [christmas songs 1,christmas songs 2,park to state 1]
### Current problem:
Some cases need coloums need to be joined by two coloum or more.

