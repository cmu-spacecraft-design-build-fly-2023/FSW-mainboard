# Electrical Power Subsystem Task

import time

import microcontroller
from core import TemplateTask
from core import state_manager as SM
from core.data_handler import DataHandler as DH


class Task(TemplateTask):

    name = "EPS"
    ID = 0x12

    data_keys = [
        "MAINBOARD_VOLTAGE",
        "MAINBOARD_CURRENT",
        "BATTERY_PACK_SOC",
        "BATTERY_PACK_REMAINING_CAPACITY_PERC",
        "BATTERY_PACK_CURRENT",
        "BATTERY_PACK_TEMPERATURE",
        "BATTERY_PACK_VOLTAGE",
        "BATTERY_PACK_MIDPOINT_VOLTAGE",
        "BATTERY_CYCLES",
        "BATTERY_PACK_TTE",
        "BATTERY_PACK_TTF",
        "BATTERY_TIME_SINCE_POWER_UP",
        "XP_COIL_VOLTAGE",
        "XP_COIL_CURRENT",
        "XM_COIL_VOLTAGE",
        "XM_COIL_CURRENT",
        "YP_COIL_VOLTAGE",
        "YP_COIL_CURRENT",
        "YM_COIL_VOLTAGE",
        "YM_COIL_CURRENT",
        "ZP_COIL_VOLTAGE",
        "ZP_COIL_CURRENT",
        "ZM_COIL_VOLTAGE",
        "ZM_COIL_CURRENT",
        "JETSON_INPUT_VOLTAGE",
        "JETSON_INPUT_CURRENT",
        "RF_LDO_OUTPUT_VOLTAGE",
        "RF_LDO_OUTPUT_CURRENT",
        "GPS_VOLTAGE",
        "GPS_CURRENT",
        "XP_SOLAR_CHARGE_VOLTAGE",
        "XP_SOLAR_CHARGE_CURRENT",
        "XM_SOLAR_CHARGE_VOLTAGE",
        "XM_SOLAR_CHARGE_CURRENT",
        "YP_SOLAR_CHARGE_VOLTAGE",
        "YP_SOLAR_CHARGE_CURRENT",
        "YM_SOLAR_CHARGE_VOLTAGE",
        "YM_SOLAR_CHARGE_CURRENT",
        "ZP_SOLAR_CHARGE_VOLTAGE",
        "ZP_SOLAR_CHARGE_CURRENT",
        "ZM_SOLAR_CHARGE_VOLTAGE",
        "ZM_SOLAR_CHARGE_CURRENT",
    ]

    async def main_task(self):

        if SM.current_state == "STARTUP":
            if not DH.data_process_exists("eps"):
                pass

        elif SM.current_state == "NOMINAL":

            if not DH.data_process_exists("eps"):
                pass

            # Get power system readings

            ##

            print(f"[{self.ID}][{self.name}] ...")
