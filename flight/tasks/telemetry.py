# Telemetry packing for transmission

from core import TemplateTask
from core import state_manager as SM


class Task(TemplateTask):

    name = "TM"
    ID = 0x12

    async def main_task(self):

        if SM.current_state == "STARTUP":
            pass

        elif SM.current_state == "NOMINAL":
            pass

        print(f"[{self.ID}][{self.name}] ...")
