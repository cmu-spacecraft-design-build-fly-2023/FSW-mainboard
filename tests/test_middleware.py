import sys

import pytest
from tests.test_lib.example_driver import TestDevice, TestException


sys.path.insert(0, "./emulator/drivers/")
from hal.drivers.middleware.middleware import Middleware  # noqa: E402

"""
setting up things for an emulated test
"""


class TestClass:
    def test_method_call(self):
        device = TestDevice(0)
        mid = Middleware(device)

        # test normal handled method
        assert mid.get_test_int() == device.get_test_int()
        assert mid.get_test_int() == 8

        # test handled method with side effects
        assert mid.test_method() == 9
        assert mid.test_method() == device.test_method()
        assert mid.update_int == 3

        # test unhandled method
        assert mid.unhandled_method(9) == 10
        assert mid.unhandled_method(1) == device.unhandled_method(1)

    def test_method_setters(self):
        # test handled property test_int
        device = TestDevice(0)
        mid = Middleware(device)
        assert mid.get_test_int() == 8
        assert device.get_test_int() == 8
        mid.set_test_int(5)
        assert mid.get_test_int() == 5
        assert device.get_test_int() == 5

        # test unhandled property test_str
        assert mid.get_test_str() == "test"
        mid.set_test_str("testing")
        assert mid.get_test_str() == "testing"
        assert device.get_test_str() == "testing"

    def test_exceptions(self):
        """
        This test ensures that the middleware can call the flag fixer functions in order to
        get a correct result from the device.
        """
        device = TestDevice(0b010)
        mid = Middleware(device)
        with pytest.raises(TestException):
            device.get_test_int()
        assert mid.get_test_int() == 8

        device = TestDevice(0b100)
        mid = Middleware(device)
        assert mid.get_test_int() == 8

        device = TestDevice(0b001)
        mid = Middleware(device)
        with pytest.raises(TestException):
            mid.get_test_int()
