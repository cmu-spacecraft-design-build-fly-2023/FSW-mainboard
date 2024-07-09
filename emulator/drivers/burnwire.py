from hal.drivers.middleware.generic_driver import Driver


class BurnWires(Driver):
    def __init__(self, enable=None) -> None:
        super().__init__(enable)

    def duty_cycle(self, duty_cycle):
        assert 0 <= duty_cycle <= 0xFFFF

    def run_diagnostics(self) -> list:
        return []

    def get_flags(self) -> dict:
        return {}
