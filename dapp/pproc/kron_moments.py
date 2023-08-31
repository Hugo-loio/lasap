import numpy as np
import pickle
import sys
import os

import dapp.utils.miscellaneous as misc
from dapp.containers.observable import Observable

def average_std_k_moment(array, k):
    if(k == 1):
        return [np.average(array, axis = 0), np.std(array, axis = 0)]

    o_shape = array.shape
    num_samples = o_shape[0]
    f_shape = list(o_shape)[1:]
    f_shape[-1] = int(f_shape[-1]**k)
    f_shape[-2] = int(f_shape[-2]**k)
    mid_dim = int(np.prod(f_shape[:-2]))

    avg_array = np.zeros((mid_dim, f_shape[-2], f_shape[-1]))
    std_array = np.zeros((mid_dim, f_shape[-2], f_shape[-1]))
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


def kron_moments(obs : Observable, avg_key : str, num_moments : int, mem_avail : float):
    keys, vals = obs.get_merged_key_contents(avg_key)

    n_samples = len(vals[0])

    obs_avg = observable.Observable(obs.props)
    obs_avg.props['name'] = obs_avg.props['name'] + avg_key + "_moms"
    obs_avg.props[avg_key + '_samples'] = n_samples
    obs_avg.props[avg_key + '_num_moments'] = num_moments

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
                key = keys[i].copy()
                key['k'] = k
                #print("Job_id", job_id, key)
                obs_avg.append(key, [np.average(val, axis = 0), np.std(val, axis = 0)/np.sqrt(n_samples)])
                if(k != num_moments):
                    val = misc.kron_last_axes(val, val1)
    else:
        for i,val in enumerate(vals):
            val = np.array(val)
            for k in range(1, num_moments+1):
                key = keys[i].copy()
                key['k'] = k
                #print("Job_id", job_id, key)
                obs_avg.append(key, average_std_k_moment(val, k))
                obs_avg.contents[-1][1] /= np.sqrt(n_samples)

    return obs_avg
