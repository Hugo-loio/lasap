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
jobid = 1
numjobs = 1

match mode:
    case "merge":
        check_argc(3)
        dirname = sys.argv[2]
        pproc.merge.merge(dirname)
    case "average":
        argc = check_argc(4,6)
        dirname = sys.argv[2]
        avg_key = sys.argv[3]
        if(argc == 6):
            jobid = int(sys.argv[4])
            numjobs = int(sys.argv[5])
        pproc.average.average(avg_key, Parallelizer(dirname, jobid, numjobs))
