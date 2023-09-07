#import copy
import pyarrow as pa
import pandas as pd
import numpy as np
import dapp.utils.io as io

class Observable:

    def __init__(self, name : str, shape : tuple = (), keynames = [], props : dict = None, **kwargs):
        props_dict = {}
        props_dict['name'] = name
        props_dict['rank'] = len(shape)
        for index,dim in enumerate(shape):
            props_dict['dim' + str(index+1)] = dim
        if(props != None): 
            props_dict.update(props)
        # Metadata about the set of arrays
        self.props = pd.DataFrame([props_dict])

        columns = keynames + list(map(str,list(np.arange(1, np.prod(shape)+1))))
        #Data dataframe
        self.data = pd.DataFrame(columns = columns)
        #Aux variables
        self.shape = shape
        self.num_keys = len(keynames)

        # kwargs
        if 'inherit_props' in kwargs:
            df = kwargs['inherit_props']
            parent_props = df.iloc[:,2+df.loc[0,'rank']:]
            self.props = pd.concat([self.props,parent_props], axis = 1)

    def __eq__(self, other):
        if not isinstance(other, Observable):
            return NotImplemented

        return self.props.equals(other.props) and self.data.equals(other.data)

    def append(self, array, keyvals = [], check_duplicate = False, replace = False):
        if(check_duplicate):
            for i, row in self.data.iterrows():
                if(np.array_equal(row.iloc[:self.num_keys].to_numpy(),keyvals)):
                    if(replace):
                        self.data.iloc[i,self.num_keys:] = array.flatten()
                        return 1
                    return 2
        row = np.concatenate((keyvals, array.flatten()))
        self.data.loc[len(self.data)] = row
        return 0

    def find(self, keyvals):
        for i, row in self.data.iterrows():
            if(np.array_equal(row.iloc[:self.num_keys].to_numpy(),keyvals)):
                return row.iloc[self.num_keys:].to_numpy().reshape(self.shape)

    def get_keynames(self):
        return self.data.columns.values.tolist()[:self.num_keys]

    def get_merged_key_data(self, key : str):
        remain_keynames = self.get_keynames()
        remain_keynames.remove(key)
        gs = self.data.groupby(remain_keynames)
        grouped_dfs = [gs.get_group(g).drop(columns=[key]) for g in gs.groups]
        keys, vals = [], []
        num_keys = self.num_keys-1
        for df in grouped_dfs:
            keys.append(df.iloc[0,:num_keys].to_numpy())
            vals.append([])
            for i, row in df.iterrows():
                vals[-1].append(row.iloc[num_keys:].to_numpy().reshape(self.shape))
        return keys, vals, remain_keynames


    def to_parquet(self):
        tables = {}
        tables['props'] = pa.Table.from_pandas(self.props)
        tables['data'] = pa.Table.from_pandas(self.data)
        return tables

    def to_disk(self, dirname = None):
        name = self.props.loc[0,'name']
        tables = self.to_parquet()
        io.write_parquet(tables['props'], name + '_props.parquet', dirname) 
        io.write_parquet(tables['data'], name + '_data.parquet', dirname) 

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
    props = io.read_parquet(name + '_props.parquet', dirname) 
    data = io.read_parquet(name + '_data.parquet', dirname) 
    return from_parquet(props, data)
