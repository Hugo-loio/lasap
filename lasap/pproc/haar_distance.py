import numpy as np
import sys
import os

import lasap.utils.miscellaneous as misc
from lasap.containers.observable import Observable
from lasap.containers.observable import from_disk
from lasap.utils.progress import Progress
from lasap.utils.timer import Timer
from lasap.utils import io
from lasap.utils.special_functions import haar_moment

def haar_distance_obs(obs, norm, avg_key, num_moments, sample_res, timer):
    keys, vals, oldkeynames= obs.get_merged_key_data(avg_key)
    ks = np.arange(1, num_moments+0.5, dtype = int)

    name = obs.props.loc[0,'name'] + "_deltaHaar(" + avg_key + ")" 
    #shape = [2] + list(obs.shape[:-2])
    shape = list(obs.shape[:-2])
    shape = tuple(shape)
    complex_data = False
    props = {}
    keynames = ['n_samples', 'k'] + oldkeynames
    dist_obs = Observable(name, shape, keynames, props, complex_data, inherit_props = obs.props)

    match norm:
        case "frob" | "frobenious":
            norm_ord = 'fro'
        case "trace":
            norm_ord = 'nuc'

    d = obs.shape[-1]
    haar_moments = [haar_moment(d,k) for k in ks]
    norm_haar_moments = [np.linalg.norm(moment, ord = norm_ord) for moment in haar_moments]

    for i,val in enumerate(vals):
        samples_found = len(val)
        n_samples = misc.logspace(1, samples_found, sample_res)
        if(sample_res == 1):
            n_samples = [samples_found]

        print("Found", samples_found, "samples in observable", obs.get_name(), "with keys", oldkeynames, "=", keys[i])

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
            if(samp not in n_samples):
                continue

            # TODO: include std here to compute the error

            # Distance
            for e,k in enumerate(ks):
                dist = np.linalg.norm(avg[e]/samp - haar_moments[e], axis = (1,2), ord = norm_ord)/norm_haar_moments[e] 
                dist_obs.append(dist.reshape(shape), np.concatenate([[samp, k], keys[i]]))
            progress.print_progress(n)

    return dist_obs

def haar_distance(avg_key, norm, num_moments, sample_res, parallelizer, disk_format):
    print("avg_key:", avg_key)
    new_dirname = parallelizer.dirname + "_deltaHaar(" + avg_key + ")"
    new_path = io.data_dir() + new_dirname
    io.check_dir(new_path)

    timer = Timer()

    print("Processing", parallelizer.numfiles, "files...")
    for i in range(parallelizer.numfiles):
        dist_obs = haar_distance_obs(parallelizer.get_obs(i), norm, avg_key, num_moments, sample_res, timer)
        dist_obs.set_disk_format(disk_format)
        dist_obs.to_disk(dirname = new_dirname)

    print("Finished haar_distance, job ID:", parallelizer.jobid)
