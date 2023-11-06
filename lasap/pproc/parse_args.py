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
