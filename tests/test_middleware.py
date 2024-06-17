import sys

import pytest

sys.path.insert(0, "./emulator/drivers/")
from middleware.generic_driver import Driver  # noqa: E402
from middleware.middleware import Middleware  # noqa: E402

"""
setting up things for an emulated test
"""


class TestException(Exception):
    def __init__(self, exception: Exception):
        self.exception = exception
        super().__init__()

    def __str__(self):
        return f"{type(self.exception).__name__}: {self.exception}"


class TestDevice(Driver):
    def __init__(self, flags: int):
        """
        flags: 2 bit flag register
            - 0: ciritcal error
            - 1: fixable error
            - 2: fixable, hidden error
        """
        self.flags = flags
        self.int_val = 8
        self.update_int = 0

        super().__init__()

        self.handleable = {
            'test_int': (True, self.int_checker, TestException),
            'test_method': (False, lambda x, y: x, TestException)
        }

    @property
    def test_int(self) -> int:
        if self.flags & 0b001:
            # best we can do is try again
            raise TestException("Critical Error")
        if self.flags & 0b010:
            raise TestException("Fixable Error")
        return self.int_val

    @test_int.setter
    def test_int(self, input: int) -> None:
        self.int_val = input

    def int_checker(self, result, flags):
        if 'fixable' in flags:
            # fixable has occured
            raise TestException("Fixable Error")
        if 'hidden' in flags:
            raise TestException("Hidden Error")
        if result > 9:
            raise TestException("Erroneous Result")
        return result

    def test_method(self):
        self.update_int += 1
        return 9

    @property
    def get_flags(self):
        res = {}
        if self.flags & 0b100:
            res['hidden'] = self.fixer
        if self.flags & 0b010:
            # fixable flag is raised
            res['fixable'] = self.fixer
        if self.flags & 0b001:
            # critical flag is raised
            res['critical'] = None
        return res

    def fixer(self):
        # remove the fixable flag
        self.flags = self.flags & 0b001


class TestClass:
    def test_method_call(self):
        device = TestDevice(0b00)
        mid = Middleware(device)
        assert mid.test_method() == device.test_method()
        assert mid.update_int == 2

    def test_property_call(self):
        device = TestDevice(0b00)
        mid = Middleware(device)
        assert mid.test_int == 8
        mid.test_int = 5
        assert mid.test_int == 5

    def test_exceptions(self):
        """
        This test ensures that the middleware can call the flag fixer functions in order to
        get a correct result from the device.
        """
        device = TestDevice(0b010)
        mid = Middleware(device)
        with pytest.raises(TestException):
            device.test_int
        assert mid.test_int == 8

        device = TestDevice(0b100)
        mid = Middleware(device)
        assert mid.test_int == 8

        device = TestDevice(0b001)
        mid = Middleware(device)
        with pytest.raises(TestException):
            mid.test_int
