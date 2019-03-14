import os
import time
import signal


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f_rec(name):
    signal.signal(signal.SIGINT, f_busy)
    signal.signal(signal.SIGTERM, f_busy)
    print("REC:")
    for i in range(10):
        print(name + ": %d th iteration" % i)
        time.sleep(0.5)

def f_busy(signum, frame):
    print("BUSY: signal %d" % signum)
    time.sleep(1)
    print("DONE")
    exit(0)

