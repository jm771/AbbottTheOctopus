from adafruit_pca9685 import PCA9685
from time import sleep
import board
import busio

# From testing - this is the range in which the servo actually moves
MIN_DUTY = 0x600
MAX_DUTY = 0x2800

DUTY_RANGE = MAX_DUTY - MIN_DUTY

class ArmController:
    def __init__(self, channel, invert: bool):
        self._channel = channel

    # 0 is bottomed out, 1 as high as possible
    def set_pos(self, pos: float):
        duty_int = round(pos * DUTY_RANGE)
        if self.invert:
            self._channel.duty_cycle = MAX_DUTY - duty_int
        else:
            self._channel.duty_cycle = MIN_DUTY + duty_int



def make_arm_controllers():
    i2c = busio.I2C()
    pca = PCA9685(i2c)
    pca.frequency = 60

    left_arm = ArmController(pca.channels[0], False)
    right_arm = ArmController(pca.channels[1], True)
    return [left_arm, right_arm]
