import sys

sys.path.append("emulator/cp/")
sys.modules["micropython"] = __import__("micropython_mock")
sys.modules["ulab"] = __import__("ulab_mock")
