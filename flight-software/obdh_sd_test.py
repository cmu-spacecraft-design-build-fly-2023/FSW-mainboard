import time
import board, microcontroller
import random
from collections import OrderedDict
import time

from hal.pycubed import hardware

from apps.data_handler import DataHandler as DH
from apps.data_handler import path_exist


# Just for debug purposes - need initial SD card scan
print("SD Card Directories: ", DH.list_directories())
DH.delete_all_files()

DH.scan_SD_card()

dk1 = [
    "time",
    "a",
    "b",
    "c",
    "d"
    ]

dk2 = [
    "time",
    "gyro",
    "acc",
    "mag"
    ]

print("SD Card Directories: ", DH.list_directories())
DH.register_data_process("log", dk1, "fBBBB", True, line_limit=20)
DH.register_data_process("sun", dk2, "ffff", True, line_limit=15)
print("SD Card Directories: ", DH.list_directories())

i = 0
MAX_STEP = 10


# To generate random boolean
rb = lambda: random.getrandbits(1)



log_data = OrderedDict(
    {
        "time": time.time(),
        "a": rb(),
        "b": rb(),
        "c": rb(),
        "d": rb(),
    }
)
imu_data = OrderedDict(
    {
        "time": time.time(),
        "gyro": random.random(),
        "acc": random.random(),
        "mag": random.random(),
    }
)



DH.log_data("log", log_data)
DH.log_data("imu", imu_data)


time.sleep(2)
DH.print_directory()
path = DH.request_TM_path("log")

print("Exclusion list: ", DH.data_process_registry["log"].excluded_paths)

DH.log_data("log", log_data)
DH.log_data("imu", imu_data)

DH.notify_TM_path("log", path)
print("Deletion list: ", DH.data_process_registry["log"].delete_paths)

DH.log_data("log", log_data)

DH.print_directory()


DH.clean_up()
DH.log_data("log", log_data)

print("Current file size log: ", DH.get_current_file_size("log"))

print("SD directories and files...")

DH.print_directory()

print("FINISHED.")
