# lasap (labeled array storage and post-processing)

This package provides interfaces in different languages for data structures with a series of labeled multi-dimensional arrays. It utilizes the Apache Parquet file format for data storage and transmission between different languages.
It also provides post-processing functions for the data, e.g. averaging over a label (key), implemented in python.

Currently only Python and Julia are supported.

**Disclamer:** This package is mostly intended for personal use and is not documented. 

## User dependencies

**Python**

* Numpy
* Pandas
* PyArrow

**Julia**

* OrderedCollections
