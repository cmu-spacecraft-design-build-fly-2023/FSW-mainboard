from hal.cubesat import CubeSat as hardware

from tasks.template_task import DebugTask

from state_manager import state_manager as SM
from apps.data_handler import DataHandler as DH

import time

class Task(DebugTask):

    name = "IMU"
    ID = 0x05

    async def main_task(self):
        print(f"[{self.ID}][{self.name}] GLOBAL STATE: {SM.current_state}.")
        print(f"[{self.ID}][{self.name}] No IMU task with updated drivers yet.")