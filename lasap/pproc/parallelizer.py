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
        files = io.ls_data_files(path)
        files_per_job = math.ceil(len(files)/numjobs)
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
        file = self.files[index]
        return observable.from_disk(file[:file.rfind('_data')], self.dirname)
