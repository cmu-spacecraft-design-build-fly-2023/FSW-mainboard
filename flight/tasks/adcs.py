# Attitude Determination and Control (ADC) task

import time

from apps.sun import SUN_VECTOR_STATUS, compute_body_sun_vector_from_lux, in_eclipse, read_light_sensors
from core import TemplateTask
from core import state_manager as SM
from core.data_handler import DataHandler as DH


class Task(TemplateTask):

    name = "ADCS"
    ID = 0x11

    data_keys = [
        "time",
        "ADCS_STATUS",
        "GYRO_X",
        "GYRO_Y",
        "GYRO_Z",
        "MAG_X",
        "MAG_Y",
        "MAG_Z",
        "SUN_VEC_X",
        "SUN_VEC_Y",
        "SUN_VEC_Z",
        "ECLIPSE",
        "LIGHT_SENSOR_XP",
        "LIGHT_SENSOR_XM",
        "LIGHT_SENSOR_YP",
        "LIGHT_SENSOR_YM",
        "LIGHT_SENSOR_ZP1",
        "LIGHT_SENSOR_ZP2",
        "LIGHT_SENSOR_ZP3",
        "LIGHT_SENSOR_ZP4",
        "LIGHT_SENSOR_ZM",
        "XP_COIL_STATUS",
        "XM_COIL_STATUS",
        "YP_COIL_STATUS",
        "YM_COIL_STATUS",
        "ZP_COIL_STATUS",
        "ZM_COIL_STATUS",
        "COARSE_ATTITUDE",
        "STAR_TRACKER_STATUS",
        "STAR_TRACKER_ATTITUDE",
    ]

    async def main_task(self):

        pass
