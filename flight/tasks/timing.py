# Time distribution and handling task

# from hal.pycubed import hardware
import time

import rtc
from flight.core import TemplateTask

import flight.core.state_manager as SM


class Task(TemplateTask):

    name = "TIMING"
    ID = 0x01

    async def main_task(self):

        if SM.current_state == "STARTUP":
            r = rtc.RTC()
            r.datetime = time.struct_time((2024, 4, 24, 9, 30, 0, 3, 115, -1))
            # rtc.set_time_source(r)
        elif SM.current_state == "NOMINAL":
            print(
                f"[{self.ID}][{self.name}] GLOBAL STATE: {SM.current_state}."
            )
            print(f"[{self.ID}][{self.name}] Time: {time.time()}")
