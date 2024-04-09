import drv8830
from micropython import const
import board
import busio
from hal.drivers.middleware.middleware import *
from hal.drivers.middleware.exceptions import *

class TorqueCoilInterfaces:
    I2C2_SDA    = board.SDA2
    I2C2_SCL    = board.SCL2
    I2C2        = busio.I2C(I2C2_SCL, I2C2_SDA)

class TorqueCoilComponents:
    
    # TORQUE COIL I2C
    TORQUE_COILS_I2C                        = TorqueCoilInterfaces.I2C2
    TORQUE_XP_I2C_ADDRESS                   = const(0xC0)
    TORQUE_XM_I2C_ADDRESS                   = const(0xC2)
    TORQUE_YP_I2C_ADDRESS                   = const(0xC4)
    TORQUE_YM_I2C_ADDRESS                   = const(0xC6)
    TORQUE_Z_I2C_ADDRESS                    = const(0xC8)

class TorqueCoil:
    """
    A class to manage DRV8830 motor drivers together based on input, i.e. X, Y, Z
    """

    def __init__(self, panel, middleware_enable):
        """
        Initializes DRV8830 instances for the input panels
        """
        self.panel = panel
        self.__middleware_enabled = middleware_enable
        self.torque = None
        
    def torque_boot(self):
        if self.panel == 'X':
            torque = self.torque_x_boot()
        elif self.panel == 'Y':
            torque = self.torque_y_boot()
        elif self.panel == 'Z':
            torque = self.torque_z_boot()
        else:
            raise ValueError("Wrong Value for Panel input") 
        
        return torque

    def torque_x_boot(self):
        """torque_xp_boot: Boot sequence for the torque driver in both x directions

        :return: list of torques if the torque driver initialized
        empty list if the torque driver failed to initialize
        """
        try:
            torque_xp = drv8830.DRV8830(TorqueCoilComponents.TORQUE_COILS_I2C,
                                        TorqueCoilComponents.TORQUE_XP_I2C_ADDRESS)
            torque_xm = drv8830.DRV8830(TorqueCoilComponents.TORQUE_COILS_I2C,
                                        TorqueCoilComponents.TORQUE_XM_I2C_ADDRESS)
            if self.__middleware_enabled:
                torque_xp = Middleware(torque_xp, torque_xp_fatal_exception)
                torque_xm = Middleware(torque_xm, torque_xm_fatal_exception)

            return [torque_xp, torque_xm]
            
        except Exception:
            return []

    def torque_y_boot(self):
        """torque_xp_boot: Boot sequence for the torque driver in both x directions

        :return: list of torques if the torque driver initialized
        empty list if the torque driver failed to initialize
        """
        try:
            torque_yp = drv8830.DRV8830(TorqueCoilComponents.TORQUE_COILS_I2C,
                                        TorqueCoilComponents.TORQUE_YP_I2C_ADDRESS)
            torque_ym = drv8830.DRV8830(TorqueCoilComponents.TORQUE_COILS_I2C,
                                        TorqueCoilComponents.TORQUE_YM_I2C_ADDRESS)
            if self.__middleware_enabled:
                torque_yp = Middleware(torque_yp, torque_yp_fatal_exception)
                torque_ym = Middleware(torque_ym, torque_ym_fatal_exception)

            return [torque_yp, torque_ym]
            
        except Exception:
            return []
        
    def torque_z_boot(self):
        """torque_xp_boot: Boot sequence for the torque driver in both x directions

        :return: list of torques if the torque driver initialized
        empty list if the torque driver failed to initialize
        """
        try:
            torque_z = drv8830.DRV8830(TorqueCoilComponents.TORQUE_COILS_I2C,
                                       TorqueCoilComponents.TORQUE_Z_I2C_ADDRESS)
            if self.__middleware_enabled:
                torque_z = Middleware(torque_z, torque_z_fatal_exception)

            return [torque_z]
            
        except Exception:
            return []