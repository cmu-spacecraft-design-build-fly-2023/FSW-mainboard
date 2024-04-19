from tasks.template_task import DebugTask
import gc

class Task(DebugTask):

    name = "MONITOR"
    ID = 0x00

    async def main_task(self):
        print(f"[{self.ID}][{self.name}] {gc.mem_free()} free bytes in memory")
