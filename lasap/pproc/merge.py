import time
import os
import tarfile

import lasap.containers.observable as observable
from lasap.utils import io
from lasap.utils.timer import Timer

# file is the data file name ending in _data.parquet
def merge_file(file, merged_names, dirname, merged_dirname):
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
    io.rm_data(dirname + "/" + name + "_props.parquet")
    io.rm_data(dirname + "/" + name + "_data.parquet")

def parquet_files(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".parquet":
            yield tarinfo

def merge(dirname : str):
    merged_names = []
    path = io.data_dir() + dirname
    io.check_dir(path)
    merged_dirname = dirname + "_merged"
    merged_path = io.data_dir() + merged_dirname
    io.check_dir(merged_path)

    timer = Timer()

    merged_files = io.ls_match(".*_data\.parquet", path + "_merged")
    for file in merged_files:
        obs = observable.from_disk(file[:-13], merged_dirname)
        merged_names.append(obs.get_name())

    print("Merging loose files...")
    files = io.ls_match(".*_data\.parquet", path)
    n = len(files)
    div = 10  
    if(n < div):
        div = n
    for i,file in enumerate(files):
        merge_file(file, merged_names, dirname, merged_dirname)
        e = i+1
        if(e % int(n/div) == 0 or e == n):
            print(str(int(100*e/n)) + " % at " + timer.pretty_time())

    tarfiles = io.ls_match(".*\.tar", path)
    n = len(tarfiles)
    div = 10  
    if(n < div):
        div = n
    print("Merging tar files...")
    for i,tarname in enumerate(tarfiles):
        tar = tarfile.open(path + "/" + tarname)
        tar.extractall(path=path, members=parquet_files(tar))
        tar.close()

        files = io.ls_match(".*_data\.parquet", path)
        for file in files:
            merge_file(file, merged_names, dirname, merged_dirname)

        delete_tar = True
        for info in tar:
            if os.path.splitext(info.name)[1] != ".parquet":
                delete_tar = False
        if(delete_tar):
            os.remove(path + "/" + tarname)

        e = i+1
        if(e % int(n/div) == 0 or e == n):
            print(str(int(100*e/n)) + " % at " + timer.pretty_time())

    if len(os.listdir(path)) == 0:
        os.rmdir(path)

