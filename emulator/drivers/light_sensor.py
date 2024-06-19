class LightSensor:
    def __init__(self, lux) -> None:
        self.__lux = lux

    def lux(self):
        return self.__lux
