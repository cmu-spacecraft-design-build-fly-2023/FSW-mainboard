import sys
from hal.configuration import SATELLITE
from state_manager import state_manager

for path in ["/hal", "/apps"]:
    if path not in sys.path:
        sys.path.append(path)

import gc

gc.collect()
print(str(gc.mem_free()) + " bytes free")

print("Booting ARGUS-1...")
boot_errors = SATELLITE.boot_sequence()
print("ARGUS-1 booted.")
print()
print("initializing the board...")
from hal.pycubed import hardware
from state_manager import state_manager

print("Boot Errors: ", boot_errors)
print()

print("Running system diagnostics...")
errors = SATELLITE.run_system_diagnostics()
print("System diagnostics complete")
print("Errors:", errors)
print()

"""
from apps.data_handler import DataHandler as DH
DH.delete_all_files()
"""

gc.collect()
print(str(gc.mem_free()) + " bytes free")

import comms_test.py

# try:
#     # Run forever
#     state_manager.start("STARTUP")
#     pass

# except Exception as e:
#     print("ERROR:", e)
#     # TODO Log the error
