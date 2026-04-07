import time
import busio
import digitalio
from board import SCK, MOSI, MISO, D25, D8, D27


from adafruit_rgb_display import color565
from adafruit_rgb_display.gc9a01a import GC9A01A


# Configuration for CS and DC pins:
CS_PIN = D8
DC_PIN = D25
print(SCK, MOSI, CS_PIN, DC_PIN)

# Setup SPI bus using hardware SPI:
spi = busio.SPI(clock=SCK, MOSI=MOSI) #, MISO=MISO)

# Create the ILI9341 display:
display = GC9A01A(spi, cs=digitalio.DigitalInOut(CS_PIN),
                          dc=digitalio.DigitalInOut(DC_PIN))

# Main loop:
while True:
    # Clear the display
    display.fill(0)
    # Draw a red pixel in the center.
    display.pixel(120, 160, color565(255, 0, 0))
    # Pause 2 seconds.
    time.sleep(2)
    # Clear the screen blue.
    display.fill(color565(0, 0, 255))
    # Pause 2 seconds.
    time.sleep(2)


