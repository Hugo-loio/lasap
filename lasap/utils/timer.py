import time

class Timer:
    def __init__(self):
        self.start_time = [time.time()]

    def begin_crono(self):
        self.start_time.append(time.time())
        return int(len(self.start_time))-1

    def time(self, crono_index = 0):
        return time.time() - self.start_time[crono_index]

    def pretty_time(self, crono_index = 0):
        delta = time.time() - self.start_time[crono_index]
        h = int(delta/3600)
        m = int(delta/60 % 60)
        s = int(delta % 60)
        ms = int(1000*delta % 1000)
        return str(h) + ":" + str(m) + ":" + str(s) + ":" + str(ms)
