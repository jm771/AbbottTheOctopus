from adafruit_pca9685 import PCA9685
from time import sleep
import board
import busio

# Create the I2C bus interface.
i2c = busio.I2C(board.SCL, board.SDA)  # uses board.SCL and board.SDA

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)

# Set the PWM frequency to 60hz.
pca.frequency = 60

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.

MAX_DUTY = 0xFFFF

# From testing - this is the range in which the servo actually moves
MIN_DUTY = 0x600
MAX_DUTY = 0x2800

# But this is more than the range required to fully actuate the octopus tentcle
MAX_OCTOPUS_REACH = 0x2000
# MAX_DUTY = MIN_DUTY + MAX_OCTOPUS_REACH


duty = MIN_DUTY
while True:
    # print(f"{duty:x}")
    pca.channels[0].duty_cycle = duty
    pca.channels[1].duty_cycle = duty
    sleep(0.05)
    duty += 0x100
    if duty > MAX_DUTY:
        duty = MIN_DUTY
