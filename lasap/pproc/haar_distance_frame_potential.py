import numpy as np
import sys
import os
import math

import lasap.utils.miscellaneous as misc
from lasap.containers.observable import Observable
from lasap.containers.observable import from_disk
from lasap.utils.progress import Progress
from lasap.utils.timer import Timer
from lasap.utils import io

def haar_distance_obs(obs, avg_key, num_moments, sample_res, timer):
    keys, vals, keynames= obs.get_merged_key_data(avg_key)
    ks = np.arange(1, num_moments+0.5, dtype = int)

    name = obs.props.loc[0,'name'] + "_deltaHaarF(" + avg_key + ")" 
    #shape = [2] + list(obs.shape[:-2])
    shape = list(obs.shape[:-2])
    shape = tuple(shape)
    complex_data = False
    props = {}
    keynames = ['n_samples', 'k']  + keynames
    dist_obs = Observable(name, shape, keynames, props, complex_data, inherit_props = obs.props)

    d = obs.shape[-1]
    haar_frame_potential = [1/math.comb(k + d - 1, k) for k in ks]

    for i,val in enumerate(vals):
        samples_found = len(val)
        n_samples = misc.logspace(1, samples_found, sample_res)
        if(sample_res == 1):
            n_samples = [samples_found]

        newkeys = np.concatenate([[samp, k], keys[i]])
        print("Found", samples_found, "samples in observable", obs.get_name(), "with keys", keynames, "=", newkeys)

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

                frame_potential = np.empty((len(ks),mid_dim))
                for e,k in enumerate(ks):
                    for j in range(mid_dim):
                        rhok = avg[e][j]/samp
                        frame_potential[e,j] = np.linalg.norm(rhok)
                        frame_potential[e,j] *= frame_potential[e,j]

                for e,k in enumerate(ks):
                    dist_obs.append(np.sqrt(frame_potential[e]/haar_frame_potential[e] - 1).reshape(shape), newkeys)
            progress.print_progress(n)

    return dist_obs

def haar_distance_frame_potential(avg_key, num_moments, sample_res, parallelizer, disk_format):
    print("avg_key:", avg_key)
    new_dirname = parallelizer.dirname + "_deltaHaarF(" + avg_key + ")"
    new_path = io.data_dir() + new_dirname
    io.check_dir(new_path)

    timer = Timer()

    print("Processing", parallelizer.numfiles, "files...")
    for i in range(parallelizer.numfiles):
        dist_obs = haar_distance_obs(parallelizer.get_obs(i), avg_key, num_moments, sample_res, timer)
        dist_obs.set_disk_format(disk_format)
        dist_obs.to_disk(dirname = new_dirname)

    print("Finished haar_distance, job ID:", parallelizer.jobid)
