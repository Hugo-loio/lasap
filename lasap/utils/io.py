from tabulate import tabulate
import os
import glob
import re
import numpy as np
import pickle
import pyarrow.parquet as pq

def cwd_path():
    return os.getcwd()
#return file_path[:file_path.rfind("/")]

def plot_dir():
    return cwd_path() + "/plots/"

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

def check_plot_dir():
    if(not os.path.isdir(cwd_path() + "/plots")):
        os.mkdir(cwd_path() + "/plots")

def remove_data_file(file_name):
    os.remove(data_dir() + file_name)

def save_pickle(pickle_name, obj):
    pickle_path = data_dir() + pickle_name
    with open(pickle_path, 'wb') as pickle_file:
        pickle.dump(obj, pickle_file)

def load_pickle(pickle_name):
    pickle_path = data_dir() + pickle_name
    try:
        with open(pickle_path, 'rb') as pickle_file:
            return pickle.load( pickle_file)
    except EOFError:
        return None

def check_data_subdir(name):
    path = data_dir() + name
    check_dir(path)
    return path

def ls_match(match, folder_path = None):
    if folder_path == None:
        folder_path = data_dir()
    return [name for name in os.listdir(folder_path) if re.match(match, name)]

def rm_data(name):
    os.remove(data_dir() + name)

def check_file(name):
    path = data_dir() + name
    return os.path.isfile(path)

def print_table(dataframe):
    print(tabulate(dataframe, headers = 'keys', tablefmt = 'psql'))

def write_parquet(table, name, dirname = None):
    check_dir(data_dir())
    path = name
    if(dirname != None):
        path = check_data_subdir(dirname) + "/" + path
    pq.write_table(table, path)

def read_parquet(name, dirname = None):
    path = name
    if(dirname != None):
        path = dirname + "/" + path
    return pq.read_table(data_dir() + path)
