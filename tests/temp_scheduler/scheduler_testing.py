
import sys
sys.path.append(".")
print("sys.path", sys.path)

import flight.apps.task_scheduler as task_scheduler
import time 

#task_scheduler.enable_debug_logging()

"""async def your_code():
    print("Hello, world!")
    return 1

async def your_code2():
    print("normandie")
    return 2

async def main_loop():
    await your_code()

scheduled_task = task_scheduler.schedule(hz=2, coroutine_function=main_loop, priority=1)
scheduled_task2 = task_scheduler.schedule(hz=1, coroutine_function=your_code2, priority=2)
task_scheduler.run()"""


from flight.state_manager import state_manager

from sm_configuration import SM_CONFIGURATION, TASK_REGISTRY

state_manager.start("STARTUP", SM_CONFIGURATION, TASK_REGISTRY)