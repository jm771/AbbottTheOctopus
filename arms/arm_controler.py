# From testing - this is the range in which the servo actually moves
MIN_DUTY = 0x600
MAX_DUTY = 0x2800

DUTY_RANGE = MAX_DUTY - MIN_DUTY


class ArmController:
    def __init__(self, channel, invert: bool):
        self._channel = channel
        self._invert = invert

    # 0 is bottomed out, 1 as high as possible
    def set_pos(self, pos: float):
        duty_int = round(pos * DUTY_RANGE)
        # print(f"{duty_int:x}")
        if self._invert:
            self._channel.duty_cycle = MAX_DUTY - duty_int
        else:
            self._channel.duty_cycle = MIN_DUTY + duty_int


class StubArmController:
    def set_pos(self, pos: float):
        pass


def make_arm_controllers():
    try:
        import board
        import busio
        from adafruit_pca9685 import PCA9685

        i2c = board.I2C()
        pca = PCA9685(i2c)
        pca.frequency = 60
        return [
            ArmController(pca.channels[0], False),
            ArmController(pca.channels[1], True),
        ]
    except NotImplementedError, ImportError:
        print("No hardware detected, using stub arm controllers")
        return [StubArmController(), StubArmController()]
