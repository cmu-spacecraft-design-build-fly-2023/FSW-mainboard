from tests.temp_scheduler.sun import Task as sun
from tests.temp_scheduler.timing import Task as timing

TASK_REGISTRY = {
    "TIMING": timing,
    "SUN": sun,
}

TASK_MAPPING_ID = {"SUN": 0x05, "TIMING": 0x01}


SM_CONFIGURATION = {
    "STARTUP": {
        "Tasks": {
            "SUN": {"Frequency": 0.5, "Priority": 1, "ScheduleLater": False},
            "TIMING": {"Frequency": 1, "Priority": 2, "ScheduleLater": False},
        },
        "MovesTo": [
            "NOMINAL",
        ],
    },
    "NOMINAL": {
        "Tasks": {
            "TIMING": {"Frequency": 1, "Priority": 2, "ScheduleLater": False},
            "SUN": {"Frequency": 0.5, "Priority": 5, "ScheduleLater": False},
        },
        "MovesTo": [
            "SAFE",
        ],
    },
}
