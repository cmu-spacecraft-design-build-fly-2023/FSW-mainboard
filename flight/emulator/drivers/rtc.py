from time import struct_time

class RTC:
    def __init__(self, date_input: struct_time) -> None:
        self.datetime = date_input

    @property
    def datetime(self):
        return self.datetime
    
    @datetime.setter
    def datetime(self, date_input:struct_time):
        self.datetime = date_input