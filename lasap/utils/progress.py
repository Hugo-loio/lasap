from lasap.utils.timer import Timer

class Progress:
    def __init__(self, num_procs, timer : Timer = None, div = 10):
        self.num_procs = num_procs
        self.timer = timer
        if(timer == None):
            self.timer = Timer()
        self.div = div
        if(num_procs < self.div):
            self.div = num_procs
        if(self.div == 0):
            self.print_progress = 0
        else:
            self.procs_per_fraction = int(num_procs/self.div)


    def set_progress_divisor(div):
        if(num_procs > div): 
            self.div = div
            self.procs_per_fraction = int(num_procs/div)

    def print_progress(self, proc_index):
        e = proc_index + 1
        if((e % self.procs_per_fraction) == 0 or e == self.num_procs):
            print(str(int(100*e/self.num_procs)) + " % at " + self.timer.pretty_time())
