# Testing script for the UART communication with the payload 

import sys
import time
import gc

from apps.data_handler import DataHandler as DH

from apps.jetson_comms.argus_comm import ArgusComm, Message
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

# Define messages to send to the payload (for testing purposes) HERE
end_img = False

while True:
    try:
        msg = argus_comms.receive_message()
        print(msg)
    except Exception as e:
        time.sleep(5)





























