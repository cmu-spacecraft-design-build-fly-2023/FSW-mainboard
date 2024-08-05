import datetime
import time

from hal.drivers.middleware.generic_driver import Driver
from numpy import array


class IMU(Driver):
    def __init__(
        self, accel=array([1.0, 2.0, 3.0]), mag=array([4.0, 3.0, 1.0]), gyro=array([0.0, 0.0, 0.0]), temp=20, sim=None
    ) -> None:
        self.__simulator = sim

        if self.__simulator:
            self.boot_sim_sensors()
            self.__accel = accel
        else:
            self.__accel = accel
            self.__mag = mag
            self.__gyro = gyro
            self.__temp = temp
            self.__enable = False
        super().__init__(None)

    def boot_sim_sensors(self):
        from simulation.argusloop.sensors import Gyroscope, Magnetometer

        self.__gyro_sensor = Gyroscope(0.01, 0.2, 0.5)
        self.__mag_sensor = Magnetometer(2.0)

    def accel(self):
        return self.__accel if self.__enable else None

    def mag(self):
        if self.__simulator:
            self.__simulator.advance_to_time(datetime.datetime.fromtimestamp(time.time()))
            return self.__mag_sensor.measure(self.__simulator.spacecraft)
        return self.__mag if self.__enable else None

    def gyro(self):
        if self.__simulator:
            self.__simulator.advance_to_time(datetime.datetime.fromtimestamp(time.time()))
            return self.__gyro_sensor.measure(self.__simulator.spacecraft)
        return self.__gyro if self.__enable else None

    def temp(self):
        return self.__temp if self.__enable else None

    def enable(self):
        self.__enable = True

    def disable(self):
        self.__enable = False

    def run_diagnostics(self) -> list:
        return []

    def get_flags(self) -> dict:
        return {}
