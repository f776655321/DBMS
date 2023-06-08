# Introduction

The main purpose of the class object `column_matcher` is to find a reasonable and joinable target column given a source table, a target table, and a source specified column.

# Hyperparameters

There are four hyperparameters that can be tuned

- `q_start` : the start value of the q_gram
- `q_end` : the end value of the q_gram
- `src_keys_ratio` : the value deciding whether a source column is the primary key of the table or not
- `matching_ratio` : the threshold ratio of (matching row pairs / number of rows in the source column)

# Usage
See testing.py as an example:
## Command line arguments
Follow the format below.

    python testing.py primary_key_file foreign_key_file sepcified_column_of_primary_file
## Build a column_matcher object:
    
    my_col_matcher = column_matcher()

Retrun a tuple (`specified_column_in_primary_key_table`, `foreign_key_table_column`) with reasonable `foreign_key_table_column` given `primary_key_table`, `foreign_key_table`, and `specified_column_in_primary_key_table`:

    foreign_key_table_column = my_col_matcher.get_column_matching(primary_key_table, foreign_key_table, specified_column_in_primary_key_table)

# Experiment

Experiment on the dataset in [**autojoin-Benchmark**](https://github.com/f776655321/DBMS/tree/column_matcher/data/autojoin-Benchmark):

- The accuracy is 30/31 (~ 96.77%)

Experiment on the dataset in [**FlashFill**](https://github.com/f776655321/DBMS/tree/column_matcher/data/FlashFill):

- The accuracy is 108/108 (~ 100%)