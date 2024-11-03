import sys

import lasap.pproc as pproc
from lasap.pproc.parallelizer import Parallelizer

def check_argc(*argcs):
    good_argc = False
    right_argc = 0
    for argc in argcs:
        if(len(sys.argv) == argc):
            good_argc = True
            right_argc = argc
    if(not good_argc):
        options = str(argcs[0]) 
        for argc in argcs[1:]:
            options += " or " + str(argc)
        print("ERROR: Expected " + options + " command line arguments, exiting script...")
        sys.exit()
    return right_argc

mode = sys.argv[1]
disk_format = sys.argv[2]
jobid = 1
numjobs = 1

match mode:
    case "merge":
        argc = check_argc(4)
        dirname = sys.argv[3]
        pproc.merge.merge(dirname, disk_format)
    case "average":
        argc = check_argc(5,7)
        dirname = sys.argv[3]
        avg_key = sys.argv[4]
        if(argc == 7):
            jobid = int(sys.argv[5])
            numjobs = int(sys.argv[6])
        pproc.average.average(avg_key, Parallelizer(dirname, jobid, numjobs), disk_format)
    case "kron_moments":
        argc = check_argc(7,9)
        dirname = sys.argv[3]
        avg_key = sys.argv[4]
        num_moments = int(sys.argv[5])
        mem_avail = int(sys.argv[6])
        if(argc == 8):
            jobid = int(sys.argv[7])
            numjobs = int(sys.argv[8])
        pproc.kron_moments.kron_moments(avg_key, num_moments, mem_avail, Parallelizer(dirname, jobid, numjobs), disk_format)
    case "kron_moments_partial":
        argc = check_argc(8,10)
        dirname = sys.argv[3]
        avg_key = sys.argv[4]
        num_moments = int(sys.argv[5])
        mem_avail = int(sys.argv[6])
        n_samples = int(sys.argv[7])
        if(argc == 10):
            jobid = int(sys.argv[8])
            numjobs = int(sys.argv[9])
        pproc.kron_moments_partial.kron_moments_partial(avg_key, num_moments, mem_avail, n_samples, Parallelizer(dirname, jobid, numjobs), disk_format)
    case "haar_distance":
        argc = check_argc(8,10)
        dirname = sys.argv[3]
        avg_key = sys.argv[4]
        norm = sys.argv[5]
        num_moments = int(sys.argv[6])
        sample_res = int(sys.argv[7])
        if(argc == 11):
            jobid = int(sys.argv[8])
            numjobs = int(sys.argv[9])
        pproc.haar_distance.haar_distance(avg_key, norm, num_moments, sample_res, Parallelizer(dirname, jobid, numjobs), disk_format)
    case "haar_distance_frame_potential":
        argc = check_argc(7,9)
        dirname = sys.argv[3]
        avg_key = sys.argv[4]
        num_moments = int(sys.argv[5])
        sample_res = int(sys.argv[6])
        if(argc == 9):
            jobid = int(sys.argv[7])
            numjobs = int(sys.argv[8])
        pproc.haar_distance_frame_potential.haar_distance_frame_potential(avg_key, num_moments, sample_res, Parallelizer(dirname, jobid, numjobs), disk_format)
    case "tail_fraction":
        argc = check_argc(6,8)
        dirname = sys.argv[3]
        avg_key = sys.argv[4]
        tail = float(sys.argv[5])
        if(argc == 8):
            jobid = int(sys.argv[6])
            numjobs = int(sys.argv[7])
        pproc.tail_fraction.tail_fraction(avg_key, tail, Parallelizer(dirname, jobid, numjobs), disk_format)
