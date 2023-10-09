import numpy as np
import pickle
import sys
import os

from lasap.containers.observable import Observable
from lasap.utils.progress import Progress
from lasap.utils.timer import Timer
from lasap.utils import io

def average_obs(obs : Observable, avg_key : str):
    keys, vals, keynames = obs.get_merged_key_data(avg_key)

    n_samples = len(vals[0])
    print("Found " + str(n_samples) + " samples")
    vals_avg = []
    vals_err = []
    for val in vals:
        vals_avg.append(np.average(val, axis = 0))
        vals_err.append(np.std(val, axis = 0)/np.sqrt(n_samples))

    name = obs.props.loc[0,'name'] + "_avg(" + avg_key + ")"
    shape = tuple([2] + list(obs.shape))
    props = {avg_key + '_samples' : n_samples}
    obs_avg = Observable(name, shape, keynames, props, inherit_props = obs.props)

    for i in range(len(vals_avg)):
        obs_avg.append(np.array([vals_avg[i], vals_err[i]]), keys[i])

    return obs_avg

def average(avg_key, parallelizer):
    print("avg_key:", avg_key)
    avg_dirname = parallelizer.dirname + "_avg(" + avg_key + ")"
    avg_path = io.data_dir() + avg_dirname
    io.check_dir(avg_path)

    timer = Timer()
    progress = Progress(parallelizer.numfiles, timer)

    for i in range(parallelizer.numfiles):
        obs_avg = average_obs(parallelizer.get_obs(i), avg_key)
        obs_avg.to_disk(dirname = avg_dirname)
        progress.print_progress(i)
