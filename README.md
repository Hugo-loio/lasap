# labeled array storage and post-processing (lasap)

This package provides interfaces in different languages for creating data structures based on a series of labeled multi-dimensional arrays. 
Each data set is identifiable with an arbitrary number of properties. 
It utilizes either the CSV or the Apache Parquet file formats for data storage.
It also provides a CLI tool for post-processing the data, i.e. merging data, averaging over a label (key) etc.

All the post-processing utilities are coded in Python but the API for data storage can be installed also in Julia and C++.
(The C++ API does not currently support the Parquet file format).

**Disclamer:** This package is mostly intended for personal use and is not properly documented. 

## Installation

Install and uninstall with the provided scripts in the root folder.

## TODO

* Choose data types for keys and data (potentially lighter data files).
