from hal.drivers.middleware.generic_driver import Driver


class Payload(Driver):
    def __init__(self) -> None:
        super().__init__(None)

    def run_diagnostics(self):
        return []

    def get_flags(self) -> dict:
        return {}
