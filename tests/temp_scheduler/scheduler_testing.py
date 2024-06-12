import sys

from sm_configuration import SM_CONFIGURATION, TASK_REGISTRY

from flight.core import state_manager as SM

sys.path.append(".")
print("sys.path", sys.path)

# import flight.core.scheduler as scheduler
# scheduler.enable_debug_logging()

SM.start("STARTUP", SM_CONFIGURATION, TASK_REGISTRY)
