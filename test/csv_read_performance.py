import numpy as np
import pandas as pd
import os
import gc

array_length = 2**20
num_arrays = 10
filename = "test.csv"

# Only run this if the data file hasn't been already generated
if(not os.path.isfile(filename)):

    # Generate arrays and write them to a dataframe
    print("Generating the dataframe...")
    columns = np.arange(1, array_length + 1)
    data = pd.DataFrame(columns = columns)
    for i in range(1,num_arrays+1):
        array = np.random.rand(array_length)
        data.loc[i] = array
    print("Done")

    # Convert the dataframe to arrow and then save to disk as parquet
    print("Saving to disk...")
    data.to_csv(filename)
    print("Done")

# Reading the data
print("Reading the data...")
pd.read_csv(filename)
print("Done")
