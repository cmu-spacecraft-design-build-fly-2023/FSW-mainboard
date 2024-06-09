from emulator.cubesat import CubeSat
from emulator.emulator import satellite

# Enable for Middleware
DEBUG_MODE = True
EN_MIDDLEWARE = True

SATELLITE: CubeSat = None
SATELLITE = satellite(enable_middleware=EN_MIDDLEWARE, debug=DEBUG_MODE)
