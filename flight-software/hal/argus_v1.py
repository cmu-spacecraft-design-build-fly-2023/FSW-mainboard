"""
File: argus_v1.py
Author: Harry
Description: This file contains the definition of the ArgusV1 class and its associated interfaces and components.
"""
import busio
from hal.cubesat import CubeSat
from micropython import const
import board
import sdcardio

import neopixel
from hal.drivers.diagnostics.diagnostics import Diagnostics
from hal.drivers import pcf8523, rfm9x, adm1176, bq25883, opt4001, gps, bmx160, drv8830, burnwire, stateflags, torque_coil
from hal.drivers.middleware.middleware import *
from hal.drivers.middleware.exceptions import *

class ArgusV1Interfaces:
    """
    This class represents the interfaces used in the ArgusV1 module.
    """
    
    I2C1_SDA    = board.SDA
    I2C1_SCL    = board.SCL
    I2C1        = busio.I2C(I2C1_SCL, I2C1_SDA)

    I2C2_SDA    = board.SDA2
    I2C2_SCL    = board.SCL2
    I2C2        = busio.I2C(I2C2_SCL, I2C2_SDA)

    SPI_SCK     = board.SCK
    SPI_MOSI    = board.MOSI
    SPI_MISO    = board.MISO
    SPI         = busio.SPI(SPI_SCK, MOSI=SPI_MOSI, MISO=SPI_MISO)

    UART_BAUD   = const(9600)

    UART1_TX    = board.TX
    UART1_RX    = board.RX
    UART1       = busio.UART(UART1_TX, UART1_RX, baudrate=UART_BAUD)

    UART2_TX    = board.JET_TX
    UART2_RX    = board.JET_RX
    UART2       = busio.UART(UART2_TX, UART2_RX, baudrate=UART_BAUD)

class ArgusV1Components:
    """
    Represents the components used in the Argus V1 system.

    This class defines constants for various components such as GPS, battery power monitor,
    Jetson power monitor, IMU, charger, torque coils, sun sensors, radio, and SD card.
    """

    # GPS
    GPS_UART                                = ArgusV1Interfaces.UART1
    GPS_ENABLE                              = board.EN_GPS

    # BATTERY POWER MONITOR
    BATTERY_POWER_MONITOR_I2C               = ArgusV1Interfaces.I2C1
    BATTERY_POWER_MONITOR_I2C_ADDRESS       = const(0x4A)

    # JETSON POWER MONITOR
    JETSON_POWER_MONITOR_I2C                = ArgusV1Interfaces.I2C1
    JETSON_POWER_MONITOR_I2C_ADDRESS        = const(0xCA)

    # IMU
    IMU_I2C                                 = ArgusV1Interfaces.I2C1
    IMU_I2C_ADDRESS                         = const(0x68)
    IMU_ENABLE                              = board.EN_IMU

    # CHARGER
    CHARGER_I2C                             = ArgusV1Interfaces.I2C1
    CHARGER_I2C_ADDRESS                     = const(0x6B)

    # TORQUE COILS
    TORQUE_COILS_I2C                        = ArgusV1Interfaces.I2C2
    TORQUE_XP_I2C_ADDRESS                   = const(0x60)
    TORQUE_XM_I2C_ADDRESS                   = const(0x62)
    TORQUE_YP_I2C_ADDRESS                   = const(0x63)
    TORQUE_YM_I2C_ADDRESS                   = const(0x64)
    TORQUE_Z_I2C_ADDRESS                    = const(0x66)

    # SUN SENSORS
    SUN_SENSORS_I2C                         = ArgusV1Interfaces.I2C2
    SUN_SENSOR_XP_I2C_ADDRESS               = const(0x44)
    SUN_SENSOR_XM_I2C_ADDRESS               = const(0x45)
    SUN_SENSOR_YP_I2C_ADDRESS               = const(0x46)
    SUN_SENSOR_YM_I2C_ADDRESS               = const(0x47)
    SUN_SENSOR_ZP_I2C_ADDRESS               = const(0x49)
    SUN_SENSOR_ZM_I2C_ADDRESS               = const(0x4b)

    # RADIO
    RADIO_SPI                               = ArgusV1Interfaces.SPI
    RADIO_CS                                = board.RF1_CS
    RADIO_RESET                             = board.RF1_RST
    RADIO_ENABLE                            = board.EN_RF
    RADIO_DIO0                              = board.RF1_IO0
    RADIO_FREQ                              = const(433.0)
    # RADIO_FREQ                            = const(915.6)

    # SD CARD
    SD_CARD_SPI                             = ArgusV1Interfaces.SPI
    SD_CARD_CS                              = board.SD_CS
    SD_BAUD                                 = const(4000000) # 4 MHz

    # BURN WIRES
    BURN_WIRE_ENABLE                        = board.RELAY_A
    BURN_WIRE_XP                            = board.BURN1
    BURN_WIRE_XM                            = board.BURN2
    BURN_WIRE_YP                            = board.BURN3
    BURN_WIRE_YM                            = board.BURN4

    # RTC
    RTC_I2C                                 = ArgusV1Interfaces.I2C1
    RTC_I2C_ADDRESS                         = const(0x68)

    # NEOPIXEL
    NEOPIXEL_SDA                            = board.NEOPIXEL
    NEOPIXEL_N                              = const(1) # Number of neopixels in chain
    NEOPIXEL_BRIGHTNESS                     = const(0.2)

    # JETSON
    JETSON_UART                             = ArgusV1Interfaces.UART2
    JETSON_ENABLE                           = board.EN_JET

