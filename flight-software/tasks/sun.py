# Sun Vector Tasks

from hal.pycubed import hardware
from tasks.template_task import DebugTask


from state_manager import state_manager as SM
from apps.data_handler import DataHandler as DH

import rtc
import time


class Task(DebugTask):

    name = "SUN"
    ID = 0x11

    data_keys = [
        "time",
        "sun_x",
        "sun_y",
        "sun_z",
    ]

    async def main_task(self):


        if SM.current_state == "NOMINAL":

            if DH.data_process_exists("imu") == False:
                DH.register_data_process(
                    "sun", self.data_keys, "ffff", True, line_limit=50
                )

            # TODO: Access Sun Sensor Readings 

            print(f"[{self.ID}][{self.name}]  ")



