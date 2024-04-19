# Sun Vector Tasks

# from hal.pycubed import hardware
from tasks.template_task import DebugTask


from state_manager import state_manager as SM
from apps.data_handler import DataHandler as DH
from apps.sun import process_sun_vector

import rtc
import time

import math


class Task(DebugTask):

    name = "SUN"
    ID = 0x11

    data_keys = ["time", "x", "y", "z", "eclipse"]

    # Fake starting sun vector
    sun_vector = [1, 0, 0]

    async def main_task(self):

        if SM.current_state == "NOMINAL":

            if DH.data_process_exists("sun") == False:
                DH.register_data_process(
                    "sun", self.data_keys, "ffffb", True, line_limit=50
                )

            # TODO: Access Sun Sensor Readings - Sun Acquisition
            lux_readings = {}

            # TODO Fake sun vector that always moves infinitesimally
            self.sun_vector, eclipse_state = process_sun_vector(
                lux_readings, self.sun_vector
            )

            readings = {
                "time": time.time(),
                "x": self.sun_vector[0],
                "y": self.sun_vector[1],
                "z": self.sun_vector[2],
                "eclipse": eclipse_state,
            }

            DH.log_data("sun", readings)
            print(f"[{self.ID}][{self.name}] Data: {readings}")
