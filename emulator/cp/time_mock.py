# import time
# from datetime import datetime


# class FakeTime:
#     def __init__(self):
#         self.time_offset = 0

#     def sleep(self, time):
#         self.time_offset += time

#     def time(self):
#         return time.time() + self.time_offset

#     def gmtime(self):
#         return datetime.fromtimestamp(self.time()).timetuple()

#     def monotonic(self):
#         return time.monotonic() + self.time_offset

#     def monotonic_ns(self):
#         return time.monotonic_ns() + self.time_offset

import realtime

time_offset = 0


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
