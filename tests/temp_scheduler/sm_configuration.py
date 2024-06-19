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
            "SUN": {"Frequency": 0.5, "Priority": 1},
            "TIMING": {"Frequency": 0.5, "Priority": 2, "ScheduleLater": True},
        },
        "MovesTo": ["NOMINAL"],
    },
    "NOMINAL": {
        "Tasks": {
            "TIMING": {"Frequency": 1, "Priority": 2},
            "SUN": {"Frequency": 0.5, "Priority": 5},
        },
        "MovesTo": ["DOWNLINK", "LOW_POWER", "SAFE"],
    },
    "DOWNLINK": {
        "Tasks": {
            "TIMING": {"Frequency": 1, "Priority": 2},
            "SUN": {"Frequency": 0.5, "Priority": 5},
        },
        "MovesTo": ["NOMINAL"],
    },
    "LOW_POWER": {
        "Tasks": {
            "TIMING": {"Frequency": 1, "Priority": 2},
            "SUN": {"Frequency": 0.5, "Priority": 5},
        },
        "MovesTo": ["NOMINAL"],
    },
    "SAFE": {
        "Tasks": {
            "TIMING": {"Frequency": 1, "Priority": 2},
            "SUN": {"Frequency": 0.5, "Priority": 5},
        },
        "MovesTo": ["NOMINAL"],
    },
}
