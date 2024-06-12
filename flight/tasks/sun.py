# Sun Vector Tasks

import time

from apps.data_handler import DataHandler as DH
from apps.sun import compute_body_sun_vector, in_eclipse
from hal.configuration import SATELLITE
from state_manager import state_manager as SM
from tasks.template_task import DebugTask


class Task(DebugTask):

    name = "SUN"
    ID = 0x11

    data_keys = ["time", "x", "y", "z", "eclipse"]

    # Fake starting sun vector
    sun_vector = [1, 0, 0]
    eclipse_state = False

    async def main_task(self):

        if SM.current_state == "NOMINAL":

            if DH.data_process_exists("sun") == False:
                DH.register_data_process(
                    "sun", self.data_keys, "ffffb", True, line_limit=50
                )

            # TODO: Access Sun Sensor Readings - Satellite must return the array directly
            lux_readings = [
                SATELLITE.SUN_SENSOR_XP,
                SATELLITE.SUN_SENSOR_XM,
                SATELLITE.SUN_SENSOR_YP,
                SATELLITE.SUN_SENSOR_YM,
                SATELLITE.SUN_SENSOR_ZP,
                SATELLITE.SUN_SENSOR_ZM,
            ]

            # TODO Fake sun vector that always moves infinitesimally
            self.sun_vector = compute_body_sun_vector(lux_readings)
            self.eclipse_state = in_eclipse(lux_readings)

            readings = {
                "time": time.time(),
                "x": self.sun_vector[0],
                "y": self.sun_vector[1],
                "z": self.sun_vector[2],
                "eclipse": self.eclipse_state,
            }

            DH.log_data("sun", readings)
            print(f"[{self.ID}][{self.name}] Data: {readings}")
