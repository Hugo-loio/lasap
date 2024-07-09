import os
import pyarrow as pa
import pandas as pd
import numpy as np

import lasap.utils.io as io
from lasap.utils.constants import SUPPORTED_DISK_FORMATS

class Observable:

    def __init__(self, name : str, shape : tuple = (), keynames = [], props : dict = None, complex_data : bool = False, **kwargs):
        props_dict = {}
        props_dict['name'] = name
        props_dict['complex'] = complex_data
        props_dict['rank'] = len(shape)
        for index,dim in enumerate(shape):
            props_dict['dim' + str(index+1)] = dim
        if(props != None): 
            props_dict.update(props)
        # Metadata about the set of arrays
        self.props = pd.DataFrame([props_dict])

        if(complex_data):
            datasize = 2*np.prod(shape) 
        else:
            datasize = np.prod(shape)

        columns = keynames + list(map(str,list(np.arange(1, datasize+1, dtype=int))))
        #Data dataframe
        self.data = pd.DataFrame(columns = columns)
        #Aux variables
        self.shape = shape
        self.num_keys = len(keynames)
        self.disk_format = 'csv'

        # kwargs
        if 'inherit_props' in kwargs:
            df = kwargs['inherit_props']
            parent_props = df.iloc[:,3+df.loc[0,'rank']:]
            self.props = pd.concat([self.props,parent_props], axis = 1)

        if 'disk_format' in kwargs:
            self.set_disk_format(kwargs['disk_format'])

    def __eq__(self, other):
        if not isinstance(other, Observable):
            return NotImplemented

        return self.props.equals(other.props) and self.data.equals(other.data)

    def set_disk_format(self, disk_format):
        if(disk_format in SUPPORTED_DISK_FORMATS):
            self.disk_format = disk_format
        else:
            self.disk_format = 'csv'
            print("Warning: disk format", disk_format, "not supported, using csv instead.")

    def append(self, array, keyvals = [], check_duplicate = False, replace = False):
        if(self.props.loc[0,'complex']):
            varray = np.concatenate((array.real.flatten(), array.imag.flatten()), axis = 0)
        else:
            varray = array.flatten()

        if(check_duplicate):
            for i, row in self.data.iterrows():
                if(np.array_equal(row.iloc[:self.num_keys].to_numpy(),keyvals)):
                    if(replace):
                        self.data.iloc[i,self.num_keys:] = varray
                        return 1
                    return 2
        row = np.concatenate((keyvals, varray))
        self.data.loc[len(self.data)] = row
        return 0

    def merge_data(self, data_df):
        self.data = pd.concat([self.data,data_df], ignore_index = True)

    def find(self, keyvals):
        for i, row in self.data.iterrows():
            if(np.array_equal(row.iloc[:self.num_keys].to_numpy(),keyvals)):
                return row.iloc[self.num_keys:].to_numpy().reshape(self.shape)

    def get_keynames(self):
        return self.data.columns.values.tolist()[:self.num_keys]

    def __reshape(self, row_array):
        if(self.props.loc[0, 'complex']):
            half = int(len(row_array)/2)
            complex_array = row_array[:half] + 1j*row_array[half:]
            return complex_array.reshape(self.shape)
        else:
            return row_array.reshape(self.shape)

    def get_merged_key_data(self, key : str):
        remain_keynames = self.get_keynames()
        remain_keynames.remove(key)
        keys, vals = [], []
        if(len(remain_keynames) > 0):
            gs = self.data.groupby(remain_keynames)
            if(len(remain_keynames) == 1):
                grouped_dfs = [gs.get_group((g,)).drop(columns=[key]) for g in gs.groups]
            else:
                grouped_dfs = [gs.get_group(g).drop(columns=[key]) for g in gs.groups]
            num_keys = self.num_keys-1
            for df in grouped_dfs:
                keys.append(df.iloc[0,:num_keys].to_numpy())
                vals.append([])
                for i, row in df.iterrows():
                    vals[-1].append(self.__reshape(row.iloc[num_keys:].to_numpy()))
        else:
            df = self.data.drop(columns=[key])
            keys.append([])
            vals.append([])
            for i, row in df.iterrows():
                vals[-1].append(self.__reshape(row.iloc[:].to_numpy()))
        return keys, np.array(vals), remain_keynames

    def to_numpy(self):
        keys = self.data.iloc[:,:self.num_keys].to_numpy()
        array = self.data.iloc[:,self.num_keys:].to_numpy()
        array_reshape = np.array([self.__reshape(row) for row in array])
        return keys, array_reshape

    def get_name(self):
        return self.props.loc[0,'name']


    def to_parquet(self):
        tables = {}
        tables['props'] = pa.Table.from_pandas(self.props)
        tables['data'] = pa.Table.from_pandas(self.data)
        return tables

    def to_disk(self, dirname, name = None, verbose = False, tarname = None):
        io.check_dir(io.data_dir())
        path = io.check_data_subdir(dirname)
        if(name == None):
            name = self.props.loc[0,'name']
        name_props = name + "_props." + self.disk_format
        name_data = name + "_data." + self.disk_format

        match self.disk_format:
            case 'parquet':
                tables = self.to_parquet()
                io.write_parquet(tables['props'], name_props, dirname) 
                io.write_parquet(tables['data'], name_data, dirname) 
            case 'csv':
                self.props.to_csv(path + "/" + name_props, index = False)
                self.data.to_csv(path + "/" + name_data, index = False)

        if(verbose):
            print("Outputed data files to: " + path + "/" + name)

        if(tarname != None):
            tarpath = path + "/" + tarname + ".tar"
            # Bundle files in tar with tarname, and remove the separate files
            os.system('tar -rf ' + tarpath + ' -C ' + path + ' ' + name_props + ' ' + name_data)
            os.remove(path + "/" + name_props)
            os.remove(path + "/" + name_data)

#TODO
"""
def array_type(type):

def key_types(types): 
    """

def from_pandas(props, data):
    obs = Observable('dummy')
    obs.props = props.copy()
    obs.data = data.copy()
    labels = obs.data.columns.values.tolist()
    obs.num_keys = len(labels) - 1 - labels[::-1].index('1')
    shape = []
    for i in range(obs.props.loc[0,'rank']):
        shape.append(obs.props.loc[0,'dim'+str(i+1)])
    obs.shape = tuple(shape)
    return obs

def from_parquet(props, data):
    return from_pandas(props.to_pandas(), data.to_pandas())

def from_disk(name, dirname = None):
    found_file = False
    for disk_format in SUPPORTED_DISK_FORMATS:
        if(io.check_file(dirname + "/" + name + '_props.' + disk_format)):
            found_file = True
            break
    if(not found_file):
        raise FileNotFoundError('No files corresponding to ' + io.data_dir() + dirname + "/" + name + "...")
    match disk_format:
        case 'parquet':
            try:
                props = io.read_parquet(name + '_props.parquet', dirname) 
                data = io.read_parquet(name + '_data.parquet', dirname) 
                obs =  from_parquet(props, data)
            except OSError:
                print("Reading with pyarrow failed, reading with pandas instead...")
                props = io.read_parquet_pandas(name + '_props.parquet', dirname) 
                data = io.read_parquet_pandas(name + '_data.parquet', dirname) 
                obs = from_pandas(props, data)
            obs.set_disk_format('parquet')
        case 'csv':
            props = io.read_csv_pandas(name + '_props.csv', dirname) 
            data = io.read_csv_pandas(name + '_data.csv', dirname) 
            obs = from_pandas(props, data)
            obs.set_disk_format('csv')
    return obs

