from datetime import datetime
from time import time

from hal.cubesat import CubeSat
from hal.emulator import satellite
from hal.simulator import Simulator

# Enable for Middleware
# DEBUG_MODE = input("Enter debug mode? (y/n): ").lower().strip() == "y"
# EN_MIDDLEWARE = input("Enable middleware testing? (y/n): ").lower().strip() == "y"
# SOCKET_RADIO = input("Communicate with locally running groundstation? (y/n): ").lower().strip() == "y"
# SIMULATION = input("Use simulator data? (y/n): ").lower().strip() == "y"
DEBUG_MODE = False
EN_MIDDLEWARE = True
SOCKET_RADIO = False
SIMULATION = False


SPACECRAFT: Simulator = None
if SIMULATION:
    SPACECRAFT = Simulator()

SATELLITE: CubeSat = None
SATELLITE = satellite(enable_middleware=EN_MIDDLEWARE, debug=DEBUG_MODE, use_socket=SOCKET_RADIO, sim_spacecraft=SPACECRAFT)
