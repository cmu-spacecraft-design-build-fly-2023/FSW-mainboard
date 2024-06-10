class IMU:
    def __init__(self, accel, mag, gyro, temp) -> None:
        self.__accel = accel
        self.__mag = mag
        self.__gyro = gyro
        self.__temp = temp

    @property
    def accel(self):
        return self.__accel
    
    @property
    def mag(self):
        return self.__mag
    
    @property
    def gyro(self):
        return self.__gyro
    
    @property
    def temp(self):
        return self.__temp