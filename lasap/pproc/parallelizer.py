import math

import lasap.containers.observable as observable
from lasap.utils import io

class Parallelizer:
    def __init__(self, dirname, jobid, numjobs):
        self.dirname = dirname
        self.jobid = jobid
        self.numjobs = numjobs

        path = io.data_dir() + dirname
        io.check_dir(path)
        files = io.ls_match(".*_data\.parquet", path)
        files_per_job = math.ceil(len(files)/numjobs)
        print(files_per_job)
        if(jobid > len(files)):
            self.files = []
            self.numfiles = 0
        else:
            if(jobid == numjobs):
                self.files = files[(jobid-1)*files_per_job:]
            else:
                self.files = files[(jobid-1)*files_per_job:jobid*files_per_job]
            self.numfiles = len(self.files)

    def get_obs(self, index):
        return observable.from_disk(self.files[index][:-13], self.dirname)
