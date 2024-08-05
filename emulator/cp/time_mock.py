import realtime

time_offset = 0
tzname = realtime.tzname
daylight = realtime.daylight


def time() -> int:
    global time_offset
    return int(realtime.time() + time_offset)


def gmtime() -> realtime.struct_time:
    global time_offset
    return realtime.gmtime(time() + time_offset)


def monotonic() -> float:
    global time_offset
    return realtime.monotonic() + time_offset


def monotonic_ns() -> float:
    global time_offset
    return realtime.monotonic_ns() + (time_offset * 1000000000)


def struct_time(data):
    return realtime.struct_time(data)


def sleep(seconds):
    global time_offset
    time_offset += seconds


def localtime(seconds=None):
    return realtime.localtime(seconds)


def perf_counter():
    return realtime.perf_counter()


def strftime(*args, **kwargs):
    return realtime.strftime(*args, **kwargs)
