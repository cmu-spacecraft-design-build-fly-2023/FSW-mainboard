import sys

import numpy  # noqa: F401

sys.path.append("tests/cp/")
sys.modules["micropython"] = __import__("micropython_mock")
sys.modules["ulab"] = __import__("ulab_mock")
