import sys
from hal.configuration import SATELLITE
from hal.cubesat import CubeSat
from state_manager import state_manager

for path in ["/hal", "/apps"]:
    if path not in sys.path:
        sys.path.append(path)

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

try:
    # Run forever
    # state_manager.start("STARTUP")
    
    # import obdh_sd_test
    pass
except Exception as e:
    print(e)
    # TODO Log the error
