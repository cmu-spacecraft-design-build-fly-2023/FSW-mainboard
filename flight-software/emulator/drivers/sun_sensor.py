class SunSensor:
    def __init__(self, lux) -> None:
        self.__lux = lux
    
    @property
    def lux(self):
        return self.__lux