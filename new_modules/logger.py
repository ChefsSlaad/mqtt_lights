from time import time


def print_file(filename = 'logger.log'):
    with open(filename, 'r') as f:
        for line in f:
            print(line)

def print_time(the_time):
    secs, ms = divmod(the_time, 1)
    mins, sec = divmod(secs, 60)
    hrs, min = divmod(mins, 60)
    return '{:0>3}:{:0>2}:{:0>2}.{:0<3}'.format(int(hrs) % 1000, int(min), int(sec), round(ms*1000))

class dummy_logger():
    def activate(self, *args):
        pass
    def log(self, *args):
        pass

class logger():
    def __init__(self, file = 'logger.log', active = True):
        self.start_time = time()
        self.active    = active
        self.buffer    = []
        self.file      = file
        self.log_freq  = 1 # no of seconds between writes 0 = allways
        self.last_log  = self.start_time
        self.activate(active)

    def __exit__(self):
        self.writelog()

    def __del__(self):
        self.writelog()

    def writelog(self):
        with open(self.file, 'a') as logfile:
            for msg in self.buffer:
                logfile.write(msg)

    def activate(self, active = None):
        if active == None:
            return self.activate
        else:
            self.active = active
        return self.active

    def log(self, *logstrings):
# logs to a file with format hh:mm:ss:mss    log message
        if not self.active:
            return
        the_time = time()
        msg = str(print_time(the_time)) + '  ' + ' '.join(logstrings)
        print(msg)
        self.buffer.append(msg)
        if the_time - self.last_log > self.log_freq:
            self.writelog()
            self.buffer = []

def test():
    log = logger()
    log.log('hello', 'world')
