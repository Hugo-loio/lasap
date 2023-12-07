import numpy as np
import sys
import os

from lasap.containers.observable import Observable
from lasap.utils.progress import Progress
from lasap.utils.timer import Timer
from lasap.utils import io

def tail_fraction_obs(obs : Observable, avg_key : str, tail : float):
    keys, vals, keynames = obs.get_merged_key_data(avg_key)

    n_samples = len(vals[0])
    print("Found " + str(n_samples) + " samples in observable " + obs.get_name())
    vals_avg = []
    vals_err = []
    for val in vals:
        istail = val < tail
        vals_avg.append(np.average(istail, axis = 0))
        vals_err.append(np.std(istail, axis = 0)/np.sqrt(n_samples))

    name = obs.props.loc[0,'name'] + "_tail_fraction(" + avg_key + "_" + str(tail)+ ")"
    shape = tuple([2] + list(obs.shape))
    props = {avg_key + '_samples' : n_samples, 'tail' : tail}
    complex_data = obs.props.loc[0,'complex']
    if(complex_data):
        raise TypeError("Not possible to find a tail for complex data") 
    obs = Observable(name, shape, keynames, props, complex_data, inherit_props = obs.props)

    for i in range(len(vals_avg)):
        obs.append(np.array([vals_avg[i], vals_err[i]]), keys[i])

    return obs

def tail_fraction(avg_key, tail, parallelizer, disk_format):
    print("avg_key:", avg_key)
    new_dirname = parallelizer.dirname + "_tail_fraction(" + avg_key + ")"
    new_path = io.data_dir() + new_dirname
    io.check_dir(new_path)

    timer = Timer()
    progress = Progress(parallelizer.numfiles, timer)

    print("Processing", parallelizer.numfiles, "files...")
    for i in range(parallelizer.numfiles):
        obs = tail_fraction_obs(parallelizer.get_obs(i), avg_key, tail)
        obs.set_disk_format(disk_format)
        obs.to_disk(dirname = new_dirname)
        progress.print_progress(i)

    print("Finished haar_distance, job ID:", parallelizer.jobid)
