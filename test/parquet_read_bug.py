import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
import gc

array_length = 2**20
num_arrays = 10
filename = "test.parquet"

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
    arrow_data = pa.Table.from_pandas(data)
    pq.write_table(arrow_data, filename, use_dictionary=False)
    print("Done")

# Reading the data
try:
    print("Option 1:")
    pq.read_table(filename)
except OSError as e:
    print("Option 1 failed with the following error:\n", e)

'''
try:
    print("Option 2: read column by column")
    div = 2**18
    limit = 2**31-1 # Maximum value I can choose
    col = pq.read_table(filename, columns = ['1'], thrift_string_size_limit = limit, thrift_container_size_limit = limit)
    #col = pq.read_table(filename, columns = ['1'])
    print(col)
    for i in range(1,array_length+1):
        print(i)
        if (i % div == 0):
            print(i)
        pq.read_table(filename, columns = [str(i)], thrift_string_size_limit = limit, thrift_container_size_limit = limit)
except OSError as e:
    print("Option 2 failed with the following error:\n", e)

exit()
'''

print("Option 3:")
print("Memory usage is blowing up here...")
limit = 2**31-1 # Maximum value I can choose
pq.read_table(filename, thrift_string_size_limit = limit, thrift_container_size_limit = limit)
gc.collect()

print("Option 4:")
print("This option either takes too long or it just gets stuck...")
print("Notice how the memory usage is still high from option 2, even after calling the garbage collector.")
pd.read_parquet(filename, engine = 'fastparquet')
