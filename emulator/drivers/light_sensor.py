from hal.drivers.middleware.generic_driver import Driver


class LightSensor:
    def __init__(self, lux) -> None:
        self.__lux = lux

    def lux(self):
        return self.__lux

    def run_diagnostics(self):
        return []
