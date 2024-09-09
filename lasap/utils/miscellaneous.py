import sys
import numpy as np
import re

def bin_list(dec, min_width : int = 0):
    if(min_width != 0):
        return [int(i) for i in list(('{0:0' + str(min_width) + 'b}').format(dec))]
    else:
        return [int(i) for i in list('{0:b}'.format(dec))]

def check_argc(argc, verbose = True):
    if(verbose):
        print("Checking args:", sys.argv)
    if(len(sys.argv) != argc):
        print("ERROR: Expected " + str(argc) + " command line arguments, exiting script...")
        sys.exit()

def logspace(begin, end, num):
    return np.unique([int(samp) for samp in np.logspace(np.log10(begin), np.log10(end), num = num)])

# float to string for file names
def ftos(val, name, decimals = 2):
    return "_" + name + '{val:.{decimals}f}'.format(val = val, decimals = decimals)

# int to string for file names
def itos(val, name):
    return "_" + name + str(val)

def logspace_from_array(array, num):
    log_points = np.logspace(np.log10(array[0]), np.log10(array[-1]), num = num)
    res = []
    for point in log_points:
        res.append(array[np.argmin(np.abs(array-point))])
    return np.unique(res)

def compare_dicts(dict1, dict2):
    keys1 = list(dict1.keys())
    keys2 = list(dict2.keys())
    values1 = list(dict1.values())
    values2 = list(dict2.values())
    for e,key in enumerate(keys1):
        if(key != keys2[e]):
            return False
        value1 = values1[e]
        value2 = values2[e]
        if(isinstance(value1, np.ndarray)):
            if(isinstance(value2, np.ndarray)):
                if(not np.array_equal(value1, value2)):
                    return False
            else:
                return False
        elif(value1 != value2):
            return False
    return True

# Get value and error strings with dig significant digits in error
def val_err_sig_dig(val, err, dig = 2):
    err_str = "{0:.{dig}g}".format(err, dig = dig)
    if('e' in err_str):
        err_str = str(np.format_float_positional(float(err_str), trim='-'))
    if('.' in err_str):
        decimals = err_str[::-1].find('.')
    else:
        decimals = 0
    val_str = '{:.{decimals}f}'.format(val, decimals=decimals)
    return val_str, err_str

def val_pm_err(val, err, dig = 2):
    val_str, err_str = val_err_sig_dig(val, err, dig)
    return val_str + '\pm' + err_str

def val_paren_err(val, err, dig = 2):
    val_str, err_str = val_err_sig_dig(val, err, dig)
    try:
        err_str = re.findall('[1-9][0-9,.]*',err_str)[0]
    except IndexError:
        err_str = ''
    return val_str + '(' + err_str + ')'

def kron_last_axes(array1, array2):
    fshape = list(array1.shape)
    fshape[-1] *= array2.shape[-1]
    fshape[-2] *= array2.shape[-2]
    fshape = tuple(fshape)

    pre = ''
    for i in range(len(fshape)-2):
        pre += chr(101+i)

    return np.einsum(pre+'ab,'+pre+'cd->'+pre+'acbd', array1, array2).reshape(fshape)

def kron_power(mat, k):
    res = np.copy(mat)
    for i in range(1,k):
        res = np.kron(res, mat)
    return res

def batch_sizes(num, max_batch_size):
    num_batch = int((num-1)/max_batch_size) + 1
    batch_sizes = [max_batch_size for _ in range(num_batch - 1)]
    if(num % max_batch_size != 0):
        batch_sizes.append(num % max_batch_size)
    elif(num >= max_batch_size):
        batch_sizes.append(max_batch_size)
    return batch_sizes
