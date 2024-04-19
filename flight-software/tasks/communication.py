# TMTC Task

from tasks.template_task import DebugTask


class Task(DebugTask):

    name = "TMTC"
    ID = 0x06

    async def main_task(self):
        print(f"[{self.ID}][{self.name}] Temp.")
