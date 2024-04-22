import time
import os
import tarfile
import gc

import lasap.containers.observable as observable
from lasap.utils import io
from lasap.utils.timer import Timer
from lasap.utils.progress import Progress
from lasap.utils.constants import SUPPORTED_DISK_FORMATS


# file is the data file name ending in _data.ext
def merge_file(file, merged_names, dirname, merged_dirname, disk_format):
    name = file[:file.rfind('_data')]
    ext = file[file.rfind('_data')+5:]
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
        obs.set_disk_format(disk_format)
        obs.to_disk(dirname = merged_dirname)
    io.rm_data(dirname + "/" + name + "_props" + ext)
    io.rm_data(dirname + "/" + name + "_data" + ext)

def ext_files(members, ext):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ext:
            yield tarinfo

def merge(dirname : str, disk_format):
    exts = ['.' + ext for ext in SUPPORTED_DISK_FORMATS]
    merged_names = []
    path = io.data_dir() + dirname
    io.check_dir(path)
    merged_dirname = dirname + "_merged"
    merged_path = io.data_dir() + merged_dirname
    io.check_dir(merged_path)

    timer = Timer()

    merged_files = io.ls_data_files(path + "_merged")
    for file in merged_files:
        obs = observable.from_disk(file[:file.rfind('_data')], merged_dirname)
        merged_names.append(obs.get_name())

    print("Merging loose files...")
    files = io.ls_data_files(path)
    progress = Progress(len(files), timer)
    for i,file in enumerate(files):
        merge_file(file, merged_names, dirname, merged_dirname, disk_format)
        progress.print_progress(i)

    tarfiles = io.ls_match(".*\.tar", path)
    progress = Progress(len(tarfiles), timer)
    print("Merging tar files...")
    for i,tarname in enumerate(tarfiles):
        tar = tarfile.open(path + "/" + tarname)
        for ext in exts:
            tar.extractall(path=path, members=ext_files(tar, ext))
        tar.close()

        files = io.ls_data_files(path)
        for file in files:
            merge_file(file, merged_names, dirname, merged_dirname, disk_format)

        delete_tar = True
        for info in tar:
            if (not os.path.splitext(info.name)[1] in exts):
                delete_tar = False
        if(delete_tar):
            os.remove(path + "/" + tarname)
            
        #gc.collect()
        progress.print_progress(i)

    if len(os.listdir(path)) == 0:
        os.rmdir(path)

