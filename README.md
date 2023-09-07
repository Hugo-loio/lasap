# dapp

A data structure and post-processing python package.
The data is stored in a parquet format with specific labeling.

Although the post-processing is done in python, the data structures can be created in other languages.
To achieve this goal I provide functions that generate the parquet tables in other languages with the intended format for the python package.
Currently only Julia is supported.

## Dependencies

### Python

* Numpy
* Pandas
* PyArrow

### Julia

* DataFrames.jl
* Parquet2.jl
* OrderedCollections
