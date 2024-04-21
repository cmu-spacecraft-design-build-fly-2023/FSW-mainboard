# Testing script for the UART communication with the payload 

import sys
import time
import gc

from apps.data_handler import DataHandler as DH

from apps.jetson_comms.argus_comm import *
from hal.configuration import SATELLITE

for path in ["/hal", "/apps"]:
    if path not in sys.path:
        sys.path.append(path)

# Just for debug purposes - need initial SD card scan
print("SD Card Directories: ", DH.list_directories())
# DH.delete_all_files()
DH.scan_SD_card()

## Put Jetson Code here 
DH.register_image_process()

## Initialize the UAR
if SATELLITE is None:
    raise RuntimeError("SATELLITE is not defined")

argus_comms = ArgusComm(SATELLITE.PAYLOADUART)

print("Waiting on header...")

tm_path = DH.request_TM_path("img")
print(tm_path)

argus_comms.receive_message()

DH.notify_TM_path("img", tm_path)

from apps.comms.radio_helpers import *

SAT_RADIO = SATELLITE_RADIO(SATELLITE)

SAT_RADIO.image_strs = [tm_path]
SAT_RADIO.image_get_info()

while True:
    if SATELLITE.RADIO is not None:
        SAT_RADIO.transmit_message()

    if SATELLITE.RADIO is not None:
        SAT_RADIO.receive_message()



    # Print out image contents from datahandler

    # try:
    #     argus_comms.receive_message()
    #     ack = Message.create_ack()
    #     argus_comms.send_message(ack)
    # except Exception as e:
    #     print("No receive")
    #     time.sleep(5)
