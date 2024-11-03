# Offer some specific maths results which are reoccurring in my problems
import scipy
import numpy as np
import math
from itertools import permutations
from scipy.special import factorial

import lasap.utils.miscellaneous as misc

def permutation_matrix(perm, d, k):
    dim = d**k
    mat = np.zeros((dim, dim), dtype=int)
    for i in range(dim):
        indices = np.base_repr(i, base=d).zfill(k)
        indices = np.array([int(char) for char in indices]) 
        permuted_indices = [indices[p] for p in perm]
        j = int(''.join(map(str, permuted_indices)), d) # flatten the index
        mat[i, j] = 1
    return mat

def haar_moment(d, k):
    if(d == 1):
        return 1
    perms = np.array(list(permutations(np.arange(k))))
    rho = np.zeros((d**k,d**k), dtype=np.complex128)
    for perm in perms: 
        rho += permutation_matrix(perm, d, k)
    return rho*factorial(d-1)/factorial(k + d - 1)


def haar_frame_potential(d,k):
    return 1/math.comb(k + d - 1, k)
