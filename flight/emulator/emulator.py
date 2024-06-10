# standard library
from numpy import array

# drivers
from emulator.drivers.burnwire import BurnWires
from emulator.cubesat import CubeSat
from emulator.drivers.imu import IMU
from emulator.drivers.payload import Payload
from emulator.drivers.power_monitor import PowerMonitor
from emulator.drivers.radio import Radio
from emulator.drivers.sd import SD
from emulator.drivers.sun_sensor import SunSensor


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

        self.__burnwires = BurnWires()
        self.__radio = Radio()
        self.__sd_card = SD()
        self.__payload_uart = Payload()

        self.__vfs = None
        self.__gps = None
        self.__charger = None
        
        self.__sun_sensor_xp = SunSensor(900)
        self.__sun_sensor_xm = SunSensor(48000)
        self.__sun_sensor_yp = SunSensor(85000)
        self.__sun_sensor_ym = SunSensor(200)
        self.__sun_sensor_zp = SunSensor(12000)
        self.__sun_sensor_zm = SunSensor(5000)

        self.__torque_x = None
        self.__torque_y = None
        self.__torque_z = None

        accel = array([1.0, 2.0, 3.0])
        mag = array([4.0, 3.0, 1.0])
        gyro = array([0.0, 0.0, 0.0])
        self.__imu = IMU(accel=accel, mag=mag, gyro=gyro, temp=20)

        self.__jetson_monitor = PowerMonitor(4, 0.05)
        self.__battery_monitor = PowerMonitor(4.2, 0.04)
