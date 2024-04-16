from drv8830 import DRV8830
import board
import busio

# TorqueCoil Management Class
class TorqueInterface:
    """Manage torque for dual or single DRV8830 motor controllers."""
    
    def __init__(self, drv1, drv2=None):
        """
        Initialize the TorqueInterface with one or two DRV8830 instances.
        
        :param drv1: The first DRV8830 instance (required).
        :param drv2: The second DRV8830 instance (optional).
        """
        self.drv1 = drv1
        self.drv2 = drv2
    
    def set_torque(self, throttle):
        """
        Set the torque level on the motor(s). This sets the throttle on one or two DRV8830s.
        
        :param throttle: Throttle value from -1.0 (full reverse) to +1.0 (full forward).
        """
        self.drv1.throttle = throttle
        if self.drv2 is not None:
            self.drv2.throttle = throttle

    def enable_torque_coil(self, enable=True):
        """
        Enable or disable the torque coil. This effectively enables or disables the motor output.
        
        :param enable: Boolean flag to either enable (True) or disable (False) the torque.
        """
        if enable:
            self.drv1.throttle = 1.0  # Set to full speed forward for demonstration
            if self.drv2 is not None:
                self.drv2.throttle = 1.0
        else:
            self.drv1.throttle = None  # Set to None for high-impedance (coast)
            if self.drv2 is not None:
                self.drv2.throttle = None