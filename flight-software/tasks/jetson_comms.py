"""
jetson_comms.py 
================
Task to interact with Jetson over UART
"""

# Template task from taskio
from tasks.template_task import DebugTask

# State manager and OBDH
from state_manager import state_manager as SM
from apps.data_handler import DataHandler as DH

# PyCubed Board Lib
from hal.configuration import SATELLITE
from apps.jetson_comms.argus_comm import *

import sys
import time
import gc