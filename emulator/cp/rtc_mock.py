from time import gmtime, struct_time


class RTC:
    def __init__(self) -> None:
        self._datetime = gmtime()

    def datetime(self):
        return self._datetime

    def set_datetime(self, date_input: struct_time):
        self._datetime = date_input
