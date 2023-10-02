# This script is meant to be run as a daemon while other simulations are outputingto a specific directory "datadir"
# Once a second, this daemon searches "datadir" for new contents, reads them, and reorganizes them in a directory named "datadir_merged" so that all the parquet data tables with corresponding properties get merged together

import time
import os

from lasap.utils.miscellaneous import check_argc
import lasap.containers.observable as observable
from lasap.utils import io

def merge_daemon(dirname : str, num_outputs : int):
    read_outputs = 0
    props_tables = []
    merged_names = []
    path = io.data_dir() + dirname
    io.check_dir(path)
    merged_dirname = dirname + "_merged"
    while(read_outputs < num_outputs):
        files = io.ls_match(".*_data.parquet", path)
        if(len(files) == 0):
            time.sleep(1)
            continue

        for file in files:
            name = file[:-13]
            obs = observable.from_disk(name, dirname)
            obs_name = obs.get_name()
            if(obs_name in merged_names):
                obs_merged = observable.from_disk(obs_name, merged_dirname)
                if(not obs_merged.props.equals(obs.props)):
                    print("Error: observables with different properties but matching names!")
                    return 1
                obs_merged.merge_data(obs.data)
                obs_merged.to_disk(dirname = merged_dirname)
            else:
                merged_names.append(obs_name)
                obs.to_disk(dirname = merged_dirname)
            read_outputs += 1
            io.rm_data(dirname + "/" + name + "_props.parquet")
            io.rm_data(dirname + "/" + name + "_data.parquet")
