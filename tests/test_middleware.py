import sys

# sys.path.insert(0, './flight-software/hal/drivers/middleware')
sys.path.insert(0, "./emulator/drivers/")

from middleware.middleware import Middleware
from middleware.generic_driver import Driver

"""
setting up things for an emulated test
"""


class TestException(Exception):
    def __init__(self, exception: Exception):
        self.exception = exception
        super().__init__()

    def __str__(self):
        return f"{type(self.exception).__name__}: {self.exception}"


class TestClass(Driver):
    def __init__(self, flags: int):
        """
        flags: 2 bit flag register
            - 0: ciritcal error
            - 1: fixable error
        """
        self.flags = flags
        self.int_val = 8

        super.__init__()

        self.handleable = {
            'test_int': (self.int_checker, TestException)
        }

    @property
    def test_int(self) -> int:
        if self.flags & 0b01:
            # best we can do is try again
            raise TestException("Critical Error")
        return self.int_val
    
    @test_int.setter
    def test_int(self, input: int) -> None:
        self.int_val = input

    def int_checker(self, result, flags):
        if flags & 0b10:
            # fixable has occured
            raise TestException("Fixable Error")
        if result > 9:
            raise TestException("Erroneous Result")
        return result

    @property
    def get_flags(self):
        res = {}
        if self.flags & 0b10:
            # fixable flag is raised
            res['fixable'] = self.fixer
        if self.flags & 0b01:
            # critical flag is raised
            res['critical'] = self.retry
        return res

    def fixer(self):
        # remove the fixable flag
        self.flags = self.flags & 0b01
