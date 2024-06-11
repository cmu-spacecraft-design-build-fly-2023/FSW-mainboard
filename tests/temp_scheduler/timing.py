# Time distribution and handling task

import time

from flight.state_manager import state_manager as SM
from flight.tasks.template_task import TemplateTask


class Task(TemplateTask):

    name = "TIMING"
    ID = 0x01

    async def main_task(self):

        print(
            f"[{self.ID}][{self.name}] GLOBAL STATE: {SM.current_state}."
        )
        print(f"[{self.ID}][{self.name}] Time: {time.time()}")

        if SM.current_state == "STARTUP":
            SM.switch_to("NOMINAL")
