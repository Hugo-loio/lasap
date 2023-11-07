from tabulate import tabulate
import os
import glob
import re
import numpy as np
import pyarrow.parquet as pq
import pandas as pd
import psutil

from lasap.utils.constants import SUPPORTED_DISK_FORMATS

def cwd_path():
    return os.getcwd()
#return file_path[:file_path.rfind("/")]

def data_dir():
    custom_path = os.environ.get('LASAP_DATA_DIR')
    if custom_path != None:
        if custom_path[-1] == '/':
            return custom_path
        else:
            return custom_path + '/'
    return cwd_path() + "/data/"

def check_dir(path):
    if(not os.path.isdir(path)):
        try:
            os.mkdir(path)
        except FileExistsError:
            print(path + " was created by another process")

def remove_data_file(file_name):
    os.remove(data_dir() + file_name)

def check_data_subdir(name):
    path = data_dir() + name
    check_dir(path)
    return path

def ls_match(match, folder_path = None):
    if folder_path == None:
        folder_path = data_dir()
    return [name for name in os.listdir(folder_path) if re.match(match, name)]

def ls_data_files(folder_path):
    res = []
    for ext in SUPPORTED_DISK_FORMATS:
        res += ls_match(".*_data\." + ext , folder_path)
    return res

def rm_data(name):
    os.remove(data_dir() + name)

def check_file(name):
    path = data_dir() + name
    return os.path.isfile(path)

def print_table(dataframe):
    print(tabulate(dataframe, headers = 'keys', tablefmt = 'psql'))

def write_parquet(table, name, dirname = None):
    path = name
    if(dirname != None):
        path = dirname + "/" + path
    pq.write_table(table, data_dir() + path)

def read_parquet(name, dirname = None):
    path = name
    if(dirname != None):
        path = dirname + "/" + path
    try:
        return pq.read_table(data_dir() + path)
    except OSError:
        avail_mem = min(0.8*psutil.virtual_memory()[1], 2**31-1)
        return pq.read_table(data_dir() + path,
                             #use_threads = False,
                             #memory_map = True,
                             thrift_string_size_limit = avail_mem,
                             thrift_container_size_limit = avail_mem
                             )

def read_parquet_pandas(name, dirname = None):
    path = name
    if(dirname != None):
        path = dirname + "/" + path
    return pd.read_parquet(data_dir() + path, engine = 'fastparquet')

def read_csv_pandas(name, dirname = None):
    path = name
    if(dirname != None):
        path = dirname + "/" + path
    return pd.read_csv(data_dir() + path)
