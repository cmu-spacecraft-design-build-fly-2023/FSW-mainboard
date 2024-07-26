from hal.drivers.middleware.generic_driver import Driver


class LightSensor(Driver):
    def __init__(self, lux) -> None:
        self.__lux = lux
        super().__init__(None)

    def lux(self):
        return self.__lux

    def run_diagnostics(self):
        return []

    def get_flags(self) -> dict:
        return {}
