import numpy as np
import pickle
import sys
import os

from lasap.containers.observable import Observable

def average(obs : Observable, avg_key : str):
    keys, vals, keynames = obs.get_merged_key_data(avg_key)

    n_samples = len(vals[0])
    print("Found " + str(n_samples) + " samples")
    vals_avg = []
    vals_err = []
    for val in vals:
        vals_avg.append(np.average(val, axis = 0))
        vals_err.append(np.std(val, axis = 0)/np.sqrt(n_samples))

    name = obs.props.loc[0,'name'] + '-' + avg_key + "_avg"
    shape = tuple([2] + list(obs.shape))
    props = {avg_key + '_samples' : n_samples}
    obs_avg = Observable(name, shape, keynames, props, inherit_props = obs.props)

    for i in range(len(vals_avg)):
        obs_avg.append(np.array([vals_avg[i], vals_err[i]]), keys[i])

    return obs_avg
