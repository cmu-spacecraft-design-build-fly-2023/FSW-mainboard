"""mw_test.py: Test the middleware system diagnostics.

"""
from hal.configuration import SATELLITE
from hal.cubesat import CubeSat

# Initialize the satellite
satellite: CubeSat = SATELLITE

# Boot the satellite
print("Booting the satellite...")
boot_errors = satellite.boot_sequence()
print("Boot errors:", boot_errors)
print("Booted the satellite")
print()

print("Errors ", satellite.get_recent_errors())
print()

# Run the system diagnostics
print("Running system diagnostics...")
errors = satellite.run_system_diagnostics()
print("System diagnostics complete")
print("Errors:", errors)
print()