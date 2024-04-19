# Time distribution and handling task

# from hal.pycubed import hardware
from tasks.template_task import DebugTask


from state_manager import state_manager as SM
from apps.data_handler import DataHandler as DH

import time


class Task(DebugTask):

    name = "TIMING"
    ID = 0x01

    async def main_task(self):
        print(f"[{self.ID}][{self.name}] GLOBAL STATE: {SM.current_state}.")
        print(f"[{self.ID}][{self.name}] No time distribution & handling yet.")
