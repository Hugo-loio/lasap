import numpy as np
import sys
import os

import lasap.utils.miscellaneous as misc
from lasap.containers.observable import Observable
from lasap.containers.observable import from_disk
from lasap.utils.progress import Progress
from lasap.utils.timer import Timer
from lasap.utils import io

def haar_distance_obs(obs, haar_dirname, haar_basename, avg_key, num_moments, sample_res, timer):
    keys, vals, keynames= obs.get_merged_key_data(avg_key)
    ks = np.arange(1, num_moments+0.5, dtype = int)

    name = obs.props.loc[0,'name'] + "_deltaHaar(" + avg_key + ")" 
    #shape = [2] + list(obs.shape[:-2])
    shape = list(obs.shape[:-2])
    shape = tuple(shape)
    complex_data = False
    props = {}
    keynames = ['n_samples', 'k']  + keynames
    dist_obs = Observable(name, shape, keynames, props, complex_data, inherit_props = obs.props)

    haar_moments = []
    norm_haar_moments = []
    for k in ks:
        haar_obs = from_disk(haar_basename + misc.itos(k,'k'), haar_dirname)
        _, haar_moment = haar_obs.to_numpy()
        haar_moments.append(haar_moment)
        norm_haar_moments.append(np.linalg.norm(haar_moment))

    for i,val in enumerate(vals):
        samples_found = len(val)
        n_samples = misc.logspace(1, samples_found, sample_res)
        if(sample_res == 1):
            n_samples = [samples_found]

        newkeys = np.concatenate([[samp, k], keys[i]])
        print("Found", samples_found, "samples in observable", obs.get_name(), "with keys", keynames, "=", keys)

        o_shape = val.shape
        mid_dim = int(np.prod(shape))

        val = val.reshape((samples_found, mid_dim, o_shape[-2], o_shape[-1]))

        avg = [np.zeros((mid_dim, int(o_shape[-2]**k), int(o_shape[-1]**k)), dtype = val.dtype) for k in ks]

        progress = Progress(samples_found, timer)
        for n,array in enumerate(val):
            # Average
            avg[0] += array 
            for j in range(mid_dim):
                aux_array = np.copy(array[j])
                for e,k in enumerate(ks):
                    if(e == 0):
                        continue
                    aux_array = np.kron(aux_array, array[j])
                    avg[e][j] += aux_array
                    

            samp = n+1
            if(samp in n_samples):
                # TODO: include std here to compute the error

                # Distance
                for e,k in enumerate(ks):
                    dist = np.linalg.norm(avg[e]/samp - haar_moments[e], axis = (1,2))/norm_haar_moments[e]
                    dist_obs.append(dist.reshape(shape), newkeys)
            progress.print_progress(n)

    return dist_obs

def haar_distance(haar_dirname, haar_basename, avg_key, num_moments, sample_res, parallelizer, disk_format):
    print("avg_key:", avg_key)
    new_dirname = parallelizer.dirname + "_deltaHaar(" + avg_key + ")"
    new_path = io.data_dir() + new_dirname
    io.check_dir(new_path)

    timer = Timer()

    print("Processing", parallelizer.numfiles, "files...")
    for i in range(parallelizer.numfiles):
        dist_obs = haar_distance_obs(parallelizer.get_obs(i), haar_dirname, haar_basename, avg_key, num_moments, sample_res, timer)
        dist_obs.set_disk_format(disk_format)
        dist_obs.to_disk(dirname = new_dirname)

    print("Finished haar_distance, job ID:", parallelizer.jobid)
