import board
import time
import digitalio

from micropython import const
from hal.drivers.diagnostics.diagnostics import Diagnostics

class CubeSat:
    """CubeSat: Base class for all CubeSat implementations
    """

    def __init__(self):
        # List of successfully initialized devices
        self.__device_list: list[Diagnostics] = []

        # List of errors from most recent system diagnostic test
        self._recent_errors: list[int] = [Diagnostics.NOERROR]
        
        # State flags
        self._state_flags = None

        # Interfaces
        self._uart1             = None
        self._uart2             = None
        self._spi               = None
        self._i2c1              = None
        self._i2c2              = None

        # Devices
        self._gps               = None
        self._battery_monitor   = None
        self._jetson_monitor    = None
        self._imu               = None
        self._charger           = None
        self._torque_x          = None
        self._torque_y          = None
        self._torque_z          = None
        self._sun_sensor_xp     = None
        self._sun_sensor_xm     = None
        self._sun_sensor_yp     = None
        self._sun_sensor_ym     = None
        self._sun_sensor_zp     = None
        self._sun_sensor_zm     = None
        self._rtc               = None
        self._radio             = None
        self._sd_card           = None
        self._burn_wires        = None
        self._jetson            = None

        # Debugging
        self._neopixel          = None
    
    ## ABSTRACT METHOD ##
    def boot_sequence(self) -> list[int]:
        """boot_sequence: Boot sequence for the CubeSat.
        """
        raise NotImplementedError("CubeSats must implement boot method")
    
    ## ABSTRACT METHOD ##
    def run_system_diagnostics(self) -> list[int] | None:
        """run_diagnostic_test: Run all tests for the component
        """
        raise NotImplementedError("CubeSats must implement diagnostics method")
    
    def get_recent_errors(self) -> list[int]:
        """get_recent_errors: Get the most recent errors from the system
        """
        return self._recent_errors
    
    @property
    def device_list(self):
        """device_list: Get the list of successfully initialized devices
        """
        return self.__device_list
    
    def append_device(self, device):
        """append_device: Append a device to the device list
        """
        self.__device_list.append(device)
    
    ######################### STATE FLAGS ########################
    @property
    def STATE_FLAGS(self):
        """STATE_FLAGS: Returns the state flags object
        :return: object or None
        """
        return self._state_flags

    ######################### INTERFACES #########################
    
    @property
    def UART1(self):
        """UART: Returns the UART interface
        """
        return self._uart1
    
    @property
    def UART2(self):
        """UART2: Returns the UART2 interface
        """
        return self._uart2
    
    @property
    def SPI(self):
        """SPI: Returns the SPI interface
        """
        return self._spi
    
    @property
    def I2C1(self):
        """I2C: Returns the I2C interface
        """
        return self._i2c1
    
    @property
    def I2C2(self):
        """I2C2: Returns the I2C2 interface
        """
        return self._i2c2
    
    ######################### DEVICES #########################
    
    @property
    def GPS(self):
        """GPS: Returns the gps object
        :return: object or None
        """
        return self._gps
    
    @property
    def BATTERY_POWER_MONITOR(self):
        """BATTERY_POWER_MONITOR: Returns the battery power monitor object
        :return: object or None
        """
        return self._battery_monitor
    
    @property
    def JETSON_POWER_MONITOR(self):
        """JETSON_MONITOR: Returns the Jetson monitor object
        :return: object or None
        """
        return self._jetson_monitor
    
    @property
    def IMU(self):
        """IMU: Returns the IMU object
        :return: object or None
        """
        return self._imu
    
    @property
    def CHARGER(self):
        """CHARGER: Returns the charger object
        :return: object or None
        """
        return self._charger
    
    @property
    def TORQUE_X(self):
        """TORQUE_X: Returns the torque driver in the x direction
        :return: object or None
        """
        return self._torque_x
    
    @property
    def TORQUE_Y(self):
        """TORQUE_Y: Returns the torque driver in the y direction
        :return: object or None
        """
        return self._torque_y
    
    @property
    def TORQUE_Z(self):
        """TORQUE_Z: Returns the torque driver in the z direction
        :return: object or None
        """
        return self._torque_z
    
    @property
    def SUN_SENSOR_XP(self):
        """SUN_SENSOR_XP: Returns the sun sensor in the x+ direction
        :return: object or None
        """
        return self._sun_sensor_xp
    
    @property
    def SUN_SENSOR_XM(self):
        """SUN_SENSOR_XM: Returns the sun sensor in the x- direction
        :return: object or None
        """
        return self._sun_sensor_xm
    
    @property
    def SUN_SENSOR_YP(self):
        """SUN_SENSOR_YP: Returns the sun sensor in the y+ direction
        :return: object or None
        """
        return self._sun_sensor_yp
    
    @property
    def SUN_SENSOR_YM(self):
        """SUN_SENSOR_YM: Returns the sun sensor in the y- direction
        :return: object or None
        """
        return self._sun_sensor_ym
    
    @property
    def SUN_SENSOR_ZP(self):
        """SUN_SENSOR_ZP: Returns the sun sensor in the z+ direction
        :return: object or None
        """
        return self._sun_sensor_zp
    
    @property
    def SUN_SENSOR_ZM(self):
        """SUN_SENSOR_ZM: Returns the sun sensor in the z- direction
        :return: object or None
        """
        return self._sun_sensor_zm
    
    @property
    def RTC(self):
        """RTC: Returns the RTC object
        :return: object or None
        """
        return self._rtc
    
    @property
    def RADIO(self):
        """RADIO: Returns the radio object
        :return: object or None
        """
        return self._radio
    
    @property
    def NEOPIXEL(self):
        """NEOPIXEL: Returns the neopixel object
        :return: object or None
        """
        return self._neopixel
    
    @property
    def BURN_WIRES(self):
        """BURN_WIRES: Returns the burn wire object
        :return: object or None
        """
        return self._burn_wires
    
    @property
    def JETSON(self):
        """JETSON: Returns the Jetson object
        :return: object or None
        """
        return self._jetson