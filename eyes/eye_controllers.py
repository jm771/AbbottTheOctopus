
import busio
import digitalio
from board import SCK, MOSI, D25, D8


from adafruit_rgb_display.gc9a01a import GC9A01A

def make_left_eye_display():
    # Configuration for CS and DC pins:
    CS_PIN = D8
    DC_PIN = D25

    # This is pysically connected but unused - seller says we have to assert RST but I guess we get away with not for now
    RST_PIN = D27

    spi = busio.SPI(clock=SCK, MOSI=MOSI)

    display = GC9A01A(spi, cs=digitalio.DigitalInOut(CS_PIN),
                            dc=digitalio.DigitalInOut(DC_PIN))
    
    return display

def make_right_eye_display():
    # Configuration for CS and DC pins:
    CS_PIN = D8
    DC_PIN = D25

    # This is pysically connected but unused - seller says we have to assert RST but I guess we get away with not for now
    RST_PIN = D27

    spi = busio.SPI(clock=SCK, MOSI=MOSI)

    display = GC9A01A(spi, cs=digitalio.DigitalInOut(CS_PIN),
                            dc=digitalio.DigitalInOut(DC_PIN))
    
    return display