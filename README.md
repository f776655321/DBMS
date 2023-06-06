## Introduction

The main purpose of the class object 'column_matcher' is to find a reasonable and joinable target column given a source table, a target table, and a source specified column.

## Hyperparameters

There are four hyperparameters that can be tuned

- q_start: the start value of the q_gram
- q_end: the end value of the q_gram
- src_keys_ratio: the value deciding whether a source column is the primary key of the table or not
- matching_ratio: the threshold ratio of (matching row pairs / number of rows in the source column)

## Usage

Build a column_matcher object:
    
    my_col_matcher = column_matcher()

Find a reasonable `target_column` given `src_table`, `target_table`, and `src_specified_column`:

    target_column = my_col_matcher.get_column_matching(src_table, target_table, src_specified_column)
