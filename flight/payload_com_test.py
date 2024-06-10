# Testing script for the UART communication with the payload

import gc
import sys
import time

from apps.data_handler import DataHandler as DH
from apps.jetson_comms.argus_comm import *
from hal.configuration import SATELLITE

for path in ["/hal", "/apps"]:
    if path not in sys.path:
        sys.path.append(path)

TIMEOUT = 1000

# Just for debug purposes - need initial SD card scan
print("SD Card Directories: ", DH.list_directories())
DH.scan_SD_card()

DH.delete_all_files()

## Put Jetson Code here
DH.register_image_process()

## Initialize the UAR
if SATELLITE is None:
    raise RuntimeError("SATELLITE is not defined")

argus_comms = ArgusComm(SATELLITE.PAYLOADUART)

from apps.comms.radio_helpers import *

SAT_RADIO = SATELLITE_RADIO(SATELLITE)

while True:
    timed_out = False

    DH.register_image_process()

    print("Waiting on header...")
    ticks = 0
    while not argus_comms.receive_message():
        if ticks > TIMEOUT:
            timed_out = True
            break

        SATELLITE.PAYLOADUART.reset_input_buffer()

    if timed_out:
        print("Timed out waiting for header")
        continue

    DH.image_completed()

    tm_path = DH.request_TM_path("img")
    print("Image path: ", tm_path)

    SAT_RADIO.image_strs = [tm_path]
    SAT_RADIO.image_get_info()

    while True:
        if SATELLITE.RADIO is not None:
            SAT_RADIO.transmit_message()

        if SATELLITE.RADIO is not None:
            SAT_RADIO.receive_message()

        if SAT_RADIO.image_done_transmitting():
            DH.notify_TM_path("img", tm_path)
            DH.clean_up()
            break

    time.sleep(5)

    # Print out image contents from datahandler

    # try:
    #     argus_comms.receive_message()
    #     ack = Message.create_ack()
    #     argus_comms.send_message(ack)
    # except Exception as e:
    #     print("No receive")
    #     time.sleep(5)