class ArgusV1(CubeSat):
    """ArgusV1: Represents the Argus V1 CubeSat.
    
    """
    
    def __init__(self, enable_middleware: bool = False, debug: bool = False):
        """__init__: Initializes the Argus V1 CubeSat.

        :param enable_middleware: Enable middleware for the Argus V1 CubeSat
        """
        self.__middleware_enabled = enable_middleware
        self.__debug = debug

        super().__init__()

    ######################## BOOT SEQUENCE ########################

    def boot_sequence(self) -> list[int]:
        """boot_sequence: Boot sequence for the CubeSat.
        """
        error_list: list[int] = []

        # Create individual torque coil driver instances
        self.__torque_xp_driver  = None
        self.__torque_xm_driver  = None
        self.__torque_yp_driver  = None
        self.__torque_ym_driver  = None
        self.__torque_z_driver   = None

        self.__state_flags_boot() # Does not require error checking

        error_list += self.__rtc_boot()
        error_list += self.__gps_boot()
        error_list += self.__battery_power_monitor_boot()
        error_list += self.__jetson_power_monitor_boot()
        error_list += self.__imu_boot()
        error_list += self.__charger_boot()
        error_list += self.__torque_interface_boot()
        error_list += self.__sun_sensor_xp_boot()
        error_list += self.__sun_sensor_xm_boot()
        error_list += self.__sun_sensor_yp_boot()
        error_list += self.__sun_sensor_ym_boot()
        error_list += self.__sun_sensor_zp_boot()
        error_list += self.__sun_sensor_zm_boot()
        error_list += self.__radio_boot()
        error_list += self.__neopixel_boot()
        error_list += self.__sd_card_boot()
        error_list += self._burn_wire_boot()
        error_list += self._jetson_boot()

        error_list = [error for error in error_list if error != Diagnostics.NOERROR]

        if self.__debug:
            print("Boot Errors:")
            print()
            for error in error_list:
                print(f"{Diagnostics.diagnostic_to_string(error)}")
            print()

        self._recent_errors = error_list

        return error_list

    def __state_flags_boot(self) -> None:
        """state_flags_boot: Boot sequence for the state flags
        """
        self._state_flags = stateflags.StateFlags()
    
    def __gps_boot(self) -> int:
        """GPS_boot: Boot sequence for the GPS

        :return: Error code if the GPS failed to initialize
        """
        try:
            gps1 = gps.GPS(ArgusV1Components.GPS_UART,
                           ArgusV1Components.GPS_ENABLE)
            
            if self.__middleware_enabled:
                gps1 = Middleware(gps1, gps_fatal_exception)

            self._gps = gps1
            self.__device_list.append(gps1)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)

            return Diagnostics.GPS_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __battery_power_monitor_boot(self) -> int:
        """battery_power_monitor_boot: Boot sequence for the battery power monitor

        :return: Error code if the battery power monitor failed to initialize
        """
        try:
            battery_monitor = adm1176.ADM1176(ArgusV1Components.BATTERY_POWER_MONITOR_I2C,
                                              ArgusV1Components.BATTERY_POWER_MONITOR_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                battery_monitor = Middleware(battery_monitor, battery_power_monitor_fatal_exception)

            self._battery_monitor = battery_monitor
            self.__device_list.append(battery_monitor)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)

            return Diagnostics.ADM1176_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __jetson_power_monitor_boot(self) -> int:
        """jetson_power_monitor_boot: Boot sequence for the Jetson power monitor

        :return: Error code if the Jetson power monitor failed to initialize
        """
        try:
            jetson_monitor = adm1176.ADM1176(ArgusV1Components.JETSON_POWER_MONITOR_I2C,
                                             ArgusV1Components.JETSON_POWER_MONITOR_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                jetson_monitor = Middleware(jetson_monitor, jetson_power_monitor_fatal_exception)
            
            self._jetson_monitor = jetson_monitor
            self.__device_list.append(jetson_monitor)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.ADM1176_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __imu_boot(self) -> int:
        """imu_boot: Boot sequence for the IMU

        :return: Error code if the IMU failed to initialize
        """
        try:
            imu = bmx160.BMX160(ArgusV1Components.IMU_I2C,
                                ArgusV1Components.IMU_I2C_ADDRESS,
                                ArgusV1Components.IMU_ENABLE)
            
            if self.__middleware_enabled:
                imu = Middleware(imu, imu_fatal_exception)
            
            self._imu = imu
            self.__device_list.append(imu)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.BMX160_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __charger_boot(self) -> int:
        """charger_boot: Boot sequence for the charger

        :return: Error code if the charger failed to initialize
        """
        try:
            charger = bq25883.BQ25883(ArgusV1Components.CHARGER_I2C,
                                      ArgusV1Components.CHARGER_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                charger = Middleware(charger, charger_fatal_exception)
            
            self._charger = charger
            self.__device_list.append(charger)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.BQ25883_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __torque_xp_boot(self) -> int:
        """torque_xp_boot: Boot sequence for the torque driver in the x+ direction

        :return: Error code if the torque driver failed to initialize
        """
        try:
            torque_xp = drv8830.DRV8830(ArgusV1Components.TORQUE_COILS_I2C,
                                        ArgusV1Components.TORQUE_XP_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                torque_xp = Middleware(torque_xp, torque_xp_fatal_exception)
            
            self.__torque_xp_driver = torque_xp
            self.__device_list.append(torque_xp)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.DRV8830_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __torque_xm_boot(self) -> int:
        """torque_xm_boot: Boot sequence for the torque driver in the x- direction

        :return: Error code if the torque driver failed to initialize
        """
        try:
            torque_xm = drv8830.DRV8830(ArgusV1Components.TORQUE_COILS_I2C,
                                        ArgusV1Components.TORQUE_XM_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                torque_xm = Middleware(torque_xm, torque_xm_fatal_exception)
            
            self.__torque_xm_driver = torque_xm
            self.__device_list.append(torque_xm)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.DRV8830_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __torque_yp_boot(self) -> int:
        """torque_yp_boot: Boot sequence for the torque driver in the y+ direction

        :return: Error code if the torque driver failed to initialize
        """
        try:
            torque_yp = drv8830.DRV8830(ArgusV1Components.TORQUE_COILS_I2C,
                                        ArgusV1Components.TORQUE_YP_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                torque_yp = Middleware(torque_yp, torque_yp_fatal_exception)
            
            self.__torque_yp_driver = torque_yp
            self.__device_list.append(torque_yp)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.DRV8830_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __torque_ym_boot(self) -> int:
        """torque_ym_boot: Boot sequence for the torque driver in the y- direction

        :return: Error code if the torque driver failed to initialize
        """
        try:
            torque_ym = drv8830.DRV8830(ArgusV1Components.TORQUE_COILS_I2C,
                                        ArgusV1Components.TORQUE_YM_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                torque_ym = Middleware(torque_ym, torque_ym_fatal_exception)
            
            self.__torque_ym_driver = torque_ym
            self.__device_list.append(torque_ym)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.DRV8830_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __torque_z_boot(self) -> int:
        """torque_z_boot: Boot sequence for the torque driver in the z direction

        :return: Error code if the torque driver failed to initialize
        """
        try:
            torque_z = drv8830.DRV8830(ArgusV1Components.TORQUE_COILS_I2C,
                                       ArgusV1Components.TORQUE_Z_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                torque_z = Middleware(torque_z, torque_z_fatal_exception)
            
            self.__torque_z_driver = torque_z
            self.__device_list.append(torque_z)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.DRV8830_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __torque_interface_boot(self) -> int:
        """torque_interface_boot: Boot sequence for the torque interface

        :return: Error code if the torque interface failed to initialize
        """
        error_list: list[int] = []

        error_list += self.__torque_xp_boot()
        error_list += self.__torque_xm_boot()
        error_list += self.__torque_yp_boot()
        error_list += self.__torque_ym_boot()
        error_list += self.__torque_z_boot()

        # X direction
        try:
            torque_interface = torque_coil.TorqueInterface(self._torque_xp, self._torque_xm)
            self._torque_x = torque_interface
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)

        # Y direction
        try:
            torque_interface = torque_coil.TorqueInterface(self._torque_yp, self._torque_ym)
            self._torque_y = torque_interface
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
        
        # Z direction
        try:
            torque_interface = torque_coil.TorqueInterface(self._torque_z)
            self._torque_z = torque_interface
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
        
        return error_list
    
    def __sun_sensor_xp_boot(self) -> int:
        """sun_sensor_xp_boot: Boot sequence for the sun sensor in the x+ direction

        :return: Error code if the sun sensor failed to initialize
        """
        try:
            sun_sensor_xp = opt4001.OPT4001(ArgusV1Components.SUN_SENSORS_I2C,
                                            ArgusV1Components.SUN_SENSOR_XP_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                sun_sensor_xp = Middleware(sun_sensor_xp, sun_sensor_xp_fatal_exception)
            
            self._sun_sensor_xp = sun_sensor_xp
            self.__device_list.append(sun_sensor_xp)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.OPT4001_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __sun_sensor_xm_boot(self) -> int:
        """sun_sensor_xm_boot: Boot sequence for the sun sensor in the x- direction

        :return: Error code if the sun sensor failed to initialize
        """
        try:
            sun_sensor_xm = opt4001.OPT4001(ArgusV1Components.SUN_SENSORS_I2C,
                                            ArgusV1Components.SUN_SENSOR_XM_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                sun_sensor_xm = Middleware(sun_sensor_xm, sun_sensor_xm_fatal_exception)
            
            self._sun_sensor_xm = sun_sensor_xm
            self.__device_list.append(sun_sensor_xm)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.OPT4001_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __sun_sensor_yp_boot(self) -> int:
        """sun_sensor_yp_boot: Boot sequence for the sun sensor in the y+ direction

        :return: Error code if the sun sensor failed to initialize
        """
        try:
            sun_sensor_yp = opt4001.OPT4001(ArgusV1Components.SUN_SENSORS_I2C, 
                                            ArgusV1Components.SUN_SENSOR_YP_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                sun_sensor_yp = Middleware(sun_sensor_yp, sun_sensor_yp_fatal_exception)
            
            self._sun_sensor_yp = sun_sensor_yp
            self.__device_list.append(sun_sensor_yp)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.OPT4001_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __sun_sensor_ym_boot(self) -> int:
        """sun_sensor_ym_boot: Boot sequence for the sun sensor in the y- direction

        :return: Error code if the sun sensor failed to initialize
        """
        try:
            sun_sensor_ym = opt4001.OPT4001(ArgusV1Components.SUN_SENSORS_I2C, 
                                            ArgusV1Components.SUN_SENSOR_YM_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                sun_sensor_ym = Middleware(sun_sensor_ym, sun_sensor_ym_fatal_exception)
            
            self._sun_sensor_ym = sun_sensor_ym
            self.__device_list.append(sun_sensor_ym)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.OPT4001_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __sun_sensor_zp_boot(self) -> int:
        """sun_sensor_zp_boot: Boot sequence for the sun sensor in the z+ direction

        :return: Error code if the sun sensor failed to initialize
        """
        try:
            sun_sensor_zp = opt4001.OPT4001(ArgusV1Components.SUN_SENSORS_I2C, 
                                            ArgusV1Components.SUN_SENSOR_ZP_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                sun_sensor_zp = Middleware(sun_sensor_zp, sun_sensor_zp_fatal_exception)
            
            self._sun_sensor_zp = sun_sensor_zp
            self.__device_list.append(sun_sensor_zp)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.OPT4001_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __sun_sensor_zm_boot(self) -> int:
        """sun_sensor_zm_boot: Boot sequence for the sun sensor in the z- direction

        :return: Error code if the sun sensor failed to initialize
        """
        try:
            sun_sensor_zm = opt4001.OPT4001(ArgusV1Components.SUN_SENSORS_I2C, 
                                            ArgusV1Components.SUN_SENSOR_ZM_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                sun_sensor_zm = Middleware(sun_sensor_zm, sun_sensor_zm_fatal_exception)
            
            self._sun_sensor_zm = sun_sensor_zm
            self.__device_list.append(sun_sensor_zm)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.OPT4001_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __radio_boot(self) -> int:
        """radio_boot: Boot sequence for the radio

        :return: Error code if the radio failed to initialize
        """
        try:
            radio = rfm9x.RFM9x(ArgusV1Components.RADIO_SPI, 
                                ArgusV1Components.RADIO_CS,
                                ArgusV1Components.RADIO_DIO0,
                                ArgusV1Components.RADIO_RESET, 
                                ArgusV1Components.RADIO_ENABLE,
                                ArgusV1Components.RADIO_FREQ)
            
            if self.__middleware_enabled:
                radio = Middleware(radio, radio_fatal_exception)
            
            self._radio = radio
            self.__device_list.append(radio)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.RFM9X_NOT_INITIALIZED
    
        return Diagnostics.NOERROR
    
    def __rtc_boot(self) -> int:
        """rtc_boot: Boot sequence for the RTC

        :return: Error code if the RTC failed to initialize
        """
        try:
            rtc = pcf8523.PCF8523(ArgusV1Components.RTC_I2C, 
                                  ArgusV1Components.RTC_I2C_ADDRESS)
            
            if self.__middleware_enabled:
                rtc = Middleware(rtc, rtc_fatal_exception)
            
            self._rtc = rtc
            self.__device_list.append(rtc)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.PCF8523_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __neopixel_boot(self) -> int:
        """neopixel_boot: Boot sequence for the neopixel
        """
        try:
            np = neopixel.NeoPixel(ArgusV1Components.NEOPIXEL_SDA,
                               ArgusV1Components.NEOPIXEL_N,
                               brightness=ArgusV1Components.NEOPIXEL_BRIGHTNESS,
                               pixel_order=neopixel.GRB)
            self._neopixel = np
            self.__device_list.append(neopixel)
            self.append_device(neopixel)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.NEOPIXEL_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def __sd_card_boot(self) -> int:
        """sd_card_boot: Boot sequence for the SD card
        """
        try:
            sd_card = sdcardio.SDCard(ArgusV1Components.SD_CARD_SPI,
                                      ArgusV1Components.SD_CARD_CS,
                                      ArgusV1Components.SD_BAUD)
            self._sd_card = sd_card
            self.append_device(sd_card)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.SDCARD_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def _burn_wire_boot(self) -> int:
        """burn_wire_boot: Boot sequence for the burn wires
        """
        try:
            burn_wires = burnwire.BurnWires(ArgusV1Components.BURN_WIRE_ENABLE,
                                            ArgusV1Components.BURN_WIRE_XP,
                                            ArgusV1Components.BURN_WIRE_XM,
                                            ArgusV1Components.BURN_WIRE_YP,
                                            ArgusV1Components.BURN_WIRE_YM)
            
            if self.__middleware_enabled:
                burn_wires = Middleware(burn_wires, burn_wire_fatal_exception)
            
            self._burn_wires = burn_wires
            self.append_device(burn_wires)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.BURNWIRES_NOT_INITIALIZED
        
        return Diagnostics.NOERROR
    
    def _jetson_boot(self) -> int:
        """jetson_boot: Boot sequence for the Jetson
        """
        try:
            jetson = Middleware(ArgusV1Components.JETSON_UART, jetson_fatal_exception)
            self._jetson = jetson
            self.append_device(jetson)
        except Exception as e:
            if not self.__middleware_enabled:
                raise e
            if self.__debug:
                print(e)
                
            return Diagnostics.JETSON_NOT_INITIALIZED
        
        return Diagnostics.NOERROR

    ######################## DIAGNOSTICS ########################
    def __get_device_diagnostic_error(self, device) -> int:
        """__get_device_diagnostic_error: Get the error code for a device that failed to initialize
        """
        if isinstance(device, Middleware): # Convert device to the wrapped instance
            device = device.get_instance()

        if device is self.RTC:
            return Diagnostics.DIAGNOSTICS_ERROR_RTC
        elif device is self.GPS:
            return Diagnostics.DIAGNOSTICS_ERROR_GPS
        elif device is self.BATTERY_POWER_MONITOR:
            return Diagnostics.DIAGNOSTICS_ERROR_BATTERY_POWER_MONITOR
        elif device is self.JETSON_POWER_MONITOR:
            return Diagnostics.DIAGNOSTICS_ERROR_JETSON_POWER_MONITOR
        elif device is self.IMU:
            return Diagnostics.DIAGNOSTICS_ERROR_IMU
        elif device is self.CHARGER:
            return Diagnostics.DIAGNOSTICS_ERROR_CHARGER
        elif device is self.TORQUE_XP:
            return Diagnostics.DIAGNOSTICS_ERROR_TORQUE_XP
        elif device is self.TORQUE_XM:
            return Diagnostics.DIAGNOSTICS_ERROR_TORQUE_XM
        elif device is self.TORQUE_YP:
            return Diagnostics.DIAGNOSTICS_ERROR_TORQUE_YP
        elif device is self.TORQUE_YM:
            return Diagnostics.DIAGNOSTICS_ERROR_TORQUE_YM
        elif device is self.TORQUE_Z:
            return Diagnostics.DIAGNOSTICS_ERROR_TORQUE_Z
        elif device is self.SUN_SENSOR_XP:
            return Diagnostics.DIAGNOSTICS_ERROR_SUN_SENSOR_XP
        elif device is self.SUN_SENSOR_XM:
            return Diagnostics.DIAGNOSTICS_ERROR_SUN_SENSOR_XM
        elif device is self.SUN_SENSOR_YP:
            return Diagnostics.DIAGNOSTICS_ERROR_SUN_SENSOR_YP
        elif device is self.SUN_SENSOR_YM:
            return Diagnostics.DIAGNOSTICS_ERROR_SUN_SENSOR_YM
        elif device is self.SUN_SENSOR_ZP:
            return Diagnostics.DIAGNOSTICS_ERROR_SUN_SENSOR_ZP
        elif device is self.SUN_SENSOR_ZM:
            return Diagnostics.DIAGNOSTICS_ERROR_SUN_SENSOR_ZM
        elif device is self.RADIO:
            return Diagnostics.DIAGNOSTICS_ERROR_RADIO
        elif device is self.NEOPIXEL:
            return Diagnostics.DIAGNOSTICS_ERROR_NEOPIXEL
        elif device is self.BURN_WIRES:
            return Diagnostics.DIAGNOSTICS_ERROR_BURN_WIRES
        else:
            return Diagnostics.DIAGNOSTICS_ERROR_UNKNOWN

    def run_system_diagnostics(self) -> list[int] | None:
        """run_diagnostic_test: Run all diagnostics across all components

        :return: A list of error codes if any errors are present
        """
        error_list: list[int] = []

        for device in self.device_list:
            try:
                # Enable the devices that are resetable
                if device.resetable:
                    device.enable()
                    
                # Concancate the error list from running diagnostics
                error_list += device.run_diagnostics()

                # Disable the devices that are resetable
                if device.resetable:
                    device.disable()
            except Exception:
                error_list.append(self.__get_device_diagnostic_error(device))
                continue 

        error_list = [err for err in error_list if err != Diagnostics.NOERROR]
        error_list = list(set(error_list)) # Remove duplicate errors

        self._recent_errors = error_list

        return error_list
    

