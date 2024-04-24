"""
jetson_comms.py 
================
Task to interact with Jetson over UART
"""

# Template task from taskio
from tasks.template_task import DebugTask

# State manager and OBDH
from state_manager import state_manager as SM
from apps.data_handler import DataHandler as DH

# PyCubed Board Lib
from hal.configuration import SATELLITE
from apps.jetson_comms.argus_comm import *
from apps.jetson_comms.message_id import *

import sys
import time
import gc
import struct

class Task(DebugTask):

    name = "JETSON"
    ID = 0x13

    argus_comms = ArgusComm(SATELLITE.PAYLOADUART)

    data_keys = [
        "ram",
        "disk",
        "cpu_temp",
        "gpu_temp",
    ]
    
    async def main_task(self):
        # Only communicate if SAT in NOMINAL state
        if SM.current_state == "NOMINAL":
            if DH.data_process_exists("jetson") == False:
                DH.register_data_process(
                    "jetson", self.data_keys, "ffff", True, line_limit=40
                )

            # if (time.time() % 1 == 0):
            #     # Ask Jetson for diagnostic info 
            #     print(f"[{self.ID}][{self.name}] Requesting Jetson for diagnostics")
            #     msg = Message(TRANSMIT_DIAGNOSTIC_DATA, struct.pack(b, 0))

            #     # Read diagnostics 

            #     # Decode message (?)

            #     # Write to data readings

            if (time.time() % 1 == 0):
                # Register image process
                if DH.data_process_exists("img") == False:
                    DH.register_image_process()

                # Ask Jetson for image 
                print(f"[{self.ID}][{self.name}] Requesting Jetson for image")
                msg = Message(TRANSMIT_IMAGE, struct.pack(b, 0))
                    
                # Wait for Jetson comms for 0.1s
                if (self.argus_comms.receive_message() == False):
                    # No message received 
                    print(f"[{self.ID}][{self.name}] No message received from Jetson")
                
                # Image received successfully
                else: 
                    DH.image_completed()
                    print(f"[{self.ID}][{self.name}] Image successfully received from Jetson")
