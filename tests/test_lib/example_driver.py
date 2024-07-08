from hal.drivers.middleware.generic_driver import Driver  # noqa: E402


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
        self.__test_str = "test"
        self.update_int = 0
        self.__property = 89

        super().__init__()

        self.handleable = {
            "get_test_int": (self.int_checker, TestException),
            "set_test_int": (lambda x, y: True, TestException),
            "test_method": (lambda x, y: x, TestException),
        }

    def get_test_int(self) -> int:
        if self.flags & 0b001:
            # best we can do is try again
            raise TestException("Critical Error")
        if self.flags & 0b010:
            raise TestException("Fixable Error")
        return self.int_val

    def set_test_int(self, input: int) -> None:
        self.int_val = input

    def get_test_str(self) -> int:
        return self.__test_str

    def set_test_str(self, input: str) -> None:
        self.__test_str = input

    def int_checker(self, result, flags):
        if "hidden" in flags:
            return False
        if result > 9:
            return False
        return True

    def test_method(self):
        self.update_int += 1
        return 9

    def unhandled_method(self, num):
        return num + 1

    def get_flags(self):
        res = {}
        if self.flags & 0b100:
            res["hidden"] = self.fixer
        if self.flags & 0b010:
            # fixable flag is raised
            res["fixable"] = self.fixer
        if self.flags & 0b001:
            # critical flag is raised
            res["critical"] = None
        return res

    def fixer(self):
        # remove the fixable flag
        self.flags = self.flags & 0b001
