from tasks.template_task import DebugTask


class Task(DebugTask):

    name = "MONITOR"
    ID = 0x00

    async def main_task(self):
        print(f"[{self.ID}][{self.name}] I am supposed to monitor the system.")
