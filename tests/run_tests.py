import os
import sys

import pytest


def add_project_root_to_path():
    project_root = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(project_root, ".."))

    # Add the project root to PYTHONPATH if it isn't already
    if project_root not in sys.path:
        sys.path.append(project_root)


if __name__ == "__main__":
    add_project_root_to_path()

    import numpy  # noqa: F401

    sys.path.append("emulator/cp")
    sys.modules["micropython"] = __import__("micropython_mock")
    sys.modules["ulab"] = __import__("ulab_mock")

    # Run pytest
    pytest.main(["tests"])
