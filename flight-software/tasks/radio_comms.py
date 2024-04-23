"""
radio_comms.py 
================
Comms FSW Task
"""

# Template task from taskio
from tasks.template_task import DebugTask

# State manager and OBDH
from state_manager import state_manager as SM
from apps.data_handler import DataHandler as DH

# PyCubed Board Lib
from hal.configuration import SATELLITE

# Argus-1 Radio Libs
from apps.comms.radio_helpers import *

import time

class Task(DebugTask):

    name = "COMMS"
    ID = 0x12

    SAT_RADIO = SATELLITE_RADIO(SATELLITE)
    tx_header = 0
    heartbeat_sent = True

    async def main_task(self):
        # Only transmit if SAT in NOMINAL state 
        if SM.current_state == "NOMINAL":
            # In NOMINAL state, can transmit 
            self.heartbeat_sent = True

            # # Check if an image is available for downlinking
            # tm_path = DH.request_TM_path("img")
            # if(tm_path != None): 
            #     # Image available, change filepath
            #     self.SAT_RADIO.image_strs = [tm_path]
            #     self.SAT_RADIO.image_get_info()
            # else:
            #     # No image available, use empty filepath
            #     self.SAT_RADIO.image_strs = []
            #     self.SAT_RADIO.image_get_info()

            """
            Heartbeats transmitted every 20s based on task frequency 
            Once transmitted, run receive_message, waits for 1s 
            """

            while(self.heartbeat_sent == True):
                self.tx_header = self.SAT_RADIO.transmit_message()
            
                # Debug message 
                print(f"[{self.ID}][{self.name}] Sent message with ID:", self.tx_header)

                # Receive message, blocking for 1s
                self.heartbeat_sent = self.SAT_RADIO.receive_message()

                if(self.SAT_RADIO.image_done_transmitting()):
                    DH.notify_TM_path("img", tm_path)
                    DH.clean_up()
                    break