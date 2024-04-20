# from hal.pycubed import hardware
from hal.configuration import SATELLITE
from tasks.template_task import DebugTask
from state_manager import state_manager as SM
from apps.data_handler import DataHandler as DH
import time


class Task(DebugTask):

    name = "IMU"
    ID = 0x03

    data_keys = [
        "time",
        "accel_x",
        "accel_y",
        "accel_z",
        "mag_x",
        "mag_y",
        "mag_z",
        "gyro_x",
        "gyro_y",
        "gyro_z",
    ]

    # Temporary fake time
    curr_time = time.monotonic_ns()

    async def main_task(self):

        if SM.current_state == "NOMINAL":

            if DH.data_process_exists("imu") == False:
                DH.register_data_process(
                    "imu", self.data_keys, "ffffffffff", True, line_limit=40
                )

            # print(f"[{self.ID}][{self.name}] Reading BMX160.")

            readings = {
                "accel": SATELLITE.IMU.accel,
                "mag": SATELLITE.IMU.mag,
                "gyro": SATELLITE.IMU.gyro,
            }

            log_data = {
                "time": time.time(),
                "accel_x": readings["accel"][0],
                "accel_y": readings["accel"][1],
                "accel_z": readings["accel"][2],
                "mag_x": readings["mag"][0],
                "mag_y": readings["mag"][1],
                "mag_z": readings["mag"][2],
                "gyro_x": readings["gyro"][0],
                "gyro_y": readings["gyro"][1],
                "gyro_z": readings["gyro"][2],
            }

            DH.log_data("imu", log_data)

            print(f"[{self.ID}][{self.name}] Data: {readings}")
