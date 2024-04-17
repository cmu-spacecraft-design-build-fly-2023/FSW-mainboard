"""
'main.py'
======================
Comms PyCubed test bench. 

Authors: DJ Morvay, Akshat Sahay
"""
from hal.configuration import SATELLITE

# Argus-1 Radio Libs
from apps.comms.radio_helpers import *

SAT_RADIO = SATELLITE_RADIO(SATELLITE)

## ---------- MAIN CODE STARTS HERE! ---------- ##

while True:
    if SATELLITE.RADIO is not None:
        SAT_RADIO.transmit_message()

    if SATELLITE.RADIO is not None:
        SAT_RADIO.receive_message()