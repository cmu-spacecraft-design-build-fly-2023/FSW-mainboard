"""
monitor.py 
================
Satellite monitoring task
"""

# Template task from taskio
from tasks.template_task import DebugTask

# State manager and OBDH
from state_manager import state_manager as SM
from apps.data_handler import DataHandler as DH

# PyCubed Board Lib
from hal.configuration import SATELLITE

# Garbage collector and time 
import gc
import time

class Task(DebugTask):

    name = "MONITOR"
    ID = 0x00

    data_keys = [
        "time",
        "system_status"
        "batt_soc",
        "current", 
        "reboot_cnt", 
    ]

    async def main_task(self):
        # If process not registered, register it 
        if DH.data_process_exists("monitor") == False:
            DH.register_data_process(
                "monitor", self.data_keys, "ffffb", True, line_limit=50
            )

        self.batt_soc = int((SATELLITE.battery_voltage / 8.4) * 100)
        
        # Read data for monitoring 
        readings = {
            "time": time.time(),
            "system_status": 0,
            "batt_soc": self.batt_soc, 
            "current": int(SATELLITE.current_draw * 1000), 
            "reboot_cnt": 0,
        }

        DH.log_data("monitor", readings)

        print(f"[{self.ID}][{self.name}] Data: {readings}")
        print(f"[{self.ID}][{self.name}] {gc.mem_free()} free bytes in memory")
