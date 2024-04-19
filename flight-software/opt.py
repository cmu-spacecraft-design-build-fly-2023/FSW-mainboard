from hal.drivers.opt4001 import OPT4001
import board, busio

I2C_ADDRESS = 0x44
I2C = busio.I2C(board.SCL2, board.SDA2)

opt = OPT4001(I2C, I2C_ADDRESS)