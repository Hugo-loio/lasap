import numpy as np
import pickle
import sys
import os

import lasap.utils.miscellaneous as misc
from lasap.containers.observable import Observable
from lasap.utils.progress import Progress
from lasap.utils.timer import Timer
from lasap.utils import io

def average_std_k_moment(array, k):
    if(k == 1):
        return [np.average(array, axis = 0), np.std(array, axis = 0)]

    o_shape = array.shape
    num_samples = o_shape[0]
    f_shape = list(o_shape)[1:]
    f_shape[-1] = int(f_shape[-1]**k)
    f_shape[-2] = int(f_shape[-2]**k)
    mid_dim = int(np.prod(f_shape[:-2]))

    avg_array = np.zeros((mid_dim, f_shape[-2], f_shape[-1]), dtype = array.dtype)
    std_array = np.zeros((mid_dim, f_shape[-2], f_shape[-1]), dtype = array.dtype)
    array = array.reshape((o_shape[0], mid_dim, o_shape[-2], o_shape[-1])) 
    
    for i,avg in enumerate(avg_array):
        for e in range(num_samples):
            avg += misc.kron_power(array[e,i], k)
        avg /= float(num_samples)

    for i,std in enumerate(std_array):
        for e in range(num_samples):
            std += np.square(misc.kron_power(array[e,i], k) - avg_array[i])
        std /= float(num_samples)
        std = np.sqrt(std)

    array = array.reshape(o_shape)
    return [avg_array.reshape(f_shape), std_array.reshape(f_shape)]


def kron_moments_obs(obs : Observable, avg_key : str, num_moments : int, mem_avail : float):
    keys, vals, keynames= obs.get_merged_key_data(avg_key)

    n_samples = len(vals[0])
    print("Found " + str(n_samples) + " samples in observable " + obs.get_name())

    moms_obs = []

    for k in range(1, num_moments+1):
        name = obs.props.loc[0,'name'] + "_moms(" + avg_key + ")" + "_k" + str(k)
        shape = [2] + list(obs.shape)
        shape[-1] = int(shape[-1]**k)
        shape[-2] = int(shape[-2]**k)
        shape = tuple(shape)
        complex_data = obs.props.loc[0,'complex']
        props = {avg_key + '_samples' : n_samples, 'k' : k}
        moms_obs.append(Observable(name, shape, keynames, props, complex_data, inherit_props = obs.props))

    sizes = np.zeros(len(vals))
    for i,val in enumerate(vals):
        shape = list(np.array(val).shape)
        for k in range(1, num_moments+1):
            sizes[i] += 8*np.prod(shape[:-2])*np.prod(shape[-2:])**k/1E9

    if(np.amax(sizes) < mem_avail):
        for i,val in enumerate(vals):
            val = np.array(val)
            val1 = np.copy(val)
            for k in range(1, num_moments+1):
                moms_obs[k-1].append(np.array([np.average(val, axis = 0), np.std(val, axis = 0)/np.sqrt(n_samples)]), keys[i])
                if(k != num_moments):
                    val = misc.kron_last_axes(val, val1)
    else:
        for i,val in enumerate(vals):
            val = np.array(val)
            for k in range(1, num_moments+1):
                res = average_std_k_moment(val, k)
                moms_obs[k-1].append(np.array([res[0], res[1]/np.sqrt(n_samples)]), keys[i])

    return moms_obs

def kron_moments(avg_key, num_moments, mem_avail, parallelizer):
    print("avg_key:", avg_key)
    new_dirname = parallelizer.dirname + "_moms(" + avg_key + ")"
    new_path = io.data_dir() + new_dirname
    io.check_dir(new_path)

    timer = Timer()
    progress = Progress(parallelizer.numfiles, timer)

    print("Processing", parallelizer.numfiles, "files...")
    for i in range(parallelizer.numfiles):
        moms_obs = kron_moments_obs(parallelizer.get_obs(i), avg_key, num_moments, mem_avail)
        [obs.to_disk(dirname = new_dirname) for obs in moms_obs]
        progress.print_progress(i)

    print("Finished kron_moments", parallelizer.jobid)
