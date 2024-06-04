"""
Payload: Payload uart driver for the ARGUS-1 CubeSat

This module provides a driver for the payload uart on the ARGUS-1 CubeSat. The
payload uart is used to communicate with the payload board. The driver provides
methods to send and receive data over the uart.

Author(s): Harry Rosmann
"""

from .diagnostics.diagnostics import Diagnostics
from digitalio import DigitalInOut

class PayloadUART(Diagnostics):
    """Payload: Payload uart driver for the ARGUS-1 CubeSat"""

    def __init__(self, uart, enable_pin):
        self.__uart = uart

        self.__enable = DigitalInOut(enable_pin)
        self.__enable.switch_to_output(value=True)

        self.handler_methods = {}

        super().__init__(self.__enable)

    def write(self, bytes: bytearray) -> None:
        self.__uart.write(bytes)

    def read(self, num_bytes: int) -> bytearray:
        return self.__uart.read(num_bytes)

    def in_waiting(self) -> int:
        return self.__uart.in_waiting
    
    def reset_input_buffer(self) -> None:
        self.__uart.reset_input_buffer()

    def run_diagnostics(self) -> list[int] | None:
        """run_diagnostic_test: Run all tests for the component"""
        return [Diagnostics.NOERROR]