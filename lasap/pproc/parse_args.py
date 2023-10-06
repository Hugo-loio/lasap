import sys

import lasap.pproc as pproc
import lasap.utils.miscellaneous as misc

mode = sys.argv[1]

match mode:
    case "merge":
        misc.check_argc(3)
        dirname = sys.argv[2]
        pproc.merge.merge(dirname)
    case _:
        print("ERROR: Mode " + mode + " not recognized!")
