import importlib
import os
import sys


def mock_time():
    import time

    return int(time.mktime(time.localtime()))


sys.path.append("./lib/hal/cp/")
sys.modules["micropython"] = __import__("micropython_mock")
sys.modules["ulab"] = __import__("ulab_mock")
sys.modules["rtc"] = __import__("rtc_mock")
sys.modules["gc"] = __import__("gc_mock")

# the fake_time environment variable set in ./run.sh
if "fake_time" in os.environ and os.environ["fake_time"] == "y":
    sys.modules["realtime"] = __import__("time")
    sys.modules["time"] = __import__("time_mock")
else:
    importlib.import_module("time").time = mock_time
