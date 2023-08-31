from tabulate import tabulate
import os
import glob
import re
import numpy as np
import pickle

def root_path():
    file_path = os.path.dirname(os.path.realpath(__file__))
    return file_path[:file_path.rfind("/")]

def plot_dir():
    return root_path() + "/plots/"

def data_dir():
    custom_path = os.environ.get('DATA_DIR')
    if custom_path != None:
        if os.path.isdir(custom_path): 
            if custom_path[-1] == '/':
                return custom_path
            else:
                return custom_path + '/'
        else:
            print("No directory in " + custom_path)
    return root_path() + "/data/"

def check_data_dir():
    if(not os.path.isdir(root_path() + "/data")):
        try:
            os.mkdir(root_path() + "/data")
        except FileExistsError:
            print("data dir was created by another process")

check_data_dir()
print("Data directory: " + data_dir())

def check_plot_dir():
    if(not os.path.isdir(root_path() + "/plots")):
        os.mkdir(root_path() + "/plots")

def clear_file(file_name):
    open(data_dir() + file_name, 'w').close()

def remove_file(file_name):
    os.remove(data_dir() + file_name)

def check_clear_file(file_name):
    if os.path.isfile(data_dir() + file_name):
        check = input("Clear contents of " + file_name + " ? [y/n] ")
        if check.lower() != "y":
            print(file_name + " not cleared")
            return False
        else:
            clear_file(file_name)
            return True
    else:
        return True


def find_file_list(basename):
    return glob.glob(data_dir() + basename + "_v*.dat")

'''
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
        '''

def check_folder(name):
    path = data_dir() + name
    if(not os.path.isdir(path)):
        try:
            os.mkdir(path)
        except FileExistsError:
            print(path + " was created by another process")
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
