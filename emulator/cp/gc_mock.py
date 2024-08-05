import time

enabled = True


def collect():
    """
    emulate gc.collect() by waiting a short time
    """
    time.sleep(0.001)


def mem_free():
    """
    just returns a constant value for now
    """
    return 1024 * 30


def isenabled():
    global enabled
    return enabled


def enable():
    global enabled
    enabled = True


def disable():
    global enabled
    enabled = False
