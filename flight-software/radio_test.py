"""
'main.py'
======================
Comms PyCubed test bench. 

Authors: DJ Morvay, Akshat Sahay
"""

# PyCubed Board Lib
from hal.pycubed import cubesat

# Argus-1 Radio Libs
from apps.argus_radio_helpers import *

SAT_RADIO1 = SATELLITE_RADIO()

## ---------- MAIN CODE STARTS HERE! ---------- ##

while True:
    if cubesat.hardware['Radio1']:
        SAT_RADIO1.transmit_message()

    if cubesat.hardware['Radio1']:
        SAT_RADIO1.receive_message()