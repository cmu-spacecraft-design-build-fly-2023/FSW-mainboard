import sys
from hal.configuration import SATELLITE
from state_manager import state_manager

for path in ["/hal", "/apps"]:
    if path not in sys.path:
        sys.path.append(path)

import gc
gc.collect()
print(str(gc.mem_free()) + " bytes free")

print("Booting Argus1...")
boot_errors = SATELLITE.boot_sequence()
print("Argus1 booted.")
print()

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
import comms_test
# import obdh_sd_test


gc.collect()
print(str(gc.mem_free()) + " bytes free")

print('sdfh')
state_manager.start("STARTUP")

# try:
    # Run forever
    # print('sdfh')
    # state_manager.start("STARTUP")
    
    # import obdh_sd_test
#     pass
# except Exception as e:
#     print(e)
#     # TODO Log the error
