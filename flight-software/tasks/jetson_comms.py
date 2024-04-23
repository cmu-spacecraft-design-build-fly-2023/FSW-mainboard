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

import sys
import time
import gc

class Task(DebugTask):

    name = "JETSON"
    ID = 0x13

    argus_comms = ArgusComm(SATELLITE.PAYLOADUART)
    TIMEOUT = 1000
    
    async def main_task(self):
        # Only communicate if SAT in NOMINAL state 
        if SM.current_state == "NOMINAL":
            # Register image process
            if DH.data_process_exists("img") == False:
                DH.register_image_process()

            # Ticks for tracking timeout  
            ticks = 0
             
            # Wait for Jetson comms for 0.1s
            if (self.argus_comms.receive_message() == False):
                # No message received 
                print(f"[{self.ID}][{self.name}] No message received from Jetson")
            
            # Image received successfully
            else: 
                DH.image_completed()
                print(f"[{self.ID}][{self.name}] Image successfully received from Jetson")
