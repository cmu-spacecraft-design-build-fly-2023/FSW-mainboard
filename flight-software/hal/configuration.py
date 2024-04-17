from micropython import const
from hal.cubesat import CubeSat
from hal.argus_v1 import ArgusV1
# from hal.pycubed import PyCubed

PYCUBED_V05 = const(0)
ARGUS_V1 = const(1)

# HARDWARE_VERSION = PyCubed_V05
HARDWARE_VERSION = ARGUS_V1

# Enable for Middleware
DEBUG_MODE = False
EN_MIDDLEWARE = False

SATELLITE: CubeSat = None

if HARDWARE_VERSION == PYCUBED_V05:
    SATELLITE = None
elif HARDWARE_VERSION == ARGUS_V1:
    SATELLITE = ArgusV1(enable_middleware=EN_MIDDLEWARE, debug=DEBUG_MODE)
else:
    raise ValueError(f"Invalid hardware version {HARDWARE_VERSION}")
