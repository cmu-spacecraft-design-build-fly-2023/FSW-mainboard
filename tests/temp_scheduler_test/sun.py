import time

import flight.core.state_manager as SM
from flight.core.template_task import DebugTask


class Task(DebugTask):

    name = "SUN"
    ID = 0x11

    async def main_task(self):
        print(f"[{self.ID}][{self.name}] Data: tt")
