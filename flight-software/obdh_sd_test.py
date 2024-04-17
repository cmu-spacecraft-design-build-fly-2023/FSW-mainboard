import time
import board, microcontroller
import random
from collections import OrderedDict
import time


from apps.data_handler import DataHandler as DH
from apps.data_handler import path_exist


# Just for debug purposes - need initial SD card scan
# DH.delete_all_files()

"""DH.print_directory()
res = path_exist("/sd/log/")
print(res)
time.sleep(500)"""

print("SD Card Directories: ", DH.list_directories())
DH.register_data_process("log", "fBBBB", True, line_limit=20)
DH.register_data_process("imu", "ffff", True, line_limit=10)
DH.register_data_process("sun", "ffffB", True, line_limit=15)
print("SD Card Directories: ", DH.list_directories())

i = 0
MAX_STEP = 10


# To generate random boolean
rb = lambda: random.getrandbits(1)


print("STARTING LOOP")
######################### MAIN LOOP ##############################
while False:

    print("STEP ", i + 1)

    # Create fake data according to the specified formatting
    log_data = OrderedDict(
        {
            "time": time.time(),
            "a_status": rb(),
            "b_status": rb(),
            "c_status": rb(),
            "d_status": rb(),
        }
    )
    DH.log_data("log", *log_data.values())

    imu_data = OrderedDict(
        {
            "time": time.time(),
            "gyro": random.random(),
            "acc": random.random(),
            "mag": random.random(),
        }
    )
    DH.log_data("imu", *imu_data.values())

    sun_data = OrderedDict(
        {
            "time": time.time(),
            "x": random.random(),
            "y": random.random(),
            "z": random.random(),
            "eclipse": rb(),
        }
    )
    DH.log_data("sun", *sun_data.values())

    print("Current file size log: ", DH.get_current_file_size("log"))
    print("Current file size imu: ", DH.get_current_file_size("imu"))
    print("Current file size sun: ", DH.get_current_file_size("sun"))

    print("latest imu: ", DH.get_latest_data("imu"))

    time.sleep(1)

    i += 1

    if i > MAX_STEP:
        break

# test clean-up

log_data = OrderedDict(
    {
        "time": time.time(),
        "a_status": rb(),
        "b_status": rb(),
        "c_status": rb(),
        "d_status": rb(),
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
sun_data = OrderedDict(
    {
        "time": time.time(),
        "x": random.random(),
        "y": random.random(),
        "z": random.random(),
        "eclipse": rb(),
    }
)

DH.log_data("log", *log_data.values())
DH.log_data("imu", *imu_data.values())
DH.log_data("log", *log_data.values())
DH.log_data("sun", *sun_data.values())
DH.log_data("imu", *imu_data.values())
DH.log_data("sun", *sun_data.values())
DH.log_data("log", *log_data.values())
DH.log_data("log", *log_data.values())
time.sleep(2)
DH.print_directory()
path = DH.request_TM_path("log")

print("Exclusion list: ", DH.data_process_registry["log"].excluded_paths)

DH.log_data("log", *log_data.values())
DH.log_data("imu", *imu_data.values())

DH.notify_TM_path("log", path)
print("Deletion list: ", DH.data_process_registry["log"].delete_paths)

DH.log_data("log", *log_data.values())

DH.print_directory()


DH.clean_up()
DH.log_data("log", *log_data.values())

print("Current file size log: ", DH.get_current_file_size("log"))

print("SD directories and files...")

DH.print_directory()

print("FINISHED.")
