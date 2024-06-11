from numpy import array

from .cubesat import CubeSat
from .drivers.burnwire import BurnWires
from .drivers.imu import IMU
from .drivers.payload import Payload
from .drivers.power_monitor import PowerMonitor
from .drivers.radio import Radio
from .drivers.sd import SD
from .drivers.sun_sensor import SunSensor


class device:
    """
    Based on the code from: https://docs.python.org/3/howto/descriptor.html#properties
    Attempts to return the appropriate hardware device.
    If this fails, it will attempt to reinitialize the hardware.
    If this fails again, it will raise an exception.
    """

    def __init__(self, fget=None):
        self.fget = fget
        self._device = None

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError(f"unreadable attribute {self._name}")

        if self._device is not None:
            return self._device
        else:
            self._device = self.fget(instance)
            return self._device


class satellite(CubeSat):
    def __init__(self, enable_middleware, debug) -> None:
        self.__middleware_enabled = enable_middleware
        self.__debug = debug

        super().__init__()

        self._burnwires = BurnWires()
        self._radio = Radio()
        self._sd_card = SD()
        self._payload_uart = Payload()

        self._vfs = None
        self._gps = None
        self._charger = None

        self._sun_sensor_xp = SunSensor(900)
        self._sun_sensor_xm = SunSensor(48000)
        self._sun_sensor_yp = SunSensor(85000)
        self._sun_sensor_ym = SunSensor(200)
        self._sun_sensor_zp = SunSensor(12000)
        self._sun_sensor_zm = SunSensor(5000)

        self._torque_x = None
        self._torque_y = None
        self._torque_z = None

        accel = array([1.0, 2.0, 3.0])
        mag = array([4.0, 3.0, 1.0])
        gyro = array([0.0, 0.0, 0.0])
        self._imu = IMU(accel=accel, mag=mag, gyro=gyro, temp=20)

        self._jetson_monitor = PowerMonitor(4, 0.05)
        self._battery_monitor = PowerMonitor(4.2, 0.04)

    def boot_sequence(self) -> list[int]:
        pass

    def run_system_diagnostics(self) -> list[int] | None:
        pass
