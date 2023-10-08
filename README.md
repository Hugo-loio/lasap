# labeled array storage and post-processing (lasap)

This package provides interfaces in different languages for creating data structures based on a series of labeled multi-dimensional arrays. 
Each data set is identifiable with an arbitrary number of properties. 
It utilizes the Apache Parquet file format for data storage and communication between different languages.
It also provides a script for post-processing the data, e.g. averaging over a label (key), implemented in python.

Currently only Python and Julia are supported.

**Disclamer:** This package is mostly intended for personal use and is not documented. 

<!
## User dependencies

**Python**

* Numpy
* Pandas
* PyArrow

**Julia**

* OrderedCollections
>

## Installation

Install and uninstall with the provided scripts in the root folder.

## TODO

* Data visualization script
