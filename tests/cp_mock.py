import importlib
import sys

# Add necessary paths
sys.path.append("emulator/cp/")
sys.path.append("flight/")

# Alias 'hal' to 'emulator'
sys.modules["hal"] = importlib.import_module("emulator")

import hal.cp_mock  # noqa: F401, E402
