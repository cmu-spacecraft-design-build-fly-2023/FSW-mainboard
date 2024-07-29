from hal.cubesat import CubeSat
from hal.emulator import satellite

# Enable for Middleware
DEBUG_MODE = input("Enter debug mode? (y/n): ").lower().strip() == "y"
EN_MIDDLEWARE = input("Enable middleware testing? (y/n): ").lower().strip() == "y"
SOCKET_RADIO = input("Communicate with locally running groundstation? (y/n): ").lower().strip() == "y"
SIMULATION = input("Use simulator data? (y/n): ").lower().strip() == "y"

SATELLITE: CubeSat = None
SATELLITE = satellite(enable_middleware=EN_MIDDLEWARE, debug=DEBUG_MODE, use_socket=SOCKET_RADIO, simulate=SIMULATION)
